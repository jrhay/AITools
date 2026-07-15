---
name: job-board-search
description: Runs a periodic, directed search of Jeff Hay's tracked company career boards (Sandia, LANL/Triad, N3B, New Mexico Consortium, SpaceNukes, AMD, Kraken Robotics, Blue River Technology) for senior/staff/principal embedded, real-time, or C/C++ systems engineering roles that are remote-eligible or Los Alamos/NM local. Use this whenever Jeff asks to "check job boards," "run my job search," "see what's open at [tracked company]," or similar — including as a recurring/scheduled check. Most of these boards render job listings with JavaScript, so this skill requires live browser access (Claude in Chrome), not just web search or a static fetch.
---

# Job board search — Jeff Hay

## Why this exists

Jeff is a senior/staff/principal-level embedded systems and real-time C/C++ engineer (20+ years, LANL Network Engineering Group alum, DOE Q clearance eligible) doing an active job search after his remote position at UT Austin's Texas Institute for Electronics was eliminated. He's explicitly told Claude that LinkedIn/aggregator "remote" tags are unreliable and that the company's own careers page is the source of truth — which is why this skill exists as a *directed* search rather than a keyword search on Indeed/Glassdoor/LinkedIn.

Full background, resume variants, and warm-contact notes live in Jeff's "Job Search" project knowledge — check there for anything that's changed (new target companies, updated resume framing, warm contact status) before running this.

## What counts as a match

Evaluate every posting against all of these, and say so explicitly when one is missing rather than glossing over it:

- **Level**: senior, staff, or principal individual-contributor scope. Roles scoped for early/mid-career engineers on an upward trajectory are a level mismatch even if the tech stack fits — flag this rather than including them as strong matches.
- **Location**: remote-eligible (US) **or** genuinely Los Alamos/Albuquerque/Santa Fe NM local (Jeff lives in Los Alamos, so onsite roles at the NM companies below still count — but onsite roles at out-of-state companies do not, and should be labeled onsite/non-remote rather than omitted, since Jeff may still want to know about them). **Exception: AMD** — see the AMD row below, its posted locations are unreliable and should be treated more loosely.
- **Domain fit**: C/C++, embedded systems, real-time/RTOS, hardware-software integration, FPGA-adjacent, RF/signal processing, motion control, or scientific instrumentation. Python-heavy or pure ML/CV roles are a stretch unless the posting explicitly also wants systems-level C/C++.
- **Mission fit**: national security/defense, aerospace/space, national labs, scientific research, or conservation. Not a hard filter, but worth noting when present or absent.
- **Avoid**: heavy people-management roles, pure sales/marketing/business-development roles even if titled "engineer," and roles requiring a security clearance Jeff can't realistically obtain (he's Q-clearance-eligible for reinstatement, not currently cleared, so "must have active TS/SCI" roles are excluded).

If nothing matches well at a given company, say so plainly rather than padding the report with weak fits.

## Companies to check

Los Alamos-area / national lab (always check first — these are Jeff's home turf and the strongest fit for the "local" side of the location filter):

| Company | Start here | Notes |
|---|---|---|
| Sandia National Laboratories | https://sandia.jobs/ | Best hit rate historically. Postings churn fast (minimum 3-day open window) — always confirm a listing is still live by opening it directly rather than trusting a cached search-engine link. The site's own keyword search box is flaky (doesn't reliably filter); it's more reliable to load the homepage listing feed and scan titles/req IDs directly, paging through with the `»` control. |
| Los Alamos National Laboratory (LANL) | https://lanl.jobs/ (search: https://lanl.jobs/search/searchjobs) | Triad National Security is LANL's managing contractor — Triad-badged postings show up on this same board, so don't search it separately. |
| N3B Los Alamos | https://n3b-la.com/careers/ | LANL's environmental/legacy-cleanup contractor. Mostly environmental/industrial roles — check, but don't expect much software fit. |
| New Mexico Consortium | https://newmexicoconsortium.org/careers/ | Small nonprofit research org at Los Alamos Research Park, partners with LANL. Very few postings at any time — quick check, low volume. |
| Space Nuclear Power Corp (SpaceNukes) | https://www.spacenukes.com/ | LANL spin-off building space fission reactor power systems (KRUSTY/Kilopower lineage) — strong mission fit if Jeff wants to lean into the space angle. Small company, no formal ATS/job board as of this writing — check the site for a careers/contact page and their LinkedIn (linkedin.com/company/81516951) for openings; may require direct outreach rather than a standard application. |

Also worth a quick check while in the neighborhood: the Los Alamos Chamber of Commerce job board (https://www.losalamoschamber.com/job-postings) aggregates other local employers and occasionally surfaces something relevant.

New Mexico quantum-sector companies (watchlist, added July 2026 — surfaced via the NM Economic Development Department's Quantum Technologies Award grants covered in the 7/15/26 newsletter digest). These lean hardware/photonics/materials rather than pure embedded C/C++, so domain fit is more mixed than the lab-adjacent companies above — flag that explicitly rather than treating a match here as automatically strong:

| Company | Start here | Notes |
|---|---|---|
| Mesa Quantum | https://apply.workable.com/mesa-quantum-systems/ | Dual HQ Albuquerque, NM / Boulder, CO. Chip-scale atomic clocks and PNT sensors. Best hit rate of this group — Photonics Test Engineer, Laser Nanofabrication, and Quantum Lab Technician roles have posted regularly in Albuquerque, and the work (component-level characterization, VCSEL/laser test, control and qualification systems) has real overlap with instrumentation/hardware-software integration even though titles skew toward optics/physics rather than straight C/C++. Check this one first. |
| Bandelier Technologies | https://www.bandeliertech.com/careers | Santa Fe. Quantum radar/sensing spinout via the LANL LEEP program, defense-focused (dual-use, DARPA-adjacent). Small team with an actual careers page, though current postings skew early-career experimental physics rather than systems engineering. Worth a periodic check for the sensing/instrumentation overlap. |
| Conductor Quantum | https://www.ycombinator.com/companies/conductor-quantum/jobs | YC-backed (S24). Currently HQ'd and hiring in San Francisco, NOT yet NM-local, despite taking NM grant money to "establish a presence" here — confirm location on any posting before getting excited. Domain fit on paper is strong when they do post (device fab, PCB design for cryogenic testing, control software for waveform generators/DACs), closer to Jeff's profile than most quantum-sector postings. Watch for an NM-based req to appear as their grant-funded expansion plays out. |
| Photon Queue | https://photonqueue.com/ | Currently HQ'd in Champaign, IL (UIUC spinout). Received a $500K NM grant (announced 7/14/26) to build out assembly/test operations in Albuquerque and hire locally — too new to have NM postings live yet. No dedicated jobs page; check LinkedIn and the company site periodically as the Albuquerque buildout gets underway. |
| UbiQD | https://www.ubiqd.com/careers (also check LinkedIn — they post there more than on their own site) | Genuinely local: HQ is in Los Alamos itself (Eastgate Road campus). Advanced-materials/quantum-dot manufacturer (agriculture, clean energy, security) rather than a software/embedded shop, so most roles (chemistry, manufacturing, safety) are a domain mismatch for Jeff's profile specifically — but the company is growing fast (Series B closed 2025, committed to 10+ new jobs by 2028) and it's about as local as it gets, so a quick scan is cheap. |
| Mesa Photonics | https://mesaphotonics.com/announcements/jobs/ | Santa Fe, tiny (2-10 employees), ultrafast-laser pulse measurement instrumentation. Site listed "no employment opportunities" as of this writing. Low-volume — quick check only, don't expect much. |

Broader target companies (check these too, but they're lower-probability for a remote or NM-local senior embedded match):

| Company | Start here | Notes |
|---|---|---|
| AMD | https://amd.jibeapply.com/careers-home/jobs | Postings almost always list a specific site (San Jose, Austin, etc.) and are tagged #Hybrid, but per an inside source Jeff trusts, AMD is internally moving toward full remote for nearly all roles regardless of the posted location, with minimal-to-no travel expected in most cases. So be looser on AMD's location filter than the posting text alone suggests — don't screen out an otherwise strong AMD match just because it lists an onsite city or #Hybrid tag. Flag it as "posted onsite/hybrid, but AMD is reportedly going remote-first internally — worth asking about during the application/interview process" rather than discarding it outright. |
| Kraken Robotics | https://ats.rippling.com/kraken-robotics-inc/jobs | Marine/subsea robotics, mission-aligned (defense-adjacent, ocean tech). Has posted genuine Remote-US embedded/firmware C++ roles before — good source. Titles like "Level 2" or "Level II" typically mean mid-level, not senior. |
| Blue River Technology | https://www.bluerivertechnology.com/careers/open-positions/ | John Deere's autonomy/robotics R&D arm. Hiring has been on-and-off — check whether they're actively posting before investing effort. Most roles skew ML/CV/Python; only flag as a strong match if a posting explicitly wants systems-level C/C++.

Companies intentionally **not** in rotation (checked before and found low-yield for Jeff's profile — don't re-add without asking): Eaton, Vertiv, RTX/Raytheon. If Jeff asks to check one of these again, do it, but don't add it back to the default rotation without confirming with him first.

## How to actually search these boards

**Use live browser access, not web search or a plain fetch.** Nearly all of these boards (Sandia, LANL, AMD, Kraken, Blue River) render job listings client-side with JavaScript. A plain web-fetch tool will return an empty page shell — this isn't a fluke, it happens on essentially every one of these sites. Load `mcp__claude-in-chrome__*` tools (via ToolSearch if deferred: `tabs_context_mcp`, `navigate`, `get_page_text`, `find`, `computer`, `browser_batch`) and actually browse.

A few site-specific quirks worth knowing before you burn time rediscovering them:

- **AMD (Jibe-based board)**: typing a keyword into the URL query param alone does *not* filter results. You have to actually click into the search box, type the keyword, and click the magnifying-glass search button (or press Enter) for the filter to apply — watch for the URL picking up a `keywords=` param as confirmation it worked.
- **Sandia**: the keyword search box on sandia.jobs is unreliable — clicks and typed text don't always trigger the underlying filter. It's faster and more reliable to just load the homepage feed (which shows current live postings sorted by req ID) and scan/page through it, or search Google for `site:sandia.jobs [keyword]` and then verify each hit is still live by opening it directly (many indexed postings have expired — the page will say so plainly if it has).
- **Kraken Robotics (Rippling ATS)**: clicking a job title link sometimes doesn't navigate — if `get_page_text` still shows the listing page after a click, re-run `find` to get the link's actual href and navigate to it directly instead of relying on the click.
- **General pattern**: if a click doesn't seem to do anything, don't just retry the same click — take a screenshot to see what's actually on screen, or fetch the href directly and navigate there. Several of these sites need a nav-menu click (e.g., clicking "Jobs > Search Jobs") to actually initialize a search widget that a direct deep-link URL leaves blank.

## Output format

Lead with the single best match, if there is one — don't bury a great fit in a wall of company-by-company detail. Then go company by company (or skip companies with nothing relevant, and say so in one line rather than a full section). For each posting worth mentioning, include:

- Title, location, and whether it's remote/onsite/hybrid
- A one- or two-line honest assessment against the match criteria above — including the gaps, not just the fit (e.g., "strong technical fit but Level II, likely below your bar" or "onsite Tucson, not remote or NM, but worth knowing about given the mission fit")
- A direct link to the posting

Close with a one-line note on anything that looked promising via search-engine caching but turned out to be expired when checked live — this tells Jeff the board is worth rechecking on a cadence rather than that it was empty.

Don't inflate weak results to make the report look more productive. If a company genuinely has nothing, one line saying so is more useful than padding.
