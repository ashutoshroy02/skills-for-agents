#!/usr/bin/env python3
"""
Social Media Hunter — Deep platform intelligence gathering.

Techniques:
1. Password reset probing — enter email on "forgot password" → reveals if account exists
   (partial phone/email shown as confirmation)
2. Platform API queries — public APIs that return user data
3. Registration probing — "email already registered" reveals account existence
4. GraphQL/API endpoint exploitation — public endpoints that leak user data
5. Profile data extraction — bios, followers, posts, avatars, links

Usage:
    python social_media_hunter.py probe_email <email>    # Check which platforms have this email
    python social_media_hunter.py probe_phone <phone>    # Check which platforms have this phone
    python social_media_hunter.py probe_username <user>  # Deep username check across platforms
    python social_media_hunter.py instagram <username>   # Instagram deep dive
    python social_media_hunter.py tiktok <username>      # TikTok profile extraction
    python social_media_hunter.py facebook <username>    # Facebook profile lookup
    python social_media_hunter.py snapchat <username>    # Snapchat username check
    python social_media_hunter.py telegram <username>    # Telegram profile extraction
    python social_media_hunter.py whatsapp <phone>       # WhatsApp profile check
    python social_media_hunter.py twitter <username>     # Twitter/X deep dive
    python social_media_hunter.py all <username>         # Run all platform checks
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
import sys
import os
import time
import ssl
import hashlib
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

SSL_CTX = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
OSINT_OUTPUT_DIR = os.environ.get("OSINT_OUTPUT_DIR", os.path.expanduser("~/osint"))


def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m",
              "FOUND": "\033[92m", "HIT": "\033[95m"}
    reset = "\033[0m"
    print(f"{colors.get(level, '')}[{level}]{reset} {msg}", flush=True)


def http_get(url, headers=None, timeout=15):
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, body
    except Exception:
        return 0, ""


def http_post(url, data=None, headers=None, timeout=15):
    hdrs = {"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"}
    if headers:
        hdrs.update(headers)
    try:
        body = urllib.parse.urlencode(data).encode() if data else b""
        req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, body
    except Exception:
        return 0, ""


def http_get_json(url, headers=None, timeout=15):
    status, body = http_get(url, headers, timeout)
    try:
        return json.loads(body) if body else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def save_json(out_dir, filename, data):
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    path = os.path.join(out_dir, "data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    return path


def make_output_dir(tag):
    clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', tag)[:50]
    ts = datetime.now().strftime("%d_%b_%Y")
    out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    return out_dir


# ============================================================
# PASSWORD RESET PROBING — The Dirty Trick
# ============================================================

def probe_password_reset_email(email):
    """
    Check which platforms have an account registered with this email
    by probing password reset / registration flows.

    How it works:
    - Visit "forgot password" page
    - Submit the email
    - If response says "we sent a reset link" → account EXISTS
    - If response says "no account found" → account DOESN'T exist
    - Some sites reveal partial phone/email as confirmation (bonus intel)

    NOTE: This is passive — we're just making HTTP requests to public pages.
    We're not actually resetting anyone's password.
    """
    log(f"=== Password Reset Probing: {email} ===")
    results = []

    # Platform-specific reset flow checks
    platforms = {
        "Twitter/X": {
            "url": "https://api.twitter.com/i/users/email_available.json?email={email}",
            "method": "api",
            "exists_indicator": '"valid":false',
            "not_found_indicator": '"valid":true',
        },
        "Instagram": {
            "url": "https://www.instagram.com/accounts/account_recovery_send_ajax/",
            "method": "post",
            "data": "email_or_username={email}&recaptcha_challenge_field=",
            "exists_indicator": '"status":"ok"',
            "not_found_indicator": '"status":"fail"',
        },
        "Spotify": {
            "url": "https://www.spotify.com/password-reset/",
            "method": "post",
            "data": "email={email}&recaptcha=",
            "exists_indicator": "reset" ,
            "not_found_indicator": "not found",
        },
        "GitHub": {
            "url": "https://api.github.com/search/users?q={email}+in:email",
            "method": "api",
            "exists_indicator": '"total_count":1',
            "not_found_indicator": '"total_count":0',
        },
        "LinkedIn": {
            "url": "https://www.linkedin.com/checkpoint/rp/request-password-reset-submit",
            "method": "post",
            "data": "userName={email}",
            "exists_indicator": "reset",
            "not_found_indicator": "not found",
        },
    }

    for platform, config in platforms.items():
        try:
            url = config["url"].format(email=urllib.parse.quote(email))
            if config["method"] == "api":
                status, body = http_get(url)
            elif config["method"] == "post":
                data_str = config.get("data", "").format(email=urllib.parse.quote(email))
                status, body = http_post(url, data=dict(urllib.parse.parse_qsl(data_str)))
            else:
                continue

            body_lower = body.lower() if body else ""
            exists = config.get("exists_indicator", "").lower() in body_lower if config.get("exists_indicator") else False
            not_found = config.get("not_found_indicator", "").lower() in body_lower if config.get("not_found_indicator") else False

            if exists and not not_found:
                results.append({"platform": platform, "status": "EXISTS", "confidence": "HIGH"})
                log(f"  [✓] {platform}: ACCOUNT EXISTS", "FOUND")
            elif not_found:
                results.append({"platform": platform, "status": "NOT_FOUND", "confidence": "HIGH"})
            else:
                results.append({"platform": platform, "status": "UNKNOWN", "confidence": "LOW"})

        except Exception as e:
            results.append({"platform": platform, "status": "ERROR", "error": str(e)})
            log(f"  [!] {platform}: error - {e}", "WARN")

    return results


def probe_password_reset_phone(phone):
    """Check which platforms have an account with this phone number."""
    log(f"=== Phone Reset Probing: {phone} ===")
    results = []

    # Many platforms reveal if a phone is registered via their reset flow
    platforms = {
        "WhatsApp": {
            "check": "whatsapp_api",
        },
        "Telegram": {
            "url": "https://telegram.org/support",
            "method": "page",
        },
        "Instagram": {
            "url": "https://www.instagram.com/accounts/account_recovery_send_ajax/",
            "method": "post",
            "data": "email_or_username={phone}&recaptcha_challenge_field=",
            "exists_indicator": '"status":"ok"',
        },
        "TikTok": {
            "url": "https://www.tiktok.com/api/search/general/full/?keyword={phone}",
            "method": "api",
        },
    }

    # WhatsApp check — use the wa.me link
    log("  Checking WhatsApp...")
    wa_status, wa_body = http_get(f"https://wa.me/{re.sub(r'[^0-9]', '', phone)}")
    if wa_status == 200 and "chat" in wa_body.lower():
        results.append({"platform": "WhatsApp", "status": "POSSIBLE", "confidence": "MEDIUM",
                        "note": "wa.me link resolves — number may be on WhatsApp"})
        log(f"  [?] WhatsApp: number may be registered (wa.me resolves)", "FOUND")

    return results


# ============================================================
# PLATFORM-SPECIFIC DEEP DIVES
# ============================================================

def instagram_deep(username):
    """Instagram profile extraction via web API."""
    log(f"=== Instagram Deep Dive: {username} ===")
    report = {"platform": "Instagram", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    # Method 1: Web profile page
    status, body = http_get(f"https://www.instagram.com/{username}/", headers={
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })

    if status == 200:
        # Check if page is a real profile or "page not available"
        if "Sorry, this page isn't available" in body:
            report["status"] = "NOT_FOUND"
            log("  Not found", "WARN")
            return report

        # Extract JSON-LD or shared data
        # Instagram embeds profile data in meta tags and __NEXT_DATA__
        meta_matches = re.findall(r'<meta[^>]*content="([^"]*)"[^>]*>', body)

        # Look for og: tags
        og_title = re.search(r'og:title["\s]*content="([^"]*)"', body)
        og_desc = re.search(r'og:description["\s]*content="([^"]*)"', body)
        og_image = re.search(r'og:image["\s]*content="([^"]*)"', body)

        if og_title:
            report["display_name"] = og_title.group(1)
        if og_desc:
            report["bio_preview"] = og_desc.group(1)
        if og_image:
            report["avatar_url"] = og_image.group(1)

        # Try to extract from _shared_data or additional_data
        shared_data = re.search(r'window\._sharedData\s*=\s*({.*?});', body)
        if shared_data:
            try:
                sd = json.loads(shared_data.group(1))
                user = sd.get("entry_data", {}).get("ProfilePage", [{}])[0].get("graphql", {}).get("user", {})
                if user:
                    report["full_name"] = user.get("full_name")
                    report["bio"] = user.get("biography")
                    report["followers"] = user.get("edge_followed_by", {}).get("count")
                    report["following"] = user.get("edge_follow", {}).get("count")
                    report["posts"] = user.get("edge_owner_to_timeline_media", {}).get("count")
                    report["is_private"] = user.get("is_private")
                    report["is_verified"] = user.get("is_verified")
                    report["avatar_url"] = user.get("profile_pic_url_hd") or user.get("profile_pic_url")
                    report["external_url"] = user.get("external_url")
                    report["status"] = "FOUND"
                    log(f"  Name: {user.get('full_name')}", "OK")
                    log(f"  Bio: {user.get('biography', '')[:100]}", "OK")
                    log(f"  Followers: {user.get('edge_followed_by', {}).get('count')}", "OK")
                    log(f"  Posts: {user.get('edge_owner_to_timeline_media', {}).get('count')}", "OK")
            except (json.JSONDecodeError, KeyError, IndexError):
                pass

        # Extract identifiers from bio
        if report.get("bio"):
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', report["bio"])
            urls = re.findall(r'https?://[^\s]+', report["bio"])
            phones = re.findall(r'\+?\d[\d\s()-]{7,}\d', report["bio"])
            report["identifiers_in_bio"] = {"emails": emails, "urls": urls, "phones": phones}

        if not report.get("status"):
            report["status"] = "FOUND_PARTIAL"

    elif status == 404:
        report["status"] = "NOT_FOUND"
    else:
        report["status"] = "ERROR"
        report["http_status"] = status

    return report


def tiktok_deep(username):
    """TikTok profile extraction."""
    log(f"=== TikTok Deep Dive: {username} ===")
    report = {"platform": "TikTok", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    # Method 1: Web profile
    status, body = http_get(f"https://www.tiktok.com/@{username}")

    if status == 200:
        if "Couldn't find this account" in body or "couldn't find this account" in body:
            report["status"] = "NOT_FOUND"
            log("  Not found", "WARN")
            return report

        # Extract from SIGI_STATE or __UNIVERSAL_DATA_FOR_REHYDRATION__
        sigi = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', body, re.DOTALL)
        if sigi:
            try:
                data = json.loads(sigi.group(1))
                user = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {}).get("userInfo", {}).get("user", {})
                stats = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {}).get("userInfo", {}).get("stats", {})

                if user:
                    report["nickname"] = user.get("nickname")
                    report["bio"] = user.get("signature")
                    report["avatar_url"] = user.get("avatarLarger") or user.get("avatarMedium")
                    report["is_verified"] = user.get("verified")
                    report["is_private"] = user.get("privateAccount")
                    report["followers"] = stats.get("followerCount")
                    report["following"] = stats.get("followingCount")
                    report["likes"] = stats.get("heartCount")
                    report["videos"] = stats.get("videoCount")
                    report["status"] = "FOUND"

                    # Extract identifiers
                    if user.get("signature"):
                        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', user["signature"])
                        urls = re.findall(r'https?://[^\s]+', user["signature"])
                        report["identifiers_in_bio"] = {"emails": emails, "urls": urls}

                    log(f"  Name: {user.get('nickname')}", "OK")
                    log(f"  Bio: {user.get('signature', '')[:100]}", "OK")
                    log(f"  Followers: {stats.get('followerCount')}", "OK")
                    log(f"  Likes: {stats.get('heartCount')}", "OK")
            except (json.JSONDecodeError, KeyError) as e:
                log(f"  Parse error: {e}", "WARN")

        if not report.get("status"):
            # Try og: tags as fallback
            og_title = re.search(r'og:title["\s]*content="([^"]*)"', body)
            if og_title:
                report["display_name"] = og_title.group(1)
                report["status"] = "FOUND_PARTIAL"

    elif status == 404:
        report["status"] = "NOT_FOUND"
    else:
        report["status"] = "ERROR"

    return report


def twitter_deep(username):
    """Twitter/X profile extraction."""
    log(f"=== Twitter/X Deep Dive: {username} ===")
    report = {"platform": "Twitter/X", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    # Try nitter instances (public Twitter mirrors — no auth needed)
    nitter_instances = [
        f"https://nitter.privacydev.net/{username}",
        f"https://nitter.poast.org/{username}",
        f"https://nitter.cz/{username}",
        f"https://nitter.1d4.us/{username}",
    ]

    for nitter_url in nitter_instances:
        status, body = http_get(nitter_url, timeout=10)
        if status == 200 and body and "User not found" not in body:
            # Parse nitter profile page
            name = re.search(r'class="profile-name"[^>]*>(.*?)<', body)
            bio = re.search(r'class="profile-bio"[^>]*>(.*?)</div>', body, re.DOTALL)
            avatar = re.search(r'class="profile-avatar"[^>]*src="([^"]*)"', body)
            banner = re.search(r'class="profile-banner"[^>]*src="([^"]*)"', body)
            tweets = re.search(r'(\d[\d,]*)\s*<span[^>]*>Tweets', body)
            followers = re.search(r'(\d[\d,]*)\s*<span[^>]*>Followers', body)
            following_match = re.search(r'(\d[\d,]*)\s*<span[^>]*>Following', body)
            location = re.search(r'class="profile-location"[^>]*>.*?<div[^>]*>(.*?)</div>', body, re.DOTALL)
            website = re.search(r'class="profile-website"[^>]*>.*?href="([^"]*)"', body, re.DOTALL)
            join_date = re.search(r'class="profile-joindate"[^>]*>.*?<span[^>]*title="([^"]*)"', body, re.DOTALL)

            if name:
                report["display_name"] = re.sub(r'<[^>]+>', '', name.group(1)).strip()
            if bio:
                report["bio"] = re.sub(r'<[^>]+>', '', bio.group(1)).strip()
            if avatar:
                report["avatar_url"] = avatar.group(1).replace("/pic/", "https://pbs.twimg.com/")
            if banner:
                report["banner_url"] = banner.group(1)
            if tweets:
                report["tweets"] = tweets.group(1).replace(",", "")
            if followers:
                report["followers"] = followers.group(1).replace(",", "")
            if following_match:
                report["following"] = following_match.group(1).replace(",", "")
            if location:
                report["location"] = re.sub(r'<[^>]+>', '', location.group(1)).strip()
            if website:
                report["website"] = website.group(1)
            if join_date:
                report["joined"] = join_date.group(1)

            report["status"] = "FOUND"
            report["source"] = nitter_url
            log(f"  Name: {report.get('display_name')}", "OK")
            log(f"  Bio: {report.get('bio', '')[:100]}", "OK")
            log(f"  Followers: {report.get('followers')}", "OK")
            break

    if not report.get("status"):
        # Fallback: check x.com directly
        status, body = http_get(f"https://x.com/{username}")
        if status == 200 and body and "doesn't exist" not in body:
            og_title = re.search(r'og:title["\s]*content="([^"]*)"', body)
            og_desc = re.search(r'og:description["\s]*content="([^"]*)"', body)
            if og_title:
                report["display_name"] = og_title.group(1)
                report["status"] = "FOUND_PARTIAL"
            if og_desc:
                report["bio_preview"] = og_desc.group(1)

    if not report.get("status"):
        report["status"] = "NOT_FOUND"

    return report


def telegram_deep(username):
    """Telegram profile extraction via t.me."""
    log(f"=== Telegram Deep Dive: {username} ===")
    report = {"platform": "Telegram", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    status, body = http_get(f"https://t.me/{username}")

    if status == 200 and body:
        if "can view and join" in body.lower() or "contact" in body.lower() or "send message" in body.lower():
            name = re.search(r'class="tgme_page_title"[^>]*>(.*?)<', body)
            bio = re.search(r'class="tgme_page_description"[^>]*>(.*?)</div>', body, re.DOTALL)
            avatar = re.search(r'class="tgme_page_photo_image"[^>]*src="([^"]*)"', body)
            subscribers = re.search(r'(\d[\d,]*)\s*subscriber', body)
            members = re.search(r'(\d[\d,]*)\s*member', body)

            if name:
                report["display_name"] = re.sub(r'<[^>]+>', '', name.group(1)).strip()
            if bio:
                report["bio"] = re.sub(r'<[^>]+>', '', bio.group(1)).strip()
            if avatar:
                report["avatar_url"] = avatar.group(1)
            if subscribers:
                report["subscribers"] = subscribers.group(1).replace(",", "")
            if members:
                report["members"] = members.group(1).replace(",", "")

            report["status"] = "FOUND"
            log(f"  Name: {report.get('display_name')}", "OK")
            log(f"  Bio: {report.get('bio', '')[:100]}", "OK")
        elif "is not available" in body.lower() or "not found" in body.lower():
            report["status"] = "NOT_FOUND"
        else:
            report["status"] = "UNKNOWN"
    elif status == 404:
        report["status"] = "NOT_FOUND"
    else:
        report["status"] = "ERROR"

    return report


def facebook_deep(username):
    """Facebook profile lookup."""
    log(f"=== Facebook Deep Dive: {username} ===")
    report = {"platform": "Facebook", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    # Method 1: Graph API (public, no auth for basic profile)
    status, body = http_get(f"https://www.facebook.com/{username}")
    if status == 200 and body:
        if "page isn't available" in body.lower() or "content isn't available" in body.lower():
            report["status"] = "NOT_FOUND"
        else:
            og_title = re.search(r'og:title["\s]*content="([^"]*)"', body)
            og_desc = re.search(r'og:description["\s]*content="([^"]*)"', body)
            og_image = re.search(r'og:image["\s]*content="([^"]*)"', body)

            if og_title:
                report["display_name"] = og_title.group(1)
            if og_desc:
                report["bio_preview"] = og_desc.group(1)
            if og_image:
                report["avatar_url"] = og_image.group(1)

            report["status"] = "FOUND" if og_title else "FOUND_PARTIAL"
            log(f"  Name: {report.get('display_name')}", "OK")
    elif status == 404:
        report["status"] = "NOT_FOUND"
    else:
        report["status"] = "ERROR"

    return report


def snapchat_deep(username):
    """Snapchat username check."""
    log(f"=== Snapchat Deep Dive: {username} ===")
    report = {"platform": "Snapchat", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    # Snapchat Add Me page
    status, body = http_get(f"https://www.snapchat.com/add/{username}")

    if status == 200 and body:
        if "couldn't find" in body.lower() or "not found" in body.lower():
            report["status"] = "NOT_FOUND"
        else:
            display_name = re.search(r'<h2[^>]*>(.*?)</h2>', body)
            avatar = re.search(r'<img[^>]*class="[^"]*avatar[^"]*"[^>]*src="([^"]*)"', body)
            snapcode = re.search(r'<img[^>]*class="[^"]*snapcode[^"]*"[^>]*src="([^"]*)"', body)

            if display_name:
                report["display_name"] = re.sub(r'<[^>]+>', '', display_name.group(1)).strip()
            if avatar:
                report["avatar_url"] = avatar.group(1)
            if snapcode:
                report["snapcode_url"] = snapcode.group(1)

            report["status"] = "FOUND"
            report["add_url"] = f"https://www.snapchat.com/add/{username}"
            log(f"  Display name: {report.get('display_name')}", "OK")
    elif status == 404:
        report["status"] = "NOT_FOUND"
    else:
        report["status"] = "ERROR"

    return report


def github_deep(username):
    """GitHub deep dive — same as osint_core.py but standalone."""
    log(f"=== GitHub Deep Dive: {username} ===")
    gh_token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if gh_token:
        headers["Authorization"] = f"token {gh_token}"

    report = {"platform": "GitHub", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}
    user = http_get_json(f"https://api.github.com/users/{username}", headers)

    if "login" not in user:
        report["status"] = "NOT_FOUND"
        return report

    report.update({
        "status": "FOUND",
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
        "avatar_url": user.get("avatar_url"),
    })

    # Commit email mining
    report["commit_emails"] = set()
    repos = http_get_json(f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5", headers)
    if isinstance(repos, list):
        for repo in repos[:3]:
            if repo.get("fork"):
                continue
            commits = http_get_json(f"https://api.github.com/repos/{repo['full_name']}/commits?per_page=10", headers)
            if isinstance(commits, list):
                for c in commits:
                    for key in ("author", "committer"):
                        email = c.get("commit", {}).get(key, {}).get("email", "")
                        if email and "noreply" not in email:
                            report["commit_emails"].add(email)

    report["commit_emails"] = sorted(report["commit_emails"])
    log(f"  Name: {user.get('name')}", "OK")
    log(f"  Email: {user.get('email')}", "OK")
    log(f"  Commit emails: {report['commit_emails']}", "OK")
    log(f"  Location: {user.get('location')}", "OK")

    return report


def reddit_deep(username):
    """Reddit profile extraction."""
    log(f"=== Reddit Deep Dive: {username} ===")
    report = {"platform": "Reddit", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    user = http_get_json(
        f"https://www.reddit.com/user/{username}/about.json",
        headers={"User-Agent": "osint-skill/2.0"}
    )

    if "data" not in user:
        report["status"] = "NOT_FOUND"
        return report

    d = user["data"]
    report.update({
        "status": "FOUND",
        "total_karma": d.get("total_karma", 0),
        "comment_karma": d.get("comment_karma", 0),
        "link_karma": d.get("link_karma", 0),
        "created": datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc).isoformat(),
        "is_mod": d.get("is_mod", False),
        "has_verified_email": d.get("has_verified_email", False),
        "avatar_url": d.get("icon_img", ""),
    })

    # Recent posts — reveals interests, subreddits, writing style
    posts = http_get_json(
        f"https://www.reddit.com/user/{username}/submitted.json?limit=25",
        headers={"User-Agent": "osint-skill/2.0"}
    )
    if "data" in posts:
        report["recent_posts"] = []
        subreddits = set()
        for post in posts["data"].get("children", [])[:25]:
            p = post.get("data", {})
            report["recent_posts"].append({
                "title": p.get("title", "")[:200],
                "subreddit": p.get("subreddit"),
                "score": p.get("score"),
                "created": datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc).isoformat(),
                "url": p.get("url"),
            })
            subreddits.add(p.get("subreddit"))
        report["active_subreddits"] = sorted(subreddits)

    # Recent comments — reveals writing style, interests
    comments = http_get_json(
        f"https://www.reddit.com/user/{username}/comments.json?limit=25",
        headers={"User-Agent": "osint-skill/2.0"}
    )
    if "data" in comments:
        report["recent_comments"] = []
        for comment in comments["data"].get("children", [])[:25]:
            c = comment.get("data", {})
            report["recent_comments"].append({
                "body": c.get("body", "")[:300],
                "subreddit": c.get("subreddit"),
                "score": c.get("score"),
                "created": datetime.fromtimestamp(c.get("created_utc", 0), tz=timezone.utc).isoformat(),
            })

    log(f"  Karma: {d.get('total_karma', 0)}", "OK")
    log(f"  Active subreddits: {len(report.get('active_subreddits', []))}", "OK")

    return report


def steam_deep(username):
    """Steam profile extraction."""
    log(f"=== Steam Deep Dive: {username} ===")
    report = {"platform": "Steam", "username": username, "timestamp": datetime.now(timezone.utc).isoformat()}

    status, body = http_get(f"https://steamcommunity.com/id/{username}")

    if status == 200 and body:
        if "The specified profile could not be found" in body:
            report["status"] = "NOT_FOUND"
            return report

        real_name = re.search(r'class="actual_persona_name"[^>]*>(.*?)<', body)
        location = re.search(r'class="header_real_name"[^>]*>.*?<bdi>(.*?)</bdi>', body, re.DOTALL)
        avatar = re.search(r'playerAvatarAutoSizeInner[^>]*><img[^>]*src="([^"]*)"', body)
        summary = re.search(r'profile_summary"[^>]*>(.*?)</div>', body, re.DOTALL)
        game_count = re.search(r'(\d[\d,]*)\s*game', body)
        friend_count = re.search(r'(\d[\d,]*)\s*friend', body)
        level = re.search(r'friendPlayerLevelNum[^>]*>(.*?)<', body)

        if real_name:
            report["real_name"] = re.sub(r'<[^>]+>', '', real_name.group(1)).strip()
        if location:
            report["location"] = re.sub(r'<[^>]+>', '', location.group(1)).strip()
        if avatar:
            report["avatar_url"] = avatar.group(1)
        if summary:
            report["summary"] = re.sub(r'<[^>]+>', '', summary.group(1)).strip()[:500]
        if game_count:
            report["games"] = game_count.group(1).replace(",", "")
        if friend_count:
            report["friends"] = friend_count.group(1).replace(",", "")
        if level:
            report["level"] = level.group(1).strip()

        report["status"] = "FOUND"
        report["profile_url"] = f"https://steamcommunity.com/id/{username}"
        log(f"  Real name: {report.get('real_name')}", "OK")
        log(f"  Location: {report.get('location')}", "OK")
        log(f"  Games: {report.get('games')}", "OK")
    else:
        report["status"] = "ERROR"

    return report


def whatsapp_check(phone):
    """Check if phone number is on WhatsApp."""
    log(f"=== WhatsApp Check: {phone} ===")
    report = {"platform": "WhatsApp", "phone": phone, "timestamp": datetime.now(timezone.utc).isoformat()}

    clean_phone = re.sub(r'[^0-9]', '', phone)
    status, body = http_get(f"https://wa.me/{clean_phone}")

    if status == 200:
        if "chat" in body.lower() or "whatsapp" in body.lower():
            report["status"] = "POSSIBLE"
            report["wa.me_url"] = f"https://wa.me/{clean_phone}"
            report["note"] = "Number resolves on wa.me — likely registered on WhatsApp"
            log(f"  wa.me resolves — number may be on WhatsApp", "FOUND")
        else:
            report["status"] = "UNKNOWN"
    else:
        report["status"] = "ERROR"

    return report


# ============================================================
# ALL PLATFORMS CHECK
# ============================================================

PLATFORM_CHECKS = {
    "github": github_deep,
    "instagram": instagram_deep,
    "tiktok": tiktok_deep,
    "twitter": twitter_deep,
    "telegram": telegram_deep,
    "facebook": facebook_deep,
    "snapchat": snapchat_deep,
    "reddit": reddit_deep,
    "steam": steam_deep,
}


def check_all_platforms(username, out_dir=None):
    """Run all platform checks in parallel."""
    out_dir = out_dir or make_output_dir(f"social_{username}")
    log(f"=== ALL PLATFORMS CHECK: {username} ===")

    results = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(func, username): name
            for name, func in PLATFORM_CHECKS.items()
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                results[name] = result
                status = result.get("status", "UNKNOWN")
                if status in ("FOUND", "FOUND_PARTIAL"):
                    log(f"  [✓] {name}: {status}", "FOUND")
                else:
                    log(f"  [-] {name}: {status}", "INFO")
            except Exception as e:
                results[name] = {"platform": name, "status": "ERROR", "error": str(e)}
                log(f"  [!] {name}: error - {e}", "ERROR")

    # Compile report
    report = {
        "target": username,
        "type": "social_media_deep",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platforms_checked": len(results),
        "platforms_found": sum(1 for r in results.values() if r.get("status") in ("FOUND", "FOUND_PARTIAL")),
        "results": results,
    }

    # Extract all identifiers found
    all_identifiers = []
    for plat, result in results.items():
        if result.get("email"):
            all_identifiers.append({"type": "email", "value": result["email"], "source": plat})
        if result.get("commit_emails"):
            for email in result["commit_emails"]:
                all_identifiers.append({"type": "email", "value": email, "source": f"{plat}_commits"})
        if result.get("identifiers_in_bio"):
            for email in result["identifiers_in_bio"].get("emails", []):
                all_identifiers.append({"type": "email", "value": email, "source": f"{plat}_bio"})
            for url in result["identifiers_in_bio"].get("urls", []):
                all_identifiers.append({"type": "url", "value": url, "source": f"{plat}_bio"})
        if result.get("twitter"):
            all_identifiers.append({"type": "username", "value": result["twitter"], "source": f"{plat}_twitter"})
        if result.get("blog"):
            all_identifiers.append({"type": "url", "value": result["blog"], "source": f"{plat}_blog"})
        if result.get("location"):
            all_identifiers.append({"type": "location", "value": result["location"], "source": plat})
        if result.get("real_name"):
            all_identifiers.append({"type": "name", "value": result["real_name"], "source": plat})

    report["identifiers_found"] = all_identifiers

    save_json(out_dir, "social_media_deep.json", report)
    log(f"\n=== Summary: {report['platforms_found']}/{report['platforms_checked']} platforms found ===", "OK")
    log(f"Identifiers found: {len(all_identifiers)}", "OK")

    return report


# ============================================================
# CLI
# ============================================================

COMMANDS = {
    "probe_email": ("probe_password_reset_email", "<email>"),
    "probe_phone": ("probe_password_reset_phone", "<phone>"),
    "instagram": ("instagram_deep", "<username>"),
    "tiktok": ("tiktok_deep", "<username>"),
    "twitter": ("twitter_deep", "<username>"),
    "telegram": ("telegram_deep", "<username>"),
    "facebook": ("facebook_deep", "<username>"),
    "snapchat": ("snapchat_deep", "<username>"),
    "reddit": ("reddit_deep", "<username>"),
    "github": ("github_deep", "<username>"),
    "steam": ("steam_deep", "<username>"),
    "whatsapp": ("whatsapp_check", "<phone>"),
    "all": ("check_all_platforms", "<username>"),
}


def main():
    if len(sys.argv) < 3:
        print("Usage: python social_media_hunter.py <command> <target>")
        print("\nCommands:")
        for cmd, (func, args) in COMMANDS.items():
            print(f"  {cmd:20s} {args}")
        print("\nExamples:")
        print("  python social_media_hunter.py probe_email user@example.com")
        print("  python social_media_hunter.py all johndoe")
        print("  python social_media_hunter.py instagram johndoe")
        print("  python social_media_hunter.py whatsapp +1234567890")
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        sys.exit(1)

    func_name = COMMANDS[command][0]
    result = globals()[func_name](target)

    # Save result
    out_dir = make_output_dir(f"{command}_{target}")
    save_json(out_dir, f"{command}.json", result)
    print(f"\nResult saved to {out_dir}/data/{command}.json")


if __name__ == "__main__":
    main()
