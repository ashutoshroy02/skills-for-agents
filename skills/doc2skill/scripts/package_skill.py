#!/usr/bin/env python3
"""
Package a skill folder into <name>.zip for upload to Claude, after checking SKILL.md.

Adapted from moinulmoin/doc2skill package_skill.py (MIT, see ../LICENSE-doc2skill).
Added: frontmatter checks (name matches folder, name format, description length),
reference links that point at missing files, __pycache__ left out.

Usage:
    python package_skill.py doc2skill-output/react
"""

import os
import re
import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass


def check_skill(skill_path):
    """-> list of problems in SKILL.md (empty = fine)."""
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    problems = []
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["SKILL.md has no '---' frontmatter block at the top"]
    front = m.group(1)
    name = re.search(r"(?m)^name:\s*(.+)$", front)
    name = name.group(1).strip() if name else ""
    if not name:
        problems.append("frontmatter has no name")
    elif name != skill_path.name:
        problems.append(f"name '{name}' does not match the folder '{skill_path.name}'")
    elif not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        problems.append(f"name '{name}' must be lowercase letters, digits, hyphens, max 64 chars")
    desc = re.search(r"(?ms)^description:\s*(>-?|\|-?)?\s*\n?(.*?)(?=^\w[\w-]*:|\Z)", front)
    desc = " ".join(desc.group(2).split()) if desc else ""
    if not desc:
        problems.append("frontmatter has no description")
    elif len(desc) > 1024:
        problems.append(f"description is {len(desc)} chars (max 1024)")
    for ref in sorted(set(re.findall(r"references/[\w./-]+\.md", text))):
        if not (skill_path / ref).exists():
            problems.append(f"SKILL.md points at missing {ref}")
    return problems


def package_skill(skill_dir):
    skill_path = Path(skill_dir).resolve()
    if not (skill_path / "SKILL.md").is_file():
        print(f"❌ SKILL.md not found in {skill_dir}")
        return False
    problems = check_skill(skill_path)
    if problems:
        print("❌ Fix SKILL.md first:")
        for p in problems:
            print(f"   - {p}")
        return False

    zip_path = skill_path.parent / f"{skill_path.name}.zip"
    print(f"📦 Packaging skill: {skill_path.name}\n   Source: {skill_path}\n   Output: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # the zip holds the folder itself (<name>/SKILL.md), the layout Claude's upload expects
        for root, dirs, files in os.walk(skill_path):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                if file.endswith(".backup"):
                    continue
                path = Path(root) / file
                arcname = Path(skill_path.name) / path.relative_to(skill_path)
                zf.write(path, arcname)
                print(f"   + {arcname.as_posix()}")
    size = zip_path.stat().st_size
    print(f"\n✅ Package created: {zip_path}\n   Size: {size:,} bytes ({size / 1024:.1f} KB)")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill_directory>")
        sys.exit(1)
    sys.exit(0 if package_skill(sys.argv[1]) else 1)
