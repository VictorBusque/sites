/* ── Single post manifest ──────────────────────────────────────────────
   One object per published post at the top level of blog/. window.VB_POSTS
   is read by index.html to render the shelf. Nothing here is invented:
   no entry, no row.

   blog/not-ready/ holds works in progress — redesigns parked until they
   ship. Those articles are never in this manifest, never rendered on the
   shelf, and excluded from sitemap + robots. When a parked article is
   finished, move it to blog/<slug>.html and add its row here (dropping
   any "status": "wip" draft marker) in the same change.

   An entry with "status": "wip" is an unfinished article that already
   sits at its final blog/ URL: index.html does not render it, the
   checker skips its metadata checks, and the file itself must stay
   noindex. Drop the field when it ships.

   slug is the href, no is the stable post number, date 'YYYY-MM', topic
   free-form. Run scripts/check_posts.py after any change. Renders newest
   first. The idea queue lives in docs/ideas.md. The array body is strict
   JSON so the checker can parse it directly. */
window.VB_POSTS = [
    {
        "slug": "blog/starlink.html",
        "no": "03",
        "title": "Starlink — A packet's journey through space",
        "date": "2026-08",
        "topic": "Space · Networks",
        "tags": ["Starlink", "Lasers", "Latency"],
        "deck": "A packet's route through the constellation: phased arrays on the ground, laser links between satellites, and the physics of latency from orbit."
    },
    {
        "slug": "blog/spain-renewable-grid.html",
        "no": "02",
        "title": "Spain, at Renewable Scale.",
        "date": "2026-08",
        "topic": "Energy · Grid",
        "tags": ["Solar", "Wind", "Grid", "Spain"],
        "deck": "A visual story about the current scale of Spain's renewable electricity deployment in 2026."
    },
    {
        "slug": "blog/apollo-to-phone.html",
        "no": "01",
        "title": "From Apollo to iPhone 17 Pro Max — 56 years of compute.",
        "date": "2026-08",
        "topic": "Hardware · Silicon",
        "tags": ["Apollo", "iPhone", "Silicon", "Compute"],
        "deck": "A scrollytelling history of computational power from the Apollo Guidance Computer to the iPhone 17 Pro Max."
    }
];
