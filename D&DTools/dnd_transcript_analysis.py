"""
D&D Zoom Transcript Analysis Tools
====================================
Analyzes Zoom meeting transcripts from D&D sessions to extract:
  - Dialog share per player (with DM lines removable)
  - Silence-breaking patterns (who speaks after gaps)
  - Roll results: attacks, saves, skill checks, initiative, nat 20s/1s
  - Dirty 20s

Built from analysis of Jeff Hay's campaign sessions (Avernus / Von / Folklore).
Tuned for this specific table's vocabulary — "dirty 20", "plus math", etc.

Usage:
    Load transcript items from Zoom meeting assets JSON files, then call
    the analysis functions. See each function's docstring for details.

Transcript item format (from Zoom get_meeting_assets):
    {"text": "Speaker Name: What they said.", "start": "00:01:23.000", "end": "00:01:25.000"}

Campaign DM mapping (update as campaigns change):
    AVERNUS sessions  → DM is Jeff
    VON sessions      → DM is Cindy
    FOLKLORE sessions → DM is Jeff
"""

import re
from collections import defaultdict


# ---------------------------------------------------------------------------
# Player name normalization
# ---------------------------------------------------------------------------

def normalize_speaker(raw_speaker: str) -> str:
    """
    Map Zoom display names (including character names in parens) to real player names.
    Update this as your table changes.
    """
    s = raw_speaker.lower()
    if 'jeff' in s:                                             return 'Jeff'
    if 'cindy' in s:                                            return 'Cindy'
    if 'litza' in s:                                            return 'Litza'
    if 'mila' in s or 'amelia' in s:                           return 'Mila'
    if 'ryan' in s or 'coach' in s:                            return 'Ryan'
    if 'wyatt' in s:                                            return 'Wyatt'
    if 'nate' in s:                                             return 'Nate'
    # Stephanie logs in as various character names from other games
    if any(x in s for x in ['vyen', 'jo m', 'claire', 'sloane']): return 'Stephanie'
    return raw_speaker  # unknown — return as-is


def parse_transcript(transcript_items: list) -> list:
    """
    Parse raw Zoom transcript items into (player, line, start_sec, end_sec) tuples.
    Skips items with no colon (no speaker attribution).
    """
    parsed = []
    for item in transcript_items:
        text = item.get('text', '')
        if ':' not in text:
            continue
        raw_speaker = text.split(':')[0].strip()
        player = normalize_speaker(raw_speaker)
        line = ':'.join(text.split(':')[1:]).strip()
        start = _ts_to_seconds(item.get('start', '0'))
        end   = _ts_to_seconds(item.get('end',   '0'))
        parsed.append({'player': player, 'line': line, 'start': start, 'end': end})
    return parsed


def _ts_to_seconds(ts: str) -> float:
    """Convert HH:MM:SS.mmm timestamp to seconds."""
    try:
        parts = ts.replace(',', '.').split(':')
        h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# Dialog share analysis
# ---------------------------------------------------------------------------

def dialog_share(parsed: list, dm: str = None) -> dict:
    """
    Count transcript lines per player and return percentage share.

    Args:
        parsed:  Output of parse_transcript()
        dm:      If provided, exclude this player's lines from the denominator
                 (returns player-only percentages).

    Returns:
        Dict of {player: {'count': int, 'pct': float}}
        sorted by count descending.
    """
    counts = defaultdict(int)
    for item in parsed:
        if dm and item['player'] == dm:
            continue
        counts[item['player']] += 1

    total = sum(counts.values())
    if total == 0:
        return {}

    return dict(sorted(
        {p: {'count': c, 'pct': round(c / total * 100, 1)} for p, c in counts.items()}.items(),
        key=lambda x: -x[1]['count']
    ))


# ---------------------------------------------------------------------------
# Silence-breaking analysis
# ---------------------------------------------------------------------------

def silence_breakers(parsed: list, threshold_seconds: float = 10.0, dm: str = None) -> dict:
    """
    Find gaps > threshold_seconds between transcript lines and count who speaks first.

    Args:
        parsed:            Output of parse_transcript()
        threshold_seconds: Minimum gap to count as "silence" (default 10s)
        dm:                If provided, also returns player-only breakdown excluding DM

    Returns:
        {
          'all':    {player: {'breaks': int, 'pct': float, 'avg_gap': float}},
          'no_dm':  {player: ...}  (only if dm provided),
          'total_silences': int,
          'avg_gap': float,
          'longest_gap': float,
        }
    """
    all_breaks  = defaultdict(list)  # player -> [gap_lengths]
    nodm_breaks = defaultdict(list)

    for i in range(1, len(parsed)):
        gap = parsed[i]['start'] - parsed[i-1]['end']
        if gap > threshold_seconds:
            p = parsed[i]['player']
            all_breaks[p].append(gap)
            if p != dm:
                nodm_breaks[p].append(gap)

    all_gaps = [g for gaps in all_breaks.values() for g in gaps]
    total    = len(all_gaps)

    def summarize(breaks_dict):
        t = sum(len(v) for v in breaks_dict.values())
        return dict(sorted({
            p: {
                'breaks':   len(gaps),
                'pct':      round(len(gaps) / t * 100, 1) if t else 0,
                'avg_gap':  round(sum(gaps) / len(gaps), 1),
            }
            for p, gaps in breaks_dict.items()
        }.items(), key=lambda x: -x[1]['breaks']))

    result = {
        'total_silences': total,
        'avg_gap':        round(sum(all_gaps) / total, 1) if all_gaps else 0,
        'longest_gap':    round(max(all_gaps), 1) if all_gaps else 0,
        'all':            summarize(all_breaks),
    }
    if dm:
        result['no_dm'] = summarize(nodm_breaks)
    return result


# ---------------------------------------------------------------------------
# Roll result extraction
# ---------------------------------------------------------------------------

# Ability save types (including common Zoom transcription errors like "deck" for "dex")
_SAVE_TYPES  = r'(?:strength|dexterity|dex|deck|constitution|con|intelligence|int|wisdom|wis|charisma|cha)'
_SKILL_TYPES = (
    r'(?:perception|insight|investigation|athletics|stealth|persuasion|deception|'
    r'intimidation|arcana|history|nature|religion|medicine|survival|acrobatics|'
    r'performance|animal\s+handling|sleight\s+of\s+hand)'
)

# Initiative call patterns (from DM)
_INIT_CALL = re.compile(
    r'\broll\s+initiative\b|\binitiative[,\s]+roll\b|give me.*initiative'
    r'|let\'?s.*initiative|want to roll initiative',
    re.I
)

# Roll category patterns: (regex, category, min_val, max_val)
# Ordered most-specific first; first match wins per span.
_ROLL_PATTERNS = [
    # Initiative — explicit
    (re.compile(r'\b(\d+)\s+(?:on\s+(?:my\s+)?)?initiative\b'),          'initiative', 1, 30),
    (re.compile(r'\binitiative[^.]{0,20}?\b(\d+)\b'),                     'initiative', 1, 30),
    # Saves
    (re.compile(r'\b(\d+)\s+on\s+(?:my\s+|the\s+)?(?:save|saving throw)\b'), 'save', 1, 40),
    (re.compile(r'\b(\d+)[^.]{0,20}?' + _SAVE_TYPES + r'\s+sav(?:e|ing)'), 'save', 1, 40),
    (re.compile(_SAVE_TYPES + r'\s+sav(?:e|ing)[^.]{0,20}?(\d+)'),        'save', 1, 40),
    # Skill checks
    (re.compile(r'\b(\d+)\s+on\s+(?:my\s+|the\s+|a\s+)?' + _SKILL_TYPES), 'skill_check', 1, 40),
    (re.compile(_SKILL_TYPES + r'[^.]{0,15}?(\d+)\b'),                    'skill_check', 1, 40),
    (re.compile(r'\b(\d+)[^.]{0,10}?' + _SKILL_TYPES),                    'skill_check', 1, 40),
    # Attacks
    (re.compile(r'\b(\d+)\s+to\s+hit\b'),                                 'attack',      1, 45),
    (re.compile(r'\bdirty\s+(\d+)\b'),                                     'attack',      1, 40),
    # Generic roll reports (fallback)
    (re.compile(r'\broll(?:ed|ing)?\s+a?\s*(\d+)\b'),                     'roll',        1, 40),
    (re.compile(r'\bthat\'?s?\s+(?:going\s+to\s+be\s+)?a\s+(\d+)\b'),    'roll',        1, 40),
    (re.compile(r'\bis\s+(?:only\s+)?a\s+(\d+)\b'),                       'roll',        1, 40),
    (re.compile(r'\bi\s+got\s+a?\s*(\d+)\b'),                             'roll',        4, 40),
    (re.compile(r'\b(\d+)\s+plus\s+math\b'),                               'roll',        1, 30),
]

# Nat 20 / nat 1 / crit patterns (fixed value, no capture group needed)
_SPECIAL_PATTERNS = [
    (re.compile(r'\bnat(?:ural)?\s*20\b'),                          20, 'nat20'),
    (re.compile(r'\bnat(?:ural)?\s*1\b'),                            1, 'nat1'),
    (re.compile(r'\b(?:i|i\'ve|i\s+just)\s+crit(?:ted)?\b'),       20, 'crit'),
    (re.compile(r'\bi\s+got\s+a\s+crit\b'),                         20, 'crit'),
    (re.compile(r'\bthat\'?s?\s+a\s+crit\b'),                       20, 'crit'),
    (re.compile(r'\b(?:i\s+)?crit(?:ical)?\s*fail\b'),               1, 'crit_fail'),
]


def extract_rolls(parsed: list) -> list:
    """
    Extract all roll results from parsed transcript lines.

    Handles:
    - Categorized totals: attacks ("19 to hit"), saves, skill checks, initiative
    - Generic roll reports: "rolled a 14", "that's a 22", "I got a 17"
    - Nat 20s, nat 1s, crits, crit fails
    - Initiative windows: bare numbers after "roll initiative" call
    - Table-specific idioms: "dirty 20", "plus math"

    Returns list of dicts:
        {
          'player':   str,
          'value':    int,
          'category': str,   # 'attack'|'save'|'skill_check'|'initiative'|'roll'|'nat20'|'nat1'|'crit'|'crit_fail'
          'is_nat':   bool,  # True for nat20/nat1/crit/crit_fail
        }
    """
    results = []
    init_window = 0  # lines remaining in initiative call window

    for i, item in enumerate(parsed):
        line      = item['line']
        line_low  = line.lower()
        player    = item['player']

        # Check for initiative call (resets window)
        if _INIT_CALL.search(line_low):
            init_window = 20
            continue

        matched_spans = []

        # --- Specials: nat20 / nat1 / crit ---
        for pat, val, kind in _SPECIAL_PATTERNS:
            for m in pat.finditer(line_low):
                if _overlaps(m, matched_spans): continue
                matched_spans.append((m.start(), m.end()))
                results.append({'player': player, 'value': val, 'category': kind, 'is_nat': True})

        # --- Initiative window: bare numbers ---
        if init_window > 0:
            init_window -= 1
            m = re.search(r'\b(\d+)\s+(?:for\b|on\s+(?:my\s+)?initiative)', line_low)
            if not m:
                # Bare number line
                m2 = re.search(r'^(\d+)\s*[.,!]?\s*$', line.strip())
                if m2:
                    val = int(m2.group(1))
                    if 1 <= val <= 30 and not _overlaps_range(0, len(line_low), matched_spans):
                        matched_spans.append((0, len(line_low)))
                        results.append({'player': player, 'value': val, 'category': 'initiative', 'is_nat': False})
            if m and not _overlaps(m, matched_spans):
                val = int(m.group(1))
                if 1 <= val <= 30:
                    matched_spans.append((m.start(), m.end()))
                    results.append({'player': player, 'value': val, 'category': 'initiative', 'is_nat': False})

        # --- Category patterns ---
        for pat, cat, min_v, max_v in _ROLL_PATTERNS:
            for m in pat.finditer(line_low):
                if _overlaps(m, matched_spans): continue
                try:
                    val = next(int(g) for g in m.groups() if g and g.isdigit())
                except StopIteration:
                    continue
                if not (min_v <= val <= max_v): continue
                matched_spans.append((m.start(), m.end()))
                results.append({'player': player, 'value': val, 'category': cat, 'is_nat': False})

    return results


def _overlaps(m, spans):
    return any(m.start() < e and m.end() > s for s, e in spans)

def _overlaps_range(start, end, spans):
    return any(start < e and end > s for s, e in spans)


# ---------------------------------------------------------------------------
# Summary helpers
# ---------------------------------------------------------------------------

def roll_summary(rolls: list) -> dict:
    """
    Summarize extracted rolls by category and per player.

    Returns:
        {
          'by_category': {cat: {'count': int, 'avg': float, 'min': int, 'max': int}},
          'by_player':   {player: {cat: {'count': int, 'avg': float}, 'nat20s': int, 'nat1s': int}},
          'nat20s': int,
          'nat1s':  int,
        }
    """
    by_cat    = defaultdict(list)
    by_player = defaultdict(lambda: defaultdict(list))
    nat20s = nat1s = 0

    for r in rolls:
        if r['is_nat']:
            if r['value'] == 20: nat20s += 1
            if r['value'] == 1:  nat1s  += 1
            # Count as separate tally, not in distributions
            by_player[r['player']]['_nat20s' if r['value'] == 20 else '_nat1s'].append(1)
        else:
            by_cat[r['category']].append(r['value'])
            by_player[r['player']][r['category']].append(r['value'])

    cat_summary = {}
    for cat, vals in sorted(by_cat.items(), key=lambda x: -len(x[1])):
        cat_summary[cat] = {
            'count': len(vals),
            'avg':   round(sum(vals) / len(vals), 1),
            'min':   min(vals),
            'max':   max(vals),
        }

    player_summary = {}
    for player, cats in by_player.items():
        player_summary[player] = {}
        for cat, vals in cats.items():
            if cat.startswith('_'):
                player_summary[player][cat.lstrip('_')] = len(vals)
            else:
                player_summary[player][cat] = {
                    'count': len(vals),
                    'avg':   round(sum(vals) / len(vals), 1),
                }

    return {
        'by_category': cat_summary,
        'by_player':   player_summary,
        'nat20s':      nat20s,
        'nat1s':       nat1s,
    }


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import json, sys

    if len(sys.argv) < 2:
        print("Usage: python dnd_transcript_analysis.py <meeting_assets.json> [dm_player_name]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        raw = json.load(f)

    # Handle both raw list (tool result format) and direct dict
    if isinstance(raw, list):
        data = json.loads(raw[0]['text'])
    else:
        data = raw

    transcript_items = data.get('meeting_transcript', {}).get('transcript_items', [])
    dm = sys.argv[2] if len(sys.argv) > 2 else None

    parsed = parse_transcript(transcript_items)
    print(f"Session: {data.get('topic', 'Unknown')}")
    print(f"Transcript lines: {len(parsed)}\n")

    print("=== Dialog share (all) ===")
    for player, stats in dialog_share(parsed).items():
        print(f"  {player:12s}: {stats['count']:4d} lines ({stats['pct']}%)")

    if dm:
        print(f"\n=== Dialog share (players only, DM={dm} excluded) ===")
        for player, stats in dialog_share(parsed, dm=dm).items():
            print(f"  {player:12s}: {stats['count']:4d} lines ({stats['pct']}%)")

    print("\n=== Silence breakers (>10s gaps) ===")
    sb = silence_breakers(parsed, threshold_seconds=10.0, dm=dm)
    print(f"  Total silences: {sb['total_silences']}  avg gap: {sb['avg_gap']}s  longest: {sb['longest_gap']}s")
    for player, stats in sb['all'].items():
        print(f"  {player:12s}: {stats['breaks']} breaks ({stats['pct']}%), avg gap {stats['avg_gap']}s")

    print("\n=== Roll results ===")
    rolls = extract_rolls(parsed)
    summary = roll_summary(rolls)
    print(f"  Nat 20s: {summary['nat20s']}  Nat 1s: {summary['nat1s']}")
    print("\n  By category:")
    for cat, stats in summary['by_category'].items():
        print(f"    {cat:15s}: n={stats['count']:3d}  avg={stats['avg']}  range={stats['min']}-{stats['max']}")
