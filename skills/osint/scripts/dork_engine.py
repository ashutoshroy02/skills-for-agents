#!/usr/bin/env python3
"""
Multi-Engine Dorking v2 — REAL SERP scraping, no API keys needed.

How SQLi Dumper / Pagodo / GHDB tools work:
1. Send HTTP GET to search engine's web interface: /search?q=DORK_QUERY
2. Parse the HTML response for result links
3. Rotate User-Agents to avoid bot detection
4. Add delays between requests to avoid rate limits
5. Hit multiple engines in parallel for redundancy

This script does exactly that. Zero API keys required.

Usage:
    python dork_engine.py domain example.com              # Generate dork queries
    python dork_engine.py domain example.com --execute    # Scrape search engines
    python dork_engine.py creds example.com --execute     # Credential leak dorks
    python dork_engine.py social "John Doe" --execute     # Social media dorks
    python dork_engine.py person "John Doe" --execute     # Person-focused dorks
    python dork_engine.py custom "your dork" --execute    # Custom query
    python dork_engine.py ghdb --execute                  # Pull from Exploit-DB GHDB
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
import sys
import os
import time
import random
import ssl
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape

SSL_CTX = ssl.create_default_context()
OSINT_OUTPUT_DIR = os.environ.get("OSINT_OUTPUT_DIR", os.path.expanduser("~/osint"))

# ============================================================
# USER AGENT ROTATION — pretend to be real browsers
# ============================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
]

def random_ua():
    return random.choice(USER_AGENTS)


def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m",
              "FOUND": "\033[92m", "HIT": "\033[95m", "DORK": "\033[96m"}
    reset = "\033[0m"
    print(f"{colors.get(level, '')}[{level}]{reset} {msg}", flush=True)


def http_get(url, headers=None, timeout=15):
    hdrs = {"User-Agent": random_ua(), "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "identity"}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def http_post(url, data=None, headers=None, timeout=15):
    hdrs = {"User-Agent": random_ua(), "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html", "Accept-Language": "en-US,en;q=0.9"}
    if headers:
        hdrs.update(headers)
    try:
        body = urllib.parse.urlencode(data).encode() if data else b""
        req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


# ============================================================
# SERP SCRAPERS — Parse search engine HTML for result links
# ============================================================

def clean_url(url):
    """Extract real URL from search engine redirect wrappers."""
    # Google: /url?q=REAL_URL&sa=...
    if "/url?" in url:
        match = re.search(r'[?&]q=([^&]+)', url)
        if match:
            url = urllib.parse.unquote(match.group(1))
    # DuckDuckGo: //duckduckgo.com/l/?uddg=REAL_URL
    if "uddg=" in url:
        match = re.search(r'uddg=([^&]+)', url)
        if match:
            url = urllib.parse.unquote(match.group(1))
    # Remove tracking params
    url = re.sub(r'[&?](utm_\w+|sa|ved|usg)=[^&]*', '', url)
    return url.strip()


def parse_google(html):
    """Parse Google SERP HTML for result links."""
    results = []
    # Google wraps result links in /url?q=ACTUAL_URL
    for match in re.finditer(r'<a[^>]+href="(/url\?q=[^"]+)"[^>]*>', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "google.com" not in url:
            results.append(url)
    # Also try direct <a> in <div class="g">
    for match in re.finditer(r'class="g"[^>]*>.*?<a[^>]+href="(https?://[^"]+)"', html, re.DOTALL):
        url = clean_url(match.group(1))
        if url.startswith("http") and "google.com" not in url and url not in results:
            results.append(url)
    return results


def parse_bing(html):
    """Parse Bing SERP HTML for result links."""
    results = []
    # Bing: <li class="b_algo"><h2><a href="URL">
    for match in re.finditer(r'class="b_algo"[^>]*>.*?<a[^>]+href="(https?://[^"]+)"', html, re.DOTALL):
        url = clean_url(match.group(1))
        if url.startswith("http") and "bing.com" not in url and "microsoft.com" not in url:
            results.append(url)
    # Alternative pattern
    for match in re.finditer(r'<h2><a[^>]+href="(https?://[^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "bing.com" not in url and url not in results:
            results.append(url)
    return results


def parse_duckduckgo(html):
    """Parse DuckDuckGo HTML SERP for result links."""
    results = []
    # DDG: <a class="result__a" href="URL">
    for match in re.finditer(r'class="result__a"[^>]*href="([^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "duckduckgo.com" not in url:
            results.append(url)
    # Alternative: <a rel="nofollow" class="result__url" href="URL">
    for match in re.finditer(r'class="result__url"[^>]*href="([^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "duckduckgo.com" not in url and url not in results:
            results.append(url)
    return results


def parse_yandex(html):
    """Parse Yandex SERP HTML for result links."""
    results = []
    # Yandex organic titles
    for match in re.finditer(r'href="(https?://[^"]+)"[^>]*class="[^"]*OrganicTitle', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "yandex" not in url:
            results.append(url)
    # Alternative pattern
    for match in re.finditer(r'class="[^"]*Link[^"]*organic__url[^"]*"[^>]*href="([^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "yandex" not in url and url not in results:
            results.append(url)
    return results


def parse_brave(html):
    """Parse Brave Search SERP HTML for result links."""
    results = []
    for match in re.finditer(r'<a[^>]*class="[^"]*result-header[^"]*"[^>]*href="(https?://[^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "brave.com" not in url:
            results.append(url)
    # Alternative
    for match in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*heading', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "brave.com" not in url and url not in results:
            results.append(url)
    return results


def parse_aol(html):
    """Parse AOL Search SERP HTML for result links."""
    results = []
    for match in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*algo', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "aol.com" not in url:
            results.append(url)
    # AOL uses Bing-like structure
    for match in re.finditer(r'class="[^"]*algo[^"]*".*?<a[^>]+href="(https?://[^"]+)"', html, re.DOTALL):
        url = clean_url(match.group(1))
        if url.startswith("http") and "aol.com" not in url and url not in results:
            results.append(url)
    return results


def parse_mojeek(html):
    """Parse Mojeek SERP HTML for result links."""
    results = []
    for match in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="[^"]*ob', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "mojeek.com" not in url:
            results.append(url)
    return results


def parse_startpage(html):
    """Parse Startpage SERP HTML for result links."""
    results = []
    for match in re.finditer(r'class="w-gl__result-url"[^>]*href="(https?://[^"]+)"', html):
        url = clean_url(match.group(1))
        if url.startswith("http") and "startpage.com" not in url:
            results.append(url)
    for match in re.finditer(r'class="[^"]*result[^"]*"[^>]*>.*?<a[^>]+href="(https?://[^"]+)"', html, re.DOTALL):
        url = clean_url(match.group(1))
        if url.startswith("http") and "startpage.com" not in url and url not in results:
            results.append(url)
    return results


# ============================================================
# SEARCH ENGINE DEFINITIONS
# ============================================================

SEARCH_ENGINES = {
    "google": {
        "name": "Google",
        "build_url": lambda q, page=0: f"https://www.google.com/search?q={urllib.parse.quote(q)}&start={page*10}&num=10",
        "parser": parse_google,
        "delay": (3, 6),  # Min/max seconds between requests
        "max_pages": 3,
        "captcha_indicators": ["captcha", "unusual traffic", "automated queries", "sorry/index"],
    },
    "bing": {
        "name": "Bing",
        "build_url": lambda q, page=0: f"https://www.bing.com/search?q={urllib.parse.quote(q)}&first={page*10+1}",
        "parser": parse_bing,
        "delay": (2, 4),
        "max_pages": 3,
        "captcha_indicators": ["captcha", "unusual traffic"],
    },
    "duckduckgo": {
        "name": "DuckDuckGo",
        "build_url": lambda q, page=0: f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}&s={page*30}",
        "parser": parse_duckduckgo,
        "delay": (2, 5),
        "max_pages": 3,
        "captcha_indicators": ["captcha", "blocked"],
    },
    "yandex": {
        "name": "Yandex",
        "build_url": lambda q, page=0: f"https://yandex.com/search/?text={urllib.parse.quote(q)}&p={page}&lr=84",
        "parser": parse_yandex,
        "delay": (3, 6),
        "max_pages": 2,
        "captcha_indicators": ["captcha", "smartcaptcha"],
    },
    "brave": {
        "name": "Brave",
        "build_url": lambda q, page=0: f"https://search.brave.com/search?q={urllib.parse.quote(q)}&offset={page*10}",
        "parser": parse_brave,
        "delay": (2, 4),
        "max_pages": 2,
        "captcha_indicators": ["captcha"],
    },
    "aol": {
        "name": "AOL",
        "build_url": lambda q, page=0: f"https://search.aol.com/aol/search?q={urllib.parse.quote(q)}&b={page*10+1}",
        "parser": parse_aol,
        "delay": (2, 4),
        "max_pages": 2,
        "captcha_indicators": [],
    },
    "startpage": {
        "name": "Startpage",
        "build_url": lambda q, page=0: f"https://www.startpage.com/sp/search",
        "parser": parse_startpage,
        "delay": (3, 6),
        "max_pages": 2,
        "captcha_indicators": ["captcha"],
        "method": "POST",
        "post_data": lambda q, page=0: {"query": q, "page": page + 1},
    },
    "mojeek": {
        "name": "Mojeek",
        "build_url": lambda q, page=0: f"https://www.mojeek.com/search?q={urllib.parse.quote(q)}&s={page*10+1}",
        "parser": parse_mojeek,
        "delay": (2, 5),
        "max_pages": 2,
        "captcha_indicators": [],
    },
}


def scrape_engine(engine_name, query, max_pages=None):
    """
    Scrape a search engine for results. Returns list of URLs.

    This is exactly how SQLi Dumper / Pagodo work:
    1. Build search URL
    2. Send HTTP request with browser User-Agent
    3. Parse HTML for result links
    4. Handle pagination
    5. Add delays between requests
    """
    engine = SEARCH_ENGINES.get(engine_name)
    if not engine:
        return {"engine": engine_name, "status": "unknown_engine", "results": []}

    pages = max_pages or engine.get("max_pages", 2)
    all_results = []
    captcha_hit = False

    for page in range(pages):
        url = engine["build_url"](query, page)

        # Add random delay between requests
        if page > 0:
            delay = random.uniform(*engine["delay"])
            time.sleep(delay)

        # Make request
        if engine.get("method") == "POST":
            post_data = engine.get("post_data", lambda q, p: {})(query, page)
            status, html = http_post(url, data=post_data)
        else:
            status, html = http_get(url)

        if status == 0:
            continue

        # Check for CAPTCHA
        html_lower = html.lower() if html else ""
        for indicator in engine.get("captcha_indicators", []):
            if indicator in html_lower:
                captcha_hit = True
                break

        if captcha_hit:
            break

        if not html or status != 200:
            continue

        # Parse results
        results = engine["parser"](html)
        all_results.extend(results)

        # If no results on this page, stop pagination
        if not results:
            break

    # Deduplicate
    seen = set()
    unique = []
    for url in all_results:
        if url not in seen:
            seen.add(url)
            unique.append(url)

    return {
        "engine": engine["name"],
        "status": "captcha_blocked" if captcha_hit else "ok",
        "pages_scraped": page + 1 if 'page' in dir() else 0,
        "results_count": len(unique),
        "results": unique,
    }


def multi_engine_scrape(query, engines=None, max_pages_per_engine=2):
    """Scrape multiple search engines in sequence (not parallel — to avoid bans)."""
    if engines is None:
        engines = ["google", "bing", "duckduckgo", "yandex", "brave"]

    all_results = {}
    combined_urls = []

    for eng in engines:
        if eng not in SEARCH_ENGINES:
            log(f"  {eng}: unknown engine, skipping", "WARN")
            continue

        log(f"  Scraping {SEARCH_ENGINES[eng]['name']}...")
        result = scrape_engine(eng, query, max_pages_per_engine)
        all_results[eng] = result

        count = result["results_count"]
        status = result["status"]
        if count > 0:
            log(f"  {eng}: {count} results", "OK")
            combined_urls.extend(result["results"])
        elif status == "captcha_blocked":
            log(f"  {eng}: CAPTCHA blocked", "WARN")
        else:
            log(f"  {eng}: 0 results", "WARN")

        # Delay between engines
        time.sleep(random.uniform(2, 4))

    # Deduplicate across engines
    seen = set()
    unique = []
    for url in combined_urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)

    return {
        "query": query,
        "engines_scraped": len(all_results),
        "total_results": len(unique),
        "unique_urls": unique,
        "per_engine": all_results,
    }


# ============================================================
# DORK GENERATORS
# ============================================================

def generate_domain_dorks(domain):
    """Generate comprehensive domain-focused dork queries."""
    return {
        # === SENSITIVE FILES ===
        "exposed_env": f'site:{domain} ext:env "DB_" OR "PASS" OR "SECRET" OR "KEY"',
        "exposed_config": f'site:{domain} ext:xml OR ext:conf OR ext:yml "password" OR "api_key"',
        "exposed_sql": f'site:{domain} ext:sql "INSERT INTO" OR "CREATE TABLE"',
        "exposed_backup": f'site:{domain} ext:bak OR ext:backup OR ext:old OR ext:orig',
        "exposed_log": f'site:{domain} ext:log "error" OR "exception" OR "password"',
        "exposed_phpinfo": f'site:{domain} "phpinfo()" OR "PHP Version"',
        "exposed_phpini": f'site:{domain} ext:ini "mysql" OR "smtp" OR "password"',
        "exposed_git": f'site:{domain} ".git" "index" OR "HEAD" OR "config"',
        "exposed_svn": f'site:{domain} ".svn" "entries"',
        "exposed_dockerfile": f'site:{domain} ext:yml "docker" OR "compose"',
        "exposed_robots": f'site:{domain} inurl:robots.txt',
        "exposed_sitemap": f'site:{domain} inurl:sitemap.xml',

        # === CREDENTIAL LEAKS ===
        "github_secrets": f'site:github.com "{domain}" "api_key" OR "apikey" OR "secret" OR "password" OR "token"',
        "github_env": f'site:github.com "{domain}" ext:env',
        "github_config": f'site:github.com "{domain}" ext:yml OR ext:yaml OR ext:json "password" OR "key"',
        "github_issues": f'site:github.com "{domain}" inurl:issues "password" OR "credential" OR "leak"',
        "gitlab_secrets": f'site:gitlab.com "{domain}" "password" OR "secret" OR "key"',
        "paste_leaks": f'site:pastebin.com OR site:paste.ee OR site:dpaste.org "{domain}"',
        "gist_leaks": f'site:gist.github.com "{domain}" "password" OR "key" OR "token"',

        # === DIRECTORIES & LOGIN ===
        "open_dir": f'site:{domain} intitle:"index of" "parent directory"',
        "open_dir_git": f'site:{domain} intitle:"index of" ".git"',
        "admin_login": f'site:{domain} inurl:admin OR inurl:login OR inurl:portal',
        "cpanel": f'site:{domain} intitle:"cPanel" OR inurl:cpanel',
        "phpmyadmin": f'site:{domain} inurl:phpmyadmin OR inurl:pma',
        "wp_admin": f'site:{domain} inurl:wp-admin OR inurl:wp-login',
        "jenkins": f'site:{domain} intitle:"Dashboard [Jenkins]"',
        "grafana": f'site:{domain} inurl:grafana OR intitle:"Grafana"',
        "swagger": f'site:{domain} inurl:swagger OR inurl:api-docs',
        "graphql": f'site:{domain} inurl:graphql OR inurl:graphiql',

        # === INFORMATION LEAKS ===
        "emails": f'site:{domain} "@{domain}" -www -mail',
        "error_pages": f'site:{domain} intitle:"error" OR intitle:"500" "stack" OR "trace"',
        "sql_errors": f'site:{domain} "mysql_fetch" OR "ORA-" OR "SQL Server"',
        "internal_ips": f'site:{domain} "192.168." OR "10.0." OR "172.16."',

        # === DOCUMENTS ===
        "pdf_docs": f'site:{domain} ext:pdf',
        "excel_docs": f'site:{domain} ext:xlsx OR ext:csv OR ext:xls',
        "word_docs": f'site:{domain} ext:docx OR ext:doc',
        "confidential_docs": f'site:{domain} ext:pdf "confidential" OR "internal"',

        # === SOCIAL ===
        "linkedin_employees": f'site:linkedin.com/in "{domain}"',
        "twitter_mentions": f'site:twitter.com "{domain}"',
        "reddit_mentions": f'site:reddit.com "{domain}"',

        # === CLOUD ===
        "s3_buckets": f'site:s3.amazonaws.com "{domain}"',
        "azure_blobs": f'site:blob.core.windows.net "{domain}"',
        "gcs_buckets": f'site:storage.googleapis.com "{domain}"',
        "firebase": f'site:firebaseio.com "{domain}"',
    }


def generate_creds_dorks(domain):
    """Generate credential leak dorks — the juicy stuff."""
    return {
        "github_api_keys": f'site:github.com "{domain}" "api_key" OR "apikey" OR "api-key"',
        "github_passwords": f'site:github.com "{domain}" "password" OR "passwd" OR "pwd"',
        "github_tokens": f'site:github.com "{domain}" "token" OR "secret" OR "bearer"',
        "github_aws": f'site:github.com "{domain}" "AKIA" OR "aws_access" OR "aws_secret"',
        "github_ssh": f'site:github.com "{domain}" "BEGIN RSA PRIVATE KEY" OR "BEGIN OPENSSH PRIVATE KEY"',
        "github_oauth": f'site:github.com "{domain}" "client_secret" OR "client_id"',
        "github_env": f'site:github.com "{domain}" ext:env',
        "github_config": f'site:github.com "{domain}" ext:json OR ext:yml "password" OR "key"',
        "github_kubernetes": f'site:github.com "{domain}" ext:yml "kind: Secret"',
        "gitlab_secrets": f'site:gitlab.com "{domain}" "password" OR "secret" OR "key"',
        "pastebin": f'site:pastebin.com "{domain}" "password" OR "login" OR "credential"',
        "gist_leaks": f'site:gist.github.com "{domain}" "password" OR "key" OR "token"',
        "s3_public": f'site:s3.amazonaws.com "{domain}"',
        "firebase": f'site:firebaseio.com "{domain}"',
        "google_drive": f'site:drive.google.com "{domain}"',
        "google_docs": f'site:docs.google.com "{domain}"',
        "notion": f'site:notion.so "{domain}"',
        "confluence": f'site:atlassian.net "{domain}"',
        "trello": f'site:trello.com "{domain}"',
        "forum_creds": f'"{domain}" "username" "password" "forum" OR "database" OR "dump"',
        "sql_dumps": f'"{domain}" ext:sql "INSERT INTO" "password" OR "user"',
        "combo_lists": f'"{domain}" ext:txt "email:password" OR "user:pass"',
    }


def generate_person_dorks(name):
    """Generate person-focused dork queries."""
    n = f'"{name}"'
    return {
        "linkedin": f'site:linkedin.com/in {n}',
        "twitter": f'site:twitter.com {n}',
        "facebook": f'site:facebook.com {n}',
        "instagram": f'site:instagram.com {n}',
        "tiktok": f'site:tiktok.com {n}',
        "youtube": f'site:youtube.com {n}',
        "reddit": f'site:reddit.com {n}',
        "github": f'site:github.com {n}',
        "stackoverflow": f'site:stackoverflow.com {n}',
        "medium": f'site:medium.com {n}',
        "keybase": f'site:keybase.io {n}',
        "aboutme": f'site:about.me {n}',
        "gravatar": f'site:en.gravatar.com {n}',
        "pinterest": f'site:pinterest.com {n}',
        "quora": f'site:quora.com {n}',
        "hackernews": f'site:news.ycombinator.com {n}',
        "behance": f'site:behance.net {n}',
        "dribbble": f'site:dribbble.com {n}',
        "flickr": f'site:flickr.com {n}',
        "twitch": f'site:twitch.tv {n}',
        "steam": f'site:steamcommunity.com {n}',
        "resume_cv": f'{n} ext:pdf "resume" OR "cv"',
        "phone": f'{n} "phone" OR "mobile" OR "cell"',
        "address": f'{n} "address" OR "street" OR "city"',
        "email": f'{n} "email" OR "@" OR "contact"',
        "court_records": f'{n} "court" OR "case" OR "docket"',
        "property": f'{n} "property" OR "deed" OR "mortgage"',
        "news": f'{n} "news" OR "article" OR "press"',
        "images": f'{n} site:flickr.com OR site:imgur.com OR site:500px.com',
        "leaked": f'site:pastebin.com OR site:paste.ee {n}',
    }


def generate_social_dorks(name):
    """Generate social media discovery dorks."""
    n = f'"{name}"'
    return {
        "facebook_profile": f'site:facebook.com {n} "profile" OR "about"',
        "twitter_profile": f'site:twitter.com {n} "followers" OR "following"',
        "instagram_profile": f'site:instagram.com {n} "followers" OR "posts"',
        "tiktok_profile": f'site:tiktok.com/@{name}',
        "linkedin_personal": f'site:linkedin.com/in {n}',
        "youtube_channel": f'site:youtube.com {n} "channel" OR "videos"',
        "reddit_user": f'site:reddit.com/user {n}',
        "pinterest_profile": f'site:pinterest.com {n}',
        "tumblr_profile": f'site:tumblr.com {n}',
        "medium_profile": f'site:medium.com {n}',
        "quora_profile": f'site:quora.com {n}',
        "github_profile": f'site:github.com {n}',
        "twitch_profile": f'site:twitch.tv {n}',
        "soundcloud_profile": f'site:soundcloud.com {n}',
        "steam_profile": f'site:steamcommunity.com {n}',
        "vk_profile": f'site:vk.com {n}',
        "dating_profiles": f'{n} "dating" OR "profile" OR "single"',
        "forum_profiles": f'{n} "member" OR "joined" "forum"',
        "blog": f'{n} "blog" OR "wrote" OR "article" -site:twitter.com',
    }


def generate_email_dorks(email):
    """Generate email-focused dork queries."""
    e = f'"{email}"'
    username = email.split("@")[0]
    return {
        "exact_email": e,
        "paste_sites": f'site:pastebin.com OR site:paste.ee {e}',
        "github": f'site:github.com {e}',
        "gist": f'site:gist.github.com {e}',
        "linkedin": f'site:linkedin.com {e}',
        "forums": f'{e} "forum" OR "thread" OR "post"',
        "documents": f'{e} ext:pdf OR ext:docx OR ext:xlsx',
        "leaked": f'{e} "leak" OR "breach" OR "dump"',
        "username_variant": f'"{username}" site:github.com OR site:reddit.com OR site:twitter.com',
    }


def generate_username_dorks(username):
    """Generate username-focused dork queries."""
    u = f'"{username}"'
    return {
        "github": f'site:github.com {u}',
        "reddit": f'site:reddit.com {u}',
        "twitter": f'site:twitter.com {u}',
        "instagram": f'site:instagram.com {u}',
        "tiktok": f'site:tiktok.com {u}',
        "facebook": f'site:facebook.com {u}',
        "youtube": f'site:youtube.com {u}',
        "twitch": f'site:twitch.tv {u}',
        "steam": f'site:steamcommunity.com {u}',
        "keybase": f'site:keybase.io {u}',
        "stackoverflow": f'site:stackoverflow.com {u}',
        "medium": f'site:medium.com {u}',
        "npm": f'site:npmjs.com {u}',
        "pypi": f'site:pypi.org {u}',
        "dockerhub": f'site:hub.docker.com {u}',
        "hackernews": f'site:news.ycombinator.com {u}',
        "behance": f'site:behance.net {u}',
        "dribbble": f'site:dribbble.com {u}',
        "soundcloud": f'site:soundcloud.com {u}',
        "bandcamp": f'site:bandcamp.com {u}',
        "pinterest": f'site:pinterest.com {u}',
        "letterboxd": f'site:letterboxd.com {u}',
        "strava": f'site:strava.com {u}',
        "chesscom": f'site:chess.com {u}',
        "roblox": f'site:roblox.com {u}',
        "minecraft": f'site:namemc.com {u}',
        "paste_sites": f'site:pastebin.com OR site:paste.ee {u}',
        "email_guess": f'"{username}@gmail.com" OR "{username}@protonmail.com" OR "{username}@yahoo.com"',
        "leaked": f'{u} "leak" OR "breach" OR "dump"',
    }


# ============================================================
# GHDB — Google Hacking Database (Exploit-DB)
# ============================================================

def fetch_ghdb(category=None, max_dorks=50):
    """Fetch dorks from the Google Hacking Database (Exploit-DB)."""
    log("Fetching GHDB from Exploit-DB...")
    url = "https://www.exploit-db.com/google-hacking-database"
    status, html = http_get(url)
    if status != 200:
        log(f"Failed to fetch GHDB: HTTP {status}", "WARN")
        return []

    # Parse GHDB entries
    dorks = []
    # GHDB table rows contain dork text
    for match in re.finditer(r'class="dork"[^>]*>(.*?)</td>', html, re.DOTALL):
        dork_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        if dork_text:
            dorks.append(dork_text)

    if not dorks:
        # Alternative parsing
        for match in re.finditer(r'<td[^>]*>(.*?)</td>', html, re.DOTALL):
            text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            if any(op in text for op in ['site:', 'inurl:', 'intitle:', 'intext:', 'filetype:']):
                dorks.append(text)

    dorks = dorks[:max_dorks]
    log(f"Fetched {len(dorks)} dorks from GHDB", "OK")
    return dorks


# ============================================================
# ORCHESTRATOR
# ============================================================

def run_dork_campaign(target, dork_type, engines=None, execute=False, max_per_engine=2):
    """Run a full dork campaign — generate queries, optionally execute them."""
    # Generate dorks
    generators = {
        "domain": generate_domain_dorks,
        "creds": generate_creds_dorks,
        "person": generate_person_dorks,
        "social": generate_social_dorks,
        "email": generate_email_dorks,
        "username": generate_username_dorks,
        "company": generate_person_dorks,
    }

    gen_func = generators.get(dork_type)
    if not gen_func:
        log(f"Unknown dork type: {dork_type}", "ERROR")
        return None

    log(f"=== Generating {dork_type} dorks for: {target} ===")
    dorks = gen_func(target)
    log(f"Generated {len(dorks)} dork queries")

    if not execute:
        # Just print the dorks
        print(f"\n{'='*60}")
        print(f"DORK QUERIES — Copy-paste into any search engine:")
        print(f"{'='*60}\n")
        for name, query in dorks.items():
            print(f"# {name}")
            print(f"  {query}")
            print()
        print(f"Total: {len(dorks)} queries")
        print(f"\nTo execute: python dork_engine.py {dork_type} {target} --execute")
        return dorks

    # Execute dorks against search engines
    if engines is None:
        engines = ["google", "bing", "duckduckgo", "yandex", "brave"]

    log(f"\n=== Executing {len(dorks)} dork queries across {len(engines)} engines ===")
    log(f"Engines: {', '.join(engines)}")

    all_results = {}
    total_hits = 0

    for i, (name, query) in enumerate(dorks.items(), 1):
        log(f"\n[{i}/{len(dorks)}] {name}", "DORK")
        log(f"  Query: {query}")

        result = multi_engine_scrape(query, engines=engines, max_pages_per_engine=max_per_engine)
        all_results[name] = {
            "query": query,
            "total_results": result["total_results"],
            "urls": result["unique_urls"],
            "per_engine": {k: v["results_count"] for k, v in result["per_engine"].items()},
        }
        total_hits += result["total_results"]

        if result["total_results"] > 0:
            for url in result["unique_urls"][:5]:
                log(f"    → {url}", "HIT")
            if result["total_results"] > 5:
                log(f"    ... and {result['total_results'] - 5} more", "INFO")

    # Save results
    clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', target)[:50]
    ts = datetime.now().strftime("%d_%b_%Y")
    out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)

    report = {
        "target": target,
        "type": f"dork_{dork_type}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "engines_used": engines,
        "total_queries": len(dorks),
        "total_hits": total_hits,
        "results": all_results,
    }

    path = os.path.join(out_dir, "data", f"dorks_{dork_type}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str, ensure_ascii=False)

    log(f"\n{'='*60}", "OK")
    log(f"CAMPAIGN COMPLETE", "OK")
    log(f"Queries: {len(dorks)}", "OK")
    log(f"Total hits: {total_hits}", "OK")
    log(f"Results: {path}", "OK")

    return report


# ============================================================
# CLI
# ============================================================

DORK_TYPES = {
    "domain": generate_domain_dorks,
    "creds": generate_creds_dorks,
    "person": generate_person_dorks,
    "social": generate_social_dorks,
    "email": generate_email_dorks,
    "username": generate_username_dorks,
    "company": generate_person_dorks,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python dork_engine.py <type> <target> [--execute] [--engines google,bing,ddg]")
        print(f"\nTypes: {', '.join(DORK_TYPES.keys())}, ghdb")
        print(f"\nEngines: google, bing, duckduckgo, yandex, brave, aol, startpage, mojeek")
        print(f"\nExamples:")
        print(f"  python dork_engine.py domain example.com                    # Generate dorks")
        print(f"  python dork_engine.py domain example.com --execute          # Scrape engines")
        print(f"  python dork_engine.py creds example.com --execute           # Credential dorks")
        print(f"  python dork_engine.py social \"John Doe\" --execute          # Social dorks")
        print(f"  python dork_engine.py domain example.com --execute --engines ddg,brave")
        print(f"  python dork_engine.py ghdb                                  # Fetch from Exploit-DB")
        print(f"\nNo API keys needed — scrapes search engine HTML directly.")
        print(f"Uses User-Agent rotation + random delays to avoid blocks.")
        sys.exit(1)

    target_type = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else ""

    # Parse flags
    execute = "--execute" in sys.argv
    engines = None
    for i, arg in enumerate(sys.argv):
        if arg == "--engines" and i + 1 < len(sys.argv):
            engines = sys.argv[i + 1].split(",")

    if target_type == "ghdb":
        dorks = fetch_ghdb()
        if execute:
            log(f"Executing {len(dorks)} GHDB dorks...")
            for dork in dorks[:10]:
                log(f"\n  Dork: {dork}", "DORK")
                result = multi_engine_scrape(dork, engines=engines or ["google", "bing"])
                if result["total_results"] > 0:
                    for url in result["unique_urls"][:3]:
                        log(f"    → {url}", "HIT")
                time.sleep(random.uniform(3, 6))
        else:
            for d in dorks:
                print(f"  {d}")
        return

    if not target:
        print("Error: target required")
        sys.exit(1)

    if target_type not in DORK_TYPES:
        print(f"Unknown type: {target_type}. Use: {', '.join(DORK_TYPES.keys())}")
        sys.exit(1)

    run_dork_campaign(target, target_type, engines=engines, execute=execute)


if __name__ == "__main__":
    main()
