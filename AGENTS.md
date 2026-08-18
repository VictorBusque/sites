# Víctor Busqué Engineering Blog site

This is the project for Víctor Busqué (victorbusque.com) engineering blog site.

# Structure

This is the project for Víctor Busqué (victorbusque.com): a notebook of
curiosities ("documents"). One idea per document, told as a scroll-driven
page — each entry is something Víctor found curious. Engineering is the
core, not the boundary — any topic that deserves a slow walk can become a
document (AI and agents, systems, Python, cloud, craft, curiosity).

- Posts live at `blog/<slug>.html`, one idea each.
- Topics are free-form metadata on each entry (`topic` + `tags` in the
  `ENTRIES` list in `index.html`) — no fixed taxonomy, no folder tree.
- The idea queue lives in `docs/ideas.md`.

# Posts

Blog posts are scrollytelling articles (one idea, scroll-driven scenes). Follow
`.agents/skills/create-a-blog-entry` when writing or editing posts, the landing
page, or the shared css/js system. Follow `.agents/skills/seo` for anything
that affects how a page appears in search or social previews (titles, meta
descriptions, OG/Twitter cards, slugs, structured data, sitemap).

# Shared system (every article works the same)

The scrollytelling behavior is centralized in the shared modules so no article
hand-writes scene wiring:

- `css/site.css` — design system, scene styles, the mobile bottom-sheet step
  card, progress rail, reduced-motion fallback.
- `js/site.js` — shared chrome (nav, footer, progress, cursor, mobile menu),
  scroll reveals, marquee, legacy figure engine.
- `js/scene.js` — the sticky-scene module. Wraps `.step` content in
  `.step-card`, injects the `.step-progress` rail, toggles `.is-active`,
  sets `data-active-step`, fills `[data-readout]`, and measures
  `--card-reserve` so the mobile diagram centers above the bottom-docked
  card. Exposes `window.VBScene` (`.onStep(fn)`, `.refresh()`).
- `js/vb.js` — shared micro-helpers for page scripts on one namespace,
  `window.VB`: `VB.reduceMotion`, `VB.esc(str)`, `VB.mulberry32(seed)`,
  `VB.fmt.pct/ordinal/sup`, and `VB.motion.retrig/countUp`. Use these
  instead of re-implementing them per page.

Every page loads **all three** shared scripts (`js/site.js` and
`js/scene.js` with defer, in that order, then `js/vb.js` **without** defer
so the helpers exist before page scripts run) — write the scene markup
from `blog/template.html` and behavior is done. Do not add per-page scene
JS; page scripts only compute honest state and key stage visuals off
`data-active-step` (react via `window.VBScene.onStep(fn)`, never a
hand-rolled MutationObserver).
