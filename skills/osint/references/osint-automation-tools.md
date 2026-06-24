# OSINT Automation Tools & Patterns

## Primary Tool: osint_core.py v2

Python-based OSINT engine with ZERO external dependencies (uses only stdlib). Lives at `scripts/osint_core.py`.

### What's New in v2

1. **Content-based username verification** — checks response body for "user not found" indicators, not just HTTP 200
2. **Recursive discovery engine** — one identifier spawns investigations of all discovered identifiers (depth-limited)
3. **GitHub deep-dive** — commit email mining, org extraction, co-author discovery, starred repos, gists
4. **Investigation graph** — tracks all identifiers and their relationships as a directed graph
5. **Username permutation engine** — generates case variations, separator swaps, number suffixes, leet speak
6. **Confidence levels** — CONFIRMED, PROBABLE, POSSIBLE, NOT_FOUND (never just "found")
7. **50+ sites with site-specific verification patterns** — each site has its own positive/negative indicators

### Confidence Levels (Critical Fix)

The #1 problem with v1: HTTP 200 does NOT mean the user exists. Many sites return 200 with a
"user not found" page or redirect to a signup page. v2 checks the response body:

| Level | Meaning | How |
|-------|---------|-----|
| CONFIRMED | Definitely exists | API returned data, or page has profile-specific content |
| PROBABLE | Likely exists | 200 with site content, no "not found" indicators |
| POSSIBLE | Might exist | Ambiguous — some positive, some negative indicators |
| NOT_FOUND | Does not exist | 404, or 200 with "user not found" / signup page |

### Recursive Discovery

The "viral" component. Start with one identifier, discover more, investigate those, repeat.

```
username "xmrnoobx"
  ├── GitHub → email: xmrnoobx@proton.me
  │   ├── email OSINT → breach data
  │   └── commit emails → xmrnoobx@gmail.com
  │       └── email OSINT → more breach data
  ├── Reddit → karma, subreddits
  ├── Steam → games, friends
  ├── [50+ other platforms]
  └── Username permutations → more accounts
```

Default depth: 3 hops. Stops when graph is saturated or max depth reached.

### GitHub Deep-Dive

GitHub is the #1 OSINT goldmine. The `github_deep_dive` command extracts:

- Profile (name, email, location, company, blog, Twitter)
- Commit emails (often personal gmail/proton, different from profile)
- Co-authors from commit messages
- Organizations (workplace, teams)
- Repos (languages, topics, descriptions, homepages)
- Starred repos (interests, technologies)
- Gists (code, configs, sometimes credentials)
- Events (recent activity, active repos)

**Always set GITHUB_TOKEN** — 5,000 req/hr vs 60 without.

### Quick Start

```bash
# Full recursive recon (recommended)
python scripts/osint_core.py orchestrator xmrnoobx username

# GitHub deep-dive only
python scripts/osint_core.py github xmrnoobx

# Verified username search
python scripts/osint_core.py username xmrnoobx

# Email OSINT
python scripts/osint_core.py email user@example.com

# Recursive discovery only (no HTML report)
python scripts/osint_core.py discover xmrnoobx username
```

### API Keys (env vars, all optional)

| Key | Service | Free Tier |
|-----|---------|-----------|
| GITHUB_TOKEN | GitHub API | 5k req/hr (vs 60 without) |
| HIBP_API_KEY | Have I Been Pwned | Paid ($3.50/month) |
| SHODAN_API_KEY | Shodan | Limited free |
| IPINFO_TOKEN | ipinfo.io | 50k req/month |
| VT_API_KEY | VirusTotal | 4 req/min free |
| ABUSEIPDB_KEY | AbuseIPDB | 1k req/day free |
| NUMVERIFY_API_KEY | NumVerify | 100 req/month free |
| INTELX_API_KEY | IntelX | Limited free |

### Supplementary Bash Scripts

For environments where CLI tools are installed (sherlock, maigret, holehe, etc.):
- `username_enum.sh` — Sherlock (400+ sites) + Maigret (3000+ sites)
- `email_osint.sh` — Holehe (120+ platforms) + HIBP + h8mail
- `domain_recon.sh` — theHarvester + Subfinder + crt.sh
- `setup.sh` — One-command installer for all CLI tools

These are supplementary — osint_core.py is the primary engine.
