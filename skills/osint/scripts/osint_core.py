#!/usr/bin/env python3
"""
OSINT Toolkit v2 — Recursive Intelligence Engine.

MASSIVE improvements over v1:
- Content-based verification (not just HTTP 200 = "found")
- Recursive identifier discovery (email → username → more emails → more accounts)
- GitHub deep-dive (commit emails, orgs, repos, starred, gists)
- Investigation graph (tracks all identifiers and their relationships)
- Site-specific verification patterns (negative indicators, positive indicators)
- Username permutation engine (case variations, separator swaps, number suffixes)

Usage:
    python osint_core.py orchestrator <target> <type>     # Full recursive recon
    python osint_core.py username <username>               # Verified username search
    python osint_core.py email <email>                     # Email OSINT + recursive
    python osint_core.py github <username>                 # GitHub deep-dive
    python osint_core.py domain <domain>                   # Domain recon
    python osint_core.py ip <ip>                           # IP recon
    python osint_core.py discover <target> <type>          # Recursive discovery only
"""

import urllib.request
import urllib.parse
import urllib.error
import socket
import json
import subprocess
import ssl
import re
import sys
import os
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# --- Config ---
OSINT_OUTPUT_DIR = os.environ.get("OSINT_OUTPUT_DIR", os.path.expanduser("~/osint"))
HIBP_API_KEY = os.environ.get("HIBP_API_KEY", "")
SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN", "")
VT_API_KEY = os.environ.get("VT_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

SSL_CTX = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"


# ============================================================
# UTILITIES
# ============================================================

def http_get(url, headers=None, timeout=10):
    """Safe HTTP GET — returns (status_code, response_text)."""
    try:
        hdrs = {"User-Agent": USER_AGENT}
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, body
    except Exception:
        return 0, ""


def http_get_json(url, headers=None, timeout=10):
    """Safe HTTP GET — returns parsed JSON or empty dict."""
    status, text = http_get(url, headers, timeout)
    try:
        return json.loads(text) if text else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def make_output_dir(tag):
    """Create output directory with timestamp."""
    clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', tag)[:50]
    ts = datetime.now().strftime("%d_%b_%Y")
    out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    return out_dir


def save_json(out_dir, filename, data):
    """Save JSON to data/ subdirectory."""
    path = os.path.join(out_dir, "data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    return path


def log(msg, level="INFO"):
    """Print log message."""
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m",
              "FOUND": "\033[92m", "LINK": "\033[96m"}
    reset = "\033[0m"
    c = colors.get(level, "")
    print(f"{c}[{level}]{reset} {msg}", flush=True)


# ============================================================
# INVESTIGATION GRAPH — Tracks all identifiers and relationships
# ============================================================

class InvestigationGraph:
    """
    Central intelligence graph. Every discovered identifier (username, email,
    phone, domain, IP) is a node. Edges represent relationships (same person,
    same org, discovered from, etc.)

    This is what makes the investigation "viral" — every discovery spawns
    new investigation threads.
    """

    def __init__(self, target, target_type):
        self.target = target
        self.target_type = target_type
        self.nodes = {}  # identifier -> {type, sources, data, verified, confidence}
        self.edges = []  # [{from, to, relationship, evidence}]
        self.investigated = set()  # identifiers already investigated
        self.queue = []  # identifiers to investigate next
        self.timestamp = datetime.now(timezone.utc).isoformat()

        # Seed with initial target
        self.add_node(target, target_type, source="user_input", confidence=1.0)

    def add_node(self, identifier, id_type, source="", data=None, confidence=0.5, verified=False):
        """Add or update a node in the graph."""
        key = identifier.lower().strip()
        if key in self.nodes:
            # Merge — update confidence if higher, add source
            existing = self.nodes[key]
            if confidence > existing.get("confidence", 0):
                existing["confidence"] = confidence
            if verified:
                existing["verified"] = True
            if source and source not in existing.get("sources", []):
                existing.setdefault("sources", []).append(source)
            if data:
                existing.setdefault("data", {}).update(data)
        else:
            self.nodes[key] = {
                "identifier": identifier,
                "type": id_type,
                "sources": [source] if source else [],
                "data": data or {},
                "verified": verified,
                "confidence": confidence,
                "first_seen": datetime.now(timezone.utc).isoformat(),
            }
            # Queue for investigation if not already investigated
            if key not in self.investigated:
                self.queue.append((identifier, id_type))
        return self.nodes[key]

    def add_edge(self, from_id, to_id, relationship, evidence=""):
        """Add a relationship edge."""
        self.edges.append({
            "from": from_id.lower().strip(),
            "to": to_id.lower().strip(),
            "relationship": relationship,
            "evidence": evidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def mark_investigated(self, identifier):
        """Mark an identifier as investigated (don't re-investigate)."""
        self.investigated.add(identifier.lower().strip())

    def get_uninvestigated(self):
        """Get next batch of identifiers to investigate."""
        batch = []
        while self.queue:
            identifier, id_type = self.queue.pop(0)
            if identifier.lower().strip() not in self.investigated:
                batch.append((identifier, id_type))
            if len(batch) >= 10:  # Process in batches
                break
        return batch

    def get_identifiers_by_type(self, id_type):
        """Get all identifiers of a given type."""
        return [k for k, v in self.nodes.items() if v["type"] == id_type]

    def to_dict(self):
        """Serialize the graph."""
        return {
            "target": self.target,
            "target_type": self.target_type,
            "timestamp": self.timestamp,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "nodes": self.nodes,
            "edges": self.edges,
            "investigated": list(self.investigated),
        }


# ============================================================
# USERNAME VERIFICATION — Content-based, not status-based
# ============================================================

# Site-specific verification config
# Each site has:
#   url_template: how to build the URL
#   negative_indicators: strings in response body that mean "user NOT found"
#   positive_indicators: strings that confirm the user EXISTS
#   check_type: 'body' (check response text), 'status' (HTTP status only), 'api' (JSON API)
#   api_key: JSON key that must exist for API-type checks

USERNAME_SITES = {
    # === HIGH CONFIDENCE (API or reliable content check) ===
    "GitHub": {
        "url": "https://api.github.com/users/{username}",
        "check_type": "api",
        "api_key": "login",
        "negative_indicators": ["Not Found"],
        "positive_indicators": [],
        "extract": {"followers": "followers", "repos": "public_repos", "bio": "bio",
                    "name": "name", "email": "email", "location": "location",
                    "company": "company", "blog": "blog", "created": "created_at"},
    },
    "Reddit": {
        "url": "https://www.reddit.com/user/{username}/about.json",
        "check_type": "api",
        "api_key": "data.name",
        "negative_indicators": [],
        "positive_indicators": [],
        "headers": {"User-Agent": "osint-skill/2.0"},
        "extract": {"karma": "data.total_karma", "created": "data.created_utc",
                    "is_mod": "data.is_mod", "has_verified_email": "data.has_verified_email"},
    },
    "GitLab": {
        "url": "https://gitlab.com/api/v4/users?username={username}",
        "check_type": "json_array",  # Returns array, non-empty = found
        "negative_indicators": [],
        "positive_indicators": [],
    },
    "npm": {
        "url": "https://registry.npmjs.org/-/v1/search?text=maintainer:{username}&size=1",
        "check_type": "api",
        "api_key": "objects",
        "negative_indicators": [],
        "positive_indicators": [],
        "extract": {"packages": "objects"},
    },
    "PyPI": {
        "url": "https://pypi.org/user/{username}/",
        "check_type": "body",
        "negative_indicators": ["Page not found", "404", "not been found"],
        "positive_indicators": [],
    },
    "Keybase": {
        "url": "https://keybase.io/_/api/1.0/user/lookup.json?username={username}",
        "check_type": "api",
        "api_key": "them",
        "negative_indicators": [],
        "positive_indicators": [],
    },
    "Twitch": {
        "url": "https://www.twitch.tv/{username}",
        "check_type": "body",
        "negative_indicators": ["Sorry. Unless you\"ve got a time machine"],
        "positive_indicators": ["channel-page", "profile-banner"],
    },
    "Instagram": {
        "url": "https://www.instagram.com/{username}/",
        "check_type": "body",
        "negative_indicators": ["Sorry, this page isn't available", "login"],
        "positive_indicators": ["edge_followed_by", "biography"],
    },
    "Twitter/X": {
        "url": "https://x.com/{username}",
        "check_type": "body",
        "negative_indicators": ["This account doesn't exist", "doesn't exist"],
        "positive_indicators": ["profile"],
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@{username}",
        "check_type": "body",
        "negative_indicators": ["Couldn't find this account", "couldn't find this account"],
        "positive_indicators": ["user-page", "uniqueId"],
    },
    "Pinterest": {
        "url": "https://www.pinterest.com/{username}/",
        "check_type": "body",
        "negative_indicators": ["Sorry, we couldn't find", "page not found"],
        "positive_indicators": ["profile", "followers"],
    },
    "Medium": {
        "url": "https://medium.com/@{username}",
        "check_type": "body",
        "negative_indicators": ["out of the void", "404"],
        "positive_indicators": ["@{username}"],
    },
    "DeviantArt": {
        "url": "https://www.deviantart.com/{username}",
        "check_type": "body",
        "negative_indicators": ["does not exist", "Page Not Found"],
        "positive_indicators": ["deviantart", "profile"],
    },
    "SoundCloud": {
        "url": "https://soundcloud.com/{username}",
        "check_type": "body",
        "negative_indicators": ["We can't find that user", "404"],
        "positive_indicators": ["soundcloud", "profile"],
    },
    "Steam": {
        "url": "https://steamcommunity.com/id/{username}",
        "check_type": "body",
        "negative_indicators": ["The specified profile could not be found"],
        "positive_indicators": ["profile_page", "persona_name"],
    },
    "HackerNews": {
        "url": "https://hacker-news.firebaseio.com/v0/user/{username}.json",
        "check_type": "api",
        "api_key": "id",
        "negative_indicators": ["null"],
        "positive_indicators": [],
        "extract": {"karma": "karma", "created": "created"},
    },
    "Replit": {
        "url": "https://replit.com/@{username}",
        "check_type": "body",
        "negative_indicators": ["404", "not found"],
        "positive_indicators": ["profile"],
    },
    "Kaggle": {
        "url": "https://www.kaggle.com/{username}",
        "check_type": "body",
        "negative_indicators": ["404", "not found"],
        "positive_indicators": ["profile"],
    },
    "Gravatar": {
        "url": "https://en.gravatar.com/{username}.json",
        "check_type": "api",
        "api_key": "entry",
        "negative_indicators": ["User not found"],
        "positive_indicators": [],
        "extract": {"display_name": "entry[0].displayName", "about": "entry[0].about"},
    },
    "Dribbble": {
        "url": "https://dribbble.com/{username}",
        "check_type": "body",
        "negative_indicators": ["404", "not found", "Page not found"],
        "positive_indicators": ["dribbble", "profile"],
    },
    "Behance": {
        "url": "https://www.behance.net/{username}",
        "check_type": "body",
        "negative_indicators": ["404", "not found"],
        "positive_indicators": ["profile"],
    },
    "Flickr": {
        "url": "https://www.flickr.com/people/{username}/",
        "check_type": "body",
        "negative_indicators": ["member not found", "doesn't exist"],
        "positive_indicators": ["profile"],
    },
    "Vimeo": {
        "url": "https://vimeo.com/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "Spotify": {
        "url": "https://open.spotify.com/user/{username}",
        "check_type": "body",
        "negative_indicators": ["not found"],
        "positive_indicators": ["profile"],
    },
    "Imgur": {
        "url": "https://imgur.com/user/{username}",
        "check_type": "body",
        "negative_indicators": ["Zoinks! You've taken a wrong turn"],
        "positive_indicators": ["profile"],
    },
    "Giphy": {
        "url": "https://giphy.com/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "Roblox": {
        "url": "https://users.roblox.com/v1/users/search?keyword={username}&limit=10",
        "check_type": "json_search",  # Search results — check if exact match exists
        "negative_indicators": [],
        "positive_indicators": [],
    },
    "Duolingo": {
        "url": "https://www.duolingo.com/2017-06-30/users?username={username}",
        "check_type": "api",
        "api_key": "users",
        "negative_indicators": [],
        "positive_indicators": [],
    },
    "Chess.com": {
        "url": "https://api.chess.com/pub/player/{username}",
        "check_type": "api",
        "api_key": "username",
        "negative_indicators": [],
        "positive_indicators": [],
        "extract": {"name": "name", "title": "title", "followers": "followers",
                    "country": "country", "joined": "joined", "status": "status"},
    },
    "Letterboxd": {
        "url": "https://letterboxd.com/{username}/",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "Error"],
        "positive_indicators": ["profile"],
    },
    "Strava": {
        "url": "https://www.strava.com/athletes/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "Last.fm": {
        "url": "https://www.last.fm/user/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "doesn't exist"],
        "positive_indicators": ["profile"],
    },
    "Wattpad": {
        "url": "https://www.wattpad.com/user/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "Goodreads": {
        "url": "https://www.goodreads.com/{username}",
        "check_type": "body",
        "negative_indicators": ["Page not found", "404"],
        "positive_indicators": ["profile"],
    },
    "MyAnimeList": {
        "url": "https://myanimelist.net/profile/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "Bad Gateway"],
        "positive_indicators": ["profile"],
    },
    "Bandcamp": {
        "url": "https://{username}.bandcamp.com",
        "check_type": "body",
        "negative_indicators": ["not found", "Sorry, that something"],
        "positive_indicators": ["bandcamp"],
    },
    "500px": {
        "url": "https://500px.com/p/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "ReverbNation": {
        "url": "https://www.reverbnation.com/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "ProductHunt": {
        "url": "https://www.producthunt.com/@{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "CodePen": {
        "url": "https://codepen.io/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "Bitbucket": {
        "url": "https://api.bitbucket.org/2.0/users/{username}",
        "check_type": "api",
        "api_key": "username",
        "negative_indicators": [],
        "positive_indicators": [],
    },
    "Patreon": {
        "url": "https://www.patreon.com/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "does not exist"],
        "positive_indicators": ["patreon", "profile"],
    },
    "About.me": {
        "url": "https://about.me/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "doesn't exist"],
        "positive_indicators": ["profile"],
    },
    "Linktree": {
        "url": "https://linktr.ee/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "doesn't exist"],
        "positive_indicators": ["linktree"],
    },
    "Mastodon": {
        "url": "https://mastodon.social/@{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404", "is not available"],
        "positive_indicators": ["profile"],
    },
    "CashApp": {
        "url": "https://cash.app/${username}",
        "check_type": "body",
        "negative_indicators": ["not found"],
        "positive_indicators": ["cash"],
    },
    "Venmo": {
        "url": "https://venmo.com/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["venmo", "profile"],
    },
    "AllTrails": {
        "url": "https://www.alltrails.com/members/{username}",
        "check_type": "body",
        "negative_indicators": ["not found", "404"],
        "positive_indicators": ["profile"],
    },
    "HackerNews_alt": {
        "url": "https://news.ycombinator.com/user?id={username}",
        "check_type": "body",
        "negative_indicators": ["No such user"],
        "positive_indicators": ["hackernews", "karma"],
    },
}


def verify_username_site(name, site_config, username, timeout=10):
    """
    Verify if a username exists on a site using CONTENT-BASED verification.
    Returns confidence: CONFIRMED, PROBABLE, POSSIBLE, NOT_FOUND, ERROR
    """
    url = site_config["url"].format(username=username)
    headers = site_config.get("headers", {})

    status, body = http_get(url, headers=headers, timeout=timeout)

    if status == 0:
        return {"site": name, "url": url, "status": "error", "confidence": "ERROR", "http_status": 0}

    check_type = site_config.get("check_type", "body")
    neg = site_config.get("negative_indicators", [])
    pos = site_config.get("positive_indicators", [])

    result = {
        "site": name,
        "url": url,
        "http_status": status,
        "confidence": "NOT_FOUND",
        "status": "not_found",
    }

    # --- API type: JSON response with specific key ---
    if check_type == "api":
        try:
            data = json.loads(body) if body else {}
        except (json.JSONDecodeError, ValueError):
            data = {}

        api_key = site_config.get("api_key", "")
        # Navigate nested keys like "data.name"
        val = data
        for part in api_key.split("."):
            if isinstance(val, dict):
                val = val.get(part)
            elif isinstance(val, list) and part.isdigit():
                idx = int(part)
                val = val[idx] if idx < len(val) else None
            else:
                val = None
                break

        if val is not None and val and str(val).lower() not in ("null", "none", ""):
            result["confidence"] = "CONFIRMED"
            result["status"] = "found"
            # Extract extra data
            extract = site_config.get("extract", {})
            if extract:
                result["extracted"] = {}
                for field, path in extract.items():
                    ev = data
                    for p in path.split("."):
                        if isinstance(ev, dict):
                            ev = ev.get(p)
                        elif isinstance(ev, list) and p.isdigit():
                            idx = int(p)
                            ev = ev[idx] if idx < len(val) else None
                        else:
                            ev = None
                            break
                    if ev is not None:
                        result["extracted"][field] = ev
        elif status == 404:
            result["confidence"] = "NOT_FOUND"
        else:
            # API returned but no key — might be rate limited or changed
            result["confidence"] = "NOT_FOUND"

    # --- JSON array type: non-empty array = found ---
    elif check_type == "json_array":
        try:
            data = json.loads(body) if body else []
        except (json.JSONDecodeError, ValueError):
            data = []
        if isinstance(data, list) and len(data) > 0:
            result["confidence"] = "CONFIRMED"
            result["status"] = "found"
        else:
            result["confidence"] = "NOT_FOUND"

    # --- JSON search type: search results, check for exact username match ---
    elif check_type == "json_search":
        try:
            data = json.loads(body) if body else {}
        except (json.JSONDecodeError, ValueError):
            data = {}
        # Roblox-style: data.data[].name exact match
        users = data.get("data", [])
        for u in users:
            if isinstance(u, dict) and u.get("name", "").lower() == username.lower():
                result["confidence"] = "CONFIRMED"
                result["status"] = "found"
                break

    # --- Body type: check response text for positive/negative indicators ---
    elif check_type == "body":
        body_lower = body.lower() if body else ""

        # Check negative indicators first (user NOT found)
        has_negative = any(neg_str.lower() in body_lower for neg_str in neg if neg_str)
        # Check positive indicators (user IS found)
        has_positive = any(
            pos_str.lower().replace("{username}", username.lower()) in body_lower
            for pos_str in pos if pos_str
        )

        if status == 404:
            result["confidence"] = "NOT_FOUND"
        elif has_negative and not has_positive:
            result["confidence"] = "NOT_FOUND"
        elif has_positive and not has_negative:
            result["confidence"] = "CONFIRMED"
            result["status"] = "found"
        elif has_positive and has_negative:
            # Ambiguous — positive indicators found but also negative ones
            result["confidence"] = "POSSIBLE"
            result["status"] = "possible"
        elif status == 200 and not neg and not pos:
            # No indicators defined — fall back to status but mark as low confidence
            result["confidence"] = "POSSIBLE"
            result["status"] = "possible"
        elif status == 200:
            # Has indicator definitions but neither matched — likely not found
            result["confidence"] = "NOT_FOUND"
        elif status == 403:
            result["confidence"] = "POSSIBLE"
            result["status"] = "possible"
        else:
            result["confidence"] = "NOT_FOUND"

    return result


def username_enum(username, out_dir=None, max_workers=25):
    """
    Enumerate username across 50+ sites with CONTENT-BASED verification.
    Returns confidence levels: CONFIRMED, PROBABLE, POSSIBLE, NOT_FOUND.
    """
    out_dir = out_dir or make_output_dir(f"username_{username}")
    log(f"=== Username Enumeration: {username} ===")
    log(f"Checking {len(USERNAME_SITES)} sites with {max_workers} threads (content-verified)...")

    results = []
    confirmed = []
    possible = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(verify_username_site, name, config, username): name
            for name, config in USERNAME_SITES.items()
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["confidence"] == "CONFIRMED":
                confirmed.append(result)
                log(f"  [✓] {result['site']}: {result['url']}", "FOUND")
            elif result["confidence"] in ("PROBABLE", "POSSIBLE"):
                possible.append(result)
                log(f"  [?] {result['site']}: {result['url']} ({result['confidence']})", "WARN")

    report = {
        "target": username,
        "type": "username",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_sites_checked": len(results),
        "confirmed_count": len(confirmed),
        "possible_count": len(possible),
        "confirmed": confirmed,
        "possible": possible,
        "all_results": results,
    }

    save_json(out_dir, "username_enum.json", report)
    log(f"=== Summary: {len(confirmed)} CONFIRMED, {len(possible)} POSSIBLE / {len(USERNAME_SITES)} sites ===", "OK")
    return report


# ============================================================
# USERNAME PERMUTATION ENGINE
# ============================================================

def generate_username_permutations(username):
    """
    Generate common username variations. People reuse patterns.

    "xmrnoobx" → ["XMrNooBX", "xmr_nooBx", "xmr-noobx", "xmrnoobx1",
                    "xmrnoobxx", "the_xmrnoobx", "real_xmrnoobx", ...]
    """
    perms = set()
    base = username.lower()

    # Original + case variations
    perms.add(base)
    perms.add(username)  # Original case
    perms.add(base.upper())
    perms.add(base.capitalize())
    # Title case for multi-part names
    if "_" in base or "-" in base or "." in base:
        sep = "_" if "_" in base else ("-" if "-" in base else ".")
        parts = base.split(sep)
        perms.add(sep.join(p.capitalize() for p in parts))
        perms.add(sep.join(p.upper() for p in parts))

    # Separator swaps
    for sep_from, sep_to in [("_", "-"), ("-", "_"), (".", "_"), ("_", "."),
                              ("-", "."), (".", "-")]:
        if sep_from in base:
            perms.add(base.replace(sep_from, sep_to))

    # Add/remove separators
    if "_" not in base and "-" not in base and "." not in base:
        # Try inserting separators at common positions
        if len(base) > 4:
            mid = len(base) // 2
            perms.add(base[:mid] + "_" + base[mid:])
            perms.add(base[:mid] + "-" + base[mid:])
            perms.add(base[:mid] + "." + base[mid:])
    else:
        # Remove separators
        for sep in ["_", "-", "."]:
            perms.add(base.replace(sep, ""))

    # Number suffixes
    for n in ["1", "2", "3", "0", "01", "007", "420", "69", "666", "13",
              "00", "001", "01", "123", "99", "100"]:
        perms.add(base + n)
        perms.add(username + n)  # Original case

    # Number prefixes
    for n in ["1", "0"]:
        perms.add(n + base)

    # Common prefixes
    for prefix in ["the", "real", "its", "im", "mr", "ms", "dr", "x", "xx"]:
        perms.add(prefix + base)
        perms.add(prefix + "_" + base)

    # Common suffixes
    for suffix in ["official", "real", "yt", "tv", "ttv", "xd", "lol", "og",
                   "gaming", "dev", "tech", "code", "art"]:
        perms.add(base + suffix)
        perms.add(base + "_" + suffix)

    # Leet speak substitutions
    leet_map = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
    leet = base
    for char, replacement in leet_map.items():
        leet = leet.replace(char, replacement)
    if leet != base:
        perms.add(leet)

    # Remove empty and very long ones
    perms = {p for p in perms if p and len(p) <= 30 and len(p) >= 2}

    return sorted(perms)


# ============================================================
# GITHUB DEEP DIVE — The goldmine
# ============================================================

def github_deep_dive(username, out_dir=None):
    """
    Deep GitHub intelligence gathering. GitHub is the #1 OSINT goldmine for
    developers — commit emails, org memberships, repo topics, starred repos,
    contribution patterns, and more.
    """
    out_dir = out_dir or make_output_dir(f"github_{username}")
    log(f"=== GitHub Deep Dive: {username} ===")

    gh_headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        gh_headers["Authorization"] = f"token {GITHUB_TOKEN}"

    report = {
        "target": username,
        "type": "github",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identifiers_found": [],  # Emails, usernames, names found
        "organizations": [],
        "repos": [],
        "emails_from_commits": set(),
        "emails_from_profile": [],
        "usernames_from_repos": [],  # Co-authors, contributors
        "languages": defaultdict(int),
        "topics": set(),
        "starred_count": 0,
        "gist_count": 0,
    }

    # 1. User profile
    log("Fetching user profile...")
    user = http_get_json(f"https://api.github.com/users/{username}", gh_headers)
    if "login" in user:
        report["profile"] = {
            "name": user.get("name"),
            "bio": user.get("bio"),
            "company": user.get("company"),
            "location": user.get("location"),
            "email": user.get("email"),
            "blog": user.get("blog"),
            "twitter": user.get("twitter_username"),
            "public_repos": user.get("public_repos", 0),
            "public_gists": user.get("public_gists", 0),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
            "avatar_url": user.get("avatar_url"),
            "html_url": user.get("html_url"),
        }
        report["gist_count"] = user.get("public_gists", 0)

        # Extract identifiers from profile
        if user.get("email"):
            report["emails_from_profile"].append(user["email"])
            report["identifiers_found"].append({"type": "email", "value": user["email"], "source": "github_profile"})
        if user.get("name"):
            report["identifiers_found"].append({"type": "name", "value": user["name"], "source": "github_profile"})
        if user.get("twitter_username"):
            report["identifiers_found"].append({"type": "username", "value": user["twitter_username"],
                                                 "source": "github_twitter", "platform": "twitter"})
        if user.get("blog"):
            report["identifiers_found"].append({"type": "url", "value": user["blog"], "source": "github_blog"})
        if user.get("company"):
            report["identifiers_found"].append({"type": "company", "value": user["company"], "source": "github_profile"})
        if user.get("location"):
            report["identifiers_found"].append({"type": "location", "value": user["location"], "source": "github_profile"})

        log(f"Profile: {user.get('name', 'N/A')} | {user.get('public_repos', 0)} repos | "
            f"{user.get('followers', 0)} followers | email: {user.get('email', 'hidden')}", "OK")
    else:
        log("User not found on GitHub", "WARN")
        save_json(out_dir, "github_deep_dive.json", report)
        return report

    # 2. Organizations
    log("Fetching organizations...")
    orgs = http_get_json(f"https://api.github.com/users/{username}/orgs", gh_headers)
    if isinstance(orgs, list):
        for org in orgs[:20]:
            org_info = {
                "login": org.get("login"),
                "description": org.get("description"),
                "url": org.get("html_url"),
                "avatar": org.get("avatar_url"),
            }
            report["organizations"].append(org_info)
            log(f"  Org: {org.get('login')}", "LINK")
    log(f"Organizations: {len(report['organizations'])}", "OK")

    # 3. Repositories (up to 100)
    log("Fetching repositories...")
    repos = http_get_json(
        f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100",
        gh_headers
    )
    if isinstance(repos, list):
        for repo in repos[:100]:
            repo_info = {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "topics": repo.get("topics", []),
                "fork": repo.get("fork", False),
                "homepage": repo.get("homepage"),
            }
            report["repos"].append(repo_info)

            # Track languages
            if repo.get("language"):
                report["languages"][repo["language"]] += 1

            # Track topics
            for topic in repo.get("topics", []):
                report["topics"].add(topic)

        log(f"Repositories: {len(repos)}", "OK")

    # 4. Commit email mining — check top repos for commit emails
    log("Mining commit emails from top repos...")
    top_repos = sorted(
        [r for r in report["repos"] if not r.get("fork")],
        key=lambda r: r.get("stars", 0) + r.get("forks", 0),
        reverse=True
    )[:5]

    for repo in top_repos:
        repo_name = repo["full_name"]
        log(f"  Checking commits in {repo_name}...")
        commits = http_get_json(
            f"https://api.github.com/repos/{repo_name}/commits?per_page=30",
            gh_headers
        )
        if isinstance(commits, list):
            for commit in commits[:30]:
                author = commit.get("commit", {}).get("author", {})
                committer = commit.get("commit", {}).get("committer", {})

                for person in [author, committer]:
                    email = person.get("email", "")
                    name = person.get("name", "")
                    if email and email not in ("noreply@github.com",) and not email.endswith("[noreply]"):
                        report["emails_from_commits"].add(email)
                        report["identifiers_found"].append({
                            "type": "email", "value": email,
                            "source": f"commit_in_{repo_name}",
                            "commit_name": name
                        })
                        log(f"    Email: {email} ({name})", "FOUND")

                # Check co-authors in commit message
                msg = commit.get("commit", {}).get("message", "")
                co_authors = re.findall(r'Co-authored-by:\s*(.+?)\s*<(.+?)>', msg)
                for co_name, co_email in co_authors:
                    if co_email not in ("noreply@github.com",):
                        report["emails_from_commits"].add(co_email)
                        report["identifiers_found"].append({
                            "type": "email", "value": co_email,
                            "source": f"co-author_in_{repo_name}",
                            "commit_name": co_name
                        })
                        report["usernames_from_repos"].append({
                            "name": co_name, "email": co_email,
                            "source": f"co-author_in_{repo_name}"
                        })
                        log(f"    Co-author: {co_name} <{co_email}>", "FOUND")

    report["emails_from_commits"] = sorted(report["emails_from_commits"])
    report["topics"] = sorted(report["topics"])
    report["languages"] = dict(report["languages"])

    # 5. Gists — often contain code, configs, even credentials
    if report["gist_count"] > 0:
        log(f"Fetching gists ({report['gist_count']} public)...")
        gists = http_get_json(
            f"https://api.github.com/users/{username}/gists?per_page=30",
            gh_headers
        )
        if isinstance(gists, list):
            report["gists"] = [{
                "id": g.get("id"),
                "description": g.get("description"),
                "url": g.get("html_url"),
                "files": list(g.get("files", {}).keys()),
                "created_at": g.get("created_at"),
            } for g in gists[:30]]
            log(f"Gists: {len(gists)}", "OK")

    # 6. Starred repos — reveals interests
    log("Fetching starred repos...")
    starred = http_get_json(
        f"https://api.github.com/users/{username}/starred?per_page=30",
        gh_headers
    )
    if isinstance(starred, list):
        report["starred"] = [{
            "name": s.get("full_name"),
            "description": s.get("description"),
            "language": s.get("language"),
            "stars": s.get("stargazers_count"),
        } for s in starred[:30]]
        report["starred_count"] = len(starred)
        log(f"Starred repos: {len(starred)}", "OK")

    # 7. Events — recent activity (pushes, PRs, issues)
    log("Fetching recent events...")
    events = http_get_json(
        f"https://api.github.com/users/{username}/events/public?per_page=30",
        gh_headers
    )
    if isinstance(events, list):
        # Extract repo names from events (reveals which repos they contribute to)
        event_repos = set()
        for evt in events[:30]:
            repo_name = evt.get("repo", {}).get("name", "")
            if repo_name:
                event_repos.add(repo_name)
        report["active_repos"] = sorted(event_repos)
        log(f"Active repos from events: {len(event_repos)}", "OK")

    # Convert sets for JSON serialization
    report["emails_from_commits"] = sorted(report["emails_from_commits"])
    report["topics"] = sorted(report["topics"])

    save_json(out_dir, "github_deep_dive.json", report)
    log(f"=== GitHub Deep Dive complete: {len(report['identifiers_found'])} identifiers found ===", "OK")
    return report


# ============================================================
# EMAIL OSINT
# ============================================================

def email_osint(email, out_dir=None):
    """Email OSINT: platform check + domain analysis + breach check + username extraction."""
    out_dir = out_dir or make_output_dir(f"email_{email.split('@')[0]}")
    log(f"=== Email OSINT: {email} ===")

    report = {
        "target": email,
        "type": "email",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identifiers_found": [],
    }

    # Domain analysis
    domain = email.split("@")[1]
    log(f"Analyzing domain: {domain}")

    # MX records
    mx_records = []
    try:
        result = subprocess.run(["nslookup", "-type=MX", domain], capture_output=True, text=True, timeout=10)
        mx_records = re.findall(r'mail exchanger = (.+)', result.stdout)
    except Exception:
        pass

    # TXT records
    spf = ""
    dmarc = ""
    try:
        result = subprocess.run(["nslookup", "-type=TXT", domain], capture_output=True, text=True, timeout=10)
        for line in result.stdout.split("\n"):
            if "spf" in line.lower():
                spf = line.strip()
            if "dmarc" in line.lower():
                dmarc = line.strip()
    except Exception:
        pass

    report["domain_analysis"] = {
        "domain": domain,
        "mx_records": mx_records,
        "spf": spf,
        "dmarc": dmarc,
    }
    log(f"MX: {mx_records}", "OK")

    # Extract username from email
    username = email.split("@")[0]
    # Common patterns: john.doe, john_doe, johndoe, j.doe
    username_variants = [username]
    for sep in [".", "_", "-"]:
        if sep in username:
            parts = username.split(sep)
            username_variants.extend(parts)  # Individual parts
            username_variants.append(sep.join(parts))  # Full with separator

    report["username_variants"] = username_variants
    for variant in username_variants:
        if len(variant) >= 3:  # Skip very short fragments
            report["identifiers_found"].append({
                "type": "username", "value": variant,
                "source": f"email_local_part_{email}"
            })

    # HIBP breach check
    if HIBP_API_KEY:
        log("Checking HIBP breaches...")
        breaches = http_get_json(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{urllib.parse.quote(email)}?truncateResponse=false",
            headers={"hibp-api-key": HIBP_API_KEY, "user-agent": "osint-skill"}
        )
        if isinstance(breaches, list):
            report["breaches"] = breaches
            report["breach_count"] = len(breaches)
            log(f"HIBP: {len(breaches)} breaches found", "OK")
        else:
            report["breaches"] = []
            report["breach_count"] = 0
    else:
        log("HIBP_API_KEY not set — skipping breach check", "WARN")
        report["breaches"] = []
        report["breach_count"] = 0

    save_json(out_dir, "email_osint.json", report)
    log(f"=== Email OSINT complete ===", "OK")
    return report


# ============================================================
# DOMAIN RECON
# ============================================================

def dns_query(domain, record_type):
    """DNS lookup using nslookup (cross-platform)."""
    try:
        result = subprocess.run(
            ["nslookup", f"-type={record_type}", domain],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.split("\n")
        records = []
        for line in lines:
            line = line.strip()
            if record_type == "A" and "Address:" in line and not line.startswith("Server:"):
                addr = line.split("Address:")[-1].strip()
                if addr and ":" not in addr:
                    records.append(addr)
            elif record_type == "MX" and "mail exchanger" in line:
                records.append(line.split("=")[-1].strip())
            elif record_type == "NS" and "nameserver" in line:
                records.append(line.split("=")[-1].strip())
            elif record_type == "TXT":
                txt_matches = re.findall(r'"([^"]*)"', line)
                if txt_matches:
                    records.append(" ".join(txt_matches))
                elif "text =" in line:
                    val = line.split("text =", 1)[-1].strip()
                    if val and val != '=':
                        records.append(val)
        return records
    except Exception:
        return []


def crtsh_query(domain):
    """Query crt.sh for certificate transparency subdomains."""
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    status, raw = http_get(url, timeout=30)
    try:
        data = json.loads(raw) if raw else []
    except (json.JSONDecodeError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    subs = set()
    for entry in data:
        name = entry.get("name_value", "")
        for sub in name.split("\n"):
            sub = sub.strip().lower()
            if sub.endswith(domain) and "*" not in sub:
                subs.add(sub)
    return sorted(subs)


def domain_recon(domain, out_dir=None):
    """Full domain reconnaissance."""
    out_dir = out_dir or make_output_dir(f"domain_{domain}")
    log(f"=== Domain Recon: {domain} ===")

    report = {
        "target": domain,
        "type": "domain",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identifiers_found": [],
    }

    # DNS records
    log("Querying DNS...")
    report["dns"] = {
        "A": dns_query(domain, "A"),
        "AAAA": dns_query(domain, "AAAA"),
        "MX": dns_query(domain, "MX"),
        "NS": dns_query(domain, "NS"),
        "TXT": dns_query(domain, "TXT"),
    }
    log(f"A records: {report['dns']['A']}", "OK")

    # Extract IPs
    for ip in report["dns"].get("A", []):
        report["identifiers_found"].append({"type": "ip", "value": ip, "source": f"dns_A_{domain}"})

    # crt.sh certificate transparency
    log("Checking certificate transparency (crt.sh)...")
    crtsh_subs = crtsh_query(domain)
    report["crtsh"] = {
        "subdomains_from_certs": crtsh_subs,
        "count": len(crtsh_subs),
    }
    log(f"crt.sh: {len(crtsh_subs)} subdomains", "OK")

    # HTTP headers
    log("Fetching HTTP headers...")
    status, _ = http_get(f"https://{domain}")
    try:
        req = urllib.request.Request(f"https://{domain}", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            report["http_headers"] = dict(resp.headers)
            report["http_status"] = resp.status
    except Exception as e:
        report["http_headers"] = {}
        report["http_status"] = str(e)

    # robots.txt
    log("Checking robots.txt...")
    _, robots = http_get(f"https://{domain}/robots.txt")
    if robots and "User-agent" in robots:
        report["robots_txt"] = robots[:2000]

    # security.txt
    log("Checking security.txt...")
    _, sec_txt = http_get(f"https://{domain}/.well-known/security.txt")
    if sec_txt and len(sec_txt) > 10:
        report["security_txt"] = sec_txt[:2000]

    save_json(out_dir, "domain_recon.json", report)
    log(f"=== Domain Recon complete ===", "OK")
    return report


# ============================================================
# IP RECON
# ============================================================

def ip_recon(ip, out_dir=None):
    """IP reconnaissance: geolocation, org, reputation."""
    out_dir = out_dir or make_output_dir(f"ip_{ip.replace('.', '_')}")
    log(f"=== IP Recon: {ip} ===")

    report = {
        "target": ip,
        "type": "ip",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Reverse DNS
    log("Reverse DNS lookup...")
    try:
        hostname = socket.gethostbyaddr(ip)
        report["reverse_dns"] = hostname[0]
    except Exception:
        report["reverse_dns"] = "none"

    # ipinfo.io
    log("Querying ipinfo.io...")
    ipinfo_url = f"https://ipinfo.io/{ip}/json"
    if IPINFO_TOKEN:
        ipinfo_url += f"?token={IPINFO_TOKEN}"
    ipinfo = http_get_json(ipinfo_url)
    if ipinfo:
        report["ipinfo"] = ipinfo
        log(f"ipinfo: {ipinfo.get('org', 'unknown')} ({ipinfo.get('city', 'unknown')})", "OK")

    # Shodan
    if SHODAN_API_KEY:
        log("Querying Shodan...")
        shodan = http_get_json(f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}")
        if "ip_str" in shodan:
            report["shodan"] = {
                "ports": shodan.get("ports", []),
                "os": shodan.get("os"),
                "org": shodan.get("org"),
                "vulns": shodan.get("vulns", []),
                "services": [
                    {"port": d.get("port"), "product": d.get("product"), "version": d.get("version")}
                    for d in shodan.get("data", [])
                ],
            }
            log(f"Shodan: {len(shodan.get('ports', []))} ports", "OK")
        else:
            report["shodan"] = {"status": "no_data"}

    # AbuseIPDB
    abuse_key = os.environ.get("ABUSEIPDB_KEY", "")
    if abuse_key:
        log("Checking AbuseIPDB...")
        abuse = http_get_json(
            f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}",
            headers={"Key": abuse_key, "Accept": "application/json"}
        )
        if "data" in abuse:
            report["abuseipdb"] = {
                "score": abuse["data"].get("abuseConfidenceScore", 0),
                "reports": abuse["data"].get("totalReports", 0),
                "country": abuse["data"].get("countryCode"),
                "isp": abuse["data"].get("isp"),
            }

    save_json(out_dir, "ip_recon.json", report)
    log(f"=== IP Recon complete ===", "OK")
    return report


# ============================================================
# SOCIAL MEDIA PROFILES (API-based)
# ============================================================

def social_media(username, out_dir=None):
    """Check social media profiles via public APIs."""
    out_dir = out_dir or make_output_dir(f"social_{username}")
    log(f"=== Social Media OSINT: {username} ===")

    report = {
        "target": username,
        "type": "social",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "profiles": {},
        "identifiers_found": [],
    }

    # GitHub API
    log("Checking GitHub...")
    gh = http_get_json(f"https://api.github.com/users/{username}")
    if "login" in gh:
        report["profiles"]["github"] = {
            "name": gh.get("name"),
            "bio": gh.get("bio"),
            "public_repos": gh.get("public_repos", 0),
            "followers": gh.get("followers", 0),
            "company": gh.get("company"),
            "location": gh.get("location"),
            "email": gh.get("email"),
            "blog": gh.get("blog"),
            "url": gh.get("html_url"),
        }
        if gh.get("email"):
            report["identifiers_found"].append({"type": "email", "value": gh["email"], "source": "github"})
        if gh.get("blog"):
            report["identifiers_found"].append({"type": "url", "value": gh["blog"], "source": "github"})
        log(f"GitHub: {gh.get('public_repos', 0)} repos, {gh.get('followers', 0)} followers", "OK")

    # Reddit API
    log("Checking Reddit...")
    reddit = http_get_json(
        f"https://www.reddit.com/user/{username}/about.json",
        headers={"User-Agent": "osint-skill/2.0"}
    )
    if "data" in reddit:
        d = reddit["data"]
        report["profiles"]["reddit"] = {
            "total_karma": d.get("total_karma", 0),
            "comment_karma": d.get("comment_karma", 0),
            "link_karma": d.get("link_karma", 0),
            "account_created": datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc).isoformat(),
            "is_mod": d.get("is_mod", False),
        }
        log(f"Reddit: {d.get('total_karma', 0)} karma", "OK")

    # Keybase
    log("Checking Keybase...")
    kb = http_get_json(f"https://keybase.io/_/api/1.0/user/lookup.json?username={username}")
    if kb.get("them"):
        report["profiles"]["keybase"] = {"basics": kb["them"][0].get("basics", {})}
        log("Keybase: found", "OK")

    save_json(out_dir, "social_media.json", report)
    log(f"=== Social Media OSINT complete ===", "OK")
    return report


# ============================================================
# RECURSIVE DISCOVERY ENGINE — The "Viral" Component
# ============================================================

def extract_identifiers(data, source=""):
    """
    Parse any OSINT result and extract identifiers (emails, usernames,
    phone numbers, URLs, domains, names, locations).
    """
    identifiers = []

    def _walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _walk(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _walk(item, f"{path}[{i}]")
        elif isinstance(obj, str):
            # Emails
            for email in re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', obj):
                if email not in ("noreply@github.com", "user@example.com", "test@test.com"):
                    identifiers.append({"type": "email", "value": email, "source": source, "path": path})
            # Phone numbers (international format)
            for phone in re.findall(r'\+?\d{1,4}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}', obj):
                cleaned = re.sub(r'[^\d+]', '', phone)
                if len(cleaned) >= 7:
                    identifiers.append({"type": "phone", "value": cleaned, "source": source, "path": path})
            # Twitter handles
            for handle in re.findall(r'(?:^|\s)@([a-zA-Z0-9_]{1,15})(?:\s|$|[.,;:!?])', obj):
                if handle.lower() not in ("username", "user", "handle", "name", "email"):
                    identifiers.append({"type": "username", "value": handle, "source": source,
                                        "platform": "twitter", "path": path})
            # URLs (extract domain + potential usernames from paths)
            for url in re.findall(r'https?://(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(?:/\S*)?', obj):
                identifiers.append({"type": "domain", "value": url, "source": source, "path": path})

    _walk(data)
    # Deduplicate
    seen = set()
    unique = []
    for ident in identifiers:
        key = (ident["type"], ident["value"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(ident)
    return unique


def recursive_discovery(target, target_type, out_dir, max_depth=3):
    """
    THE VIRAL ENGINE.

    Start with one identifier. Discover more. Investigate those. Repeat.

    depth 0: investigate the original target
    depth 1: investigate identifiers found in depth 0
    depth 2: investigate identifiers found in depth 1
    ...

    Stops when max_depth reached or no new identifiers found.
    """
    graph = InvestigationGraph(target, target_type)

    for depth in range(max_depth + 1):
        batch = graph.get_uninvestigated()
        if not batch:
            log(f"Depth {depth}: No new identifiers to investigate. Stopping.", "INFO")
            break

        log(f"\n{'='*50}", "INFO")
        log(f"RECURSIVE DISCOVERY — Depth {depth} — {len(batch)} identifiers", "INFO")
        log(f"{'='*50}", "INFO")

        for identifier, id_type in batch:
            graph.mark_investigated(identifier)
            log(f"\n>>> Investigating: {identifier} (type: {id_type})", "INFO")

            new_data = None
            new_identifiers = []

            if id_type == "username":
                # Username enumeration + social media
                user_report = username_enum(identifier, out_dir)
                social_report = social_media(identifier, out_dir)
                new_data = {"username_enum": user_report, "social_media": social_report}

                # Extract identifiers from social media profiles
                for plat, profile in social_report.get("profiles", {}).items():
                    graph.add_node(identifier, "username", source=f"{plat}_profile",
                                   data=profile, confidence=0.9, verified=True)
                    # Profile may contain email, blog, etc.
                    for key in ("email", "blog", "url"):
                        if profile.get(key):
                            new_identifiers.append({"type": key if key != "blog" else "url",
                                                    "value": profile[key],
                                                    "source": f"{plat}_{key}"})

                # Also try GitHub deep dive for any username
                gh_report = github_deep_dive(identifier, out_dir)
                new_data["github"] = gh_report
                for ident in gh_report.get("identifiers_found", []):
                    new_identifiers.append(ident)

            elif id_type == "email":
                email_report = email_osint(identifier, out_dir)
                new_data = email_report
                for ident in email_report.get("identifiers_found", []):
                    new_identifiers.append(ident)

                # Also run username search on email local part
                local_part = identifier.split("@")[0]
                graph.add_node(local_part, "username",
                               source=f"email_local_part_{identifier}", confidence=0.6)

            elif id_type == "domain":
                domain_report = domain_recon(identifier, out_dir)
                new_data = domain_report
                for ident in domain_report.get("identifiers_found", []):
                    new_identifiers.append(ident)

            elif id_type == "ip":
                ip_report = ip_recon(identifier, out_dir)
                new_data = ip_report

            # Process newly discovered identifiers
            for ident in new_identifiers:
                value = ident["value"]
                itype = ident["type"]
                source = ident["source"]

                # Skip generic/meaningless values
                if len(value) < 3:
                    continue
                if value.lower() in ("none", "null", "n/a", "unknown", "test", "example"):
                    continue

                graph.add_node(value, itype, source=source, confidence=0.7)
                graph.add_edge(target, value, f"discovered_via_{source}",
                               evidence=f"Found in {source}")

                log(f"  [NEW] {itype}: {value} (from {source})", "LINK")

    return graph


# ============================================================
# GOOGLE DORKS
# ============================================================

def generate_dorks(domain, out_dir=None):
    """Generate Google dork queries for a domain."""
    out_dir = out_dir or make_output_dir(f"dork_{domain}")
    log(f"=== Google Dork Generator: {domain} ===")

    dorks = {
        "exposed_files": {
            "pdf": f'site:{domain} filetype:pdf',
            "excel": f'site:{domain} filetype:xlsx OR filetype:csv',
            "word": f'site:{domain} filetype:docx OR filetype:doc',
            "sql_dumps": f'site:{domain} filetype:sql',
        },
        "sensitive_dirs": {
            "open_directories": f'site:{domain} intitle:"index of"',
            "git_repos": f'site:{domain} intitle:"index of" .git',
            "env_files": f'site:{domain} filetype:env',
            "config_files": f'site:{domain} filetype:xml OR filetype:conf',
            "log_files": f'site:{domain} filetype:log',
            "backup_files": f'site:{domain} filetype:bak OR filetype:sql OR filetype:dump',
        },
        "login_pages": {
            "admin": f'site:{domain} inurl:admin OR inurl:login',
            "cpanel": f'site:{domain} intitle:"cPanel Login"',
            "phpmyadmin": f'site:{domain} inurl:phpmyadmin',
            "wp_admin": f'site:{domain} inurl:wp-admin',
        },
        "info_leaks": {
            "emails": f'site:{domain} "@{domain}"',
            "error_pages": f'site:{domain} intitle:"error" OR intitle:"500"',
            "stack_traces": f'site:{domain} "stack trace" OR "exception"',
        },
        "github_leaks": {
            "secrets": f'site:github.com "{domain}" "api_key" OR "password" OR "secret"',
            "env_files": f'site:github.com "{domain}" filetype:env',
            "credentials": f'site:github.com "{domain}" "credentials" OR "token"',
        },
        "social_media": {
            "linkedin": f'site:linkedin.com/in "{domain}"',
            "github_org": f'site:github.com "{domain}"',
            "twitter": f'site:twitter.com "{domain}"',
        },
        "paste_sites": {
            "pastebin": f'site:pastebin.com "{domain}"',
            "github_gist": f'site:gist.github.com "{domain}"',
        },
    }

    total = sum(len(cat) for cat in dorks.values())
    log(f"Generated {total} dork queries across {len(dorks)} categories", "OK")

    report = {
        "target": domain,
        "type": "dorks",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_dorks": total,
        "categories": dorks,
    }

    save_json(out_dir, "google_dorks.json", report)
    return report


# ============================================================
# ORCHESTRATOR — Full recursive recon
# ============================================================

def orchestrator(target, target_type, out_dir=None):
    """
    Full OSINT orchestrator — chains all tools with RECURSIVE DISCOVERY.

    This is the main entry point. It:
    1. Creates a single output directory
    2. Runs the recursive discovery engine (which chains investigations)
    3. Merges all findings into a master report
    """
    if out_dir is None:
        clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', target)[:50]
        ts = datetime.now().strftime("%d_%b_%Y")
        out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
        os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)

    log(f"╔══════════════════════════════════════════════╗")
    log(f"║     OSINT ORCHESTRATOR v2 — Recursive        ║")
    log(f"╚══════════════════════════════════════════════╝")
    log(f"Target: {target}")
    log(f"Type:   {target_type}")
    log(f"Output: {out_dir}")

    start = time.time()

    # Run recursive discovery
    graph = recursive_discovery(target, target_type, out_dir, max_depth=2)

    # Also run type-specific extras
    if target_type == "domain":
        generate_dorks(target, out_dir)
    elif target_type == "email":
        domain = target.split("@")[1]
        domain_recon(domain, out_dir)

    # Merge all JSON files from data/ into master
    report = {
        "target": target,
        "type": target_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "output_directory": out_dir,
        "graph_summary": {
            "total_identifiers": len(graph.nodes),
            "total_relationships": len(graph.edges),
            "identifiers_by_type": {},
        },
        "phases": {},
    }

    # Count identifiers by type
    type_counts = defaultdict(int)
    for node in graph.nodes.values():
        type_counts[node["type"]] += 1
    report["graph_summary"]["identifiers_by_type"] = dict(type_counts)

    # Merge all tool outputs
    data_dir = os.path.join(out_dir, "data")
    for fname in os.listdir(data_dir):
        if fname == "master_report.json":
            continue
        if fname.endswith(".json"):
            try:
                with open(os.path.join(data_dir, fname), encoding="utf-8") as f:
                    tool_data = json.load(f)
                tool_name = fname.replace(".json", "")
                report["phases"][tool_name] = tool_data
            except Exception:
                pass

    # Save investigation graph
    save_json(out_dir, "investigation_graph.json", graph.to_dict())
    report["investigation_graph"] = graph.to_dict()

    save_json(out_dir, "master_report.json", report)

    duration = time.time() - start
    log(f"\n╔══════════════════════════════════════════════╗")
    log(f"║     OSINT COMPLETE                           ║")
    log(f"╚══════════════════════════════════════════════╝")
    log(f"Duration:      {duration:.1f}s")
    log(f"Identifiers:   {len(graph.nodes)} discovered")
    log(f"Relationships: {len(graph.edges)} mapped")
    log(f"Files:         {len(os.listdir(data_dir))} JSON reports in {data_dir}")
    log(f"Master:        {out_dir}/data/master_report.json", "OK")

    return report


# ============================================================
# CLI
# ============================================================

COMMANDS = {
    "username": ("username_enum", "<username>"),
    "email": ("email_osint", "<email>"),
    "domain": ("domain_recon", "<domain>"),
    "ip": ("ip_recon", "<ip>"),
    "social": ("social_media", "<username>"),
    "github": ("github_deep_dive", "<username>"),
    "dork": ("generate_dorks", "<domain>"),
    "discover": ("recursive_discovery", "<target> <type>"),
    "orchestrator": ("orchestrator", "<target> <type>"),
}


def main():
    if len(sys.argv) < 3:
        print("Usage: python osint_core.py <command> <target> [type]")
        print("\nCommands:")
        for cmd, (func, args) in COMMANDS.items():
            print(f"  {cmd:15s} {args}")
        print("\nTarget types for orchestrator/discover: email, phone, username, domain, ip, person")
        print("\nAPI keys (set as env vars):")
        print("  GITHUB_TOKEN, HIBP_API_KEY, SHODAN_API_KEY, IPINFO_TOKEN, VT_API_KEY, ABUSEIPDB_KEY")
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    if command in ("orchestrator", "discover"):
        if len(sys.argv) < 4:
            print(f"Usage: python osint_core.py {command} <target> <type>")
            sys.exit(1)
        target_type = sys.argv[3]
        if command == "orchestrator":
            orchestrator(target, target_type)
        else:
            out_dir = make_output_dir(f"discover_{target}")
            graph = recursive_discovery(target, target_type, out_dir)
            save_json(out_dir, "investigation_graph.json", graph.to_dict())
            print(f"\nInvestigation graph saved to {out_dir}/data/investigation_graph.json")
            print(f"Total identifiers: {len(graph.nodes)}")
            print(f"Total relationships: {len(graph.edges)}")
    elif command in COMMANDS:
        func_name = COMMANDS[command][0]
        globals()[func_name](target)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
