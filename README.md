# sites — engineering.victorbusque.com

One curious idea per scroll-driven document. Engineering is the centre, not a
boundary: AI, systems, Python, cloud, craft — anything that benefits from a
slow, visual explanation.

## Architecture — hub and spokes

- **Hub:** `index.html` — a single, SEO-optimized landing page that owns the
  shared visual system (`css/site.css`, `js/site.js`, `js/scene.js`,
  `js/vb.js`) and renders the shelf of posts from the manifest.
  `about.html` shares the same system.
- **Spokes:** each article at `blog/<slug>.html` is a standalone,
  one-of-a-kind HTML file with its own inlined styles, scripts, and scene
  logic. The only shared components are the reading indicator
  (`../css/post-progress.css` + `../js/post-progress.js`) and the post
  navigator (`../css/post-nav.css` + `../js/post-nav.js`).
- **Binding:** `js/posts.js` (`window.VB_POSTS`) — the manifest linking
  articles to the landing. Titles, meta, canonicals, OG cards, and JSON-LD
  in each article must agree with its manifest row.

## Layout

    index.html          landing page
    about.html          about
    blog/*.html         published posts
    blog/not-ready/     parked works in progress (unlisted)
    blog/not-ready/template.html  post scaffold
    css/ js/            shared landing system + post chrome
    docs/ideas.md       new-idea queue
    topics/<topic>/     research (context.md) and story briefs (narrative.md)
    scripts/            quality-gate checks
    sitemap.xml robots.txt CNAME site.webmanifest

## Workflow

New pages flow from `topics/<topic>/context.md` → `narrative.md` →
standalone post, guided by the skills in `.agents/skills/`
(`create-a-narrative`, `create-a-blog-entry`, `seo`).

## Quality gates

```sh
python3 scripts/check_posts.py
node --check js/site.js
node --check js/scene.js
node --check js/vb.js
git diff --check
```

See `AGENTS.md` for the full craft contract: semantic documents first,
nothing faked, motion with meaning, reduced-motion support.
