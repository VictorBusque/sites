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
        "slug": "blog/git-github-at-scale.html",
        "no": "07",
        "title": "How Git and GitHub Work at Scale",
        "date": "2026-08",
        "topic": "Systems · Developer tools",
        "tags": ["Git", "GitHub", "Version control", "Commits"],
        "deck": "See exactly what a Git push sends: new file contents, a folder listing, a commit, and a branch update request—then see where GitHub fits in."
    },
    {
        "slug": "blog/apollo-to-phone.html", 
        "no": "06",
        "title": "Apollo and iPhone: Two Scales of Computing",
        "date": "2026-08",
        "topic": "Computing · Space",
        "tags": ["Apollo", "iPhone", "Computing"],
        "deck": "Compare the Apollo Guidance Computer and iPhone 17 Pro Max on two scales: physical size, and the memory and specialized engines behind modern computing."
    },
    {
        "slug": "blog/digi-costes.html",
        "no": "05",
        "title": "Por qué DIGI puede ser tan barata en España",
        "date": "2026-08",
        "topic": "Redes · Economía",
        "tags": ["DIGI", "Fibra", "XGS-PON", "España"],
        "deck": "Por qué DIGI ofrece fibra y móvil baratos en España: red propia en zonas densas, capacidad compartida y acuerdos mayoristas que reducen el coste por línea."
    },
    {
        "slug": "blog/gnss.html",
        "no": "04",
        "title": "How GPS and Galileo Find Your Phone",
        "date": "2026-08",
        "topic": "Space · Navigation",
        "tags": ["GNSS", "GPS", "Galileo", "Positioning"],
        "deck": "How GPS and Galileo turn coded radio signals, satellite orbit data and precise timing from four satellites into the position shown on your phone."
    },
    {
        "slug": "blog/airplane-entertainment.html",
        "no": "03",
        "title": "How In-Flight Entertainment Uses a Cabin CDN",
        "date": "2026-08",
        "topic": "Networks · CDN",
        "tags": ["CDN", "Airplane", "Entertainment"],
        "deck": "How an aircraft’s onboard media servers, cabin network and seat computers deliver films without sending every playback request to the internet."
    },
    {
        "slug": "blog/starlink.html",
        "no": "02",
        "title": "How a Starlink Packet Travels Through Space",
        "date": "2026-08",
        "topic": "Space · Networks",
        "tags": ["Starlink", "Lasers", "Latency"],
        "deck": "Follow one packet from a Starlink terminal through a moving satellite network, laser links and a gateway before it reaches the terrestrial internet."
    },
    {
        "slug": "blog/spain-renewable-grid.html",
        "no": "01",
        "title": "Spain, at Renewable Scale.",
        "date": "2026-08",
        "topic": "Energy · Grid",
        "tags": ["Solar", "Wind", "Grid", "Spain"],
        "deck": "A visual story about the current scale of Spain's renewable electricity deployment in 2026."
    }
];
