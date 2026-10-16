"""Look at media: probe, sheet (contact sheet), frames (stills). Images are for Claude to Read."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from vk_common import FFQ, die, measure_loudness, need, probe, run, say, ts, work_dir


def register(sub):
    p = sub.add_parser("probe", help="resolution, fps, rotation, HDR, audio, duration")
    p.add_argument("files", nargs="+")
    p.add_argument("--json", action="store_true")
    p.add_argument("--loudness", action="store_true", help="also measure integrated LUFS / true peak")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("sheet", help="contact sheet PNG with timestamps (Read it to see the video)")
    p.add_argument("file")
    p.add_argument("-n", type=int, default=12, help="number of frames (default 12)")
    p.add_argument("--from", dest="t0", type=float, default=None)
    p.add_argument("--to", dest="t1", type=float, default=None)
    p.add_argument("--cols", type=int, default=0)
    p.add_argument("-o", "--out")
    p.set_defaults(func=cmd_sheet)

    p = sub.add_parser("frames", help="full-size stills at given times")
    p.add_argument("file")
    p.add_argument("--at", required=True, nargs="+",
                   help="seconds, comma- or space-separated, e.g. 0.5,3,12.25 (PowerShell splits commas; both work)")
    p.add_argument("--width", type=int, default=720)
    p.set_defaults(func=cmd_frames)


def cmd_probe(a):
    for f in a.files:
        pr = probe(f)
        if a.loudness and pr["audio"]:
            pr["loudness"] = measure_loudness(f)
        if a.json:
            say(json.dumps(pr, indent=2))
            continue
        v, au = pr["video"], pr["audio"]
        say(f"{Path(f).name}: {pr['duration']:.2f}s, {pr['size_mb']} MB, {pr['bitrate_kbps']} kbps")
        if v:
            say(f"  video: {v['width']}x{v['height']} (display) {v['fps']} fps {v['codec']} {v['pix_fmt']}"
                + (f" rotation={v['rotation']}" if v["rotation"] else ""))
            if v["hdr"]:
                say(f"  HDR ({v['color_transfer']}): vk tone-maps to SDR bt709 automatically")
            if v["vfr_likely"]:
                say("  variable frame rate likely: vk outputs constant fps")
            if min(v["width"], v["height"]) < 720:
                say("  below 720p: keep zooms/punch-ins <= 1.06")
        else:
            say("  no video stream")
        if au:
            say(f"  audio: {au['codec']} {au['rate']} Hz {au['channels']}ch"
                + (f", starts {au['offset'] * 1000:.0f} ms after file start" if abs(au["offset"]) > 0.005 else ""))
        else:
            say("  no audio stream")
        if "loudness" in pr:
            L = pr["loudness"]
            say(f"  loudness: {L['lufs']} LUFS, true peak {L['true_peak']} dBFS, LRA {L['lra']} LU")


def _grab(src: Path, t: float, out: Path, width: int):
    run(FFQ + ["-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"scale={width}:-2", out], echo=False)


def cmd_sheet(a):
    need("PIL", "Pillow")
    from PIL import Image, ImageDraw, ImageFont

    src = Path(a.file).resolve()
    pr = probe(src)
    if not pr["video"]:
        die("no video stream")
    v = pr["video"]
    t0 = a.t0 or 0.0
    t1 = min(a.t1 or pr["duration"], pr["duration"])
    n = max(1, a.n)
    times = [t0 + (t1 - t0) * (i + 0.5) / n for i in range(n)]
    vertical = v["height"] > v["width"]
    cols = a.cols or (6 if vertical else 4)
    cell_w = 1600 // cols
    tmp = work_dir(src) / ".sheet-tmp"
    tmp.mkdir(exist_ok=True)
    tiles = []
    for i, t in enumerate(times):
        out = tmp / f"{i:03d}.png"
        _grab(src, t, out, cell_w)
        if out.exists():
            tiles.append((t, Image.open(out).convert("RGB")))
    if not tiles:
        die("could not extract frames")
    cw, ch = tiles[0][1].size
    rows = (len(tiles) + cols - 1) // cols
    label_h = 26
    sheet = Image.new("RGB", (cols * cw, rows * (ch + label_h)), (20, 20, 20))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (t, im) in enumerate(tiles):
        x, y = (i % cols) * cw, (i // cols) * (ch + label_h)
        sheet.paste(im, (x, y + label_h))
        draw.text((x + 6, y + 3), f"#{i + 1}  {ts(t)}", fill=(255, 220, 0), font=font)
    out = Path(a.out) if a.out else work_dir(src) / f"sheet-{src.stem}.png"
    sheet.save(out)
    for im in tiles:
        im[1].close()
    shutil.rmtree(tmp, ignore_errors=True)
    say(f"sheet: {out}  ({len(tiles)} frames, {ts(t0)}-{ts(t1)})")


def cmd_frames(a):
    src = Path(a.file).resolve()
    outdir = work_dir(src) / "frames"
    outdir.mkdir(exist_ok=True)
    for t in [float(x) for x in ",".join(a.at).split(",") if x.strip()]:
        out = outdir / f"{src.stem}-{t:07.2f}.png"
        _grab(src, t, out, a.width)
        say(f"frame {ts(t)}: {out}")
