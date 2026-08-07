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
| `--paper-2` | `#ece9de` | secondary surfaces, fig head bars |
| `--acid` | `#c7ff3d` | the accent — highlights, found/ok states, selection |
| `--blue` | `#546cff` | secondary accent — scanning, in-flight, structure |
| `--orange` | `#ff6b2c` | attention — probes, candidates, warnings |
| `--muted` | `#716f68` | secondary text |
| `--line` | `#111111` | 1px rules |
| `--stage` | `#121212` | dark figure canvas (with `--grid #ffffff0d`) |

Semantic mapping on dark canvases: **acid** = found / settled / active flow,
**blue** = currently being examined, **orange** = the thing to watch right now
(probe, smallest-so-far, dropped item). Keep this mapping consistent across
posts — readers learn it once.

## Type

| Face | Role |
|---|---|
| Unbounded | display and headings (letter-spacing ~ `-.07em`, weights 400–600) |
| Instrument Serif | italic accents inside headlines, big ghost numerals, callouts |
| Newsreader | body text |
| DM Mono | labels, kickers, readouts, figure captions' kicker, meta |

Headline pattern: stacked `.h-line` masked lines, `clamp(46px, 7.5vw, 116px)`,
line-height ~ `.86`. One line per span; an `<em>` adds the serif accent.

## Layout

- **Nav:** fixed 70px, sticky, `#f2f0e9e8` + backdrop blur, logo left, links
  right (`.links a::after` underline scales from right), `.status` far right
  (`NOTE NN / TOPIC`).
- **Post hero:** `post-hero` — crumb (link back to `../index.html`), `h1` with
  `.h-line` spans, `.dek` (max 620px, fades up on load), `.post-meta`
  (`MON YEAR · ~N MIN · N FIGURES`), plus a `.ghost` numeral (`01`, `02`, …).
- **Prose column:** `.post-prose` — max 700px, centered. `h2` sections carry a
  small `.sec-no` (orange, DM Mono). `.callout` (serif italic, acid left
  border) holds the takeaway; `.aside` (DM Mono, muted) holds provenance.
- **Figures:** full-width, breaking the prose column, spaced `11vh` vertically.
- **Post nav:** two-column `post-nav` at the bottom, previous / next note.
- **Footer:** ink background, huge `footer-big` masked reveal, small mono
  `foot` line. Shared — copy it verbatim, change only the footer label.

## Reveal system (shared)

- `.reveal` / `.reveal.seen` — fade + rise on scroll (IntersectionObserver in
  `js/site.js`).
- `.stagger` — parent reveals children in sequence (delays ≤ 450ms).
- `.mask .row > span` — masked line reveal for quotes and big statements.
- `.h-line > span` — load-time masked line reveal for headlines.
- Never write your own scroll-triggered reveal; always reuse these classes.

## Dark figure canvases

The `.fig-body` from `css/site.css` provides the dark canvas, the 32px grid,
and the decorative bottom-right circle. Inside, follow the stage conventions:

- Nodes/cells: `1px` borders in `#ffffff2a–45`, text in `#888–ccc`,
  backgrounds `#121212` / `#1c1c1c`.
- A "current" element: accent border + soft glow (`box-shadow: 0 0 14px
  <accent>33`).
- A "consumed/past" element: opacity to `~.2` or dimmed border — never delete
  it from the layout (position stability matters).
- Always add a mono micro-label (9–10px, letter-spacing `.12–.16em`) so a
  figure is legible without the caption.

## Responsive

Shared breakpoints (in `css/site.css`): 850px collapses nav links/status,
stacks grids, shrinks `post-nav` to one column; the landing page stacks its
hero and card grids at 1050px. Keep new figure stages flexible: cell sizes in
`clamp` or percentages, labels that shrink, and figure bodies that accept
`min-height` reductions without clipping content.

Figures on narrow screens follow the same rule as the page grids: they
**reframe, they don't shrink**. Full-bleed SVG stages declare a tighter mobile
`viewBox` via `data-vb-narrow` (swapped by `js/site.js` below 850px), get
mobile font bumps in the page's media query (≥ 8px rendered), and a side rail
(meter, legend) moves above or below the diagram so the SVG keeps full width.
A full-bleed figure's `.fig-body` gets `aspect-ratio` set to the narrow frame
so the canvas matches it exactly. HTML/CSS figures shrink fixed cell sizes and
wrap rows in a media query. See `references/FIGURE-ENGINE.md` and
`blog/template.html` for working examples.

## Reduced motion

A global `@media (prefers-reduced-motion: reduce)` block in `css/site.css`
collapses all animation to near-instant and forces reveals visible. Do not
weaken or override it. It is the reason pages stay usable for every reader.
