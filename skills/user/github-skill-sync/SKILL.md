---
name: github-skill-sync
description: "Push updated skill files to the jrhay/AITools GitHub repo. Use this automatically whenever a skill file under /mnt/skills/user/ or /mnt/skills/plugins/ is created or modified in a conversation. Do not wait to be asked — push immediately after the skill file is written."
---

# GitHub Skill Sync

Automatically keeps the jrhay/AITools GitHub repo in sync whenever skill files are created or modified.

## When to use

Trigger automatically (without being asked) after any of these actions:
- A skill file under `/mnt/skills/user/` is created or modified
- A skill file under `/mnt/skills/plugins/` is created or modified

Do not use for `/mnt/skills/public/` or `/mnt/skills/examples/` — those are managed externally.

## Repo details

- Owner: `jrhay`
- Repo: `AITools`
- Branch: `main`
- Skill files map to: `skills/user/<skill-name>/SKILL.md` or `skills/plugins/<skill-name>/SKILL.md`

## Auth

Do NOT store the GitHub token in memory — a fine-grained PAT is a live credential, and memory files aren't a secrets vault (they're plain text, readable back into future conversations, and not scoped the way a proper secrets manager is).

Instead, prompt for the token each time a push is needed in a session that doesn't already have it in context:
"I need to push `<repo_path>` to jrhay/AITools — can you paste the GitHub token for this?"

Once provided, use it only for pushes within the current conversation. Never write it to memory, never echo it back in full, and don't carry it forward into a new conversation — ask again next time. If several pushes happen in the same session, reuse the token already given rather than asking again for each file.

## Push procedure

Use the GitHub Contents API via `bash_tool` with `urllib` (no `gh` CLI, no `requests` — use stdlib only):

```python
import base64, json, urllib.request, urllib.error
from pathlib import Path

TOKEN = "<token pasted by user this session>"
OWNER = "jrhay"
REPO  = "AITools"

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def push_file(local_path, repo_path, message):
    content = Path(local_path).read_bytes()
    encoded = base64.b64encode(content).decode()
    existing = api("GET", f"/repos/{OWNER}/{REPO}/contents/{repo_path}")
    sha = existing.get("sha")
    payload = {"message": message, "content": encoded}
    if sha:
        payload["sha"] = sha
    result = api("PUT", f"/repos/{OWNER}/{REPO}/contents/{repo_path}", payload)
    return "content" in result
```

## Commit message format

```
Update <repo_path> — <brief reason>
```

Examples:
- `Update skills/user/newsletter-stats/SKILL.md — add 30-day inactive threshold`
- `Update skills/user/newsletter-digest/SKILL.md — add Edinburgh Live exclusion`
- `Add skills/user/new-skill/SKILL.md — initial commit`

The reason should come from the context of what changed in the conversation — be specific, not generic ("update skill" is not useful).

## After pushing

Confirm silently with a single line, e.g.:
`↑ Pushed to [jrhay/AITools](https://github.com/jrhay/AITools/blob/main/<repo_path>)`

Do not narrate the push process or show the code unless there's an error.

## Error handling

If the push fails, report the error clearly and offer to retry. Do not silently swallow failures.
