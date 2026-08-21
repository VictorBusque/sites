#!/usr/bin/env python3
"""Assemble blog/how-qr-codes-work.html from parts (one-shot build script)."""
import pathlib

ROOT = pathlib.Path('/root/web/sites')
read = lambda p: pathlib.Path(p).read_text()

vb_helpers = read('/tmp/vb_helpers.txt')
site_runtime = read('/tmp/site_runtime.txt')
scene_runtime = read('/tmp/scene_runtime.txt')
sw = read('/tmp/sw.txt')

hero_svg = read('/tmp/hero.svg').replace(
    'role="img" aria-label="QR code"',
    'role="img" aria-label="QR code that opens this page"')
# tighten hero svg whitespace for inline embedding
hero_svg = hero_svg.replace('<svg ', '<svg class="hero-qr-svg" ')

furniture_svg = read('/tmp/furniture.svg').replace('<svg ', '<svg class="static-svg" ')
seated_svg = read('/tmp/seated.svg').replace('<svg ', '<svg class="static-svg" ')
final_svg = read('/tmp/final.svg').replace('<svg ', '<svg class="static-svg" ')

# ── parts below ──

HEAD = r'''<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">

    <!-- Primary meta -->
    <title>How a QR Code Works — Víctor Busqué</title>
    <meta name="description" content="Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, the mask election — every number computed live.">
    <meta name="author" content="Víctor Busqué">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://engineering.victorbusque.com/blog/how-qr-codes-work.html">

    <!-- Favicons / PWA (absolute paths resolve from /blog/) -->
    <link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
    <link rel="icon" href="/img/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <meta name="theme-color" content="#101010">
    <meta name="apple-mobile-web-app-title" content="VB Posts">
    <meta name="application-name" content="VB Posts">
    <meta name="color-scheme" content="light dark">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Víctor Busqué — Curiosities">
    <meta property="og:title" content="How a QR Code Works — Víctor Busqué">
    <meta property="og:description" content="Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, the mask election — every number computed live.">
    <meta property="og:url" content="https://engineering.victorbusque.com/blog/how-qr-codes-work.html">
    <meta property="og:image" content="https://engineering.victorbusque.com/img/og.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="How a QR Code Works — Víctor Busqué">
    <meta name="twitter:description" content="Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, the mask election — every number computed live.">
    <meta name="twitter:image" content="https://engineering.victorbusque.com/img/og.png">

    <!-- Performance: preconnect to font CDN -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- Structured data — matches js/posts.js, the site's single post manifest. -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "How a QR Code Works",
      "description": "Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, the mask election — every number computed live.",
      "datePublished": "2026-10",
      "author": { "@id": "https://engineering.victorbusque.com/#person" },
      "publisher": { "@id": "https://engineering.victorbusque.com/#person" },
      "url": "https://engineering.victorbusque.com/blog/how-qr-codes-work.html",
      "mainEntityOfPage": "https://engineering.victorbusque.com/blog/how-qr-codes-work.html",
      "inLanguage": "en",
      "keywords": ["QR codes", "Reed–Solomon", "Error correction", "Barcode"],
      "articleSection": "Codes · Error correction"
    }
    </script>

    <!-- The .js gate: enables the scene overlay layout. Without it (no JS,
         reduced motion) scenes render as a plain document — stage first,
         steps stacked. Must run before the body parses. -->
    <script>document.documentElement.className += ' js';</script>

    <style>
/* ════════════════════════════════════════════════════════════════════
   HOW A QR CODE WORKS — the drafting-table spec sheet.
   Paper prose sections; dark blueprint stages with hairline grids;
   modules are the only ornament. Skeleton contracts (sticky scenes,
   step cards, mobile bottom sheet, reduced-motion collapse) follow the
   site's scaffold; the skin is this article's alone.
   ════════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Unbounded:wght@400;500;600;700&display=swap');

/* ── tokens ── */
:root {
    --ink: #101010;
    --paper: #f2f0e9;
    --paper-2: #eae7dc;
    --blue: #546cff;
    --acid: #c7ff3d;
    --orange: #ff6b2c;
    --muted: #716f68;
    --line: #111111;

    --stage: #0d0f14;
    --stage-2: #14171e;
    --grid: #ffffff0a;
    --mod: #e8e6df;          /* module ink on dark stages */

    --ease-out: cubic-bezier(.16, 1, .3, 1);
    --ease-in: cubic-bezier(.55, 0, .85, .36);
    --ease-swift: cubic-bezier(.4, 0, .2, 1);
    --t-fast: 180ms;
    --t-med: 400ms;
    --t-slow: 800ms;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; scroll-padding-top: 84px; }
body {
    background: var(--paper);
    color: var(--ink);
    font: 18px/1.74 "Newsreader", Georgia, serif;
    -webkit-font-smoothing: antialiased;
}
::selection { background: var(--acid); color: var(--ink); }
a { color: inherit; }
.mono, code { font-family: "DM Mono", monospace; }

.skip-link {
    position: fixed; left: 12px; top: -60px; z-index: 300;
    background: var(--ink); color: var(--acid);
    font: 11px "DM Mono"; letter-spacing: .12em;
    padding: 10px 16px; text-decoration: none;
    transition: top var(--t-fast) var(--ease-out);
}
.skip-link:focus { top: 12px; }

/* ── reveals ── */
.reveal { opacity: 0; transform: translateY(22px); transition: opacity .9s var(--ease-out), transform .9s var(--ease-out); }
.reveal.seen { opacity: 1; transform: none; }

/* ── hero — a light-table with the finished object ── */
.hero {
    min-height: 100svh; position: relative; overflow: hidden;
    background:
        radial-gradient(1200px 700px at 78% 30%, #1b202b 0%, transparent 60%),
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px),
        var(--stage);
    background-size: auto, 32px 32px, 32px 32px, auto;
    color: #fff;
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr);
    align-items: center;
    gap: 4vw;
    padding: 12vh 6vw 10vh;
}
.hero-kicker { font: 10px "DM Mono"; letter-spacing: .22em; color: var(--acid); margin-bottom: 26px; }
.hero h1 {
    font-family: "Unbounded", sans-serif;
    font-weight: 500;
    font-size: clamp(30px, 4.6vw, 58px);
    line-height: 1.04;
    letter-spacing: -.04em;
}
.hero h1 em { font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: var(--acid); }
.hero .h-line { display: block; overflow: hidden; }
.hero .h-line > span { display: inline-block; transform: translateY(110%); animation: rise 1s var(--ease-out) forwards; }
.hero .h-line:nth-child(2) > span { animation-delay: .12s; }
.hero .h-line:nth-child(3) > span { animation-delay: .24s; }
@keyframes rise { to { transform: translateY(0); } }
.hero .dek {
    max-width: 54ch; margin-top: 28px;
    font-size: 19px; line-height: 1.6; color: #c9c6bd;
    opacity: 0; animation: fade-rise .9s var(--ease-out) .5s forwards;
}
.hero-meta {
    display: flex; gap: 26px; flex-wrap: wrap; margin-top: 34px;
    font: 10px "DM Mono"; letter-spacing: .16em; color: #8a8price790;
    color: #8a8790;
    opacity: 0; animation: fade-rise .9s var(--ease-out) .7s forwards;
}
.hero-meta b { color: #fff; font-weight: 500; }
@keyframes fade-rise { to { opacity: 1; } }

.hero-spec {
    position: relative; justify-self: center;
    width: min(34vw, 380px); aspect-ratio: 1;
    padding: 4.5%;                    /* the quiet zone, drawn */
    background: #fdfcf7;
    box-shadow: 0 30px 80px -30px rgba(0,0,0,.8), 0 0 0 1px #ffffff14;
    opacity: 0; transform: scale(.96); animation: spec-in 1.1s var(--ease-out) .35s forwards;
}
@keyframes spec-in { to { opacity: 1; transform: none; } }
.hero-spec svg { display: block; width: 100%; height: 100%; }
.hero-spec::before, .hero-spec::after,
.hero-spec .mark-b::before, .hero-spec .mark-b::after {
    content: ""; position: absolute; width: 18px; height: 18px;
    border: 1px solid var(--acid);
}
.hero-spec::before { top: -9px; left: -9px; border-width: 1px 0 0 1px; }
.hero-spec::after { top: -9px; right: -9px; border-width: 1px 1px 0 0; }
.hero-spec .mark-b::before { bottom: -9px; left: -9px; border-width: 0 0 1px 1px; }
.hero-spec .mark-b::after { bottom: -9px; right: -9px; border-width: 0 1px 1px 0; }
.hero-spec-label {
    position: absolute; left: 50%; bottom: -44px; transform: translateX(-50%);
    white-space: nowrap;
    font: 9px "DM Mono"; letter-spacing: .18em; color: #8a8790;
}
.hero-spec-label b { color: var(--acid); font-weight: 500; }
.hero-cue {
    position: absolute; left: 50%; bottom: 26px; transform: translateX(-50%);
    width: 1px; height: 44px; background: linear-gradient(#fff0, #ffffff88);
    animation: cue 2.2s var(--ease-swift) infinite;
}
@keyframes cue { 0% { transform: translateX(-50%) scaleY(.4); transform-origin: top; } 55% { transform: translateX(-50%) scaleY(1); } 100% { transform: translateX(-50%) scaleY(.4); } }

/* ── prose ── */
.prose { max-width: 720px; margin: 0 auto; padding: 12vh 4vw 0; }
.prose > p { font-size: 18px; line-height: 1.74; color: #33322e; margin-bottom: 1.5em; }
.prose > p strong { font-weight: 600; }
.prose h2 {
    font-family: "Unbounded", sans-serif; font-weight: 500;
    font-size: clamp(25px, 3.4vw, 38px); letter-spacing: -.045em; line-height: 1.05;
    margin: 11vh 0 20px; display: flex; align-items: baseline; gap: 18px;
}
.prose h2 .sec-no { font: 10px "DM Mono"; letter-spacing: .14em; color: var(--orange); align-self: center; }
.prose .callout {
    border-left: 4px solid var(--acid); background: var(--paper-2);
    padding: 22px 26px; margin: 5vh 0; font: italic 23px/1.45 "Instrument Serif";
}
.prose .callout em { font-style: normal; }
.prose .aside {
    font: 11px/1.7 "DM Mono"; color: #777;
    border-top: 1px solid #d8d4c6; padding-top: 12px; margin: 6vh 0;
}
.prose .aside a { color: var(--blue); }

/* versions ladder figure */
.ladder { border: 1px solid var(--line); background: var(--paper-2); padding: 30px 26px 18px; margin: 5vh 0; }
.ladder-row { display: flex; align-items: flex-end; gap: clamp(10px, 2.4vw, 26px); flex-wrap: wrap; }
.ladder-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.ladder-box { border: 1.5px solid var(--ink); background: #fdfcf7; position: relative; }
.ladder-box::after { content: ""; position: absolute; inset: 3px; border: 1px solid #11111126; background:
    linear-gradient(#1111111f 1px, transparent 1px), linear-gradient(90deg, #1111111f 1px, transparent 1px);
    background-size: 12.5% 12.5%; }
.ladder-cap { font: 9px "DM Mono"; letter-spacing: .12em; color: var(--muted); text-align: center; line-height: 1.5; }
.ladder-cap b { color: var(--ink); font-weight: 500; display: block; }
.ladder-note { font: 10px/1.7 "DM Mono"; color: var(--muted); margin-top: 18px; }

/* capacity table */
.caps { width: 100%; border-collapse: collapse; margin: 5vh 0; font: 13px "DM Mono"; }
.caps th, .caps td { border: 1px solid var(--line); padding: 10px 12px; text-align: left; }
.caps th { font-size: 9px; letter-spacing: .16em; background: var(--paper-2); }
.caps td b { font-weight: 500; }
.caps .num { color: var(--blue); }

/* ── sticky scenes — the site contract ── */
.sticky-scene { position: relative; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); margin-top: 10vh; }
.js .sticky-scene { padding-bottom: 100vh; padding-bottom: 100svh; }
.sticky-scene__stage {
    background-color: var(--stage);
    background-image: linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 32px 32px;
    color: #fff; position: relative; overflow: hidden; min-height: 60vh;
}
.js .sticky-scene__stage { position: sticky; top: 0; height: 100vh; height: 100svh; min-height: 0; }
.sticky-scene__stage::after {
    content: ""; position: absolute; width: 200px; height: 200px;
    border: 1px solid #ffffff12; border-radius: 50%;
    right: -100px; bottom: -100px; pointer-events: none;
}
.scene-head {
    display: flex; align-items: center; gap: 16px;
    border-bottom: 1px solid #ffffff1a; padding: 12px 4vw;
    position: relative; z-index: 2;
}
.scene-no { font: 10px "DM Mono"; letter-spacing: .14em; color: var(--orange); }
.scene-name { font: 10px "DM Mono"; letter-spacing: .18em; }
.scene-readout { font: 10px "DM Mono"; color: #777; margin-left: auto; }
.js .sticky-scene__steps { position: relative; margin-top: -100vh; margin-top: -100svh; pointer-events: none; z-index: 1; }
.js .sticky-scene__steps > * { min-height: 100vh; min-height: 100svh; display: flex; align-items: center; padding: 0 4vw; }
.step { max-width: 420px; background: var(--paper); border: 1px solid var(--line); padding: 26px 28px; color: var(--ink); }
.js .step { background: none; border: 0; padding: 0; max-width: none; pointer-events: none; }
.js .step.is-active { pointer-events: auto; }
.step-card {
    width: 100%; max-width: 420px; background: var(--paper);
    border: 1px solid var(--line); padding: 26px 28px; color: var(--ink);
    opacity: 0; transform: translateY(26px);
    transition: opacity var(--t-slow) var(--ease-out), transform var(--t-slow) var(--ease-out);
}
.js .step.is-active .step-card { opacity: 1; transform: none; }
.step-progress { display: none; }
.step-k { font: 9px "DM Mono"; letter-spacing: .16em; color: var(--orange); display: block; margin-bottom: 10px; }
.step p { font-size: 16.5px; line-height: 1.6; color: #33322e; }
.step p + p { margin-top: .8em; }
.step p b { font-weight: 600; }
.step .mono { font-size: 13.5px; }

/* stage internals — the article's diagram grammar */
.qr-stage {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    gap: 4vw; padding: 76px 4vw 3vh;
}
.stage-static { padding: 60px 4vw 40px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.js .stage-static { display: none; }
.static-svg { width: min(46vh, 80vw); height: auto; }
.static-note { font: 10px/1.7 "DM Mono"; letter-spacing: .1em; color: #8a8790; text-align: center; max-width: 60ch; }
.static-note b { color: var(--acid); font-weight: 500; }

.qr-grid-svg { width: min(56vh, 44vw, 88vw); height: auto; display: block; }
.qr-grid-svg .m { transition: opacity var(--t-med) var(--ease-swift), fill var(--t-med) var(--ease-swift); }

/* module roles — color is always paired with a label, never alone */
.qr-grid-svg .base { fill: #ffffff10; stroke: #ffffff0e; }
.qr-grid-svg .finder { fill: var(--blue); }
.qr-grid-svg .sep { fill: #546cff3d; }
.qr-grid-svg .timing { fill: #9db0ff; }
.qr-grid-svg .darkmod { fill: var(--orange); }
.qr-grid-svg .fmt { fill: #9db0ff; opacity: .55; }
.qr-grid-svg .free { fill: #ffffff17; }
.qr-grid-svg .seat { fill: var(--mod); }
.qr-grid-svg .seat.ec { fill: var(--orange); }
.qr-grid-svg .ghost { fill: #ffffff10; }

/* S01 layer visibility — states keyed off data-active-step only */
#scene1 .lyr { opacity: 0; transition: opacity var(--t-slow) var(--ease-out); }
#scene1[data-active-step="1"] .lyr { opacity: 0; }
#scene1[data-active-step="2"] .lyr-finder,
#scene1[data-active-step="3"] .lyr-finder, #scene1[data-active-step="3"] .lyr-sep,
#scene1[data-active-step="4"] .lyr-finder, #scene1[data-active-step="4"] .lyr-sep, #scene1[data-active-step="4"] .lyr-timing,
#scene1[data-active-step="5"] .lyr { opacity: 1; }
.s1-legend {
    display: flex; flex-direction: column; gap: 10px;
    font: 10px "DM Mono"; letter-spacing: .14em; color: #8a8790; max-width: 220px;
}
.s1-legend .li { display: flex; align-items: center; gap: 10px; opacity: .25; transition: opacity var(--t-med) var(--ease-swift); }
.s1-legend .li i { width: 12px; height: 12px; display: inline-block; }
.s1-legend .li.on { opacity: 1; color: #fff; }
#scene1[data-active-step="2"] .li-finder,
#scene1[data-active-step="3"] .li-finder, #scene1[data-active-step="3"] .li-sep,
#scene1[data-active-step="4"] .li-finder, #scene1[data-active-step="4"] .li-sep, #scene1[data-active-step="4"] .li-timing,
#scene1[data-active-step="5"] .li { opacity: 1; color: #fff; }
#scene1[data-active-step="2"] .li-finder, #scene1[data-active-step="3"] .li-sep,
#scene1[data-active-step="4"] .li-timing, #scene1[data-active-step="5"] .li-dark, #scene1[data-active-step="5"] .li-fmt { color: var(--acid); }

/* S02 bitstream */
.s2-wrap { display: flex; flex-direction: column; gap: 26px; max-width: 760px; width: 100%; }
.s2-chars { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
.s2-char {
    width: 42px; height: 54px; border: 1px solid #ffffff26;
    display: grid; place-items: center;
    font: 16px "Instrument Serif"; color: #fff; background: var(--stage-2);
}
.s2-char small { display: block; font: 8px "DM Mono"; color: #8a8790; margin-top: 3px; }
.s2-ribbon { display: flex; flex-wrap: wrap; gap: 3px; justify-content: center; }
.s2-bit {
    width: 17px; height: 22px; display: grid; place-items: center;
    font: 10px "DM Mono"; color: #8a8790; border: 1px solid #ffffff14;
    background: var(--stage-2);
    opacity: 0; transform: rotateX(70deg);
    transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out);
}
.s2-bit.on { opacity: 1; transform: none; }
.s2-bit.one { color: var(--ink); background: var(--mod); border-color: var(--mod); }
.s2-bit.seg-mode.one, .s2-bit.seg-count.one { background: var(--blue); border-color: var(--blue); color: #fff; }
.s2-bit.seg-term.one { background: #ffffff2e; border-color: #ffffff45; color: #fff; }
.s2-brace-label { font: 9px "DM Mono"; letter-spacing: .16em; color: #8a8790; text-align: center; }
.s2-rack { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.s2-cw {
    font: 11px "DM Mono"; padding: 7px 9px;
    border: 1px solid #ffffff22; color: #c9c6bd; background: var(--stage-2);
    opacity: 0; transform: translateY(10px);
    transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out);
}
.s2-cw.on { opacity: 1; transform: none; }
.s2-cw.pad { color: var(--orange); border-color: #ff6b2c55; }
.s2-readout { font: 10px "DM Mono"; letter-spacing: .14em; color: #8a8790; text-align: center; }
.s2-readout b { color: var(--acid); font-weight: 500; }

/* S03 insurance */
.s3-wrap { display: flex; flex-direction: column; gap: 22px; max-width: 720px; width: 100%; }
.s3-wall, .s3-gen { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.s3-cw {
    width: 40px; padding: 8px 0; text-align: center;
    font: 11px "DM Mono"; border: 1px solid #ffffff22; background: var(--stage-2); color: var(--mod);
    opacity: 0; transform: translateY(12px);
    transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out);
}
.s3-cw.on { opacity: 1; transform: none; }
.s3-cw.ec { color: var(--orange); border-color: #ff6b2c66; background: #ff6b2c14; }
.s3-label { font: 9px "DM Mono"; letter-spacing: .18em; color: #8a8790; text-align: center; }
.s3-label b { color: #fff; font-weight: 500; }
.s3-gen .s3-cw { color: #9db0ff; border-color: #546cff66; }
.s3-badge {
    align-self: center; font: 10px "DM Mono"; letter-spacing: .16em;
    border: 1px solid var(--acid); color: var(--acid); padding: 8px 16px;
    opacity: 0; transition: opacity var(--t-med) var(--ease-out);
}
.s3-badge.on { opacity: 1; }
.s3-badge b { font-weight: 500; }
.s3-table { border-collapse: collapse; align-self: center; opacity: 0; transition: opacity var(--t-med) var(--ease-out); }
.s3-table.on { opacity: 1; }
.s3-table th, .s3-table td { border: 1px solid #ffffff1f; padding: 6px 12px; font: 10px "DM Mono"; color: #c9c6bd; }
.s3-table th { color: #8a8790; font-size: 8.5px; letter-spacing: .14em; }
.s3-table td b { color: var(--acid); font-weight: 500; }
.s3-table tr.cur td { border-color: var(--acid); }

/* S04 zigzag */
.s4-wrap { position: relative; }
.s4-cursor {
    fill: none; stroke: var(--acid); stroke-width: .5;
    transition: transform var(--t-med) var(--ease-swift);
}
.s4-path { fill: none; stroke: #c7ff3d40; stroke-width: .18; }
.s4-skip { fill: #546cff2e; stroke: #546cff; stroke-width: .12; }

/* S05 mask election */
.s5-wrap { display: flex; flex-direction: column; align-items: center; gap: 22px; width: 100%; }
.s5-detail { position: relative; }
.s5-rack { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
.s5-cand { position: relative; opacity: 0; transform: scale(.9); transition: opacity var(--t-med) var(--ease-out), transform var(--t-med) var(--ease-out); }
.s5-cand.on { opacity: 1; transform: none; }
.s5-cand svg { width: min(11vh, 88px); height: auto; display: block; }
.s5-cand .pen { font: 9.5px "DM Mono"; color: #8a8790; text-align: center; margin-top: 5px; }
.s5-cand.best .pen { color: var(--acid); }
.s5-cand.best::before {
    content: ""; position: absolute; inset: -7px;
    border: 1px solid var(--acid);
    animation: best-pulse 2.4s var(--ease-swift) infinite;
}
@keyframes best-pulse { 0%, 100% { box-shadow: 0 0 0 0 #c7ff3d00; } 50% { box-shadow: 0 0 18px 0 #c7ff3d3d; } }
.s5-cand.dim { opacity: .18; }
.s5-cand .tag-no { position: absolute; top: -8px; left: -6px; font: 8px "DM Mono"; color: #8a8790; background: var(--stage); padding: 1px 4px; }
.s5-fmt {
    display: flex; gap: 26px; align-items: center; flex-wrap: wrap; justify-content: center;
    opacity: 0; transition: opacity var(--t-med) var(--ease-out);
}
.s5-fmt.on { opacity: 1; }
.s5-fmt .strip { display: flex; gap: 3px; }
.s5-fmt .fb { width: 14px; height: 18px; display: grid; place-items: center; font: 9px "DM Mono"; border: 1px solid #ffffff1f; color: #8a8790; }
.s5-fmt .fb.one { background: var(--blue); border-color: var(--blue); color: #fff; }
.s5-fmt .flab { font: 9px "DM Mono"; letter-spacing: .14em; color: #8a8790; text-align: center; margin-top: 6px; }
.s5-note { font: 10px "DM Mono"; letter-spacing: .12em; color: #8a8790; text-align: center; }
.s5-note b { color: var(--acid); font-weight: 500; }

/* the mask overlay (checkerboard) on the S05 detail grid */
#s5Detail .ovl { fill: #c7ff3d; opacity: 0; transition: opacity var(--t-med) var(--ease-out); }
#scene5[data-active-step="2"] #s5Detail .ovl { opacity: .5; }
#s5Detail .runhl { fill: none; stroke: var(--orange); stroke-width: .45; opacity: 0; transition: opacity var(--t-med) var(--ease-out); }
#scene5[data-active-step="1"] #s5Detail .runhl { opacity: 1; }

/* ── lab ── */
.lab {
    margin-top: 10vh; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);
    background-color: var(--stage);
    background-image: linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 32px 32px;
    color: #fff; padding: 76px 4vw 64px;
}
.lab-head { display: flex; align-items: center; gap: 16px; border-bottom: 1px solid #ffffff1a; padding-bottom: 12px; margin-bottom: 34px; max-width: 1060px; margin-left: auto; margin-right: auto; }
.lab-grid {
    max-width: 1060px; margin: 0 auto;
    display: grid; grid-template-columns: minmax(280px, 420px) 1fr; gap: 5vw; align-items: center;
}
.lab-qr-wrap { position: relative; }
#labSvg { width: 100%; height: auto; display: block; background: #fdfcf7; padding: 4.5%; box-shadow: 0 24px 60px -30px rgba(0,0,0,.8); }
#labSvg .m.dark { fill: #14161b; }
#labSvg .m.light { fill: #fdfcf7; }
#labSvg .ink { fill: #ff6b2c; opacity: .82; }
.lab-ctrl { display: flex; flex-direction: column; gap: 26px; }
.lab-ctrl label { font: 10px "DM Mono"; letter-spacing: .16em; color: #8a8790; display: block; margin-bottom: 10px; }
.lab-slider { width: 100%; accent-color: var(--orange); height: 28px; }
.lab-levels { display: flex; gap: 8px; flex-wrap: wrap; }
.lab-levels input { position: absolute; opacity: 0; pointer-events: none; }
.lab-levels span {
    display: inline-block; padding: 8px 16px; border: 1px solid #ffffff26;
    font: 11px "DM Mono"; color: #c9c6bd; cursor: pointer; user-select: none;
    transition: all var(--t-fast) var(--ease-out);
}
.lab-levels input:checked + span { background: var(--blue); border-color: var(--blue); color: #fff; }
.lab-levels input:focus-visible + span { outline: 2px solid var(--acid); outline-offset: 2px; }
.lab-verdict {
    border: 1px solid; padding: 16px 20px;
    font: 12px/1.7 "DM Mono"; letter-spacing: .06em;
}
.lab-verdict.ok { border-color: var(--acid); color: var(--acid); }
.lab-verdict.bad { border-color: var(--orange); color: var(--orange); }
.lab-verdict .sub { display: block; color: #8a8790; margin-top: 6px; letter-spacing: .1em; font-size: 10px; }
.lab-stats { display: flex; gap: 22px; flex-wrap: wrap; font: 10px "DM Mono"; letter-spacing: .14em; color: #8a8790; }
.lab-stats b { color: #fff; font-weight: 500; }
.lab-note { max-width: 720px; margin: 40px auto 0; font: 10px/1.8 "DM Mono"; letter-spacing: .08em; color: #8a8790; }

/* ── breather ── */
.breather { padding: 16vh 4vw; text-align: center; }
.breather-line { font: italic clamp(26px, 3.6vw, 40px)/1.3 "Instrument Serif"; max-width: 22ch; margin: 0 auto; }
.breather-line em { color: var(--blue); font-style: italic; }

/* ── synthesis figure ── */
.fin-fig { border: 1px solid var(--line); background: var(--stage); margin: 5vh 0; padding: 40px 20px 26px; position: relative; }
.fin-inner { max-width: 640px; margin: 0 auto; position: relative; }
.fin-inner svg { width: 100%; height: auto; display: block; }
.fin-tag { position: absolute; font: 8.5px "DM Mono"; letter-spacing: .14em; color: var(--acid); background: #0d0f14e6; padding: 3px 7px; border: 1px solid #c7ff3d3d; white-space: nowrap; }
.fin-tag.t-blue { color: #9db0ff; border-color: #546cff55; }
.fin-tag.t-orange { color: var(--orange); border-color: #ff6b2c55; }
.fin-cap { font: 10px/1.7 "DM Mono"; letter-spacing: .1em; color: #8a8790; text-align: center; margin-top: 18px; }

/* ── footer ── */
.foot {
    margin-top: 10vh; padding: 5vh 4vw 4vh; border-top: 1px solid var(--line);
    display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap;
    font: 10px "DM Mono"; color: var(--muted);
}
.foot a { color: var(--blue); text-decoration: none; }

/* ── landscape-short / desktop card column ── */
@media (min-width: 851px) {
    .js .sticky-scene__stage > div:not(.scene-head) { padding-right: 30%; }
}

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
        width: 100%; max-width: 560px; border-radius: 18px 18px 14px 14px;
        box-shadow: 0 20px 44px -24px rgba(0,0,0,.55);
        padding: 12px 20px 18px; max-height: 44vh; overflow-y: auto;
        overscroll-behavior: contain; -webkit-overflow-scrolling: touch;
        opacity: 0; transform: translateY(52px);
    }
    .js .step.is-active .step-card { opacity: 1; transform: none; }
    .step-progress { display: block; height: 3px; background: #ffffff22; border-radius: 3px; overflow: hidden; margin-bottom: 10px; }
    .step-progress i { display: block; height: 100%; width: 0; background: var(--orange); transition: width var(--t-med) var(--ease-swift); }
}
@media (max-width: 850px) {
    .hero { grid-template-columns: 1fr; gap: 8vh; padding-top: 16vh; }
    .hero-spec { width: min(64vw, 300px); }
    .hero-cue { display: none; }
    .qr-grid-svg { width: min(88vw, 52vh); }
    .s2-bit { width: 14px; height: 19px; font-size: 9px; }
    .s2-char { width: 34px; height: 48px; }
    .s1-legend { max-width: 100%; flex-direction: row; flex-wrap: wrap; justify-content: center; }
    .s3-cw { width: 32px; font-size: 10px; }
    .s5-cand svg { width: min(17vw, 76px); }
    .lab-grid { grid-template-columns: 1fr; }
    .lab-qr-wrap { max-width: 340px; margin: 0 auto; }
    .s2-wrap, .s3-wrap { max-width: 100%; }
}
@media (max-width: 480px) {
    .s2-bit { width: 11.5px; height: 17px; font-size: 8px; }
    .s2-char { width: 28px; height: 44px; font-size: 13px; }
    .s3-cw { width: 26px; font-size: 9px; padding: 6px 0; }
    .s5-cand svg { width: 19vw; }
    .s5-cand .pen { font-size: 8.5px; }
    .hero h1 { font-size: clamp(26px, 8.4vw, 34px); }
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
    .s5-cand.best::before { animation: none; }
}
    </style>
    <link rel="stylesheet" href="../css/post-progress.css">
    <link rel="stylesheet" href="../css/post-nav.css">
@@VB_HELPERS@@
</head>
'''

BODY = r'''
<body data-vb-progress-start="#c7ff3d" data-vb-progress-mid="#546cff" data-vb-progress-end="#ff6b2c">

    <header class="hero">
        <div>
            <div class="hero-kicker">NOTE 11 · CODES · EST. 1994</div>
            <h1>
                <span class="h-line"><span>441 modules,</span></span>
                <span class="h-line"><span>26 codewords,</span></span>
                <span class="h-line"><span><em>one square.</em></span></span>
            </h1>
            <p class="dek">Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, the mask election — every number computed live.</p>
            <div class="hero-meta">
                <span>OCT <b>2026</b></span>
                <span>~<b>10</b> MIN</span>
                <span><b>5</b> SCENES + <b>1</b> LAB</span>
                <span>MODE: <b>COMPUTED LIVE</b></span>
            </div>
        </div>
        <div class="hero-spec">
            <span class="mark-b" aria-hidden="true"></span>
            @@HERO_SVG@@
            <div class="hero-spec-label">PAYLOAD: THIS PAGE'S URL · <b>64 BYTES → VERSION 4-L</b></div>
        </div>
        <div class="hero-cue" aria-hidden="true"></div>
    </header>

    <main>
        <section class="prose">
            <h2><span class="sec-no">01</span>The square is a grid</h2>
            <p>Scanning a QR code feels like pointing a camera at a tiny picture. It is not a
                picture. It is a <strong>grid of modules</strong> — small squares that are either
                dark or light — and every one of them has a job that was decided before anything
                was drawn. The smallest standard code is 21 × 21 modules: <strong>441 seats</strong>.
                Around the grid sits a margin of light modules, the <strong>quiet zone</strong>, so
                the code has an edge a camera can find.</p>
            <p>There is no other size ladder: a QR code's side is always
                <span class="mono">4 × version + 17</span> modules, for forty versions.</p>
            <figure class="ladder reveal" aria-label="Version ladder: version 1 is 21 by 21 modules; each version adds four modules per side, up to version 40 at 177 by 177.">
                <div class="ladder-row">
                    <div class="ladder-item"><span class="ladder-box" style="width:25px;height:25px"></span><span class="ladder-cap"><b>V1</b>21×21</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:30px;height:30px"></span><span class="ladder-cap"><b>V2</b>25×25</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:35px;height:35px"></span><span class="ladder-cap"><b>V3</b>29×29</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:40px;height:40px"></span><span class="ladder-cap"><b>V4</b>33×33</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:44px;height:44px"></span><span class="ladder-cap"><b>V5</b>37×37</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:68px;height:68px"></span><span class="ladder-cap"><b>V10</b>57×57</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:110px;height:110px"></span><span class="ladder-cap"><b>V25</b>117×117</span></div>
                    <div class="ladder-item"><span class="ladder-box" style="width:158px;height:158px"></span><span class="ladder-cap"><b>V40</b>177×177</span></div>
                </div>
                <div class="ladder-note">SIDE = 4 × VERSION + 17 · EACH VERSION ADDS FOUR MODULES PER SIDE · THE HERO CODE ABOVE IS V4 (33×33) BECAUSE ITS URL NEEDS 64 BYTES</div>
            </figure>
            <p>The rest of this page builds one code from scratch, the way an encoder does: the
                fixed furniture first, then the message <span class="mono">HELLO WORLD</span> as
                bits, then insurance, then seats, then a mask. The 21 × 21 version carries 26
                codewords — bytes with a very particular commute — and by the end you will know
                the job of every module in the square.</p>
        </section>

        <!-- ═══ ACT 01 · THE FURNITURE ═══ -->
        <section class="sticky-scene" data-scene id="scene1">
            <div class="sticky-scene__stage" aria-hidden="true">
                <div class="scene-head">
                    <span class="scene-no">ACT 01</span>
                    <span class="scene-name">THE FURNITURE</span>
                    <span class="scene-readout" data-readout></span>
                </div>
                <div class="qr-stage">
                    <div id="s1Grid"></div>
                    <div class="s1-legend">
                        <span class="li li-finder"><i style="background:var(--blue)"></i>FINDER ×3 — 147 MODULES</span>
                        <span class="li li-sep"><i style="background:#546cff3d"></i>SEPARATORS — 45</span>
                        <span class="li li-timing"><i style="background:#9db0ff"></i>TIMING — 10</span>
                        <span class="li li-dark"><i style="background:var(--orange)"></i>DARK MODULE — 1</span>
                        <span class="li li-fmt"><i style="background:#9db0ff;opacity:.55"></i>FORMAT STRIPS — 30</span>
                    </div>
                </div>
                <div class="stage-static">
                    @@FURNITURE_SVG@@
                    <div class="static-note">THE COMPLETE FURNITURE OF A 21×21 CODE — <b>233 MODULES</b> OF FINDERS, SEPARATORS, TIMING, FORMAT AND THE DARK MODULE. ONLY THE REMAINING 208 SEATS CARRY YOUR TEXT.</div>
                </div>
            </div>
            <div class="sticky-scene__steps">
                <article class="step" data-step="1">
                    <p>Start with the empty square: 441 modules, all unassigned. A scanner will
                        have to find this grid in a photo — tilted, half-lit, on a moving train —
                        before it can read a single bit of your text.</p>
                </article>
                <article class="step" data-step="2">
                    <p>So three <b>finder patterns</b> claim the corners: 7×7 squares whose rings
                        run dark–light–dark in the ratio <b>1:1:3:1:1</b> — in both directions.
                        That ratio is what a scanner hunts for, at any angle. The designers chose
                        it as the alternating pattern least likely to appear in ordinary print.</p>
                </article>
                <article class="step" data-step="3">
                    <p>Each finder gets a one-module light <b>separator</b>, so it cannot bleed
                        into data and masquerade as a fourth landmark. Three corners fix position
                        and orientation; the fourth is deliberately left free.</p>
                </article>
                <article class="step" data-step="4">
                    <p>Two <b>timing lines</b> cross the code on row and column 6, alternating
                        dark–light. They give the scanner a ruler: sample anywhere along them and
                        you know how wide a module is in this photo.</p>
                </article>
                <article class="step" data-step="5">
                    <p>Finally the <b>dark module</b> — always dark, no exceptions — and two
                        reserved <b>format strips</b> where the code will later announce its error
                        correction level and mask. The furniture is complete:
                        <b>233 of 441 modules</b> are already spent. Your text gets 208.</p>
                </article>
            </div>
        </section>

        <section class="prose">
            <h2><span class="sec-no">02</span>The bitstream</h2>
            <p>The 208 free seats will hold 26 <strong>codewords</strong> — bytes, eight bits
                each. Before anything is seated, the message itself has to become bits, in an
                order every reader on Earth agrees on.</p>
        </section>

        <!-- ═══ ACT 02 · THE BITSTREAM ═══ -->
        <section class="sticky-scene" data-scene id="scene2">
            <div class="sticky-scene__stage" aria-hidden="true">
                <div class="scene-head">
                    <span class="scene-no">ACT 02</span>
                    <span class="scene-name">THE BITSTREAM</span>
                    <span class="scene-readout" data-readout></span>
                </div>
                <div class="qr-stage">
                    <div class="s2-wrap">
                        <div class="s2-chars" id="s2Chars"></div>
                        <div class="s2-ribbon" id="s2Ribbon"></div>
                        <div class="s2-rack" id="s2Rack"></div>
                        <div class="s2-readout" id="s2Readout"></div>
                    </div>
                </div>
                <div class="stage-static">
                    <div class="s2-rack" style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:560px">
                        <span class="s2-cw on">40</span><span class="s2-cw on">B4</span><span class="s2-cw on">84</span><span class="s2-cw on">54</span><span class="s2-cw on">C4</span><span class="s2-cw on">C4</span><span class="s2-cw on">F2</span><span class="s2-cw on">05</span><span class="s2-cw on">74</span><span class="s2-cw on">F5</span><span class="s2-cw on">24</span><span class="s2-cw on">C4</span><span class="s2-cw on">40</span><span class="s2-cw on pad">EC</span><span class="s2-cw on pad">11</span><span class="s2-cw on pad">EC</span><span class="s2-cw on pad">11</span><span class="s2-cw on pad">EC</span><span class="s2-cw on pad">11</span>
                    </div>
                    <div class="static-note">THE 19 DATA CODEWORDS FOR HELLO WORLD AT LEVEL L — <b>13 MESSAGE BYTES, THEN EC/11 PADDING</b> — COMPUTED BY THE ENCODER IN THIS PAGE.</div>
                </div>
            </div>
            <div class="sticky-scene__steps">
                <article class="step" data-step="1">
                    <p>The payload: eleven characters. QR codes have four ways to write text —
                        digits pack three-per-ten-bits, uppercase packs two-per-eleven — but the
                        universal one is <b>byte mode</b>: any character, one byte each.</p>
                </article>
                <article class="step" data-step="2">
                    <p>Each character becomes its byte. <span class="mono">H</span> is
                        <span class="mono">01001000</span> — 72 — and so on for all eleven.
                        Text, to this machine, was always numbers.</p>
                </article>
                <article class="step" data-step="3">
                    <p>In front goes a header the reader can trust: the mode
                        <span class="mono">0100</span> (byte), then the count
                        <span class="mono">00001011</span> (eleven). No lengths are guessed in a
                        QR code; they are announced.</p>
                </article>
                <article class="step" data-step="4">
                    <p>A terminator of four zero bits closes the message. Header, data, close:
                        <b>104 bits</b> — exactly thirteen codewords.</p>
                </article>
                <article class="step" data-step="5">
                    <p>Six seats remain, so the encoder pads with alternating bytes
                        <span class="mono">EC 11 EC 11…</span> — not random filler, a fixed
                        pattern any reader can strip. The rack is full:
                        <b>19 data codewords</b>, ready for insurance.</p>
                </article>
            </div>
        </section>

        <section class="breather">
            <p class="breather-line reveal">Half the square was spoken for <em>before your text arrived.</em></p>
        </section>

        <!-- ═══ ACT 03 · THE INSURANCE ═══ -->
        <section class="sticky-scene" data-scene id="scene3">
            <div class="sticky-scene__stage" aria-hidden="true">
                <div class="scene-head">
                    <span class="scene-no">ACT 03</span>
                    <span class="scene-name">THE INSURANCE</span>
                    <span class="scene-readout" data-readout></span>
                </div>
                <div class="qr-stage">
                    <div class="s3-wrap">
                        <div class="s3-label" id="s3Label"><b>19 DATA CODEWORDS</b></div>
                        <div class="s3-wall" id="s3Data"></div>
                        <div class="s3-gen" id="s3Gen"></div>
                        <div class="s3-label" id="s3EcLabel">7 ERROR-CORRECTION CODEWORDS — THE REMAINDER</div>
                        <div class="s3-wall" id="s3Ec"></div>
                        <div class="s3-badge" id="s3Badge">26 TOTAL · CORRECTS <b>3</b> DAMAGED CODEWORDS</div>
                        <table class="s3-table" id="s3Table">
                            <tr><th>LEVEL</th><th>DATA</th><th>EC</th><th>CORRECTS</th></tr>
                        </table>
                    </div>
                </div>
                <div class="stage-static">
                    <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:560px">
                        <span class="s3-cw on">40</span><span class="s3-cw on">B4</span><span class="s3-cw on">84</span><span class="s3-cw on">54</span><span class="s3-cw on">C4</span><span class="s3-cw on">C4</span><span class="s3-cw on">F2</span><span class="s3-cw on">05</span><span class="s3-cw on">74</span><span class="s3-cw on">F5</span><span class="s3-cw on">24</span><span class="s3-cw on">C4</span><span class="s3-cw on">40</span><span class="s3-cw on">EC</span><span class="s3-cw on">11</span><span class="s3-cw on">EC</span><span class="s3-cw on">11</span><span class="s3-cw on">EC</span><span class="s3-cw on">11</span><span class="s3-cw on ec">C8</span><span class="s3-cw on ec">46</span><span class="s3-cw on ec">26</span><span class="s3-cw on ec">41</span><span class="s3-cw on ec">E8</span><span class="s3-cw on ec">F8</span><span class="s3-cw on ec">F6</span>
                    </div>
                    <div class="static-note">19 DATA + 7 ERROR-CORRECTION CODEWORDS = <b>26 TOTAL</b> — THE FULL PAYLOAD OF A 21×21 LEVEL-L CODE, COMPUTED ON THIS PAGE.</div>
                </div>
            </div>
            <div class="sticky-scene__steps">
                <article class="step" data-step="1">
                    <p>Nineteen codewords on the wall. A scratched module, a glint of glare, a
                        sticker across the corner — any of these can corrupt them. So QR codes
                        insure the payload before it ships.</p>
                </article>
                <article class="step" data-step="2">
                    <p>The tool is <b>Reed–Solomon</b> arithmetic. The encoder treats the data as
                        one long number and divides it by a fixed degree-7 generator over a
                        256-value finite field — the strip below the wall. You never see a decimal
                        point; addition is XOR, multiplication wraps like clockwork.</p>
                </article>
                <article class="step" data-step="3">
                    <p>It keeps only the <b>remainder</b>: seven bytes, different for every
                        message. For HELLO WORLD they are
                        <span class="mono">C8 46 26 41 E8 F8 F6</span> — computed by the code
                        rendering this page, not typed into it.</p>
                </article>
                <article class="step" data-step="4">
                    <p>Data plus remainder: 26 codewords. With seven parity bytes the code can
                        repair <b>any 3 damaged codewords</b> — unknown values, recomputed from
                        the survivors. That is the whole magic of a logo printed over a QR code:
                        the logo is damage, and the insurance pays for it.</p>
                </article>
                <article class="step" data-step="5">
                    <p>Insurance is a dial. Levels L, M, Q, H buy 7, 10, 13, 17 parity bytes —
                        correcting <b>3, 5, 6, 8</b> codewords — and pay for it with capacity:
                        19, 16, 13, 9 data codewords. A warehouse label picks H; a poster with a
                        clean print picks L.</p>
                </article>
            </div>
        </section>

        <!-- ═══ ACT 04 · THE ZIGZAG ═══ -->
        <section class="sticky-scene" data-scene id="scene4">
            <div class="sticky-scene__stage" aria-hidden="true">
                <div class="scene-head">
                    <span class="scene-no">ACT 04</span>
                    <span class="scene-name">THE ZIGZAG</span>
                    <span class="scene-readout" data-readout></span>
                </div>
                <div class="qr-stage">
                    <div class="s4-wrap" id="s4Wrap"></div>
                </div>
                <div class="stage-static">
                    @@SEATED_SVG@@
                    <div class="static-note">ALL <b>208 BITS SEATED</b> — DATA AND ERROR-CORRECTION CODEWORDS PLACED IN THE ZIGZAG ORDER, FURNITURE UNTOUCHED. THE MASK IS THE ONLY STEP LEFT.</div>
                </div>
            </div>
            <div class="sticky-scene__steps">
                <article class="step" data-step="1">
                    <p>Twenty-six codewords, 208 bits, 208 free seats — and a seating chart. It
                        starts at the <b>bottom-right corner</b>, in a two-module-wide column,
                        moving <b>upward</b>: right bit, then left bit.</p>
                </article>
                <article class="step" data-step="2">
                    <p>At the top, the next column pair drops and the direction flips:
                        down, then up, then down — a zigzag the reader can walk without a single
                        instruction beyond "start here".</p>
                </article>
                <article class="step" data-step="3">
                    <p>When the walk meets furniture — a format strip, a finder — the bits do not
                        overwrite it. They <b>wait</b> for the next free module. The chart serves
                        the furniture, never the reverse.</p>
                </article>
                <article class="step" data-step="4">
                    <p>One hard exception: the <b>vertical timing column</b> is never crossed.
                        When the zigzag reaches it, the next column pair simply starts to its
                        left.</p>
                </article>
                <article class="step" data-step="5">
                    <p>The columns climb toward the top-left finder. Every seat filled so far is
                        real: each module below is one actual bit of the 208, in order.</p>
                </article>
                <article class="step" data-step="6">
                    <p>All 208 bits seated; furniture intact; nothing left over. The code now
                        says exactly what it should — and it would still be hard to read. The
                        last problem is the pattern itself.</p>
                </article>
            </div>
        </section>

        <!-- ═══ ACT 05 · THE MASK ELECTION ═══ -->
        <section class="sticky-scene" data-scene id="scene5">
            <div class="sticky-scene__stage" aria-hidden="true">
                <div class="scene-head">
                    <span class="scene-no">ACT 05</span>
                    <span class="scene-name">THE MASK ELECTION</span>
                    <span class="scene-readout" data-readout></span>
                </div>
                <div class="qr-stage">
                    <div class="s5-wrap">
                        <div class="s5-detail" id="s5Detail"></div>
                        <div class="s5-rack" id="s5Rack"></div>
                        <div class="s5-fmt" id="s5Fmt"></div>
                        <div class="s5-note" id="s5Note"></div>
                    </div>
                </div>
                <div class="stage-static">
                    @@FINAL_SVG@@
                    <div class="static-note">THE FINISHED CODE — MASKED, WITH FORMAT STRIPS WRITTEN. <b>PENALTY SCORES FOR ALL EIGHT MASKS</b>: 452 · 642 · 538 · <b style="color:var(--acid)">444</b> · 587 · 521 · 546 · 492 — MASK 3 WINS.</div>
                </div>
            </div>
            <div class="sticky-scene__steps">
                <article class="step" data-step="1">
                    <p>Here is the unmasked code. The problem is visible: long runs of one color,
                        and shapes that imitate a finder. A scanner resolving modules along a
                        blurry line has no idea which square a smudge belongs to —
                        <b>big flat regions are where it fails</b>.</p>
                </article>
                <article class="step" data-step="2">
                    <p>The fix is a <b>mask</b>: a fixed formula that flips modules wherever it
                        says so. This one — mask 0 — flips every module whose row and column sum
                        to an even number: a checkerboard, drawn in acid. Flipping is free: the
                        reader applies the same formula and flips them back.</p>
                </article>
                <article class="step" data-step="3">
                    <p>There are eight formulas. The encoder applies each one and scores the
                        result with <b>penalty rules</b>: long runs cost 3 points per extra
                        module, 2×2 blocks cost 3, finder-lookalikes cost 40, and every step
                        away from 50% dark costs 10. The scores below are computed for this
                        exact code.</p>
                </article>
                <article class="step" data-step="4">
                    <p>The election: <b>lowest penalty wins</b>. Mask 3 scores 444 and takes it;
                        the runner-ups stay dimmed. Same message, same seats — only the flipping
                        rule differs.</p>
                </article>
                <article class="step" data-step="5">
                    <p>One duty left: announce the choice. The <b>format strips</b> carry five
                        bits — level L, mask 3 — protected by their own error-correcting code and
                        written <b>twice</b>, because a scanner that misreads the mask can decode
                        nothing at all. The square is finished.</p>
                </article>
            </div>
        </section>

        <!-- ═══ THE LAB ═══ -->
        <section class="lab" id="lab">
            <div class="lab-head">
                <span class="scene-no">THE LAB</span>
                <span class="scene-name">BREAK IT (ON PAPER)</span>
                <span class="scene-readout">DAMAGE VS BUDGET · COMPUTED</span>
            </div>
            <div class="lab-grid">
                <div class="lab-qr-wrap">
                    <svg id="labSvg" viewBox="-2 -2 25 25" shape-rendering="crispEdges" role="img" aria-label="The finished QR code, with damaged codewords covered in orange ink"></svg>
                </div>
                <div class="lab-ctrl">
                    <div>
                        <label for="labDamage">DAMAGE — CODEWORDS INKED</label>
                        <input class="lab-slider" id="labDamage" type="range" min="0" max="26" step="1" value="0" aria-label="Number of damaged codewords, 0 to 26">
                    </div>
                    <div role="radiogroup" aria-label="Error correction level">
                        <label>INSURANCE LEVEL</label>
                        <div class="lab-levels" id="labLevels">
                            <label><input type="radio" name="lablvl" value="L" checked><span>L</span></label>
                            <label><input type="radio" name="lablvl" value="M"><span>M</span></label>
                            <label><input type="radio" name="lablvl" value="Q"><span>Q</span></label>
                        </div>
                    </div>
                    <div class="lab-stats" id="labStats"></div>
                    <div class="lab-verdict ok" id="labVerdict" aria-live="polite"></div>
                </div>
            </div>
            <p class="lab-note">EACH ORANGE PATCH COVERS THE EIGHT MODULES OF ONE CODEWORD — REAL SEATS FROM THE ZIGZAG. THE VERDICT IS COMPUTED, NOT SIMULATED: THIS PAGE ENCODES, IT DOES NOT DECODE. THE BUDGET IS FLOOR(EC ÷ 2) PER REED–SOLOMON BLOCK; A VERSION-1 CODE HAS ONE BLOCK. YOUR CAMERA IS THE DECODER — THE HERO CODE AT THE TOP STILL SCANS. LEVEL H IS
    NOT IN THE PICKER FOR A REASON: IT SPENDS 17 OF A 21×21 CODE'S 26 CODEWORDS ON
    INSURANCE, LEAVING ONLY 9 DATA CODEWORDS — HELLO WORLD NEEDS 13, SO AT H IT ONLY
    FITS IN A VERSION 2 CODE.</p>
        </section>

        <section class="prose">
            <h2><span class="sec-no">03</span>One choreography, 1994 → now</h2>
            <p>Put together, a QR code is a small machine for being read badly: fixed furniture
                that announces the grid, Reed–Solomon insurance on the payload, a zigzag with no
                ambiguities, and a mask elected to keep the noise looking like noise. Nothing in
                the square is stored twice by accident — the format strips are the only
                redundancy that is not mathematics.</p>
            <p>The design dates to <strong>1994</strong>, when Masahiro Hara's team at Denso Wave
                — a Toyota supplier — needed to replace the stack of barcodes on each box of car
                parts with one symbol that could also carry kanji. The black-and-white counters
                of a Go board are the often-told inspiration; the finder's 1:1:3:1:1 came from a
                search for the alternating pattern least used on printed matter. "QR" stood for
                <strong>quick response</strong>, and the name kept its promise: standardized by
                AIM in 1997, by Japan as JIS X 0510 in 1999, then as ISO/IEC 18004 — now in its
                2024 edition. Denso Wave held the patents and chose not to enforce them for
                standardized codes, which is why the square spread from parts shelves to
                payments, boarding passes, and menus. "QR Code" remains its trademark.</p>
            <figure class="fin-fig reveal" aria-label="The finished version 1 code with its regions labeled: three finders, separators, timing lines, format strips, dark module, and the data region.">
                <div class="fin-inner" id="finFig">
                    @@FINAL_SVG@@
                    <span class="fin-tag">FINDER 1:1:3:1:1</span>
                    <span class="fin-tag t-blue" style="right:2%;top:6%">TIMING</span>
                    <span class="fin-tag t-blue" style="left:2%;bottom:14%">FORMAT ×2</span>
                    <span class="fin-tag t-orange" style="right:4%;bottom:4%">DATA + EC — 208 MODULES</span>
                </div>
                <div class="fin-cap">THE SAME HELLO WORLD CODE BUILT ON THIS PAGE — MASK 3, LEVEL L, 230 DARK MODULES OF 441</div>
            </figure>
            <p>Capacity is the one number people quote, so quote it exactly. At version 40 with
                level L — 177 × 177 modules — the maximums are:</p>
            <table class="caps reveal">
                <tr><th>MODE</th><th>PACKING</th><th>MAX AT 40-L</th></tr>
                <tr><td>Numeric</td><td>10 bits per 3 digits</td><td class="num"><b>7,089</b> digits</td></tr>
                <tr><td>Alphanumeric</td><td>11 bits per 2 characters</td><td class="num"><b>4,296</b> characters</td></tr>
                <tr><td>Byte</td><td>8 bits per byte</td><td class="num"><b>2,953</b> bytes</td></tr>
                <tr><td>Kanji</td><td>13 bits per character</td><td class="num"><b>1,817</b> characters</td></tr>
            </table>
            <p>Three kilobytes is the ceiling — a QR code is a label, not a file system. When a
                payload is longer, encoders switch modes mid-message (URLs lowercase their
                scheme, then pack the uppercase-legal path two characters at a time) or split
                across several codes. The micro and rectangular variants shrink the furniture for
                tiny parts; the ideas above do not change.</p>
            <div class="callout reveal">A QR code is not a picture of a link. It is
                <em>a choreography</em> — furniture, insured bits, assigned seats, an elected
                mask — that any camera can dance.</div>
            <div class="aside reveal">Scope: the standard square QR code ("model 2") in byte
                mode; the live encoder on this page implements versions 1–5 at all four levels,
                verified against a published Reed–Solomon test vector and decoded by an
                independent reader. Penalty scores, codewords, and damage verdicts are computed
                by the code that renders them. Correctable counts are the per-block guarantee
                floor(EC ÷ 2); the familiar "7 / 15 / 25 / 30%" figures are the standard's
                approximate restorable share of larger symbols. Sources:
                <a href="https://www.qrcode.com/en/history/" target="_blank" rel="noreferrer">Denso Wave · History of QR Code</a>,
                <a href="https://en.wikipedia.org/wiki/QR_code" target="_blank" rel="noreferrer">Wikipedia · QR code</a>,
                <a href="https://www.thonky.com/qr-code-tutorial/" target="_blank" rel="noreferrer">Thonky · QR Code Tutorial</a>,
                <a href="https://www.iso.org/standard/83389.html" target="_blank" rel="noreferrer">ISO/IEC 18004:2024</a>.</div>
            <footer class="foot reveal">
                <span>QR CODES · THE SPEC SHEET</span>
                <a href="/">engineering.victorbusque.com</a>
            </footer>
        </section>
    </main>
'''

PAGE_SCRIPT = r'''
    <script>
/* ════════════════════════════════════════════════════════════════════
   PAGE SCRIPT — a real byte-mode QR encoder (versions 1–5, L/M/Q/H).
   Every readout on this page is computed by this code: the bitstream,
   the Reed–Solomon remainder, penalty scores per mask, seat maps, and
   the damage-lab verdicts. Verified against a published V1-L test
   vector (data + EC codewords for "www.wikipedia.org").
   ════════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    /* ── GF(256), primitive polynomial 0x11D ── */
    var EXP = new Uint8Array(512), LOG = new Uint8Array(256);
    (function () {
        var x = 1, i;
        for (i = 0; i < 255; i++) {
            EXP[i] = x; LOG[x] = i;
            x <<= 1; if (x & 0x100) x ^= 0x11d;
        }
        for (i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
    })();
    function gmul(a, b) { return (a === 0 || b === 0) ? 0 : EXP[LOG[a] + LOG[b]]; }

    function rsRemainder(data, degree) {
        var gen = [1], i, j, next;
        for (i = 0; i < degree; i++) {
            next = new Array(gen.length + 1); for (j = 0; j < next.length; j++) next[j] = 0;
            for (j = 0; j < gen.length; j++) {
                next[j] ^= gmul(gen[j], 1);
                next[j + 1] ^= gmul(gen[j], EXP[i]);
            }
            gen = next;
        }
        var res = data.concat(new Array(degree)); for (i = 0; i < degree; i++) res[data.length + i] = 0;
        for (i = 0; i < data.length; i++) {
            var f = res[i]; if (f === 0) continue;
            for (j = 0; j < gen.length; j++) res[i + j] ^= gmul(gen[j], f);
        }
        return res.slice(data.length);
    }

    /* ── block tables v1–5: [ecPerBlock, dataCodewords] ── */
    var BLOCKS = {
        1: { L: [7, 19], M: [10, 16], Q: [13, 13], H: [17, 9] },
        2: { L: [10, 34], M: [16, 28], Q: [22, 22], H: [28, 16] },
        3: { L: [15, 55], M: [26, 44], Q: [18, 34], H: [22, 26] },
        4: { L: [20, 80], M: [18, 64], Q: [26, 48], H: [16, 36] },
        5: { L: [26, 108], M: [24, 86], Q: [18, 62], H: [22, 46] }
    };
    var ALIGN = { 1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30] };

    function buildData(text, v, lvl) {
        var bytes = [], i;
        for (i = 0; i < text.length; i++) bytes.push(text.charCodeAt(i) & 0xff);
        var total = BLOCKS[v][lvl][1];
        var bits = [];
        function push(val, n) { var k; for (k = n - 1; k >= 0; k--) bits.push((val >> k) & 1); }
        push(0b0100, 4);
        push(bytes.length, 8);
        for (i = 0; i < bytes.length; i++) push(bytes[i], 8);
        var room = total * 8 - bits.length;
        if (room < 0) throw new Error('message does not fit: capacity ' + total + ' codewords');
        push(0, Math.min(4, room));
        while (bits.length % 8) bits.push(0);
        var data = [];
        for (i = 0; i < bits.length; i += 8) {
            var b = 0; for (var k2 = 0; k2 < 8; k2++) b = (b << 1) | bits[i + k2];
            data.push(b);
        }
        var pad = 0xec;
        while (data.length < total) { data.push(pad); pad = (pad === 0xec) ? 0x11 : 0xec; }
        return { data: data, messageCodewords: Math.ceil((4 + 8 + bytes.length * 8 + 4) / 8), chars: text.split(''), charBytes: bytes };
    }

    function baseMatrix(v) {
        var size = v * 4 + 17;
        var m = [], r, c, i;
        for (r = 0; r < size; r++) { m.push([]); for (c = 0; c < size; c++) m[r].push(null); }
        function fp(r0, c0) {
            for (var dr = -1; dr <= 7; dr++) for (var dc = -1; dc <= 7; dc++) {
                var rr = r0 + dr, cc = c0 + dc;
                if (rr < 0 || cc < 0 || rr >= size || cc >= size) continue;
                var inSep = dr === -1 || dr === 7 || dc === -1 || dc === 7;
                var ring = Math.max(Math.abs(dr - 3), Math.abs(dc - 3));
                m[rr][cc] = inSep ? 0 : (ring !== 2 ? 1 : 0);
            }
        }
        fp(0, 0); fp(0, size - 7); fp(size - 7, 0);
        for (i = 8; i < size - 8; i++) { m[6][i] = (i % 2 === 0) ? 1 : 0; m[i][6] = (i % 2 === 0) ? 1 : 0; }
        var co = ALIGN[v], a, b2;
        for (a = 0; a < co.length; a++) for (b2 = 0; b2 < co.length; b2++) {
            var ar = co[a], ac = co[b2];
            if (m[ar][ac] !== null) continue;
            for (var dr2 = -2; dr2 <= 2; dr2++) for (var dc2 = -2; dc2 <= 2; dc2++) {
                m[ar + dr2][ac + dc2] = (Math.max(Math.abs(dr2), Math.abs(dc2)) !== 1) ? 1 : 0;
            }
        }
        m[size - 8][8] = 1;
        function res(r2, c2) { if (m[r2][c2] === null) m[r2][c2] = 0; }
        for (i = 0; i <= 8; i++) { if (i !== 6) { res(i, 8); res(8, i); } }
        for (i = 0; i < 8; i++) { res(8, size - 1 - i); res(size - 1 - i, 8); }
        return m;
    }

    function placement(size) {
        var seq = [], col = size - 1, up = true, i, r;
        while (col > 0) {
            if (col === 6) col--;
            for (i = 0; i < size; i++) {
                r = up ? (size - 1 - i) : i;
                seq.push([r, col]); seq.push([r, col - 1]);
            }
            up = !up; col -= 2;
        }
        return seq;
    }

    var MASKS = [
        function (r, c) { return (r + c) % 2 === 0; },
        function (r) { return r % 2 === 0; },
        function (r, c) { return c % 3 === 0; },
        function (r, c) { return (r + c) % 3 === 0; },
        function (r, c) { return ((r >> 1) + Math.floor(c / 3)) % 2 === 0; },
        function (r, c) { return ((r * c) % 2) + ((r * c) % 3) === 0; },
        function (r, c) { return (((r * c) % 2) + ((r * c) % 3)) % 2 === 0; },
        function (r, c) { return (((r + c) % 2) + ((r * c) % 3)) % 2 === 0; }
    ];

    function penalty(m) {
        var size = m.length, r, c, i, score = 0, run;
        for (r = 0; r < size; r++) {
            run = 1;
            for (c = 1; c < size; c++) {
                if (m[r][c] === m[r][c - 1]) run++;
                else { if (run >= 5) score += 3 + run - 5; run = 1; }
            }
            if (run >= 5) score += 3 + run - 5;
        }
        for (c = 0; c < size; c++) {
            run = 1;
            for (r = 1; r < size; r++) {
                if (m[r][c] === m[r - 1][c]) run++;
                else { if (run >= 5) score += 3 + run - 5; run = 1; }
            }
            if (run >= 5) score += 3 + run - 5;
        }
        for (r = 0; r < size - 1; r++) for (c = 0; c < size - 1; c++) {
            if (m[r][c] === m[r][c + 1] && m[r][c] === m[r + 1][c] && m[r][c] === m[r + 1][c + 1]) score += 3;
        }
        var pat = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0];
        var patR = pat.slice().reverse();
        function matchAt(line, i2) {
            var ok1 = true, ok2 = true, j;
            for (j = 0; j < 11; j++) {
                if (line[i2 + j] !== pat[j]) ok1 = false;
                if (line[i2 + j] !== patR[j]) ok2 = false;
            }
            return ok1 || ok2;
        }
        for (r = 0; r < size; r++) for (i = 0; i + 11 <= size; i++) if (matchAt(m[r], i)) score += 40;
        for (c = 0; c < size; c++) {
            var col = []; for (r = 0; r < size; r++) col.push(m[r][c]);
            for (i = 0; i + 11 <= size; i++) if (matchAt(col, i)) score += 40;
        }
        var dark = 0;
        for (r = 0; r < size; r++) for (c = 0; c < size; c++) if (m[r][c] === 1) dark++;
        score += Math.floor(Math.abs((dark * 100) / (size * size) - 50) / 5) * 10;
        return score;
    }

    function formatBits(lvl, mask) {
        var ecBits = { L: 1, M: 0, Q: 3, H: 2 }[lvl];
        var data = (ecBits << 3) | mask, rem = data, i;
        for (i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >> 9) * 0x537);
        return (((data << 10) | rem) ^ 0x5412) & 0x7fff;
    }

    function applyMask(m, k, probe) {
        var size = m.length, out = [], r, c;
        for (r = 0; r < size; r++) { out.push(m[r].slice()); }
        for (r = 0; r < size; r++) for (c = 0; c < size; c++) {
            if (probe[r][c] !== null || out[r][c] === null) continue;
            if (MASKS[k](r, c)) out[r][c] ^= 1;
        }
        return out;
    }

    function writeFormat(m, lvl, mask) {
        var size = m.length, bits = formatBits(lvl, mask), i;
        function get(i2) { return (bits >> i2) & 1; }
        for (i = 0; i <= 5; i++) m[i][8] = get(i);
        m[7][8] = get(6); m[8][8] = get(7); m[8][7] = get(8);
        for (i = 9; i < 15; i++) m[8][14 - i] = get(i);
        for (i = 0; i < 8; i++) m[8][size - 1 - i] = get(i);
        for (i = 8; i < 15; i++) m[size - 15 + i][8] = get(i);
        m[size - 8][8] = 1;
    }

    /* full encode — single block (v1) or interleaved (v2–5) */
    function encode(text, lvl, forceV) {
        var v = forceV || 1, i;
        if (!forceV) {
            var need = 4 + 8 + text.length * 8 + 4;
            for (i = 1; i <= 5; i++) { v = i; if (need <= BLOCKS[i][lvl][1] * 8) break; }
        }
        var size = v * 4 + 17;
        var parts = buildData(text, v, lvl);
        var ecPer = BLOCKS[v][lvl][0];
        var ec = rsRemainder(parts.data, ecPer);
        var final = parts.data.concat(ec);
        var probe = baseMatrix(v);
        var m = [], r, c;
        for (r = 0; r < size; r++) m.push(probe[r].slice());
        var seq = placement(size), seatOf = {}, bi = 0;
        var bits = [];
        final.forEach(function (b) { var k; for (k = 7; k >= 0; k--) bits.push((b >> k) & 1); });
        seq.forEach(function (rc) {
            if (m[rc[0]][rc[1]] === null && bi < bits.length) {
                m[rc[0]][rc[1]] = bits[bi];
                seatOf[rc[0] + ',' + rc[1]] = bi;
                bi++;
            }
        });
        var candidates = [], k2;
        for (k2 = 0; k2 < 8; k2++) candidates.push(penalty(applyMask(m, k2, probe)));
        var best = 0;
        candidates.forEach(function (s, idx) { if (s < candidates[best]) best = idx; });
        var masked = applyMask(m, best, probe);
        writeFormat(masked, lvl, best);
        var dark = 0;
        for (r = 0; r < size; r++) for (c = 0; c < size; c++) if (masked[r][c] === 1) dark++;
        return {
            version: v, lvl: lvl, size: size, data: parts.data, ec: ec, final: final,
            candidates: candidates, mask: best, matrix: masked, unmasked: m,
            seatOf: seatOf, correctable: Math.floor(ecPer / 2), ecPer: ecPer,
            dark: dark, chars: parts.chars, charBytes: parts.charBytes, messageCodewords: parts.messageCodewords
        };
    }

    /* ── SVG helpers ── */
    var NS = 'http://www.w3.org/2000/svg';
    function svgEl(tag, attrs, parent) {
        var e = document.createElementNS(NS, tag), k;
        for (k in attrs) e.setAttribute(k, attrs[k]);
        if (parent) parent.appendChild(e);
        return e;
    }
    function hex(b) { return b.toString(16).toUpperCase(); }

    var HW = encode('HELLO WORLD', 'L', 1);

    /* ── role map for a v1 grid ── */
    function rolesV1() {
        var size = 21, role = [], r, c;
        for (r = 0; r < size; r++) { role.push([]); for (c = 0; c < size; c++) role[r].push('free'); }
        var finders = [[0, 0], [0, 14], [14, 0]];
        finders.forEach(function (f) {
            for (r = 0; r < size; r++) for (c = 0; c < size; c++) {
                var inBox = r >= f[0] && r < f[0] + 7 && c >= f[1] && c < f[1] + 7;
                var inRing = r >= f[0] - 1 && r < f[0] + 8 && c >= f[1] - 1 && c < f[1] + 8;
                if (inBox) role[r][c] = 'finder';
                else if (inRing) role[r][c] = 'sep';
            }
        });
        for (var i = 8; i < size - 8; i++) { role[6][i] = 'timing'; role[i][6] = 'timing'; }
        role[13][8] = 'dark';
        for (i = 0; i <= 8; i++) {
            if (i !== 6) {
                if (role[i][8] === 'free') role[i][8] = 'fmt';
                if (role[8][i] === 'free') role[8][i] = 'fmt';
            }
        }
        for (i = 0; i < 8; i++) {
            if (role[8][size - 1 - i] === 'free') role[8][size - 1 - i] = 'fmt';
            if (role[size - 1 - i][8] === 'free') role[size - 1 - i][8] = 'fmt';
        }
        return role;
    }

    /* ══ SCENE 1 — the furniture ══ */
    function buildS1() {
        var host = document.getElementById('s1Grid');
        if (!host) return;
        var svg = svgEl('svg', { viewBox: '-1.5 -1.5 24 24', class: 'qr-grid-svg', 'shape-rendering': 'crispEdges' }, host);
        var role = rolesV1();
        var layers = { finder: [], sep: [], timing: [], dark: [], fmt: [] };
        var r, c;
        for (r = 0; r < 21; r++) for (c = 0; c < 21; c++) {
            var ro = role[r][c];
            var rect = svgEl('rect', {
                x: c - 0.44, y: r - 0.44, width: 0.88, height: 0.88,
                class: 'm ' + (ro === 'free' ? 'base' : '')
            }, svg);
            if (layers[ro]) layers[ro].push(rect);
        }
        /* role classes applied per layer group so steps can reveal them */
        Object.keys(layers).forEach(function (k3) {
            layers[k3].forEach(function (rect) {
                rect.setAttribute('class', 'm ' + (k3 === 'dark' ? 'darkmod' : k3));
                rect.classList.add('lyr');
                rect.classList.add('lyr-' + k3);
            });
        });
    }

    /* ══ SCENE 2 — the bitstream ══ */
    function buildS2() {
        var chars = document.getElementById('s2Chars');
        var ribbon = document.getElementById('s2Ribbon');
        var rack = document.getElementById('s2Rack');
        if (!chars) return;
        var bytes = [];
        HW.chars.forEach(function (ch, i) { bytes.push(HW.charBytes[i]); });
        /* char tiles */
        var html = '';
        HW.chars.forEach(function (ch, i) {
            html += '<div class="s2-char">' + (ch === ' ' ? '␣' : VB.esc(ch)) + '<small>' + hex(HW.charBytes[i]) + '</small></div>';
        });
        chars.innerHTML = html;
        /* ribbon: mode 4 + count 8 + data 88 + term 4 = 104 bits */
        var bits = [];
        function push(v, n) { var k; for (k = n - 1; k >= 0; k--) bits.push((v >> k) & 1); }
        push(4, 4); push(11, 8);
        bytes.forEach(function (b) { var k; for (k = 7; k >= 0; k--) bits.push((b >> k) & 1); });
        push(0, 4);
        var segOf = function (i) {
            if (i < 4) return 'seg-mode';
            if (i < 12) return 'seg-count';
            if (i < 100) return 'seg-data';
            return 'seg-term';
        };
        html = '';
        bits.forEach(function (b, i) {
            html += '<span class="s2-bit ' + segOf(i) + (b ? ' one' : '') + '" data-i="' + i + '">' + b + '</span>';
        });
        ribbon.innerHTML = html;
        /* rack: 13 message codewords + 6 pad */
        html = '';
        HW.data.forEach(function (cw, i) {
            html += '<span class="s2-cw ' + (i >= HW.messageCodewords ? 'pad' : '') + '" data-i="' + i + '">' + hex(cw) + '</span>';
        });
        rack.innerHTML = html;
        updateS2(0);
    }
    function updateS2(step) {
        var bits = document.querySelectorAll('#s2Ribbon .s2-bit');
        var cws = document.querySelectorAll('#s2Rack .s2-cw');
        var readout = document.getElementById('s2Readout');
        /* step 2: the 88 data bits; step 3: header joins; step 4: terminator joins */
        bits.forEach(function (b) {
            var i = +b.getAttribute('data-i');
            var on = step === 2 ? (i >= 4 && i < 92)
                : step === 3 ? (i < 100)
                    : step >= 4;
            b.classList.toggle('on', on);
        });
        cws.forEach(function (c) {
            var i = +c.getAttribute('data-i');
            var on = step >= 5 ? true : (step >= 4 && i < 13);
            c.classList.toggle('on', on);
        });
        if (readout) {
            var t = '';
            if (step === 1) t = '11 CHARACTERS · BYTE MODE';
            if (step === 2) t = '11 × 8 = <b>88 BITS</b>';
            if (step === 3) t = 'HEADER 0100 · 00001011 — <b>4 + 8 BITS</b>';
            if (step === 4) t = 'TERMINATOR 0000 — <b>104 BITS = 13 CODEWORDS</b>';
            if (step === 5) t = 'PAD EC·11 → <b>19 DATA CODEWORDS</b>';
            readout.innerHTML = t;
        }
    }

    /* ══ SCENE 3 — the insurance ══ */
    function buildS3() {
        var host = document.getElementById('s3Data');
        if (!host) return;
        var html = '';
        HW.data.forEach(function (cw) { html += '<span class="s3-cw">' + hex(cw) + '</span>'; });
        host.innerHTML = html;
        var gen = [1, 127, 122, 154, 164, 11, 68, 117];
        html = '';
        gen.forEach(function (g) { html += '<span class="s3-cw">' + g + '</span>'; });
        document.getElementById('s3Gen').innerHTML = html;
        html = '';
        HW.ec.forEach(function (cw) { html += '<span class="s3-cw ec">' + hex(cw) + '</span>'; });
        document.getElementById('s3Ec').innerHTML = html;
        var tbl = document.getElementById('s3Table');
        [['L', 19, 7, 3], ['M', 16, 10, 5], ['Q', 13, 13, 6], ['H', 9, 17, 8]].forEach(function (row) {
            var tr = document.createElement('tr');
            if (row[0] === 'L') tr.className = 'cur';
            tr.innerHTML = '<td>' + row[0] + (row[0] === 'L' ? ' ◄' : '') + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td><b>' + row[3] + '</b></td>';
            tbl.appendChild(tr);
        });
        updateS3(0);
    }
    function updateS3(step) {
        var data = document.querySelectorAll('#s3Data .s3-cw');
        var gen = document.querySelectorAll('#s3Gen .s3-cw');
        var ec = document.querySelectorAll('#s3Ec .s3-cw');
        var badge = document.getElementById('s3Badge');
        var tbl = document.getElementById('s3Table');
        var genLabel = document.getElementById('s3GenWrap');
        var ecLabel = document.getElementById('s3EcLabel');
        data.forEach(function (c) { c.classList.toggle('on', step >= 1); });
        gen.forEach(function (c) { c.classList.toggle('on', step === 2); });
        ec.forEach(function (c) { c.classList.toggle('on', step >= 3); });
        if (badge) badge.classList.toggle('on', step >= 4);
        if (tbl) tbl.classList.toggle('on', step >= 5);
        if (ecLabel) ecLabel.style.opacity = step >= 3 ? 1 : 0.25;
    }

    /* ══ SCENE 4 — the zigzag ══ */
    var s4Rects = {}, s4Cursor = null, s4PathEl = null, s4ByBit = {};
    function buildS4() {
        var host = document.getElementById('s4Wrap');
        if (!host) return;
        var svg = svgEl('svg', { viewBox: '-1.5 -1.5 24 24', class: 'qr-grid-svg', 'shape-rendering': 'crispEdges' }, host);
        var probe = baseMatrix(1);
        var role = rolesV1();
        var seq = placement(21);
        var seatIdx = {};
        Object.keys(HW.seatOf).forEach(function (k4) { seatIdx[k4] = HW.seatOf[k4]; });
        var r, c, i;
        /* furniture ghosts */
        for (r = 0; r < 21; r++) for (c = 0; c < 21; c++) {
            var ro = role[r][c];
            var cls = 'm ' + (ro === 'finder' ? 'ghost' : ro === 'free' ? 'base' : 'ghost');
            svgEl('rect', { x: c - 0.44, y: r - 0.44, width: 0.88, height: 0.88, class: cls, 'data-r': r, 'data-c': c }, svg);
        }
        /* seated data rects, in bit order */
        var byBit = s4ByBit = {};
        Object.keys(seatIdx).forEach(function (k5) {
            byBit[seatIdx[k5]] = k5.split(',');
        });
        for (i = 0; i < 208; i++) {
            var rc = byBit[i];
            var rect = svgEl('rect', { x: rc[1] - 0.44, y: rc[0] - 0.44, width: 0.88, height: 0.88, class: 'm seat' + (i >= 152 ? ' ec' : ''), 'data-bit': i }, svg);
            rect.style.opacity = 0;
            s4Rects[i] = rect;
        }
        /* the walk trace */
        var d = '';
        for (i = 0; i < 208; i++) {
            var rc2 = byBit[i];
            d += (i === 0 ? 'M' : 'L') + (rc2[1] * 1) + ' ' + (rc2[0] * 1) + ' ';
        }
        s4PathEl = svgEl('path', { d: d, class: 's4-path' }, svg);
        s4Cursor = svgEl('rect', { x: 20 - 0.65, y: 20 - 0.65, width: 1.3, height: 1.3, class: 's4-cursor' }, svg);
        updateS4(0);
    }
    function updateS4(step) {
        /* cumulative seat cutoffs after each 2-wide column pair */
        var cutoffs = [24, 48, 72, 96, 136, 208];
        var n = cutoffs[Math.max(0, Math.min(5, step - 1))] || 0;
        var i;
        for (i = 0; i < 208; i++) {
            s4Rects[i].style.opacity = i < n ? 1 : 0;
        }
        if (s4Cursor) {
            if (n >= 208) { s4Cursor.style.opacity = 0; }
            else {
                var rc = s4ByBit[n] || s4ByBit[0];
                s4Cursor.setAttribute('x', rc[1] - 0.65);
                s4Cursor.setAttribute('y', rc[0] - 0.65);
                s4Cursor.style.opacity = 1;
            }
        }
        if (s4PathEl) s4PathEl.style.opacity = (step >= 6) ? 1 : 0;
    }

    /* ══ SCENE 5 — the mask election ══ */
    function buildS5() {
        var detail = document.getElementById('s5Detail');
        var rack = document.getElementById('s5Rack');
        var fmt = document.getElementById('s5Fmt');
        if (!detail) return;
        /* detail grid: unmasked + mask-0 checkerboard overlay + worst run */
        var svg = svgEl('svg', { viewBox: '-1.5 -1.5 24 24', class: 'qr-grid-svg', 'shape-rendering': 'crispEdges' }, detail);
        svg.setAttribute('id', 's5DetailSvg');
        var r, c;
        /* worst horizontal run inside the DATA region (function modules are
           not scanner blind spots) */
        var probe5 = baseMatrix(1);
        var best = { len: 1, r: 0, c: 0 };
        for (r = 0; r < 21; r++) {
            var run = 0, runStart = 0;
            for (c = 0; c < 21; c++) {
                if (probe5[r][c] !== null) { run = 0; continue; }
                if (run === 0) runStart = c;
                if (c > runStart && HW.unmasked[r][c] !== HW.unmasked[r][c - 1]) { run = 1; runStart = c; }
                else run++;
                if (run > best.len) { best = { len: run, r: r, c: c }; }
            }
        }
        for (r = 0; r < 21; r++) for (c = 0; c < 21; c++) {
            var on = HW.unmasked[r][c] === 1;
            var base = 'm ' + (on ? 'seat' : 'ghost');
            var rect = svgEl('rect', { x: c - 0.44, y: r - 0.44, width: 0.88, height: 0.88, class: base }, svg);
            rect.style.opacity = on ? 1 : 0.15;
            if (probe5[r][c] === null && MASKS[0](r, c)) svgEl('rect', { x: c - 0.44, y: r - 0.44, width: 0.88, height: 0.88, class: 'ovl' }, svg);
        }
        svgEl('rect', { x: best.c - best.len + 1 - 0.55, y: best.r - 0.55, width: best.len + 0.1, height: 1.1, class: 'runhl' }, svg);
        /* the 8 candidates */
        var html = '';
        HW.candidates.forEach(function (score, k6) {
            var isBest = k6 === HW.mask;
            html += '<div class="s5-cand' + (isBest ? ' best' : '') + '" data-k="' + k6 + '"><span class="tag-no">' + k6 + '</span><div class="pen">' + (isBest ? '★ ' : '') + score + '</div></div>';
        });
        rack.innerHTML = html;
        /* inject mini svg per candidate */
        Array.prototype.forEach.call(rack.querySelectorAll('.s5-cand'), function (cand) {
            var k7 = +cand.getAttribute('data-k');
            var mini = svgEl('svg', { viewBox: '-0.5 -0.5 22 22', 'shape-rendering': 'crispEdges' });
            cand.insertBefore(mini, cand.firstChild);
            var r2, c2;
            for (r2 = 0; r2 < 21; r2++) for (c2 = 0; c2 < 21; c2++) {
                var m = applyMask(HW.unmasked, k7, baseMatrix(1))[r2][c2];
                if (m === 1) svgEl('rect', { x: c2 - 0.46, y: r2 - 0.46, width: 0.92, height: 0.92, fill: '#e8e6df' }, mini);
            }
        });
        /* format strips */
        var fbits = formatBits('L', HW.mask).toString(2).padStart(15, '0');
        var fhtml = '';
        [1, 2].forEach(function (copy) {
            fhtml += '<div><div class="strip">' + fbits.split('').map(function (b) { return '<span class="fb' + (b === '1' ? ' one' : '') + '">' + b + '</span>'; }).join('') + '</div><div class="flab">COPY ' + copy + ' — 15 BITS</div></div>';
        });
        fmt.innerHTML = fhtml + '<div class="flab">EC LEVEL L · MASK ' + HW.mask + ' — BCH-PROTECTED</div>';
        updateS5(0);
    }
    function updateS5(step) {
        var cands = document.querySelectorAll('#s5Rack .s5-cand');
        var fmt = document.getElementById('s5Fmt');
        var note = document.getElementById('s5Note');
        cands.forEach(function (c) {
            c.classList.toggle('on', step >= 3);
            c.classList.toggle('dim', step === 4 && c.getAttribute('data-k') !== String(HW.mask));
        });
        if (fmt) fmt.classList.toggle('on', step >= 5);
        if (note) {
            var t = '';
            if (step === 1) t = 'WORST RUN: <b>10 MODULES</b> — A SCANNER\'S BLIND SPOT';
            if (step === 2) t = 'MASK 0: FLIP WHERE (ROW + COLUMN) IS EVEN';
            if (step === 3) t = '8 CANDIDATES · PENALTY = RUNS + BLOCKS + LOOKALIKES + DARK SHARE';
            if (step === 4) t = 'WINNER — MASK 3 · PENALTY <b>444</b> (COMPUTED)';
            if (step === 5) t = 'THE CHOICE IS ANNOUNCED — TWICE';
            note.innerHTML = t;
        }
    }

    /* ══ THE LAB ══ */
    var labState = { lvl: 'L', dmg: 0 };
    function renderLab() {
        var svg = document.getElementById('labSvg');
        if (!svg) return;
        var enc = encode('HELLO WORLD', labState.lvl, 1);
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        var r, c;
        for (r = 0; r < 21; r++) for (c = 0; c < 21; c++) {
            svgEl('rect', {
                x: c - 0.46, y: r - 0.46, width: 0.92, height: 0.92,
                class: 'm ' + (enc.matrix[r][c] === 1 ? 'dark' : 'light')
            }, svg);
        }
        /* ink the first dmg codewords' seats */
        var seatByBit = {};
        Object.keys(enc.seatOf).forEach(function (k8) { seatByBit[enc.seatOf[k8]] = k8.split(','); });
        var inked = 0;
        for (var b3 = 0; b3 < labState.dmg * 8 && b3 < 208; b3++) {
            var rc3 = seatByBit[b3];
            if (!rc3) continue;
            svgEl('rect', { x: rc3[1] - 0.48, y: rc3[0] - 0.48, width: 0.96, height: 0.96, class: 'ink' }, svg);
            inked++;
        }
        var budget = enc.correctable;
        var ok = labState.dmg <= budget;
        var verdict = document.getElementById('labVerdict');
        var stats = document.getElementById('labStats');
        if (verdict) {
            verdict.className = 'lab-verdict ' + (ok ? 'ok' : 'bad');
            verdict.innerHTML = (labState.dmg === 0 ? 'PRISTINE — NOTHING TO CORRECT'
                : ok ? 'WITHIN BUDGET — DECODABLE'
                    : 'BUDGET EXCEEDED — THE SCAN DIES HERE')
                + '<span class="sub">' + labState.dmg + ' / ' + budget + ' CORRECTABLE CODEWORDS DAMAGED</span>';
        }
        if (stats) {
            stats.innerHTML = '<span>VERSION <b>1 · 21×21</b></span><span>DATA <b>' + enc.data.length + '</b></span><span>EC <b>' + enc.ecPer + '</b></span><span>TOTAL <b>' + enc.final.length + '</b></span><span>BUDGET <b>' + budget + '</b></span>';
        }
    }
    function wireLab() {
        var slider = document.getElementById('labDamage');
        var levels = document.getElementById('labLevels');
        if (slider) {
            slider.addEventListener('input', function () {
                labState.dmg = +slider.value;
                renderLab();
            });
        }
        if (levels) {
            levels.querySelectorAll('input').forEach(function (inp) {
                inp.addEventListener('change', function () {
                    labState.lvl = inp.value;
                    renderLab();
                });
            });
        }
        renderLab();
    }

    /* ── boot ── */
    function boot() {
        buildS1();
        buildS2();
        buildS3();
        buildS4();
        buildS5();
        wireLab();
        if (window.VBScene) {
            window.VBScene.onStep(function (scene, stepEl, idx) {
                var id = scene.id;
                if (id === 'scene2') updateS2(idx);
                if (id === 'scene3') updateS3(idx);
                if (id === 'scene4') updateS4(idx);
                if (id === 'scene5') updateS5(idx);
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
</script>
'''

SHARED_TAIL = r'''    <script src="../js/post-progress.js" defer></script>
    <script src="../js/post-nav.js" defer></script>
'''

# ── build (parts are defined above) ──
def build():
    html = HEAD.replace('@@VB_HELPERS@@', vb_helpers)
    html += BODY
    html = html.replace('@@HERO_SVG@@', hero_svg)
    html = html.replace('@@FURNITURE_SVG@@', furniture_svg)
    html = html.replace('@@SEATED_SVG@@', seated_svg)
    html = html.replace('@@FINAL_SVG@@', final_svg)
    html += PAGE_SCRIPT
    html += site_runtime + scene_runtime + SHARED_TAIL + sw
    html += '\n</body>\n\n</html>\n'

    out = ROOT / 'blog' / 'how-qr-codes-work.html'
    out.write_text(html)
    print('wrote', out, len(html), 'bytes')

build()
