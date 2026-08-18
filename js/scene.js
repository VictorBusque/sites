/* ==========================================================================
   scene.js — the scrollytelling scene module
   --------------------------------------------------------------------------
   Single source of truth for sticky scenes on this site. Any article that
   ships a <section class="sticky-scene"> gets identical behavior from this
   module — no per-page scene JS needed:

     · wraps each .step's content in a .step-card
     · injects a .step-progress rail into each card (mobile bottom sheet)
     · toggles .is-active while a step crosses its activation window
     · sets data-active-step on the section (pages key stage states off it)
     · fills [data-readout] with 'STEP k / n'
     · measures the tallest step card and exposes --card-reserve so the
       mobile diagram centers above the bottom-docked card and never runs
       underneath it

   Presentation (the bottom-sheet card, the rise/fade choreography, the
   progress rail) lives in css/site.css — this module only toggles classes
   and CSS variables. It is the "every article works the same" contract:
   write the scene markup from blog/template.html and the behavior is done.

   Load AFTER js/site.js, with defer, in every page:
     <script src="../js/site.js" defer></script>
     <script src="../js/scene.js" defer></script>

   Optional hook for page scripts: window.VBScene.onStep(fn) — fn(sceneEl,
   stepEl, index, total) is called each time a step becomes active. Page
   scripts that must react to step changes (e.g. apply a computed state)
   may use it, or keep watching data-active-step via a MutationObserver.
   ========================================================================== */
(function () {
    'use strict';

    var portraitMob = window.matchMedia('(max-width: 850px) and (min-height: 521px)');

    /* each scene is one observer; steps are exclusive (one card active) */
    function wireScene(scene) {
        var steps = scene.querySelectorAll('[data-step]');
        if (!steps.length) return;
        var readout = scene.querySelector('[data-readout]');
        var total = steps.length;

        /* Portrait phones dock the card at the bottom, so a step must stay
           active for a much wider scroll window than the desktop middle
           band — otherwise the text vanishes after a few vh of scroll. */
        var band = portraitMob.matches ? '-20% 0px -20% 0px' : '-45% 0px -45% 0px';

        /* A step card only reads well once the stage is pinned. While the
           stage is still scrolling into place, the first step overlaps its
           activation window early, so its card is caught mid-fade, off its
           settled position — barely readable. Every later step activates
           only once the stage is already pinned, which is why they look
           right. So we never light a card until the stage has reached the
           top of the viewport, and we bootstrap the first (or any missed)
           step the moment it does. */
        function stagePinned() {
            var stage = scene.querySelector('.sticky-scene__stage');
            return !stage || stage.getBoundingClientRect().top <= 0;
        }
        /* engaged = a card is lit while the stage is pinned. Reset whenever
           the stage scrolls away, so re-entering the scene re-bootstraps. */
        var engaged = false;
        function activate(step) {
            /* exclusive: only one step card is active at a time */
            steps.forEach(function (s) { s.classList.remove('is-active'); });
            step.classList.add('is-active');
            scene.dataset.activeStep = step.getAttribute('data-step');
            if (readout) {
                readout.textContent = 'STEP ' + step.getAttribute('data-step') + ' / ' + total;
            }
            /* the mobile progress rail sweeps to this step's place */
            var fill = step.querySelector('.step-progress i');
            if (fill) {
                var pi = parseInt(step.getAttribute('data-step'), 10) || 1;
                fill.style.width = (total > 1 ? ((pi - 1) / (total - 1)) * 100 : 100) + '%';
            }
            engaged = true;
            /* let page hooks react (window.VBScene.onStep) */
            notifyHooks(scene, step, total);
        }

        var io = new IntersectionObserver(function (es) {
            es.forEach(function (e) {
                /* wait until the stage is pinned; the observer re-fires on
                   later band entries (steps 2..n) once it is */
                if (!e.isIntersecting || !stagePinned()) return;
                activate(e.target);
            });
        }, { rootMargin: band });

        /* While the stage pins, step 1 was deliberately blocked — so its
           card would otherwise stay dark until a later band entry fires. As
           soon as the stage reaches the top, light the step sitting at the
           viewport center, then hand back to the observer. Running only
           while nothing is engaged keeps it from racing the observer during
           normal scroll (it never re-flips a step the observer already
           set). */
        var ticking = false;
        function bootstrap() {
            if (engaged || !stagePinned()) return;
            var c = innerHeight / 2;
            for (var i = 0; i < steps.length; i++) {
                var r = steps[i].getBoundingClientRect();
                if (r.top <= c && r.bottom >= c) {
                    activate(steps[i]);
                    return;
                }
            }
        }
        function onScroll() {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () {
                ticking = false;
                if (!stagePinned()) engaged = false; /* stage scrolled away */
                bootstrap();
            });
        }
        addEventListener('scroll', onScroll, { passive: true });
        addEventListener('resize', onScroll);
        bootstrap(); /* in case the scene is already in view on load */

        steps.forEach(function (s) {
            /* The article is a full-height transparent track over the pinned
               stage; its content is wrapped in .step-card, the visual card
               (see css/site.css). The wrap exists only with JS — the no-JS
               document keeps .step as a plain card. */
            if (!s.querySelector(':scope > .step-card')) {
                var card = document.createElement('div');
                card.className = 'step-card';
                /* mobile bottom-sheet progress rail (hidden on desktop) */
                var prog = document.createElement('div');
                prog.className = 'step-progress';
                prog.innerHTML = '<i></i>';
                card.appendChild(prog);
                while (s.firstChild) card.appendChild(s.firstChild);
                s.appendChild(card);
            }
            io.observe(s);
        });
    }

    /* On portrait phones the step card docks at the bottom of the pinned
       stage, so the diagram must center in the space above it and never run
       underneath (which is what cropped it). Measure the tallest card and
       expose its height + breathing room as --card-reserve on the stage;
       the portrait CSS pads the diagram with that value and centers it.
       Desktop and landscape ignore this. */
    function measureCardReserve() {
        if (!portraitMob.matches) return;
        document.querySelectorAll('.sticky-scene').forEach(function (scene) {
            var stage = scene.querySelector('.sticky-scene__stage');
            if (!stage) return;
            var max = 0;
            scene.querySelectorAll('.step-card').forEach(function (c) {
                var h = c.getBoundingClientRect().height;
                if (h > max) max = h;
            });
            /* card bottom gap (18px) + a little air above it */
            stage.style.setProperty('--card-reserve', (max + 30) + 'px');
        });
    }

    /* optional page hooks */
    var hooks = [];
    function notifyHooks(scene, step, total) {
        for (var i = 0; i < hooks.length; i++) {
            hooks[i](scene, step, parseInt(step.getAttribute('data-step'), 10), total);
        }
    }

    function init() {
        document.querySelectorAll('.sticky-scene').forEach(wireScene);
        measureCardReserve();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init(); /* defer scripts run after parse → DOM is ready */
    }

    window.VBScene = {
        init: init,
        refresh: measureCardReserve,
        onStep: function (fn) { if (typeof fn === 'function') hooks.push(fn); }
    };
    addEventListener('resize', measureCardReserve);
    addEventListener('orientationchange', measureCardReserve);
    addEventListener('load', measureCardReserve);
})();
