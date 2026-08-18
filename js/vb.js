/* ==========================================================================
   vb.js — tiny shared utilities for page scripts
   --------------------------------------------------------------------------
   Small, general-purpose helpers that posts reach for over and over: HTML
   escaping for computed text, a deterministic seeded PRNG, motion
   choreography (retrigger / count-up), reduced-motion detection, and a few
   number formatters (pct / ordinal / superscript). Centralized here so no
   article re-implements them by hand — the site's "every article works the
   same" rule extends to helpers, not just scene wiring.

   Everything lives on one namespace, window.VB:

     VB.reduceMotion   boolean — (prefers-reduced-motion: reduce) at load
     VB.esc(str)       HTML-escape &, <, >, quotes for safe computed HTML
     VB.mulberry32(seed) → fn() deterministic float PRNG in [0,1)
     VB.fmt.pct(p[, d])   d=0..100 → "88.2%"
     VB.fmt.ordinal(n)    21 → "ST", 3 → "RD"  (n≥1)
     VB.fmt.sup(n)        1024 → "¹⁰²⁴"         (negative → ⁻ prefix)
     VB.motion.retrig(el, cls)   force-restart a CSS animation class
     VB.motion.countUp(el, txt[, opts])
         animate a numeric textContent from 0 to parseFloat(txt)
         opts: { ms: 480, digits: 1 } — reduced-motion → set instantly

   Load: js/site.js and js/scene.js use defer (in that order), but this file
   loads WITHOUT defer, right after them in <head>. Page scripts run during
   parsing (before deferred scripts execute), so the helpers must already be
   on window.VB. This file never touches window.VBScene, so synchronous
   loading is safe. To register scene reactions from a page script, use
   VB.onReady(fn) — it runs fn once the deferred js/scene.js has mounted
   window.VBScene (usually at DOMContentLoaded), so no hand-rolled
   MutationObserver on data-active-step.
   ========================================================================== */
(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* HTML-escape computed strings before writing them into innerHTML. */
    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    /* Deterministic seeded PRNG (mulberry32) — identical sequence for the
       same seed, so sampled/randomized page state is reproducible. */
    function mulberry32(seed) {
        var a = seed | 0;
        return function () {
            a |= 0; a = a + 0x6D2B79F5 | 0;
            var t = Math.imul(a ^ a >>> 15, 1 | a);
            t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
            return ((t ^ t >>> 14) >>> 0) / 4294967296;
        };
    }

    /* ── number formatters ── */
    function pct(p, digits) {
        return (p * 100).toFixed(digits == null ? 1 : digits) + '%';
    }
    function ordinal(n) {
        var s = ['TH', 'ST', 'ND', 'RD'], v = n % 100;
        return s[(v - 20) % 10] || s[v] || s[0];
    }
    function sup(n) {
        var D = '⁰¹²³⁴⁵⁶⁷⁸⁹';
        return (n < 0 ? '⁻' : '') + String(Math.abs(n)).split('').map(function (c) { return D[+c]; }).join('');
    }

    /* ── motion choreography helpers ──
       retrig(el, cls) removes then re-adds a class after a forced reflow,
       so a CSS animation restarts from its beginning. */
    function retrig(el, cls) {
        el.classList.remove(cls);
        void el.offsetWidth;
        el.classList.add(cls);
    }

    /* countUp(el, txt) animates a numeric textContent from 0 up to
       parseFloat(txt) over ~480ms (eased), then sets the exact string.
       Non-numeric or reduced-motion → set instantly. Safe to re-call:
       a later call cancels the earlier one. */
    function countUp(el, txt, opts) {
        opts = opts || {};
        var target = parseFloat(txt);
        if (reduceMotion || isNaN(target)) { el.textContent = txt; return; }
        var ms = opts.ms || 480;
        var digits = opts.digits == null ? 1 : opts.digits;
        var id = (el._vbCountUpId || 0) + 1;
        el._vbCountUpId = id;
        (function frame(t) {
            if (id !== el._vbCountUpId) return;
            var k = Math.max(0, Math.min(1, (t - t0) / ms));
            var e = 1 - Math.pow(1 - k, 3);
            el.textContent = (target * e).toFixed(digits) + '%';
            if (k < 1) requestAnimationFrame(frame);
            else el.textContent = txt;
        })(t0);
    }

    /* onReady(fn) — run fn once the scene module (window.VBScene) exists.
       js/scene.js is deferred, so it mounts after page scripts run; this
       queues fn until DOMContentLoaded, which the spec guarantees fires
       only after the deferred scripts execute. */
    function onReady(fn) {
        if (window.VBScene) { fn(); return; }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function () { fn(); });
        } else if (window.VBScene) {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', function () { fn(); });
        }
    }

    window.VB = {
        reduceMotion: reduceMotion,
        esc: esc,
        mulberry32: mulberry32,
        fmt: { pct: pct, ordinal: ordinal, sup: sup },
        motion: { retrig: retrig, countUp: countUp },
        onReady: onReady
    };
})();
