#!/usr/bin/env python3
"""
svg_generator.py - Generate SVG logos programmatically.
Creates clean, scalable vector logos from text/shapes without any API.

Usage:
    python svg_generator.py --name "ProjectName" --style modern --output ./brand/
    python svg_generator.py --name "NO" --style monogram --color "#6366f1" --output ./brand/
"""

import argparse
import math
import os
import sys
from pathlib import Path

# --- SVG Helpers ---

def svg_header(width=512, height=512, bg=None):
    bg_rect = '<rect width="{}" height="{}" fill="{}" rx="32"/>'.format(width, height, bg) if bg else ""
    return '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {} {}" width="{}" height="{}">\n  {}\n'.format(width, height, width, height, bg_rect)

SVG_FOOTER = "</svg>"

def svg_wrap(inner, width=512, height=512, bg=None):
    return svg_header(width, height, bg) + inner + "\n" + SVG_FOOTER

# --- Shape Primitives ---

def circle(cx, cy, r, fill, stroke=None, sw=0):
    s = ' stroke="{}" stroke-width="{}"'.format(stroke, sw) if stroke else ""
    return '<circle cx="{}" cy="{}" r="{}" fill="{}"{}/>'.format(cx, cy, r, fill, s)

def rect(x, y, w, h, fill, rx=0, stroke=None, sw=0):
    s = ' stroke="{}" stroke-width="{}"'.format(stroke, sw) if stroke else ""
    r = ' rx="{}"'.format(rx) if rx else ""
    return '<rect x="{}" y="{}" width="{}" height="{}" fill="{}"{}{}/>'.format(x, y, w, h, fill, r, s)

def rounded_rect(x, y, w, h, fill, rx=16):
    return rect(x, y, w, h, fill, rx=rx)

def hexagon(cx, cy, r, fill, stroke=None, sw=0):
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        points.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
    s = ' stroke="{}" stroke-width="{}"'.format(stroke, sw) if stroke else ""
    return '<polygon points="{}" fill="{}"{}/>'.format(" ".join(points), fill, s)

def triangle(cx, cy, r, fill, rotation=0):
    points = []
    for i in range(3):
        angle = math.radians(120 * i - 90 + rotation)
        points.append("{:.1f},{:.1f}".format(cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return '<polygon points="{}" fill="{}"/>'.format(" ".join(points), fill)

def diamond(cx, cy, r, fill):
    return '<polygon points="{},{},{},{},{},{}" fill="{}"/>'.format(
        cx, cy-r, cx+r, cy, cx, cy+r, cx-r, cy, fill)

def text_elem(x, y, text, size, fill, anchor="middle", weight="bold", family="Arial, Helvetica, sans-serif"):
    return '<text x="{}" y="{}" text-anchor="{}" font-size="{}" font-weight="{}" font-family="{}" fill="{}">{}</text>'.format(
        x, y, anchor, size, weight, family, fill, text)

# --- Logo Styles ---

def style_modern(name, primary="#1a1a2e", accent="#e94560", size=512, **kw):
    cx, cy = size // 2, size // 2
    initial = name[0].upper()
    r = int(size * 0.3)
    inner = "\n  ".join([
        circle(cx, cy, r, primary),
        text_elem(cx, cy + int(r * 0.15), initial, int(r * 1.2), "#ffffff"),
        rect(cx - int(r * 0.6), cy + int(r * 0.55), int(r * 1.2), 6, accent, rx=3),
    ])
    return svg_wrap(inner, size, size)

def style_tech(name, primary="#0f0f23", accent="#00d4ff", size=512, **kw):
    cx, cy = size // 2, size // 2
    initial = name[0].upper()
    r = int(size * 0.32)
    inner = "\n  ".join([
        hexagon(cx, cy, r, primary, stroke=accent, sw=3),
        text_elem(cx, cy + int(r * 0.15), initial, int(r * 0.9), accent, family="'Courier New', monospace"),
        '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="2" opacity="0.5"/>'.format(
            cx - int(r * 0.4), cy + int(r * 0.5), cx + int(r * 0.4), cy + int(r * 0.5), accent),
    ])
    return svg_wrap(inner, size, size, bg="#0a0a1a")

def style_playful(name, primary="#ff6b6b", secondary="#4ecdc4", size=512, **kw):
    cx, cy = size // 2, size // 2
    initial = name[0].upper()
    r = int(size * 0.32)
    inner = "\n  ".join([
        circle(cx, cy, r, primary),
        circle(cx - int(r * 0.15), cy - int(r * 0.15), int(r * 0.7), secondary),
        text_elem(cx, cy + int(r * 0.15), initial, int(r * 1.0), "#ffffff"),
    ])
    return svg_wrap(inner, size, size)

def style_elegant(name, primary="#2c3e50", accent="#c9a96e", size=512, **kw):
    cx, cy = size // 2, size // 2
    initial = name[0].upper()
    r = int(size * 0.28)
    inner = "\n  ".join([
        circle(cx, cy, r + 8, "none", stroke=accent, sw=2),
        circle(cx, cy, r, primary),
        text_elem(cx, cy + int(r * 0.18), initial, int(r * 1.1), accent,
                  family="'Georgia', 'Times New Roman', serif"),
    ])
    return svg_wrap(inner, size, size)

def style_monogram(name, primary="#6366f1", size=512, **kw):
    words = name.split()
    if len(words) >= 2:
        initials = (words[0][0] + words[1][0]).upper()
    else:
        initials = name[:2].upper()
    cx, cy = size // 2, size // 2
    r = int(size * 0.35)
    inner = "\n  ".join([
        circle(cx, cy, r, primary),
        text_elem(cx, cy + int(r * 0.15), initials, int(r * 0.85), "#ffffff"),
    ])
    return svg_wrap(inner, size, size)

def style_icon(name, primary="#3b82f6", size=512, **kw):
    cx, cy = size // 2, size // 2
    r = int(size * 0.3)
    seed = sum(ord(c) for c in name) % 4

    if seed == 0:
        inner = "\n  ".join([
            circle(cx - int(r * 0.3), cy, int(r * 0.65), primary),
            circle(cx + int(r * 0.3), cy, int(r * 0.65), primary + "88"),
        ])
    elif seed == 1:
        inner = "\n  ".join([
            triangle(cx, cy - int(r * 0.2), int(r * 0.6), primary),
            triangle(cx, cy + int(r * 0.3), int(r * 0.45), primary + "88", rotation=180),
        ])
    elif seed == 2:
        inner = "\n  ".join([
            diamond(cx, cy, int(r * 0.8), primary),
            circle(cx, cy, int(r * 0.35), "#ffffff"),
        ])
    else:
        s = int(r * 1.4)
        inner = "\n  ".join([
            rounded_rect(cx - s//2, cy - s//2, s, s, primary, rx=s//4),
            circle(cx + s//4, cy - s//4, s//4, "#ffffff"),
        ])
    return svg_wrap(inner, size, size)

# --- Style Registry ---

STYLES = {
    "modern": style_modern,
    "tech": style_tech,
    "playful": style_playful,
    "elegant": style_elegant,
    "monogram": style_monogram,
    "icon": style_icon,
}

# --- Brand Kit Generation ---

def svg_to_png(svg_path, png_path, size):
    """Convert SVG to PNG. Tries cairosvg, falls back to Pillow placeholder."""
    try:
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size)
        return True
    except ImportError:
        pass

    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle(
            [size//6, size//6, size*5//6, size*5//6],
            fill="#3b82f6", radius=size//8
        )
        try:
            font = ImageFont.truetype("arial.ttf", size // 3)
        except OSError:
            font = ImageFont.load_default()
        draw.text((size//2, size//2), "LOGO", fill="white", font=font, anchor="mm")
        img.save(png_path, "PNG")
        return True
    except ImportError:
        print("  [!] Neither cairosvg nor Pillow available, skipping PNG: {}".format(png_path))
        return False

def generate_brand_kit(svg_dir, output_dir):
    """Generate full brand kit from SVG files."""
    sizes = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-48.png": 48,
        "favicon-96.png": 96,
        "apple-touch-icon.png": 180,
        "android-chrome-192.png": 192,
        "android-chrome-512.png": 512,
    }

    svg_path = os.path.join(svg_dir, "icon-only.svg")
    if not os.path.exists(svg_path):
        svg_path = os.path.join(svg_dir, "logo-modern.svg")
    if not os.path.exists(svg_path):
        print("[!] No SVG found to convert")
        return

    os.makedirs(output_dir, exist_ok=True)

    for filename, sz in sizes.items():
        out = os.path.join(output_dir, filename)
        if svg_to_png(svg_path, out, sz):
            print("  [+] {} ({}x{})".format(filename, sz, sz))

    # OG image (1200x630)
    try:
        from PIL import Image
        og = Image.new("RGB", (1200, 630), "#ffffff")
        icon_path = os.path.join(output_dir, "android-chrome-512.png")
        if os.path.exists(icon_path):
            icon = Image.open(icon_path)
            icon = icon.resize((400, 400), Image.LANCZOS)
            og.paste(icon, (400, 115), icon if icon.mode == "RGBA" else None)
        og.save(os.path.join(output_dir, "og-image.png"), "PNG")
        print("  [+] og-image.png (1200x630)")
    except Exception as e:
        print("  [!] OG image failed: {}".format(e))

    # favicon.ico
    try:
        from PIL import Image
        ico_sizes = [16, 32, 48]
        ico_images = []
        for s in ico_sizes:
            p = os.path.join(output_dir, "favicon-{}.png".format(s))
            if os.path.exists(p):
                ico_images.append(Image.open(p))
        if ico_images:
            ico_path = os.path.join(output_dir, "favicon.ico")
            ico_images[0].save(
                ico_path, format="ICO",
                sizes=[(img.width, img.height) for img in ico_images],
                append_images=ico_images[1:]
            )
            print("  [+] favicon.ico")
    except Exception as e:
        print("  [!] ICO generation failed: {}".format(e))

# --- Main ---

def generate_logo(name, style="modern", primary=None, accent=None, size=512, output_dir="./brand"):
    """Generate a logo SVG and save variants."""
    os.makedirs(output_dir, exist_ok=True)

    style_fn = STYLES.get(style, style_modern)
    kwargs = {"name": name, "size": size}
    if primary:
        kwargs["primary"] = primary
    if accent:
        kwargs["accent"] = accent

    svg_content = style_fn(**kwargs)

    out_path = os.path.join(output_dir, "logo-{}.svg".format(style))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("[+] Logo saved: {}".format(out_path))

    # Icon-only variant
    icon_svg = style_icon(name, primary=primary or "#3b82f6", size=size)
    icon_path = os.path.join(output_dir, "icon-only.svg")
    with open(icon_path, "w", encoding="utf-8") as f:
        f.write(icon_svg)
    print("[+] Icon saved: {}".format(icon_path))

    # Monogram variant
    mono_svg = style_monogram(name, primary=primary or "#6366f1", size=size)
    mono_path = os.path.join(output_dir, "monogram.svg")
    with open(mono_path, "w", encoding="utf-8") as f:
        f.write(mono_svg)
    print("[+] Monogram saved: {}".format(mono_path))

    return {"logo": out_path, "icon": icon_path, "monogram": mono_path}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SVG logos programmatically")
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument("--style", default="modern", choices=list(STYLES.keys()),
                        help="Logo style")
    parser.add_argument("--primary", help="Primary color (hex)")
    parser.add_argument("--accent", help="Accent color (hex)")
    parser.add_argument("--size", type=int, default=512, help="Output size in pixels")
    parser.add_argument("--output", default="./brand", help="Output directory")
    parser.add_argument("--brand-kit", action="store_true", help="Also generate PNGs, ICO, OG image")
    args = parser.parse_args()

    results = generate_logo(args.name, args.style, args.primary, args.accent, args.size, args.output)

    if args.brand_kit:
        print("\n[*] Generating brand kit...")
        generate_brand_kit(args.output, args.output)

    print("\n[Done] Files in {}/".format(args.output))
