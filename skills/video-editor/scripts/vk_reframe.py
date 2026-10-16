"""Face-tracked crop path for turning wide footage vertical (used by `vk render --reframe face`)."""
from __future__ import annotations

import math
from pathlib import Path

from vk_common import TOOLS_HOME, die, need, probe, read_json, say, work_dir, write_json

YUNET = TOOLS_HOME / "models" / "face_detection_yunet_2023mar.onnx"


def register(sub):
    p = sub.add_parser("track", help="analyse faces for a vertical crop; prints coverage (render uses it)")
    p.add_argument("file")
    p.add_argument("--aspect", default="9:16")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_track)


def _even(x: float) -> int:
    return int(x) // 2 * 2


def _detector(cv2):
    if YUNET.exists():
        det = cv2.FaceDetectorYN.create(str(YUNET), "", (320, 320), 0.7, 0.3, 50)

        def detect(img):
            det.setInputSize((img.shape[1], img.shape[0]))
            _, faces = det.detect(img)
            return [] if faces is None else [(f[0], f[1], f[2], f[3]) for f in faces]
        return "yunet", detect
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def detect(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        m = int(img.shape[0] * 0.06)
        return [tuple(r) for r in casc.detectMultiScale(gray, 1.1, 6, minSize=(m, m))]
    return "haar", detect


def track_faces(src: Path, pr: dict, aspect: float, sample_fps: float = 4.0, force: bool = False) -> dict | None:
    """Per-frame crop x for a crop of `aspect` (w/h). None when the source is not wider than that."""
    v = pr["video"]
    iw, ih = v["width"], v["height"]
    if iw / ih <= aspect + 0.01:
        return None
    cw = _even(ih * aspect)
    cache = work_dir(src) / f"{src.stem}.track.json"
    key = f"{src.stat().st_size}-{int(src.stat().st_mtime)}-{aspect:.4f}"
    old = read_json(cache)
    if old and old.get("key") == key and not force:
        return old

    cv2 = need("cv2", "opencv-python-headless<5")
    np = need("numpy", "numpy")
    name, detect = _detector(cv2)
    cap = cv2.VideoCapture(str(src))
    if hasattr(cv2, "CAP_PROP_ORIENTATION_AUTO"):
        cap.set(cv2.CAP_PROP_ORIENTATION_AUTO, 1)
    fps = cap.get(cv2.CAP_PROP_FPS) or v["fps"]
    step = max(1, round(fps / sample_fps))
    say(f"tracking faces ({name}) every {step} frames ...")
    samples, i = [], 0
    while cap.grab():
        if i % step == 0:
            ok, frame = cap.retrieve()
            if not ok:
                break
            fh, fw = frame.shape[:2]
            sc = min(1.0, 640 / fw)
            small = cv2.resize(frame, None, fx=sc, fy=sc) if sc < 1 else frame
            faces = []
            for x, y, w, h in detect(small):
                if h / small.shape[0] < 0.05:  # tiny background "faces" are mostly false positives
                    continue
                faces.append(((x + w / 2) / sc * iw / fw, w * h))
            samples.append(faces)
        i += 1
    cap.release()
    nframes = i
    if not samples:
        die("could not decode frames for tracking")

    # choose a subject per sample: stay on the current one unless another is much bigger
    raw, prev = [], None
    for faces in samples:
        if not faces:
            raw.append(None)
            continue
        largest = max(faces, key=lambda f: f[1])
        pick = largest
        if prev is not None:
            near = min(faces, key=lambda f: abs(f[0] - prev))
            if near[1] >= 0.5 * largest[1] and abs(near[0] - prev) < 0.15 * iw:
                pick = near
        raw.append(pick[0])
        prev = pick[0]
    coverage = sum(r is not None for r in raw) / len(raw)
    filled = list(raw)
    last = next((r for r in raw if r is not None), iw / 2)
    for k, r in enumerate(filled):
        last = r if r is not None else last
        filled[k] = last
    arr = np.array(filled, dtype=float)
    med = np.array([np.median(arr[max(0, k - 2):k + 3]) for k in range(len(arr))])  # drop 1-sample blips

    # virtual camera: dead zone + easing, hard cut on a subject switch
    alpha = 1 - math.exp(-1 / (fps * 0.35))
    dead = 0.08 * cw
    cam = med[0]
    xs = []
    for f in range(nframes):
        k = min(f // step, len(med) - 1)
        tx = med[k]
        d = tx - cam
        if abs(d) > 0.22 * iw:
            cam = tx
        elif abs(d) > dead:
            cam += (d - math.copysign(dead, d)) * alpha
        xs.append(_even(min(max(cam - cw / 2, 0), iw - cw)))
    res = {"key": key, "detector": name, "iw": iw, "ih": ih, "cw": cw, "ch": ih, "fps": fps,
           "coverage": round(coverage, 3), "xs": xs}
    write_json(cache, res)
    return res


def write_sendcmd(track: dict, path: Path, t_offset: float = 0.0, target: str = "crop@rf"):
    """sendcmd script: one line per frame where the crop x changes."""
    fps, xs = track["fps"], track["xs"]
    first = int(round(t_offset * fps))
    lines, last = [], None
    for f in range(first, len(xs)):
        if xs[f] != last:
            lines.append(f"{(f - first) / fps:.4f} {target} x {xs[f]};")
            last = xs[f]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return xs[min(first, len(xs) - 1)]


def cmd_track(a):
    src = Path(a.file).resolve()
    pr = probe(src)
    w, h = (float(x) for x in a.aspect.split(":"))
    tr = track_faces(src, pr, w / h, force=a.force)
    if tr is None:
        say("source is not wider than the target aspect: no horizontal tracking needed")
        return
    xs = tr["xs"]
    moves = sum(1 for i in range(1, len(xs)) if abs(xs[i] - xs[i - 1]) > 0.2 * tr["iw"])
    say(f"faces in {tr['coverage'] * 100:.0f}% of samples ({tr['detector']}); crop {tr['cw']}x{tr['ch']} "
        f"of {tr['iw']}x{tr['ih']}; x range {min(xs)}-{max(xs)}; {moves} hard subject switches")
    say("render uses face tracking when coverage >= 30%, otherwise blurred-background fit")
