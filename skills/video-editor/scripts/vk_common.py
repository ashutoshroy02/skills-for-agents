"""Shared helpers for vk, the video-editor toolkit (ffmpeg + faster-whisper + OpenCV)."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path

TOOLS_HOME = Path(os.environ.get("VK_HOME") or Path.home() / ".video-tools")
CONFIG_FILE = TOOLS_HOME / "config.json"
VENV_PY = TOOLS_HOME / "venv" / "Scripts" / "python.exe"
MARKER = ".vk-workspace"
STATE = "vk.json"
SUBDIRS = ("source", "work", "assets", "exports")
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mts", ".m2ts", ".3gp"}
AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".opus"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MEDIA_EXT = VIDEO_EXT | AUDIO_EXT | IMAGE_EXT

# Quiet ffmpeg for many small jobs; FF adds a live progress line for long ones.
FFQ = ["ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error"]
FF = FFQ + ["-stats"]


class VkError(Exception):
    pass


def die(msg: str):
    raise VkError(msg)


_stdout_ok = True


def say(msg: str = ""):
    """Print, but never let a closed pipe (`| head`, `Select-Object -First`) abort a half-done job."""
    global _stdout_ok
    if not _stdout_ok:
        return
    try:
        print(msg, flush=True)
    except (BrokenPipeError, OSError, ValueError):
        _stdout_ok = False


def warn(msg: str):
    say(f"WARN: {msg}")


def utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def need(module: str, pip_name: str):
    """Import a heavy optional module or fail with the exact install command."""
    try:
        return __import__(module)
    except ImportError:
        die(f"Python package '{pip_name}' is missing. Install it with:\n"
            f'  uv pip install --python "{VENV_PY}" {pip_name}')


# ---------- json / paths ----------

def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def rel(base: Path, path: Path) -> str:
    """Path relative to base in posix form; absolute if it lives elsewhere."""
    try:
        return Path(os.path.relpath(Path(path).resolve(), Path(base).resolve())).as_posix()
    except ValueError:
        return str(Path(path).resolve())


def slugify(text: str, maxlen: int = 40) -> str:
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:maxlen].rstrip("-") or "video"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    n = 2
    while True:
        cand = path.with_name(f"{path.stem}-{n}{path.suffix}")
        if not cand.exists():
            return cand
        n += 1


def free_gb(path) -> float:
    return shutil.disk_usage(Path(path).anchor or path).free / 2**30


def dir_mb(path: Path) -> float:
    if not path.exists():
        return 0.0
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / 2**20


def ts(t: float) -> str:
    m, s = divmod(max(t, 0.0), 60)
    return f"{int(m):02d}:{s:05.2f}"


def parse_time(text: str) -> float:
    """'83.5', '1:23.5' or '0:01:23.5' -> seconds."""
    parts = [float(p) for p in str(text).strip().split(":")]
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


# ---------- workspace / video folders ----------

def workspace_root(required: bool = True) -> Path | None:
    env = os.environ.get("VK_WORKSPACE")
    if env and Path(env).exists():
        return Path(env).resolve()
    cwd = Path.cwd().resolve()
    for d in (cwd, *cwd.parents):
        if (d / MARKER).exists():
            return d
    cfg = read_json(CONFIG_FILE, {}) or {}
    if cfg.get("workspace") and Path(cfg["workspace"]).exists():
        return Path(cfg["workspace"]).resolve()
    if required:
        die(f"No video workspace found (no {MARKER} above {cwd}, no 'workspace' in {CONFIG_FILE}).")
    return None


def find_video_dir(start) -> Path | None:
    p = Path(start).resolve()
    if p.is_file() or not p.exists():
        p = p.parent
    for d in (p, *p.parents):
        if (d / STATE).exists():
            return d
    return None


def resolve_video(arg: str | None) -> Path:
    """A video folder from a path, a slug (or unique part of one), or the cwd."""
    if arg:
        p = Path(arg)
        if p.exists():
            vd = find_video_dir(p)
            if vd:
                return vd
        videos = workspace_root() / "videos"
        exact = videos / arg
        if (exact / STATE).exists():
            return exact
        matches = [d for d in sorted(videos.glob(f"*{arg}*")) if (d / STATE).exists()]
        if len(matches) == 1:
            return matches[0]
        if matches:
            die(f"'{arg}' matches several videos: " + ", ".join(m.name for m in matches))
        die(f"no video folder matches '{arg}' (see `vk status`)")
    vd = find_video_dir(Path.cwd())
    if not vd:
        die("not inside a video folder; pass the video slug or path (see `vk status`)")
    return vd


def require_video_dir(path) -> Path:
    vd = find_video_dir(path)
    if not vd:
        die(f"{path} is not inside a video folder. Create one first: vk new \"<title>\" --from {path}")
    return vd


def load_state(vd: Path) -> dict:
    return read_json(vd / STATE, {}) or {}


def save_state(vd: Path, state: dict):
    write_json(vd / STATE, state)


def work_dir(path) -> Path:
    """work/ of the video folder that holds path (outputs never land next to sources)."""
    vd = require_video_dir(path)
    w = vd / "work"
    w.mkdir(exist_ok=True)
    return w


# ---------- process / ffmpeg ----------

def run(cmd, cwd=None, capture=False, echo=True, check=True):
    cmd = [str(c) for c in cmd]
    if echo:
        say("$ " + subprocess.list2cmdline(cmd))
    r = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        detail = ""
        if capture:
            detail = "\n" + "\n".join((r.stderr or "").strip().splitlines()[-15:])
        die(f"{Path(cmd[0]).name} exited with code {r.returncode}{detail}")
    return r


def _f(v, default=0.0) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _rate(text) -> float:
    try:
        r = float(Fraction(str(text)))
        return r if 0 < r < 1000 else 0.0
    except (ValueError, ZeroDivisionError):
        return 0.0


def probe(path) -> dict:
    """Display size (after rotation), fps, HDR, audio offset relative to the file start."""
    path = Path(path)
    if not path.exists():
        die(f"not found: {path}")
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
            capture=True, echo=False)
    data = json.loads(r.stdout or "{}")
    streams, fmt = data.get("streams", []), data.get("format", {})
    v = next((s for s in streams if s.get("codec_type") == "video"
              and not (s.get("disposition") or {}).get("attached_pic")), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    fstart = _f(fmt.get("start_time"))
    out = {
        "path": str(path),
        "size_mb": round(path.stat().st_size / 2**20, 1),
        "duration": round(_f(fmt.get("duration")), 3),
        "format": fmt.get("format_name"),
        "bitrate_kbps": int(_f(fmt.get("bit_rate")) / 1000),
        "video": None,
        "audio": None,
    }
    if v:
        rot = 0
        for sd in v.get("side_data_list") or []:
            if "rotation" in sd:
                rot = int(round(_f(sd["rotation"])))
        if not rot and (v.get("tags") or {}).get("rotate"):
            rot = int(_f(v["tags"]["rotate"]))
        w, h = int(v.get("width", 0)), int(v.get("height", 0))
        if abs(rot) % 180 == 90:
            w, h = h, w
        avg, real = _rate(v.get("avg_frame_rate")), _rate(v.get("r_frame_rate"))
        fps = avg or real or 30.0
        trc = v.get("color_transfer") or ""
        out["video"] = {
            "codec": v.get("codec_name"), "width": w, "height": h, "rotation": rot,
            "fps": round(fps, 3), "vfr_likely": bool(avg and real and abs(avg - real) > 0.5),
            "pix_fmt": v.get("pix_fmt"), "color_transfer": trc,
            "hdr": trc in ("arib-std-b67", "smpte2084"),
            "duration": round(_f(v.get("duration"), out["duration"]), 3),
        }
    if a:
        out["audio"] = {
            "codec": a.get("codec_name"), "rate": int(_f(a.get("sample_rate"))),
            "channels": a.get("channels"),
            "offset": round(_f(a.get("start_time"), fstart) - fstart, 4),
            "duration": round(_f(a.get("duration"), out["duration"]), 3),
        }
    return out


STD_RATES = [("24000/1001", 23.976), ("24", 24.0), ("25", 25.0), ("30000/1001", 29.97),
             ("30", 30.0), ("50", 50.0), ("60000/1001", 59.94), ("60", 60.0)]


def std_fps(fps: float) -> tuple[str, float]:
    """Snap a measured rate to a standard one; high-frame-rate sources cap at 60."""
    fps = min(fps or 30.0, 60.0)
    best = min(STD_RATES, key=lambda r: abs(r[1] - fps))
    return best[0], float(Fraction(best[0]))


def tonemap_chain(vinfo: dict | None) -> list[str]:
    """HDR (HLG/PQ phone footage) -> SDR bt709; without it HDR looks washed out."""
    if not vinfo or not vinfo.get("hdr"):
        return []
    return ["zscale=t=linear:npl=100", "format=gbrpf32le", "zscale=p=bt709",
            "tonemap=tonemap=hable:desat=0", "zscale=t=bt709:m=bt709:r=tv", "format=yuv420p"]


def fpath(path, cwd) -> str:
    """A file path usable inside a filtergraph option (relative to cwd, both escape levels)."""
    path, cwd = Path(path).resolve(), Path(cwd).resolve()
    try:
        r = os.path.relpath(path, cwd)
    except ValueError:  # different drive: bring the file next to the job
        local = cwd / "_ext" / path.name
        local.parent.mkdir(exist_ok=True)
        shutil.copy2(path, local)
        r = os.path.relpath(local, cwd)
    r = r.replace("\\", "/")
    lvl1 = re.sub(r"([\\':])", r"\\\1", r)
    return re.sub(r"([\\'\[\],;])", r"\\\1", lvl1)


def audio16k(src: Path, outdir: Path, pr: dict | None = None) -> Path:
    """Mono 16 kHz WAV on the file's timeline (audio start offset restored). Cached."""
    src = Path(src).resolve()
    out = Path(outdir) / f"{src.stem}.16k.wav"
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return out
    pr = pr or probe(src)
    if not pr["audio"]:
        die(f"{src.name} has no audio stream")
    off = pr["audio"]["offset"]
    af = [f"adelay={int(round(off * 1000))}:all=1"] if off > 0.005 else []
    run(FFQ + ["-i", src, "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000"]
        + (["-af", ",".join(af)] if af else []) + ["-c:a", "pcm_s16le", out], echo=False)
    return out


def measure_loudness(path) -> dict:
    r = run(["ffmpeg", "-hide_banner", "-nostdin", "-i", path, "-map", "0:a:0",
             "-af", "ebur128=peak=true:framelog=verbose", "-f", "null", "-"],
            capture=True, echo=False, check=False)
    txt = r.stderr or ""

    def last(pattern):
        m = re.findall(pattern, txt)
        if not m:
            return None
        return float("-inf") if m[-1] == "-inf" else float(m[-1])

    return {"lufs": last(r"I:\s+(-?[\d.]+|-inf) LUFS"),
            "true_peak": last(r"Peak:\s+(-?[\d.]+|-inf) dBFS"),
            "lra": last(r"LRA:\s+(-?[\d.]+) LU")}
