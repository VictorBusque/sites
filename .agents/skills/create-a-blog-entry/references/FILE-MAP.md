# Site File Map

Repo: `Documents/sites` — living engineering notes as scrollytelling articles.
This map is the source of truth for what exists and what each file is allowed
to contain.

## Layout

```
sites/
├── index.html                  # Landing page (the only page at repo root)
├── css/
│   └── site.css                # SHARED design system — tokens, nav, footer,
│                               #   reveals, scene system, legacy figure system,
│                               #   responsive, reduced motion
├── js/
│   └── site.js                 # SHARED engine — progress bar, reveals, cursor,
│                               #   marquee, sticky-scene step activation,
│                               #   legacy figure engine (about.html only)
├── blog/
│   ├── template.html           # Working scrollytelling post + scene catalog
│   └── <slug>.html             # One article per file (the-queue.html, …)
├── about.html                  # Personal page — uses the LEGACY figure system
├── .agents/skills/create-a-blog-entry/
│   ├── SKILL.md
│   └── references/             # SCROLLYTELLING.md, DESIGN.md, MOTION.md
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
| `index.html` | Add/remove note entries and update copy | Delete the hero/manifesto/principles sections |
| `blog/<slug>.html` | Everything inside the page (styles, scripts, prose, scenes) | Duplicate shared system or hand-write scene wiring |
| `blog/template.html` | Keep it current as the catalog + starting point | Remove scene kinds or layout pieces it documents |
| `about.html` | Fix bugs in its inline figure logic | Convert it to scrollytelling — it intentionally keeps the legacy figure system (it documents how the author learns) |
| `mock*.html` | Nothing | Anything |

## Contracts with the shared files

- **`css/site.css` guarantees:** `.progress`, `.cursor-dot/ring`, `nav`,
  `.logo`, `.marquee`, `.reveal/.stagger/.mask/.h-line`, `.btn`, `.tag`,
  the scene system (`.scene`, `.sticky-scene`, `.scene-head`, `.step`,
  `.breather`, …), the legacy figure system (`.fig` frame, `.fig-btn`),
  `footer`, tokens, keyframes, responsive + reduced-motion blocks.
- **`js/site.js` guarantees:** fills `#progress`; observes `.reveal/.stagger/
  .mask`; duplicates `.marquee-track`; powers the custom cursor; for every
  `.sticky-scene` it observes `[data-step]` articles, toggles `.is-active`,
  sets `data-active-step` on the section, and fills `[data-readout]`; the
  legacy figure engine for `about.html`; responsive SVG framing
  (`data-vb-narrow`).
- **Pages must:** include both shared files, keep the fixed body elements,
  set the `<html class="js">` gate in `<head>`, add only page-scoped styles,
  and register page logic in an inline `<script>` before `</body>`.

## Scrollytelling vs legacy figures

Two visual systems coexist on purpose.

- **Blog posts** (`blog/*.html`) are scrollytelling articles: dark sticky
  stages, step cards, scroll-driven choreography. The shared scene engine
  handles step activation; pages key stage states off `data-active-step`.
- **about.html** keeps the legacy `.fig` system (fig-head, fig-body, engine
  PAUSE/REPLAY controls) because it is a personal "how I learn" page built
  around interactive figures. Do not port it, do not delete the figure
  system while about.html uses it.

Never mix the two on one page.

## Versioning the skill

The skill is versioned in its frontmatter (`metadata.version`). Bump the minor
version when standards change; bump the major when the file contract changes
(new shared file, breaking engine change). Update `SKILL.md`'s golden rules and
this map in the same change.
