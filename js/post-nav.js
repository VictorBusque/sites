/*
 * post-nav.js — shared article chrome, alongside post-progress.js:
 * a discreet top-center pager, just under the reading bar — the home
 * link (→ ../index.html) flanked by previous/next arrows.
 *
 * Include once in a top-level post with:
 *   <script src="../js/post-nav.js" defer></script>
 * (Use ../../js/post-nav.js from blog/not-ready/.)
 *
 * Neighbors are derived at runtime from the post manifest — js/posts.js,
 * the sibling of this file — ordered by stable post number, so shipping a
 * post updates every article's pager with nothing to maintain by hand.
 * Previous = older post, next = newer post. When the manifest cannot load
 * (offline preview, unlisted draft), only the home link is rendered; the
 * home link itself targets index.html relative to this script
 * (../index.html from blog/, ../../index.html from blog/not-ready/).
 *
 * This is chrome, not content: the article stays a complete document
 * without it, and no conclusion lives here.
 *
 * Optional per-post overrides on <body>:
 *   data-vb-nav-home-label  (default "Notebook")
 *   data-vb-nav-prev-label  (default "Previous curiosity")
 *   data-vb-nav-next-label  (default "Next curiosity")
 *   data-vb-nav-home-href   (default: derived, see above)
 */
(function () {
    'use strict';

    function option(name, fallback) {
        var config = document.body || document.documentElement;
        return config.getAttribute('data-vb-nav-' + name) || fallback;
    }

    function scriptBase() {
        var me = document.querySelector('script[src*="post-nav.js"]');
        return me ? me.getAttribute('src').replace(/[^/]*$/, '') : '../js/';
    }

    function start() {
        if (document.querySelector('.vb-post-chrome')) return;
        var base = scriptBase();

        var chrome = document.createElement('div');
        chrome.className = 'vb-post-chrome';

        var home = document.createElement('a');
        home.className = 'vb-post-home';
        home.href = option('home-href', base.replace(/js\/$/, 'index.html'));
        var arrow = document.createElement('i');
        arrow.setAttribute('aria-hidden', 'true');
        arrow.textContent = '\u2190';
        home.appendChild(arrow);
        home.appendChild(document.createTextNode(option('home-label', 'Notebook')));

        chrome.appendChild(home);
        document.body.appendChild(chrome);

        if (window.VB_POSTS) {
            addArrows(window.VB_POSTS);
            return;
        }
        /* Fetch the manifest — a sibling of this file — and flank the home
           link with the neighbors when it arrives. Offline, nothing breaks:
           the home link above already rendered. */
        var s = document.createElement('script');
        s.src = base + 'posts.js';
        s.onload = function () { addArrows(window.VB_POSTS || []); };
        s.onerror = function () { /* offline or missing: home link only */ };
        document.head.appendChild(s);
    }

    /* Manifest slugs are site-rooted ("blog/<file>.html"); match the tail
       so previews under any base path still find the current post. */
    function findCurrent(posts) {
        for (var i = 0; i < posts.length; i++) {
            if (posts[i].slug && location.pathname.endsWith('/' + posts[i].slug)) {
                return posts[i];
            }
        }
        return null;
    }

    function addArrows(posts) {
        var published = posts.filter(function (p) {
            return p.status !== 'wip' && p.slug && p.no && p.title;
        }).sort(function (a, b) {
            return (parseInt(a.no, 10) || 0) - (parseInt(b.no, 10) || 0);
        });
        var index = published.indexOf(findCurrent(posts));
        if (index < 0) return; /* unlisted draft: the home link is enough */

        function arrow(post, dir) {
            var label = dir === 'prev'
                ? option('prev-label', 'Previous curiosity')
                : option('next-label', 'Next curiosity');
            var a = document.createElement('a');
            a.className = 'vb-post-arrow vb-post-arrow--' + dir;
            a.href = post.slug.split('/').pop(); /* sibling file in blog/ */
            a.rel = dir;
            a.setAttribute('aria-label', label + ': ' + post.title);
            a.setAttribute('data-title', label + ' \u00b7 ' + post.title);
            var glyph = document.createElement('b');
            glyph.setAttribute('aria-hidden', 'true');
            glyph.textContent = dir === 'prev' ? '\u2039' : '\u203a';
            a.appendChild(glyph);
            return a;
        }

        var chrome = document.querySelector('.vb-post-chrome');
        var home = document.querySelector('.vb-post-home');
        if (!chrome || !home) return;
        var prev = published[index - 1];
        var next = published[index + 1];
        if (prev) chrome.insertBefore(arrow(prev, 'prev'), home);
        if (next) chrome.insertBefore(arrow(next, 'next'), home.nextSibling);
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
})();
