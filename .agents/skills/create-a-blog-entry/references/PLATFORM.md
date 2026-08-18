# Platform defaults for scrollytelling

This site treats a scrollytelling article as a **semantic document first** and
a visual guided experience second. The shared modules own the expensive,
repeated behavior; a post owns its truthful prose and named visual states.

## Decisions baked into the shared system

| Default | Why it belongs in the module | Platform basis |
|---|---|---|
| DOM-ordered step paragraphs and a decorative `aria-hidden` stage | The article remains understandable with JavaScript off, reduced motion, assistive technology, or a failed enhancement. | [W3C accessibility principles](https://www.w3.org/WAI/fundamentals/accessibility-principles/) |
| IntersectionObserver activates discrete steps | Visibility changes are asynchronous and avoid bespoke scroll loops per article. The module falls back to document flow if the API is absent. | [MDN: Intersection Observer](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) |
| CSS scroll timeline for the reading rail, rAF fallback elsewhere | Browsers that support it can drive the non-essential rail directly from scroll; readers in other browsers see the same rail through the fallback. | [MDN: scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations) |
| `transform` + `opacity` for cards and reveals | These are the safest default animation properties for smooth composition. Do not animate layout properties to make a scene feel active. | [web.dev: animation performance](https://web.dev/articles/animations-and-performance) |
| Reduced-motion document flow plus `Motion: on/off` | System preference is respected, and readers can pause ambient loops that run beside content. Scroll-controlled states remain tied to the reader's own input. | [W3C: reduced motion](https://www.w3.org/WAI/WCAG22/Techniques/css/C39), [W3C: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) |
| One viewport per mobile step, with final-stage reserve | A card begins bottom-docked, has a stable reading interval, and cannot escape into the next prose section. | Site regression proof; implemented in `css/site.css` and `js/scene.js` |

## Authoring implication

For a normal sticky scene, the post provides only:

```html
<section class="sticky-scene">
  <div class="sticky-scene__stage" aria-hidden="true">
    <div class="scene-head">
      <span class="scene-no">ACT 02</span>
      <span class="scene-name">THE MECHANISM</span>
      <span class="scene-readout" data-readout></span>
    </div>
    <div class="stage"><!-- named visual states --></div>
  </div>
  <div class="sticky-scene__steps">
    <article class="step" data-step="1"><p>Meaning in plain text.</p></article>
    <article class="step" data-step="2"><p>The next true state.</p></article>
  </div>
</section>
```

The shared module provides the card, conventional step label, progress rail,
activation, bottom sheet, and fallback. A page must not add a scroll listener,
progress control, or step observer for this scene.

## Non-negotiable review questions

1. Does each step change the reader's mental model, not just the picture?
2. Can a reader understand the conclusion from the prose alone?
3. Does reverse scrolling land on real, named states?
4. Does the diagram still fit above the mobile card at 390px?
5. Is any ambient movement useful enough to deserve its motion budget?

`scripts/check_posts.py` enforces the structural parts. The content and visual
questions remain an author review, because code cannot judge whether a story is
honest or clear.
