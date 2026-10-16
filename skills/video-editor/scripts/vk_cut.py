"""Edits as data: speech detection by audio, EDLs from transcript picks, frame-accurate cutting.

EDL (work/*.edl.json), paths relative to the video folder:
  {"sources": {"A": "source/clip.mov"},
   "ranges": [{"src": "A", "start": 12.30, "end": 18.90, "note": "hook", "zoom": 1.15, "speed": 1.1}]}
`zoom` and `speed` per range are optional (cut --punch / --speed set them globally).
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
from pathlib import Path

from vk_common import (FF, FFQ, audio16k, die, need, parse_time, probe, read_json, rel, require_video_dir,
                       run, say, std_fps, tonemap_chain, ts, warn, work_dir, write_json)

WIN = 0.01  # envelope window, s


def register(sub):
    p = sub.add_parser("silence", help="speech-by-audio EDL: shorten pauses in a file or in an EDL's ranges")
    p.add_argument("input", help="media file, or an EDL to tighten")
    p.add_argument("--pause", type=float, default=0.30, help="pauses longer than this get shortened (s)")
    p.add_argument("--keep", type=float, default=0.12, help="pause length left at each cut (s)")
    p.add_argument("--thresh", type=float, help="speech threshold dBFS (default: auto from the recording)")
    p.add_argument("--min-speech", type=float, default=0.11, help="ignore sounds shorter than this (s)")
    p.add_argument("-o", "--out")
    p.set_defaults(func=cmd_silence)

    p = sub.add_parser("edl", help="EDL from transcript picks; edges snapped to words and audio silence")
    p.add_argument("transcript")
    p.add_argument("--keep", required=True, help='"12.3-25.1, 1:02-1:15.5" (source seconds or m:ss)')
    p.add_argument("--no-snap", action="store_true")
    p.add_argument("-o", "--out")
    p.set_defaults(func=cmd_edl)

    p = sub.add_parser("cut", help="render an EDL -> work/<name>.mp4 + <name>.map.json")
    p.add_argument("edl")
    p.add_argument("-o", "--out")
    p.add_argument("--speed", type=float, default=1.0, help="global speed-up with pitch kept (1.1-1.2 for slow talkers)")
    p.add_argument("--punch", type=float, default=0.0, help="alternate segments zoom in by this factor (e.g. 1.12) to hide jump cuts")
    p.add_argument("--crf", type=int, default=16, help="intermediate quality (lower = better/bigger)")
    p.add_argument("--fade", type=float, default=0.02, help="audio fade at every cut (s)")
    p.set_defaults(func=cmd_cut)


# ---------- audio analysis ----------

def envelope(wav: Path):
    np = need("numpy", "numpy")
    import wave
    with wave.open(str(wav), "rb") as w:
        sr, n = w.getframerate(), w.getnframes()
        data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    hop = int(sr * WIN)
    m = len(data) // hop
    frames = data[: m * hop].reshape(m, hop)
    return 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)


def speech_mask(db, thresh=None, hold=0.03):
    """Rolling max over +-hold keeps 30-60 ms dips inside words from reading as pauses."""
    np = need("numpy", "numpy")
    from numpy.lib.stride_tricks import sliding_window_view
    k = max(1, int(round(hold / WIN)))
    sdb = sliding_window_view(np.pad(db, k, mode="edge"), 2 * k + 1).max(axis=1)
    if thresh is None:
        voiced = db[db > -60]
        p95 = float(np.percentile(voiced, 95)) if voiced.size else -20.0
        thresh = max(min(-30.0, p95 - 20.0), -50.0)
    return sdb >= thresh, thresh


def spans(mask, min_len=0.11) -> list[tuple[float, float]]:
    np = need("numpy", "numpy")
    edges = np.diff(np.concatenate(([0], mask.astype(np.int8), [0])))
    starts, ends = np.where(edges == 1)[0], np.where(edges == -1)[0]
    return [(s * WIN, e * WIN) for s, e in zip(starts, ends) if (e - s) * WIN >= min_len]


def tighten(sp: list[tuple[float, float]], lo: float, hi: float, pause: float, keep: float):
    """Speech spans inside [lo, hi] -> keep ranges with long pauses shortened to `keep`."""
    inner = [(max(s - 0.03, lo), min(e + 0.05, hi)) for s, e in sp if e > lo and s < hi]
    out: list[list[float]] = []
    for s, e in inner:
        if out and s - out[-1][1] <= pause:
            out[-1][1] = max(out[-1][1], e)
        elif out:
            gap_mid = (out[-1][1] + s) / 2
            out[-1][1] = min(out[-1][1] + keep / 2, gap_mid)
            out.append([max(s - keep / 2, gap_mid), e])
        else:
            out.append([s, e])
    return [(s, e) for s, e in out if e - s > 0.05]


def _snap(ranges, fps):
    return [(math.floor(s * fps) / fps, math.ceil(e * fps) / fps) for s, e in ranges]


def _src_context(src: Path):
    vd = require_video_dir(src)
    pr = probe(src)
    wav = audio16k(src, vd / "work", pr)
    db = envelope(wav)
    return vd, pr, db


# ---------- silence ----------

def cmd_silence(a):
    inp = Path(a.input).resolve()
    vd = require_video_dir(inp)
    if inp.suffix.lower() == ".json":
        edl = read_json(inp)
        sources = {k: (vd / v).resolve() for k, v in edl["sources"].items()}
        jobs = [(r["src"], r["start"], r["end"], r) for r in edl["ranges"]]
        out = Path(a.out) if a.out else inp.with_name(re.sub(r"(\.edl)?\.json$", "", inp.name) + "-tight.json")
    else:
        sources = {"A": inp}
        jobs = [("A", 0.0, None, {})]
        edl = {"sources": {"A": rel(vd, inp)}, "ranges": []}
        out = Path(a.out) if a.out else vd / "work" / "edl.json"
    ctx = {}
    new_ranges, before, after = [], 0.0, 0.0
    for key, lo, hi, extra in jobs:
        if key not in ctx:
            _, pr, db = _src_context(sources[key])
            mask, th = speech_mask(db, a.thresh)
            ctx[key] = (pr, spans(mask, a.min_speech), th)
            say(f"{sources[key].name}: speech threshold {th:.1f} dBFS")
        pr, sp, _ = ctx[key]
        hi = pr["duration"] if hi is None else hi
        fps = std_fps(pr["video"]["fps"] if pr["video"] else 30)[1]
        kept = _snap(tighten(sp, lo, hi, a.pause, a.keep), fps)
        before += hi - lo
        for s, e in kept:
            r = {k: v for k, v in extra.items() if k not in ("start", "end")}
            r.update({"src": key, "start": round(s, 3), "end": round(e, 3)})
            new_ranges.append(r)
            after += e - s
    if not new_ranges:
        die("no speech found; lower --thresh (e.g. -45) or check the audio")
    edl["ranges"] = new_ranges
    write_json(out, edl)
    say(f"EDL: {out}\n{len(new_ranges)} ranges, {before:.1f}s -> {after:.1f}s "
        f"(-{before - after:.1f}s, {100 * (before - after) / max(before, 1e-6):.0f}% removed)")


# ---------- edl from transcript ----------

def _parse_keep(text: str):
    out = []
    for part in re.split(r"[,;]\s*", text.strip()):
        if part:
            s, e = re.split(r"\s*-\s*(?=\d)", part, maxsplit=1)
            out.append((parse_time(s), parse_time(e)))
    return out


def _refine(mask, t: float, edge: str) -> float | None:
    """Move an edge onto the nearest speech onset/offset by audio; None if no silence nearby."""
    i = int(round(t / WIN))
    if edge == "start":
        lo, hi = max(0, i - 50), min(len(mask) - 1, i + 50)  # whisper word times drift 0.1-0.5 s
        on = [j for j in range(lo + 1, hi + 1) if mask[j] and not mask[j - 1]]
        return None if not on else min(on, key=lambda j: abs(j - i)) * WIN - 0.03
    lo, hi = max(0, i - 50), min(len(mask) - 1, i + 50)
    off = [j for j in range(lo, hi) if mask[j] and not mask[j + 1]]
    return None if not off else (min(off, key=lambda j: abs(j - i)) + 1) * WIN + 0.05


def cmd_edl(a):
    from vk_transcribe import load_transcript
    tpath = Path(a.transcript).resolve()
    data, words, src = load_transcript(tpath)
    vd, pr, db = _src_context(src)
    mask, _ = speech_mask(db)
    fps = std_fps(pr["video"]["fps"] if pr["video"] else 30)[1]
    ranges = []
    for s, e in _parse_keep(a.keep):
        if e <= s:
            die(f"bad range {s}-{e}")
        inside = [w for w in words if w["e"] > s + 0.02 and w["s"] < e - 0.02]
        if not a.no_snap and inside:
            s, e = inside[0]["s"], inside[-1]["e"]
            rs, re_ = _refine(mask, s, "start"), _refine(mask, e, "end")
            if rs is None:
                warn(f"start {s:.2f}: no silence nearby (edge inside continuous speech); kept word time")
            if re_ is None:
                warn(f"end {e:.2f}: no silence nearby; kept word time")
            s, e = (rs if rs is not None else s - 0.03), (re_ if re_ is not None else e + 0.05)
        s, e = _snap([(max(0.0, s), min(pr["duration"], e))], fps)[0]
        first = inside[0]["w"] if inside else "?"
        last = inside[-1]["w"] if inside else "?"
        say(f"{s:8.2f} -> {e:8.2f} ({e - s:5.1f}s)  \"{first} ... {last}\"")
        ranges.append({"src": "A", "start": round(s, 3), "end": round(e, 3)})
    out = Path(a.out) if a.out else vd / "work" / "edl.json"
    write_json(out, {"sources": {"A": rel(vd, src)}, "ranges": ranges})
    say(f"EDL: {out}  total {sum(r['end'] - r['start'] for r in ranges):.1f}s")


# ---------- cut ----------

def _atempo(speed: float) -> list[str]:
    chain, s = [], speed
    while s > 2.0:
        chain.append("atempo=2.0")
        s /= 2.0
    while s < 0.5:
        chain.append("atempo=0.5")
        s /= 0.5
    return chain + [f"atempo={s:.5f}"]


def cmd_cut(a):
    edl_path = Path(a.edl).resolve()
    vd = require_video_dir(edl_path)
    edl = read_json(edl_path)
    if not edl or not edl.get("ranges"):
        die("EDL has no ranges")
    sources = {k: (vd / v).resolve() for k, v in edl["sources"].items()}
    probes = {k: probe(p) for k, p in sources.items()}
    first = probes[edl["ranges"][0]["src"]]
    if not first["video"]:
        die("first range's source has no video")
    W, H = edl.get("size") or (first["video"]["width"], first["video"]["height"])
    W, H = W // 2 * 2, H // 2 * 2
    fps_str, fps = std_fps(edl.get("fps") or first["video"]["fps"])
    out = Path(a.out).resolve() if a.out else vd / "work" / "cut.mp4"
    tmp = out.parent / f".{out.stem}-segs"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)

    segments, t_out = [], 0.0
    n = len(edl["ranges"])
    say(f"cutting {n} segments -> {W}x{H} @ {fps_str} fps")
    for i, r in enumerate(edl["ranges"]):
        key = r["src"]
        src, pr = sources[key], probes[key]
        sp = float(r.get("speed", a.speed))
        dur = r["end"] - r["start"]
        nframes = max(1, round(dur / sp * fps))
        out_d = nframes / fps
        zoom = r.get("zoom") or (a.punch if a.punch and i % 2 == 1 else 0)
        vf = tonemap_chain(pr["video"]) + [
            f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos",
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2", "setsar=1"]
        if zoom and zoom > 1:
            # punch-in centred a little above the middle, where faces usually are
            vf += [f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})/2:(ih-ih/{zoom})*0.4",
                   f"scale={W}:{H}:flags=lanczos"]
        if sp != 1:
            vf.append(f"setpts=PTS/{sp}")
        vf += [f"fps={fps_str}", "tpad=stop_mode=clone:stop_duration=1"]
        vseg, aseg = tmp / f"v{i:04d}.mp4", tmp / f"a{i:04d}.wav"
        run(FFQ + ["-ss", f"{r['start']:.4f}", "-i", src, "-map", "0:v:0", "-vf", ",".join(vf),
                   "-frames:v", nframes, "-c:v", "libx264", "-preset", "veryfast", "-crf", a.crf,
                   "-pix_fmt", "yuv420p", "-r", fps_str, "-video_track_timescale", "90000", "-an", vseg], echo=False)
        samples = round(out_d * 48000)
        fade = min(a.fade, out_d / 4)
        if pr["audio"]:
            af = ["aresample=48000"] + (_atempo(sp) if sp != 1 else []) + [
                "apad", f"atrim=end_sample={samples}",
                f"afade=t=in:d={fade:.4f}", f"afade=t=out:st={out_d - fade:.4f}:d={fade:.4f}"]
            run(FFQ + ["-ss", f"{r['start']:.4f}", "-t", f"{dur + 0.2:.4f}", "-i", src, "-map", "0:a:0",
                       "-af", ",".join(af), "-ac", "2", "-c:a", "pcm_s16le", aseg], echo=False)
        else:
            run(FFQ + ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-af", f"atrim=end_sample={samples}",
                       "-c:a", "pcm_s16le", aseg], echo=False)
        segments.append({"src": key, "path": rel(vd, src), "start": r["start"], "end": r["end"], "speed": sp,
                         "zoom": zoom or 1, "out_start": round(t_out, 4), "out_end": round(t_out + out_d, 4),
                         "note": r.get("note", "")})
        t_out += out_d
        say(f"  [{i + 1}/{n}] {ts(r['start'])}-{ts(r['end'])} -> {ts(segments[-1]['out_start'])}"
            + (f" zoom {zoom}" if zoom else ""))

    for kind, ext in (("v", "mp4"), ("a", "wav")):
        (tmp / f"{kind}.txt").write_text("".join(f"file '{kind}{i:04d}.{ext}'\n" for i in range(n)), encoding="utf-8")
    run(FFQ + ["-f", "concat", "-safe", "0", "-i", "v.txt", "-c", "copy", "video.mp4"], cwd=tmp, echo=False)
    run(FFQ + ["-f", "concat", "-safe", "0", "-i", "a.txt", "-c", "copy", "audio.wav"], cwd=tmp, echo=False)
    run(FF + ["-i", tmp / "video.mp4", "-i", tmp / "audio.wav", "-map", "0:v:0", "-map", "1:a:0",
              "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", out])
    shutil.rmtree(tmp, ignore_errors=True)

    mp = {"output": rel(vd, out), "fps": fps_str, "size": [W, H], "duration": round(t_out, 4), "segments": segments}
    map_path = out.with_suffix(".map.json")
    write_json(map_path, mp)
    res = probe(out)
    vdur, adur = res["video"]["duration"], (res["audio"] or {}).get("duration", 0)
    say(f"\ncut: {out}  {t_out:.2f}s ({res['size_mb']} MB), map: {map_path}")
    if abs(vdur - adur) > 1.5 / fps:
        warn(f"video {vdur:.3f}s vs audio {adur:.3f}s differ by more than a frame")
    _check_repeats(vd, segments, sources)


def _check_repeats(vd: Path, segments: list[dict], sources: dict):
    """An identical 3-word run on both sides of a cut usually means a leftover retake."""
    from vk_captions import remap_words
    from vk_transcribe import load_transcript, transcript_path
    words = []
    for key, src in sources.items():
        t = transcript_path(src)
        if t.exists():
            _, w, s = load_transcript(t)
            words += remap_words(w, s, segments, vd)
    if not words:
        say("tip: transcribe the source first and cut will also check for repeated phrases at cuts")
        return
    words.sort(key=lambda w: w["s"])
    norm = lambda x: re.sub(r"[^\w]", "", x.lower())
    found, last, hidden = 0, -1e9, 0
    for sg in segments[1:]:
        b = sg["out_start"]
        if b - last < 8:  # later cuts inside an already-flagged repeated passage
            hidden += 1
            continue
        before = [norm(w["w"]) for w in words if b - 12 < w["s"] < b][-20:]
        after = [norm(w["w"]) for w in words if b <= w["s"] < b + 6][:6]
        grams = {tuple(before[i:i + 3]) for i in range(len(before) - 2)}
        rep = [tuple(after[i:i + 3]) for i in range(len(after) - 2) if tuple(after[i:i + 3]) in grams]
        if rep:
            found, last = found + 1, b
            warn(f"possible repeated take at {ts(b)}: '{' '.join(rep[0])}' appears on both sides of the cut")
    if not found:
        say("repeat check: no duplicated phrases at cuts")
    elif hidden:
        say(f"  (cuts within 8 s after a flagged one were not re-checked)")
