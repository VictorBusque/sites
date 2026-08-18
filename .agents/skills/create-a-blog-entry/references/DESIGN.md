# Design Reference

Single source of truth for how the site looks. All tokens, base styles,
navigation, footer and reveal mechanics live in `css/site.css` — never
duplicate or restyle them. Pages may only **add** page-specific styles in an
inline `<style>` block.

## Tokens (css/site.css, `:root`)

| Token | Value | Use |
|---|---|---|
| `--ink` | `#101010` | text, borders, dark fills |
| `--paper` | `#f2f0e9` | page background |
| `--paper-2` | `#ece9de` | secondary surfaces, scene-head bars |
| `--acid` | `#c7ff3d` | the accent — highlights, found/ok states, selection |
| `--blue` | `#546cff` | secondary accent — scanning, in-flight, structure |
| `--orange` | `#ff6b2c` | attention — the thing to watch right now |
| `--muted` | `#716f68` | secondary text |
| `--line` | `#111111` | 1px rules |
| `--stage` | `#121212` | dark scene canvas (with `--grid #ffffff0d`) |

Semantic mapping on dark canvases: **acid** = found / settled / active flow,
**blue** = currently being examined, **orange** = the thing to watch right now
(probe, smallest-so-far, dropped item). Keep this mapping consistent across
articles — readers learn it once.

## Type

| Face | Role |
|---|---|
| Unbounded | display and headings (letter-spacing ~ `-.07em`, weights 400–600) |
| Instrument Serif | italic accents inside headlines, big ghost numerals, callouts, metrics numerals |
| Newsreader | body text |
| DM Mono | labels, kickers, readouts, step numbers, captions' kicker, meta |

Headline pattern: stacked `.h-line` masked lines, `clamp(46px, 7.5vw, 116px)`,
line-height ~ `.86`. One line per span; an `<em>` adds the serif accent.

## Layout

- **Nav + footer (embedded):** rendered by `js/site.js` into mount points —
  `<div data-vb-nav data-active="…" data-status="…" data-status-em="…">`
  and `<div data-vb-footer data-label="…">`, each with a `<noscript>`
  fallback row. Links are root-relative. Never hand-write them.
- **Nav:** fixed 70px, sticky, `#f2f0e9e8` + backdrop blur, logo left, links
  right (`.links a::after` underline scales from right), `.status` far right
  (`POST NN / TOPIC`).
- **Post hero:** `post-hero` — crumb (link back to `../index.html`), `h1` with
  `.h-line` spans, `.dek` (max 620px, fades up on load), `.post-meta`
  (`MON YEAR · ~N MIN · N SCENES`), plus a `.ghost` numeral (`01`, `02`, …).
- **Prose column:** `.post-prose` — max 700px, centered. `h2` sections carry a
  small `.sec-no` (orange, DM Mono). `.callout` (serif italic, acid left
  border) holds the takeaway; `.aside` (DM Mono, muted) holds provenance.
- **Scenes:** full-width, breaking the prose column. Sticky scenes are the
  workhorse — see below.
- **Post nav:** two-column `post-nav` at the bottom, previous / next post.
- **Footer (embedded):** ink background, huge `footer-big` masked reveal,
  small mono `foot` line. Rendered by the engine from `[data-vb-footer]` —
  change the label on the mount, never the markup.

## Reveal system (shared)

- `.reveal` / `.reveal.seen` — fade + rise on scroll (IntersectionObserver in
  `js/site.js`).
- `.stagger` — parent reveals children in sequence (delays ≤ 450ms).
- `.mask .row > span` — masked line reveal for quotes and big statements.
- `.h-line > span` — load-time masked line reveal for headlines.
- Never write your own scroll-triggered reveal; always reuse these classes.

## Dark scene canvases

The `.sticky-scene__stage` from `css/site.css` provides the dark canvas, the
32px grid, and the decorative bottom-right circle. Inside, follow the stage
conventions:

- Nodes/cells: `1px` borders in `#ffffff2a–45`, text in `#888–ccc`,
  backgrounds `#121212` / `#1c1c1c`.
- A "current" element: accent border + soft glow (`box-shadow: 0 0 14px
  <accent>33`).
- A "consumed/past" element: opacity to `~.2` or dimmed border — never delete
  it from the layout (position stability matters).
- Always add a mono micro-label (9–10px, letter-spacing `.12–.16em`) so a
  stage is legible without the caption.

### Sticky scenes

```text
<section class="sticky-scene">          tall track = n × 100svh (desktop)
  .sticky-scene__stage                  pinned (position: sticky, top 0, 100svh)
    .scene-head                         ACT NN / NAME / live STEP k / n readout
    .stage                              the diagram
  .sticky-scene__steps                  overlays the stage (only under .js)
    article.step[data-step]             card: STEP k / n label + 1 short ¶
```

- The scene module `js/scene.js` wraps each `.step` in a `.step-card`
  (injecting a `.step-progress` rail) and toggles `.is-active`; it sets
  `data-active-step` and fills the `[data-readout]`.
- Step cards: paper background, ink border, mono `step-k` label, one short
  paragraph (1–2 sentences). On portrait phones the card becomes a rounded
  bottom sheet (capped `44vh`, scrollable) and steps pace at `64svh`; the
  module measures `--card-reserve` so the diagram centers above it. Inactive
  cards rest dimmed; the active sheet rises in after a beat (animation-
then-text, reverses on scroll up).
- Stage states key off `data-active-step` attribute selectors, e.g.
  `.sticky-scene[data-active-step="2"] .marker { … }`.
- Without JS or under reduced motion the overlay collapses: the stage is a
  plain block and the steps stack below it — still a complete article.

### Non-sticky scenes

- `.scene.split` — copy and a bounded visual side by side, stacked below
  850px.
- `.comparison` — two labeled states of the same composition.
- `.metrics-scene` — a large Instrument Serif numeral with the mechanism that
  produced it beside it.
- `.breather` — a quiet beat: a centered serif line or masked quote, no
  diagram.

## Responsive

Shared breakpoints (in `css/site.css`): 850px collapses nav links/status,
stacks grids, shrinks `post-nav` to one column; the landing page stacks its
hero and card grids at 1050px.

Scenes on narrow screens follow the same rule as the page grids: they
**reframe, they don't shrink**. Sticky stages keep their track but use `svh`
and centered compositions; full-bleed SVG stages declare a tighter mobile
`viewBox` via `data-vb-narrow` (swapped by `js/site.js` below 850px) and get
mobile font bumps in the page's media query (≥ 8px rendered). Step cards go
full-width with generous padding. See `references/SCROLLYTELLING.md` and
`blog/template.html` for working examples.

## Reduced motion

A global `@media (prefers-reduced-motion: reduce)` block in `css/site.css`
collapses all animation to near-instant, forces reveals visible, and restores
document flow for sticky scenes (stage static, steps stacked, all text
visible). Do not weaken or override it. It is the reason pages stay usable for
every reader.

## Legacy figure system

`about.html` keeps the older `.fig` frame (fig-head, fig-body, engine
PAUSE/REPLAY controls). The styles remain in `css/site.css` and the engine in
`js/site.js`. Blog posts never use it. See `references/FILE-MAP.md`.
