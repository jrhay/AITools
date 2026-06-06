---
name: newsletter-stats
description: "Report on newsletter-digest skill.  When the user types `/newsletter-stats` (or asks \"how are my newsletters performing\", \"which newsletters should I cut\", etc.), query Airtable and produce a stats report."
---

## `/newsletter-stats` command

When the user types `/newsletter-stats` (or asks "how are my newsletters performing", "which newsletters should I cut", etc.), query Airtable and produce a stats report.

### What to pull
1. All records from **Newsletter Usage** (all runs)
2. All records from **Digest Runs** (for total run count and date range)

### Filtering before analysis

Before computing any stats, apply these filters to the Newsletter Usage records:

1. **Silently exclude `(discarded)`** — these are sub-edition noise from subscriptions; never surface them in any part of the report.

2. **Active vs. inactive split** — determine the most recent appearance date for each newsletter. A newsletter is **inactive** if its most recent appearance across all runs is more than 30 days before the most recent digest run date.
   - Include only **active** newsletters in the main stats table and editorial sections.
   - Collect inactive newsletters into a separate **"Not heard from in 30+ days"** summary at the end of the report (see format below).

### Stats to compute and report

- **Total runs tracked** and date range (first → most recent)
- **Per-newsletter summary table** (active sources only), sorted by Total Stories desc:

| Newsletter | Tier | Runs Present | Total Stories | Avg/Run | Full Content % |
|---|---|---|---|---|---|

- **Workhorses:** top 3–5 active sources by total story count.
- **Snippet-only problem sources:** active newsletters with Content Quality = "Snippet only" in most/all runs. Flag as unreliable for full content.
- **Underperformers:** active sources present in ≥3 runs but averaging <1 story/run.
- **Editorial note:** brief recommendations — candidates to cut, candidates to promote, structural issues.

### "Not heard from in 30+ days" section

Append this section at the end of the report, after the editorial note:

---
**📭 Not heard from in 30+ days**
*These sources haven't appeared in a digest run since [date of most recent appearance]. Some (like The Iranist) are known to be periodic — others may warrant unsubscribing.*

| Newsletter | Tier | Last Seen | Total Stories (all-time) |
|---|---|---|---|
| ... | ... | ... | ... |

Sort by Last Seen descending (most recently inactive first). Omit this section entirely if no sources qualify.

Format the overall report clearly. The inactive section is informational only — do not include inactive sources in the editorial recommendations unless their all-time stats suggest they were never useful.
