/* ==========================================================================
   site.js — shared behaviors + figure engine
   --------------------------------------------------------------------------
   Looping figures (CSS choreography):  .fig > .fig-body
       get PAUSE / REPLAY controls in the head bar.
   Scripted figures:                    .fig > .fig-body[data-script="name"]
       the page registers window.__figScripts["name"] = { steps, draw, label? }
       get PREV / PLAY / NEXT / RESET controls.
       data-autoplay  → starts playing when first visible
       data-loop      → wraps to step 0 after the last step
       data-speed     → ms per step (default 950)
   draw(i, body) renders step i into the figure body and may return a string
   to display in the .fig-readout element.
   ========================================================================== */

(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    /* ── Scroll progress ─────────────────────────────────── */
    var progress = document.getElementById('progress');
    function onScroll() {
        if (!progress) return;
        var h = document.documentElement;
        var max = h.scrollHeight - h.clientHeight;
        progress.style.transform = 'scaleX(' + (max > 0 ? h.scrollTop / max : 0) + ')';
    }
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    /* ── Intersection reveals ────────────────────────────── */
    var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
            if (e.isIntersecting) {
                e.target.classList.add('seen');
                io.unobserve(e.target);
            }
        });
    }, { threshold: .15 });
    document.querySelectorAll('.reveal, .stagger').forEach(function (x) { io.observe(x); });

    /* ── Masked line reveals ─────────────────────────────── */
    var maskIO = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
            if (e.isIntersecting) {
                e.target.querySelectorAll('.row > span').forEach(function (s) { s.style.transform = 'translateY(0)'; });
                maskIO.unobserve(e.target);
            }
        });
    }, { threshold: .25 });
    document.querySelectorAll('.mask').forEach(function (x) { maskIO.observe(x); });

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

        function setOpen(open) {
            nav.classList.toggle('is-open', open);
            btn.classList.toggle('is-open', open);
            btn.setAttribute('aria-expanded', open ? 'true' : 'false');
            btn.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
            links.inert = !open;
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

    /* ── Figure engine ───────────────────────────────────── */
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
