---
name: animal-pickmeup
description: Find and present 3–5 recent, genuinely heartwarming animal stories or videos from the web. Use this skill whenever the user asks for a pick-me-up, mood boost, cute animal content, heartwarming news, or anything like "cheer me up," "I need something happy," "find me some animal stories," "any good animal news lately?", "show me something cute," or "I need a distraction." Also trigger when the user seems to want a brief emotional reset or light content after a heavy topic. Always use this skill proactively — don't just answer with a generic suggestion to search YouTube.
---

# Animal Pick-Me-Up Skill

Searches the web for recent heartwarming animal stories and videos, then presents 3–5 of them in a warm, readable format with summaries and direct links.

## Workflow

### 1. Search for Recent Stories

Run 2–3 targeted web searches to find genuinely recent content. Prioritize stories from the **past 2–4 weeks**. Good search queries:

- `heartwarming animal story [current month] [year]`
- `viral animal video [current month] [year]`
- `cute animal news [year]`
- `animal rescue story [current month] [year]`
- Specific sources: `site:thedodo.com`, NPR Animals section, Washington Post Animals, Good News Post

**Avoid:** Generic listicle sites that recycle old stories (Aproposh, Ragus Associates, owhwyln.info, lokasitogel — these are low-quality SEO farms that fabricate or recycle content). Prefer NPR, The Dodo, Washington Post, BBC, local news outlets, and verified wildlife organizations.

### 2. Verify Recency and Authenticity

Before including a story:
- Check that it has a real publication date within the past few weeks
- Confirm it describes a specific, named animal or documented event (not a generic "Buddy the dog")
- Prefer stories with photos, video links, or named sources (rescue orgs, wildlife agencies, journalists)
- **Avoid AI-generated or synthetic content.** Red flags: viral "videos" with no identifiable creator or platform link, suspiciously perfect emotional beats, stock-photo-style descriptions, and stories that can't be traced to a named journalist, organization, or original social media post. The specificity check (named animal, named rescuer, named location) catches most of this — if a story could have been written by filling in a template, skip it.

If search results are thin on truly recent content, broaden to the past 2 months rather than padding with old or generic material.

### 3. Diversify the Selection

Aim for variety across the 3–5 stories:
- Mix species (not all dogs)
- Mix story types: rescues, wildlife moments, unusual friendships, feel-good reunions, citizen science wins
- Include at least one with a direct video link when possible

### 4. Format the Output

Present each story in this format:

```
**[Number]. [Emoji] [Story Title]**
[2–3 sentence summary in your own words — warm but not saccharine]
👉 [Link text](URL)
```

End with a brief personal note recommending 1–2 favorites if they're clearly standout stories.

## Tone Guidelines

- Warm and genuine, not over-the-top gushing
- Brief summaries — let the story do the work
- Don't editorialize excessively; trust the user to feel the feelings
- If a story has a bittersweet or surprising angle, mention it — that's often what makes it stick

## Example Output Structure

> **1. 🐋 Timmy the Humpback Whale Finally Goes Free**
> After being stranded five separate times near the German coast since March, a 40-foot humpback whale named Timmy was finally transported to open sea via a water-filled barge funded by two private donors. Footage of him surfacing freely in the North Sea made a lot of people cry happy tears.
> 👉 [NPR story](https://www.npr.org/...)

> **2. 🐻 Baby Bear Mishka's First Walk**
> A Texas wildlife park shared video of bear cub Mishka's first outing on a leash — she sniffed everything, got tangled in her own leash, picked a fight with a bush, and ended the walk by staring intensely at some chickens and cows. Extremely relatable.
> 👉 [Watch the clip](https://...)

*(Continue for 3–5 total)*

> *Personal note: [Story X] and [Story Y] are the standouts this week if you only have time for two.*
