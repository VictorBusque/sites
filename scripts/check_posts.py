#!/usr/bin/env python3
"""
check_posts.py — keep js/posts.js (window.VB_POSTS, the single post
manifest) consistent with the published posts in blog/.

Checks, for every .html file in blog/ (excluding template.html):
  * it has an entry in the manifest  (shelf row exists)
  * the manifest title matches the post's <title> tag
  * the manifest deck matches the post's meta description
  * the post carries a BlogPosting JSON-LD block
  * the canonical, shared scripts, component mounts, and semantic <main>
    match the site contract
  * every sticky scene has a hidden visual stage and sequential, readable
    data-step articles (the shared module supplies the card behavior)

And for every manifest entry:
  * the file it points to exists

The sitemap must also list each published post. These are intentionally
structural checks: they make every entry inherit the shared system instead of
re-implementing it page by page.

The unlisted `blog/template.html` is checked against the shared post shell too,
so the next article starts from a working contract.

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
MANIFEST = ROOT / "js" / "posts.js"
EXCLUDE = {"template.html"}
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
    """Return author-facing errors for the shared post and scene contract."""
    text = path.read_text(encoding="utf-8")
    errors = []

    canonical = f'https://victorbusque.com/{slug}'
    if not re.search(r'<link\s+rel="canonical"\s+href="' + re.escape(canonical) + r'"\s*/?>', text):
        errors.append(f"'{slug}': canonical must be '{canonical}'")
    if not re.search(r"<script>document\.documentElement\.className \+= ' js';</script>", text):
        errors.append(f"'{slug}': missing the early .js enhancement gate from blog/template.html")

    script_paths = [
        '<script src="../js/site.js" defer></script>',
        '<script src="../js/scene.js" defer></script>',
        '<script src="../js/vb.js"></script>',
    ]
    positions = [text.find(script) for script in script_paths]
    if -1 in positions or positions != sorted(positions):
        errors.append(f"'{slug}': shared scripts must be site.js → scene.js → vb.js (template order)")
    if not re.search(r'<div\s+[^>]*data-vb-nav\b', text):
        errors.append(f"'{slug}': missing [data-vb-nav] shared-chrome mount")
    if not re.search(r'<div\s+[^>]*data-vb-footer\b', text):
        errors.append(f"'{slug}': missing [data-vb-footer] shared-chrome mount")
    if not re.search(r'<main\b[^>]*>', text) or '</main>' not in text:
        errors.append(f"'{slug}': article content needs a semantic <main>")

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
    # Drafts copied from the template deliberately retain noindex until their
    # metadata and manifest row are ready. They are not published posts yet.
    files = {
        p.name: p for p in BLOG.glob("*.html")
        if p.name not in EXCLUDE and not is_noindex(p)
    }
    errors = []
    locations = sitemap_locations()

    # Each published file must be in the manifest.
    for name in sorted(files):
        slug = f"blog/{name}"
        entry = by_slug.get(slug)
        if entry is None:
            errors.append(f"'{slug}' has no entry in js/posts.js — add one or remove the file")
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
        if f"https://victorbusque.com/{slug}" not in locations:
            errors.append(f"'{slug}': missing from sitemap.xml")

    template = BLOG / "template.html"
    if template.is_file():
        errors.extend(post_structure_errors(template, "blog/template.html"))

    # Each manifest entry must point to a real file.
    for e in entries:
        slug = e.get("slug", "")
        missing = [k for k in ("slug", "no", "title", "date", "topic", "deck") if not e.get(k)]
        if missing:
            errors.append(f"js/posts.js entry '{slug or '[unknown]'}' missing field(s): {', '.join(missing)}")
            continue
        if not re.fullmatch(r"blog/[a-z0-9]+(?:-[a-z0-9]+)*\.html", slug):
            errors.append(f"js/posts.js slug '{slug}' must be a lowercase blog/<slug>.html path")
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", e["date"]):
            errors.append(f"js/posts.js entry '{slug}' has invalid date '{e['date']}' (use YYYY-MM)")
        if not re.fullmatch(r"\d+", e["no"]):
            errors.append(f"js/posts.js entry '{slug}' has invalid post number '{e['no']}'")
        if not isinstance(e.get("tags", []), list) or not all(isinstance(tag, str) and tag for tag in e.get("tags", [])):
            errors.append(f"js/posts.js entry '{slug}' has invalid tags (use a list of non-empty strings)")
        if not (ROOT / slug).is_file():
            errors.append(f"js/posts.js points to '{slug}' but no such file exists")
        elif is_noindex(ROOT / slug):
            errors.append(f"js/posts.js points to '{slug}', but that file is marked noindex (publish its metadata first)")

    if errors:
        print("Blog manifest or page contract is OUT OF CONSISTENCY:")
        for err in errors:
            print("  ✗ " + err)
        sys.exit(1)
    print(f"OK — {len(entries)} post(s) match the manifest and published-post contract.")
    sys.exit(0)


if __name__ == "__main__":
    main()
