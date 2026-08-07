# Figure Engine Reference

The engine lives in `js/site.js` (shared, do not edit). It discovers every
`.fig` element, builds controls into `.fig-controls`, and drives scripts
registered on `window.__figScripts`. Page scripts must register **before** the
engine runs — an inline `<script>` at the end of `<body>` (the engine loads
with `defer`, so this is guaranteed).

## The two figure kinds

| | Scripted | Looping |
| --- | --- | --- |
| Markup | `<div class="fig-body" data-script="name">` | `<div class="fig-body">` |
| Driver | `__figScripts.name.draw(i, body)` | pure CSS keyframes |
| Controls | PREV / PLAY / NEXT / RESET | PAUSE / REPLAY |
| Readout | string returned by `draw` | static text you write, or nothing |
| Use for | state with a sequence the reader must inspect | ambient scenes, background life |

## Script API

```js
__figScripts.name = {
  steps: 12,                          // frames 0..11
  draw: function (i, body) {          // required — render frame i
    var stage = body.querySelector('.my-stage');
    if (!stage._built) {              // build DOM once
      stage.innerHTML = '…';
      stage._built = true;
    }
    // mutate state per step
    return 'STEP ' + (i + 1) + ' / 12';   // optional; shown in .fig-readout
  },
  label: function (k) { return '…'; }     // optional; overrides default STEP n/total
};
```

Data attributes on `.fig-body`:

- `data-autoplay` — start playing when the figure first scrolls into view
  (ignored under `prefers-reduced-motion`).
- `data-loop` — wrap from the last step back to step 0.
- `data-speed="900"` — ms per step (default 950).

Controls note: `PREV` is disabled at step 0, `NEXT` is disabled at the last
step when `data-loop` is absent. `RESET` always returns to step 0. Never build
these buttons by hand.

## Contract for `draw`

1. **Idempotent.** The engine can render any step in any order (`render(0)`
   then `render(i+1)` then `render(3)`). Never increment a counter inside
   `draw`; recompute state from `i` every time, or precompute the whole
   sequence once at registration (guarded by an IIFE) and index into it.
2. **Build DOM once.** Guard construction with a flag on the stage element
   (`stage._built`). Subsequent calls only mutate classes, styles, text.
3. **Return a string** for the readout, or nothing. If the readout should
   differ from "STEP n / total", return it from `draw` directly (e.g. the
   algorithm's own decision text).
4. **Reset classes fully.** When a cell/bar can be in several states, set the
   base class first, then re-add the state classes, so stale states never
   survive a backwards step.

## Two reliable patterns

**Precomputed sequence** (preferred when steps have event text):

```js
(function () {
  var INPUT = [6, 3, 8, 2];
  var steps = [];
  (function sim() {
    var a = INPUT.slice();
    // …push one {a, scan, min, ev} object per comparison…
  })();
  __figScripts.my_sort = {
    steps: steps.length,
    draw: function (i, body) { /* render steps[i] */ return steps[i].ev; }
  };
})();
```

**Deterministic re-simulation** (when the timeline is regular):

```js
function runSim(ticks) {
  var q = 0, hist = [];
  for (var t = 0; t < ticks; t++) { /* … */ hist.push({ t: t, q: q }); }
  return hist;
}
__figScripts.queue = {
  steps: 30,
  draw: function (t, body) {
    var h = runSim(t + 1).pop();   // same input → same result, every replay
    // …render h…
    return 'T+' + t + ' — QUEUE ' + h.q;
  }
};
```

Re-simulation is only acceptable if it is deterministic (no `Math.random`, no
`Date.now`, no shared mutable state) — replay and stepping backward must be
exact.

## Shared CSS hooks

- `.fig-body` gives you the dark canvas, 32px grid, and the bottom-right
  decorative circle. Position page content with `position: absolute; inset: 0`
  on an inner stage, or flex/grid centering — never fight the canvas.
- `.fig-caption b` renders the orange "WHAT TO WATCH" kicker automatically.
- Pause/replay and reduced-motion are handled globally: the engine adds
  `is-paused` / `is-restarting` classes on the `.fig`; the shared stylesheet
  freezes animations. Do not add your own pause logic.

## Responsive framing

A full-bleed `<svg>` stage that is a scaled copy of the desktop scene looks
small on phones. The engine provides one hook — a tighter mobile frame — and
the page CSS provides the rest:

1. **Narrow frame.** Add `data-vb-narrow="minX minY w h"` to the `<svg>`.
   Below the 850px breakpoint the engine swaps the `viewBox` to this frame
   (reframed and zoomed, never shrunk) and restores it on resize. Choose the
   tightest frame that keeps every meaningful element inside.

   ```html
   <svg class="my-svg" viewBox="0 0 600 430" data-vb-narrow="85 66 420 290" …>
   ```

2. **Type bumps.** SVG text still scales with the canvas, so bump font sizes in
   the page's `@media (max-width: 850px)` block. Rendered size ≈ css font-size
   × (rendered svg width ÷ viewBox width); aim for ≥ 8px rendered. Override
   only `font-size` — positions stay in viewBox units.

3. **Free the width.** If a side rail (meter, legend, cost panel) shares the
   canvas, move it above or below the diagram on mobile so the SVG gets the
   full width. The shared breakpoint stacks grids already — do the same inside
   the figure.

4. **Match the canvas.** For a full-bleed SVG, set the fig-body to the frame's
   aspect ratio so there is no letterbox: `#myFig .fig-body { min-height: 0;
   aspect-ratio: 420 / 290; }` (page CSS, higher specificity wins over the
   shared 300px minimum).

HTML/CSS figures (cells, orbs) don't need frames — shrink fixed sizes in a
media query and let rows wrap. See `blog/template.html` for working examples
of both approaches.

## Verification

Run from the repo root with node:

```bash
node -e "
const fs=require('fs');
const s=fs.readFileSync('blog/<slug>.html','utf8');
const regs=[...s.matchAll(/__figScripts\.(\w+)\s*=/g)].map(m=>m[1]);
const attrs=[...s.matchAll(/data-script=\"(\w+)\"/g)].map(m=>m[1]);
console.log('registered:',regs,'used:',attrs);
console.log('missing on page:', regs.filter(r=>!attrs.includes(r)));
console.log('missing registration:', attrs.filter(a=>!regs.includes(a)));
"
```

And parse every inline script (a `<script>` without `src`):

```bash
node -e "
const fs=require('fs');
const s=fs.readFileSync('blog/<slug>.html','utf8');
[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{
  try{ new Function(m[1]); console.log('inline script',i+1,'OK'); }
  catch(e){ console.log('inline script',i+1,'FAIL:',e.message); }
});
"
```

Then open the page and check, by hand: controls appear on every figure, no
console errors, `data-autoplay` figures start on scroll into view, PREV works
backwards with no stale state, and `prefers-reduced-motion: reduce` renders
readable static content. Finally resize to 390px wide and check every figure
is legible (SVG labels ≥ 8px rendered), rails stacked, nothing overflowing.
