# AI Logo Generation Prompts

> Copy-paste these into ChatGPT (DALL-E 3), Gemini (Imagen), or Midjourney.
> Replace `[BRACKETS]` with your project details.

---

## ChatGPT / DALL-E 3 Prompts

### Minimal Tech Logo
```
Design a minimal, modern logo for a software project called "[NAME]".

Style: Clean geometric shapes, flat design, no gradients.
Colors: [PRIMARY] and [ACCENT] on white background.
The logo should work at 16x16 pixels (favicon) and scale up to 512x512.
Include: the first letter of the project name in a geometric shape.
Avoid: 3D effects, shadows, photorealism, complex illustrations.

Output: Simple SVG-style vector graphic, centered, with padding.
```

### App Icon
```
Create a mobile app icon for "[NAME]", a [DESCRIPTION] app.

Requirements:
- Square with rounded corners (iOS style, 20% corner radius)
- Simple, recognizable symbol — not text
- Colors: [PRIMARY] background with [ACCENT] symbol
- Must be legible at 60x60 pixels
- Flat design, no gradients, no shadows
- Single focal point in the center

Style reference: Apple's built-in app icons — clean, bold, iconic.
```

### GitHub/Developer Logo
```
Design a logo for a GitHub organization/repo called "[NAME]".

Style: Developer-friendly, slightly technical feel.
Use: Monospace typography, geometric shapes, dark theme.
Colors: [DARK_BG] with [NEON_ACCENT] (think terminal/hacker aesthetic).
Include: The project initials in a hexagonal or rounded-square badge.
The logo should look good in GitHub README headers and as a repo avatar.

No: gradients, 3D effects, cartoon characters, overly complex designs.
```

### Monogram/Initials
```
Create an elegant monogram logo using the initials "[INITIALS]".

Style: [MODERN/CLASSIC/PLAYFUL]
The letters should interlock or overlap artistically.
Colors: [PRIMARY] on transparent/white background.
The monogram should be enclosed in a [CIRCLE/HEXAGON/SHIELD/NONE].
Make it work as a favicon (16px) and profile picture (512px).

Avoid: Decorative flourishes that disappear at small sizes.
```

---

## Gemini / Imagen Prompts

### Clean Vector Logo
```
Generate a clean vector-style logo icon for "[NAME]".

Design specifications:
- Shape: [CIRCLE/HEXAGON/ROUNDED SQUARE] badge
- Symbol: [DESCRIBE SYMBOL - e.g., "stylized owl", "abstract rocket", "circuit pattern"]
- Colors: [PRIMARY] and [ACCENT], maximum 2 colors
- Style: Flat, geometric, minimal detail
- Background: Solid [COLOR] or transparent
- Must be recognizable at 16x16 pixels

The logo should feel [PROFESSIONAL/PLAYFUL/BOLD/ELEGANT] and work for a [TYPE] project.
```

### Favicon Set
```
Create a set of favicon icons for a website called "[NAME]".

Generate these variants:
1. 16x16: Ultra-simple, just the essential shape
2. 32x32: Slightly more detail, clear symbol
3. 180x180: Full icon with subtle details
4. 512x512: Complete icon, all details visible

All should be the same design, just at different detail levels.
Colors: [PRIMARY] and [ACCENT].
Style: Flat, modern, no text, single recognizable symbol.
Background: [COLOR] solid.
```

---

## Midjourney Prompts

### Stylized Logo
```
minimal logo design for "[NAME]", [STYLE] style, vector art,
flat colors [PRIMARY] and [ACCENT], centered composition,
white background, scalable vector graphic style,
professional branding, simple geometric shapes
--no text, shadows, gradients, 3d effects
--ar 1:1 --s 250 --v 6
```

### App Icon
```
mobile app icon for "[NAME]", flat design, minimal,
[SYMBOL_DESCRIPTION] centered on [PRIMARY] background,
rounded square shape, iOS app icon style,
bold colors, clean lines, professional
--no text, noise, texture, photorealism
--ar 1:1 --s 200 --v 6
```

---

## Prompt Engineering Tips

### For Logos
- **Specify "flat design"** — prevents 3D/photorealistic output
- **Say "no text"** — AI text rendering is unreliable; add text in post-processing
- **Name specific colors** — "indigo (#4f46e5)" > "blue"
- **Reference icon styles** — "like Apple's Settings icon" or "like a GitHub Octicon"
- **Set pixel targets** — "must be legible at 16x16" forces simplicity

### For Favicons
- **Demand simplicity** — "single shape, maximum 2 colors"
- **Test mentally** — "would this be recognizable as a 16px square in a browser tab?"
- **Avoid fine detail** — thin lines, small text, and gradients disappear at small sizes

### For Brand Kits
- **Ask for variants** — "light version, dark version, monochrome version"
- **Specify platform sizes** — "1200x630 for Open Graph, 1280x640 for GitHub"
- **Request SVG** — "output as clean SVG code, not rasterized"

---

## Post-Processing After AI Generation

1. **Vectorize** the output using:
   - `potrace` (CLI) — bitmap to vector
   - `vtracer` (CLI, Rust) — better quality, `cargo install vtracer`
   - Online: vectorizer.io, svgmaker.io

2. **Clean up** the SVG:
   - Remove unnecessary paths and metadata
   - Simplify paths with SVGO: `svgo input.svg -o output.svg`
   - Convert text to paths (so fonts aren't needed)

3. **Generate favicon set**:
   ```bash
   python scripts/favicon_generator.py --input logo.svg --output brand/ --html
   ```

4. **Verify at small sizes** — open favicon-16.png and check it's recognizable
