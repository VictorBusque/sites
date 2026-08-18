/* ==========================================================================
   site.js — shared site behaviors (chrome + reveals + legacy figures)
   --------------------------------------------------------------------------
   Shared components (embedded chrome):  [data-vb-nav] / [data-vb-footer]
       the nav, footer and fixed chrome (#progress, cursor) are rendered
       here, once, into every page — pages only keep mount points.
   Scroll reveals:                       .reveal / .stagger / .mask
   Legacy figures:                       .fig > .fig-body
       looping figures get PAUSE / REPLAY; scripted figures get
       PREV / PLAY / NEXT / RESET (window.__figScripts).
   Sticky scenes (scrollytelling posts) are handled by the dedicated scene
   module, js/scene.js — load it after this file. See that file for the
   step-card / progress / data-active-step contract.
   ========================================================================== */

(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    /* ── Shared components (embedded chrome) ─────────────
       Nav and footer are written once, here, and rendered into every
       page. Mount points replace the hand-copied markup:

         <div data-vb-nav data-active="about"
              data-status="POST 01" data-status-em="AI-BASICS"></div>
         <div data-vb-footer data-label="POST 01 · TOKEN BY TOKEN"></div>

       data-active   posts | latest | about → aria-current="page"
       data-status   mono prefix (optional)   data-status-em  bold tail
       Links are root-relative (the site is served from the domain root,
       like the /img/ favicons). Keep a <noscript> link row inside a mount
       as the no-JS fallback — this block only runs with JS. */
    (function () {
        /* fixed chrome first, so #progress exists for the scroller below */
        if (!document.getElementById('progress')) {
            [['progress', 'progress'], ['cDot', 'cursor-dot'], ['cRing', 'cursor-ring']]
                .forEach(function (pair) {
                    var el = document.createElement('div');
                    el.id = pair[0];
                    el.className = pair[1];
                    document.body.appendChild(el);
                });
        }

        document.querySelectorAll('[data-vb-nav]').forEach(function (mount) {
            var active = mount.getAttribute('data-active');
            var status = mount.getAttribute('data-status') || '';
            var em = mount.getAttribute('data-status-em') || '';
            /* Links are relative to the current page so they work over http and
               file:// (which reports an absolute filesystem path in pathname,
               unusable for depth). Depth is declared on the mount:
               data-depth="0" at the site root, "1" one folder down (blog/). */
            var depth = parseInt(mount.getAttribute('data-depth') || '0', 10) || 0;
            var pre = depth ? new Array(depth + 1).join('../') : '';
            var home = pre + 'index.html';
            function link(href, key, label) {
                return '<a href="' + href + '"' + (active === key ? ' aria-current="page"' : '') + '>' + label + '</a>';
            }
            var html = '<a class="logo" href="' + home + '">VB<i></i></a><div class="links">'
                + link(home + '#posts', 'posts', 'Posts')
                + link(pre + 'about.html', 'about', 'About')
                + '<button class="motion-toggle" type="button" aria-pressed="false">Motion: on</button>'
                + '</div>';
            if (status || em) {
                html += '<div class="status">' + (status ? status + ' / ' : '') + (em ? '<b>' + em + '</b>' : '') + '</div>';
            }
            var nav = document.createElement('nav');
            nav.innerHTML = html;
            mount.replaceWith(nav);
        });

        document.querySelectorAll('[data-vb-footer]').forEach(function (mount) {
            var label = mount.getAttribute('data-label') || '';
            var foot = document.createElement('footer');
            foot.innerHTML = '<div class="footer-big mask">'
                + '<span class="row"><span>BUILD.</span></span>'
                + '<span class="row"><span>BREAK.</span></span>'
                + '<span class="row"><span><em>EXPLAIN.</em></span></span>'
                + '</div><div class="foot"><span>© ' + new Date().getFullYear()
                + ' VÍCTOR BUSQUÉ</span><span>' + label + '</span></div>';
            mount.replaceWith(foot);
        });

        /* Every page that has a document body gets a reliable keyboard route
           past the shared navigation. A page only needs semantic <main> — no
           per-page link markup. */
        var main = document.querySelector('main');
        if (main && !document.querySelector('.skip-link')) {
            if (!main.id) main.id = 'main-content';
            var skip = document.createElement('a');
            skip.className = 'skip-link';
            skip.href = '#' + main.id;
            skip.textContent = 'Skip to content';
            document.body.insertBefore(skip, document.body.firstChild);
        }
    })();

    /* ── Scroll progress ─────────────────────────────────── */
    var progress = document.getElementById('progress');
    var progressTicking = false;
    var nativeScrollProgress = window.CSS && window.CSS.supports &&
        window.CSS.supports('animation-timeline: scroll(root block)');
    function onScroll() {
        if (progressTicking) return;
        progressTicking = true;
        requestAnimationFrame(function () {
            progressTicking = false;
            if (!progress) return;
            var h = document.documentElement;
            var max = h.scrollHeight - h.clientHeight;
            progress.style.transform = 'scaleX(' + (max > 0 ? h.scrollTop / max : 0) + ')';
        });
    }
    if (!nativeScrollProgress) {
        addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Intersection reveals ────────────────────────────── */
    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) {
            es.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.classList.add('seen');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: .15 });
        document.querySelectorAll('.reveal, .stagger').forEach(function (x) { io.observe(x); });

        /* ── Masked line reveals ─────────────────────────── */
        var maskIO = new IntersectionObserver(function (es) {
            es.forEach(function (e) {
                if (e.isIntersecting) {
                    e.target.querySelectorAll('.row > span').forEach(function (s) { s.style.transform = 'translateY(0)'; });
                    maskIO.unobserve(e.target);
                }
            });
        }, { threshold: .25 });
        document.querySelectorAll('.mask').forEach(function (x) { maskIO.observe(x); });
    } else {
        /* Old browsers get the complete document, never a partly hidden one. */
        document.querySelectorAll('.reveal, .stagger').forEach(function (x) { x.classList.add('seen'); });
        document.querySelectorAll('.mask .row > span').forEach(function (x) { x.style.transform = 'translateY(0)'; });
    }

    /* ── Marquee: duplicate for a seamless loop ──────────── */
    document.querySelectorAll('.marquee-track').forEach(function (t) { t.innerHTML += t.innerHTML; });

    /* ── Mobile nav menu ────────────────────────────────── */
    (function () {
        var nav = document.querySelector('nav');
        if (!nav || nav.querySelector('.nav-toggle')) return;
        var links = nav.querySelector('.links');
        if (!links) return;

        if (!links.id) links.id = 'nav-links';
        Array.prototype.forEach.call(links.children, function (a, i) {
            a.style.setProperty('--i', i);
        });

        var btn = document.createElement('button');
        btn.className = 'nav-toggle';
        btn.type = 'button';
        btn.setAttribute('aria-label', 'Menu');
        btn.setAttribute('aria-expanded', 'false');
        btn.setAttribute('aria-controls', links.id);
        btn.innerHTML = '<span class="nav-toggle-icon" aria-hidden="true"><i></i><i></i><i></i></span>';
        nav.appendChild(btn);

        var mobileNav = window.matchMedia('(max-width: 850px)');
        function setOpen(open) {
            /* A visually collapsed menu must not stay in the tab order.
               On desktop the links are always available, regardless of
               which state the mobile menu had before a resize. */
            var shouldOpen = mobileNav.matches && open;
            nav.classList.toggle('is-open', shouldOpen);
            btn.classList.toggle('is-open', shouldOpen);
            btn.setAttribute('aria-expanded', shouldOpen ? 'true' : 'false');
            btn.setAttribute('aria-label', shouldOpen ? 'Close menu' : 'Menu');
            links.inert = mobileNav.matches && !shouldOpen;
        }
        btn.addEventListener('click', function () {
            setOpen(!nav.classList.contains('is-open'));
        });
        nav.addEventListener('click', function (e) {
            if (e.target.closest('a')) setOpen(false);
        });
        addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && nav.classList.contains('is-open')) setOpen(false);
        });
        function syncNav() { setOpen(false); }
        if (mobileNav.addEventListener) mobileNav.addEventListener('change', syncNav);
        else if (mobileNav.addListener) mobileNav.addListener(syncNav);
        setOpen(false);
    })();

    /* ── Reader motion preference ───────────────────────── */
    (function () {
        var key = 'vb-motion-paused';
        var root = document.documentElement;
        var paused = false;
        try { paused = window.localStorage.getItem(key) === 'true'; } catch (ignore) {}
        function apply() {
            root.classList.toggle('vb-motion-paused', paused);
            document.querySelectorAll('.motion-toggle').forEach(function (button) {
                button.setAttribute('aria-pressed', paused ? 'true' : 'false');
                button.textContent = paused ? 'Motion: off' : 'Motion: on';
            });
        }
        document.querySelectorAll('.motion-toggle').forEach(function (button) {
            button.addEventListener('click', function () {
                paused = !paused;
                try { window.localStorage.setItem(key, String(paused)); } catch (ignore) {}
                apply();
            });
        });
        apply();
    })();

    /* ── Custom cursor ───────────────────────────────────── */
    if (finePointer && !reduceMotion) {
        var dot = document.getElementById('cDot');
        var ring = document.getElementById('cRing');
        if (dot && ring) {
            var mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
            addEventListener('mousemove', function (e) {
                mx = e.clientX;
                my = e.clientY;
                dot.style.left = mx + 'px';
                dot.style.top = my + 'px';
            }, { passive: true });
            (function follow() {
                rx += (mx - rx) * .16;
                ry += (my - ry) * .16;
                ring.style.left = rx + 'px';
                ring.style.top = ry + 'px';
                requestAnimationFrame(follow);
            })();
            document.querySelectorAll('a, button, .tag, .fig-btn').forEach(function (el) {
                el.addEventListener('mouseenter', function () { ring.classList.add('is-hot'); });
                el.addEventListener('mouseleave', function () { ring.classList.remove('is-hot'); });
            });
        }
    }

    /* ── Responsive figure framing ───────────────────────────
       Full-bleed SVGs may declare a tighter mobile frame with
       data-vb-narrow="minX minY w h". Below 850px the engine swaps
       the viewBox (reframed/zoomed, never shrunken) and restores it
       on resize. Font bumps and canvas aspect live in each page's
       media query. */
    (function () {
        var mq = window.matchMedia('(max-width: 850px)');
        var svgs = document.querySelectorAll('[data-vb-narrow]');
        svgs.forEach(function (s) {
            if (s._vbWide === undefined) s._vbWide = s.getAttribute('viewBox');
        });
        function applyVB() {
            svgs.forEach(function (s) {
                s.setAttribute('viewBox', mq.matches ? s.getAttribute('data-vb-narrow') : s._vbWide);
            });
        }
        applyVB();
        if (mq.addEventListener) mq.addEventListener('change', applyVB);
        else if (mq.addListener) mq.addListener(applyVB);
    })();

    /* ── Figure engine (legacy — about.html only) ───────────
       Sticky scenes are handled by js/scene.js (loaded after this file). */
    var scripts = window.__figScripts = window.__figScripts || {};

    function makeBtn(label) {
        var b = document.createElement('button');
        b.className = 'fig-btn';
        b.type = 'button';
        b.textContent = label;
        return b;
    }

    document.querySelectorAll('.fig').forEach(function (fig) {
        var body = fig.querySelector('.fig-body');
        if (!body) return;
        var head = fig.querySelector('.fig-head');
        if (!head) return;

        var controls = fig.querySelector('.fig-controls');
        if (!controls) {
            controls = document.createElement('div');
            controls.className = 'fig-controls';
            head.appendChild(controls);
        }
        var readout = fig.querySelector('.fig-readout');
        var name = body.getAttribute('data-script');

        if (name) {
            /* ── Scripted figure ── */
            var s = scripts[name];
            if (!s || !s.draw) return;
            var i = 0, playing = false, timer = null;
            var autoplay = body.hasAttribute('data-autoplay');
            var loop = body.hasAttribute('data-loop');
            var speed = parseInt(body.getAttribute('data-speed'), 10) || 950;

            var prevBtn = makeBtn('PREV');
            var playBtn = makeBtn('PLAY');
            var nextBtn = makeBtn('NEXT');
            var resetBtn = makeBtn('RESET');
            controls.appendChild(prevBtn);
            controls.appendChild(playBtn);
            controls.appendChild(nextBtn);
            controls.appendChild(resetBtn);

            function note(k) {
                return s.label ? s.label(k) : 'STEP ' + (k + 1) + ' / ' + s.steps;
            }
            function update() {
                prevBtn.disabled = i === 0;
                nextBtn.disabled = i >= s.steps - 1 && !loop;
                if (readout) readout.textContent = note(i);
            }
            function render(k) {
                i = k < 0 ? 0 : (k >= s.steps ? s.steps - 1 : k);
                var out = s.draw(i, body);
                if (readout && typeof out === 'string') readout.textContent = out;
                update();
            }
            function stop() {
                playing = false;
                if (timer) clearInterval(timer);
                timer = null;
                playBtn.textContent = 'PLAY';
                playBtn.classList.remove('is-active');
            }
            function play() {
                if (playing) { stop(); return; }
                playing = true;
                playBtn.textContent = 'PAUSE';
                playBtn.classList.add('is-active');
                timer = setInterval(function () {
                    if (i >= s.steps - 1) {
                        if (loop) { render(0); return; }
                        stop();
                        return;
                    }
                    render(i + 1);
                }, speed);
            }
            prevBtn.addEventListener('click', function () { stop(); render(i - 1); });
            nextBtn.addEventListener('click', function () { stop(); render(i + 1); });
            playBtn.addEventListener('click', play);
            resetBtn.addEventListener('click', function () { stop(); render(0); });

            render(0);
            if (autoplay && !reduceMotion) {
                var started = false;
                var autoIO = new IntersectionObserver(function (es) {
                    es.forEach(function (e) {
                        if (e.isIntersecting && !started) {
                            started = true;
                            play();
                            autoIO.unobserve(body);
                        }
                    });
                }, { threshold: .3 });
                autoIO.observe(body);
            }
        } else {
            /* ── Looping figure ── */
            var pauseBtn = makeBtn('PAUSE');
            var replayBtn = makeBtn('REPLAY');
            controls.appendChild(pauseBtn);
            controls.appendChild(replayBtn);

            pauseBtn.addEventListener('click', function () {
                var paused = fig.classList.toggle('is-paused');
                pauseBtn.classList.toggle('is-active', paused);
                pauseBtn.textContent = paused ? 'RESUME' : 'PAUSE';
            });
            replayBtn.addEventListener('click', function () {
                fig.classList.add('is-restarting');
                void body.offsetWidth;
                fig.classList.remove('is-restarting');
            });
        }
    });
})();
