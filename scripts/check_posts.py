#!/usr/bin/env python3
"""
check_posts.py — keep js/posts.js (window.VB_POSTS, the single post
manifest) consistent with the published posts in blog/.

Site architecture: one landing page (index.html) bound to standalone
articles through metadata. Every article is a self-contained HTML file —
its own styles, document, and scene logic. Posts share only two required
chrome components: the reading indicator (/css/post-progress.css +
/js/post-progress.js) and the post navigator (/css/post-nav.css +
/js/post-nav.js — a discreet top-center pager: home link plus prev/next
arrows, derived from the manifest at runtime); no article links the landing's
shared files
(css/site.css, js/site.js, js/scene.js, js/vb.js).

Checks, for every .html file at the top level of blog/ (files parked in
blog/not-ready/ are WIP and invisible to this checker):
  * it has an entry in the manifest and the manifest title/deck match
    the post's own <title> / meta description
  * it carries a BlogPosting JSON-LD block, a canonical URL, and the
    OG/Twitter card basics
  * it loads the two shared chrome components (top-edge reading indicator
    + post navigator) and has no hand-rolled persistent navigation or
    masthead chrome
  * it is otherwise standalone: no links to ../css/ or ../js/ assets —
    styles and scene scripts are owned by the page
  * it is a semantic document: <main>
  * every sticky scene has a hidden visual stage and sequential,
    readable data-step articles (the honest-document contract)

And for every manifest entry:
  * the file it points to exists and is indexable (or is a wip draft:
    "status": "wip" — not rendered on the shelf, checker relaxed,
    file must stay noindex until it ships)

The sitemap must list exactly the published posts — parked not-ready
articles and wip drafts never appear in it.

Exit code 0 when clean, 1 when anything disagrees. Run after adding or
editing a post, before shipping.

Usage:  python3 scripts/check_posts.py
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
NOT_READY = BLOG / "not-ready"
MANIFEST = ROOT / "js" / "posts.js"
SITEMAP = ROOT / "sitemap.xml"


def load_manifest():
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(r"window\.VB_POSTS\s*=\s*(\[.*\])\s*;", text, re.S)
    if not match:
        sys.exit("js/posts.js: could not find window.VB_POSTS = [...]; array")
    entries = json.loads(match.group(1))
    if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
        sys.exit("js/posts.js: VB_POSTS must be a JSON array of objects")
    by_slug = {e.get("slug"): e for e in entries}
    if len(by_slug) != len(entries):
        sys.exit("js/posts.js has duplicate slugs — each post may appear once")
    by_no = {e.get("no"): e for e in entries}
    if len(by_no) != len(entries):
        sys.exit("js/posts.js has duplicate post numbers — each post needs a stable number")
    return entries, by_slug


def post_title(path):
    m = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return None
    # The manifest holds the plain headline; the post appends the site name.
    return re.sub(r"\s*—\s*Víctor Busqué\s*$", "", m.group(1)).strip()


def post_description(path):
    text = path.read_text(encoding="utf-8")
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', text, re.S)
    if not m:
        m = re.search(r'<meta\s+content="(.*?)"\s+name="description"\s*/?>', text, re.S)
    return m.group(1).strip() if m else None


def has_blog_posting(path):
    return "BlogPosting" in path.read_text(encoding="utf-8")


def is_noindex(path):
    return bool(re.search(
        r'<meta\s+name="robots"\s+content="[^"]*\bnoindex\b',
        path.read_text(encoding="utf-8"), re.I,
    ))


def post_structure_errors(path, slug):
    """Author-facing errors for the standalone-post and honest-document contract."""
    text = path.read_text(encoding="utf-8")
    errors = []

    canonical = f'https://engineering.victorbusque.com/{slug}'
    if not re.search(r'<link\s+rel="canonical"\s+href="' + re.escape(canonical) + r'"\s*/?>', text):
        errors.append(f"'{slug}': canonical must be '{canonical}'")
    if not re.search(r"<main\b[^>]*>", text) or "</main>" not in text:
        errors.append(f"'{slug}': article content needs a semantic <main>")

    # The reading indicator and post navigator are the two shared article
    # components. The indicator's palette stays local to the article through
    # data-vb-progress-* attributes; the navigator derives prev/next and the
    # home link from js/posts.js at runtime (nothing to maintain per post).
    if not re.search(r'<link\s+rel="stylesheet"\s+href="\.\./css/post-progress\.css"\s*/?>', text):
        errors.append(f"'{slug}': missing the shared ../css/post-progress.css reading indicator")
    if not re.search(r'<script\s+src="\.\./js/post-progress\.js"\s+defer\s*></script>', text):
        errors.append(f"'{slug}': missing the shared ../js/post-progress.js reading indicator")
    if not re.search(r'<body\b[^>]*\bdata-vb-progress-start="[^"]+"[^>]*\bdata-vb-progress-mid="[^"]+"[^>]*\bdata-vb-progress-end="[^"]+"', text):
        errors.append(f"'{slug}': set data-vb-progress-start, data-vb-progress-mid, and data-vb-progress-end on <body>")
    if not re.search(r'<link\s+rel="stylesheet"\s+href="\.\./css/post-nav\.css"\s*/?>', text):
        errors.append(f"'{slug}': missing the shared ../css/post-nav.css navigator")
    if not re.search(r'<script\s+src="\.\./js/post-nav\.js"\s+defer\s*></script>', text):
        errors.append(f"'{slug}': missing the shared ../js/post-nav.js navigator")

    # Standalone contract: never link the landing system. The two shared
    # components above are deliberately the only exception. Strip script/style
    # bodies first — an inlined runtime may mention old file names in comments.
    stripped = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", "", text, flags=re.S)
    stripped = re.sub(
        r'<link\s+rel="stylesheet"\s+href="\.\./css/post-progress\.css"\s*/?>|'
        r'<script\s+src="\.\./js/post-progress\.js"\s+defer\s*></script>|'
        r'<link\s+rel="stylesheet"\s+href="\.\./css/post-nav\.css"\s*/?>|'
        r'<script\s+src="\.\./js/post-nav\.js"\s+defer\s*></script>',
        "",
        stripped,
    )
    shared = re.search(r'<(?:link|script)\b[^>]*(?:\.\./(?:css|js)/|/(?:css/site|js/(?:site|scene|vb))\.)', stripped)
    if shared:
        errors.append(
            f"'{slug}': not standalone — posts own their styles/scene scripts and never link the landing system ({shared.group(0)}…)"
        )
    if not re.search(r'<style\b', text):
        errors.append(f"'{slug}': an article owns at least a base <style> block")
    if re.search(r'<nav\b', stripped, re.I):
        errors.append(f"'{slug}': prev/next navigation comes from the shared post-nav component — remove hand-rolled <nav> chrome")
    if re.search(r'<(?:header|div)\b[^>]*\bclass="[^"]*\b(?:masthead|topbar|header)\b[^"]*"', stripped, re.I):
        errors.append(f"'{slug}': remove persistent masthead/topbar chrome; keep only the shared reading indicator")

    # Public metadata basics (full rules live in the seo skill).
    for pattern, label in (
        (r'<meta\s+property="og:title"', "og:title"),
        (r'<meta\s+property="og:image"', "og:image"),
        (r'<meta\s+name="twitter:card"', "twitter:card"),
    ):
        if not re.search(pattern, text):
            errors.append(f"'{slug}': missing {label} (see the seo skill)")

    scene_re = re.compile(
        r'<section\b[^>]*\bclass="[^"]*\bsticky-scene\b[^"]*"[^>]*>(.*?)</section>', re.S
    )
    for scene_no, scene in enumerate(scene_re.findall(text), 1):
        if not re.search(r'<div\b[^>]*\bsticky-scene__stage\b[^>]*aria-hidden="true"', scene):
            errors.append(f"'{slug}', sticky scene {scene_no}: stage must be aria-hidden with its conclusion in step text")
        if not re.search(r'<div\b[^>]*\bsticky-scene__steps\b', scene):
            errors.append(f"'{slug}', sticky scene {scene_no}: missing .sticky-scene__steps")
            continue
        steps = re.findall(r'<article\b[^>]*\bdata-step="(\d+)"[^>]*>(.*?)</article>', scene, re.S)
        numbers = [int(number) for number, _ in steps]
        if not 2 <= len(steps) <= 6:
            errors.append(f"'{slug}', sticky scene {scene_no}: use 2–6 data-step articles (found {len(steps)})")
        if numbers != list(range(1, len(steps) + 1)):
            errors.append(f"'{slug}', sticky scene {scene_no}: data-step values must run 1…n without gaps")
        for number, step in steps:
            if not re.search(r'<p\b[^>]*>\s*\S', step):
                errors.append(f"'{slug}', sticky scene {scene_no}, step {number}: needs readable paragraph fallback text")
    return errors


def sitemap_locations():
    try:
        root = ET.parse(SITEMAP).getroot()
    except (ET.ParseError, OSError) as exc:
        sys.exit(f"sitemap.xml could not be read: {exc}")
    return {node.text for node in root.findall('.//{*}loc') if node.text}


def main():
    entries, by_slug = load_manifest()
    files = {p.name: p for p in BLOG.glob("*.html")}
    errors = []
    locations = sitemap_locations()

    for name in sorted(files):
        slug = f"blog/{name}"
        entry = by_slug.get(slug)
        if entry is None:
            # Unlisted drafts are fine while clearly unpublished.
            if not is_noindex(files[name]):
                errors.append(
                    f"'{slug}' is not in js/posts.js — add an entry (status wip "
                    f"while drafting) or mark it noindex"
                )
            continue
        if entry.get("status") == "wip":
            if not is_noindex(files[name]):
                errors.append(f"'{slug}' is wip in js/posts.js — keep the file noindex until it ships")
            continue
        if is_noindex(files[name]):
            errors.append(f"'{slug}' is published in js/posts.js but marked noindex — publish it or set status wip")
            continue
        # Compare case-insensitively, ignoring trailing period — the tab
        # title may be title-cased while the shelf is sentence-cased.
        norm = lambda s: re.sub(r"[\s.]*$", "", (s or "").lower())
        if norm(entry["title"]) != norm(post_title(files[name])):
            errors.append(f"'{slug}': manifest title != post <title>")
        if entry["deck"] != post_description(files[name]):
            errors.append(f"'{slug}': manifest deck != post meta description")
        if not has_blog_posting(files[name]):
            errors.append(f"'{slug}': missing BlogPosting JSON-LD in <head>")
        errors.extend(post_structure_errors(files[name], slug))
        if f"https://engineering.victorbusque.com/{slug}" not in locations:
            errors.append(f"'{slug}': missing from sitemap.xml")

    # Each manifest entry must point to a real file with a valid status.
    for e in entries:
        slug = e.get("slug", "")
        if e.get("status") not in (None, "wip"):
            errors.append(f"js/posts.js entry '{slug}': status must be omitted (published) or 'wip'")
        missing = [k for k in ("slug", "no", "title", "date", "topic", "deck") if not e.get(k)]
        if missing:
            errors.append(f"js/posts.js entry '{slug or '[unknown]'}' missing field(s): {', '.join(missing)}")
            continue
        if not re.fullmatch(r"blog/[a-z0-9]+(?:-[a-z0-9]+)*\.html", slug):
            errors.append(f"js/posts.js slug '{slug}' must be a lowercase blog/<slug>.html path")
        if slug.startswith("blog/not-ready/"):
            errors.append(f"js/posts.js slug '{slug}' points into the parked WIP folder — publish to blog/ or leave it unlisted")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", e["date"]):
            errors.append(f"js/posts.js entry '{slug}' has invalid date '{e['date']}' (use YYYY-MM)")
        if not re.fullmatch(r"\d+", e["no"]):
            errors.append(f"js/posts.js entry '{slug}' has invalid post number '{e['no']}'")
        if not isinstance(e.get("tags", []), list) or not all(isinstance(tag, str) and tag for tag in e.get("tags", [])):
            errors.append(f"js/posts.js entry '{slug}' has invalid tags (use a list of non-empty strings)")
        if not (ROOT / slug).is_file():
            errors.append(f"js/posts.js points to '{slug}' but no such file exists")

    # The landing is the hub: it must load the manifest and link posts through it.
    landing = (ROOT / "index.html").read_text(encoding="utf-8")
    if "js/posts.js" not in landing:
        errors.append("index.html no longer loads js/posts.js — the landing binds posts through the manifest")

    # Sitemap must list exactly the published posts — no parked, no wip, no ghosts.
    published = {
        f"https://engineering.victorbusque.com/{e['slug']}" for e in entries
        if e.get("status") != "wip" and (ROOT / e.get("slug", "zzz")).is_file()
    }
    sitemap_blog = {loc for loc in locations if "/blog/" in loc}
    for loc in sitemap_blog - published:
        errors.append(f"sitemap.xml lists '{loc}' but it is not a published post — remove the row (parked/wip articles are not listed)")

    if errors:
        print("Blog manifest or page contract is OUT OF CONSISTENCY:")
        for err in errors:
            print("  ✗ " + err)
        sys.exit(1)
    wip = sum(1 for e in entries if e.get("status") == "wip")
    print(f"OK — {len(entries) - wip} published + {wip} wip post(s) match the manifest and the standalone-post contract.")
    sys.exit(0)


if __name__ == "__main__":
    main()
