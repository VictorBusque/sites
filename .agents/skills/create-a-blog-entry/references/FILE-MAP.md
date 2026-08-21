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
├── topics/
│   └── <topic>/
│       ├── context.md          # Private research, sources, and caveats
│       └── narrative.md        # Private story + visual + build brief
├── about.html                  # Personal page — landing system + legacy figures
├── .agents/skills/
│   ├── create-a-narrative/    # context.md → narrative.md workflow + template
│   └── create-a-blog-entry/   # narrative.md → standalone post workflow
│       ├── SKILL.md
│       └── references/         # SCROLLYTELLING.md, DESIGN.md, MOTION.md,
│                               #   PLATFORM.md
├── docs/ideas.md               # New-idea queue
├── README.md                   # Personal notes
├── robots.txt                  # Disallows /blog/not-ready/ parked work
├── sitemap.xml                 # Public URLs; update real lastmod dates when pages change
└── scripts/check_posts.py      # Enforces the manifest + standalone contract
```

## File ownership

| File | You may | You may not |
|---|---|---|
| `index.html` | Update landing copy and shelf presentation | Duplicate post data; it belongs in `js/posts.js` |
| `css/site.css`, `js/site.js`, `js/scene.js`, `js/vb.js` | Extend/fix the landing system | Point a blog article at any of them |
| `js/posts.js` | Add/update manifest rows when posts ship | Invent rows without files, or stash post data anywhere else |
| `topics/<topic>/context.md` | Record research, sources, source dates, facts, caveats, and open questions for one prospective article | Serve it publicly, treat it as the post’s copy, or use it as landing data |
| `topics/<topic>/narrative.md` | Make the approved story, evidence, scene, visual, accessibility, implementation, and publishing brief from its context | Invent facts outside its linked context, substitute it for the public article, or leave design decisions as vague decoration |
| `blog/<slug>.html` | Everything — the whole file is the article's own: styles, scripts, chrome, prose, scenes | Link landing/shared assets; the sole exception is the required `../css/post-progress.css` + `../js/post-progress.js` indicator (or `../../` while parked) |
| `blog/not-ready/` | Park WIP redesigns here while reworking them; move back to `blog/` + add the manifest row when done | Render, list, or crawl parked files — they are invisible to the shelf, sitemap, and robots |
| `blog/not-ready/template.html` | Keep it current as the standalone scaffold + catalog | Remove scene kinds or layout pieces it documents |
| `about.html` | Fix bugs in its inline figure logic | Convert it to scrollytelling — it intentionally keeps the legacy figure system |
| `scripts/check_posts.py` | Extend the contract checks | Weaken the standalone or honesty rules |

## The topic pipeline (research → narrative → post)

- **One folder per prospective article:** `topics/<topic>/context.md` is the
  private evidence record; `topics/<topic>/narrative.md` is the private,
  implementation-ready story contract. Topic names are lowercase and
  hyphenated when more than one word.
- **The order is deliberate:** research first, then use
  `create-a-narrative` to copy its `_narrative.md` template and turn evidence
  into story, scenes, visual direction, fallbacks, and publishing handoff.
  Then use `create-a-blog-entry` with the `scrollytelling` skill to make the
  standalone page. A narrative does not publish by itself and never appears in
  `js/posts.js`, `sitemap.xml`, or public navigation.
- **Narrative evidence governs implementation:** every number or claim used in
  a scene must remain verified, explicitly inferred, or visibly illustrative
  as classified in `narrative.md`. Its state models, responsive behavior, and
  reduced-motion fallbacks are build requirements, not optional inspiration.

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
  scripts, the nav/footer markup or runtime, scene wiring, helpers. The only
  permitted shared references are the required reading indicator:
  `../css/post-progress.css` + `../js/post-progress.js` (or `../../` from
  `blog/not-ready/`). No other `<link>`/`<script>` may reference shared
  `../css/` or `../js/` assets.
- Allowed external references: root-relative static assets (`/img/…`,
  `/site.webmanifest`), the Google Fonts stylesheet, absolute `https://`
  metadata URLs (og:image, canonical).
- The scaffold's inlined blocks keep a provenance banner ("Formerly the
  shared … this copy belongs to this article"). Treat inlined copies as the
  article's own code: edit them freely, but preserve the honest-document
  behavior they ship (no-JS stacked document, reduced-motion collapse, real
  states at every scroll position, honest readouts).
- `blog/not-ready/template.html` is the canonical scaffold: `<html class="js">` gate +
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

The `create-a-blog-entry` skill is versioned in its frontmatter
(`metadata.version`). Bump the minor version when standards change; bump the
major when the file contract changes (e.g. the 5.0.0 move to standalone
posts). Update its `SKILL.md` and this map in the same change. The separate
`create-a-narrative` skill versions its own context-to-narrative contract.
