#!/usr/bin/env python3
"""Deterministic helpers for the chat-handoff skill (Python 3 standard library only).

  python handoff.py rename ZIP NEW_NAME          rename the export next to itself; refuses to overwrite
  python handoff.py add-to-zip ZIP FILE [FILE..] put files at the zip's root (replacing older copies), then test it
  python handoff.py check-links FILE [FILE..]    fetch every https link in the files; exit 1 if any fails

check-links treats 200 (after redirects) as OK. It retries once, waits between requests to stay polite with
GitHub, and prints each failure as "<status> <url>". Set HANDOFF_TIMEOUT (seconds, default 20) if needed.
"""
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile


def rename(zip_path, new_name):
    if os.sep in new_name or "/" in new_name:
        sys.exit("NEW_NAME is a file name, not a path")
    if not new_name.lower().endswith(".zip"):
        new_name += ".zip"
    target = os.path.join(os.path.dirname(os.path.abspath(zip_path)), new_name)
    if os.path.exists(target):
        sys.exit(f"{target} already exists: pick another name")
    os.rename(zip_path, target)
    print(f"{target} ({os.path.getsize(target)} bytes)")


def add_to_zip(zip_path, files):
    names = {os.path.basename(f) for f in files}
    tmp = zip_path + ".tmp"
    with zipfile.ZipFile(zip_path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info in src.infolist():
            if info.filename in names:
                continue  # replaced below
            out.writestr(info, src.read(info.filename))
        for f in files:
            out.write(f, os.path.basename(f))
    os.replace(tmp, zip_path)
    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        if bad:
            sys.exit(f"zip is corrupt at {bad}")
        present = [n for n in z.namelist() if n in names]
    print(f"{zip_path}: added {', '.join(sorted(present))} ({os.path.getsize(zip_path)} bytes)")


URL = re.compile(r"https://[^\s)\]>`'\"]+")


def status(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "chat-handoff-link-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # DNS, timeout, TLS
        return type(e).__name__


def check_links(files):
    timeout = float(os.environ.get("HANDOFF_TIMEOUT", "20"))
    urls = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for u in URL.findall(fh.read()):
                u = u.rstrip(".,;:")
                if u not in urls:
                    urls.append(u)
    broken = []
    for u in urls:
        s = status(u, timeout)
        if s != 200:
            time.sleep(2)
            s = status(u, timeout)
        if s != 200:
            broken.append((s, u))
            print(f"{s} {u}")
        time.sleep(0.2)
    print(f"checked {len(urls)} links, broken: {len(broken)}")
    sys.exit(1 if broken else 0)


def main(argv):
    if len(argv) >= 3 and argv[0] == "rename":
        rename(argv[1], argv[2])
    elif len(argv) >= 3 and argv[0] == "add-to-zip":
        add_to_zip(argv[1], argv[2:])
    elif len(argv) >= 2 and argv[0] == "check-links":
        check_links(argv[1:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
