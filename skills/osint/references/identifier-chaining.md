# Identifier Chaining — How to Propagate Identifiers

> Reference for the /osint skill. Explains how to extract and chain identifiers
> from OSINT findings to build a complete intelligence picture.

---

## The Identifier Graph

Every investigation builds a directed graph:

```
Nodes = identifiers (username, email, phone, name, domain, IP, URL, location, company)
Edges = relationships (discovered_from, same_person, same_org, uses, owns)
```

The graph starts with one node (the target) and grows as each investigation
discovers new identifiers. The key insight: **every piece of data contains
identifiers, and every identifier contains more data.**

---

## Identifier Extraction Rules

### From Emails

An email `john.doe@company.com` contains:

| Extracted Identifier | Type | How |
|---------------------|------|-----|
| `johndoe` | username | Local part (before @) |
| `john.doe` | username | Local part with separator |
| `john` | name | First part of local part |
| `doe` | name | Second part of local part |
| `company.com` | domain | Domain part (after @) |
| `Company` | company | Domain name, capitalized |

**Also try:**
- Remove separators: `johndoe`, `john_doe`, `johndoe1`
- Swap name order: `doejohn`, `doe.john`
- Add common suffixes: `johndoe1`, `johndoeofficial`

### From Usernames

A username `xmrnoobx` can be searched on:

| Action | Result |
|--------|--------|
| Search on 50+ sites | Find accounts → extract bios, emails, names |
| Check GitHub API | Get profile (name, email, location, company, blog, Twitter) |
| Check commit history | Get commit emails (often personal gmail/proton) |
| Generate permutations | Check `XMrNooBX`, `xmr_nooBx`, `xmrnoobx1`, etc. |
| Search Google | Find mentions in forums, paste sites, cached pages |

### From Domains

A domain `company.com` contains:

| Extracted Identifier | Type | How |
|---------------------|------|-----|
| Subdomains | domain | crt.sh, DNS enumeration |
| IP addresses | ip | DNS A records |
| Email addresses | email | WHOIS, security.txt, website |
| Employee names | name | Website, LinkedIn, press |
| Technologies | info | HTTP headers, WhatWeb |
| Login portals | url | robots.txt, directory listing |

### From GitHub Profiles

A GitHub profile is an identifier goldmine:

| Field | Identifier Type | Example |
|-------|----------------|---------|
| `login` | username | `xmrnoobx` |
| `name` | name | `John Doe` |
| `email` | email | `john@proton.me` |
| `blog` | url | `https://johndoe.com` |
| `twitter_username` | username | `@johndoe` |
| `company` | company | `@acme-corp` |
| `location` | location | `San Francisco, CA` |
| Commit author emails | email | `johndoe@gmail.com` |
| Commit co-author emails | email | `colleague@company.com` |
| Repo descriptions | info | Project descriptions |
| Starred repos | interests | Technology preferences |
| Org memberships | company | Workplace affiliations |

### From IP Addresses

An IP `1.2.3.4` can reveal:

| Action | Result |
|--------|--------|
| Reverse DNS | Domain name |
| Shodan | Open ports, services, organization |
| ipinfo.io | City, region, country, org, timezone |
| AbuseIPDB | Abuse reports, reputation |
| VirusTotal | Malicious associations |

---

## Chaining Strategies

### Strategy 1: Breadth-First (Recommended)

Investigate all identifiers at the current depth before going deeper.

```
Depth 0: [username] → find 5 emails, 3 usernames
Depth 1: [5 emails, 3 usernames] → find 10 more emails, 8 more usernames
Depth 2: [10 emails, 8 usernames] → find 15 more, but mostly duplicates
Depth 3: saturated → stop
```

**Pros:** Catches the most identifiers, good coverage
**Cons:** Uses more API calls, takes longer

### Strategy 2: Depth-First

Follow the most promising identifier chain as deep as possible.

```
username → GitHub → commit email → breach data → leaked password → ...
```

**Pros:** Deep investigation of one chain
**Cons:** May miss other chains

### Strategy 3: Priority-Based (Best)

Combine breadth-first with priority scoring. Investigate high-confidence,
high-information identifiers first.

**Priority scoring:**
- GitHub username with public repos → HIGH (reveals emails, orgs, locations)
- Email with breach data → HIGH (reveals passwords, IPs, other accounts)
- Username with many confirmed platforms → MEDIUM (reveals cross-platform presence)
- Domain with many subdomains → MEDIUM (reveals infrastructure)
- Username with no confirmed platforms → LOW (dead end)

---

## Deduplication

Always deduplicate before investigating. Same identifier can be discovered
multiple times from different sources.

**Dedup keys:**
- Emails: lowercase, strip `+` aliases (john+test@gmail.com = john@gmail.com)
- Usernames: lowercase
- Domains: lowercase, strip `www.`
- IPs: normalize (192.168.001.001 = 192.168.1.1)
- Names: lowercase, strip extra spaces

---

## Confidence Propagation

When an identifier is discovered from a high-confidence source, it inherits
high confidence. When discovered from a low-confidence source, it starts low.

| Discovery Source | Initial Confidence |
|-----------------|-------------------|
| GitHub profile email field | 0.95 (almost certainly theirs) |
| GitHub commit author email | 0.90 (theirs, but might be work email) |
| Social media bio link | 0.85 (likely theirs) |
| Username similarity match | 0.40 (might be coincidence) |
| Email local part extraction | 0.50 (might not use same username) |
| Domain WHOIS email | 0.70 (might be privacy-protected) |

**Confidence boosting:** If the same identifier is discovered from multiple
independent sources, increase confidence. 3 sources = very high confidence.

---

## Stopping Conditions

Stop investigating when:

1. **Graph saturated** — no new identifiers discovered in the last depth level
2. **Max depth reached** — default 3 hops from original target
3. **API limits hit** — rate limited on critical APIs
4. **Diminishing returns** — last 10 identifiers produced 0 new findings
5. **All identifier types exhausted** — investigated all emails, usernames, domains, IPs

**Never stop because:**
- "I found enough" — there's always more
- "The target doesn't have GitHub" — they might, under a different username
- "The email doesn't work" — try the username variants

---

## Output: The Investigation Graph

The final output is a JSON graph:

```json
{
  "target": "xmrnoobx",
  "target_type": "username",
  "total_nodes": 47,
  "total_edges": 82,
  "nodes": {
    "xmrnoobx": {
      "identifier": "xmrnoobx",
      "type": "username",
      "sources": ["user_input"],
      "confidence": 1.0,
      "verified": true,
      "data": {"github_followers": 5, "reddit_karma": 1234}
    },
    "xmrnoobx@proton.me": {
      "identifier": "xmrnoobx@proton.me",
      "type": "email",
      "sources": ["github_profile"],
      "confidence": 0.95,
      "verified": true
    }
  },
  "edges": [
    {"from": "xmrnoobx", "to": "xmrnoobx@proton.me",
     "relationship": "discovered_via_github_profile",
     "evidence": "Email field in GitHub profile"}
  ],
  "investigated": ["xmrnoobx", "xmrnoobx@proton.me", "xmrnoobx@gmail.com"]
}
```

This graph is the machine-readable backbone of the intelligence report.
Every finding traces back to how it was discovered and with what confidence.
