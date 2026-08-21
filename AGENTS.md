# Víctor Busqué — A Notebook of Curiosities

This repository publishes `engineering.victorbusque.com`: one curious idea per
scroll-driven document. Engineering is the centre, not a boundary; topics can
include AI, systems, Python, cloud, craft, or anything that benefits from a
slow, visual explanation.

## Architecture — hub and spokes

- **The hub:** `index.html`, a single, fully featured, SEO-optimized landing
  page. It owns the shared visual system (`css/site.css`, `js/site.js`,
  `js/scene.js`, `js/vb.js`) and renders the shelf of posts from the
  manifest. `about.html` shares that system.
- **The spokes:** each article at `blog/<slug>.html` is a **standalone,
  one-of-a-kind HTML file**. It owns its styles, document, and scene logic;
  no article links `../css/` or `../js/` assets. The sole shared post chrome
  is the required top-edge reading indicator: `../css/post-progress.css` +
  `../js/post-progress.js` (or `../../` from `blog/not-ready/`), with
  per-post gradient parameters on `<body>`.
  Articles have no site navigation bar, masthead, or persistent post rail.
  Every other visual decision is free to diverge.
- **The binding:** articles are bound to the landing only through metadata —
  one object per post in `js/posts.js` (`window.VB_POSTS`). The landing reads
  the manifest and links each article; the article's own `<title>`,
  meta description, canonical, OG/Twitter cards, and `BlogPosting` JSON-LD
  must agree with its manifest row.

In short: the landing is the only page built from shared components; every
article is its own small website.

## Source of truth

- Landing page: `index.html` (+ `css/site.css`, `js/site.js`, `js/scene.js`,
  `js/vb.js` — landing/about chrome only).
- Published posts: `blog/<slug>.html` (top level), each owns its document and
  scene code; every one loads the shared relative `../css/post-progress.css`
  and `../js/post-progress.js` reading indicator.
- Parked works in progress: `blog/not-ready/` — redesigns waiting to ship.
  They are never in `js/posts.js`, never rendered on the shelf, absent from
  `sitemap.xml`, and disallowed in `robots.txt`.
- Post manifest (the only landing↔post binding): `js/posts.js`.
  Do not add post data to `index.html`; topics and tags remain free-form.
- New-idea queue: `docs/ideas.md`.
- Topic pipeline: `topics/<topic>/context.md` holds the research for one
  prospective article; `topics/<topic>/narrative.md` is its approved
  story-and-build brief. Topic material is private working material, never a
  landing-page data source or public URL. New pages flow from context →
  narrative → standalone post.
- Post scaffold: `blog/not-ready/template.html` — a complete standalone
  article with a working base stylesheet, runtime, and scene catalog inlined.

## Required guidance

Use `.agents/skills/create-a-narrative/SKILL.md` to turn a topic's
`context.md` into its `narrative.md` build brief. Use
`.agents/skills/create-a-blog-entry/SKILL.md` plus the `scrollytelling` skill
to turn a ready narrative into a post, and for any post, landing-page, or
shared-system change. Use `.agents/skills/seo/SKILL.md` for every public page
change that may affect search or social metadata. Keep these instructions and
their references accurate when changing a shared contract.

## Craft contract (applies to every article, standalone or not)

- A post is a semantic document first: it must read as a complete article
  with JavaScript off and under reduced motion. Sticky-scene stages are
  decorative (`aria-hidden="true"`); step paragraphs carry the conclusions
  in document order.
- Nothing is faked: every readout, count, or number is computed state or a
  verified fact.
- Motion has meaning, honors `prefers-reduced-motion`, and never hides the
  conclusion.
- The template's inlined runtime (`VBScene`, `window.VB`) is a proven starting
  point, not a requirement — an article may replace any of it, but it must
  keep the honest-document behavior above. The shared reading indicator is
  the exception: keep the relative `../css/post-progress.css` and
  `../js/post-progress.js` references.

## Quality gates

After a content or contract change, run the relevant checks. The post checker
verifies the manifest binding, public metadata, sitemap, required shared
reading indicator, standalone-ness (no shared `../css/` or `../js/` assets
except the required reading indicator), and the sticky-scene honesty rules:

```sh
python3 scripts/check_posts.py
node --check js/site.js
node --check js/scene.js
node --check js/vb.js
git diff --check
```

Unlisted or in-progress articles in `blog/` carry `<meta name="robots"
content="noindex, nofollow">`; works in progress parked in
`blog/not-ready/` are invisible to the checker, and drafts registered in
`js/posts.js` with `"status": "wip"` stay off the shelf until they ship.

Verify narrow mobile layout, keyboard navigation, and reduced motion whenever
layout or interaction changes. Do not attempt browser screenshots in this
repository.
