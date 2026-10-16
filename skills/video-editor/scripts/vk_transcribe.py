"""Word-level transcripts with faster-whisper (CPU int8), cached per source; word lookup."""
from __future__ import annotations

import os
import re
import time
from pathlib import Path

from vk_common import (FFQ, audio16k, die, find_video_dir, need, probe, read_json, rel, run, say, ts,
                       warn, work_dir, write_json)

DEFAULT_MODEL = os.environ.get("VK_WHISPER_MODEL")  # None = auto: medium <= 10 min, small above


def register(sub):
    p = sub.add_parser("transcribe", help="word-level transcript -> work/<stem>.transcript.{json,txt,srt}")
    p.add_argument("file")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help="tiny|base|small|medium|large-v3 (default: medium up to 10 min of audio, small above; ~2x realtime for medium on this CPU)")
    p.add_argument("--lang", help="language code (en, hi, ...); default auto-detect")
    p.add_argument("--prompt", help="spelling hints: names, brands, jargon")
    p.add_argument("--beam", type=int, default=5)
    p.add_argument("--from", dest="t0", type=float, help="only this window (re-check a retake); times stay absolute")
    p.add_argument("--to", dest="t1", type=float)
    p.add_argument("--force", action="store_true", help="ignore the cache")
    p.set_defaults(func=cmd_transcribe)

    p = sub.add_parser("words", help="print words with times (range or phrase search)")
    p.add_argument("transcript")
    p.add_argument("--from", dest="t0", type=float, default=0.0)
    p.add_argument("--to", dest="t1", type=float, default=1e9)
    p.add_argument("--find", help="phrase to locate (case/punctuation-insensitive)")
    p.set_defaults(func=cmd_words)


def transcript_path(src: Path, t0=None, t1=None) -> Path:
    tag = "" if t0 is None else f".{t0:g}-{t1:g}"
    return work_dir(src) / f"{src.stem}{tag}.transcript.json"


def load_transcript(path) -> tuple[dict, list[dict], Path]:
    """(data, flat word list, resolved source path)."""
    path = Path(path).resolve()
    data = read_json(path)
    if not data:
        die(f"not a transcript: {path}")
    words = [w for s in data["segments"] for w in s.get("words", [])]
    src = Path(data["source"])
    if not src.is_absolute():
        src = (find_video_dir(path) or path.parent) / src
    return data, words, src.resolve()


def _wav_array(path: Path):
    """16 kHz mono PCM -> float32 array; skips faster-whisper's PyAV decoder (breaks across av versions)."""
    import wave
    np = need("numpy", "numpy")
    with wave.open(str(path), "rb") as w:
        if w.getframerate() != 16000 or w.getnchannels() != 1:
            die(f"{path.name}: expected 16 kHz mono")
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0


def _sib(p: Path, ext: str) -> Path:
    """x.transcript.json -> x.transcript.txt"""
    return p.with_name(p.name[: -len(".json")] + ext)


def _srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path: Path, cues: list[tuple[float, float, str]]):
    lines = []
    for i, (s, e, text) in enumerate(cues, 1):
        lines += [str(i), f"{_srt_time(s)} --> {_srt_time(e)}", text, ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def cmd_transcribe(a):
    src = Path(a.file).resolve()
    vd = find_video_dir(src)
    if not vd:
        die(f"{src} is not inside a video folder; run `vk new` first")
    if (a.t0 is None) != (a.t1 is None):
        die("--from and --to go together")
    out_json = transcript_path(src, a.t0, a.t1)
    if out_json.exists() and not a.force:
        say(f"cached: {out_json}\ntext:   {_sib(out_json, '.txt')}")
        return
    pr = probe(src)
    wav = audio16k(src, work_dir(src), pr)
    clip, offset = wav, 0.0
    if a.t0 is not None:
        clip = work_dir(src) / f"{src.stem}.snip.wav"
        run(FFQ + ["-ss", f"{a.t0:.3f}", "-to", f"{a.t1:.3f}", "-i", wav, "-c:a", "pcm_s16le", clip], echo=False)
        offset = a.t0

    if not a.model:
        a.model = "medium" if pr["duration"] <= 600 or a.t0 is not None else "small"
    need("faster_whisper", "faster-whisper")
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
    from faster_whisper import WhisperModel

    say(f"whisper '{a.model}' int8 on CPU ({os.cpu_count()} threads); first use downloads the model")
    t_start = time.time()
    model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)
    segments, info = model.transcribe(
        _wav_array(clip), language=a.lang, word_timestamps=True, beam_size=a.beam, initial_prompt=a.prompt,
        vad_filter=True, vad_parameters={"min_silence_duration_ms": 500}, condition_on_previous_text=False)
    say(f"language: {info.language} (p={info.language_probability:.2f}), audio {info.duration:.1f}s")
    segs = []
    for s in segments:
        words = [{"w": w.word.strip(), "s": round(w.start + offset, 3), "e": round(w.end + offset, 3),
                  "p": round(w.probability, 3)} for w in (s.words or []) if w.word.strip()]
        seg = {"s": round(s.start + offset, 3), "e": round(s.end + offset, 3), "text": s.text.strip(), "words": words}
        segs.append(seg)
        say(f"[{ts(seg['s'])} -> {ts(seg['e'])}] {seg['text']}")
    if a.t0 is not None:
        clip.unlink(missing_ok=True)
    data = {"source": rel(vd, src), "model": a.model, "language": info.language,
            "duration": round(info.duration, 3), "window": [a.t0, a.t1] if a.t0 is not None else None,
            "segments": segs}
    write_json(out_json, data)
    txt = _sib(out_json, ".txt")
    header = f"# {rel(vd, src)} | whisper {a.model} | {info.language} | {info.duration:.1f}s\n"
    txt.write_text(header + "\n".join(f"[{ts(s['s'])} -> {ts(s['e'])}] {s['text']}" for s in segs) + "\n",
                   encoding="utf-8")
    write_srt(_sib(out_json, ".srt"), [(s["s"], s["e"], s["text"]) for s in segs])
    say(f"\ntranscript: {out_json}\ntext:       {txt}\ntook {time.time() - t_start:.0f}s")
    _flag_suspects(segs)


def _flag_suspects(segs):
    """Whisper merges a repeated take into one stretched word; low-probability words are often misheard."""
    words = [w for s in segs for w in s["words"]]
    long_words = [w for w in words if w["e"] - w["s"] > 1.0]
    unsure = [w for w in words if w["p"] < 0.4]
    if long_words:
        warn("stretched words (possible retake / repeated phrase hidden inside): "
             + ", ".join(f"'{w['w']}'@{ts(w['s'])}({w['e'] - w['s']:.1f}s)" for w in long_words[:10])
             + "  -> re-check with: vk transcribe <file> --from S --to E")
    if unsure:
        warn("low-confidence words (check spelling, add --prompt): "
             + ", ".join(f"'{w['w']}'@{ts(w['s'])}" for w in unsure[:15]))


def _norm(word: str) -> str:
    return re.sub(r"[^\w]", "", word.lower())


def cmd_words(a):
    _, words, _ = load_transcript(a.transcript)
    if a.find:
        target = [_norm(x) for x in a.find.split() if _norm(x)]
        normed = [_norm(w["w"]) for w in words]
        hits = 0
        for i in range(len(words) - len(target) + 1):
            if normed[i:i + len(target)] == target:
                hits += 1
                ctx = " ".join(w["w"] for w in words[max(0, i - 4):i + len(target) + 4])
                say(f"{words[i]['s']:.2f}-{words[i + len(target) - 1]['e']:.2f}  ...{ctx}...")
        if not hits:
            say("no match")
        return
    for w in words:
        if a.t0 <= w["s"] <= a.t1:
            say(f"{w['s']:8.2f} {w['e']:8.2f}  {w['w']}" + ("  (?)" if w["p"] < 0.4 else ""))
