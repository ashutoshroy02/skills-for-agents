#!/usr/bin/env python3
"""
logo_hunter.py — Search the web for existing logos, icons, and favicons.
Downloads candidates from free icon libraries and image search.

Usage:
    python logo_hunter.py --name "ProjectName" --topic "AI chatbot" --output ./brand/
    python logo_hunter.py --name "NightOwl" --symbol owl --output ./brand/
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import hashlib
from pathlib import Path

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

def get_ua():
    import random
    return random.choice(USER_AGENTS)

def fetch(url, timeout=15):
    """Fetch URL content. Returns (content_bytes, content_type) or (None, None)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": get_ua()})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get("Content-Type", "")
            return resp.read(), ct
    except Exception as e:
        return None, str(e)

def download_file(url, output_path, timeout=30):
    """Download a file to disk. Returns True on success."""
    data, ct = fetch(url, timeout=timeout)
    if data and len(data) > 100:  # Minimum viable file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(data)
        return True
    return False

# ─── Source 1: Google Favicon API ───
def fetch_google_favicon(domain, output_dir):
    """Fetch favicon from Google's favicon API (works for any domain)."""
    url = f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    out = os.path.join(output_dir, f"google-favicon-{domain}.png")
    if download_file(url, out):
        return {"source": "google_favicon", "url": url, "file": out, "size": "128x128"}
    return None

# ─── Source 2: DuckDuckGo Favicon API ───
def fetch_ddg_favicon(domain, output_dir):
    """Fetch favicon from DuckDuckGo's API."""
    url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
    out = os.path.join(output_dir, f"ddg-favicon-{domain}.ico")
    if download_file(url, out):
        return {"source": "duckduckgo_favicon", "url": url, "file": out}
    return None

# ─── Source 3: Favicon.im API ───
def fetch_favicon_im(domain, output_dir):
    """Fetch favicon from favicon.im."""
    url = f"https://favicon.im/{domain}"
    out = os.path.join(output_dir, f"favicon-im-{domain}.png")
    if download_file(url, out):
        return {"source": "favicon.im", "url": url, "file": out}
    return None

# ─── Source 4: Search SVG Repo ───
def search_svg_repo(query, output_dir, max_results=3):
    """Search SVG Repo for free SVG icons."""
    results = []
    search_url = f"https://www.svgrepo.com/vectors/{urllib.parse.quote(query)}/"
    data, _ = fetch(search_url)
    if not data:
        return results

    html = data.decode("utf-8", errors="ignore")
    # Extract SVG download links
    svg_pattern = r'href="(/download/[^"]+\.svg)"'
    matches = re.findall(svg_pattern, html)

    for i, path in enumerate(matches[:max_results]):
        url = f"https://www.svgrepo.com{path}"
        out = os.path.join(output_dir, f"svgrepo-{query}-{i+1}.svg")
        if download_file(url, out):
            results.append({"source": "svg_repo", "query": query, "file": out, "url": url})
        time.sleep(1)

    return results

# ─── Source 5: Search Flaticon (free icons) ───
def search_flaticon(query, output_dir, max_results=3):
    """Search Flaticon for free icons (downloads PNG previews)."""
    results = []
    search_url = f"https://www.flaticon.com/search?word={urllib.parse.quote(query)}&type=icon"
    data, _ = fetch(search_url)
    if not data:
        return results

    html = data.decode("utf-8", errors="ignore")
    # Extract icon image URLs from the page
    img_pattern = r'https://cdn-icons-png\.flaticon\.com/[^"]+\.png'
    matches = list(set(re.findall(img_pattern, html)))

    for i, url in enumerate(matches[:max_results]):
        out = os.path.join(output_dir, f"flaticon-{query}-{i+1}.png")
        if download_file(url, out):
            results.append({"source": "flaticon", "query": query, "file": out, "url": url})
        time.sleep(1)

    return results

# ─── Source 6: Search Icons8 ───
def search_icons8(query, output_dir, max_results=3):
    """Search Icons8 for free icons."""
    results = []
    # Icons8 has a public API for searching
    api_url = f"https://api.icons8.com/api/iconsets/v4/search?term={urllib.parse.quote(query)}&platform=color&limit={max_results}"
    data, _ = fetch(api_url)
    if data:
        try:
            icons = json.loads(data)
            for icon in icons[:max_results]:
                if "png" in icon:
                    url = icon["png"].get("128") or icon["png"].get("64")
                    if url:
                        out = os.path.join(output_dir, f"icons8-{query}-{icon.get('id', 'unknown')}.png")
                        if download_file(url, out):
                            results.append({"source": "icons8", "file": out, "url": url})
        except json.JSONDecodeError:
            pass

    return results

# ─── Source 7: OpenMoji (open-source emojis) ───
def search_openmoji(query, output_dir, max_results=3):
    """Search OpenMoji for emoji-based logos."""
    results = []
    # OpenMoji has a searchable JSON
    data, _ = fetch("https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/data/openmoji.json")
    if not data:
        return results

    try:
        emojis = json.loads(data)
        matches = [e for e in emojis if query.lower() in e.get("annotation", "").lower()
                   or query.lower() in e.get("tags", "").lower()]

        for emoji in matches[:max_results]:
            hex_code = emoji["hexcode"]
            url = f"https://openmoji.org/data/color/svg/{hex_code}.svg"
            out = os.path.join(output_dir, f"openmoji-{hex_code}.svg")
            if download_file(url, out):
                results.append({"source": "openmoji", "annotation": emoji["annotation"], "file": out})
            time.sleep(0.5)
    except json.JSONDecodeError:
        pass

    return results

# ─── Source 8: Twemoji (Twitter emojis) ───
def fetch_twemoji(emoji_char, output_dir):
    """Fetch a Twemoji SVG by emoji character."""
    # Convert emoji to codepoint
    codepoint = "-".join(f"{ord(c):x}" for c in emoji_char)
    url = f"https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg/{codepoint}.svg"
    out = os.path.join(output_dir, f"twemoji-{codepoint}.svg")
    if download_file(url, out):
        return {"source": "twemoji", "codepoint": codepoint, "file": out}
    return None

# ─── Main Hunt ───
def hunt(name, topic=None, symbol=None, domain=None, output_dir="./brand"):
    """Run the full logo hunt across all sources."""
    os.makedirs(output_dir, exist_ok=True)
    results = {"queries": [], "downloads": [], "errors": []}

    search_terms = [name]
    if topic:
        search_terms.append(topic)
    if symbol:
        search_terms.append(symbol)

    print(f"[*] Hunting logos for: {name}")
    print(f"[*] Search terms: {search_terms}")
    print(f"[*] Output: {output_dir}\n")

    # 1. Google/DDG favicons (if domain provided)
    if domain:
        print(f"[1] Fetching favicons for {domain}...")
        for fetcher in [fetch_google_favicon, fetch_ddg_favicon, fetch_favicon_im]:
            result = fetcher(domain, output_dir)
            if result:
                results["downloads"].append(result)
                print(f"    + {result['source']}: {result['file']}")

    # 2. SVG Repo
    for term in search_terms[:2]:
        print(f"\n[2] Searching SVG Repo for '{term}'...")
        found = search_svg_repo(term, output_dir)
        results["downloads"].extend(found)
        for r in found:
            print(f"    + {r['file']}")
        time.sleep(2)

    # 3. Flaticon
    for term in search_terms[:2]:
        print(f"\n[3] Searching Flaticon for '{term}'...")
        found = search_flaticon(term, output_dir)
        results["downloads"].extend(found)
        for r in found:
            print(f"    + {r['file']}")
        time.sleep(2)

    # 4. Icons8
    for term in search_terms[:1]:
        print(f"\n[4] Searching Icons8 for '{term}'...")
        found = search_icons8(term, output_dir)
        results["downloads"].extend(found)
        for r in found:
            print(f"    + {r['file']}")
        time.sleep(1)

    # 5. OpenMoji
    symbol_term = symbol or name
    print(f"\n[5] Searching OpenMoji for '{symbol_term}'...")
    found = search_openmoji(symbol_term, output_dir)
    results["downloads"].extend(found)
    for r in found:
        print(f"    + {r['file']} ({r.get('annotation', '')})")

    # Summary
    print(f"\n{'='*60}")
    print(f"[RESULTS] Found {len(results['downloads'])} assets")
    print(f"{'='*60}")
    for d in results["downloads"]:
        print(f"  [{d['source']}] {d['file']}")

    # Save manifest
    manifest_path = os.path.join(output_dir, "hunt-results.json")
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[*] Manifest saved: {manifest_path}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hunt for logos, icons, and favicons across the web")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--topic", help="Project topic/description (for broader search)")
    parser.add_argument("--symbol", help="Symbol/animal/object to search for (e.g., 'owl', 'rocket')")
    parser.add_argument("--domain", help="Domain to fetch favicon from")
    parser.add_argument("--output", default="./brand", help="Output directory")
    args = parser.parse_args()

    hunt(args.name, args.topic, args.symbol, args.domain, args.output)
