#!/usr/bin/env python3
"""
doc2skill scraper: documentation -> Claude skill folder (references/ + draft SKILL.md).

Adapted from moinulmoin/doc2skill (MIT, see ../LICENSE-doc2skill), itself based on
Skill Seekers by Yusuf Karaaslan. Changes from the original doc_scraper.py:
non-interactive, --out folder, robots.txt respected, URL #fragments dropped,
crawl follows navigation links too, main-content selector fallbacks, list items
kept, --markdown-dir source (docs folder of a repo), UTF-8 console on Windows.
The API / new-terminal enhancement steps are gone: Claude writes SKILL.md itself.

Usage:
    python doc_scraper.py --config ../configs/react.json --out ./doc2skill-output
    python doc_scraper.py --name mylib --url https://docs.mylib.dev/ --max-pages 20
    python doc_scraper.py --name mylib --markdown-dir ./mylib/docs
    python doc_scraper.py --config ../configs/react.json --skip-scrape   # rebuild from cache
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict, deque
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.robotparser import RobotFileParser

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001 - older Pythons / redirected streams
    pass

USER_AGENT = "Mozilla/5.0 (compatible; Doc2Skill-Scraper/1.0; +https://github.com/moinulmoin/doc2skill)"
# tried in order when the configured main_content selector finds nothing
FALLBACK_MAIN = ["article", "main", "div[role='main']", "div.content", "div.document", "body"]
MD_CODE_RE = re.compile(r"```([\w+-]*)[^\n]*\n(.*?)```", re.S)


def skill_name(name):
    """Claude skill names: lowercase letters, digits and hyphens, at most 64 chars."""
    return re.sub(r"[^a-z0-9-]+", "-", (name or "").lower()).strip("-")[:64]


class DocToSkillConverter:
    def __init__(self, config, out_dir="output"):
        self.config = config
        self.name = config["name"]
        self.base_url = config.get("base_url", "")
        self.data_dir = os.path.join(out_dir, f"{self.name}_data")
        self.skill_dir = os.path.join(out_dir, self.name)
        self.visited_urls = set()
        self.pending_urls = deque(urldefrag(u)[0] for u in config.get("start_urls", [self.base_url]) if u)
        self.pages = []
        self.robots = None
        self.session = None
        os.makedirs(os.path.join(self.data_dir, "pages"), exist_ok=True)
        for sub in ("references", "scripts", "assets"):
            os.makedirs(os.path.join(self.skill_dir, sub), exist_ok=True)

    # ── crawling ──────────────────────────────────────────────────────────────
    def is_valid_url(self, url):
        """Inside base_url, matches an include pattern (if any), no exclude pattern."""
        if not url.startswith(self.base_url):
            return False
        includes = self.config.get("url_patterns", {}).get("include", [])
        if includes and not any(pattern in url for pattern in includes):
            return False
        excludes = self.config.get("url_patterns", {}).get("exclude", [])
        return not any(pattern in url for pattern in excludes)

    def _load_robots(self):
        parts = urlparse(self.base_url)
        robots = RobotFileParser()
        robots.set_url(f"{parts.scheme}://{parts.netloc}/robots.txt")
        try:
            robots.read()
        except Exception:  # noqa: BLE001 - no robots.txt reachable: nothing to obey
            return None
        return robots

    def extract_content(self, soup, url):
        page = {"url": url, "title": "", "content": "", "headings": [],
                "code_samples": [], "patterns": [], "links": []}
        selectors = self.config.get("selectors", {})

        title_elem = soup.select_one(selectors.get("title", "title")) or soup.select_one("title")
        if title_elem:
            page["title"] = self.clean_text(title_elem.get_text())

        # links from the whole page (sidebar navigation lists every doc page)
        for link in soup.find_all("a", href=True):
            href = urldefrag(urljoin(url, link["href"]))[0]
            if self.is_valid_url(href) and href not in page["links"]:
                page["links"].append(href)

        main = None
        for selector in [selectors.get("main_content", "div[role='main']"), *FALLBACK_MAIN]:
            main = soup.select_one(selector)
            if main:
                break
        if not main:
            print(f"  ⚠ No content: {url}")
            return page

        for h in main.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            text = self.clean_text(h.get_text())
            if text:
                page["headings"].append({"level": h.name, "text": text, "id": h.get("id", "")})

        for code_elem in main.select(selectors.get("code_blocks", "pre code")):
            code = code_elem.get_text()
            if len(code.strip()) > 10:
                page["code_samples"].append({"code": code.strip(), "language": self.detect_language(code_elem, code)})

        page["patterns"] = self.extract_patterns(main)

        # paragraphs and list items in page order; a <li> wrapping a <p> is read once
        blocks = []
        for elem in main.find_all(["p", "li"]):
            if elem.name == "li" and elem.find("p"):
                continue
            text = self.clean_text(elem.get_text())
            if len(text) > 20:
                blocks.append(f"- {text}" if elem.name == "li" else text)
        page["content"] = "\n\n".join(blocks)
        return page

    def detect_language(self, elem, code):
        for node in (elem, elem.parent):
            for cls in (node.get("class", []) if node is not None else []):
                if cls.startswith(("language-", "lang-")):
                    return cls.split("-", 1)[1]
        if "import " in code and "from " in code:
            return "python"
        if "const " in code or "let " in code or "=>" in code:
            return "javascript"
        if "func " in code and "var " in code:
            return "gdscript"
        if "def " in code and ":" in code:
            return "python"
        if "#include" in code or "int main" in code:
            return "cpp"
        return "unknown"

    def extract_patterns(self, main):
        """'Example:' / 'Usage:' text followed by code -> quick-reference candidates."""
        patterns = []
        for elem in main.find_all(["p", "div"]):
            text = elem.get_text().lower()
            if any(word in text for word in ["example:", "pattern:", "usage:", "typical use"]):
                next_code = elem.find_next(["pre", "code"])
                if next_code:
                    patterns.append({"description": self.clean_text(elem.get_text())[:200],
                                     "code": next_code.get_text().strip()})
        return patterns[:5]

    @staticmethod
    def clean_text(text):
        return re.sub(r"\s+", " ", text or "").strip()

    def save_page(self, page):
        url_hash = hashlib.md5(page["url"].encode()).hexdigest()[:10]
        safe_title = re.sub(r"[-\s]+", "_", re.sub(r"[^\w\s-]", "", page["title"])[:50])
        path = os.path.join(self.data_dir, "pages", f"{safe_title}_{url_hash}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(page, f, indent=2, ensure_ascii=False)

    def scrape_page(self, url, max_retries=3):
        import requests
        from bs4 import BeautifulSoup

        for attempt in range(max_retries):
            try:
                print(f"  {url}" if attempt == 0 else f"  Retry {attempt + 1}: {url}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                if "html" not in response.headers.get("Content-Type", "html"):
                    return
                page = self.extract_content(BeautifulSoup(response.content, "html.parser"), url)
                self.save_page(page)
                self.pages.append(page)
                for link in page["links"]:
                    if link not in self.visited_urls and link not in self.pending_urls:
                        self.pending_urls.append(link)
                time.sleep(self.config.get("rate_limit", 1.0))
                return
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    print(f"  ✗ Failed after {max_retries} attempts: {e}")
                    return
                wait = (2 ** attempt) + 1
                print(f"  ⚠ Attempt {attempt + 1} failed: {e}, retrying in {wait}s...")
                time.sleep(wait)
            except Exception as e:  # noqa: BLE001 - one bad page never stops the crawl
                print(f"  ✗ Unexpected error: {e}")
                return

    def scrape_all(self):
        import requests

        print(f"\n{'=' * 60}\nSCRAPING: {self.name}\n{'=' * 60}")
        print(f"Base URL: {self.base_url}\nOutput: {self.data_dir}\n")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        self.robots = self._load_robots()
        max_pages = self.config.get("max_pages", 500)
        blocked = 0
        while self.pending_urls and len(self.visited_urls) < max_pages:
            url = self.pending_urls.popleft()
            if url in self.visited_urls:
                continue
            self.visited_urls.add(url)
            if self.robots is not None and not self.robots.can_fetch(USER_AGENT, url):
                blocked += 1
                print(f"  ⊘ robots.txt disallows: {url}")
                continue
            self.scrape_page(url)
            if len(self.visited_urls) % 10 == 0:
                print(f"  [{len(self.visited_urls)} pages]")
        print(f"\n✅ Scraped {len(self.pages)} pages ({blocked} blocked by robots.txt, "
              f"{len(self.pending_urls)} left unvisited at max_pages={max_pages})")
        self.save_summary()

    # ── markdown source (a repo's docs folder) ────────────────────────────────
    def load_markdown_dir(self, folder):
        root = Path(folder)
        print(f"\n{'=' * 60}\nREADING MARKDOWN: {root}\n{'=' * 60}")
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() not in (".md", ".mdx") or any(
                    part in ("node_modules", ".git") for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)      # front matter
            rel = path.relative_to(root).as_posix()
            code = [{"code": m.group(2).strip(), "language": m.group(1) or "unknown"}
                    for m in MD_CODE_RE.finditer(text) if len(m.group(2).strip()) > 10]
            prose = MD_CODE_RE.sub("", text)
            headings = [{"level": f"h{len(m.group(1))}", "text": m.group(2).strip(), "id": ""}
                        for m in re.finditer(r"(?m)^(#{1,6})\s+(.+)$", prose)]
            blocks = [self.clean_text(b) for b in re.split(r"\n\s*\n", prose)]
            page = {
                "url": rel,
                # a page whose top heading is not '# ' (mkdocs takes it from the nav)
                # is named after its file, not after a sub-section
                "title": (headings[0]["text"] if headings and headings[0]["level"] == "h1"
                          else path.stem.replace("_", " ").replace("-", " ").title()),
                "content": "\n\n".join(b for b in blocks if len(b) > 20 and not b.startswith("#")),
                "headings": headings,
                "code_samples": code,
                "patterns": [],
                "links": [],
                "markdown": text.strip(),      # references keep code where the docs put it
            }
            self.save_page(page)
            self.pages.append(page)
            print(f"  {rel}")
        print(f"\n✅ Read {len(self.pages)} markdown files")
        self.save_summary()

    def save_summary(self):
        summary = {"name": self.name, "total_pages": len(self.pages), "base_url": self.base_url,
                   "pages": [{"title": p["title"], "url": p["url"]} for p in self.pages]}
        with open(os.path.join(self.data_dir, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

    def load_scraped_data(self):
        pages = []
        for json_file in sorted((Path(self.data_dir) / "pages").glob("*.json")):
            try:
                pages.append(json.loads(json_file.read_text(encoding="utf-8")))
            except Exception as e:  # noqa: BLE001
                print(f"⚠ Error loading {json_file}: {e}")
        return pages

    # ── building the skill ────────────────────────────────────────────────────
    def smart_categorize(self, pages):
        """Each page goes to the first category whose keywords score >= 2
        (keyword in URL +3, in title +2, in the first 500 chars +1), else 'other'."""
        category_defs = self.config.get("categories") or self.infer_categories(pages)
        categories = {cat: [] for cat in category_defs}
        categories["other"] = []
        for page in pages:
            url, title = page["url"].lower(), page["title"].lower()
            content = page.get("content", "").lower()[:500]
            for cat, keywords in category_defs.items():
                score = sum(3 * (k.lower() in url) + 2 * (k.lower() in title) + (k.lower() in content)
                            for k in keywords)
                if score >= 2:
                    categories[cat].append(page)
                    break
            else:
                categories["other"].append(page)
        return {k: v for k, v in categories.items() if v}

    def infer_categories(self, pages):
        """No categories in the config: the URL path segments shared by >= 3 pages."""
        counts = defaultdict(int)
        for page in pages:
            for seg in urlparse(page["url"]).path.split("/"):
                seg = re.sub(r"\.(html?|mdx?)$", "", seg)
                if seg and seg not in ("en", "stable", "latest", "docs", "index"):
                    counts[seg] += 1
        categories = {seg: [seg] for seg, n in sorted(counts.items(), key=lambda x: -x[1])[:8] if n >= 3}
        urls = [p["url"] for p in pages]
        if "tutorial" not in categories and any("tutorial" in u for u in urls):
            categories["tutorials"] = ["tutorial", "guide", "getting-started"]
        if "api" not in categories and any("api" in u or "reference" in u for u in urls):
            categories["api"] = ["api", "reference", "class"]
        return categories

    def generate_quick_reference(self, pages):
        quick_ref, seen = [], set()
        for pattern in (p for page in pages for p in page.get("patterns", [])):
            if pattern["code"] not in seen and len(pattern["code"]) < 300:
                quick_ref.append(pattern)
                seen.add(pattern["code"])
                if len(quick_ref) >= 15:
                    break
        return quick_ref

    @staticmethod
    def demote_headings(markdown):
        """'# X' -> '### X' outside code fences (a '# comment' inside code stays)."""
        out, fence = [], False
        for line in markdown.splitlines():
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
            elif not fence and re.match(r"#{1,6}\s", line):
                hashes = len(line) - len(line.lstrip("#"))
                line = "#" * min(6, hashes + 2) + line[hashes:]
            out.append(line)
        return "\n".join(out)

    @staticmethod
    def file_slug(category):
        return re.sub(r"[^\w-]+", "_", category).strip("_") or "other"

    def create_reference_file(self, category, pages):
        page_chars = self.config.get("ref_page_chars", 2500)
        code_chars = self.config.get("ref_code_chars", 600)
        lines = [f"# {self.name.title()} - {category.replace('_', ' ').title()}\n",
                 f"**Pages:** {len(pages)}\n", "---\n"]
        for page in sorted(pages, key=lambda p: p["url"]):
            lines += [f"## {page['title']}\n", f"**URL:** {page['url']}\n"]
            if page.get("markdown"):
                # markdown source: the page as written, its headings moved under '## title'
                body = self.demote_headings(page["markdown"])
                if len(body) > page_chars:
                    body = body[:page_chars] + "\n\n*[Content truncated]*"
                lines += [body, "", "---\n"]
                continue
            if page.get("headings"):
                lines.append("**Contents:**")
                for h in page["headings"][:10]:
                    lines.append(f"{'  ' * max(0, int(h['level'][1]) - 2)}- {h['text']}")
                lines.append("")
            if page.get("content"):
                content = page["content"][:page_chars]
                if len(page["content"]) > page_chars:
                    content += "\n\n*[Content truncated]*"
                lines += [content, ""]
            if page.get("code_samples"):
                lines.append("**Examples:**\n")
                for i, sample in enumerate(page["code_samples"][:4], 1):
                    lang, code = sample.get("language", "unknown"), sample.get("code", "")
                    lines += [f"Example {i} ({lang}):", f"```{lang}", code[:code_chars]]
                    if len(code) > code_chars:
                        lines.append("...")
                    lines.append("```\n")
            lines.append("---\n")
        path = os.path.join(self.skill_dir, "references", f"{self.file_slug(category)}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  ✓ {self.file_slug(category)}.md ({len(pages)} pages)")

    def create_draft_skill_md(self, categories, quick_ref):
        """Generic draft. Claude replaces it with the real SKILL.md (doc2skill step 4)."""
        description = self.config.get("description") or f"Comprehensive assistance with {self.name}"
        examples = []
        for pages in categories.values():
            for page in pages[:3]:
                for sample in page.get("code_samples", [])[:2]:
                    if len(sample.get("code", "")) < 200 and sample.get("language") != "unknown":
                        examples.append((sample["language"], sample["code"]))
        out = [f"---\nname: {self.name}\ndescription: {description}\n---\n",
               f"# {self.name.title()} Skill\n",
               f"Comprehensive assistance with {self.name}, generated from its documentation.\n",
               "## When to Use This Skill\n",
               f"- Working with {self.name}, its features or APIs",
               f"- Implementing or debugging {self.name} code\n",
               "## Quick Reference\n"]
        for i, pattern in enumerate(quick_ref[:8], 1):
            out += [f"**Pattern {i}:** {pattern.get('description', '')}\n", "```", pattern["code"][:300], "```\n"]
        for i, (lang, code) in enumerate(examples[:5], 1):
            out += [f"**Example {i}** ({lang}):", f"```{lang}", code, "```\n"]
        out.append("## Reference Files\n")
        out += [f"- `references/{self.file_slug(cat)}.md` - {cat.replace('_', ' ').title()} ({len(p)} pages)"
                for cat, p in sorted(categories.items())]
        with open(os.path.join(self.skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")
        print(f"  ✓ SKILL.md (draft, {min(len(examples), 5)} examples)")

    def create_index(self, categories):
        lines = [f"# {self.name.title()} Documentation Index\n", "## Categories\n"]
        for cat, pages in sorted(categories.items()):
            lines += [f"### {cat.replace('_', ' ').title()}", f"**File:** `{self.file_slug(cat)}.md`",
                      f"**Pages:** {len(pages)}"]
            lines += [f"- {p['title']}" for p in sorted(pages, key=lambda p: p["url"])[:40]]
            lines.append("")
        with open(os.path.join(self.skill_dir, "references", "index.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("  ✓ index.md")

    def build_skill(self):
        print(f"\n{'=' * 60}\nBUILDING SKILL: {self.name}\n{'=' * 60}\n")
        pages = self.load_scraped_data()
        if not pages:
            print("✗ No scraped data found!")
            return False
        print(f"  ✓ Loaded {len(pages)} pages")
        categories = self.smart_categorize(pages)
        print(f"  ✓ {len(categories)} categories: "
              + ", ".join(f"{c} ({len(p)})" for c, p in categories.items()))
        refs = Path(self.skill_dir) / "references"
        for old in refs.glob("*.md"):        # no stale category files from an earlier build
            old.unlink()
        for cat, cat_pages in categories.items():
            self.create_reference_file(cat, cat_pages)
        self.create_index(categories)
        self.create_draft_skill_md(categories, self.generate_quick_reference(pages))
        print(f"\n✅ Skill built: {self.skill_dir}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Convert documentation into a Claude skill folder")
    parser.add_argument("--config", "-c", help="config JSON (see ../configs/)")
    parser.add_argument("--name", help="skill name (lowercase-hyphen)")
    parser.add_argument("--url", help="base documentation URL (HTML crawl)")
    parser.add_argument("--markdown-dir", help="folder of .md/.mdx docs instead of a crawl")
    parser.add_argument("--description", "-d", help="skill description")
    parser.add_argument("--out", default="output", help="output folder (default: ./output)")
    parser.add_argument("--max-pages", type=int, help="override max_pages (use 20 for a test run)")
    parser.add_argument("--skip-scrape", action="store_true", help="rebuild from cached pages")
    args = parser.parse_args()

    if args.config:
        with open(args.config, encoding="utf-8") as f:
            config = json.load(f)
    elif args.name and (args.url or args.markdown_dir):
        config = {
            "name": args.name,
            "base_url": args.url or "",
            "selectors": {"main_content": "div[role='main']", "title": "title", "code_blocks": "pre code"},
            "url_patterns": {"include": [], "exclude": []},
            "rate_limit": 1.0,
            "max_pages": 500,
        }
    else:
        parser.error("give --config, or --name with --url or --markdown-dir")
    if args.description:
        config["description"] = args.description
    if args.max_pages:
        config["max_pages"] = args.max_pages
    config["name"] = skill_name(config["name"])
    if config.get("base_url") and not config["base_url"].endswith("/"):
        config["base_url"] += "/"

    converter = DocToSkillConverter(config, args.out)
    if args.skip_scrape:
        print(f"\n⏭  Skipping scrape, using cached pages in {converter.data_dir}")
    else:
        shutil.rmtree(os.path.join(converter.data_dir, "pages"), ignore_errors=True)
        os.makedirs(os.path.join(converter.data_dir, "pages"))
        try:
            if args.markdown_dir:
                converter.load_markdown_dir(args.markdown_dir)
            else:
                converter.scrape_all()
        except KeyboardInterrupt:
            print("\nScraping interrupted: building from the pages read so far.")
            converter.save_summary()
    if not converter.build_skill():
        sys.exit(1)
    print("\nNext: Claude rewrites SKILL.md from references/ (doc2skill step 4), then:")
    print(f"  python package_skill.py {converter.skill_dir}")


if __name__ == "__main__":
    main()
