# Site File Map

Repo: `Documents/sites` — a notebook of curiosities: one landing page plus
standalone, one-of-a-kind scroll-driven articles. This map is the source of
truth for what exists and what each file is allowed to contain.

## Layout

```
sites/
├── index.html                  # THE HUB — landing page, fully featured,
│                               #   SEO-optimized; renders the shelf from
│                               #   js/posts.js; owns the shared system below
├── css/
│   └── site.css                # Landing/about design system — tokens, nav,
│                               #   footer, reveals, scene system, responsive,
│                               #   reduced motion. ARTICLES NEVER LINK IT.
├── js/
│   ├── site.js                 # Landing/about chrome: nav/footer mounts,
│   │                           #   progress, cursor, reveals, motion pause
│   ├── scene.js                # Landing scene module (sticky scenes on the
│   │                           #   landing). Posts inline their own copy.
│   ├── vb.js                   # Micro-helpers (window.VB) for landing page
│   │                           #   scripts. Posts inline their own copy.
│   └── posts.js                # THE BINDING — single post manifest
│                               #   (window.VB_POSTS) read by index.html
├── blog/
│   ├── <slug>.html             # One standalone article per file — its own
│   │                           #   styles, scripts, and chrome, inlined.
│   │                           #   Top level = published, rendered on shelf
│   └── not-ready/              # Parked WIP redesigns — never in the
│                               #   manifest, shelf, sitemap, or robots;
│                               #   includes template.html (the scaffold)
├── about.html                  # Personal page — landing system + legacy figures
├── .agents/skills/create-a-blog-entry/
│   ├── SKILL.md
│   └── references/             # SCROLLYTELLING.md, DESIGN.md, MOTION.md,
│                               #   PLATFORM.md
├── docs/ideas.md               # New-idea queue
├── README.md                   # Personal notes
├── robots.txt                  # Disallows /blog/template.html only
├── sitemap.xml                 # Public URLs; update real lastmod dates when pages change
└── scripts/check_posts.py      # Enforces the manifest + standalone contract
```

## File ownership

| File | You may | You may not |
|---|---|---|
| `index.html` | Update landing copy and shelf presentation | Duplicate post data; it belongs in `js/posts.js` |
| `css/site.css`, `js/site.js`, `js/scene.js`, `js/vb.js` | Extend/fix the landing system | Point a blog article at any of them |
| `js/posts.js` | Add/update manifest rows when posts ship | Invent rows without files, or stash post data anywhere else |
| `blog/<slug>.html` | Everything — the whole file is the article's own: styles, scripts, chrome, prose, scenes | Link `../css/` or `../js/` assets; depend on any file outside `blog/` (except `/img/` static assets and external fonts) |
| `blog/not-ready/` | Park WIP redesigns here while reworking them; move back to `blog/` + add the manifest row when done | Render, list, or crawl parked files — they are invisible to the shelf, sitemap, and robots |
| `blog/not-ready/template.html` | Keep it current as the standalone scaffold + catalog | Remove scene kinds or layout pieces it documents |
| `about.html` | Fix bugs in its inline figure logic | Convert it to scrollytelling — it intentionally keeps the legacy figure system |
| `scripts/check_posts.py` | Extend the contract checks | Weaken the standalone or honesty rules |

## The binding contract (landing ↔ posts)

- **`js/posts.js` is the only link.** One strict-JSON object per post
  (`slug`, `no`, `title`, `date`, `topic`, `tags`, `deck`); `index.html`
  reads `window.VB_POSTS` and renders the shelf. No entry without a file, no
  file without an entry.
- **Each post carries its own public metadata** and it must agree with the
  manifest: `<title>` ↔ `title`, `<meta name="description">` ↔ `deck`, plus
  canonical, OG/Twitter cards, and `BlogPosting` JSON-LD pointing at
  `https://victorbusque.com/blog/<slug>.html`.
- **A post publishes when it moves out of `blog/not-ready/` (or drops its
  `"status": "wip"` draft marker) and its manifest row is live.** Parked
  files are never listed; a top-level wip draft must carry `<meta
  name="robots" content="noindex, nofollow">`; unlisted top-level files
  must also stay noindex.

## The standalone contract (per article)

- Everything the article needs is inlined: at least one `<style>` block, all
  scripts, the nav/footer markup or runtime, scene wiring, helpers. No
  `<link>`/`<script>` may reference `../css/` or `../js/`.
- Allowed external references: root-relative static assets (`/img/…`,
  `/site.webmanifest`), the Google Fonts stylesheet, absolute `https://`
  metadata URLs (og:image, canonical).
- The scaffold's inlined blocks keep a provenance banner ("Formerly the
  shared … this copy belongs to this article"). Treat inlined copies as the
  article's own code: edit them freely, but preserve the honest-document
  behavior they ship (no-JS stacked document, reduced-motion collapse, real
  states at every scroll position, honest readouts).
- `blog/template.html` is the canonical scaffold: `<html class="js">` gate +
  `window.VB` helpers in `<head>`, page script at end of body, then the
  inlined site + scene runtimes (that order reproduces the historical defer
  semantics and must be preserved when reorganizing).

## Scrollytelling vs legacy figures

- The landing and posts are scrollytelling. The scaffold's scene runtime
  handles step activation; pages key stage states off `data-active-step`.
- The legacy `.fig` system (fig-head, fig-body, PAUSE/REPLAY controls) is
  kept for `about.html` compatibility. Do not start new work on it.

Never mix the two on one page.

## Versioning the skill

The skill is versioned in its frontmatter (`metadata.version`). Bump the minor
version when standards change; bump the major when the file contract changes
(e.g. the 5.0.0 move to standalone posts). Update `SKILL.md`'s golden rules
and this map in the same change.
