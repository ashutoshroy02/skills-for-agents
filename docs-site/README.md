# Skills for Agents — Documentation Site

VitePress documentation site for the Skills for Agents ecosystem.

## Design Philosophy

**Register:** Brand-leaning Product (distinctive but serves content)  
**Strategy:** Committed (30-60% color presence with wavy aesthetic)  
**Typography:** System fonts for performance and familiarity

### Visual Identity

**Wavy Aesthetic** — flowing, organic design language
- Animated wave patterns in hero section
- Smooth gradient transitions (purple-blue spectrum)
- Curved borders and elevated cards
- Scroll-linked progress indicators

### Key Decisions

1. **OKLCH colors** — vibrant purple-blue spectrum (280° hue)
2. **Committed color strategy** — 30-60% brand presence vs restrained 10%
3. **Animated waves** — SVG wave patterns with smooth motion
4. **Gradient accents** — linear gradients for buttons, links, borders
5. **Elevated cards** — transform + shadow on hover, wavy top border
6. **System font stack** — no web fonts, instant load
7. **Reduced motion support** — animations disabled for accessibility
8. **Touch targets ≥44px** — mobile-first interaction
9. **Skip link** — keyboard navigation support
10. **High contrast mode** — respects user preferences

## Quick Start

```bash
npm install
npm run docs:dev
```

Docs live at `http://localhost:5173/skills-for-agents/`

## Build

```bash
npm run docs:build
```

Output → `docs-site/.vitepress/dist`

## Deploy

GitHub Actions auto-deploys to GitHub Pages on push to main.

Live site: `https://isnoobgrammer.github.io/skills-for-agents/`

## Structure

```
docs-site/
├── .vitepress/
│   ├── config.ts          # VitePress config
│   ├── theme/
│   │   ├── index.ts       # Custom theme entry
│   │   └── custom.css     # Design tokens + polish
│   └── dist/              # Build output (gitignored)
├── guide/                 # Getting started guides
├── skills/                # Individual skill docs
├── reference/             # Deep-dive references
├── public/                # Static assets
│   └── logo.svg          # Site logo
├── index.md              # Landing page
└── 404.md                # Custom 404 page
```

## Accessibility

- WCAG AA compliant
- Keyboard navigation (skip link, focus rings)
- Reduced motion support
- High contrast mode support
- Touch targets ≥44px
- Semantic HTML
- Screen reader friendly

## Performance

- System fonts (no web font loading)
- Optimized CSS (~600 lines with wavy aesthetic)
- VitePress static generation
- Local search (no external dependencies)
- GPU-accelerated animations (transform + opacity only)
- SVG wave patterns (lightweight, scalable)

## Tech Stack

- **VitePress** — Vue-powered static site generator
- **Vue 3** — modern reactive framework
- **Vite** — lightning-fast dev server
- **GitHub Actions** — auto-deploy to GitHub Pages

## License

MIT

