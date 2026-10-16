"""Final render in one encode (reframe, LUT, logo, captions, music, two-pass loudness) + verification."""
from __future__ import annotations

import datetime as dt
import json
import re
from fractions import Fraction
from pathlib import Path

from vk_common import (FF, die, fpath, load_state, measure_loudness, probe, rel, require_video_dir, run, save_state,
                       say, std_fps, tonemap_chain, ts, unique_path, warn, workspace_root)

PRESETS = {
    "shorts":  dict(w=1080, h=1920, crf=18, abr="192k", lufs=-14.0, max_dur=180, x264="medium"),
    "reels":   dict(w=1080, h=1920, crf=18, abr="192k", lufs=-14.0, max_dur=180, x264="medium"),
    "tiktok":  dict(w=1080, h=1920, crf=18, abr="192k", lufs=-14.0, max_dur=600, x264="medium"),
    "youtube": dict(w=1920, h=1080, crf=18, abr="192k", lufs=-14.0, max_dur=None, x264="medium"),
    "square":  dict(w=1080, h=1080, crf=18, abr="192k", lufs=-14.0, max_dur=None, x264="medium"),
    "preview": dict(w=540, h=960, crf=28, abr="128k", lufs=-14.0, max_dur=None, x264="veryfast", fps="30"),
    "source":  dict(w=None, h=None, crf=18, abr="192k", lufs=-14.0, max_dur=None, x264="medium"),
}


def register(sub):
    p = sub.add_parser("render", help="final render: reframe+LUT+logo+captions+music+loudness, one encode, verified")
    p.add_argument("input")
    p.add_argument("-o", "--out", help="default exports/<slug>-<preset>.mp4 (never overwrites: -v2, -v3)")
    p.add_argument("--preset", choices=sorted(PRESETS), default="shorts")
    p.add_argument("--size", help="override WxH (e.g. 960x540 for a wide preview)")
    p.add_argument("--fps", help="output fps (default: source, snapped, max 60)")
    p.add_argument("--reframe", choices=["auto", "none", "center", "blur", "face"], default="auto",
                   help="auto: face-track if faces in >=30%% of frames, else blurred-background fit")
    p.add_argument("--ass", help="captions .ass from `vk captions` (use the same WxH as the preset)")
    p.add_argument("--lut", help=".cube colour LUT")
    p.add_argument("--lut-mix", type=float, default=1.0, help="LUT strength 0-1")
    p.add_argument("--logo", help="PNG with transparency")
    p.add_argument("--logo-pos", choices=["tl", "tr", "bl", "br"], default="tr")
    p.add_argument("--logo-scale", type=float, default=0.16, help="logo width as fraction of frame width")
    p.add_argument("--music", help="background track (loops if short)")
    p.add_argument("--music-db", type=float, default=-20.0, help="music gain before ducking (dB)")
    p.add_argument("--duck", action="store_true", help="dip music under speech (sidechain)")
    p.add_argument("--lufs", type=float, help="loudness target (default preset, -14)")
    p.add_argument("--no-norm", action="store_true", help="skip loudness normalisation")
    p.add_argument("--denoise", action="store_true", help="FFT noise reduction (only for audible hiss/hum)")
    p.add_argument("--no-highpass", action="store_true")
    p.add_argument("--hw", action="store_true", help="Intel Quick Sync encode: faster, slightly bigger")
    p.add_argument("--crf", type=int)
    p.add_argument("--from", dest="t0", type=float, help="render only from this input time")
    p.add_argument("--to", dest="t1", type=float)
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("verify", help="check a file against a platform preset (size, fps, codec, LUFS, peak, faststart)")
    p.add_argument("file")
    p.add_argument("--preset", choices=sorted(PRESETS), default=None)
    p.set_defaults(func=cmd_verify)


def _even(x: float) -> int:
    return int(round(x)) // 2 * 2


def _loudnorm_measure(cmd_inputs: list, agraph: str, target: float, tp: float) -> dict | None:
    g = agraph + f",loudnorm=I={target}:TP={tp}:LRA=11:print_format=json[aout]"
    r = run(["ffmpeg", "-hide_banner", "-nostdin", "-y"] + cmd_inputs + ["-filter_complex", g, "-map", "[aout]",
                                                                         "-f", "null", "-"], capture=True, echo=False)
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr or "", re.S)
    if not m:
        warn("loudness measurement failed; rendering without normalisation")
        return None
    data = json.loads(m[-1])
    if data["input_i"] in ("-inf", "inf"):
        warn("audio is silent; skipping normalisation")
        return None
    return data


def cmd_render(a):
    src = Path(a.input).resolve()
    vd = require_video_dir(src)
    pr = probe(src)
    v = pr["video"] or die("input has no video stream")
    P = PRESETS[a.preset]
    if a.size:
        W, H = (int(x) for x in a.size.lower().split("x"))
    elif P["w"]:
        W, H = P["w"], P["h"]
    else:
        W, H = v["width"], v["height"]
    W, H = _even(W), _even(H)
    fps_str, fps = std_fps(float(Fraction(a.fps or P.get("fps") or str(v["fps"]))))
    crf = a.crf if a.crf is not None else P["crf"]
    t0 = a.t0 or 0.0
    dur = (min(a.t1, pr["duration"]) if a.t1 else pr["duration"]) - t0
    if dur <= 0:
        die("empty time window")
    out = Path(a.out).resolve() if a.out else unique_path(vd / "exports" / f"{vd.name}-{a.preset}.mp4")
    if a.out and out.exists():
        out = unique_path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # inputs (identical for the measuring pass, so stream indices match)
    inputs = (["-ss", f"{t0:.3f}"] if t0 else []) + ["-t", f"{dur:.3f}", "-i", str(src)]
    idx = 1
    logo_i = music_i = None
    if a.logo:
        inputs += ["-i", str(Path(a.logo).resolve())]
        logo_i, idx = idx, idx + 1
    if a.music:
        inputs += ["-stream_loop", "-1", "-i", str(Path(a.music).resolve())]
        music_i, idx = idx, idx + 1

    # ----- video -----
    iw, ih = v["width"], v["height"]
    ta = W / H
    mode, track = a.reframe, None
    if a.preset == "source" and mode == "auto":
        mode = "none"
    if mode in ("auto", "face"):
        if abs(iw / ih - ta) < 0.02:
            mode = "none"
        elif iw / ih > ta:
            from vk_reframe import track_faces
            track = track_faces(src, pr, ta)
            if mode == "auto":
                mode = "face" if track and track["coverage"] >= 0.3 else "blur"
                say(f"reframe auto -> {mode} (faces in {track['coverage'] * 100:.0f}% of samples)")
        else:
            mode = "blur" if mode == "auto" else "center"
    pre = tonemap_chain(v)
    if (v.get("pix_fmt") or "").startswith("yuvj"):
        # full-range input (e.g. Remotion's JPEG frames): convert to standard TV range, don't just relabel it
        pre.append("scale=in_range=pc:out_range=tv")
    graph = []
    if mode == "blur":
        graph.append("[0:v]" + ",".join(pre + ["split=2[bg0][fg0]"]))
        graph.append(f"[bg0]scale={W // 4}:{H // 4}:force_original_aspect_ratio=increase,crop={W // 4}:{H // 4},"
                     f"gblur=sigma=10,eq=brightness=-0.06,scale={W}:{H}[bg1]")
        graph.append(f"[fg0]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos[fg1]")
        graph.append(f"[bg1][fg1]overlay=(W-w)/2:(H-h)/2,setsar=1,fps={fps_str}[base]")
    else:
        chain = list(pre)
        if mode == "face" and track:
            from vk_reframe import write_sendcmd
            cmdfile = vd / "work" / f"{src.stem}.reframe.cmd"
            x0 = write_sendcmd(track, cmdfile, t0)
            chain += [f"sendcmd=f={fpath(cmdfile, vd)}", f"crop@rf=w={track['cw']}:h={track['ch']}:x={x0}:y=0"]
        elif mode in ("center", "face"):
            if iw / ih > ta:
                cw = _even(ih * ta)
                chain.append(f"crop={cw}:{ih}:{(iw - cw) // 2}:0")
            else:
                chh = _even(iw / ta)
                chain.append(f"crop={iw}:{chh}:0:{(ih - chh) // 2}")
        if mode == "none":
            chain += [f"scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos",
                      f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2"]
        else:
            chain.append(f"scale={W}:{H}:flags=lanczos")
        chain += ["setsar=1", f"fps={fps_str}"]
        graph.append("[0:v]" + ",".join(chain) + "[base]")
    cur = "[base]"
    if a.lut:
        lut = fpath(a.lut, vd)
        if a.lut_mix >= 0.999:
            graph.append(f"{cur}lut3d=file={lut}[graded]")
        else:
            graph += [f"{cur}split=2[la][lb]", f"[lb]lut3d=file={lut}[lc]",
                      f"[lc][la]blend=all_mode=normal:all_opacity={a.lut_mix:.3f}[graded]"]
        cur = "[graded]"
    if logo_i is not None:
        lw = _even(W * a.logo_scale)
        m = round(W * 0.05)
        top = round(H * 0.12) if H > W else m
        bottom = f"{round(H * 0.70)}-h" if H > W else f"H-h-{m}"
        pos = {"tl": (f"{m}", f"{top}"), "tr": (f"W-w-{m}", f"{top}"),
               "bl": (f"{m}", bottom), "br": (f"W-w-{m}", bottom)}[a.logo_pos]
        graph += [f"[{logo_i}:v]scale={lw}:-1,format=rgba[lg]", f"{cur}[lg]overlay={pos[0]}:{pos[1]}[withlogo]"]
        cur = "[withlogo]"
    final = []
    if a.ass:
        ass = f"ass=filename={fpath(a.ass, vd)}"
        ws = workspace_root(required=False)
        fonts = ws / "library" / "fonts" if ws else None
        if fonts and fonts.exists() and any(p.suffix.lower() in (".ttf", ".otf", ".ttc") for p in fonts.iterdir()):
            ass += f":fontsdir={fpath(fonts, vd)}"
        final.append(ass)
    final.append("format=nv12" if a.hw else "format=yuv420p")
    graph.append(f"{cur}{','.join(final)}[vout]")

    # ----- audio -----
    has_voice = pr["audio"] is not None
    agraph = None
    if has_voice or music_i is not None:
        parts = []
        if has_voice:
            vchain = ["aresample=48000"] + ([] if a.no_highpass else ["highpass=f=80"]) \
                + (["afftdn=nf=-25"] if a.denoise else [])
            parts.append("[0:a]" + ",".join(vchain) + "[voice]")
        if music_i is not None:
            parts.append(f"[{music_i}:a]aresample=48000,volume={a.music_db}dB,atrim=0:{dur:.3f},"
                         f"afade=t=in:d=0.5,afade=t=out:st={max(dur - 2, 0):.3f}:d=2[mus]")
            if has_voice and a.duck:
                parts += ["[voice]asplit=2[v1][sc]",
                          "[mus][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md]",
                          "[v1][md]amix=inputs=2:duration=first:normalize=0"]
            elif has_voice:
                parts.append("[voice][mus]amix=inputs=2:duration=first:normalize=0")
            else:
                parts.append("[mus]anull")
        else:
            parts.append("[voice]anull")
        agraph = ";".join(parts)
        target = a.lufs if a.lufs is not None else P["lufs"]
        tp = -1.0
        tail = ""
        if not a.no_norm:
            say(f"measuring loudness (target {target} LUFS) ...")
            ms = _loudnorm_measure(inputs, agraph, target, tp)
            if ms:
                lra = min(max(11.0, float(ms["input_lra"]) + 0.5), 20.0)
                tail = (f",loudnorm=I={target}:TP={tp}:LRA={lra}:measured_I={ms['input_i']}:"
                        f"measured_TP={ms['input_tp']}:measured_LRA={ms['input_lra']}:"
                        f"measured_thresh={ms['input_thresh']}:offset={ms['target_offset']}:linear=true,"
                        f"aresample=48000")
                say(f"  input {ms['input_i']} LUFS, peak {ms['input_tp']} dBTP")
        graph.append(agraph + tail + "[aout]")

    if a.hw:
        venc = ["-c:v", "h264_qsv", "-preset", "medium", "-global_quality", str(crf + 3)]
    else:
        venc = ["-c:v", "libx264", "-preset", P["x264"], "-crf", str(crf), "-profile:v", "high"]
    cmd = FF + inputs + ["-filter_complex", ";".join(graph), "-map", "[vout]"] \
        + (["-map", "[aout]", "-c:a", "aac", "-b:a", P["abr"], "-ar", "48000", "-ac", "2"] if agraph else ["-an"]) \
        + venc + ["-r", fps_str, "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                  "-color_range", "tv", "-t", f"{dur:.3f}", "-movflags", "+faststart", str(out)]
    say(f"rendering {ts(dur)} -> {W}x{H} @ {fps_str} ({a.preset}, reframe={mode}, {'qsv' if a.hw else 'x264'})")
    run(cmd, cwd=vd)
    ok, rep = verify(out, a.preset, None if a.no_norm else (a.lufs if a.lufs is not None else P["lufs"]))
    st = load_state(vd)
    st.setdefault("outputs", []).append({
        "file": rel(vd, out), "preset": a.preset, "from": rel(vd, src), "reframe": mode,
        "captions": bool(a.ass), "duration": rep.get("duration"), "lufs": rep.get("lufs"),
        "verify": "pass" if ok else "fail", "created": dt.datetime.now().isoformat(timespec="seconds")})
    save_state(vd, st)
    return 0 if ok else 1


def _moov_first(path: Path) -> bool:
    with open(path, "rb") as f:
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                return False
            size, typ = int.from_bytes(hdr[:4], "big"), hdr[4:8]
            if typ == b"moov":
                return True
            if typ == b"mdat":
                return False
            if size == 1:
                size = int.from_bytes(f.read(8), "big")
                f.seek(size - 16, 1)
            elif size < 8:
                return False
            else:
                f.seek(size - 8, 1)


def verify(path: Path, preset: str | None, lufs_target: float | None) -> tuple[bool, dict]:
    pr = probe(path)
    v, au = pr["video"], pr["audio"]
    P = PRESETS.get(preset) if preset else None
    rows, ok = [], True

    def chk(name, good, detail, level="FAIL"):
        nonlocal ok
        if not good and level == "FAIL":
            ok = False
        rows.append(f"[{'ok' if good else level.lower()}] {name:12s} {detail}")

    rep = {"duration": pr["duration"], "size_mb": pr["size_mb"]}
    if not v:
        chk("video", False, "no video stream")
    else:
        if P and P["w"]:
            chk("size", (v["width"], v["height"]) == (P["w"], P["h"]), f"{v['width']}x{v['height']}")
        else:
            chk("size", True, f"{v['width']}x{v['height']}")
        chk("codec", v["codec"] == "h264" and v["pix_fmt"] == "yuv420p", f"{v['codec']} {v['pix_fmt']}", "WARN")
        chk("fps", v["fps"] <= 60.5 and not v["vfr_likely"], f"{v['fps']}", "WARN")
    if au:
        chk("audio", au["codec"] == "aac" and au["rate"] == 48000, f"{au['codec']} {au['rate']} Hz", "WARN")
        if v:
            gap = abs(v["duration"] - au["duration"])
            chk("a/v length", gap <= 0.1, f"video {v['duration']:.2f}s, audio {au['duration']:.2f}s", "WARN")
        L = measure_loudness(path)
        rep.update({"lufs": L["lufs"], "true_peak": L["true_peak"]})
        if lufs_target is not None and L["lufs"] is not None:
            chk("loudness", abs(L["lufs"] - lufs_target) <= 1.0, f"{L['lufs']} LUFS (target {lufs_target})", "WARN")
        else:
            chk("loudness", True, f"{L['lufs']} LUFS")
        if L["true_peak"] is not None:
            chk("true peak", L["true_peak"] <= -0.5, f"{L['true_peak']} dBFS", "WARN")
    else:
        chk("audio", False, "no audio stream", "WARN")
    if P and P.get("max_dur"):
        chk("duration", pr["duration"] <= P["max_dur"], f"{pr['duration']:.1f}s (platform max {P['max_dur']}s)", "WARN")
    else:
        chk("duration", True, f"{pr['duration']:.1f}s")
    chk("faststart", _moov_first(Path(path)), "moov atom first (streams before full download)", "WARN")
    say(f"\nverify {Path(path).name}  ({pr['size_mb']} MB)")
    for r in rows:
        say("  " + r)
    say("  RESULT: " + ("PASS" if ok else "FAIL"))
    return ok, rep


def cmd_verify(a):
    P = PRESETS.get(a.preset) if a.preset else None
    ok, _ = verify(Path(a.file).resolve(), a.preset, P["lufs"] if P else None)
    return 0 if ok else 1
