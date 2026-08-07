# Site File Map

Repo: `Documents/sites` — living engineering notes. This map is the source of
truth for what exists and what each file is allowed to contain.

## Layout

```
sites/
├── index.html                  # Landing page (the only page at repo root)
├── css/
│   └── site.css                # SHARED design system — tokens, nav, footer,
│                               #   reveals, figure frame, responsive, reduced motion
├── js/
│   └── site.js                 # SHARED engine — progress bar, reveals, cursor,
│                               #   marquee, figure engine (controls + playback)
├── blog/
│   ├── template.html           # The mock/catalog + canonical starting point
│   └── <slug>.html             # One post per file (order.html, the-line.html, …)
├── .agents/skills/create-a-blog-entry/
│   ├── SKILL.md
│   └── references/             # FIGURE-ENGINE.md, DESIGN.md, MOTION.md
├── mock-1.html                 # Historical mockup — DO NOT TOUCH
├── mock.html                   # Historical mockup — DO NOT TOUCH
├── README.md                   # Personal notes
├── robots.txt
└── sitemap.xml                 # Stale (points at engineering.victorbusque.com)
```

## File ownership

| File | You may | You may not |
|---|---|---|
| `css/site.css` | Extend (new shared components, keyframes, tokens) | Restyle existing shared classes to fit one page |
| `js/site.js` | Fix bugs, add engine features | Move it, break `defer` ordering, add page-specific logic |
| `index.html` | Add/remove note cards, update copy | Delete the hero/manifesto/principles sections |
| `blog/<slug>.html` | Everything inside the page (styles, scripts, prose) | Duplicate shared system or hand-write figure controls |
| `blog/template.html` | Keep it current as the catalog + starting point | Remove figure kinds or layout pieces it documents |
| `mock*.html` | Nothing | Anything |

## Contracts with the shared files

- **`css/site.css` guarantees:** `.progress`, `.cursor-dot/ring`, `nav`,
  `.logo`, `.marquee`, `.reveal/.stagger/.mask/.h-line`, `.btn`, `.tag`,
  `.fig` frame (`.fig-head/.fig-body/.fig-caption/.fig-btn`), `footer`,
  tokens, keyframes, responsive + reduced-motion blocks.
- **`js/site.js` guarantees:** fills `#progress`; observes `.reveal/.stagger/
  .mask`; duplicates `.marquee-track`; powers the custom cursor; for every
  `.fig` it fills `.fig-controls`, reads `data-script`/`data-autoplay`/
  `data-loop`/`data-speed`, and calls registered `__figScripts` draws.
- **Pages must:** include both shared files, keep the fixed body elements,
  register scripts in an inline `<script>` before `</body>`, and add only
  page-scoped styles.

## Versioning the skill

The skill is versioned in its frontmatter (`metadata.version`). Bump the minor
version when standards change; bump the major when the file contract changes
(new shared file, breaking engine change). Update `SKILL.md`'s golden rules and
this map in the same change.
