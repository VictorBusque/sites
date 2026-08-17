---
name: create-a-blog-entry
description: >
  Creates new scrollytelling articles for the engineering blog in this repo
  (landing page index.html + posts at blog/<slug>.html that teach one idea as a
  scroll-driven narrative). Use whenever writing a new post, adding or editing
  scenes, touching the shared design system (css/site.css), the shared engine
  (js/site.js), or updating the landing page's cards and copy. Enforces the
  site's voice, design tokens, motion standards and scrollytelling conventions
  so every agent produces consistent, polished pages.
metadata:
  author: Víctor Busqué
  version: "2.0.0"
  site: living-engineering-notes
---

# Create a Scrollytelling Blog Entry

Every post on this site is a **scrollytelling article**: one idea, told as a
guided visual experience. Scrolling is the reader's timeline — scenes pin a
visual while step-by-step text scrolls over it, diagrams transform as you
travel, and the story has a beginning, middle, and end. The reader steps
through the process; nothing is faked.

This skill is the site-specific application of the **scrollytelling skill**
(Atelier, in the pi-extensions repo). That skill is the craft source of truth
for storyboarding, scene design, progressive enhancement, and validation; this
file adds the site's contracts: shared system, voice, and landing page wiring.

## The one deliberate deviation

The Atelier skill's output contract says "one self-contained `.html` file, no
linked local asset". **Posts on this site deliberately override that rule**:
they live inside the victorbusque.com site, link `css/site.css` and
`js/site.js` (shared tokens, nav, footer, fonts, reveals, scene engine), and
are not standalone artifacts. Everything else in that skill — story first,
scenes, scroll choreography, accessibility, mobile, performance, validation —
applies in full. State this trade-off in code comments, don't silently break
it.

## Golden rules (never break)

1. **The story is the article.** Every scene advances the mental model. If a
   scene doesn't change what the reader understands, cut it. Prose tells the
   reader *what is happening and why it matters* — never just decorates.
2. **Nothing is faked.** Every readout, count, or number is computed state or
   a real, verified fact. If a scene claims "8 probes", the algorithm really
   made 8. If you cannot compute it honestly, say something vaguer or don't
   say it.
3. **Motion has meaning.** Nothing moves just to look cool. Every major
   animation exists to make a state change obvious. See
   [references/MOTION.md](references/MOTION.md) and the scrollytelling skill.
4. **Polished, no AI slop.** No "systems online" metaphors, no hacker/nerd
   slang, no emoji, no invented stats, no filler adjectives. Plain,
   confident, precise prose.
5. **Use the shared system.** Never redefine tokens, fonts, nav, footer or
   reveal mechanics — they live in `css/site.css`. Never hand-write scene
   wiring — the engine in `js/site.js` handles step activation. Page-specific
   styles add to the system, they never restyle it.
6. **Never touch `mock-1.html` / `mock.html`.** They are historical mockups,
   not part of the site.

Full file ownership and contracts: [references/FILE-MAP.md](references/FILE-MAP.md).
Scene engine and recipes: [references/SCROLLYTELLING.md](references/SCROLLYTELLING.md).

## Workflow

### 1. Storyboard before writing a line

Create a compact internal storyboard using the Atelier progression:

```text
ACT 0 — Hook
ACT 1 — Establish the mental model
ACT 2 — Reveal the mechanism
ACT 3 — Zoom into the critical detail
ACT 4 — Change perspective
ACT 5 — Simulate, compare, or stress the system
ACT 6 — Synthesize
ACT 7 — Final takeaway
```

Not every story needs every act, but every page needs a progression. For each
section decide:

```text
Question:            what the reader is trying to understand
Reader should know:  the mental model before → after
Visual anchor:       the one thing the eye follows
Scroll mechanic:     what scroll does to the visual
Narrative payoff:    what this section hands the reader
Static fallback:     how the idea survives no-JS / reduced-motion
```

Vary the rhythm — `quiet → reveal → dense → quiet → dramatic → technical →
quiet`. Never make every section equally tall, animated, or loud. Your story
is valid only when it works as a document too: readable prose in DOM order
with the conclusion written out, not hidden in motion.

### 2. Copy the template

```bash
cp blog/template.html blog/<slug>.html
```

`blog/template.html` is a working scrollytelling post that doubles as a
catalog: a sticky scene with a transforming diagram, split and comparison
scenes, a metrics scene, a breather, and every prose piece. It is the
canonical starting point and is kept current — always copy from it.

`<slug>`: lowercase, hyphenated, one idea per article (e.g. `the-queue.html`,
`token-budget.html`, `kv-cache.html`).

### 3. Edit the new file only

Replace in order: `<title>` and meta → hero (`crumb`, `h1`, `dek`,
`post-meta`) → acts (prose sections + scenes) → `post-nav` links → footer
label. Update the `status` in `<nav>` (e.g. `NOTE 03 / WAITING`).

Shared pieces that must stay **exactly as in the template**:

- `<link rel="stylesheet" href="../css/site.css">` in `<head>`
- `<script src="../js/site.js" defer></script>` in `<head>`
- The `<html class="js">` gate script in `<head>` (set before the body parses
  — see the template; without it scenes degrade to a plain document)
- The four fixed elements: `#progress`, `#cDot`, `#cRing`, `<nav>`
- `post-hero`, `post-prose`, `post-nav`, `footer` structure and classes
- The motion defaults: `--ease-*` and `--t-*` variables, `.reveal` /
  `.stagger` / `.mask` / `.h-line` reveal classes

Script order is a hard rule: the shared engine loads with `defer`; inline
scripts run during parsing. Page-specific scene logic goes in an inline
`<script>` before `</body>` — never after the engine tag, never in a module.

### 4. Build the document first, then enhance

Write the headings, prose, captions, and diagrams as static HTML/SVG before
adding any motion. Then enhance in this order (from the Atelier skill):

```text
HTML        semantic story and static fallback
CSS         layout, visual system, simple motion
CSS timelines  progressive, continuous scroll-linked enhancement (@supports)
IntersectionObserver  discrete step activation (done by js/site.js)
requestAnimationFrame custom continuous state or Canvas drawing
Canvas/WebGL genuinely spatial or high-density visual explanation
```

The shared engine in `js/site.js` already provides the IntersectionObserver
step activation for sticky scenes. Page scripts only do what the shared engine
can't: compute honest state and drive per-step stage states via
`data-active-step` CSS hooks.

### 5. Register the story on the landing page

Add one entry to the `ENTRIES` array in `index.html` (find it under "Real
entries only"):

```js
{
    slug: 'blog/<slug>.html', title: 'Short, concrete title.',
    deck: 'One or two sentences that promise the experience: what the reader will scroll through and understand.',
    date: 'YYYY-MM', path: 'Topic/Category', tags: ['Tag', 'Tag']
}
```

The entry appears automatically in both the IDE explorer tree and the Latest
index — the row and the file are the same object. `slug` must match the file,
`path` must match a leaf in `TAXONOMY` (see [AGENTS.md](../../../AGENTS.md)).
No entry may point at a file that doesn't exist, and no file may be missing
its entry. Update the site's framing copy (hero demo labels, marquee items)
only if the site's promise changes.

### 6. Verify (run the checklist)

See [Checklist](#checklist) and the validation section in
[references/SCROLLYTELLING.md](references/SCROLLYTELLING.md#validation) before
handing an article over.

## Content conventions

- **Sections:** `<h2>` with `<span class="sec-no">NN</span>` inside
  `post-prose`. Section headings are concrete, not cute ("The problem",
  "Selection sort, step by step").
- **Scenes:** each scene gets a `scene-head` with an act label (e.g.
  `ACT 02`) and a concrete name (e.g. `THE MECHANISM`). Step cards carry a
  mono `STEP k / n` label — author it by hand, it never lies.
- **Captions** (`.fig-caption` and scene captions) open with `<b>What to
  watch</b>` and tell the reader exactly which element moves and what it
  means. Max ~2 sentences.
- **Callouts** (`.callout`) hold the one takeaway. **Asides** (`.aside`) hold
  provenance ("Both counts are computed by the code that renders them").
- **Tone:** teach, don't perform. No "under the hood", "hack", "nerd",
  "powerful", "seamless", "seamlessly", "delve", "in today's world", emoji,
  or exclamation marks in copy. Numbers are exact or not stated.
- **Post meta** (`.post-meta`): `MON YEAR · ~N MIN · N SCENES`. Reading time
  = words/200 rounded.

## Scene vocabulary (quick reference)

Full recipes: [references/SCROLLYTELLING.md](references/SCROLLYTELLING.md).

- `sticky-scene` — a tall scroll track with a pinned dark stage; step cards
  scroll over it. The workhorse of the site.
- `scene` / `split` — a narrative moment; copy and a bounded visual side by
  side (stacked on mobile).
- `full-bleed` — a cinematic visual with restrained overlay text.
- `comparison` — before/after or A/B transformation.
- `metrics-scene` — a large number with visible evidence.
- `breather` — a low-information beat between demanding ideas (a big serif
  line, a quote).

Reuse the shared classes from `css/site.css` (`scene`, `sticky-scene`,
`scene-head`, `step`, …) and add page-specific styles (diagram choreography,
keyframes) in the page's inline `<style>`. Dark stages use `--stage` with the
32px grid, exactly like the legacy figure canvases — never invent a new stage
background.

## Design system (quick reference)

Full reference: [references/DESIGN.md](references/DESIGN.md).

- Tokens live in `css/site.css`: `--ink #101010`, `--paper #f2f0e9`,
  `--paper-2 #ece9de`, `--acid #c7ff3d`, `--blue #546cff`, `--orange #ff6b2c`,
  `--muted #716f68`, `--line #111`.
- Type: Unbounded (display/headings), Instrument Serif (italic accents and
  big numerals), Newsreader (body), DM Mono (labels/readouts).
- Semantic color on dark stages: **acid** = found / settled / active flow,
  **blue** = currently being examined / structure, **orange** = the thing to
  watch right now. Keep this mapping consistent across posts — readers learn
  it once.
- Sticky stages: `position: sticky; top: 0; height: 100svh`, `--stage`
  background + grid, decorative bottom-right circle, `scene-head` bar.
- Step cards: paper background, ink border, 420px max width, mono `STEP k / n`
  label, one short paragraph.

## Motion standards (quick reference)

Full reference: [references/MOTION.md](references/MOTION.md).

- Entrance = decelerate (`--ease-out`), exit = accelerate (`--ease-in`),
  on-screen = `--ease-swift`, ambient loops = seamless sine in/out.
- Never `linear` easing for spatial movement (spinners/progress bars excepted).
- Always three motion layers per scene: primary action, secondary support,
  ambient life.
- No single element travels more than 1/3 of the stage before a keyframe
  change; no more than 1/3 of the elements in active motion at once.
- Step-state transitions 600–900ms; ambient loops 2.5–4s; entrance reveals
  800–1100ms; hover < 100ms, press < 150ms.
- Every scene must make sense at any scroll position: intermediate and
  reverse states are real states, critical conclusions exist in the DOM text,
  and the scene is intelligible if the reader jumps via the scrollbar.
- `prefers-reduced-motion: reduce` is handled globally — the overlay collapses
  to a plain stacked document. Never disable that block.

## Checklist

- [ ] Storyboarded (acts + per-section question/payoff) before coding
- [ ] Copied `blog/template.html`; shared files untouched
- [ ] `<html class="js">` gate present in `<head>`; relative paths correct:
      `../index.html`, `../css/site.css`, `../js/site.js`
- [ ] Document-first: the page reads as a complete article with JS disabled
      and with reduced motion (stage + stacked steps, all text visible)
- [ ] Every `sticky-scene` uses the shared engine contract: `[data-step]`
      articles, stage states keyed off `data-active-step`, `[data-readout]`
      if a live step indicator is wanted
- [ ] Every readout/caption number is computed state or a verified fact,
      re-checked by running the logic (REPL) or citing the source
- [ ] Inline scripts parse (`node --check` equivalent); page has no console
      errors; no duplicate IDs; SVG diagrams have `<title>`/`<desc>` or are
      `aria-hidden` with the conclusion in adjacent DOM text
- [ ] Scroll-timeline enhancements sit inside `@supports (animation-timeline:
      view())` and have a working discrete fallback
- [ ] No network requests beyond the site's own fonts and `og:image`;
      no CDN, no remote script, no `fetch()`
- [ ] Landing `ENTRIES` entry added with a slug that matches the file; no
      stale rows; explorer and Latest show the new note
- [ ] Mobile check at 390px: sticky stage fits (labels ≥ 8px rendered), step
      cards legible, lanes/rails stack, nothing clips or overflows
- [ ] Copy follows the tone rules; no fake stats, no slang, no emoji
