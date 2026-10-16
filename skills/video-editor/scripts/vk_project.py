"""Workspace and per-video folders: new, ingest, status, clean, doctor."""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
import shutil
import sys
from pathlib import Path

from vk_common import (CONFIG_FILE, FFQ, IMAGE_EXT, MEDIA_EXT, STATE, SUBDIRS, TOOLS_HOME, VENV_PY,
                       dir_mb, die, free_gb, load_state, probe, read_json, rel, resolve_video, run,
                       save_state, say, slugify, unique_path, warn, workspace_root)

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "project.md"
KEEP_ON_CLEAN = {".json", ".txt", ".srt", ".ass", ".cmd", ".md", ".cube"}
LOW_DISK_GB = 5.0


def register(sub):
    p = sub.add_parser("new", help="create the video's subfolder (always the first step)")
    p.add_argument("title", help="short human title, e.g. 'gym tips short'")
    p.add_argument("--from", dest="files", nargs="*", default=[],
                   help="source files, folders or URLs to bring into source/")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--move", action="store_true", help="move sources instead of copying")
    g.add_argument("--copy", action="store_true", help="copy even from inbox/ (default there is move)")
    p.add_argument("--date", help="YYYY-MM-DD prefix (default: today)")
    p.add_argument("--brief", default="", help="one-line goal written into project.md")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("ingest", help="add more sources (files, folders, URLs) to a video")
    p.add_argument("video", help="video slug or path")
    p.add_argument("files", nargs="+")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--move", action="store_true")
    g.add_argument("--copy", action="store_true")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("status", help="list videos and free disk, or show one video")
    p.add_argument("video", nargs="?")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("clean", help="delete regenerable media in work/ (keeps json/txt/srt/ass)")
    p.add_argument("video", nargs="?")
    p.add_argument("--yes", action="store_true", help="actually delete (default: dry run)")
    p.set_defaults(func=cmd_clean)

    p = sub.add_parser("doctor", help="check ffmpeg, python packages, models, disk")
    p.set_defaults(func=cmd_doctor)


# ---------- ingest ----------

def _download(vd: Path, url: str) -> list[Path]:
    exe = shutil.which("yt-dlp")
    if not exe:
        die("yt-dlp is not installed: uv tool install yt-dlp")
    tmpl = str(vd / "source" / "%(title).60B [%(id)s].%(ext)s")
    say(f"downloading {url} …")
    r = run([exe, "--no-playlist", "--restrict-filenames", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
             "--merge-output-format", "mp4", "-o", tmpl, "--no-simulate", "--print", "after_move:filepath", url],
            capture=True, echo=False)
    paths = [Path(line.strip()) for line in r.stdout.splitlines() if line.strip()]
    return [p for p in paths if p.exists()]


def _describe(vd: Path, path: Path) -> dict:
    entry = {"file": rel(vd, path)}
    if path.suffix.lower() in IMAGE_EXT:
        return entry
    pr = probe(path)
    v, a = pr["video"], pr["audio"]
    entry.update({"duration": pr["duration"], "size_mb": pr["size_mb"]})
    if v:
        entry["video"] = f"{v['width']}x{v['height']} {v['fps']}fps {v['codec']}" + (" HDR" if v["hdr"] else "")
    if a:
        entry["audio"] = f"{a['codec']} {a['rate']}Hz {a['channels']}ch"
    return entry


def ingest(vd: Path, items: list[str], move=False, copy=False) -> list[dict]:
    ws = workspace_root(required=False)
    inbox = (ws / "inbox").resolve() if ws else None
    added: list[Path] = []
    for item in items:
        if re.match(r"https?://", item):
            added += _download(vd, item)
            continue
        src = Path(item).expanduser().resolve()
        if not src.exists():
            die(f"source not found: {item}")
        files = sorted(f for f in src.iterdir() if f.suffix.lower() in MEDIA_EXT) if src.is_dir() else [src]
        for f in files:
            dest = unique_path(vd / "source" / f.name)
            do_move = move or (inbox is not None and inbox in f.parents and not copy)
            if not do_move:
                need_gb = f.stat().st_size / 2**30 + 1.0
                if free_gb(vd) < need_gb:
                    die(f"only {free_gb(vd):.1f} GB free; copying {f.name} needs ~{need_gb:.1f} GB. Use --move.")
            (shutil.move if do_move else shutil.copy2)(str(f), str(dest))
            say(f"{'moved ' if do_move else 'copied'} {f.name} -> source/{dest.name}")
            added.append(dest)
    return [_describe(vd, p) for p in added]


def _print_sources(entries: list[dict]):
    for e in entries:
        bits = [e["file"]]
        if "duration" in e:
            bits.append(f"{e['duration']:.1f}s")
        bits += [e.get("video", ""), e.get("audio", "no audio" if "duration" in e else ""),
                 f"{e['size_mb']} MB" if "size_mb" in e else ""]
        say("  - " + " | ".join(b for b in bits if b))


def _write_project_md(vd: Path, state: dict, brief: str):
    md = vd / "project.md"
    if md.exists():
        return
    text = TEMPLATE.read_text(encoding="utf-8") if TEMPLATE.exists() else "# {{TITLE}}\n"
    sources = "\n".join(f"- `{s['file']}`" for s in state["sources"]) or "- (none yet)"
    for k, v in {"{{TITLE}}": state["title"], "{{SLUG}}": state["slug"], "{{DATE}}": state["created"][:10],
                 "{{BRIEF}}": brief or "(fill in: platform, length, audience, goal)", "{{SOURCES}}": sources}.items():
        text = text.replace(k, v)
    md.write_text(text, encoding="utf-8")


def cmd_new(a):
    ws = workspace_root()
    date = a.date or dt.date.today().isoformat()
    base = f"{date}-{slugify(a.title)}"
    vd = ws / "videos" / base
    n = 2
    while vd.exists():
        vd = ws / "videos" / f"{base}-{n}"
        n += 1
    for d in SUBDIRS:
        (vd / d).mkdir(parents=True, exist_ok=True)
    state = {"version": 1, "title": a.title, "slug": vd.name,
             "created": dt.datetime.now().isoformat(timespec="seconds"), "sources": [], "outputs": []}
    save_state(vd, state)
    if a.files:
        state["sources"] += ingest(vd, a.files, a.move, a.copy)
        save_state(vd, state)
    _write_project_md(vd, state, a.brief)
    say(f"\nVIDEO FOLDER: {vd}")
    say(f"slug: {vd.name}")
    _print_sources(state["sources"])
    gb = free_gb(vd)
    say(f"free disk: {gb:.1f} GB" + ("  <-- LOW: prefer --move, previews, `vk clean`" if gb < LOW_DISK_GB else ""))
    say("next: work inside this folder only (outputs -> work/ and exports/)")


def cmd_ingest(a):
    vd = resolve_video(a.video)
    state = load_state(vd)
    new = ingest(vd, a.files, a.move, a.copy)
    state.setdefault("sources", []).extend(new)
    save_state(vd, state)
    _print_sources(new)


# ---------- status / clean ----------

def cmd_status(a):
    if a.video:
        vd = resolve_video(a.video)
        st = load_state(vd)
        say(f"{vd.name}  ({st.get('title', '')})\n{vd}")
        say("sources:")
        _print_sources(st.get("sources", []))
        for sub in ("work", "exports"):
            files = sorted(p for p in (vd / sub).rglob("*") if p.is_file())
            say(f"{sub}/ ({dir_mb(vd / sub):.0f} MB):")
            for p in files:
                say(f"  - {rel(vd, p)}  {p.stat().st_size / 2**20:.1f} MB")
        for o in st.get("outputs", []):
            say(f"output: {o.get('file')}  {o.get('preset', '')}  {o.get('duration', '')}s  "
                f"{o.get('lufs', '')} LUFS  verify={o.get('verify', '?')}")
        return
    ws = workspace_root()
    vids = sorted(d for d in (ws / "videos").glob("*") if (d / STATE).exists())
    say(f"workspace: {ws}")
    say(f"free disk: {free_gb(ws):.1f} GB" + ("  <-- LOW" if free_gb(ws) < LOW_DISK_GB else ""))
    inbox = [p.name for p in (ws / "inbox").glob("*") if p.is_file() and not p.name.startswith(".")] if (ws / "inbox").exists() else []
    if inbox:
        say(f"inbox ({len(inbox)}): " + ", ".join(inbox[:10]))
    if not vids:
        say("no videos yet: vk new \"<title>\" --from <file>")
    for d in vids:
        st = load_state(d)
        n_exp = len([p for p in (d / "exports").glob("*") if p.is_file()])
        say(f"- {d.name:45s} src={len(st.get('sources', []))} exports={n_exp} "
            f"source={dir_mb(d / 'source'):.0f}MB work={dir_mb(d / 'work'):.0f}MB")


def cmd_clean(a):
    vd = resolve_video(a.video)
    victims = [p for p in (vd / "work").rglob("*") if p.is_file() and p.suffix.lower() not in KEEP_ON_CLEAN]
    total = sum(p.stat().st_size for p in victims) / 2**20
    if not victims:
        say("work/ has no regenerable media to delete")
        return
    for p in victims:
        say(f"  {'delete' if a.yes else 'would delete'} {rel(vd, p)}  {p.stat().st_size / 2**20:.1f} MB")
    if not a.yes:
        say(f"{total:.0f} MB reclaimable. Re-run with --yes to delete (sources and exports are never touched).")
        return
    for p in victims:
        p.unlink()
    for d in sorted((vd / "work").rglob("*"), reverse=True):
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()
    say(f"freed {total:.0f} MB; free disk now {free_gb(vd):.1f} GB")


# ---------- doctor ----------

def cmd_doctor(a):
    ok = True

    def row(name, good, detail="", fix=""):
        nonlocal ok
        ok = ok and (good or not fix.startswith("REQUIRED"))
        say(f"[{'ok' if good else '--'}] {name:22s} {detail}" + (f"\n      fix: {fix}" if not good and fix else ""))

    ff = shutil.which("ffmpeg")
    ver = run(["ffmpeg", "-version"], capture=True, echo=False).stdout.split("\n")[0] if ff else ""
    row("ffmpeg", bool(ff), ver[:60], "REQUIRED: winget install Gyan.FFmpeg")
    row("ffprobe", bool(shutil.which("ffprobe")), "", "REQUIRED: comes with ffmpeg")
    if ff:
        conf = run(["ffmpeg", "-hide_banner", "-buildconf"], capture=True, echo=False).stdout
        row("libass (captions)", "--enable-libass" in conf, "", "install a full ffmpeg build (Gyan.FFmpeg)")
        row("zimg (HDR->SDR)", "--enable-libzimg" in conf, "", "install a full ffmpeg build")
        qsv = run(FFQ + ["-f", "lavfi", "-i", "testsrc2=size=320x240:rate=30", "-t", "0.5",
                         "-c:v", "h264_qsv", "-f", "null", "-"], capture=True, echo=False, check=False)
        row("Intel QSV (--hw)", qsv.returncode == 0, "hardware H.264 encode", "optional; libx264 is used without --hw")
    row("python", sys.version_info >= (3, 10), f"{sys.version.split()[0]} at {sys.executable}")
    for mod, pip in (("faster_whisper", "faster-whisper"), ("cv2", "opencv-python-headless<5"),
                     ("numpy", "numpy"), ("PIL", "Pillow")):
        row(pip, importlib.util.find_spec(mod) is not None, "",
            f'uv pip install --python "{VENV_PY}" "{pip}"')
    hub = Path.home() / ".cache" / "huggingface" / "hub"
    models = sorted(p.name.split("faster-whisper-")[-1] for p in hub.glob("models--*faster-whisper-*")) if hub.exists() else []
    row("whisper models", bool(models), ", ".join(models) or "none cached (first `vk transcribe` downloads ~460 MB for 'small')")
    yunet = TOOLS_HOME / "models" / "face_detection_yunet_2023mar.onnx"
    row("YuNet face model", yunet.exists(), str(yunet) if yunet.exists() else "", "face reframe falls back to Haar")
    row("yt-dlp", bool(shutil.which("yt-dlp")), "", "uv tool install yt-dlp")
    row("node / npx (Remotion)", bool(shutil.which("node") and shutil.which("npx")), "", "winget install OpenJS.NodeJS.LTS")
    ws = workspace_root(required=False)
    row("workspace", ws is not None, str(ws or ""), f"create {CONFIG_FILE} with {{\"workspace\": \"<path>\"}}")
    if ws:
        gb = free_gb(ws)
        row("free disk", gb >= LOW_DISK_GB, f"{gb:.1f} GB", "clear space: `vk clean <video> --yes`, empty Recycle Bin")
    cfg = read_json(CONFIG_FILE, None)
    if cfg is None:
        warn(f"{CONFIG_FILE} missing (workspace is found via .vk-workspace marker only)")
    return 0 if ok else 1
