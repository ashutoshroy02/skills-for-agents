#!/usr/bin/env python3
"""
favicon_generator.py - Convert any SVG/PNG image into a complete favicon package.
Generates all sizes, formats, and platform-specific icons.

Usage:
    python favicon_generator.py --input logo.svg --output ./brand/
    python favicon_generator.py --input icon.png --output ./brand/
    python favicon_generator.py --input logo.svg --output ./brand/ --html
"""

import argparse
import os
import sys
from pathlib import Path

# --- Favicon Sizes (industry standard) ---

FAVICON_SIZES = {
    "favicon-16.png": 16,
    "favicon-32.png": 32,
    "favicon-48.png": 48,
    "favicon-96.png": 96,
    "favicon-128.png": 128,
    "favicon-192.png": 192,
    "apple-touch-icon.png": 180,
    "android-chrome-192.png": 192,
    "android-chrome-512.png": 512,
    "mstile-150.png": 150,
}

SOCIAL_SIZES = {
    "og-image.png": (1200, 630),
    "twitter-card.png": (1200, 600),
    "github-preview.png": (1280, 640),
}

HTML_SNIPPET = """<!-- Favicon & App Icons -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#ffffff">

<!-- Open Graph -->
<meta property="og:image" content="/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/twitter-card.png">
"""

WEBMANIFEST_TEMPLATE = """{
  "name": "{name}",
  "short_name": "{short_name}",
  "icons": [
    {{ "src": "/android-chrome-192.png", "sizes": "192x192", "type": "image/png" }},
    {{ "src": "/android-chrome-512.png", "sizes": "512x512", "type": "image/png" }}
  ],
  "theme_color": "{theme_color}",
  "background_color": "{bg_color}",
  "display": "standalone"
}
"""


def load_source_image(input_path):
    """Load source image (SVG or raster). Returns PIL Image or None for SVG."""
    ext = Path(input_path).suffix.lower()

    if ext == ".svg":
        # For SVG, we'll convert via cairosvg
        try:
            import cairosvg
            # Convert SVG to large PNG first for processing
            png_data = cairosvg.svg2png(url=input_path, output_width=1024, output_height=1024)
            from PIL import Image
            import io
            return Image.open(io.BytesIO(png_data))
        except ImportError:
            print("[!] cairosvg not installed. Install with: pip install cairosvg")
            print("    Falling back to direct SVG copy.")
            return None

    # Raster image
    try:
        from PIL import Image
        img = Image.open(input_path)
        # Convert to RGBA for transparency support
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        return img
    except ImportError:
        print("[!] Pillow not installed. Install with: pip install Pillow")
        return None


def resize_image(img, size):
    """Resize image to target size with high-quality resampling."""
    from PIL import Image
    return img.resize((size, size), Image.LANCZOS)


def generate_ico(images, output_path):
    """Generate multi-size ICO file from list of PIL Images."""
    if not images:
        return False
    try:
        images[0].save(
            output_path, format="ICO",
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        return True
    except Exception as e:
        print("  [!] ICO failed: {}".format(e))
        return False


def generate_social_card(icon_img, width, height, bg_color="#ffffff", output_path=None):
    """Generate social media card with centered icon."""
    from PIL import Image
    card = Image.new("RGBA", (width, height), bg_color)
    # Icon takes up ~40% of the card height
    icon_size = int(height * 0.6)
    icon = resize_image(icon_img, icon_size)
    x = (width - icon_size) // 2
    y = (height - icon_size) // 2
    card.paste(icon, (x, y), icon if icon.mode == "RGBA" else None)
    if output_path:
        card.save(output_path, "PNG")
    return card


def generate_favicon_package(input_path, output_dir, name="My App", theme_color="#ffffff",
                             bg_color="#ffffff", generate_html=False):
    """Generate complete favicon package from a single source image."""
    os.makedirs(output_dir, exist_ok=True)

    # Copy SVG if source is SVG
    if input_path.lower().endswith(".svg"):
        import shutil
        svg_dest = os.path.join(output_dir, "favicon.svg")
        shutil.copy2(input_path, svg_dest)
        print("  [+] favicon.svg (copied)")

    # Load and process source image
    img = load_source_image(input_path)
    if img is None:
        print("[!] Could not load source image. Copying SVG only.")
        return

    # Generate all favicon sizes
    ico_images = []
    for filename, size in FAVICON_SIZES.items():
        resized = resize_image(img, size)
        out_path = os.path.join(output_dir, filename)
        resized.save(out_path, "PNG")
        print("  [+] {} ({}x{})".format(filename, size, size))
        if size in [16, 32, 48]:
            ico_images.append(resized)

    # Generate ICO
    ico_path = os.path.join(output_dir, "favicon.ico")
    if generate_ico(ico_images, ico_path):
        print("  [+] favicon.ico (multi-size)")

    # Generate social media cards
    for filename, (w, h) in SOCIAL_SIZES.items():
        out_path = os.path.join(output_dir, filename)
        generate_social_card(img, w, h, bg_color, out_path)
        print("  [+] {} ({}x{})".format(filename, w, h))

    # Generate WebP versions
    for size_name in ["favicon-32", "favicon-96", "android-chrome-512"]:
        png_path = os.path.join(output_dir, "{}.png".format(size_name))
        if os.path.exists(png_path):
            from PIL import Image
            webp_path = os.path.join(output_dir, "{}.webp".format(size_name))
            Image.open(png_path).save(webp_path, "WEBP", quality=90)
            print("  [+] {}.webp".format(size_name))

    # Generate web manifest
    short_name = name[:12]
    manifest = WEBMANIFEST_TEMPLATE.format(
        name=name, short_name=short_name,
        theme_color=theme_color, bg_color=bg_color
    )
    manifest_path = os.path.join(output_dir, "site.webmanifest")
    with open(manifest_path, "w") as f:
        f.write(manifest)
    print("  [+] site.webmanifest")

    # Generate HTML snippet
    if generate_html:
        html_path = os.path.join(output_dir, "favicon-tags.html")
        with open(html_path, "w") as f:
            f.write(HTML_SNIPPET)
        print("  [+] favicon-tags.html (copy into <head>)")

    # Summary
    total = len(FAVICON_SIZES) + len(SOCIAL_SIZES) + 3  # +ico, +webmanifest, +svg
    print("\n[Done] {} files generated in {}".format(total + 5, output_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate complete favicon package from a single image")
    parser.add_argument("--input", required=True, help="Source image (SVG, PNG, JPG)")
    parser.add_argument("--output", default="./brand", help="Output directory")
    parser.add_argument("--name", default="My App", help="App/site name for manifest")
    parser.add_argument("--theme-color", default="#ffffff", help="Theme color for PWA")
    parser.add_argument("--bg-color", default="#ffffff", help="Background color for social cards")
    parser.add_argument("--html", action="store_true", help="Generate HTML snippet file")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("[!] Input file not found: {}".format(args.input))
        sys.exit(1)

    generate_favicon_package(args.input, args.output, args.name, args.theme_color, args.bg_color, args.html)
