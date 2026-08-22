#!/usr/bin/env python3
"""Restyle the article with a Google-Maps-flavored light skin: light map
stages with white roads and yellow arterials, the Maps-blue route line,
red destination pin and blue origin dot, traffic-red jams, Roboto +
Roboto Mono, Material cards. Structural contracts (sticky scenes, step
cards, mobile bottom sheet, reduced-motion collapse) are unchanged."""
import re

s = open('article_src.html', encoding='utf-8').read()

CSS = """
/* ════════════════════════════════════════════════════════════════════
   THE FLOOD AND THE ARROW — the Google Maps skin.
   The subject is a navigation app, so the article wears one: light map
   canvases with white roads and yellow arterials, the Maps-blue route,
   a red destination pin and a blue origin dot, traffic-red jams, and
   Roboto on Material cards. Skeleton contracts (sticky scenes, step
   cards, mobile bottom sheet, reduced-motion collapse) follow the
   site's scaffold; the skin is this article's alone.

   Map coordinates are integers on a ~1 m grid (1e-5°), viewBox width
   ~3,200–4,100 units. Stroke widths below are in those units: at desktop
   scale (~0.3 px/unit) they render as hairlines; the mobile and hero
   blocks below rescale them.
   ════════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Roboto+Mono:wght@400;500&display=swap');

/* ── tokens — the Google palette, scoped to this page ── */
:root {
    --g-blue: #4285f4;
    --g-blue-dark: #1967d2;
    --g-blue-ink: #174ea6;
    --g-blue-deep: #0b39a0;
    --g-red: #ea4335;
    --g-red-deep: #d93025;
    --g-yellow: #fbbc04;
    --g-yellow-deep: #f9ab00;
    --g-green: #34a853;
    --g-green-deep: #188038;
    --g-ink: #202124;
    --g-ink-2: #3c4043;
    --g-ink-3: #5f6368;
    --g-ink-4: #80868b;
    --g-gray-1: #f8f9fa;
    --g-gray-2: #f1f3f4;
    --g-gray-3: #e8eaed;
    --g-line: #dadce0;

    --ink: #202124;
    --paper: #ffffff;
    --paper-2: #f8f9fa;
    --muted: #5f6368;
    --line: #dadce0;

    --stage: #f1f3f4;
    --stage-2: #f8f9fa;
    --grid: #2021240a;

    --ease-out: cubic-bezier(.16, 1, .3, 1);
    --ease-in: cubic-bezier(.55, 0, .85, .36);
    --ease-swift: cubic-bezier(.4, 0, .2, 1);
    --t-fast: 180ms;
    --t-med: 400ms;
    --t-slow: 800ms;

    --shadow-1: 0 1px 2px rgba(60,64,67,.3), 0 1px 3px 1px rgba(60,64,67,.12);
    --shadow-2: 0 1px 3px rgba(60,64,67,.3), 0 4px 12px 2px rgba(60,64,67,.15);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: 84px; }
body {
    background: var(--g-gray-1);
    color: var(--g-ink);
    font: 17px/1.72 "Roboto", Arial, Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
}
::selection { background: var(--g-blue); color: #fff; }
a { color: var(--g-blue-dark); }
.mono, code { font-family: "Roboto Mono", monospace; }

.skip-link {
    position: fixed; left: 12px; top: -60px; z-index: 300;
    background: var(--g-ink); color: #fff;
    font: 11px "Roboto Mono"; letter-spacing: .1em;
    padding: 10px 16px; text-decoration: none; border-radius: 8px;
    transition: top var(--t-fast) var(--ease-out);
}
.skip-link:focus { top: 12px; }

/* ── reveals ── */
.reveal { opacity: 0; transform: translateY(22px); transition: opacity .9s var(--ease-out), transform .9s var(--ease-out); }
.reveal.seen { opacity: 1; transform: none; }

/* ── hero — the app opens on the route ── */
.hero {
    min-height: 100svh; position: relative; overflow: hidden;
    background:
        radial-gradient(1200px 700px at 78% 26%, #e8f0fe 0%, transparent 60%),
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px),
        var(--g-gray-1);
    background-size: auto, 32px 32px, 32px 32px, auto;
    color: var(--g-ink);
    display: grid;
    grid-template-columns: minmax(0, 1.12fr) minmax(0, .88fr);
    align-items: center;
    gap: 4vw;
    padding: 12vh 6vw 10vh;
}
.hero-kicker {
    display: inline-block;
    font: 10px "Roboto Mono"; letter-spacing: .18em; color: var(--g-ink-3);
    background: #fff; border: 1px solid var(--g-line); border-radius: 999px;
    padding: 9px 16px; margin-bottom: 30px; box-shadow: var(--shadow-1);
}
.hero h1 {
    font-family: "Roboto", sans-serif;
    font-weight: 600;
    font-size: clamp(32px, 4.8vw, 60px);
    line-height: 1.08;
    letter-spacing: -.02em;
    color: var(--g-ink);
}
.hero h1 em { font-style: normal; color: var(--g-blue); }
.hero .h-line { display: block; overflow: hidden; }
.hero .h-line > span { display: inline-block; transform: translateY(110%); animation: rise 1s var(--ease-out) forwards; }
.hero .h-line:nth-child(2) > span { animation-delay: .12s; }
.hero .h-line:nth-child(3) > span { animation-delay: .24s; }
@keyframes rise { to { transform: translateY(0); } }
.hero .dek {
    max-width: 54ch; margin-top: 26px;
    font-size: 18px; line-height: 1.65; color: var(--g-ink-3);
    opacity: 0; animation: fade-rise .9s var(--ease-out) .5s forwards;
}
.hero-meta {
    display: flex; gap: 12px 26px; flex-wrap: wrap; margin-top: 32px;
    font: 10px "Roboto Mono"; letter-spacing: .14em; color: var(--g-ink-4);
    opacity: 0; animation: fade-rise .9s var(--ease-out) .7s forwards;
}
.hero-meta b { color: var(--g-ink); font-weight: 500; }
@keyframes fade-rise { to { opacity: 1; } }

/* the hero map plate — a Maps card with the route settled */
.hero-spec {
    position: relative; justify-self: center;
    width: min(34vw, 430px); aspect-ratio: 4/3;
    background: var(--g-gray-2);
    border-radius: 18px; overflow: hidden;
    border: 1px solid var(--g-line);
    box-shadow: var(--shadow-2);
    opacity: 0; transform: scale(.96); animation: spec-in 1.1s var(--ease-out) .35s forwards;
}
@keyframes spec-in { to { opacity: 1; transform: none; } }
.hero-spec svg { display: block; width: 100%; height: 100%; }
.hero-spec-label {
    position: absolute; left: 50%; bottom: -42px; transform: translateX(-50%);
    white-space: nowrap;
    font: 9px "Roboto Mono"; letter-spacing: .16em; color: var(--g-ink-3);
}
.hero-spec-label b { color: var(--g-blue-dark); font-weight: 500; }
.hero-cue {
    position: absolute; left: 50%; bottom: 26px; transform: translateX(-50%);
    width: 1px; height: 44px; background: linear-gradient(#5f636800, #5f636880);
    animation: cue 2.2s var(--ease-swift) infinite;
}
@keyframes cue { 0% { transform: translateX(-50%) scaleY(.4); transform-origin: top; } 55% { transform: translateX(-50%) scaleY(1); } 100% { transform: translateX(-50%) scaleY(.4); } }

/* ── prose ── */
.prose { max-width: 720px; margin: 0 auto; padding: 12vh 4vw 0; }
.prose > p { font-size: 17px; line-height: 1.74; color: var(--g-ink-2); margin-bottom: 1.5em; }
.prose > p strong { font-weight: 600; color: var(--g-ink); }
.prose h2 {
    font-family: "Roboto", sans-serif; font-weight: 600;
    font-size: clamp(24px, 3.2vw, 34px); letter-spacing: -.015em; line-height: 1.15;
    color: var(--g-ink);
    margin: 11vh 0 20px; display: flex; align-items: baseline; gap: 16px;
}
.prose h2 .sec-no { font: 10px "Roboto Mono"; letter-spacing: .14em; color: var(--g-red); align-self: center; }
.prose .callout {
    border-left: 4px solid var(--g-blue);
    background: #e8f0fe;
    border-radius: 4px 14px 14px 4px;
    padding: 22px 26px; margin: 5vh 0;
    font: 500 19px/1.55 "Roboto";
    color: var(--g-blue-ink);
}
.prose .callout em { font-style: normal; color: var(--g-blue-deep); }
.prose .aside {
    font: 10.5px/1.75 "Roboto Mono"; color: var(--g-ink-4);
    border-top: 1px solid var(--g-line); padding-top: 14px; margin: 6vh 0;
}
.prose .aside a { color: var(--g-blue-dark); }

/* ── sticky scenes — the site contract, in a Maps skin ── */
.sticky-scene { position: relative; border-top: 1px solid var(--g-line); border-bottom: 1px solid var(--g-line); margin-top: 10vh; }
.js .sticky-scene { padding-bottom: 100vh; padding-bottom: 100svh; }
.sticky-scene__stage {
    background-color: var(--stage);
    background-image: linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 32px 32px;
    color: var(--g-ink); position: relative; overflow: hidden; min-height: 60vh;
}
.js .sticky-scene__stage { position: sticky; top: 0; height: 100vh; height: 100svh; min-height: 0; }
.scene-head {
    display: flex; align-items: center; gap: 16px;
    border-bottom: 1px solid var(--g-line); padding: 12px 4vw;
    position: relative; z-index: 5;
    background: #fffffff2;
}
.scene-no { font: 10px "Roboto Mono"; letter-spacing: .14em; color: var(--g-red); }
.scene-name { font: 10px "Roboto Mono"; letter-spacing: .18em; color: var(--g-ink-2); }
.scene-readout { font: 10px "Roboto Mono"; color: var(--g-ink-4); margin-left: auto; }
.js .sticky-scene__steps { position: relative; margin-top: -100vh; margin-top: -100svh; pointer-events: none; z-index: 1; }
.js .sticky-scene__steps > * { min-height: 100vh; min-height: 100svh; display: flex; align-items: center; padding: 0 4vw; }
.step { max-width: 420px; background: #fff; border: 1px solid var(--g-line); border-radius: 16px; padding: 24px 26px; color: var(--g-ink); }
.js .step { background: none; border: 0; padding: 0; max-width: none; pointer-events: none; }
.js .step.is-active { pointer-events: auto; }
.step-card {
    width: 100%; max-width: 420px; background: #fff;
    border: 1px solid var(--g-line); border-radius: 16px; padding: 24px 26px;
    color: var(--g-ink); box-shadow: var(--shadow-2);
    opacity: 0; transform: translateY(26px);
    transition: opacity var(--t-slow) var(--ease-out), transform var(--t-slow) var(--ease-out);
}
.js .step.is-active .step-card { opacity: 1; transform: none; }
.step-progress { display: none; }
.step-k { font: 9px "Roboto Mono"; letter-spacing: .16em; color: var(--g-red); display: block; margin-bottom: 10px; }
.step p { font-size: 15.5px; line-height: 1.62; color: var(--g-ink-2); }
.step p + p { margin-top: .8em; }
.step p b { font-weight: 600; color: var(--g-ink); }
.step .mono { font-size: 13px; }

/* stage internals — the article's diagram grammar, in map colors */
.map-stage {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    padding: 66px 2vw 3vh;
}
.map-svg { width: 100%; height: 100%; display: block; }
/* roads on the light map canvas: locals white hairlines, avenues white,
   arterials the classic Maps yellow */
.map-svg .st-loc { stroke: #ffffff; stroke-width: 2.6; fill: none; }
.map-svg .st-ter { stroke: #ffffff; stroke-width: 3.8; fill: none; }
.map-svg .st-art { stroke: #fdd663; stroke-width: 4.6; fill: none; }
.map-svg .st-loc, .map-svg .st-ter, .map-svg .st-art { transition: opacity var(--t-slow) var(--ease-out), stroke var(--t-slow) var(--ease-out); }

/* dots: search state, drawn as round-capped stroked points.
   frontier = deep blue; settled = light blue; ghost = gray */
.map-svg .dots { stroke: #4285f442; stroke-width: 6; fill: none; stroke-linecap: round; transition: opacity var(--t-slow) var(--ease-out), stroke var(--t-med) var(--ease-swift); }
.map-svg .dots.frontier { stroke: var(--g-blue-dark); }
.map-svg .dots.ghost { stroke: #9aa0a638; stroke-width: 3.6; }
/* the route: the Maps blue line */
.map-svg .route {
    stroke: var(--g-blue); stroke-width: 6.5; fill: none;
    stroke-linecap: round; stroke-linejoin: round;
}
.map-svg .route-glow { stroke: #4285f42e; stroke-width: 14; fill: none; stroke-linecap: round; }
.map-svg .route-old { stroke: #4285f470; stroke-width: 4; fill: none; stroke-dasharray: 10 12; }
/* the jammed street: traffic red */
.map-svg .jam-street { stroke: var(--g-red-deep); stroke-width: 5.6; fill: none; }
/* pins: blue origin dot, red destination pin */
.map-svg .pin { fill: var(--g-red); }
.map-svg .pin-o { fill: var(--g-blue-dark); }
.map-svg .pin-d { fill: var(--g-red); }
.map-svg .pin-ring { stroke: var(--g-red); stroke-width: 1.6; fill: none; }
.map-svg .pin-ring.ring-o { stroke: var(--g-blue-dark); }
.map-svg .mlab {
    font: 30px "Roboto Mono"; letter-spacing: .18em; fill: var(--g-ink-2);
    paint-order: stroke; stroke: #fffffff5; stroke-width: 7px;
}
.map-svg .mlab.lab-o { fill: var(--g-blue-dark); }
.map-svg .mlab.lab-d { fill: var(--g-red-deep); }
.map-svg .mlab.mlab-ros { fill: var(--g-red-deep); }
.map-svg .mlab { transition: opacity var(--t-med) var(--ease-out); }
.ring { stroke: #4285f466; stroke-width: 1.6; fill: #4285f40d; stroke-dasharray: 8 10; }

/* chips — Maps-style pills pinned to the stage; JS rewrites the values it
   can compute, the authored values are the verified build-time ones */
.chips {
    position: absolute; top: 62px; right: 3vw; z-index: 4;
    display: flex; flex-direction: column; gap: 8px; align-items: flex-end;
    pointer-events: none;
}
.chip {
    font: 10px "Roboto Mono"; letter-spacing: .12em; color: var(--g-ink-2);
    background: #fffffff2; border: 1px solid var(--g-line); border-radius: 999px;
    padding: 7px 13px; box-shadow: var(--shadow-1);
    opacity: 0; transform: translateY(-6px);
    transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out);
}
.chip b { color: var(--g-green-deep); font-weight: 500; }
.chip.c-blue b { color: var(--g-blue-dark); }
.chip.c-orange b { color: var(--g-red-deep); }

/* no-JS static stage content */
.stage-static { padding: 60px 4vw 40px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.js .stage-static { display: none; }
.static-svg { width: min(52vh, 84vw); height: auto; border: 1px solid var(--g-line); border-radius: 12px; background: var(--g-gray-2); }
.static-note { font: 10px/1.7 "Roboto Mono"; letter-spacing: .1em; color: var(--g-ink-3); text-align: center; max-width: 60ch; }
.static-note b { color: var(--g-blue-dark); font-weight: 500; }

/* ── S01 · layer states (data-active-step keys everything) ── */
#scene1 .dots-v { opacity: 0; stroke: #5f636866; }
#scene1[data-active-step="2"] .dots-v, #scene1[data-active-step="3"] .dots-v,
#scene1[data-active-step="4"] .dots-v, #scene1[data-active-step="5"] .dots-v { opacity: 1; }
#scene1 .ex-edge { stroke: var(--g-blue-dark); stroke-width: 7; fill: none; opacity: 0; }
#scene1[data-active-step="3"] .ex-edge, #scene1[data-active-step="4"] .ex-edge,
#scene1[data-active-step="5"] .ex-edge { opacity: 1; }
#scene1[data-active-step="4"] .st-loc { stroke: #f8f9fa; }
#scene1[data-active-step="4"] .st-art { stroke: var(--g-yellow-deep); }
#scene1[data-active-step="4"] .st-ter { stroke: #aecbfa; }
#scene1 .pin-o, #scene1 .pin-d, #scene1 .pin-ring, #scene1 .mlab { opacity: 0; }
#scene1[data-active-step="1"] .pin-o,
#scene1[data-active-step="5"] .pin-o, #scene1[data-active-step="5"] .pin-d,
#scene1[data-active-step="5"] .pin-ring, #scene1[data-active-step="5"] .mlab { opacity: 1; }
#scene1 .pin-ring { transform-box: fill-box; transform-origin: center; animation: ping 2.8s var(--ease-swift) infinite; }
@keyframes ping {
    0% { transform: scale(.6); opacity: .9; } 70% { transform: scale(1.6); opacity: 0; } 100% { opacity: 0; }
}
#scene1[data-active-step="1"] .chip.c1, #scene1[data-active-step="2"] .chip.c2,
#scene1[data-active-step="3"] .chip.c3, #scene1[data-active-step="4"] .chip.c4,
#scene1[data-active-step="5"] .chip.c5 { opacity: 1; transform: none; }

/* ── S02 · the flood — slices cumulative; newest slice is the frontier ── */
#scene2 .dj { opacity: 0; }
#scene2[data-active-step="2"] .dj-s1, #scene2[data-active-step="3"] .dj-s1, #scene2[data-active-step="4"] .dj-s1, #scene2[data-active-step="5"] .dj-s1,
#scene2[data-active-step="3"] .dj-s2, #scene2[data-active-step="4"] .dj-s2, #scene2[data-active-step="5"] .dj-s2,
#scene2[data-active-step="4"] .dj-s3, #scene2[data-active-step="5"] .dj-s3 { opacity: 1; }
#scene2[data-active-step="2"] .dj-s1 { stroke: var(--g-blue-dark); }
#scene2[data-active-step="3"] .dj-s1, #scene2[data-active-step="4"] .dj-s2, #scene2[data-active-step="5"] .dj-s2 { stroke: #4285f442; }
#scene2[data-active-step="3"] .dj-s2, #scene2[data-active-step="4"] .dj-s3 { stroke: var(--g-blue-dark); }
#scene2[data-active-step="5"] .dj-s3 { stroke: #4285f42e; }
#scene2 .st-loc, #scene2 .st-ter, #scene2 .st-art { opacity: .8; }
#scene2 .route, #scene2 .route-glow { opacity: 0; }
#scene2[data-active-step="5"] .route, #scene2[data-active-step="5"] .route-glow { opacity: 1; }
#scene2 .route { stroke-dasharray: 3600; stroke-dashoffset: 3600; }
#scene2[data-active-step="5"] .route { animation: draw 1.1s var(--ease-out) forwards; }
#scene2 .route-glow { stroke-dasharray: 3600; stroke-dashoffset: 3600; }
#scene2[data-active-step="5"] .route-glow { animation: draw 1.1s var(--ease-out) forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
#scene2[data-active-step="1"] .chip.c1, #scene2[data-active-step="2"] .chip.c2,
#scene2[data-active-step="3"] .chip.c3, #scene2[data-active-step="4"] .chip.c4,
#scene2[data-active-step="5"] .chip.c5 { opacity: 1; transform: none; }

/* ── S03 · the arrow ── */
#scene3 .as { opacity: 0; }
#scene3[data-active-step="2"] .as-s1, #scene3[data-active-step="3"] .as-s1, #scene3[data-active-step="4"] .as-s1, #scene3[data-active-step="5"] .as-s1,
#scene3[data-active-step="3"] .as-s2, #scene3[data-active-step="4"] .as-s2, #scene3[data-active-step="5"] .as-s2,
#scene3[data-active-step="4"] .as-s3, #scene3[data-active-step="5"] .as-s3 { opacity: 1; }
#scene3[data-active-step="2"] .as-s1 { stroke: var(--g-blue-dark); }
#scene3[data-active-step="3"] .as-s1, #scene3[data-active-step="4"] .as-s2, #scene3[data-active-step="5"] .as-s2 { stroke: #4285f442; }
#scene3[data-active-step="3"] .as-s2, #scene3[data-active-step="4"] .as-s3 { stroke: var(--g-blue-dark); }
#scene3[data-active-step="5"] .as-s3 { stroke: #4285f42e; }
#scene3 .ghost { opacity: 0; }
#scene3[data-active-step="3"] .ghost, #scene3[data-active-step="4"] .ghost, #scene3[data-active-step="5"] .ghost { opacity: 1; }
#scene3 .route, #scene3 .route-glow { opacity: 0; }
#scene3[data-active-step="4"] .route, #scene3[data-active-step="4"] .route-glow,
#scene3[data-active-step="5"] .route, #scene3[data-active-step="5"] .route-glow { opacity: 1; }
#scene3 .st-loc, #scene3 .st-ter, #scene3 .st-art { opacity: .8; }
#scene3[data-active-step="1"] .chip.c1, #scene3[data-active-step="2"] .chip.c2,
#scene3[data-active-step="3"] .chip.c3, #scene3[data-active-step="4"] .chip.c4,
#scene3[data-active-step="5"] .chip.c5 { opacity: 1; transform: none; }

/* ── S04 · the skeleton ── */
#scene4 .ring, #scene4 .dots-h { opacity: 0; }
#scene4[data-active-step="3"] .ring, #scene4[data-active-step="4"] .ring, #scene4[data-active-step="5"] .ring,
#scene4[data-active-step="3"] .dots-h, #scene4[data-active-step="4"] .dots-h, #scene4[data-active-step="5"] .dots-h { opacity: 1; }
#scene4[data-active-step="3"] .st-loc, #scene4[data-active-step="4"] .st-loc, #scene4[data-active-step="5"] .st-loc { opacity: .22; }
#scene4[data-active-step="3"] .st-art, #scene4[data-active-step="4"] .st-art, #scene4[data-active-step="5"] .st-art { stroke: var(--g-yellow-deep); stroke-width: 6; }
#scene4[data-active-step="3"] .st-ter, #scene4[data-active-step="4"] .st-ter, #scene4[data-active-step="5"] .st-ter { opacity: .3; }
#scene4 .route { opacity: 0; }
#scene4[data-active-step="1"] .route, #scene4[data-active-step="5"] .route { opacity: 1; }
#scene4[data-active-step="1"] .chip.c1, #scene4[data-active-step="2"] .chip.c2,
#scene4[data-active-step="3"] .chip.c3, #scene4[data-active-step="4"] .chip.c4,
#scene4[data-active-step="5"] .chip.c5 { opacity: 1; transform: none; }
/* the contraction inset — a Material card */
.inset {
    position: absolute; top: 62px; right: 3vw; z-index: 4;
    width: min(300px, 30vw);
    background: #fffffff5; border: 1px solid var(--g-line); border-radius: 14px;
    padding: 12px 14px 10px; box-shadow: var(--shadow-2);
    opacity: 0; transform: translateY(-8px);
    transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out);
    pointer-events: none;
}
#scene4[data-active-step="4"] .inset, #scene4[data-active-step="5"] .inset { opacity: 1; transform: none; }
.inset-cap { font: 9px "Roboto Mono"; letter-spacing: .16em; color: var(--g-ink-3); margin-top: 6px; }
.inset-cap b { color: var(--g-green-deep); font-weight: 500; }
.inset svg { width: 100%; height: auto; display: block; }
.inset .node { fill: #fff; stroke: var(--g-blue-dark); stroke-width: 1.6; }
.inset .edge { stroke: #9aa0a6; stroke-width: 1.6; fill: none; }
.inset .shortcut { stroke: var(--g-green-deep); stroke-width: 2.4; fill: none; stroke-dasharray: 260; stroke-dashoffset: 260; }
#scene4[data-active-step="4"] .shortcut, #scene4[data-active-step="5"] .shortcut { animation: draw .7s var(--ease-out) forwards; }
.inset .vnode { transition: opacity var(--t-med) var(--ease-swift); }
#scene4[data-active-step="4"] .vnode, #scene4[data-active-step="5"] .vnode { opacity: .12; }
.inset .nlab { font: 10px "Roboto Mono"; fill: var(--g-ink-2); }

/* ── S05 · the price of a street ── */
#scene5 .jam-street { opacity: 0; }
#scene5[data-active-step="1"] .jam-street, #scene5[data-active-step="2"] .jam-street,
#scene5[data-active-step="3"] .jam-street, #scene5[data-active-step="4"] .jam-street,
#scene5[data-active-step="5"] .jam-street { opacity: 1; }
#scene5 .route-old { opacity: 0; }
#scene5[data-active-step="2"] .route-old, #scene5[data-active-step="3"] .route-old,
#scene5[data-active-step="4"] .route-old, #scene5[data-active-step="5"] .route-old { opacity: 1; }
#scene5 .route, #scene5 .route-glow { opacity: 0; }
#scene5[data-active-step="3"] .route, #scene5[data-active-step="3"] .route-glow,
#scene5[data-active-step="4"] .route, #scene5[data-active-step="4"] .route-glow,
#scene5[data-active-step="5"] .route, #scene5[data-active-step="5"] .route-glow { opacity: 1; }
#scene5 .dots-j { opacity: 0; stroke: #4285f438; }
#scene5[data-active-step="4"] .dots-j, #scene5[data-active-step="5"] .dots-j { opacity: 1; }
#scene5 .mlab { opacity: 0; }
#scene5[data-active-step="1"] .mlab-ros, #scene5[data-active-step="2"] .mlab-ros,
#scene5[data-active-step="3"] .mlab-ros, #scene5[data-active-step="4"] .mlab-ros,
#scene5[data-active-step="5"] .mlab-ros { opacity: 1; }
#scene5[data-active-step="3"] .mlab-val, #scene5[data-active-step="4"] .mlab-val, #scene5[data-active-step="5"] .mlab-val { opacity: 1; }
#scene5 .st-loc, #scene5 .st-ter, #scene5 .st-art { opacity: .8; }
#scene5[data-active-step="1"] .chip.c1, #scene5[data-active-step="2"] .chip.c2,
#scene5[data-active-step="3"] .chip.c3, #scene5[data-active-step="4"] .chip.c4,
#scene5[data-active-step="5"] .chip.c5 { opacity: 1; transform: none; }

/* scene 4 chips dock bottom-left on desktop (the inset owns the top-right) */
@media (min-width: 851px) {
    #scene4 .chips { top: auto; bottom: 26px; right: auto; left: 3vw; align-items: flex-start; }
}

/* ── scoreboard — the Google Cloud console table ── */
.board {
    margin-top: 10vh; border-top: 1px solid var(--g-line); border-bottom: 1px solid var(--g-line);
    background-color: #fff;
    background-image: linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 32px 32px;
    color: var(--g-ink); padding: 70px 4vw 60px;
}
.board-inner { max-width: 1000px; margin: 0 auto; }
.board-head { display: flex; align-items: center; gap: 16px; border-bottom: 1px solid var(--g-line); padding-bottom: 12px; margin-bottom: 38px; }
.board-duel {
    display: grid; grid-template-columns: 1fr auto 1fr; gap: 4vw; align-items: center;
    margin-bottom: 46px;
}
.duel-num { font: 600 clamp(42px, 6.8vw, 90px)/1 "Roboto"; letter-spacing: -.02em; }
.duel-num.d-big { color: var(--g-red-deep); }
.duel-num.d-small { color: var(--g-green-deep); }
.duel-mid { font: 10px/1.9 "Roboto Mono"; letter-spacing: .16em; color: var(--g-ink-4); text-align: center; }
.duel-mid .arr { font-size: 22px; color: var(--g-ink-2); display: block; }
.duel-cap { font: 9.5px "Roboto Mono"; letter-spacing: .14em; color: var(--g-ink-4); margin-top: 10px; }
.duel-cap b { color: var(--g-ink); font-weight: 500; }
.board table { width: 100%; border-collapse: collapse; font: 12px "Roboto Mono"; }
.board th, .board td { border: 1px solid var(--g-gray-3); padding: 9px 12px; text-align: left; color: var(--g-ink-2); }
.board th { color: var(--g-ink-3); font-size: 9px; letter-spacing: .15em; background: var(--g-gray-1); }
.board td b { color: var(--g-ink); font-weight: 500; }
.board tr.hl td { border-color: #34a85366; background: #e6f4ea66; }
.board tr.hl td b { color: var(--g-green-deep); }
.board .ratio-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 22px; }
.ratio {
    font: 11px "Roboto Mono"; letter-spacing: .1em; color: var(--g-green-deep);
    border: 1px solid #34a85366; border-radius: 999px; padding: 9px 15px; background: #e6f4ea;
}
.board-note { font: 10px/1.8 "Roboto Mono"; letter-spacing: .08em; color: var(--g-ink-3); margin-top: 28px; }
.board-note b { color: var(--g-ink-2); font-weight: 500; }

/* ── breather ── */
.breather { padding: 16vh 4vw; text-align: center; }
.breather-line { font: 300 clamp(26px, 3.6vw, 40px)/1.35 "Roboto"; max-width: 24ch; margin: 0 auto; color: var(--g-ink); }
.breather-line em { color: var(--g-blue-dark); font-style: normal; font-weight: 500; }

/* ── footer ── */
.foot {
    margin-top: 10vh; padding: 5vh 4vw 4vh; border-top: 1px solid var(--g-line);
    display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap;
    font: 10px "Roboto Mono"; color: var(--g-ink-4);
}
.foot a { color: var(--g-blue-dark); text-decoration: none; }

/* ── hero plate scales (small svg → thicker strokes, bigger pins) ── */
.hero-spec .st-loc { stroke-width: 4; }
.hero-spec .st-ter { stroke-width: 5.6; }
.hero-spec .st-art { stroke-width: 6.6; }
.hero-spec .route { stroke-width: 16; }
.hero-spec .route-glow { stroke-width: 30; }
.hero-spec .pin { transform: scale(3.4); transform-box: fill-box; transform-origin: center; }

/* ── portrait phones: stage becomes a column, card docks bottom ── */
@media (max-width: 850px) and (min-height: 521px) {
    .js .sticky-scene__stage { display: flex; flex-direction: column; padding-top: 62px; }
    .js .sticky-scene__stage .scene-head { flex: 0 0 auto; width: 100%; padding: 8px 4vw; }
    .js .sticky-scene__stage > :not(.scene-head) {
        position: static !important; flex: 1 1 auto; width: 100%; min-height: 0;
        justify-content: center !important; align-items: center;
        padding: 10px 4vw calc(var(--card-reserve, 36vh) + 4px) !important;
    }
    .js .sticky-scene__steps > * { min-height: 100vh; min-height: 100svh; align-items: flex-end; }
    .js .step-card {
        width: 100%; max-width: 560px; border-radius: 20px 20px 16px 16px;
        padding: 12px 20px 18px; max-height: 44vh; overflow-y: auto;
        overscroll-behavior: contain; -webkit-overflow-scrolling: touch;
        opacity: 0; transform: translateY(52px);
    }
    .js .step.is-active .step-card { opacity: 1; transform: none; }
    .step-progress { display: block; height: 3px; background: var(--g-gray-3); border-radius: 3px; overflow: hidden; margin-bottom: 10px; }
    .step-progress i { display: block; height: 100%; width: 0; background: var(--g-blue); transition: width var(--t-med) var(--ease-swift); }
}
@media (max-width: 850px) {
    .hero { grid-template-columns: 1fr; gap: 8vh; padding-top: 16vh; }
    .hero-spec { width: min(78vw, 360px); }
    .hero-cue { display: none; }
    /* map strokes rescale for contain-mode framing (~0.1 px/unit) */
    .map-svg .st-loc { stroke-width: 9; }
    .map-svg .st-ter { stroke-width: 13; }
    .map-svg .st-art { stroke-width: 16; }
    .map-svg .dots { stroke-width: 20; }
    .map-svg .dots.ghost { stroke-width: 13; }
    .map-svg .route { stroke-width: 23; }
    .map-svg .route-glow { stroke-width: 42; }
    .map-svg .route-old { stroke-width: 16; stroke-dasharray: 34 40; }
    .map-svg .jam-street { stroke-width: 21; }
    .map-svg .ring { stroke-width: 6; stroke-dasharray: 26 32; }
    .map-svg .pin { transform: scale(2.6); transform-box: fill-box; transform-origin: center; }
    .map-svg .pin-ring { transform: scale(2.6); transform-box: fill-box; transform-origin: center; stroke-width: .8; }
    .map-svg .mlab { font-size: 84px; stroke-width: 18px; }
    .map-svg .ex-edge { stroke-width: 23; }
    .chips { top: 56px; max-width: 52vw; }
    /* scene 4: the inset owns the top-right corner on phones */
    #scene4 .chips { top: 56px; bottom: auto; right: auto; left: 3vw; align-items: flex-start; max-width: 44vw; }
    .inset { width: min(220px, 44vw); top: 56px; }
    .board-duel { grid-template-columns: 1fr; text-align: center; gap: 18px; }
    .duel-mid .arr { transform: rotate(90deg); }
}
@media (max-width: 480px) {
    .chips { max-width: 62vw; }
    .chip { font-size: 9px; padding: 6px 10px; }
    .hero h1 { font-size: clamp(28px, 8.6vw, 36px); }
    .board { padding: 56px 4vw 44px; }
    .board table { font-size: 10.5px; }
    .board th, .board td { padding: 7px 8px; }
    .map-svg .mlab { font-size: 96px; }
    #scene4 .chips { max-width: 40vw; }
}

/* ── reduced motion: the plain document ── */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .01ms !important;
        scroll-behavior: auto !important;
    }
    .reveal, .h-line > span, .hero .dek, .hero-meta, .hero-spec { opacity: 1 !important; transform: none !important; }
    .js .sticky-scene__stage { position: relative; height: auto; min-height: 50vh; }
    .js .sticky-scene { padding-bottom: 0; }
    .js .sticky-scene__steps { margin-top: 0; }
    .js .sticky-scene__steps > * { min-height: auto; display: block; padding: 0 4vw; }
    .js .step { opacity: 1 !important; transform: none !important; max-width: none; background: none; border: 0; padding: 30px 0; pointer-events: auto; }
    .js .step-card {
        opacity: 1 !important; transform: none !important; background: none; border: 0; padding: 0; max-width: none;
        border-radius: 0 !important; box-shadow: none !important; overflow: visible !important; max-height: none !important;
    }
    .step-progress { display: none !important; }
    .hero-cue { display: none; }
    /* every layer finds its final, most informative state */
    #scene1 .dots-v, #scene1 .ex-edge, #scene1 .pin-o, #scene1 .pin-d, #scene1 .pin-ring, #scene1 .mlab { opacity: 1 !important; }
    #scene1 .pin-ring { animation: none !important; opacity: .5 !important; }
    #scene2 .dj, #scene2 .route, #scene2 .route-glow { opacity: 1 !important; }
    #scene2 .dj { stroke: #4285f438 !important; }
    #scene2 .route, #scene2 .route-glow { stroke-dashoffset: 0 !important; }
    #scene3 .as, #scene3 .ghost, #scene3 .route, #scene3 .route-glow { opacity: 1 !important; }
    #scene3 .as { stroke: #4285f45c !important; }
    #scene4 .ring, #scene4 .dots-h, #scene4 .route { opacity: 1 !important; }
    #scene4 .st-loc { opacity: .22 !important; }
    #scene4 .st-art { stroke: var(--g-yellow-deep) !important; }
    #scene4 .st-ter { opacity: .3 !important; }
    #scene4 .inset { opacity: 1 !important; }
    #scene4 .shortcut { stroke-dashoffset: 0 !important; }
    #scene5 .jam-street, #scene5 .route-old, #scene5 .route, #scene5 .route-glow, #scene5 .dots-j, #scene5 .mlab { opacity: 1 !important; }
    .chip { opacity: 1 !important; transform: none !important; }
}
"""

# replace the style block
s = re.sub(r'<style>.*?</style>', lambda m: '<style>' + CSS + '</style>', s, count=1, flags=re.S)

# markup touch-ups --------------------------------------------------------
# reading indicator gradient: Maps blue → traffic red → yellow
s = s.replace('<body data-vb-progress-start="#c7ff3d" data-vb-progress-mid="#546cff" data-vb-progress-end="#ff6b2c">',
              '<body data-vb-progress-start="#4285f4" data-vb-progress-mid="#ea4335" data-vb-progress-end="#fbbc04">')

# hero plate pins get their roles (blue origin, red destination)
s = s.replace('<svg viewBox="%%VB_CORR%%" role="img" aria-label="The settled route',
              '<svg viewBox="%%VB_CORR%%" role="img" aria-label="The settled route')
s = s.replace('<circle class="pin" cx="%%OX%%" cy="%%OY%%" r="7"/>\n                <circle class="pin" cx="%%DX%%" cy="%%DY%%" r="7"/>',
              '<circle class="pin pin-o" cx="%%OX%%" cy="%%OY%%" r="7"/>\n                <circle class="pin pin-d" cx="%%DX%%" cy="%%DY%%" r="7"/>')

# scene pin rings: origin ring blue, destination ring red
s = s.replace('<circle class="pin-ring" cx="%%OX%%" cy="%%OY%%" r="13"/>',
              '<circle class="pin-ring ring-o" cx="%%OX%%" cy="%%OY%%" r="13"/>')

open('article_src.html', 'w', encoding='utf-8').write(s)
print('restyled source,', len(s), 'bytes')
