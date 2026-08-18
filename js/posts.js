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
