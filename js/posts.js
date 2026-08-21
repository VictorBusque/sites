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
        "slug": "blog/how-s3-works.html",
        "no": "09",
        "title": "How Amazon S3 Works: Eleven Nines, Explained",
        "date": "2026-09",
        "topic": "Cloud storage · Systems",
        "tags": ["S3", "AWS", "Erasure coding", "Durability"],
        "deck": "Follow one S3 upload: erasure-coded shards across three Availability Zones, a continuous repair loop, and the read barrier behind strong consistency."
    },
    {
        "slug": "blog/write-ahead-log.html",
        "no": "08",
        "title": "How WAL Saves a $100 Transfer.",
        "date": "2026-08",
        "topic": "Databases · Systems",
        "tags": ["WAL", "Databases", "Durability", "Systems"],
        "deck": "Follow one $100 transfer through memory, a durable write-ahead log, a sudden crash, recovery, and the checkpoint that lets data catch up."
    },
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
        "title": "Apollo in Your Pocket: AGC vs iPhone",
        "date": "2026-08",
        "topic": "Computing · Space",
        "tags": ["Apollo", "iPhone", "Computing"],
        "deck": "The Apollo Guidance Computer and your phone, measured scale by scale — size, mass, memory, time. Every ratio computed, none invented. Measured, not scored."
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
        "title": "How Spain's Grid Reached 62.3% Renewables.",
        "date": "2026-08",
        "topic": "Energy · Grid",
        "tags": ["Solar", "Wind", "Grid", "Spain"],
        "deck": "See how Spain's peninsular grid reached 109.3 GW of renewables and 62.3% of its electricity mix by May 2026 — and why flexibility is now the bottleneck."
    }
];
