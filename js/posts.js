/* ── Single post manifest ──────────────────────────────────────────────
   One object per published post in blog/. window.VB_POSTS is read by
   index.html to render the shelf. Nothing here is invented: no entry,
   no row. When a post ships, add it below (slug is the href, no is the
   stable post number, date 'YYYY-MM', topic free-form) and run
   scripts/check_posts.py. Renders newest first. The queue lives in
   docs/ideas.md. The array body is strict JSON so the checker can parse
   it directly. */
window.VB_POSTS = [
    {
        "slug": "blog/apollo-to-phone.html",
        "no": "06",
        "title": "How compute went from Apollo to the iPhone.",
        "date": "2026-08",
        "topic": "Hardware · Silicon",
        "tags": ["Apollo", "iPhone", "Silicon", "Compute"],
        "deck": "From Apollo's 2 KB of RAM to a phone in your pocket: scroll the curves — frequency, transistor density, memory, parallelism and specialization — that made the leap."
    },
    {
        "slug": "blog/gps-is-not-just-gps.html",
        "no": "05",
        "title": "How GPS Turns Time Into Location.",
        "date": "2026-08",
        "topic": "Space · Infrastructure",
        "tags": ["GPS", "Galileo", "PNT"],
        "deck": "GPS and Galileo do more than draw a blue dot. Four clocks in orbit locate devices and synchronise networks, grids, markets—until a signal is blocked or faked."
    },
    {
        "slug": "blog/european-cloud.html",
        "no": "04",
        "title": "Can Europe Build a Sovereign Cloud?",
        "date": "2026-08",
        "topic": "Europe · Cloud",
        "tags": ["Europe", "Cloud", "Data Act"],
        "deck": "A European cloud needs more than servers on European soil: control of keys, operators, software, supply chain and a credible exit. See the layers that matter."
    },
    {
        "slug": "blog/digital-dependence.html",
        "no": "03",
        "title": "Europe’s Digital Dependence.",
        "date": "2026-08",
        "topic": "Europe · Technology",
        "tags": ["Europe", "Sovereignty", "Standards"],
        "deck": "Europe’s software and cloud dependence is a stack: chips, identity, devices, cloud, apps and data. Follow dependencies, the exits and what sovereignty can mean."
    },
    {
        "slug": "blog/one-process-per-person.html",
        "no": "02",
        "title": "How WhatsApp handles 100B messages a day.",
        "date": "2026-08",
        "topic": "Systems · Distributed",
        "tags": ["Erlang", "Architecture", "E2EE"],
        "deck": "How WhatsApp carries a hundred billion messages a day: one Erlang process per connection, queues that live in memory, islands that replicate in one direction, and keys the servers never hold."
    },
    {
        "slug": "blog/token-by-token.html",
        "no": "01",
        "title": "How LLMs write text, token by token.",
        "date": "2026-02",
        "topic": "AI · LLMs",
        "tags": ["LLM", "Sampling"],
        "deck": "An LLM is a next-token predictor. Walk the loop with a toy model trained on twelve sentences — read, score, pick, append — and watch the whole vocabulary compete for every token."
    }
];
