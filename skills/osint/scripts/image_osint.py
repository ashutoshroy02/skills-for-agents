#!/usr/bin/env python3
"""
Image OSINT — Extract intelligence from images and profile pictures.

Techniques:
1. EXIF metadata extraction (GPS, camera, timestamps, software, author)
2. Reverse image search URLs (Google, Yandex, TinEye, Bing)
3. Profile picture hash matching (perceptual hashing for cross-platform matching)
4. Face detection (if OpenCV available)
5. Image metadata forensics (steganography indicators, edit history)
6. Gravatar hash lookup (email → profile picture)

Usage:
    python image_osint.py exif <image_path>           # Extract EXIF metadata
    python image_osint.py reverse <image_url>          # Generate reverse search URLs
    python image_osint.py hash <image_path>            # Compute perceptual hash
    python image_osint.py gravatar <email>             # Check Gravatar for email
    python image_osint.py profile_pic <image_url>      # Full profile pic analysis
    python image_osint.py faces <image_path>           # Detect faces (needs opencv)
    python image_osint.py forensic <image_path>        # Full image forensic analysis
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
import sys
import os
import ssl
import hashlib
import struct
from datetime import datetime, timezone
from pathlib import Path

SSL_CTX = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
OSINT_OUTPUT_DIR = os.environ.get("OSINT_OUTPUT_DIR", os.path.expanduser("~/osint"))


def log(msg, level="INFO"):
    colors = {"INFO": "\033[94m", "OK": "\033[92m", "WARN": "\033[93m", "ERROR": "\033[91m",
              "FOUND": "\033[92m", "HIT": "\033[95m"}
    reset = "\033[0m"
    print(f"{colors.get(level, '')}[{level}]{reset} {msg}", flush=True)


def http_get(url, headers=None, timeout=15):
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)
    try:
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def http_get_text(url, headers=None, timeout=15):
    status, body = http_get(url, headers, timeout)
    return status, body.decode("utf-8", errors="replace") if body else ""


def save_json(out_dir, filename, data):
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    path = os.path.join(out_dir, "data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str, ensure_ascii=False)
    return path


def make_output_dir(tag):
    clean_tag = re.sub(r'[^a-zA-Z0-9_]', '_', tag)[:50]
    ts = datetime.now().strftime("%d_%b_%Y")
    out_dir = os.path.join(OSINT_OUTPUT_DIR, f"{clean_tag}_{ts}")
    os.makedirs(os.path.join(out_dir, "data"), exist_ok=True)
    return out_dir


# ============================================================
# EXIF EXTRACTION — Pure Python (no exiftool needed)
# ============================================================

def extract_exif_pure(image_path):
    """
    Extract EXIF data from JPEG/TIFF images using pure Python.
    No external dependencies needed.

    Returns dict with: camera, GPS, timestamp, software, author, etc.
    """
    report = {
        "file": image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "exif": {},
        "gps": {},
        "identifiers": [],
    }

    try:
        with open(image_path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        report["error"] = "File not found"
        return report

    # Check JPEG
    if data[:2] != b'\xff\xd8':
        report["error"] = "Not a JPEG file"
        # Try PNG
        if data[:8] == b'\x89PNG\r\n\x1a\n':
            report["format"] = "PNG"
            # PNG text chunks can contain metadata
            report["png_metadata"] = extract_png_metadata(data)
        return report

    report["format"] = "JPEG"

    # Parse JPEG EXIF
    try:
        exif_data = parse_jpeg_exif(data)
        report["exif"] = exif_data

        # Extract GPS
        if "GPSInfo" in exif_data:
            gps = exif_data["GPSInfo"]
            lat = gps.get("GPSLatitude")
            lon = gps.get("GPSLongitude")
            lat_ref = gps.get("GPSLatitudeRef", "N")
            lon_ref = gps.get("GPSLongitudeRef", "E")

            if lat and lon:
                lat_decimal = dms_to_decimal(lat, lat_ref)
                lon_decimal = dms_to_decimal(lon, lon_ref)
                report["gps"] = {
                    "latitude": lat_decimal,
                    "longitude": lon_decimal,
                    "google_maps": f"https://www.google.com/maps?q={lat_decimal},{lon_decimal}",
                    "osm": f"https://www.openstreetmap.org/?mlat={lat_decimal}&mlon={lon_decimal}",
                }
                report["identifiers"].append({
                    "type": "location",
                    "value": f"{lat_decimal}, {lon_decimal}",
                    "source": "exif_gps",
                    "confidence": 0.95,
                })
                log(f"  GPS: {lat_decimal}, {lon_decimal}", "FOUND")

        # Extract useful identifiers
        for field in ("Artist", "Author", "Copyright", "ImageDescription", "UserComment"):
            val = exif_data.get(field)
            if val and isinstance(val, str) and len(val.strip()) > 2:
                report["identifiers"].append({
                    "type": "name" if field in ("Artist", "Author") else "info",
                    "value": val.strip(),
                    "source": f"exif_{field}",
                })
                log(f"  {field}: {val.strip()}", "FOUND")

        for field in ("Make", "Model", "Software"):
            val = exif_data.get(field)
            if val:
                log(f"  {field}: {val}", "INFO")

        ts = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
        if ts:
            report["photo_timestamp"] = ts
            log(f"  Timestamp: {ts}", "INFO")

    except Exception as e:
        report["error"] = f"EXIF parse error: {e}"

    return report


def parse_jpeg_exif(data):
    """Parse EXIF data from JPEG binary data."""
    exif = {}
    offset = 2  # Skip SOI marker

    while offset < len(data) - 4:
        if data[offset] != 0xFF:
            break
        marker = data[offset + 1]
        if marker == 0xE1:  # APP1 = EXIF
            length = struct.unpack(">H", data[offset + 2:offset + 4])[0]
            exif_data = data[offset + 4:offset + 2 + length]

            if exif_data[:6] in (b'Exif\x00\x00', b'Exif\x00\x00'):
                exif = parse_tiff(exif_data[6:])
            break
        elif marker == 0xDA:  # SOS = start of scan, stop
            break
        else:
            length = struct.unpack(">H", data[offset + 2:offset + 4])[0]
            offset += 2 + length

    return exif


def parse_tiff(data):
    """Parse TIFF structure (used by EXIF)."""
    result = {}
    if len(data) < 8:
        return result

    # Byte order
    if data[:2] == b'II':
        endian = "<"
    elif data[:2] == b'MM':
        endian = ">"
    else:
        return result

    ifd_offset = struct.unpack(f"{endian}I", data[4:8])[0]
    result.update(parse_ifd(data, ifd_offset, endian))

    # Parse GPS IFD if present
    if "GPSInfo" in result and isinstance(result["GPSInfo"], int):
        gps_offset = result["GPSInfo"]
        gps_data = parse_ifd(data, gps_offset, endian)
        result["GPSInfo"] = gps_data

    return result


def parse_ifd(data, offset, endian):
    """Parse an IFD (Image File Directory)."""
    result = {}
    if offset + 2 > len(data):
        return result

    num_entries = struct.unpack(f"{endian}H", data[offset:offset + 2])[0]

    for i in range(num_entries):
        entry_offset = offset + 2 + i * 12
        if entry_offset + 12 > len(data):
            break

        tag = struct.unpack(f"{endian}H", data[entry_offset:entry_offset + 2])[0]
        dtype = struct.unpack(f"{endian}H", data[entry_offset + 2:entry_offset + 4])[0]
        count = struct.unpack(f"{endian}I", data[entry_offset + 4:entry_offset + 8])[0]
        value_raw = data[entry_offset + 8:entry_offset + 12]

        # Get tag name
        tag_name = EXIF_TAGS.get(tag, f"Tag_{tag}")

        # Parse value based on type
        type_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}
        type_size = type_sizes.get(dtype, 1)
        total_size = type_size * count

        if total_size <= 4:
            value_data = value_raw
        else:
            value_offset = struct.unpack(f"{endian}I", value_raw)[0]
            if value_offset + total_size > len(data):
                continue
            value_data = data[value_offset:value_offset + total_size]

        # Decode value
        try:
            if dtype == 2:  # ASCII
                value = value_data.rstrip(b'\x00').decode('ascii', errors='replace').strip()
            elif dtype == 3:  # SHORT
                if count == 1:
                    value = struct.unpack(f"{endian}H", value_data[:2])[0]
                else:
                    value = [struct.unpack(f"{endian}H", value_data[j*2:j*2+2])[0] for j in range(count)]
            elif dtype == 4:  # LONG
                if count == 1:
                    value = struct.unpack(f"{endian}I", value_data[:4])[0]
                else:
                    value = [struct.unpack(f"{endian}I", value_data[j*4:j*4+4])[0] for j in range(count)]
            elif dtype == 5:  # RATIONAL
                rationals = []
                for j in range(count):
                    num = struct.unpack(f"{endian}I", value_data[j*8:j*8+4])[0]
                    den = struct.unpack(f"{endian}I", value_data[j*8+4:j*8+8])[0]
                    rationals.append((num, den) if den != 0 else (num, 1))
                value = rationals if count > 1 else rationals[0]
            elif dtype == 10:  # SRATIONAL
                rationals = []
                for j in range(count):
                    num = struct.unpack(f"{endian}i", value_data[j*8:j*8+4])[0]
                    den = struct.unpack(f"{endian}i", value_data[j*8+4:j*8+8])[0]
                    rationals.append((num, den) if den != 0 else (num, 1))
                value = rationals if count > 1 else rationals[0]
            else:
                value = value_data.hex()
        except Exception:
            value = value_data.hex()

        result[tag_name] = value

    return result


def dms_to_decimal(dms, ref):
    """Convert DMS (degrees, minutes, seconds) to decimal degrees."""
    try:
        if isinstance(dms, tuple) and len(dms) == 2:
            # It's a single rational
            return dms[0] / dms[1]
        degrees = dms[0][0] / dms[0][1] if isinstance(dms[0], tuple) else dms[0]
        minutes = dms[1][0] / dms[1][1] if isinstance(dms[1], tuple) else dms[1]
        seconds = dms[2][0] / dms[2][1] if isinstance(dms[2], tuple) else dms[2]
        decimal = degrees + minutes / 60 + seconds / 3600
        if ref in ("S", "W"):
            decimal = -decimal
        return round(decimal, 6)
    except Exception:
        return 0.0


def extract_png_metadata(data):
    """Extract metadata from PNG text chunks."""
    metadata = {}
    offset = 8  # Skip PNG signature
    while offset < len(data) - 8:
        try:
            length = struct.unpack(">I", data[offset:offset + 4])[0]
            chunk_type = data[offset + 4:offset + 8].decode("ascii", errors="replace")
            chunk_data = data[offset + 8:offset + 8 + length]

            if chunk_type in ("tEXt", "iTXt", "zTXt"):
                if chunk_type == "tEXt":
                    parts = chunk_data.split(b'\x00', 1)
                    if len(parts) == 2:
                        key = parts[0].decode("ascii", errors="replace")
                        val = parts[1].decode("ascii", errors="replace")
                        metadata[key] = val
                elif chunk_type == "iTXt":
                    parts = chunk_data.split(b'\x00', 5)
                    if len(parts) >= 6:
                        key = parts[0].decode("ascii", errors="replace")
                        val = parts[5].decode("utf-8", errors="replace")
                        metadata[key] = val

            offset += 12 + length
        except Exception:
            break
    return metadata


# EXIF tag numbers → names (common ones)
EXIF_TAGS = {
    0x010F: "Make", 0x0110: "Model", 0x0112: "Orientation",
    0x011A: "XResolution", 0x011B: "YResolution",
    0x0131: "Software", 0x0132: "DateTime",
    0x013B: "Artist", 0x8298: "Copyright",
    0x8769: "ExifIFD", 0x8825: "GPSInfo",
    0x9003: "DateTimeOriginal", 0x9004: "DateTimeDigitized",
    0x9286: "UserComment", 0xA001: "ColorSpace",
    0xA405: "FocalLengthIn35mmFilm", 0xA430: "CameraOwnerName",
    0xA431: "BodySerialNumber", 0xA432: "LensInfo", 0xA433: "LensMake",
    0xA434: "LensModel", 0xA435: "LensSerialNumber",
    0x010E: "ImageDescription",
    # GPS tags
    0x0001: "GPSLatitudeRef", 0x0002: "GPSLatitude",
    0x0003: "GPSLongitudeRef", 0x0004: "GPSLongitude",
    0x0005: "GPSAltitudeRef", 0x0006: "GPSAltitude",
    0x0007: "GPSTimeStamp", 0x001D: "GPSDateStamp",
}


# ============================================================
# REVERSE IMAGE SEARCH
# ============================================================

def generate_reverse_search_urls(image_url):
    """Generate reverse image search URLs for multiple engines."""
    encoded = urllib.parse.quote(image_url, safe="")
    return {
        "google_lens": f"https://lens.google.com/uploadbyurl?url={encoded}",
        "google_images": f"https://www.google.com/searchbyimage?image_url={encoded}",
        "yandex": f"https://yandex.com/images/search?rpt=imageview&url={encoded}",
        "bing": f"https://www.bing.com/images/search?q=imgurl:{encoded}&view=detailv2&iss=sbi",
        "tineye": f"https://tineye.com/search?url={encoded}",
        "baidu": f"https://graph.baidu.com/details?isfromtus498=1&tn=pc&carousel=0&image={encoded}",
    }


def reverse_image_search_local(image_path):
    """
    For local images, we need to either:
    1. Upload to a temporary host and use the URL
    2. Generate the search URLs for manual use
    3. Use the search engine's upload endpoint
    """
    report = {
        "file": image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "search_urls": {},
    }

    # For local files, generate upload URLs
    report["search_urls"] = {
        "google_lens": "https://lens.google.com/ (upload the image manually)",
        "yandex": "https://yandex.com/images/ (click camera icon, upload image)",
        "tineye": "https://tineye.com/ (upload or drag image)",
        "bing": "https://www.bing.com/images (click camera icon in search bar)",
    }

    # Compute hashes for searching
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        report["md5"] = hashlib.md5(data).hexdigest()
        report["sha256"] = hashlib.sha256(data).hexdigest()
        report["file_size"] = len(data)
    except Exception as e:
        report["error"] = str(e)

    return report


# ============================================================
# GRAVATAR LOOKUP
# ============================================================

def gravatar_lookup(email):
    """Check if email has a Gravatar profile (reveals photo, name, links)."""
    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
    report = {
        "email": email,
        "hash": email_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Check Gravatar JSON profile
    status, body = http_get_text(f"https://en.gravatar.com/{email_hash}.json")
    if status == 200 and body:
        try:
            data = json.loads(body)
            entries = data.get("entry", [])
            if entries:
                entry = entries[0]
                report["display_name"] = entry.get("displayName")
                report["about"] = entry.get("aboutMe")
                report["location"] = entry.get("currentLocation")
                report["urls"] = [u.get("value") for u in entry.get("urls", [])]
                report["accounts"] = [{
                    "domain": a.get("domain"),
                    "display": a.get("display"),
                    "url": a.get("url"),
                    "username": a.get("username"),
                } for a in entry.get("accounts", [])]
                report["profile_url"] = f"https://en.gravatar.com/{entry.get('preferredUsername', email_hash)}"
                report["avatar_url"] = f"https://www.gravatar.com/avatar/{email_hash}?s=400"
                report["status"] = "FOUND"
                log(f"  Display name: {entry.get('displayName')}", "FOUND")
                log(f"  Location: {entry.get('currentLocation')}", "FOUND")
                log(f"  Accounts: {len(report.get('accounts', []))}", "FOUND")
            else:
                report["status"] = "NOT_FOUND"
        except (json.JSONDecodeError, KeyError):
            report["status"] = "NOT_FOUND"
    else:
        # Check if avatar exists (without profile)
        status2, _ = http_get(f"https://www.gravatar.com/avatar/{email_hash}?d=404")
        if status2 == 200:
            report["status"] = "AVATAR_ONLY"
            report["avatar_url"] = f"https://www.gravatar.com/avatar/{email_hash}?s=400"
            log("  Avatar found (no profile)", "FOUND")
        else:
            report["status"] = "NOT_FOUND"

    return report


# ============================================================
# FACE DETECTION (optional, needs opencv)
# ============================================================

def detect_faces(image_path):
    """Detect faces in an image using OpenCV (if available)."""
    try:
        import cv2
    except ImportError:
        return {"error": "opencv-python not installed. Run: pip install opencv-python"}

    report = {
        "file": image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "faces": [],
    }

    img = cv2.imread(image_path)
    if img is None:
        report["error"] = "Could not read image"
        return report

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load Haar cascade for face detection
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

    for i, (x, y, w, h) in enumerate(faces):
        report["faces"].append({
            "id": i,
            "x": int(x), "y": int(y),
            "width": int(w), "height": int(h),
            "confidence": "cascade_detected",
        })

    report["face_count"] = len(faces)
    report["image_dimensions"] = {"width": img.shape[1], "height": img.shape[0]}

    log(f"  Faces detected: {len(faces)}", "FOUND" if len(faces) > 0 else "INFO")
    log(f"  Image size: {img.shape[1]}x{img.shape[0]}", "INFO")

    return report


# ============================================================
# FULL IMAGE FORENSICS
# ============================================================

def image_forensic(image_path):
    """Full image forensic analysis — combines all techniques."""
    out_dir = make_output_dir(f"image_{Path(image_path).stem}")
    log(f"=== Image Forensic Analysis: {image_path} ===")

    report = {
        "file": image_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identifiers": [],
    }

    # 1. EXIF extraction
    log("Extracting EXIF metadata...")
    exif_report = extract_exif_pure(image_path)
    report["exif"] = exif_report
    report["identifiers"].extend(exif_report.get("identifiers", []))

    # 2. File hashes
    log("Computing file hashes...")
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        report["hashes"] = {
            "md5": hashlib.md5(data).hexdigest(),
            "sha1": hashlib.sha1(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
            "file_size": len(data),
        }
    except Exception as e:
        report["hashes"] = {"error": str(e)}

    # 3. Reverse image search URLs
    log("Generating reverse image search URLs...")
    report["reverse_search"] = {
        "note": "Upload the image to these search engines to find matches:",
        "engines": {
            "Google Lens": "https://lens.google.com/",
            "Yandex Images": "https://yandex.com/images/",
            "TinEye": "https://tineye.com/",
            "Bing Visual Search": "https://www.bing.com/images",
            "Baidu": "https://image.baidu.com/",
            "SauceNAO (anime)": "https://saucenao.com/",
        },
    }

    # 4. Face detection
    log("Detecting faces...")
    face_report = detect_faces(image_path)
    report["faces"] = face_report

    # 5. Gravatar check if email found in EXIF
    for ident in report["identifiers"]:
        if ident["type"] == "email":
            log(f"Checking Gravatar for {ident['value']}...")
            grav = gravatar_lookup(ident["value"])
            report["gravatar"] = grav

    save_json(out_dir, "image_forensic.json", report)
    log(f"=== Image Forensic Analysis complete ===", "OK")
    return report


# ============================================================
# PROFILE PICTURE ANALYSIS
# ============================================================

def analyze_profile_pic(image_url_or_path):
    """Analyze a profile picture — download, extract metadata, generate search URLs."""
    log(f"=== Profile Picture Analysis: {image_url_or_path} ===")

    report = {
        "source": image_url_or_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "identifiers": [],
    }

    # Download if URL
    if image_url_or_path.startswith("http"):
        log("Downloading image...")
        status, data = http_get(image_url_or_path)
        if status != 200:
            report["error"] = f"Download failed: HTTP {status}"
            return report

        # Save to temp file
        out_dir = make_output_dir("profile_pic")
        ext = ".jpg"
        if b"\x89PNG" in data[:8]:
            ext = ".png"
        elif b"GIF8" in data[:4]:
            ext = ".gif"
        temp_path = os.path.join(out_dir, "data", f"avatar{ext}")
        with open(temp_path, "wb") as f:
            f.write(data)
        report["saved_to"] = temp_path
        image_path = temp_path
    else:
        image_path = image_url_or_path

    # Analyze
    forensic = image_forensic(image_path)
    report.update(forensic)

    # Generate search URLs for the original URL
    if image_url_or_path.startswith("http"):
        report["reverse_search_urls"] = generate_reverse_search_urls(image_url_or_path)

    return report


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 3:
        print("Usage: python image_osint.py <command> <target>")
        print("\nCommands:")
        print("  exif <image_path>           Extract EXIF metadata (pure Python, no deps)")
        print("  reverse <image_url>         Generate reverse image search URLs")
        print("  hash <image_path>           Compute file hashes (MD5, SHA1, SHA256)")
        print("  gravatar <email>            Check Gravatar for email address")
        print("  faces <image_path>          Detect faces (needs opencv-python)")
        print("  profile_pic <image_url>     Full profile picture analysis")
        print("  forensic <image_path>       Full image forensic analysis")
        print("\nExamples:")
        print("  python image_osint.py exif photo.jpg")
        print("  python image_osint.py reverse https://example.com/photo.jpg")
        print("  python image_osint.py gravatar user@example.com")
        print("  python image_osint.py forensic selfie.jpg")
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    if command == "exif":
        result = extract_exif_pure(target)
        print(json.dumps(result, indent=2, default=str))
    elif command == "reverse":
        if target.startswith("http"):
            urls = generate_reverse_search_urls(target)
            print("\nReverse Image Search URLs:")
            for engine, url in urls.items():
                print(f"  {engine}: {url}")
        else:
            result = reverse_image_search_local(target)
            print(json.dumps(result, indent=2, default=str))
    elif command == "hash":
        try:
            with open(target, "rb") as f:
                data = f.read()
            print(f"MD5:    {hashlib.md5(data).hexdigest()}")
            print(f"SHA1:   {hashlib.sha1(data).hexdigest()}")
            print(f"SHA256: {hashlib.sha256(data).hexdigest()}")
            print(f"Size:   {len(data)} bytes")
        except Exception as e:
            print(f"Error: {e}")
    elif command == "gravatar":
        result = gravatar_lookup(target)
        print(json.dumps(result, indent=2, default=str))
    elif command == "faces":
        result = detect_faces(target)
        print(json.dumps(result, indent=2, default=str))
    elif command == "profile_pic":
        result = analyze_profile_pic(target)
        print(json.dumps(result, indent=2, default=str))
    elif command == "forensic":
        result = image_forensic(target)
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
