# Scrollytelling Reference

How posts work on this site: the scene vocabulary, the scene runtime that
the scaffold inlines into every post, progressive enhancement, responsive
and reduced-motion rules, and how to validate a finished article. The craft
(storyboarding, choreography, accessibility) lives in the Atelier
**scrollytelling** skill in the pi-extensions repo — read it before writing
a scene. This file is the site-specific application.

## Storyboard (before code)

Use the act progression and per-section questions from the Atelier skill
(also summarized in `SKILL.md`). One proven rhythm for engineering ideas:

```text
ACT 0  Hook — the question, stated plainly (hero)
ACT 1  Mental model — the simplest true picture (split scene)
ACT 2  Mechanism — the pieces and how they connect (sticky scene)
ACT 3  Critical detail — zoom into the one subtle thing (sticky scene)
ACT 4  Change perspective — the same idea from another angle (comparison)
ACT 5  Stress it — simulate, compare, or push the system (metrics/simulation)
ACT 6  Synthesize — the takeaway as prose, not motion
ACT 7  Final line (closing / footer-adjacent)
```

For every scene decide: question, model before → after, visual anchor, scroll
mechanic, payoff, static fallback. Vary the rhythm; keep the article readable
as a document.

## Scene vocabulary

All classes below come from the base stylesheet the scaffold inlines (each
page owns its copy) unless marked (page).

### sticky-scene — the workhorse

A tall track (`n` × 100svh) with a
pinned dark stage; step cards scroll over it. The stage is the visual; the
steps carry the narrative in DOM order. On mobile the step text is a rounded
bottom sheet with a progress rail; the scene runtime (inlined by the
scaffold) handles all of it.

```html
<section class="sticky-scene" data-scene>
  <div class="sticky-scene__stage" aria-hidden="true">
    <div class="scene-head">
      <span class="scene-no">ACT 02</span>
      <span class="scene-name">THE MECHANISM</span>
      <span class="scene-readout" data-readout></span>
    </div>
    <div class="stage">
      <!-- the diagram: inline SVG or DOM nodes -->
    </div>
  </div>

  <div class="sticky-scene__steps">
    <article class="step" data-step="1">
      <p>One short paragraph. Real text, real conclusion.</p>
    </article>
    <article class="step" data-step="2"><!-- … --></article>
    <!-- one article per state of the diagram -->
  </div>
</section>
```

Runtime contract (inlined by the scaffold — keep it intact unless the
article deliberately replaces it, preserving the fallbacks):

- Each `.step` with `[data-step]` is wrapped in a `.step-card` (with a
  `.step-progress` rail and conventional `.step-k` label injected), gets
  `.is-active` while it crosses its
  activation window; the section's `data-active-step` is set to the current
  step number; `[data-readout]` receives `STEP k / n`.
- Style the *text cards* with `.step.is-active` (show/hide/position).
- Style the *stage states* with attribute selectors:
  `.sticky-scene[data-active-step="2"] .marker { … }`. Each step number is
  one named state of the diagram — never arbitrary pixels.
- Steps should be 2–6 per scene. Fewer than 2 and the scene is a plain
  figure; more than 6 and the track feels endless.

Progressive enhancement for the overlay:

- The template sets `<html class="js">` in `<head>`. The overlay layout
  (negative-margin steps, dimmed cards) exists only under `.js`.
- Without JS: the stage renders as a plain block and the steps stack below it
  — a complete, readable article.
- Without IntersectionObserver: the module removes the `.js` enhancement gate
  and preserves that same plain-document state.
- Under `prefers-reduced-motion: reduce`: the same stacked-document layout
  (see the reduced-motion block of the base styles). Do not rely on the overlay there.

### scene / split — copy beside a bounded visual

```html
<section class="scene split">
  <div class="scene__copy">
    <h2><span class="sec-no">02</span>The mental model</h2>
    <p>…</p>
  </div>
  <div class="scene__visual">
    <!-- a bounded diagram, max ~520px; no sticky -->
  </div>
</section>
```

Collapses to vertical order below 850px (base stylesheet). Use for establishing
scenes where the visual is small and the prose does the work.

### comparison — before/after or A/B

Two states of the same thing. Label both sides with mono kickers, keep the
same composition so the difference reads instantly. A `.is-switched` class
(one button, optional) or scroll-linked reveal both work; if the comparison is
essential, show both states side by side in the DOM — never only on hover.

### metrics-scene — a number with evidence

A large Instrument Serif numeral with the mechanism that produced it drawn
beside it. The number must be computed state (real counts, real sums) — see
Golden rule 2 in `SKILL.md`.

### breather — the quiet beat

A centered Instrument Serif line, a masked quote (`.mask`), or a full-width
rule. No diagram. Place one after dense scenes so the next idea lands.

### full-bleed (page)

A cinematic visual that breaks the prose column. Wide SVG stages: declare
`data-vb-narrow="minX minY w h"` and the inlined runtime swaps the viewBox below
850px (reframed, never shrunken), plus a mobile font bump in the page's media
query (labels ≥ 8px rendered).

## Progressive enhancement ladder

From the Atelier skill — start at the bottom, climb only as needed:

```text
HTML        semantic story and static fallback
CSS         layout, visual system, simple motion
CSS timelines  scroll-linked opacity/transform/rotation (progressive)
IntersectionObserver  discrete step activation (scaffold runtime)
requestAnimationFrame custom continuous state or Canvas
Canvas/WebGL genuinely spatial or high-density explanation
```

### CSS scroll timelines (optional, feature-detected)

Use for continuous, subtle scroll-linked effects (a marker easing along a
path, a bar filling). Feature-detect and keep the base state meaningful:

```css
@supports (animation-timeline: view()) {
  .stage .path-progress {
    animation: fill 1s linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 40%;
  }
}
/* outside @supports the element simply sits at its base state */
```

Never put essential conclusions in a scroll-timeline-only animation — they are
decoration over the step story.

### Scene runtime (IntersectionObserver) — inlined by the scaffold

Already inlined in every post from `blog/template.html` (the page owns its
copy). For every `.sticky-scene` it:

- wraps each `[data-step]`'s content in a `.step-card` and injects a
  `.step-progress` rail plus a conventional label when one is not authored;
- toggles `.is-active` on the crossing `[data-step]` and sets
  `data-active-step` on the section (pages key stage states off it);
- fills `[data-readout]` with `STEP k / n`;
- measures the tallest card into `--card-reserve` on the stage so the
  portrait layout centers the diagram above the bottom-docked card.

Public API for page scripts: `window.VBScene.onStep(fn)` — called as
`fn(sceneEl, stepEl, index, total)` when a step becomes active — plus
`.refresh()` and `.init()`. Page
scripts only:

- compute honest state (probe sequences, counts, timings) at build time and
  write it into the DOM as labels;
- nothing else, unless the scene needs rAF or Canvas (below).

### requestAnimationFrame / Canvas

Only for genuinely continuous state (a live simulation, an animated queue).
Rules: never heavy work in a `scroll` handler (rAF-throttle or IO), map scroll
into named states, pause when offscreen, cap DPR (`Math.min(devicePixelRatio,
1.75)`), bound particle counts, and keep the conclusion in DOM text nearby.
Prefer CSS/IO unless the extra machinery clearly buys comprehension.

## Motion rules for scenes

- Choreograph each scene `ENTER → HOLD → TRANSFORM → RESOLVE → EXIT`; no
  instant A→B jumps unless the contrast is the point.
- The story must survive fast scrolling, scrollbar jumps, and reverse
  scrolling: every intermediate state is a real state.
- Step-card transitions: opacity + `translateY` (never position alone),
  600–900ms, `--ease-out` entering. Inactive cards rest dimmed.
- Stage-state transitions: 150–300ms for the primary element, `--ease-swift`;
  a supporting pulse or glow lands with it (`pop`, `ping` keyframes are
  shared).
- One hero element per scene. Anticipation before movement. Settling echo
  after a found/settled state.
- Keep semantic color mapping: acid = found/settled/active, blue =
  examining/structure, orange = the thing to watch.

## Responsive

- Sticky stages stay sticky on mobile; shrink heights with `svh` and keep the
  diagram centered, labels ≥ 8px rendered.
- On portrait phones the step text becomes a **bottom sheet** (from the base
  stylesheet): a rounded, docked card capped at `44vh` (scrolls if its
  text is long) with a progress rail. Each step owns one `100svh` viewport,
  so the card boots at the bottom and has a stable reading interval. The scene module exposes
  `--card-reserve` on the stage so the diagram centers in the space above the
  card and never runs underneath. Choreography is animation-then-text: the
  diagram state changes, the outgoing sheet clears, then after a beat the
  sheet rises with the label before the paragraph — and it reverses on scroll
  up.
- Keep step paragraphs to one or two sentences.
- Split scenes stack: copy above visual.
- Full-bleed SVGs reframe via `data-vb-narrow` (see above).
- Verify at 320–390px: no clipping, no horizontal scroll, sticky elements
  don't cover nav.

## Reduced motion

The reduced-motion block in each page's base styles collapses durations and, for scenes,
restores document flow (stage static, steps stacked, all text visible). Do
not weaken it. If a scene's *meaning* depends on a diagram state, ensure the
step text states the conclusion — it always should.

The inlined chrome also exposes `Motion: on/off`, which pauses ambient
loops without changing the reader-controlled scroll states. Do not add a
second pause button inside a normal scene.

## Validation

Run these checks before delivery:

1. `grep -n "http://\|https://\|@import" blog/<slug>.html` — only the font
   preconnect and `og:image` URLs may appear; no CDN scripts, no `fetch()`.
2. Extract and syntax-check inline scripts with `node --check`.
3. Confirm every `.sticky-scene` has 2–6 sequential `[data-step]` children,
   an `aria-hidden` stage, readable paragraph fallback text, and stage states
   use `[data-active-step="N"]` selectors that exist in the HTML.
4. Confirm the page reads top to bottom with JS disabled (temporarily remove
   the `js` class / engine) and under reduced motion: stage + stacked steps,
   every paragraph visible.
5. No duplicate IDs, SVG diagrams titled/described or `aria-hidden` with
   adjacent DOM text, controls keyboard-operable with visible focus.
6. Mobile pass at 390px; desktop pass with a quick scroll to the end.

Then answer the Atelier delivery questions: would it still be beautiful if
motion stopped? Can a reader understand after scrolling too quickly? Does the
visual clarify more than prose alone? Does it feel like one editorial piece?
