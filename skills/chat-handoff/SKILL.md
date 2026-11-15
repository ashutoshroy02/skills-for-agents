---
name: chat-handoff
description: >-
  Packages the current Claude Code chat so another Claude account or a later session can continue it: exports
  the transcript zip, names it after the chat's main task, writes a hand-off note and puts it in the zip, and
  writes a compact detailed summary (a few thousand tokens instead of a huge transcript) with GitHub links to
  commits, releases and code files, every link checked. Use whenever the user says '/handoff', 'hand off',
  'share this chat', 'export this chat', 'move this to another Claude account', 'continue this later',
  'summary of this conversation', 'resume note', 'the transcript is too big', or wants to pass the work on.
domain: process
composable: true
yields_to: []
---

# Chat Handoff

A 45 MB transcript costs ~500k tokens to import; a good summary with links costs ~5k and loses nothing that
matters, because the code lives on GitHub. This skill produces three things, in this order of importance:

| Output | File | Purpose |
|---|---|---|
| **Summary** (the main deliverable) | `<Project>-Chat-Summary.md` | What a new session reads: goal, timeline, features, links, open tasks, warnings |
| **Hand-off note** | `HANDOFF-<Project>.md`, also inside the zip | Short "resume from here" note |
| **Transcript export** | `<Project>-<Main-Task>-Chat.zip` | Full backup, only for digging into history |

Success = a fresh Claude, given only the summary and the repo, can continue the open tasks without asking what
happened. Every link in the summary opens (HTTP 200). No secret appears in any file.

## When to Use

- "/handoff", "hand off this task", "make a resume note", "write a hand-off"
- "share this chat with my other Claude account", "how do I move this conversation"
- "export this chat", "name the export after the task"
- "summarise this conversation with GitHub links", "the export is too big to import"
- The user is about to switch accounts, machines or sessions mid-project

If the user asks for only one of the three outputs, make that one (the summary still benefits from Steps 1
and 5). Everything is written locally; nothing is uploaded.

## Core Workflow

### Step 1: Gather facts from git, not from the transcript

Read the transcript file only if your own context lacks something: it is huge and repeats itself. Collect:

```bash
git remote get-url origin; git branch --show-current; git status -sb   # ahead/behind = unpushed commits
git log --reverse --format="%h %ad %s" --date=short
gh release list --repo OWNER/REPO          # skip if gh is missing or the repo has no releases
git ls-files <dir>                         # real paths, for links
```

Because links point at GitHub, they only work for pushed commits and tracked files. If `git status -sb` shows
unpushed commits or uncommitted work, say so in the summary's Open tasks instead of linking it, and tell the
user (don't push for them unless they ask).

### Step 2: Export the transcript

Call `mcp__ccd_session_mgmt__export_transcript` with `session_id: "self"` (load it first with ToolSearch
`select:mcp__ccd_session_mgmt__export_transcript` if it is deferred). It writes a zip to Downloads and returns
the path. Outside the desktop app (plain CLI), zip the session's `.jsonl` from
`~/.claude/projects/<project-key>/` instead.

### Step 3: Name the zip after the chat's main task

Name it after the goal of the **whole** chat, not its first message (sessions drift: a chat titled "Fix 3
navigation bugs" became a full game release). Pattern: `<Project>-<Main-Task>-Chat.zip`, Title-Case words
joined by hyphens, no spaces.

- ✅ `Velocity-Blocks-Game-Build-Release-and-Website-Chat.zip`
- ❌ `session-export-1792678181677.zip`, `chat.zip`, `Fix-3-navigation-bugs.zip`

Rename with `python <skill>/scripts/handoff.py rename ZIP NEW_NAME` (refuses to overwrite).

### Step 4: Write the hand-off note

Start from `templates/HANDOFF.md`. Keep it to one screen: what the project is, what is done, open tasks,
how to release, warnings. Then put it in the zip:
`python <skill>/scripts/handoff.py add-to-zip ZIP HANDOFF-<Project>.md` (replaces an older copy, then checks
the zip). Keep a copy next to the zip so it can be read without unzipping.

### Step 5: Write the summary with links

Start from `templates/SUMMARY.md`. Target 15-25 KB (about 4-6k tokens). Link everything a reader would want
to open, with these URL shapes:

| Thing | URL |
|---|---|
| Commit | `https://github.com/OWNER/REPO/commit/<short-sha>` |
| File | `https://github.com/OWNER/REPO/blob/<branch>/<path>` |
| Release | `https://github.com/OWNER/REPO/releases/tag/<tag>` |

Write it so it stands alone:
- **Timeline:** one table row per commit, saying in plain words what changed and why the user wanted it.
- **Feature sections:** each claim names the file that implements it, as a link, so the next session opens the
  file instead of searching.
- **Decisions:** record the user's choices and their reasons (e.g. "GitHub APK free, Play Store paid"), because
  a new session would otherwise re-ask.
- **Open tasks:** what was offered but not decided, what is untested, what only the user can do.
- **Warnings:** anything that silently breaks on another machine or account (signing keys, which account can
  publish, build quirks, the user's working rules).

### Step 6: Check every link and every secret

```bash
python <skill>/scripts/handoff.py check-links SUMMARY.md HANDOFF.md   # prints failures; exit 1 if any
```

Fix or remove each broken link (usually a typo'd path or an unpushed commit), then re-run until it reports
0 broken. Then scan both notes for secrets: passwords, API keys, tokens, keystore passwords, private emails
beyond what the user shares on purpose. Write "ask the user" where a secret would go, because these files are
made to be sent to someone.

### Step 7: Report

Tell the user, briefly: each file's path and size, the summary's rough token cost (bytes / 4), that the
transcript contains their paths and account names (share with care), and the prompt to use in the new session:

> Read `<Project>-Chat-Summary.md` and continue from Open tasks.

## Boundaries

- Writes files locally only. Sending or uploading them (Drive, email, Slack, another account) is the user's
  action, or needs their explicit go-ahead.
- Commits, pushes and releases nothing; if links need unpushed work, report that instead.
- Leaves the session's own title and the repo untouched unless the user asks.
- Summarises what happened; it does not re-run or re-verify the project's work (say "not verified" where the
  chat left something unverified).

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

Chat-handoff owns **process**: the export, naming, hand-off and summary workflow and the structure of its two
notes.

### When Chat-Handoff Leads

- The user wants to move, share, resume or archive a chat's work
- The user asks for a conversation summary meant for another session

### When Chat-Handoff Defers

| Other Skill's Domain | What Chat-Handoff Does |
|---|---|
| **Density** (caveman, compress) | Keeps every section, table and link; lets the density skill shorten the prose inside them. |
| **Voice** (blogger, humanize) | Keeps facts, links and section order; the voice skill may reword sentences. |
| **Process** (memory) | Runs alongside: memory saves facts for this machine, the summary carries them to another one. |

### Conflict Signal

> `⚠️ Process conflict: [skill] wants to drop [section/links]. Kept them, because the next session needs them to resume; shortened the prose instead.`

---

**Remember:** the summary is the product. Facts from git, a link for every claim, every link checked, no
secrets, and an Open tasks list a stranger could act on.
