---
name: github-skill-pull
description: "Pull skill files from the jrhay/AITools GitHub repo down into their correct local location under /mnt/skills/user/ or /mnt/skills/plugins/. Use when the user asks to pull, sync down, restore, or refresh their skills from GitHub — e.g. 'pull my skills', 'sync skills from github', 'get the latest skills from the repo', 'restore my skills from AITools'. This is the read-direction companion to github-skill-sync (which pushes local changes up)."
---

# GitHub Skill Pull

Companion to `github-skill-sync`. Where that skill pushes local skill edits up to
GitHub, this skill pulls skill files down from GitHub into the local
`/mnt/skills/` tree — e.g. after a fresh session/container reset, or to recover
a skill that only exists in the repo.

## When to use

Trigger when the user explicitly asks to pull, sync down, restore, or refresh
skills from the `jrhay/AITools` repo. Unlike `github-skill-sync`, this is NOT
automatic — pulling overwrites local files, so only run it when asked.

Scope: `skills/user/` and `skills/plugins/` in the repo, mapping to
`/mnt/skills/user/` and `/mnt/skills/plugins/` locally. Do not touch
`/mnt/skills/public/` or `/mnt/skills/examples/` (managed externally, and
read-only on disk anyway).

## Repo details

- Owner: `jrhay`
- Repo: `AITools`
- Branch: `main`
- Repo path `skills/user/<skill-name>/SKILL.md` maps to local
  `/mnt/skills/user/<skill-name>/SKILL.md` (same for `plugins`).

## Auth

Same as `github-skill-sync`: use the fine-grained GitHub personal access
token (jrhay/AITools, Contents read/write) if one is already available in
the current session's context. Never log, display, or write it to
persistent memory.

If no token is available, ask the user directly for the current PAT — do
not guess, reuse a token from an old conversation, or search past chats for
one. Use it for this session only.

## Pull procedure

Use the GitHub Contents API via `bash_tool` with `urllib` (stdlib only, no
`gh` CLI, no `requests`):

```python
import base64, json, urllib.request, urllib.error
from pathlib import Path

TOKEN = "<token from session>"
OWNER = "jrhay"
REPO  = "AITools"

def api(method, path):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "detail": json.loads(e.read())}

def list_dir(repo_path):
    """List entries (files/dirs) at a path in the repo. Returns [] if missing."""
    result = api("GET", f"/repos/{OWNER}/{REPO}/contents/{repo_path}")
    return result if isinstance(result, list) else []

def pull_file(repo_path, local_path):
    """Fetch one file from the repo and write it locally. Returns 'updated', 'unchanged', or 'created'."""
    result = api("GET", f"/repos/{OWNER}/{REPO}/contents/{repo_path}")
    if "content" not in result:
        return f"error: {result}"
    new_content = base64.b64decode(result["content"])
    local = Path(local_path)
    if local.exists():
        status = "unchanged" if local.read_bytes() == new_content else "updated"
    else:
        status = "created"
        local.parent.mkdir(parents=True, exist_ok=True)
    if status != "unchanged":
        local.write_bytes(new_content)
    return status
```

Steps:
1. For each of `skills/user` and `skills/plugins`, call `list_dir` to get the
   list of skill subdirectories in the repo.
2. For each skill directory, `pull_file` its `SKILL.md` (and any other files
   it contains, if the skill has more than one file) to the matching local
   path.
3. Also list the corresponding local directory (`/mnt/skills/user/` or
   `/mnt/skills/plugins/`) via `view` or `bash_tool` (`ls`), and note any
   local skill folder that has no matching entry in the repo listing — this
   usually means either an unpushed local skill or a repo-side deletion.
   **Do not delete it automatically** — just flag it and ask.

## Reporting back

Give a short summary grouped by status, not a wall of text:

```
Pulled from jrhay/AITools:
- updated: skills/user/newsletter-digest
- created: skills/user/job-board-search
- unchanged: skills/user/animal-pickmeup, skills/user/newsletter-stats, skills/plugins/... (n unchanged)

Local-only (not in repo, left untouched): skills/user/some-wip-skill
```

Skip the "unchanged" list entirely if everything was unchanged — just say so
in one line.

## Error handling

If the GitHub API call fails (auth, rate limit, missing path), report the
actual error clearly — don't guess at the cause. Do not silently skip a
failed skill; call it out by name.
