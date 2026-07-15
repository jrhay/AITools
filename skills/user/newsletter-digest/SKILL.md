---
name: newsletter-digest
description: "Fetches and synthesizes newsletter emails from Gmail into a thematic daily digest. Use this skill whenever the user asks to summarize, digest, or catch up on their newsletters, emails from news sources, or daily briefings. Triggers include phrases like \"run my digest\", \"summarize my newsletters\", \"what did I miss today\", \"catch me up on my newsletters\", or \"newsletter digest\". Also triggers if the user mentions a specific time window like \"past 12 hours\" in relation to email or news. Always use this skill proactively when the user wants to process their newsletter inbox — don't just search Gmail manually without following this format."
---

# Newsletter Digest Skill

Produces a synthesized, thematic daily digest from the user's Gmail newsletter inbox — similar to a morning news briefing, organized by topic rather than by source.

## User context

- Based in Los Alamos, New Mexico
- Interested in: world/national news with broad impact, New Mexico state politics, Los Alamos local news, Technology/Automative/Gaming updates
- Preferred format: prose synthesis grouped by theme, not per-newsletter summaries
- When multiple sources cover the same story, note the overlap and any differences in framing

## Key newsletter sources to prioritize

**National/international:**
- Semafor Flagship — `flagship@semafor.com` — the primary Semafor edition; strongest international framing. Ignore all other Semafor sub-editions (DC, Gulf, Africa, Business, Media) if they appear in search results — their top stories are duplicated in the Flagship and they are consistently snippet-only.
- Axios (AM, PM, and topic editions) — `axios.com` / look for sender containing "axios"
- ProPublica (The Big Story and topic newsletters, irregular cadence) — `propublica.org` / look for sender containing "propublica"
- The Dispatch — `newsletter.thedispatch.com`
- Advisory Opinions  — `newsletter.scotusblog.com`
- The Bulwark — `thebulwark.com` or `@substack.com` sender containing "thebulwark"
- The Flip Side — `theflipside.io`
- International Intrigue — `internationalintrigue.io`
- Nice News — `nicenews.com`
- The Telegraph — `telegraph.co.uk`
- The Kyiv Independent — look for subject/sender containing "The Kyiv Independent"
- Letters from an American (Heather Cox Richardson) — `@substack.com` sender containing "heathercoxrichardson"; or subject matching "Letters from an American"
- Future Perfect (Vox) — `newsletter@vox.com` / look for sender `newsletter@vox.com` or subject containing "Future Perfect" — weekly (Wednesdays). HTML-only email, do NOT call get_thread, see below for handliong.
- The Iranist — `@substack.com` sender containing "iranist" — periodic analysis on Iran; surface whenever present given current conflict relevance
- Interruptrr (Elmira Bayrasli) — `@substack.com` sender containing "interruptrr" — weekly international affairs with feminist foreign policy lens
- NOTUS — `notus.org` / look for sender containing "notus" — nonprofit reported journalism, domestic policy focus
- The Ink (Anand Giridharadas) — `@substack.com` sender containing "anand" or "the ink" — left-progressive essay-driven
- Decision Desk HQ (The Bellwether) — `@substack.com` senders containing "decisiondeskhq" — electoral and political trend analysis; data-driven but with a mild leftward editorial lean. Surface whenever present; keep treatment brief unless a finding is particularly significant.
- Pew Research Center — `info@pewresearch.org` — low-volume; data-driven research and polling; include when present
- USAFacts — `info@usafacts.org` — low-volume; nonpartisan data and statistics on government and society; include when present
- Al Jazeera — `newsletter@sbmail.aljazeera.com` — weekly; headline + one-sentence summary format (no full article text in email).  Fetch with `get_thread` and synthesize from the summaries; use `web_fetch` on article URLs for any story worth deeper coverage. Note: "Personalised For You" subject line is a generic label, not meaningful personalization — treat as standard Al Jazeera top stories.
- Reuters World News — look for sender containing `reuters.com` or subject containing "Reuters" — wire-service neutral, non-US perspective, broad international coverage. Fetch with `get_thread`; email body typically delivers full text. Prioritize fetching full content.
- BBC World News / BBC News daily digest — look for sender containing `bbc.co.uk` or `bbc.com` or subject containing "BBC" — editorially British, strong non-US global bureau coverage. Fetch with `get_thread`; email body typically delivers full text. Prioritize fetching full content.

**Conflict analysis (threshold only):**

- Institute for the Study of War (ISW) — `understandingwar.org` / look for sender containing "ISW" or "Institute for the Study of War"

Do NOT include ISW content in the digest by default. Only surface it when the update contains a significant battlefield development — major territorial changes, a new front opening, significant force movements, or a meaningful shift in the conflict's trajectory. Routine daily situational updates should be skipped silently.

When included, note the source and its analytical stance: "ISW, which takes a hawkish pro-Western analytical stance, assesses that..."

**Local (Los Alamos / New Mexico — always include if present):**
- Source NM — `sourcenm.com`
- Los Alamos Daily Post — look for subject/sender containing "Los Alamos Daily Post"
- The Los Alamos Reporter — look for subject/sender containing "Los Alamos Reporter"
- BoomTown — `boomtownlosalamos@substack.com` (caught by `@substack.com`; confirm by sender or "BoomTown" in subject)
- The Santa Fe New Mexican — `newsletters@santafenewmexican-email.com` — headlines digest; delivers headline + short summary per story (not full article text, but substantively usable); covers Santa Fe/NM statewide news, politics, sports, and opinion

**Tech & Automotive (occasional):**
- Stack Overflow newsletter — `stackoverflow.email`
- ACM TechNews — `acm.org`
- MotorTrend — `mail.motortrend.com`
- CTA SmartBrief  —  `cta@smartbrief.com`
- Wired — `wired@newsletters.wired.com` — center-left tech journalism. Surface only when a story is particularly significant; skip routine coverage silently.

**Curiosity/delight (low priority):**

- Everything Is Amazing — `everythingisamazing@substack.com` (caught by `@substack.com`) — not news; idle curiosity, wonder, and wandering.
- 

## Source bias handling

Apply these tiers consistently regardless of which sources appear on a given day.

**Tier 1 — Synthesize normally:**
Sources that aim for neutrality or present balanced perspectives. Synthesize into the digest without special framing notes.

- Semafor Flagship, Axios, ProPublica, Source NM, Los Alamos local outlets, The Santa Fe New Mexican, Nice News, International Intrigue, Stack Overflow, ACM TechNews, Ad Fontes Media, Pew Research Center, USAFacts, NOTUS, Everything Is Amazing, Reuters World News, BBC World News

**Tier 1.5 — Synthesize with framing note (conflict analysis):**
Include only when threshold conditions are met (see sources section). Always attribute the stance explicitly.

- ISW / Institute for the Study of War (hawkish, factually rigorous on battlefield details, pro-Western intervention)
- The Iranist (scholarly Iran analysis)

**Tier 2 — Note the framing:**
Sources with a clear editorial lean but practicing legitimate journalism. Include content but attribute perspective explicitly where it matters (e.g., "The Dispatch frames this as...", "The Bulwark is critical of..."). Do not adopt their framing as neutral fact.

- The Dispatch (center-right)
- Advisory Opinions (center-right)
- The Bulwark (anti-Trump conservative / center)
- The Flip Side (explicitly presents both sides — note when their framing differs from Tier 1 sources)
- The Telegraph (center-right British)
- The Kyiv Independent  (center-left Ukraine)
- Letters from an American / Heather Cox Richardson (center-left; historical/constitutional framing)
- Future Perfect / Vox (center-left; science, health, AI, and policy focus)
- Interruptrr / Elmira Bayrasli (center-left internationalist; explicit feminist foreign policy stance — note framing when relevant, e.g. "Interruptrr frames this through a feminist foreign policy lens...")
- The Ink / Anand Giridharadas (left-progressive; essay-driven; focuses on power, inequality, democracy — note framing)
- Decision Desk HQ / The Bellwether (data-driven electoral analysis; aims for nonpartisan but mild leftward editorial lean — note framing when editorializing beyond the numbers, e.g. "Decision Desk HQ's data shows..." vs. flagging opinion)
- Wired (center-left; tech, science, and culture focus — note framing on political or cultural pieces)
- Al Jazeera English (Qatari state-funded; Global South / pro-Palestinian framing on Middle East coverage; valuable counterweight on Iran war and Gaza where Western sources dominate — always note the framing, e.g. "Al Jazeera, which covers the conflict from a pro-Palestinian perspective, reports that...")

**Tier 3 — Flag and use sparingly:**
Outlets with strong ideological lean or activist framing. Use only to note what stories are being amplified from that perspective — do not treat as primary sourcing or adopt their framing. Always identify the outlet and its lean explicitly when citing.

- The Post Millennial — right-leaning
- Judicial Watch - `pr.judicialwatch.org` —  right-leaning

When a Tier 3 source is the only source for a breaking story, note that the story is being reported by that outlet and suggest the user verify with a Tier 1 or 2 source.

## Airtable tracking

All digest runs are logged to the **Newsletter Digest Tracker** base in Airtable.

- **Base ID:** `appTDgMZbYXFcUumA`
- **Digest Runs table ID:** `tblRkX43CDKTY7HBm`
- **Newsletter Usage table ID:** `tbld0qdH1bPXlZNrY`

### Digest Runs fields
| Field | ID | Notes |
|---|---|---|
| Run ID | `fldqFwOYAU6YF7cYT` | Format: `YYYY-MM-DD-NN` (NN = run number that day, e.g. `2026-05-07-01`) |
| Date | `fldWDz6CZISrR7fhj` | ISO date `YYYY-MM-DD` |
| Run Timestamp | `fldKLiYeVabIIWAI1`| Full UTC datetime when the digest was run, ISO 8601, e.g. 2026-05-08T20:50:00.000Z. Use the actual current time at the moment of logging.| 
| Time Window | `fldDb7YPWoUVrcp93` | e.g. "Past 12 hours" |
| Total Newsletters Used | `fldl6DpVQrdbEOHtL` | Count of newsletters that contributed ≥1 story |
| Total Sources | `fldZ04gJw7cXrDkp8` | Count of distinct source outlets |
| Notes | `fld6UTR3o0hdsjHl6` | Any anomalies, e.g. Semafor snippet-only |

### Newsletter Usage fields
| Field | ID | Notes |
|---|---|---|
| Newsletter | `fld7CVhbAdzTAeupR` | Exact newsletter name |
| Run ID | `fldsz9wZH6ZTXh2pe` | Foreign key matching Digest Runs Run ID |
| Story Count | `fldF2RdUYcUsRZBGU` | Number of stories/items used from this newsletter |
| Sections Used | `fldnRoZFP6ncIOFog` | Comma-separated digest sections where this newsletter contributed |
| Content Quality | `fldlfRG0pnAZm4uv1` | "Full content", "Snippet only", or "Not fetched" |
| Tier | `fld2DaeHEm1lYQ6MP` | "Tier 1", "Tier 1.5", "Tier 2", "Tier 3", or "Local" |

Log **every** newsletter that appeared in the Gmail search results and was identified as a relevant newsletter — even if it contributed 0 stories (e.g. Semafor Flagship when snippets were too thin). This captures absence as well as presence. **Do not log** silently discarded sources (Semafor sub-editions, Edinburgh Live, NPR).

---

## Step-by-step workflow

### Step 1: Search Gmail

Search for newsletters in the requested time window (default: past 12 hours). Use a broad query to catch all newsletter-style emails:

```
newer_than:Xh (digest OR briefing OR flagship@semafor.com OR dispatch OR bulwark OR sourcenm OR "los alamos" OR flipside OR intrigue OR nicenews OR motortrend OR telegraph OR "The Kyiv Independent" OR judicialwatch.org OR axios OR propublica OR "understandingwar" OR "institute for the study of war" OR hello@newsletter.scotusblog.com OR @substack.com OR heathercoxrichardson OR "Letters from an American" OR "future perfect" OR futureperfect OR pewresearch OR usafacts OR notus OR giridharadas OR "santa fe new mexican" OR santafenewmexican OR stackoverflow OR acm OR cta@smartbrief.com OR wired OR updates.thedispatch.com OR aljazeera OR reuters OR bbc.co.uk OR bbc.com)
```

Request up to 30–50 results. Scan the sender and subject fields to identify actual newsletters vs. promotional/transactional email. Discard:
- Marketing/promotional emails (sales, offers, discounts)
- Transactional emails (shipping, account alerts, booking confirmations)
- Social notifications (Nextdoor, Quora digests, etc.)
- Bookbub / literary agent / personal hobby newsletters (unless user asks for them)
- Podcast notification emails (subject lines indicating new episode releases — these contain no article content)

### Step 2: Fetch full content

For each identified newsletter thread, call `get_thread` with `messageFormat: FULL_CONTENT` to retrieve the `plaintextBody`. Some threads will only return a snippet — use what's available. Prioritize fetching full content for: Dispatch, Bulwark, Semafor Flagship, Source NM, Los Alamos local sources, Flip Side, International Intrigue, NOTUS, Letters from an American.

**Semafor Flagship:** The email format is intentionally brief — typically 2–3 short paragraphs per story. This is the complete content, not a truncation issue. When the flagship edition (`flagship@semafor.com`) is present and the snippet suggests a significant lead story, attempt `web_fetch` on the flagship article URL to retrieve fuller coverage. The flagship often has the strongest international framing of the day and is worth the extra fetch when the snippet suggests substantive content. Log as "Full content" if web_fetch succeeds, "Snippet only (short format)" if it does not. **Discard any other Semafor sub-editions** (DC, Gulf, Africa, Business, Media) silently — do not log or fetch them.

**The Bulwark:** Full article text is delivered to Gmail for paid subscribers — fetch with `FULL_CONTENT` and treat as full content. Discard any Bulwark emails that are podcast release notifications (identifiable by subject lines like "New episode", "Listen now", or sender patterns like episode titles) during Step 1 source identification — these contain no article content. If `get_thread` returns only a snippet (no `plaintextBody`), attempt `web_fetch` on any article URL visible in the snippet before giving up. Log as "Full content" if web_fetch succeeds, "Snippet only" if it does not.

**The Dispatch (teaser emails from `hello@updates.thedispatch.com`):** These are single-article promotional emails — headline, a two-sentence blurb, and a "Continue Reading" link only. The full article text is not in the email. First check whether the morning Dispatch (`hello@newsletter.thedispatch.com`) already covered the same article. If it did, discard the teaser. If the topic looks significant and isn't covered elsewhere, use `web_fetch` on the article URL from the email to retrieve the full text.

**Axios:** Axios emails (AM, PM, and topic editions) do not include a plaintext MIME part — get_thread will return metadata and a snippet but no plaintextBody. Do not waste a fetch call on Axios threads. Log them as "Snippet only." If Axios coverage of a specific story is needed, use `web_fetch` on the article URL from the snippet instead. Retrieve Axios articles in this way if the snippet does not seem to be covered by other sources.

**NPR:** NPR emails (Up First and others from `email@nl.npr.org`) do not include a plaintext MIME part — confirmed unfetchable. Do NOT call get_thread on NPR threads; it will return only a snippet. NPR has been removed from the active source list. If an NPR story looks important and isn't covered by other sources, use `web_search` on NPR.org directly.

**Future Perfect (Vox):** Future Perfect emails from `newsletter@vox.com` are HTML-only — no plaintextBody available via get_thread. Do NOT call get_thread. Instead, when a Future Perfect email appears and the subject line looks relevant (science, AI, health, ethics, policy), use `web_fetch` on the article URL embedded in the snippet to retrieve the full text. Log as "Snippet only" if no web_fetch is performed, or "Full content" if web_fetch succeeds.

**Managing HTML payload / context cost:** `get_thread` cannot be told to omit `htmlBody` — when it's present it comes back alongside `plaintextBody` regardless of `messageFormat`. For most sources this is harmless (plaintextBody dominates), but a known set of senders wrap a tiny amount of useful text in a very large HTML payload:

- BBC News Briefing (`email.bbc.com`)
- Santa Fe New Mexican, both editions (`santafenewmexican-email.com`)
- Los Alamos Daily Post (Constant Contact / `shared1.ccsend.com`)
- Reuters Daily Briefing and Semafor Flagship, occasionally

If the tool result is large enough to trigger auto-redirect ("Tool result too large for context, stored at..."), that's actually the *good* outcome — use `bash_tool` (`python3 -c "import json; ..."`) to load the saved JSON and print only the `plaintextBody` field(s), never `cat` or `view` the raw file. This keeps the HTML out of context entirely.

The harder case is when one of the senders above returns its bloated HTML *inline* rather than being auto-redirected — this has happened even for 50-100KB+ payloads and isn't fully predictable. There's no tool-level fix for this, so:
1. Fetch these three local/wire sources **early** in Step 2, before lower-priority Tier 2/3 sources, so that if the run is running hot on context, it's a less important source that gets dropped rather than local news or the lead story.
2. When reading a get_thread result, go straight to the `plaintextBody` value and ignore everything under `htmlBody` — don't read through it, quote it, or let it inform the digest even incidentally.
3. If context is already tight after fetching several full-content sources, it's fine to fall back to the search-result snippet for one of these three and log it as "Snippet only (context budget)" rather than force a full fetch.

### Step 3: Write the digest

Organize by theme, not by publication. Use the structure below.

**Always lead with the most globally significant story.** Then proceed through national, then state/local.

Use `###` headers for each thematic section. Write in clear prose paragraphs — no bullet-point summaries. When a story appears in multiple newsletters, synthesize them and note where framings differ (e.g., "The Dispatch covers this neutrally; The Bulwark is more critical of...").

**Sections to use (as applicable — omit if no relevant content):**

1. Major world/geopolitical story (lead section, always present if available)
2. Additional international stories
3. U.S. national politics & federal government
4. Economy, business, tech
5. Science, health, environment
   5b. Tech & automotive (include only if content is present — skip silently if not)
6. New Mexico statewide
7. Los Alamos local (always include if present, even minor items)
8. Curiosity/Delight (always include if present, skip silently if not)
9. Briefly noted (a few sentences on smaller items worth flagging)
10. Palate cleanser (always present — see below)

**Format rules:**
- Use `## Your newsletter digest — [Day], [Date] ([time window])` as the top header
- Below the header, a single italic line: `*Sources: [comma-separated list of newsletters used]*`
- Horizontal rule (`---`) between the header block and the first section
- Section headers: `### [Theme]`
- Horizontal rule between sections
- End with: `---` then `*[N] newsletters from [M] sources. Let me know if you'd like to dig into any of these stories.*`

**Palate cleanser (mandatory final section):**

Every digest must end with a `### 🍹 Palate cleanser` section immediately before the closing footer line. Use `web_search` to find one genuinely fun, frivolous, or delightful piece of recent news — something weird, charming, absurd, or heartwarming. Avoid anything heavy, political, or conflict-adjacent. Good categories: unusual animal stories, quirky world records, unexpected scientific discoveries, oddball human achievements, small acts of joy. Write it in 2–4 sentences of warm, lightly amused prose. Do not use content already covered elsewhere in the digest.  Nice News might provide content for this if not used elsewhere.

### Step 4: Flag local sources prominently

If Source NM, Los Alamos Daily Post, Los Alamos Reporter, BoomTown, or The Santa Fe New Mexican are present, always give them their own **"New Mexico"** and/or **"Los Alamos local"** section — even if the content is brief. Do not fold local stories into national sections.

### Step 5: Log to Airtable

After writing the digest, log the run to Airtable. Do this silently — no narration in the digest output.

1. Create one record in **Digest Runs** with the run metadata.
2. Create one record per newsletter in **Newsletter Usage**, including newsletters that were present but contributed 0 stories (log them with Story Count = 0 and a note in Sections Used like "Not used — snippet only").

Run ID format: `YYYY-MM-DD-NN` where NN increments if multiple runs happen in one day. Check the most recent Digest Runs record to determine the next NN; default to `01` if none exist for that date.

### Step 6: Append usage summary table to digest

After the closing footer line of the digest, append a collapsible usage summary under a `### 📊 Source usage — this run` header. Format as a markdown table:

```
| Newsletter | Stories used | Sections | Content |
|---|---|---|---|
| The Dispatch | 6 | International, U.S. Politics, Economy/Tech, Science/Health | Full |
| International Intrigue | 7 | International (lead), Briefly Noted | Full |
...
```

Sort by Stories Used descending. Include all newsletters that appeared in the search, even those with 0 stories used.

## Default time window

If the user doesn't specify, use the past 12 hours. Accept natural language like "past 6 hours", "last 24 hours", "yesterday's newsletters", "this week's".

## Handling thin results

If fewer than 3 newsletters are found in the time window, say so and suggest extending the window. Don't synthesize a single newsletter as if it were a multi-source digest.

## Tone

Neutral and informative. Do not editorialize or add opinions. When The Bulwark or similar opinionated sources take a strong stance, you may note the framing ("The Bulwark frames this as...") but don't adopt it yourself.