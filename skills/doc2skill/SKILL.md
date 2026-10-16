---
name: doc2skill
description: >
  Turn documentation into a ready-to-use Claude skill: crawl a docs website (or read a
  repo's markdown docs), sort the pages into categorized references/, write a real
  SKILL.md from the docs' own examples, and package it as a .zip or install it for
  Claude Code. Use whenever the user wants a skill built FROM existing documentation —
  "doc2skill", "make a skill from these docs", "turn <url> docs into a skill", "create a
  React / FastAPI / Godot / <library> skill", "scrape the docs for Claude", "package this
  documentation as a skill", "give Claude the docs of X" — even if they only paste a
  docs URL and say "skill". Presets ship for React, Vue, Django, FastAPI, Godot, Steam.
domain: process
composable: true
yields_to: []
license: MIT (adapted from github.com/moinulmoin/doc2skill)
---

# doc2skill

Documentation in, skill out. A script does the crawling and sorting the same way every time; Claude does the part a script does badly — reading the references and writing a SKILL.md built from the docs' real examples. The script's generic draft is a starting point, never the deliverable.

## Rules That Decide Quality

1. **Copy examples, never invent them.** Every code block in the final SKILL.md exists in `references/` (same API names, same arguments), because a skill teaches every future session — an invented API becomes a hallucination baked into all of them.
2. **Test crawl first.** Run with `--max-pages 20`, look at the output, then do the full run — because wrong selectors silently produce empty pages, and finding that after 500 pages wastes the user's time and the site's bandwidth.
3. **Be a polite crawler.** Keep `rate_limit` at 0.5 s or more; the script obeys robots.txt. Skip pages behind logins, and use another source (step 1) when a site blocks the crawler.
4. **Ask before two things:** a crawl over ~300 pages, and copying the finished skill into `~/.claude/skills/` (it then loads in every future session).

## When to Use

- A docs URL plus "make a skill", "doc2skill", "Claude should know this library"
- A GitHub repo whose `docs/` folder should become a skill
- Rebuilding or refreshing a skill made earlier from docs (`--skip-scrape` reuses the cache)
- Packaging an existing skill folder as a `.zip` for upload

## Workflow

Scripts live in this skill's folder: `SKILL_DIR = ~/.claude/skills/doc2skill` (`C:\Users\<user>\.claude\skills\doc2skill` on Windows). Needs Python 3.8+ with `requests` and `beautifulsoup4` (`pip install requests beautifulsoup4`); markdown mode needs neither. Work in a folder the user chose, else `./doc2skill-output/`.

### Step 1 — Pick the source (cheapest faithful one first)

| Source | When | How |
|---|---|---|
| Repo markdown | Docs live on GitHub as `.md`/`.mdx` | `git clone --depth 1 <repo>` then `--markdown-dir <repo>/docs` |
| `llms-full.txt` | Site publishes one (check `<site>/llms-full.txt`, `<site>/llms.txt`) | Download it into a folder, split by `#` headings into `.md` files, use `--markdown-dir` |
| HTML crawl | Everything else | A preset from `configs/`, or a config you write (step 2) |

Markdown beats HTML because it keeps code fences and headings exactly; a crawl reads whatever the page template wraps around them.

### Step 2 — Write the config (HTML crawl only)

Start from the closest preset in `$SKILL_DIR/configs/`. Copy it next to the output, then change it:

```json
{
  "name": "fastapi",
  "description": "FastAPI web framework. Use for path operations, request bodies, dependencies, security and async endpoints.",
  "base_url": "https://fastapi.tiangolo.com/",
  "selectors": {"main_content": "article", "title": "h1", "code_blocks": "pre code"},
  "url_patterns": {"include": ["/tutorial/", "/advanced/"], "exclude": ["/help/"]},
  "categories": {"dependencies": ["dependencies", "injection"], "security": ["security", "oauth"]},
  "rate_limit": 0.5,
  "max_pages": 250
}
```

| Field | Meaning |
|---|---|
| `name` | Skill and folder name; lowercased and hyphenated by the script |
| `base_url` | Only URLs starting with it are crawled |
| `start_urls` | Optional list of entry pages (default: `base_url`) |
| `selectors` | CSS for the main content, the title, the code blocks. If `main_content` misses, the script tries `article`, `main`, `div[role='main']`, `div.content`, `div.document`, `body` |
| `url_patterns` | Substrings: a URL must contain one `include` (if any) and no `exclude` |
| `categories` | `{"file_name": [keywords]}`; a page joins the first category scoring ≥ 2 (keyword in URL +3, title +2, first 500 chars +1); the rest go to `other`. Leave it out and categories come from URL path segments |
| `rate_limit`, `max_pages` | Seconds between requests; crawl size |
| `ref_page_chars`, `ref_code_chars` | Per-page text / per-example code kept in references (default 2500 / 600) |

Find the selectors by fetching one page (`curl -s <url> | head -c 20000`) and looking for the element wrapping the article text: usually `<article>`, `<main>` or `div[role=main]`.

### Step 3 — Build

```bash
python "$SKILL_DIR/scripts/doc_scraper.py" --config fastapi.json --out doc2skill-output --max-pages 20
python "$SKILL_DIR/scripts/doc_scraper.py" --config fastapi.json --out doc2skill-output
python "$SKILL_DIR/scripts/doc_scraper.py" --name mylib --markdown-dir mylib/docs --out doc2skill-output
python "$SKILL_DIR/scripts/doc_scraper.py" --config fastapi.json --out doc2skill-output --skip-scrape
```

Markdown docs with no folder structure all land in `other.md`: pass `--config` holding `name` and `categories` together with `--markdown-dir` to sort them.

After the test run, open `doc2skill-output/<name>_data/summary.json` and one file in `doc2skill-output/<name>/references/`. Real paragraphs and code there mean the selectors are right; then run the full crawl.

Output:
```
doc2skill-output/
├── <name>_data/           cache: pages/*.json + summary.json (reused by --skip-scrape)
└── <name>/
    ├── SKILL.md           generic draft, replaced in step 4
    ├── references/        index.md + one <category>.md per category
    ├── scripts/  assets/  empty, for the user
```

### Step 4 — Write the real SKILL.md

Copy the draft to `SKILL.md.backup`, read `index.md` in `references/`, then every category file (for a large one, its headings first, then the pages that matter). Write SKILL.md with these parts:

1. **Frontmatter:** `name` = folder name (lowercase, hyphens, ≤ 64 chars); `description` ≤ 1024 chars saying what the library is and listing concrete triggers ("Use when writing FastAPI path operations, dependencies, OAuth2 security…").
2. **When to Use** — specific tasks and question types, with the library's real terms.
3. **Quick Reference** — 5 to 10 of the best examples from the references, 5–20 lines each, language tag, one line saying when to use it. Simple first, then intermediate.
4. **Key Concepts** — the library's core terms, one or two lines each.
5. **Reference Files** — what each `references/*.md` holds and when to open it.
6. **Working with This Skill** — where a beginner starts, where to look up a specific API, where advanced topics are.

A Quick Reference entry, good vs. generic:

````markdown
**Declare a dependency** — share logic (auth, DB session) across endpoints:
```python
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```
````

The generic version — "**Pattern 1:** Example pattern" over a truncated block with no context — tells a future session nothing it can act on.

Aim for 150–400 lines. When the skill goes into this user's `~/.claude/skills/`, also add `domain: content`, `composable: true`, `yields_to: [process, craft]` to the frontmatter and a short composability section per `~/.claude/skills/PROTOCOL.md`, because every skill there follows SIP.

### Step 5 — Verify, package, install

- Check every code block: its first meaningful line is found by `grep -rF "<line>" references/`. Rewrite or drop any that is not.
- Package (checks name/folder, description length, missing reference files; leaves out `.backup` files):
  ```bash
  python "$SKILL_DIR/scripts/package_skill.py" doc2skill-output/<name>
  ```
  The zip holds `<name>/SKILL.md` + `references/` — upload it in Claude's Skills settings.
- Claude Code: after the user says yes, copy `doc2skill-output/<name>/` to `~/.claude/skills/<name>/` (personal) or `<project>/.claude/skills/<name>/` (one project). Leave out `SKILL.md.backup`.

## Troubleshooting

| Symptom | Cause → Fix |
|---|---|
| `⚠ No content` on most pages | `main_content` selector wrong → inspect one page, set the right one |
| Only the first page scraped | Links leave `base_url`, or `include` too strict → widen them, or add `start_urls` |
| Pages empty although the browser shows text | Site renders with JavaScript → use repo markdown or `llms-full.txt` |
| Almost everything in `other.md` | Category keywords miss → add keywords seen in the URLs, rebuild with `--skip-scrape` |
| `⊘ robots.txt disallows` | Site asks crawlers to stay out → use another source |
| 403 / 429 errors | Blocked or rate-limited → raise `rate_limit`, or use another source |

## Boundaries

- Builds skills from existing documentation only. A skill that encodes a workflow, a voice or a judgment is skill-creator's work.
- Reads public pages only: no logins, paywalls, CAPTCHAs, and robots.txt is obeyed.
- Copies documentation into the skill: fine for the user's own use; before sharing the zip publicly, check the docs' license.
- Uses no API key: Claude, in this session, writes SKILL.md. The original repo's `enhance_skill.py` API mode is not part of this skill.

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: process
composable: true
yields_to: []
```

doc2skill owns **process** for one job — documentation → crawl → references → SKILL.md → zip/install. The step order and the output layout are fixed.

### When doc2skill Leads

- Any request to build or refresh a skill from a docs site, a repo's docs folder or `llms-full.txt`
- Packaging a skill folder into an uploadable zip

### When doc2skill Defers

| Other Skill's Domain | What doc2skill Does |
|---|---|
| **Process** (skill-creator) | Advisory: follows skill-creator's writing rules for SKILL.md (position, examples, imperative voice). doc2skill keeps the pipeline; a request for a behaviour skill without source docs goes to skill-creator. |
| **Density** (caveman, compress) | Compresses chat messages only. Generated SKILL.md and references keep full examples and tables. |
| **Content** (researcher, documenter) | Takes their findings as an extra source when the user asks; the docs stay the source of truth for examples. |
| **Voice** | Applies to chat; SKILL.md stays in plain imperative instructions. |

### Conflict Signal

> `⚠️ Process conflict: <other skill> wants <X>; doc2skill keeps <pipeline step / file layout>. <What was preserved>.`

**Remember: test crawl first, copy examples from the references, and ask before a big crawl or an install into `~/.claude/skills/`.**
