---
name: seo
description: >
  SEO for the victorbusque.com notebook-of-curiosities site: search-friendly <title> tags,
  meta descriptions, slugs, canonicals, Open Graph/Twitter cards, structured
  data (JSON-LD), heading structure, internal linking, alt text, and
  sitemap.xml/robots.txt hygiene. Use whenever creating or editing any public
  page (landing, posts, about), shipping a new post, or reviewing how the site
  presents in search results and social previews.
metadata:
  author: Víctor Busqué
  version: "1.2.0"
  site: notebook-of-curiosities
---

# SEO — how this site meets search

Every page on this site competes for attention in three arenas: the SERP
(title + description), the social card (OG/Twitter), and the page itself
(headings, structure, links). SEO here means making all three honestly
describe what the page teaches — never clickbait, never keyword stuffing.
The site's voice rules (see the create-a-blog-entry skill) apply in full:
if a phrase wouldn't survive in the dek, it doesn't belong in a title tag.

## Core principle: two headlines, both true

- **The `<title>` is the contract with the searcher.** Descriptive,
  keyword-first, says what the page teaches. This is what Google shows.
- **The `<h1>` is the contract with the reader.** Evocative, display-set,
  part of the scrollytelling experience ("One process per person.").

They are allowed to differ. The shelf title in `js/posts.js` follows the h1;
the `<title>`/`og:title`/`twitter:title` follow the searcher. Never make
the `<title>` poetic at the cost of clarity — that's the mistake this
skill exists to prevent.

## Site naming (guard rail)

The site is **"A Notebook of Curiosities"** — brand string
`Víctor Busqué — Curiosities` on og:site_name and manifest. Never brand it
"Living Notes" or "Engineering Essays": engineering is the core, not the
boundary, and public copy must not lead with "scrollytelling" — the scroll
is the medium, not the promise. What the reader is promised is a curiosity,
walked through step by step.

## Titles

Pattern: `{What the page teaches, primary keyword first} — Víctor Busqué`

- **≤ 60 characters** (~580px). The brand suffix ` — Víctor Busqué` costs
  16 chars; keep the descriptive part ≤ ~44.
- Lead with the subject (WhatsApp, LLM, Erlang), not the metaphor.
- Numbers are allowed when verified ("100B messages a day") — never
  invented.
- `<title>`, `og:title`, and `twitter:title` must carry the same
  descriptive headline (og/twitter may drop the brand suffix if long).
- One primary query per page ("how llms generate text",
  "how whatsapp handles 100 billion messages"). The title answers it.

Good examples on this site:

```html
<title>How WhatsApp Handles 100B Messages a Day — Víctor Busqué</title>
<title>How LLMs Write Text, Token by Token — Víctor Busqué</title>
<title>About Víctor Busqué — Software Engineer (AI & Agents, Barcelona)</title>
```

Anti-patterns (real, fixed): `One process per person — Víctor Busqué`
says nothing to a searcher who doesn't know the essay; `Token by token`
hides "LLM" entirely.

## Meta descriptions

- 140–160 characters, one or two sentences, states the concrete payoff.
- Usually a tightened version of the dek; don't duplicate the dek verbatim
  if it's too long — the description is a snippet, not a summary.
- Include the primary fact/number ("a hundred billion messages a day",
  "a toy model trained on twelve sentences").
- No quotes around it, no exclamation marks, no "click to find out".
- Keep the site's casual voice: "things I find curious, shown with
  animated visuals" — never formal or intense ("walked through step by
  step", "nothing is faked" are retired phrasing, don't bring them back).

## Slugs and URLs

- `blog/<slug>.html`: lowercase, hyphenated, 2–5 words, contains the
  primary keyword if natural (`token-by-token`, `one-process-per-person`).
- Slugs are permanent — never rename a shipped URL (breaks canonicals,
  sitemap, and inbound links). Title changes are always safe; slug
  changes never are.
- One canonical per page, absolute, matching `CNAME`
  (`https://victorbusque.com/...`). `blog/` pages canonicalize to their
  own URL, not to the site root.

## Open Graph and Twitter

Every public page ships the full card set inline in its own `<head>` (see
`blog/not-ready/template.html`) — posts are standalone files, so their SEO
block is theirs alone:

- `og:type` (`website` for index/about, `article` for posts), `og:site_name`,
  `og:title`, `og:description`, `og:url`, `og:locale`
- `og:image` 1200×630 absolute URL + width/height meta
- `twitter:card summary_large_image` + matching title/description/image
- When titles change, update `og:title` and `twitter:title` in the same
  commit — a mismatched social card is a stale title bug.

## Structured data (JSON-LD)

- **index.html:** `WebSite` (name, url) and `Person` (name, url, sameAs
  to GitHub/LinkedIn) — one `<script type="application/ld+json">` block.
- **Posts:** `BlogPosting` with headline (the descriptive title),
  description, datePublished (from `js/posts.js`), author Person, image
  (the og:image), mainEntityOfPage the canonical URL.
- No other schema needed; don't add `Article` *and* `BlogPosting`.
- Validate markup at validator.schema.org after editing.

## Headings and content

- `<h2>` section headings stay concrete ("The problem", "Selection sort,
  step by step") — they're the page's outline and long-tail surface.
  Never stuff keywords into scene labels or step cards.
- The dek is the meta-description draft: write it as the honest one-sentence
  promise of the page.
- The article must read complete without JS (create-a-blog-entry rule);
  that same rule is what makes it indexable. Scrollytelling content hidden
  behind step activation must exist as DOM text — it does, keep it that way.
- SVG diagrams are decorative → `aria-hidden` with the conclusion in
  adjacent DOM text. Only informative standalone images need alt text.

## Internal linking

- Every post links its neighbors through the shared `post-nav` component,
  which reads `js/posts.js` at runtime — shipping a post updates every
  article's prev/next automatically; never hand-write neighbor links.
- The landing `js/posts.js` shelf is the hub: deck text doubles as the
  SERP-snippet voice of the site. No entry without a file, no file
  without an entry (create-a-blog-entry rule). The manifest is the only
  landing↔post binding — never mirror post data into `index.html`.
- Cross-link between posts only where the reader genuinely benefits
  ("the sampling loop behind this is its own note").

## sitemap.xml and robots.txt

- **Every shipped page must be in `sitemap.xml`** — this is the step that
  gets forgotten. When a post ships, add its `<url>` (priority 0.9,
  changefreq monthly) and bump `lastmod` for changed pages (real dates,
  commit date). The sitemap lists exactly the published posts: parked
  `blog/not-ready/` articles and wip drafts never appear.
- `robots.txt` disallows `/blog/not-ready/` only. Never disallow anything
  else; never noindex a real page.
- Every public page: `<meta name="robots" content="index, follow">`.

## Checklist (run when shipping or editing any page)

- [ ] `<title>` ≤ 60 chars, descriptive, keyword-first, ends with the brand
- [ ] `og:title` + `twitter:title` match the new title
- [ ] Meta description 140–160 chars, concrete, no clickbait
- [ ] Canonical present and absolute; slug untouched if already shipped
- [ ] `robots` = index, follow (except template)
- [ ] JSON-LD present and valid; headline matches `<title>`
- [ ] `sitemap.xml` lists the page; `lastmod` bumped for changed pages
- [ ] h2 headings concrete; dek could serve as the description
- [ ] `node --check`-clean if `js/posts.js` or scripts were touched

## Workflow integration

- **New post:** do SEO while doing step 3 of create-a-blog-entry (replace
  `<title>` and meta) — title, description, OG/Twitter, JSON-LD, sitemap
  entry, all in the same pass, before the landing-page registration. Drop
  the draft's `noindex` and its manifest `"status": "wip"` together, when
  the article ships.
- **Editing a shipped page:** if the idea didn't change, keep the title's
  keyword contract; re-check char budgets and sync og/twitter.
- **Landing page:** its title should say what the site is
  ("A Notebook of Curiosities"), not just the brand.
