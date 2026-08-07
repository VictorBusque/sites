---
name: create-a-blog-entry
description: >
  Creates new blog entries for the living-engineering-notes site in this repo
  (landing page index.html + posts at blog/<slug>.html that teach ideas through
  animated figures). Use whenever writing a new post, adding or editing
  figures, touching the shared design system (css/site.css) or the figure
  engine (js/site.js), or updating the landing page's note cards. Enforces the
  site's voice, design tokens, motion standards and figure conventions so every
  agent produces consistent, polished pages.
metadata:
  author: Víctor Busqué
  version: "1.0.0"
  site: living-engineering-notes
---

# Create a Blog Entry

Every post on this site teaches **one idea through diagrams that move**. The
reader steps through the process; nothing is faked. This skill is the single
source of truth for how posts are built, how figures are wired, and how the
site must look and behave.

## Golden rules (never break)

1. **Every figure runs the real process.** Counters in readouts are computed
   state, never decoration. If a figure claims "8 probes", the code produced 8.
   If you cannot compute it honestly, say something vaguer or don't say it.
2. **The diagram is the article.** Figures sit at the center of the story.
   Prose tells the reader _what to watch_, not what to conclude.
3. **Motion has meaning.** Nothing moves just to look cool. See
   [references/MOTION.md](references/MOTION.md).
4. **Polished, no AI slop.** No "systems online" metaphors, no hacker/nerd
   slang, no emoji, no invented stats, no filler adjectives. Plain,
   confident, precise prose.
5. **Use the shared system.** Never redefine tokens, fonts, nav, footer or
   reveal mechanics — they live in `css/site.css`. Never hand-write figure
   controls — the engine in `js/site.js` builds them.
6. **Never touch `mock-1.html` / `mock.html`.** They are historical mockups,
   not part of the site.

Full file ownership and contracts: [references/FILE-MAP.md](references/FILE-MAP.md).

## Workflow

### 1. Copy the template

```bash
cp blog/template.html blog/<slug>.html
```

`blog/template.html` is a working mock that is also a catalog: scripted
figures, looping figures, autoplay, and every layout piece. It is the canonical
starting point and is kept current — always copy from it.

`<slug>`: lowercase, hyphenated, one idea per note (e.g. `order.html`,
`the-line.html`, `fingerprint.html`).

### 2. Edit the new file only

Replace in order: `<title>` → hero (`crumb`, `h1`, `dek`, `post-meta`) →
prose sections → figures → `post-nav` links → footer label. Update the `status`
in `<nav>` (e.g. `NOTE 03 / WAITING`).

Shared pieces that must stay **exactly as in the template**:

- `<link rel="stylesheet" href="../css/site.css">` in `<head>`
- `<script src="../js/site.js" defer></script>` in `<head>`
- The four fixed elements: `#progress`, `#cDot`, `#cRing`, `<nav>`
- `post-hero`, `post-prose`, `post-nav`, `footer` structure and classes
- The inline `<script>` block **at the end of `<body>`** that registers
  figure scripts (see why below)
- The motion defaults: `--ease-*` and `--t-*` variables, `.reveal` /
  `.stagger` / `.mask` / `.h-line` reveal classes

**Script order is a hard rule:** the shared engine loads with `defer`; inline
scripts run during parsing. Therefore figure registrations **must** go in an
inline `<script>` before `</body>` — never after the engine tag, never in a
module.

### 3. Add figures

Two kinds, both with automatic controls (see
[references/FIGURE-ENGINE.md](references/FIGURE-ENGINE.md) for the full API):

- **Scripted** (`data-script="name"`): a `__figScripts.name = { steps, draw }`
  object. Engine adds PREV / PLAY / NEXT / RESET. `draw(i, body)` returns a
  string shown in the readout.
- **Looping** (no `data-script`): pure CSS keyframes. Engine adds
  PAUSE / REPLAY.

Figure markup contract:

```html
<figure class="fig">
  <div class="fig-head">
    <span class="fig-no">FIG. 01</span>
    <span class="fig-name">UPPERCASE TITLE</span>
    <span class="fig-readout"></span>
    <!-- optional, engine fills it -->
    <div class="fig-controls"></div>
    <!-- engine fills it — never hand-write buttons -->
  </div>
  <div
    class="fig-body"
    data-script="my_script"
    data-autoplay
    data-loop
    data-speed="900"
  >
    <div class="my-stage"></div>
  </div>
  <figcaption class="fig-caption"><b>What to watch</b> …</figcaption>
</figure>
```

Page-specific figure styles (the `.my-stage` / `.w-*` / `.b-*` blocks) go in
the page's inline `<style>` — that keeps `css/site.css` shared and stable.

Full-bleed `<svg>` stages: add `data-vb-narrow="minX minY w h"` and the mobile
type bumps in the page's media query so the figure reframes instead of
shrinking (see [references/FIGURE-ENGINE.md](references/FIGURE-ENGINE.md#responsive-framing)).
HTML/CSS stages: shrink fixed sizes / wrap rows in a media query — the
template's walker and search race are working examples.

### 4. Register the story on the landing page

Add a card to `index.html`'s `#notes` section, following the existing cards:

```html
<a class="story reveal" data-fig="04" href="blog/slug.html">
  <div class="story-copy">
    <span class="num">NOTE 04 / TOPIC</span>
    <h3>Short, concrete title.</h3>
    <p>
      One or two sentences that promise the figure: what the reader will watch.
    </p>
    <div class="tags">
      <span class="tag">Tag</span><span class="tag">Tag</span>
    </div>
    <span class="read">Read the note</span>
  </div>
  <div class="stage">
    <div class="stage-label">PREVIEW / <b>LABEL</b></div>
    <!-- a small looping preview + its keyframes, also in index's inline <style> -->
  </div>
</a>
```

`data-fig` numbers are the card's ordinal (01, 02, …) — keep them sequential.
Card previews must be lightweight loops that hint at the post's hero figure.
When the first real note lands, **remove the template card** and its preview
styles; the template card is scaffolding, not content.

### 5. Verify (run the checklist)

See [Checklist](#checklist). Always run the syntax and wiring checks in
[references/FIGURE-ENGINE.md](references/FIGURE-ENGINE.md#verification) before
handing a post over.

## Content conventions

- **Numbering:** figures are `FIG. 01` upward per post. `FIG. 00` is reserved
  for the landing hero demo.
- **Captions** always open with `<b>What to watch</b>` and tell the reader
  exactly which element moves and what it means. Max ~2 sentences.
- **Sections:** `<h2>` with `<span class="sec-no">NN</span>`. Section headings
  are concrete, not cute ("The problem", "Selection sort, step by step").
- **Callouts** (`.callout`) hold the one takeaway. **Asides** (`.aside`) hold
  provenance ("Both counts are computed by the same code that renders them").
- **Tone:** teach, don't perform. No "under the hood", "hack", "nerd",
  "powerful", "seamless", "seamlessly", "delve", "in today's world", emoji,
  or exclamation marks in copy. Numbers are exact or not stated.
- **Post meta** (`.post-meta`): `MON YEAR · ~N MIN · N FIGURES`. Reading time
  = words/200 rounded.

## Design system (quick reference)

Full reference: [references/DESIGN.md](references/DESIGN.md).

- Tokens live in `css/site.css`: `--ink #101010`, `--paper #f2f0e9`,
  `--paper-2 #ece9de`, `--acid #c7ff3d`, `--blue #546cff`, `--orange #ff6b2c`,
  `--muted #716f68`, `--line #111`.
- Type: Unbounded (display/headings), Instrument Serif (italic accents and
  big numerals), Work Sans (body), DM Mono (labels/readouts).
- Dark figure canvases use `--stage #121212` with the 32px grid from the
  shared `.fig-body` — never invent a new stage background.
- Page-specific styles may only add to this system (new keyframes for figures
  and previews); they may not restyle shared classes.

## Motion standards (quick reference)

Full reference: [references/MOTION.md](references/MOTION.md).

- Entrance = decelerate (`--ease-out`), exit = accelerate (`--ease-in`),
  on-screen = `--ease-swift`, ambient loops = seamless sine in/out.
- Never `linear` easing for spatial movement (spinners/progress bars excepted).
- Always three motion layers: primary action, secondary support, ambient life.
- No single motion travels more than 1/3 of the canvas; stagger budgets stay
  under 500ms; hover < 100ms, press < 150ms.
- Loop periods 2.5–4s for ambient; scripted figures 500–1300ms per step.
- `prefers-reduced-motion` is handled globally — never disable that block.

## Checklist

- [ ] Copied `blog/template.html`; shared files untouched
- [ ] All relative paths correct: `../index.html`, `../css/site.css`, `../js/site.js`
- [ ] Every `__figScripts.<name>` matches a `data-script="<name>"` on the page
      (and nothing references a script that isn't defined)
- [ ] `draw(i, body)` is idempotent: `render(0)` then `render(n)` must both be
      correct — the engine replays arbitrary steps, including backwards
- [ ] Every readout/caption number is computed state, verified by re-running
      the logic in your head or a REPL
- [ ] Inline scripts parse (`node --check` equivalent); page has no console
      errors; `data-autoplay` figures start only when visible
- [ ] Landing card added, `data-fig` sequential, template card removed once a
      real note exists
- [ ] Mobile check at 390px: every figure legible (SVG labels ≥ 8px rendered),
      rails stacked, nothing clips or overflows
- [ ] Copy follows the tone rules; no fake stats, no slang, no emoji
- [ ] `prefers-reduced-motion: reduce` still renders readable content
