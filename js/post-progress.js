/*
 * post-progress.js — the only shared article chrome.
 *
 * Include once in a top-level post with:
 *   <script src="../js/post-progress.js" defer></script>
 * (Use ../../js/post-progress.js from blog/not-ready/.)
 * Set its palette on <body> (or <html>):
 *   data-vb-progress-start="#80e7ff"
 *   data-vb-progress-mid="#b9a0ff"   (optional)
 *   data-vb-progress-end="#bdf58b"
 *
 * The bar is decorative: it reports document position but is not required
 * to read or navigate the article.
 */
(function () {
    'use strict';

    function start() {
        if (document.querySelector('.vb-scroll-progress')) return;

        var root = document.documentElement;
        var config = document.body || root;
        var bar = document.createElement('div');
        var fill = document.createElement('i');
        var ticking = false;

        bar.className = 'vb-scroll-progress';
        bar.setAttribute('aria-hidden', 'true');
        bar.appendChild(fill);
        document.body.insertBefore(bar, document.body.firstChild);

        [
            ['start', '--vb-progress-start'],
            ['mid', '--vb-progress-mid'],
            ['end', '--vb-progress-end']
        ].forEach(function (pair) {
            var value = config.getAttribute('data-vb-progress-' + pair[0]) || root.getAttribute('data-vb-progress-' + pair[0]);
            if (value) bar.style.setProperty(pair[1], value);
        });

        function paint() {
            ticking = false;
            var documentElement = document.documentElement;
            var maximum = documentElement.scrollHeight - documentElement.clientHeight;
            var progress = maximum > 0 ? Math.min(1, Math.max(0, window.scrollY / maximum)) : 0;
            fill.style.transform = 'scaleX(' + progress + ')';
        }

        function requestPaint() {
            if (ticking) return;
            ticking = true;
            window.requestAnimationFrame(paint);
        }

        window.addEventListener('scroll', requestPaint, { passive: true });
        window.addEventListener('resize', requestPaint, { passive: true });
        window.addEventListener('pageshow', requestPaint, { passive: true });
        window.setTimeout(paint, 0);
        paint();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
    else start();
})();
