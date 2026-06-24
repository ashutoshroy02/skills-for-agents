<div class="domain-header">
  <span class="skill-badge craft">Craft</span>
  <span style="color: var(--ink-muted); font-size: var(--text-sm);">Composable &middot; Yields to: Process</span>
</div>

# Logo & Favicon

Find, generate, or create logos, favicons, and SVGs for any project — by any means necessary, before bothering the user about style.

## When to Use

- A project needs a logo, favicon, app icon, or OG image
- User mentions "new project" or "deploying" — every project needs a face
- You need brand assets and want the cheapest viable source first

## Triggers

```
"logo", "favicon", "icon", "brand kit", "SVG", "app icon", "og image"
"make me a logo", "need a favicon", "brand identity", "website icon"
```

## How It Works

A cascading strategy — exhaust the cheap options before the expensive ones:

1. **Search the web** for existing official assets (the project may already have a logo).
2. **Scrape free logo sites** for usable marks.
3. **Generate SVGs programmatically** with Python — wordmarks, monograms, geometric icons.
4. **AI image generation** only as a last resort.

Style questions come *after* the free resources are exhausted, not before.

## Examples

<div class="example-box">
<div class="example-label">Example 1</div>
<div class="example-title">Favicon for a new project</div>
<div class="example-desc">Get a favicon set without a design tool.</div>

```
"I need a favicon for my CLI tool 'ripgrep-tui'."

The agent checks for an existing mark, then generates a monogram SVG
and exports the favicon sizes (16, 32, 180, 512) — no AI calls needed.
```
</div>

<div class="example-box">
<div class="example-label">Example 2</div>
<div class="example-title">Brand kit before deploy</div>
<div class="example-desc">Logo + OG image ahead of a launch.</div>

```
"Deploying tonight — I have no logo or social card."

The agent produces an SVG wordmark, derives the favicon set, and
builds an OG image, escalating to AI generation only if a richer
illustration is genuinely required.
```
</div>
