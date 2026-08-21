---
topic: apollo-to-phone
status: ready-for-build
language: en
source_context: blog/apollo-to-phone.html (2026-08 shipped article — its sources section is the evidence record for this redesign; no separate context.md exists)
created: 2026-10-08
updated: 2026-10-08
intended_slug: apollo-to-phone
---

# Apollo in Your Pocket — A Game of Changing Scale

> **Purpose of this file:** build brief for the redesign of
> `blog/apollo-to-phone.html`, drafted as `blog/apollo-to-phone-v2.html`
> (noindex) until it replaces the shipped file in place. The shipped article
> defended its methodology and buried the idea under the defense. This
> redesign makes a more fundamental change: the article stops being "an
> article containing visualizations" and becomes **a game of changing scale**
> — the numbers drive the visual world itself.

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Curious engineers and lay readers who have heard "your phone is more powerful than Apollo" and suspect it is both true and meaningless. No hardware background assumed. |
| Central question | How far did computing come? Measured — not scored. |
| One-sentence answer | On every countable scale the two machines are separated by factors that stop being intuitive (≈298× smaller, ≈136× lighter, ≈2.97M× the writable memory, ≈4,160× the clock), and where no honest ratio exists (computation), the article refuses the number. |
| Core takeaway | **The computer that went to the Moon became invisible.** The astonishing thing isn't that the phone is more powerful; it's that computing became dense enough to disappear inside everyday objects. |
| Why it matters | "More powerful than Apollo" is the most common computing comparison in popular culture and it is measurably empty. The unit-change game gives the reader a reusable habit: choose a unit, replicate it, change the unit, and never trust a single composite "power" number. |
| Scope and exclusions | Compares the Block II AGC with the iPhone 17 Pro Max on: bounding-box size/volume, mass, erasable memory, reported clock, average instruction rate, named compute engines, and compute density. Does NOT claim performance equivalence, "the phone could fly the mission", transistor counts, or energy efficiency (no authoritative like-for-like sources — deliberately excluded; the method note says so). |
| Narrative point of view | A scientific experiment with a ruler: both machines on one table; each chapter plays the same game with a different unit. |
| Reading language | English. |

### Reader journey

```text
Before: "A phone is way more powerful than Apollo" — one fuzzy number.
Bridge: One repeated interaction — HERE IS ONE THING; USE IT AS THE UNIT;
        HOW MANY FIT INTO THE OTHER THING? — played four times
        (size → mass → memory → time), each ending in a ratio the reader
        watched emerge.
After:  "The gap is real but it is several absurd ratios on separate
        scales — and the truly strange part is that computing became dense
        enough to disappear."
```

### The repeated chapter grammar (the interaction the reader learns)

```text
MEASUREMENT → ESTABLISH UNIT → ZOOM OUT → CHANGE THE UNIT →
REPLICATE → INTRODUCE PHONE → RATIO EMERGES
```

Raw computation is deliberately **not staged as a scale** — the two
machines share no unit. The refusal lives in the time-scene caveat, the
ledger's "no honest single ratio" row, and the method note.

Semantic color, held constant through every chapter: **orange = Apollo**,
**blue = modern phone**, **ink = the ruler / the unit**.

### Plain-language opening and ending

- **Opening promise:** How far did computing come? Put the computer that flew
  Apollo next to the computer in your pocket — not with a power score, with a
  ruler. **"Scroll to change the scale."** establishes the mechanic.
- **Ending:** The astonishing thing isn't that your phone is more powerful
  than Apollo's computer — it's that the computer stopped being the thing you
  noticed. In 1969 computing was a machine; today it is a layer underneath
  everything. **The computer that went to the Moon became invisible.**

## 2. Evidence and editorial boundaries

Evidence record: the shipped article's sources plus additions verified during
the redesigns (E7, E10, E11). Stage readouts are live counts computed by the
page script from these values.

| ID | Claim or datum | Type | Source / anchor | Caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | AGC enclosure ~61 × 32 × 17 cm, 31.8 kg | verified | NASA CR 182505 (NTRS 19880069935) | Bounding box, not internal volume | hero, S01, ledger |
| E2 | iPhone 17 Pro Max 16.34 × 7.8 × 0.875 cm, 233 g | verified | Apple specifications | Bounding box | hero, S01, S02, ledger |
| E3 | AGC erasable memory 2,048 words × 15 bits = 3,840 byte-equivalents | verified | Virtual AGC / Block II literature | Writable memory only | S03, meaning |
| E4 | Phone reported system memory 11.42 GB (decimal) | verified | Geekbench Browser sample 18452470 | One reported sample; always "reported" | S03, ledger |
| E5 | AGC clock 1.024 MHz; A19 Pro reported 4.26 GHz | verified | Virtual AGC; Geekbench sample | Frequency comparison, not performance; 4.26 GHz is one reported peak core — never multiplied by core count | S04, ledger |
| E6 | A19 Pro: 6 CPU + 6 GPU + 16 Neural Engine cores | verified | Apple specifications | Named engines only; not a die map; not summed | S06, ledger |
| E7 | AGC fixed memory 36,864 words of hand-woven core rope | verified | Ken Shirriff, righto.com (2019) | Program store, kept out of the writable comparison | meaning aside |
| E8 | Derived: volume ≈297.6→298×, depth ≈19.4×, mass ≈136.5→136×, memory ≈2,973,958×, clock ≈4,160× | inference | Computed by page script on every load | Prose says "about" | scenes, chips, ledger |
| E9 | Powers-of-1,024 walls: 1× → 1,024× → 1,048,576×; phone ≈ 2.84 walls (94.5% of a 3-wall track) | illustrative | Constructed unit-swap ladder; marker computed | Labeled a zoom device | S03 |
| E10 | AGC average instruction time ≈24 μs (two 11.72 μs memory cycles) → ≈41,700 average instructions/s; literature ≈40,000–43,000/s | verified range, computed display | Virtual AGC memory cycle; AGC literature | Always "average"; instruction mix varies | S04, ledger |
| E11 | iPhone 17 Pro Geekbench 6 multi-core ≈9,000+ | verified | Geekbench Browser aggregate | Benchmark score — NOT instructions/s, NOT FLOPS; varies by sample; named only as the refused artifact (the phone's instruction rate is not published) | ledger |

### Facts to preserve exactly

- 2,048 words × 15 bits · 36,864 words rope · 61 × 32 × 17 cm · 31.8 kg ·
  1.024 MHz · ≈41,700 average instructions/s for the AGC.
- 16.34 × 7.8 × 0.875 cm · 233 g · 11.42 GB *reported* · 4.26 GHz
  *reported* · 6 + 6 + 16 cores for the phone.

### Claims to avoid or qualify

- Never "the phone is N times more powerful" — computation has **no honest
  single ratio**, and the article says so as a result, not an apology; the
  phone's instructions/s is not a published figure, and benchmark scores are
  never presented as rates.
- Never multiply peak clock by core count — 4.26 GHz is one reported peak
  core of six; peak is not sustained all-core speed.
- Never transistor counts or performance-per-watt (sources not defensible).
- Clock ratio always labeled "frequency comparison, not a performance
  benchmark"; clock cycles ≠ instructions.
- Volume is bounding-box; memory is erasable-only vs reported RAM, with the
  rope exclusion stated in an aside.

## 3. Narrative architecture

| Act | Reader question | Beat | Scroll mechanic | Evidence |
| --- | --- | --- | --- | --- |
| 0 · Hook | How different are these two things? | Hero: both machines at one true scale (SVG units = cm); "Scroll to change the scale."; no comparison chips up front | static drawing | E1, E2 |
| 1 · The game | What am I about to do? | The one move ("Here is one thing…"), color legend (orange/blue/ink), honesty rule, index of four scales + the missing fifth | static prose | — |
| 2 · Size | How much space? | Face → depth → **change the unit to one phone-volume**: transparent AGC box fills with 298 blue phone silhouettes, counted live | sticky, 3 steps | E1, E2, E8 |
| 3 · Mass | How much material? | Beam balance slams left (31.8 kg vs 233 g); phones pile up until the beam levels at 136 | sticky, 3 steps | E2, E8 |
| 4 · Memory ★ | How much memory, felt? | 2,048 cells → whole grid becomes ONE orange unit → wall of 1,024 → wall becomes one tile → mega-wall 1,048,576 → phone marker lands at ≈2.84 walls | sticky, 5 steps | E3, E4, E8, E9 |
| 5 · Meaning | Why does the number matter? | "Memory went from a budget to an assumption" + rope aside | static prose | E3, E7 |
| 6 · Time | What happens inside one second? | AGC's whole second as a small bar at a stated scale; the phone's same second at that scale runs off the reader's screen; caveat chip | sticky, 3 steps | E5, E8, E10 |
| 7 · Density | What did density do? | Scene header "THE OTHER QUESTION · DENSITY": big nearly-empty card (33 L · 1 processor) vs tiny packed card (111.5 mL · 28 cores); "dense enough to disappear" | sticky, 3 steps | E1, E2, E6 |
| 8 · Reconstruction | Can I see it all at once? | The AGC's five numbers become the chapter objects again; ledger rows assemble one per step | sticky, 5 steps | E8 |
| 9 · Ledger | The exact numbers | Static spec-sheet table incl. the "no honest single ratio" row | static table | all |
| 10 · Synthesis | So what changed? | Dark closing: "the computer stopped being the thing you noticed" → **"became invisible"** | static | inference |

## 4. Scene specifications

Common pattern: sticky scene (`sticky-scene` + `sticky-scene__stage`
aria-hidden + `sticky-scene__steps` with sequential `data-step` articles),
page-owned step engine keyed off `data-active-step`-equivalent
`data-step` on the section; count-ups are rAF-driven live readouts that
resolve instantly under reduced motion; no-JS collapses to stacked prose
(stage hidden). Mobile: steps dock as bottom cards; visuals scale, never clip.

- **S01 SIZE (3 steps).** Stage: two SVG figures (units = cm) + DOM fill.
  Step 3 fills the transparent AGC box with `round(volumeRatio)` = 298 phone
  glyphs (staggered) while a readout counts to 298; caption "bounding-box
  volume — not usable internal space". Acceptance: DOM glyph count = computed
  ratio; count-up ends exactly on it.
- **S02 MASS (3 steps).** Beam balance; `--tilt` runs −6° → 0° driven by the
  count-up progress callback; pile = `round(massRatio)` = 136 glyphs.
  Verdict "1 AGC ≈ 136 iPhones". Acceptance: pile count = computed ratio.
- **S03 MEMORY (5 steps, signature).** Exactly 2,048 + 1,024 + 1,024
  script-generated cells. Unit swaps are scale+fade transforms (no continuous
  zoom). Phone marker width = `wallsInPhone/3` of a 3-wall track = 94.5%,
  computed inline. Readouts count to 1,024 / 1,048,576 / 2,973,958.
  Acceptance: generated cell counts exact; marker fraction = computed 2.84.
- **S04 TIME (3 steps).** Two bars, one stated scale: the AGC bar is one
  whole second of its clock (1,024,000 cycles, ~92 px); the phone bar is the
  same second at the same scale — 4,160× longer — and physically runs off
  the reader's screen (width 190vw, clipped by the stage) with an
  "OFF YOUR SCREEN»" cut tag. Live scale notes computed for the reader's
  window: cycles-per-pixel and the bar's length in screen-widths (recomputed
  on resize). The blue bar is labeled **one reported peak core of six**;
  the caveat states cores are not multiplied into frequencies. Count-up:
  41,700 (AGC average instructions). Acceptance: displayed count = computed
  1e6/24 rounded to hundreds; screen-width count recomputes on resize.
- **S05 DENSITY (3 steps).** Spec cards: AGC 33.18 L / 31.8 kg / 1 processor /
  1.024 MHz; phone 111.5 mL / 233 g / 28 cores / 4.26 GHz reported; phone
  card labeled "shown enlarged". Core tiles = 6 + 6 + 16, staggered in.
  Verdict: "dense enough to disappear."
- **S06 RECONSTRUCTION (5 steps).** Rows assemble per step from the same
  glyph objects used in S01–S04 (phone silhouettes, wall mini-track with
  computed 94.5% blue bar, off-the-page clock-bar echo). Acceptance: row
  ratios equal the script-computed values.

Non-scene beats: hero (Act 0), rules (Act 1), two breathers (after size;
before closing), meaning prose (Act 5), static ledger table (Act 10),
dark closing with post links (Act 11), sources + method note.

## 5. Visual direction

Archival aerospace dossier: cream drafting paper `#f3efe4` / `#e9e4d3`,
ink hairlines, mono annotations, dimensioned orthographic SVGs whose user
units are centimetres, serif display (Iowan/Georgia stack), system mono for
every label/readout. Semantic palette: **international orange `#d64b1d` =
Apollo, cobalt `#23649f` = phone, ink `#171512` = ruler/unit**, stated as a
legend in Act 1 and held everywhere. Motion is restrained: cross-fades and
scales (600–900ms ease-out), live count-ups, one ambient cue animation;
reduced motion collapses everything to final states; nothing loops faster
than 3s; no canvas; ≤ ~4,600 generated DOM nodes.

## 6. Build handoff

- **Target:** replaces `blog/apollo-to-phone.html` in place (same slug,
  same canonical). Drafted as `blog/apollo-to-phone-v2.html` with
  `noindex, nofollow` until it ships; SEO block (canonical, OG/Twitter,
  BlogPosting JSON-LD, shared `og.png`) already present so shipping is a
  file move + robots flip + manifest title/deck update + sitemap already
  lists the URL.
- **Enhancement ladder:** semantic HTML → CSS states keyed off `data-step` →
  page-owned rAF scroll engine → rAF count-ups (reduced-motion guarded).
- **Dependencies:** only `../css/post-progress.css` + `../js/post-progress.js`
  with `data-vb-progress-*` on `<body>` (orange → ink → blue).
- **Verified in build:** node --check on both inline scripts;
  `scripts/check_posts.py` passes (draft noindex-exempt, but scene markup is
  checker-compatible: stages aria-hidden, steps 1…n with paragraph text);
  all ratios recomputed and cross-checked against prose.

## 7. Publishing handoff

| Field | Proposed value | Note |
| --- | --- | --- |
| Slug | `apollo-to-phone` | unchanged, permanent |
| Search title | Apollo in Your Pocket: AGC vs iPhone — Víctor Busqué | |
| H1 | Apollo, in your pocket. | |
| Meta description / deck | The Apollo Guidance Computer and your phone, measured scale by scale — size, mass, memory, time. Every ratio computed, none invented. Measured, not scored. | 155 chars |
| Topic / Tags | Computing · Space / Apollo, iPhone, Computing | unchanged |
| Canonical | https://engineering.victorbusque.com/blog/apollo-to-phone.html | unchanged |
| Date | 2026-08 | keep original publication month; bump dateModified |
| Internal links | prev gnss · next git-github-at-scale | unchanged neighbors |

## 8. Definition of ready

- [x] Central question, takeaway, scope, ending explicit.
- [x] Every readout has an E# or illustrative label; E10/E11 added and
      sourced; transistor/energy chapters explicitly excluded with rationale.
- [x] Each scene: job, state model, motion reason, fallback, mobile rule.
- [x] Aesthetic named; color semantics + chapter grammar defined.
- [x] Document outline, ladder, target, and verification plan stated.
- [x] Publishing fields drafted.
