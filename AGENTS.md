# Víctor Busqué — A Notebook of Curiosities

This repository publishes `victorbusque.com`: one curious idea per
scroll-driven document. Engineering is the centre, not a boundary; topics can
include AI, systems, Python, cloud, craft, or anything that benefits from a
slow, visual explanation.

## Source of truth

- Published posts: `blog/<slug>.html` (one idea per file).
- Post manifest and landing-shelf data: `js/posts.js` (`window.VB_POSTS`).
  Do not add post data to `index.html`; topics and tags remain free-form.
- New-idea queue: `docs/ideas.md`.
- Shared visual and interaction system: `css/site.css`, `js/site.js`,
  `js/scene.js`, and `js/vb.js`.
- The canonical post scaffold: `blog/template.html`.

## Required guidance

Use `.agents/skills/create-a-blog-entry/SKILL.md` for any post, landing-page,
or shared-system change. Use `.agents/skills/seo/SKILL.md` for every public
page change that may affect search or social metadata. Keep those instructions
and their references accurate when changing a shared contract.

## Shared-system contract

- Pages load `js/site.js`, then `js/scene.js`, both with `defer`; load
  `js/vb.js` without `defer` before page scripts. Use the relative paths from
  `blog/template.html` for posts.
- Shared nav/footer are mounts (`[data-vb-nav]`, `[data-vb-footer]`) rendered
  by `js/site.js`. Keep their `<noscript>` fallback; do not hand-copy chrome.
- `js/scene.js` owns sticky-scene activation, cards, progress rails, and
  `data-active-step`; it also supplies conventional step labels when omitted.
  Page scripts may compute honest state and subscribe with `VBScene.onStep`;
  never add a competing `MutationObserver` or scroll handler.
- `js/site.js` owns reading progress, the keyboard skip link, responsive
  navigation, and the reader's ambient-motion pause preference. Do not copy
  those controls into a post.
- A sticky stage is decorative (`aria-hidden="true"`); its step paragraphs
  carry the complete conclusion in document order. The modules fall back to
  that document if JavaScript or IntersectionObserver is unavailable.
- `js/vb.js` owns reusable helpers on `window.VB`. Reuse them instead of
  copying escaping, formatting, PRNG, or motion helpers into pages.
- New page styles are page-scoped. Change shared CSS only for a behaviour that
  genuinely belongs to every document. Never edit `mock.html` or `mock-1.html`.

## Quality gates

After a content or shared-system change, run the relevant checks. The post
checker verifies the manifest, public metadata, sitemap, shared shell, and
sticky-scene contract:

```sh
python3 scripts/check_posts.py
node --check js/site.js
node --check js/scene.js
node --check js/vb.js
git diff --check
```

Verify narrow mobile layout, keyboard navigation, and reduced motion whenever
layout or interaction changes. Do not attempt browser screenshots in this
repository.
