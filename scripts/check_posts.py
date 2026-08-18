#!/usr/bin/env python3
"""
check_posts.py — keep js/posts.js (window.VB_POSTS, the single post
manifest) consistent with the published posts in blog/.

Checks, for every .html file in blog/ (excluding template.html):
  * it has an entry in the manifest  (shelf row exists)
  * the manifest title matches the post's <title> tag
  * the manifest deck matches the post's meta description
  * the post carries a BlogPosting JSON-LD block

And for every manifest entry:
  * the file it points to exists

Exit code 0 when clean, 1 when anything disagrees. Run after adding or
editing a post, before shipping.

Usage:  python3 scripts/check_posts.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
MANIFEST = ROOT / "js" / "posts.js"
EXCLUDE = {"template.html"}


def load_manifest():
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(r"window\.VB_POSTS\s*=\s*(\[.*\])\s*;", text, re.S)
    if not match:
        sys.exit("js/posts.js: could not find window.VB_POSTS = [...]; array")
    entries = json.loads(match.group(1))
    by_slug = {e["slug"]: e for e in entries}
    if len(by_slug) != len(entries):
        sys.exit("js/posts.js has duplicate slugs — each post may appear once")
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


def main():
    entries, by_slug = load_manifest()
    files = {p.name: p for p in BLOG.glob("*.html") if p.name not in EXCLUDE}
    errors = []

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

    # Each manifest entry must point to a real file.
    for e in entries:
        if not (ROOT / e["slug"]).is_file():
            errors.append(f"js/posts.js points to '{e['slug']}' but no such file exists")
        missing = [k for k in ("slug", "no", "title", "date", "topic", "deck") if not e.get(k)]
        if missing:
            errors.append(f"js/posts.js entry '{e['slug']}' missing field(s): {', '.join(missing)}")

    if errors:
        print("js/posts.js is OUT OF CONSISTENCY with blog/:")
        for err in errors:
            print("  ✗ " + err)
        sys.exit(1)
    print(f"OK — {len(entries)} post(s) in js/posts.js match blog/ exactly.")
    sys.exit(0)


if __name__ == "__main__":
    main()
