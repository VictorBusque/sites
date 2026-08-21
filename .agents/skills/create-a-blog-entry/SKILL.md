---
name: create-a-blog-entry
description: >
  Creates articles for the notebook at victorbusque.com: a single, fully
  featured landing page (index.html) plus standalone, one-of-a-kind posts at
  blog/<slug>.html — each a self-contained scroll-driven document with its own
  inlined styles, scripts, and chrome, bound to the landing only through the
  js/posts.js manifest. Use whenever writing a new post, editing an article,
  touching the landing system (css/site.css, js/site.js, js/scene.js,
  js/vb.js), or updating the landing page's cards and copy. Enforces the
  site's voice, craft standards, and scrollytelling conventions so every
  article is honest, polished, and complete on its own.
metadata:
  author: Víctor Busqué
  version: "5.1.0"
  site: notebook-of-curiosities
---

# Create a Standalone Scrollytelling Post

The site is a **hub and spokes**: one landing page, and articles that are each
their own small website. Every post is a **standalone scrollytelling
article** — one idea, told as a guided visual experience, in a single
self-contained HTML file. Scrolling is the reader's timeline — scenes pin a
visual while step-by-step text scrolls over it, diagrams transform as you
travel, and the story has a beginning, middle, and end. The reader steps
through the process; nothing is faked.

This skill is the site-specific application of the **scrollytelling skill**
(Atelier, in the pi-extensions repo). That skill is the craft source of truth
for storyboarding, scene design, progressive enhancement, and validation —
including its single-file output contract, which this site now follows
exactly. This file adds the site's contracts: the standalone rule, voice, and
the landing binding through `js/posts.js`.

## Start with the topic narrative

A new article normally begins with the three-stage topic pipeline:

```text
topics/<topic>/context.md → topics/<topic>/narrative.md → blog/<slug>.html
```

Use `create-a-narrative` to create and approve `narrative.md` before building.
Read that file in full alongside its linked `context.md`; the narrative is the
implementation brief, while the context is the evidence record. Do not invent
missing story, visual, data, or metadata decisions during frontend work —
record an open question in the narrative and resolve it first.

Treat the narrative as the page contract:

- its story contract and act table set the article’s order and prose purpose;
- its evidence IDs, caveats, and illustrative labels govern copy, numbers,
  labels, charts, and live readouts;
- its scene specifications set state models, motion intent, static fallbacks,
  accessibility, and mobile rules;
- its visual direction sets the article’s one-of-a-kind aesthetic; and
- its publishing handoff drafts the manifest and SEO values, which the `seo`
  skill verifies before release.

Keep `topics/` private: do not load it at runtime or link to it publicly. An
existing published article can be edited without a narrative only when the
change is narrowly corrective; create or update a matching narrative for any
substantial story, scene, or design revision.

## The architecture in one paragraph

`index.html` is the hub: fully featured, SEO-optimized, built from the
landing's own system (`css/site.css`, `js/site.js`, `js/scene.js`,
`js/vb.js`) and rendering its shelf from `js/posts.js` (`window.VB_POSTS`).
Each `blog/<slug>.html` is a spoke: a standalone page that inlines
everything it needs and links no shared `../css/` or `../js/` asset **except
the two shared chrome components: the required reading indicator and the
post navigator** (prev/next + home, derived from the manifest at runtime).
The only contract between an article and the
landing is metadata: the manifest
row plus the article's own `<title>`, description, canonical, OG/Twitter
cards, and `BlogPosting` JSON-LD, which must all agree. Articles are
one-of-a-kind — two posts may share craft standards and house style, but no
component is shared by reference.

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
5. **Standalone means owned.** Everything a post needs — base styles,
   runtime, helpers, chrome — lives inline in that file, copied from the
   scaffold and then owned by the article. Edit the inlined copies freely;
   that is the point. But keep the honest-document behavior they provide
   (document-first fallbacks, reduced-motion collapse, real states at every
   scroll position). If a future article replaces the scaffold's runtime
   with something bespoke, it must preserve that behavior.
6. **The landing binding is metadata only.** Register the post in
   `js/posts.js` and keep its SEO block in agreement. Never add post data to
   `index.html`, and never make an article depend on landing files.

Full file ownership and contracts: [references/FILE-MAP.md](references/FILE-MAP.md).
Scene recipes: [references/SCROLLYTELLING.md](references/SCROLLYTELLING.md).
Browser-platform rationale: [references/PLATFORM.md](references/PLATFORM.md).

## What the scaffold inlines for you

`blog/not-ready/template.html` (the canonical starting point) already
contains, inlined and working: the base stylesheet (tokens, chrome, reveals,
scene system,
responsive + reduced-motion blocks), the site runtime (nav/footer mounts,
progress, cursor, reveals), the scene runtime (step cards, progress rail,
`data-active-step`, mobile bottom sheet, `--card-reserve`), and the
`window.VB` helpers (`esc`, `mulberry32`, `fmt.pct/ordinal/sup`,
`motion.retrig/countUp`, `reduceMotion`). The load order inside the file is
part of the contract: helpers in `<head>`, page script at end of body, then
the site + scene runtimes — preserve it when you reorganize.

This means an author normally writes a decorative `aria-hidden` stage plus
ordered `<article class="step" data-step="…">` paragraphs, and page-specific
logic in one inline script before the runtime blocks. If the article keeps
the scaffold's scene runtime, do not add local scroll handlers,
`MutationObserver`s, progress bars, or step-label plumbing — the runtime
already does it; page scripts compute honest state and key stage states off
`data-active-step`, registering reactions with `VB.onReady(fn)` +
`window.VBScene.onStep(fn)`.

## Workflow

### 1. Read the narrative, then validate the storyboard

For a new topic, `topics/<topic>/narrative.md` is the required storyboard and
build brief. Confirm it is `ready-for-build`, that every proposed fact/readout
has evidence or an explicit illustrative label, and that every scene has a
state model and fallback. Use its opening, ending, act table, and scene IDs as
the source of truth; do not create a competing storyboard.

If you are repairing an older article with no topic narrative, create a compact
internal storyboard using the Atelier progression below. When the repair
changes the story or visual system materially, capture the resulting decisions
in `topics/<topic>/narrative.md` through `create-a-narrative`.

The Atelier progression is:

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
cp blog/not-ready/template.html blog/<slug>.html
```

`blog/not-ready/template.html` is a working standalone post that doubles as
a catalog: a sticky scene with a transforming diagram, split and comparison
scenes, a metrics scene, a breather, and every prose piece — with the base
stylesheet and runtime inlined. It is kept current; always copy from it.

`<slug>`: lowercase, hyphenated, one idea per article (e.g. `the-queue.html`,
`token-budget.html`, `kv-cache.html`).

### 3. Build the post from the narrative

Replace in order: `<title>` and meta → hero (`crumb`, `h1`, `dek`,
`post-meta`) → acts (prose sections + scenes) → footer
label. (No prev/next links to write: the shared post-nav component renders
them from the manifest.) Update the `status` in the nav mount (e.g. `POST 03 /
WAITING`).

Map the narrative one-to-one while building:

- Use its **document outline** and act table for semantic headings and DOM
  order; prose carries every conclusion before enhancement is added.
- Build each **scene specification** with its stated visual inventory, named
  stable states, evidence, choreography, acceptance check, and responsive
  behavior. Keep ordered `[data-step]` paragraphs as the text equivalent.
- Implement only the narrative’s declared **enhancement ladder** and state
  source of truth. Extend it through the scrollytelling skill only when a
  documented open question requires a better mechanism.
- Translate its **visual direction** into page-local tokens, type roles,
  diagram grammar, and motion character; do not default to the house style
  when the narrative selected a different justified aesthetic.
- Carry its **evidence boundaries** into captions and code. A computed
  illustrative model must say so; a verified figure must retain its scope and
  qualification. Never make the stage look more precise than its source.

The shared reading indicator and post navigator are the two shared post
assets — everything else a post needs is inlined. Keep the template's
relative `../../css/post-progress.css` + `../../js/post-progress.js` and
`../../css/post-nav.css` + `../../js/post-nav.js` while the
file is parked, and change all to the `../css/…` + `../js/…` forms
when it moves to top-level `blog/`. The navigator derives the home link and
neighbors from `js/posts.js` on its own — never hand-write prev/next links —
and its wording can be localized through `data-vb-nav-*` attributes on
`<body>`.

Pieces of the scaffold that must survive the copy **exactly** (they are the
progressive-enhancement and binding contract):

- The `<html class="js">` gate script in `<head>` (set before the body parses
  — without it scenes degrade to a plain document)
- The inlined `window.VB` helper block in `<head>` (page scripts use it while
  parsing)
- The nav/footer mounts (`[data-vb-nav]`, `[data-vb-footer]`) with their
  `<noscript>` fallback rows — the inlined runtime renders into them
- The `<script>` order at end of body: page script first, then the inlined
  site + scene runtime blocks (matching the original defer semantics)
- The full SEO block (see the seo skill): canonical, OG/Twitter cards,
  `BlogPosting` JSON-LD
- `post-hero`, `post-prose` structure — unless the article's
  one-of-a-kind design deliberately replaces them

Everything else — theme, palette, stage design, fonts, scene mechanics — is
the article's own. Diverge boldly; the house style is a starting point, not a
police.

### 4. Build the document first, then enhance

Write the headings, prose, captions, and diagrams as static HTML/SVG before
adding any motion. Then enhance in this order (from the Atelier skill):

```text
HTML        semantic story and static fallback
CSS         layout, visual system, simple motion
CSS timelines  progressive, continuous scroll-linked enhancement (@supports)
IntersectionObserver  discrete step activation (the scaffold's runtime)
requestAnimationFrame custom continuous state or Canvas drawing
Canvas/WebGL genuinely spatial or high-density visual explanation
```

The scaffold's scene runtime already provides step activation, step-card
wrapping, the progress rail, and the mobile bottom-sheet layout for sticky
scenes. Page scripts only do what it can't: compute honest state and drive
per-step stage states via `data-active-step` CSS hooks.

### 5. Bind the post to the landing

Add one object to the `posts` array in `js/posts.js` at the site root (the
site's single post manifest, `window.VB_POSTS` — `index.html` reads it and
renders the shelf, so there is no inline entry data to edit; it works both
locally and on the server):

```json
{
    "slug": "blog/<slug>.html",
    "no": "02",
    "title": "Short, concrete title.",
    "date": "YYYY-MM",
    "topic": "Free-form topic label (e.g. \"AI · LLMs\")",
    "tags": ["Tag", "Tag"],
    "deck": "One or two sentences that promise the experience: what the reader will scroll through and understand."
}
```

The row and the file are the same object. `slug` must match the file and
is the internal link; `no` is the stable post number; `topic` is free-form
metadata shown on the row (there is no fixed taxonomy and no folder tree —
the site is a curiosity notebook where engineering is the core, not the
boundary). The `deck` must equal the post's `<meta name="description">` and
the `title` must equal the post's `<title>` (only case and a trailing
"."/" — Víctor Busqué" suffix may differ). The idea queue lives in
`docs/ideas.md` — move an idea from there into `js/posts.js` when its
document ships. Update the site's framing copy (hero demo labels, marquee
items) only if the site's promise changes.

While an article is being written, park it in `blog/not-ready/` (never in
the manifest) or register it at its final URL with `"status": "wip"` plus a
`noindex` file: the landing filters wip rows out of the shelf and the checker
relaxes its metadata checks. Shipping means moving the file to `blog/`,
dropping the status field, and completing the page's canonical, OG/Twitter
cards, JSON-LD, and sitemap row in the same pass.

### 6. Verify (run the checklist)

After adding or editing a post, run the consistency guard:

```sh
python3 scripts/check_posts.py
node --check js/site.js
node --check js/scene.js
node --check js/vb.js
git diff --check
```

It fails unless every top-level file in `blog/` has a matching `js/posts.js`
entry whose `title`/`deck` match the post's own `<title>` and meta
description; every manifest entry points at a real file carrying a
`BlogPosting` JSON-LD block, a canonical, and OG/Twitter cards; every post is
standalone (no shared `../css/` or `../js/` links except the reading
indicator and post navigator, and at least one `<style>` block); the
sticky-scene honesty rules hold; both shared components are
present; and the sitemap lists exactly the published posts. Parked
`blog/not-ready/` drafts are invisible to it; unlisted top-level drafts must
be `noindex`.

See [Checklist](#checklist) and the validation section in
[references/SCROLLYTELLING.md](references/SCROLLYTELLING.md#validation) before
handing an article over.

## Content conventions

- **Sections:** `<h2>` with `<span class="sec-no">NN</span>` inside
  `post-prose`. Section headings are concrete, not cute ("The problem",
  "Selection sort, step by step").
- **Scenes:** each scene gets a `scene-head` with an act label (e.g.
  `ACT 02`) and a concrete name (e.g. `THE MECHANISM`). The runtime derives
  the mono `STEP k / n` label from ordered `data-step` values; only author
  `.step-k` when its wording genuinely needs to differ.
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
All classes below come from the scaffold's inlined base stylesheet — an
article keeps, restyles, or replaces them at will.

- `sticky-scene` — a tall scroll track with a pinned dark stage; step cards
  scroll over it. The workhorse of the site.
- `scene` / `split` — a narrative moment; copy and a bounded visual side by
  side (stacked on mobile).
- `full-bleed` — a cinematic visual with restrained overlay text.
- `comparison` — before/after or A/B transformation.
- `metrics-scene` — a large number with visible evidence.
- `breather` — a low-information beat between demanding ideas (a big serif
  line, a quote).

Dark stages use the `--stage` background with the 32px grid — or the
article's own equivalent.

## House style (quick reference)

Full reference: [references/DESIGN.md](references/DESIGN.md). The house style
is the default look, not a mandate — but keep it unless the article has a
reason to differ.

- Palette tokens: `--ink #101010`, `--paper #f2f0e9`, `--paper-2 #ece9de`,
  `--acid #c7ff3d`, `--blue #546cff`, `--orange #ff6b2c`, `--muted #716f68`,
  `--line #111`, `--stage #121212`.
- Type: Unbounded (display/headings), Instrument Serif (italic accents and
  big numerals), Newsreader (body), DM Mono (labels/readouts).
- Semantic color on dark stages: **acid** = found / settled / active flow,
  **blue** = currently being examined / structure, **orange** = the thing to
  watch right now. Keep this mapping consistent across posts — readers learn
  it once.
- Sticky stages: `position: sticky; top: 0; height: 100svh`, dark background
  + grid, decorative bottom-right circle, `scene-head` bar.
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
- `prefers-reduced-motion: reduce` must collapse the article to a plain
  stacked document. Never weaken that block in the inlined styles.

## Checklist

- [ ] Storyboarded (acts + per-section question/payoff) before coding
- [ ] Copied `blog/not-ready/template.html`; landing files untouched
- [ ] `<html class="js">` gate present in `<head>`; no shared `../css/` or
      `../js/` links except the reading indicator and post navigator — the
      post is otherwise standalone
- [ ] Document-first: the page reads as a complete article with JS disabled
      and with reduced motion (stage + stacked steps, all text visible)
- [ ] Every `sticky-scene` honors the honesty contract: `[data-step]`
      articles in an unbroken 1…n sequence, a decorative `aria-hidden` stage,
      readable paragraph fallback text, stage states keyed off
      `data-active-step`, and `[data-readout]` if a live stage indicator is
      wanted
- [ ] Every readout/caption number is computed state or a verified fact,
      re-checked by running the logic (REPL) or citing the source
- [ ] Inline scripts parse (`node --check` equivalent); page has no console
      errors; no duplicate IDs; SVG diagrams have `<title>`/`<desc>` or are
      `aria-hidden` with the conclusion in adjacent DOM text
- [ ] Scroll-timeline enhancements sit inside `@supports (animation-timeline:
      view())` and have a working discrete fallback
- [ ] Do not add CDN scripts, analytics, or `fetch()` without an explicit
      product need and approval. The Google Fonts stylesheet is the only
      accepted third-party presentation dependency.
- [ ] `js/posts.js` entry added with a slug that matches the file, title/deck
      matching the post's `<title>` and meta description; no stale rows;
      `python3 scripts/check_posts.py` passes; the shelf shows the new post
- [ ] Post carries the matching `BlogPosting` JSON-LD in its `<head>`
- [ ] Mobile check at 390px: sticky stage fits (labels ≥ 8px rendered), step
      cards boot bottom-docked and stay readable, lanes/rails stack, nothing
      clips or crosses into the next section; reverse scrolling remains stable
- [ ] Keyboard check: the “Skip to content” link reaches `<main>`, navigation
      and controls are focusable, and no scene requires a pointer to
      understand
- [ ] Motion check: `prefers-reduced-motion` exposes the document fallback;
      ambient loops pause without hiding the scroll-controlled states
- [ ] Copy follows the tone rules; no fake stats, no slang, no emoji
