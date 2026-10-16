"""Styled word-by-word captions (.ass for burn-in, .srt for upload) from a transcript.

Transcript times are on the source timeline; with a cut map they are remapped onto the cut,
so the cut never needs a second transcription.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from vk_common import die, find_video_dir, read_json, say, warn, write_json

# px values at a 1080-px short side; scaled for other sizes
STYLES = {
    "bold":    dict(font="Arial Black", size=88, bold=0, upper=True, outline=7, shadow=0, box=False,
                    hl="FFD60A", words=3, line_chars=14, pop=True),
    "clean":   dict(font="Segoe UI", size=76, bold=-1, upper=False, outline=0, shadow=3, box=False,
                    hl="4DE3FF", words=4, line_chars=20, pop=False),
    "box":     dict(font="Segoe UI", size=70, bold=-1, upper=False, outline=14, shadow=0, box=True,
                    hl="FFD60A", words=4, line_chars=20, pop=False),
    "minimal": dict(font="Segoe UI", size=60, bold=0, upper=False, outline=0, shadow=3, box=False,
                    hl=None, words=7, line_chars=28, pop=False),
}
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


def register(sub):
    p = sub.add_parser("captions", help="word-highlight captions -> work/captions.ass (+ .srt)")
    p.add_argument("transcript")
    p.add_argument("--map", help="cut map (default: work/cut.map.json when the transcript's source is in it)")
    p.add_argument("--no-map", action="store_true", help="keep source timeline")
    p.add_argument("--style", choices=sorted(STYLES), default="bold")
    p.add_argument("--words", type=int, help="max words per caption")
    p.add_argument("--y", type=float, help="vertical centre as fraction of height (default 0.70 vertical, 0.82 wide)")
    p.add_argument("--font")
    p.add_argument("--size", type=int, help="font px at a 1080-px short side")
    p.add_argument("--color", default="FFFFFF", help="text colour RRGGBB")
    p.add_argument("--hl", help="highlight colour RRGGBB for the spoken word ('none' to disable)")
    p.add_argument("--upper", action=argparse.BooleanOptionalAction, default=None)
    p.add_argument("--fix", help='word fixes: "jeeny=Jinny;cloud=Claude"')
    p.add_argument("--res", default="1080x1920", help="final video size WxH (match the render preset)")
    p.add_argument("-o", "--out")
    p.set_defaults(func=cmd_captions)


def remap_words(words: list[dict], src: Path, segments: list[dict], vd: Path) -> list[dict]:
    """Source-timeline words -> cut timeline; words mostly removed by a cut are dropped."""
    out = []
    for sg in segments:
        if (vd / sg["path"]).resolve() != Path(src).resolve():
            continue
        sp = sg.get("speed", 1) or 1
        for w in words:
            s, e = max(w["s"], sg["start"]), min(w["e"], sg["end"])
            if e - s <= 0 or (e - s) < 0.5 * (w["e"] - w["s"]):
                continue
            os_ = sg["out_start"] + (s - sg["start"]) / sp
            oe = sg["out_start"] + (e - sg["start"]) / sp
            out.append({**w, "s": round(max(os_, sg["out_start"]), 3), "e": round(min(oe, sg["out_end"]), 3)})
    return sorted(out, key=lambda w: w["s"])


def _ass_time(t: float) -> str:
    cs = int(round(max(t, 0) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _bgr(hex_rgb: str, alpha: str = "00") -> str:
    h = hex_rgb.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        die(f"bad colour '{hex_rgb}', use RRGGBB")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _chunks(words, max_words, max_chars, gap=0.5):
    chunks, cur = [], []
    for w in words:
        if cur:
            prev = cur[-1]
            chars = sum(len(x["w"]) + 1 for x in cur) + len(w["w"])
            if (len(cur) >= max_words or chars > max_chars or w["s"] - prev["e"] > gap
                    or re.search(r"[.!?]$", prev["w"]) or (prev["w"].endswith(",") and len(cur) >= 2)):
                chunks.append(cur)
                cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def _break(tokens: list[str], line_chars: int) -> list[int]:
    """Indices after which to break so no line is much longer than line_chars (max 2 lines)."""
    total = sum(len(t) for t in tokens) + len(tokens) - 1
    if total <= line_chars or len(tokens) < 2:
        return []
    best, best_cost = 0, 10**9
    for i in range(1, len(tokens)):
        a = sum(len(t) for t in tokens[:i]) + i - 1
        b = total - a - 1
        cost = max(a, b)
        if cost < best_cost:
            best, best_cost = i, cost
    return [best - 1]


def cmd_captions(a):
    from vk_transcribe import load_transcript, write_srt

    tpath = Path(a.transcript).resolve()
    vd = find_video_dir(tpath)
    if not vd:
        die("transcript must be inside a video folder")
    data, words, src = load_transcript(tpath)

    map_path = Path(a.map).resolve() if a.map else vd / "work" / "cut.map.json"
    if not a.no_map and map_path.exists():
        mp = read_json(map_path)
        mapped = remap_words(words, src, mp["segments"], vd)
        if mapped:
            say(f"timeline: cut ({map_path.name}), {len(mapped)}/{len(words)} words kept")
            words = mapped
        elif a.map:
            die(f"none of the transcript's words fall inside {map_path.name}; is it the same source?")
        else:
            say("timeline: source (transcript's source is not in cut.map.json)")
    else:
        say("timeline: source")
    if not words:
        die("no words to caption")

    fixes = {}
    for pair in (a.fix or "").split(";"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            fixes[re.sub(r"[^\w]", "", k.strip().lower())] = v.strip()
    if fixes:
        for w in words:
            key = re.sub(r"[^\w]", "", w["w"].lower())
            if key in fixes:
                w["w"] = re.sub(r"[\w']+", fixes[key], w["w"], count=1)

    st = dict(STYLES[a.style])
    W, H = (int(x) for x in a.res.lower().split("x"))
    k = min(W, H) / 1080
    hindi = any(DEVANAGARI.search(w["w"]) for w in words)
    font = a.font or ("Nirmala UI" if hindi else st["font"])
    upper = (st["upper"] and not hindi) if a.upper is None else a.upper
    size = round((a.size or st["size"]) * k)
    line_chars = round(st["line_chars"] * W / min(W, H) * (st["size"] / (a.size or st["size"])))
    max_words = a.words or st["words"]
    hl = None if (a.hl or "").lower() == "none" else (a.hl or st["hl"])
    y = round(H * (a.y if a.y is not None else (0.70 if H > W else 0.82)))
    x = W // 2

    if st["box"]:
        border, outline_c, back_c = 3, "&H59000000", "&H59000000"
    else:
        border, outline_c, back_c = 1, "&H00000000", "&H80000000"
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font},{size},{_bgr(a.color)},{_bgr(a.color)},{outline_c},{back_c},{st['bold']},0,0,0,100,100,0,0,{border},{round(st['outline'] * k)},{round(st['shadow'] * k)},5,{round(W * 0.08)},{round(W * 0.08)},0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def disp(w: str) -> str:
        t = w.strip()
        if a.style == "bold":
            t = re.sub(r"[.,;:]+$", "", t)
        t = t.replace("\\", "/").replace("{", "(").replace("}", ")")
        return t.upper() if upper else t

    hl_tag = ("\\1c&H" + _bgr(hl)[4:] + "&") if hl else ""
    base_tag = "\\1c&H" + _bgr(a.color)[4:] + "&"

    events, srt = [], []
    chunks = _chunks(words, max_words, round(line_chars * 1.6))
    for ci, ch in enumerate(chunks):
        tokens = [disp(w["w"]) for w in ch]
        breaks = _break(tokens, line_chars)
        c_start = ch[0]["s"]
        nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else None
        c_end = ch[-1]["e"] + 0.35
        if nxt is not None:
            c_end = nxt if nxt - ch[-1]["e"] < 0.6 else min(c_end, nxt)
        c_end = max(c_end, c_start + 0.3) if nxt is None else max(min(c_end, nxt), c_start + 0.05)
        srt.append((c_start, c_end, " ".join(tokens)))

        def text_for(active):
            parts = []
            for i, t in enumerate(tokens):
                parts.append(f"{{{hl_tag}}}{t}{{{base_tag}}}" if i == active else t)
                if i < len(tokens) - 1:
                    parts.append("\\N" if i in breaks else " ")
            return "".join(parts)

        prefix = f"{{\\an5\\pos({x},{y})}}"
        pop = "{\\fscx82\\fscy82\\t(0,90,\\fscx100\\fscy100)}" if st["pop"] else ""
        if hl:
            for i, w in enumerate(ch):
                s = c_start if i == 0 else w["s"]
                e = ch[i + 1]["s"] if i + 1 < len(ch) else c_end
                if e - s >= 0.01:
                    events.append((s, e, prefix + (pop if i == 0 else "") + text_for(i)))
        else:
            events.append((c_start, c_end, prefix + pop + text_for(None)))

    out = Path(a.out).resolve() if a.out else vd / "work" / "captions.ass"
    out.write_text(header + "\n".join(f"Dialogue: 0,{_ass_time(s)},{_ass_time(e)},Cap,,0,0,0,,{t}"
                                      for s, e, t in events) + "\n", encoding="utf-8")
    srt_path = out.with_suffix(".srt")
    write_srt(srt_path, srt)
    write_json(out.with_suffix(".words.json"), words)
    say(f"captions: {out}  ({len(chunks)} captions, style {a.style}, font '{font}' {size}px, y={y}/{H})")
    say(f"srt:      {srt_path}")
    if hindi:
        warn("Devanagari detected: using 'Nirmala UI' and no uppercase")
