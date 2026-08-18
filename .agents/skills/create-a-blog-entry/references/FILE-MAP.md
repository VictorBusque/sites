# Site File Map

Repo: `Documents/sites` — a notebook of curiosities, told as scroll-driven documents.
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
│   ├── site.js                 # SHARED — chrome, skip link, progress,
│   │                           #   motion preference, reveals, legacy figures
│   ├── scene.js                # SHARED scene module — sticky-scene step cards,
│   │                           #   labels, progress rail, data-active-step,
│   │                           #   mobile bottom-sheet layout (--card-reserve)
│   └── vb.js                   # SHARED micro-helpers for page scripts:
│                               #   window.VB — esc, mulberry32, fmt.*,
│                               #   motion.retrig/countUp, reduceMotion
├── blog/
│   ├── template.html           # Working scrollytelling post + scene catalog
│   └── <slug>.html             # One article per file (the-queue.html, …)
├── about.html                  # Personal page — uses the LEGACY figure system
├── .agents/skills/create-a-blog-entry/
│   ├── SKILL.md
│   └── references/             # SCROLLYTELLING.md, DESIGN.md, MOTION.md,
│                               #   PLATFORM.md
├── mock-1.html                 # Historical mockup — DO NOT TOUCH
├── mock.html                   # Historical mockup — DO NOT TOUCH
├── README.md                   # Personal notes
├── robots.txt
└── sitemap.xml                 # Public URLs; update real lastmod dates when pages change
```

## File ownership

| File | You may | You may not |
|---|---|---|
| `css/site.css` | Extend (new shared components, keyframes, tokens) | Restyle existing shared classes to fit one page |
| `js/site.js` | Fix bugs, add site-chrome features | Move it, break `defer` ordering, add page-specific logic |
| `js/scene.js` | Fix bugs, extend the scene contract | Split scene logic across pages; change the step-card contract without updating this map and the skill |
| `js/vb.js` | Fix bugs, add general-purpose helpers (esc, rng, fmt, motion) | Duplicate a helper into a page instead of using `window.VB`; add page-specific logic |
| `index.html` | Update landing copy and shelf presentation | Duplicate post data; it belongs in `js/posts.js` |
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
- **`js/site.js` guarantees:** embeds the shared components — the nav
  (`[data-vb-nav]`, knobs `data-active` / `data-status` / `data-status-em`),
  the footer (`[data-vb-footer]`, knob `data-label`), and the fixed chrome
  (`#progress`, `#cDot`, `#cRing`); fills `#progress`; observes `.reveal/.stagger/
  .mask`; duplicates `.marquee-track`; powers the custom cursor; adds a
  reader-facing skip link (when a semantic `<main>` exists) and a persisted
  ambient-motion pause control; powers the legacy figure engine; and handles
  responsive SVG framing (`data-vb-narrow`). Its reading-progress rail uses a
  native CSS scroll timeline when available and rAF otherwise.
- **`js/scene.js` guarantees:** for every `.sticky-scene` it wraps each
  `[data-step]`'s content in a `.step-card` (injecting a `.step-progress`
  rail and conventional `.step-k` label when missing), toggles `.is-active`
  as a step crosses its activation window, sets
  `data-active-step` on the section, fills `[data-readout]` with
  `STEP k / n`, and measures the tallest card into `--card-reserve` so the
  portrait bottom-sheet layout centers the diagram above the card. Public
  API: `window.VBScene.onStep(fn)` / `.refresh()` / `.init()`.
- **`js/vb.js` guarantees:** one namespace, `window.VB`, with the
  general-purpose helpers page scripts reach for — `VB.reduceMotion`,
  `VB.esc(str)` (HTML-escape computed text before `innerHTML`),
  `VB.mulberry32(seed)` (deterministic seeded PRNG), `VB.fmt.pct/ordinal/sup`
  (number formatters), `VB.motion.retrig(el, cls)` and
  `VB.motion.countUp(el, txt[, opts])` (animation choreography). Never
  re-implement these in a page.
- **Pages must:** include **all three** shared files (`js/site.js` then
  `js/scene.js`, both `defer`, in that order, then `js/vb.js` **without**
  defer so `window.VB` exists while page scripts parse), keep the
  component mounts (`[data-vb-nav]` / `[data-vb-footer]`, with their
  `<noscript>` fallbacks), set the `<html class="js">` gate in `<head>`,
  add only page-scoped styles, and register page logic in an inline
  `<script>` before `</body>`. To react to scene step changes, register with
  `window.VBScene.onStep(fn)` inside `VB.onReady(fn)` — never hand-roll a
  `MutationObserver` on `data-active-step`. Pages with a sticky scene make
  the stage decorative (`aria-hidden="true"`) and carry the conclusion in
  step text.

## Scrollytelling vs legacy figures

- All narrative pages (`index.html`, `about.html`, `blog/*.html`) are
  scrollytelling. The shared scene engine handles step activation; pages
  key stage states off `data-active-step`.
- The legacy `.fig` system (fig-head, fig-body, PAUSE/REPLAY controls) is
  kept in `css/site.css` / `js/site.js` for compatibility but is currently
  unused by any page. Do not start new work on it.

Never mix the two on one page.

## Versioning the skill

The skill is versioned in its frontmatter (`metadata.version`). Bump the minor
version when standards change; bump the major when the file contract changes
(new shared file, breaking engine change). Update `SKILL.md`'s golden rules and
this map in the same change.
