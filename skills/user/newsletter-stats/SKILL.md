---
name: newsletter-stats
description: "Report on newsletter-digest skill.  When the user types `/newsletter-stats` (or asks \"how are my newsletters performing\", \"which newsletters should I cut\", etc.), query Airtable and produce a stats report."
---

## `/newsletter-stats` command

When the user types `/newsletter-stats` (or asks "how are my newsletters performing", "which newsletters should I cut", etc.), query Airtable and produce a stats report.

### What to pull
1. All records from **Newsletter Usage** (all runs)
2. All records from **Digest Runs** (for total run count and date range)

### Staleness filter — keep current stats meaningful
Before computing per-newsletter stats, determine "today" from the most recent Digest Runs date, then exclude any newsletter whose most recent appearance in Newsletter Usage (by the run's Date) is more than 14 days before that. A source that hasn't been fetched in over two weeks is either genuinely gone from the person's inbox or has stopped being relevant — including it stales the "never shown / rarely shown" and "underperformers" sections with sources that aren't really live candidates for a cut/keep decision anymore.

Report this filter's effect explicitly: list which sources were excluded as stale (name + last-seen date), separately from the sources excluded for genuinely underperforming while still active. Don't silently drop them — a source that vanished from the inbox entirely (e.g., an unsubscribe) is a different finding than one that's merely low-value, and the person may want to know both.

All other computations (Times Used, Avg Stories/Run, Total Stories, etc.) still use the newsletter's full history, not just the last 14 days — the staleness filter only controls which sources are *included* in the report, not how their historical numbers are calculated.

### Stats to compute and report
- **Total runs tracked** and date range (first → most recent)
- **Per-newsletter summary table**, sorted by Times Used (desc):

| Newsletter | Tier | Times Used | Avg Stories/Run | Total Stories | Content Quality (most common) | Sections most often |
|---|---|---|---|---|---|---|

- **Never shown / rarely shown:** newsletters in the source list that appear in 0 or very few runs. Flag these as candidates for removal.
- **Snippet-only problem sources:** newsletters with Content Quality = "Snippet only" in most/all runs. Flag as unreliable for full content.
- **Workhorses:** top 3–5 sources by total story count.
- **Underperformers:** sources present in ≥3 runs but averaging <1 story/run.

Format the report clearly. End with a brief editorial note on candidates to cut, candidates to promote, and any structural issues (e.g. persistent snippet-only problem).