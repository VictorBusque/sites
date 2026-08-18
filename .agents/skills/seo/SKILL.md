---
name: seo
description: >
  SEO for the victorbusque.com living-notes site: search-friendly <title> tags,
  meta descriptions, slugs, canonicals, Open Graph/Twitter cards, structured
  data (JSON-LD), heading structure, internal linking, alt text, and
  sitemap.xml/robots.txt hygiene. Use whenever creating or editing any public
  page (landing, posts, about), shipping a new post, or reviewing how the site
  presents in search results and social previews.
metadata:
  author: Víctor Busqué
  version: "1.0.0"
  site: living-engineering-notes
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

They are allowed to differ. The shelf title in `ENTRIES` follows the h1;
the `<title>`/`og:title`/`twitter:title` follow the searcher. Never make
the `<title>` poetic at the cost of clarity — that's the mistake this
skill exists to prevent.

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

Every public page ships the full card set (see `blog/template.html`):

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
  description, datePublished (from `ENTRIES` date), author Person, image
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

- Every post links its neighbors via `post-nav`; when shipping a post,
  update the prev/next links of adjacent posts.
- The landing `ENTRIES` shelf is the hub: deck text doubles as the
  SERP-snippet voice of the site. No entry without a file, no file
  without an entry (create-a-blog-entry rule).
- Cross-link between posts only where the reader genuinely benefits
  ("the sampling loop behind this is its own note").

## sitemap.xml and robots.txt

- **Every shipped page must be in `sitemap.xml`** — this is the step that
  gets forgotten. When a post ships, add its `<url>` (priority 0.9,
  changefreq monthly) and bump `lastmod` for changed pages (real dates,
  commit date).
- `robots.txt` disallows `/blog/template.html` only. Never disallow
  anything else; never noindex a real page.
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
- [ ] `node --check`-clean if `ENTRIES` or scripts were touched

## Workflow integration

- **New post:** do SEO while doing step 3 of create-a-blog-entry (replace
  `<title>` and meta) — title, description, OG/Twitter, JSON-LD, sitemap
  entry, all in the same pass, before the landing-page registration.
- **Editing a shipped page:** if the idea didn't change, keep the title's
  keyword contract; re-check char budgets and sync og/twitter.
- **Landing page:** its title should say what the site is
  ("Scrollytelling Engineering Essays"), not just the brand.
