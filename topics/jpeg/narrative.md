---
topic: "jpeg"
status: built
language: en
source_context: topics/jpeg/context.md
created: 2026-08-22
updated: 2026-08-22
intended_slug: how-jpeg-works
---

# How JPEG Compression Works

> Build brief for one standalone scrollytelling article. All numeric claims
> are either E# from context.md or computed live from the page's own
> procedural photo (768×576, seeded, deterministic).

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Tech-savvy (knows bytes, pixels, that lossy exists); no signal-processing background. |
| Central question | How does JPEG make a photo ~10× smaller with no visible damage? |
| One-sentence answer | JPEG converts each 8×8 block into weighted wave patterns, rounds the weights against what the eye notices (color detail and fine grain first), and stores the surviving small table of numbers with entropy coding. |
| Core takeaway | The file doesn't store pixels; it stores a prediction of what your eye will check — brightness structure first, coarse color second, fine grain last, and the knob is just how hard you round. |
| Why it matters | Every photo shared since 1992 passes through this bet; knowing it explains file sizes, quality sliders, artifacts, and when to pick PNG instead. |
| Scope and exclusions | Baseline sequential JPEG only (E6); no progressive/arithmetic modes; no patent history; successors one line (E8). |
| Narrative point of view | Inspect one machine: the reader watches one specific photo travel the pipeline, stage by stage, with numbers computed in front of them. |
| Reading language | English. |

### Reader journey

```text
Before: "JPEG compresses by making the picture smaller / lowering quality somehow."
Bridge:  The photo is numbers; vision has known blind spots; waves + rounding
         delete exactly what lives in those blind spots.
After:   Pixels → YCbCr → 4:2:0 → 8×8 DCT → quantize → entropy code; the
         quality dial is the rounding strength; artifacts are the rounding
         made visible.
```

### Plain-language opening and ending

- **Opening promise:** "One photograph, 1.3 MB of raw samples. By the end it
  will be a fraction of that — and you'll watch every cut happen, computed
  live in this page."
- **Ending:** "JPEG never stored your picture. It stored a forecast of your
  attention — brightness first, rough color second, fine grain last — rounded
  to whatever your quality setting allows. That is why a photo survives the
  cut, why text and logos don't, and why the dial works at all."

## 2. Evidence and editorial boundaries

| ID | Claim or datum that may appear | Type | Source | Caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | Group formed 1986; standard approved Sept 1992 (ITU-T T.81), ISO/IEC 10918-1 in 1994 | verified | context.md E1 | — | intro |
| E2 | "Typically ~10:1 with little perceptible loss" | verified | context.md E2 | typical, not guaranteed; page computes its own ratio | intro, synthesis |
| E3 | HVS lower acuity for chroma than luma | verified | context.md E3 | — | Act 2 |
| E4 | 4:2:0 is the common JPEG mode; keeps 1 chroma sample per 2×2 block | verified | context.md E3–E4 | "common", not mandatory | Act 2 |
| E5 | Annex K tables; libjpeg quality scaling (5000/q, 200−2q, clamp 1..255) | verified | context.md E5 | label "classic mapping" | Act 4, lab |
| E6 | Pipeline order; DCT lossless, quantization lossy | verified | context.md E6 | — | all acts |
| E7 | Blockiness and mosquito noise are quantization artifacts | verified | context.md E7 | — | lab |
| E8 | Successors keep transform+quantize+entropy-code core | verified | context.md E8 | one line | ending |
| C1–C9 | Raw bytes, 4:2:0 bytes, coefficients, zeros %, MSE, measured sizes, ratio | computed | page's own pipeline | labeled "computed/measured on this photo" | all readouts |

### Claims to avoid or qualify

- No claim that browser quality numbers equal libjpeg quality (say "your
  browser's encoder" for measured sizes).
- No invented camera photo stats; the demo image is synthetic and says so
  in the scope note.
- Avoid "destroys/destroys data" framing beyond what rounding does.

### Terminology

| Term | Definition | First use |
| --- | --- | --- |
| sample | one number: R, G, B or Y/Cb/Cr value 0–255 | Act 1 |
| luma (Y) | brightness plane | Act 2 |
| chroma (Cb, Cr) | two color-offset planes | Act 2 |
| 4:2:0 | one chroma sample kept per 2×2 luma block | Act 2 |
| DCT coefficient | weight of one fixed 8×8 cosine pattern | Act 3 |
| quantization | divide-by-table + round; the lossy step | Act 4 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Beat | Anchor | Scroll / state | Evidence | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 Hook | What am I looking at? | photo → photo is numbers | Hero + intro prose; the full photo, title, promise | the photo | load-in reveal; scroll hint | C1 | static hero + prose |
| 1 Mental model | What is a photo, to a computer? | "an image" → 442,368 dots × 3 numbers | S01 sticky zoom into samples | the pixel grid at 48× | 5 steps: grid → squares → RGB numbers → byte total → promise | C1 | stacked steps, numbers in prose |
| 2 Mechanism | What does the eye fail to see? | "all bits equal" → luma ≫ chroma; coarse ≫ fine | Prose (E3) + S02 sticky YCbCr/4:2:0 | the three planes | 5 steps: split → Y is the B&W photo → chroma is soft → keep ¼ → recombine | E3, E4, C2 | stacked steps |
| breather | — | — | "The eye forgives what it never measured." | serif line | reveal | — | visible |
| 3 Critical detail | How do blocks become weights? | pixels → 64 weights over fixed waves | S03 sticky DCT | the cosine dictionary + rebuild | 6 steps: grid → dictionary → frequency order → one block k=1 → k=15 → whole photo sweep | C3–C5 | stacked; k states in prose |
| 4 Change perspective | Where is the loss? | "DCT compresses" → rounding compresses | Prose + S04 sticky quantization | wall of zeros | 4 steps: coefficients → divide by table → zeros → reverse is lossy | E5, E6, C6 | stacked |
| 5 Stress | What does the dial do? | "quality is magic" → dial scales the table | LAB interactive: slider 5–100 | 3× crop pair + size | continuous control; measured toBlob size | E5, E7, C7 | static q=75 pair, sizes in prose |
| 5b Squeeze | Why do zeros shrink files? | zeros are wasted bits → runs + Huffman | S05 split scene: zigzag loop | zigzag walk | autoplay loop, pausable | E6, C8 | static final frame |
| 6 Synthesis | The whole machine? | stages remembered separately → one line | Prose + pipeline diagram + final comparison | before/after pair | reveal | C9 | visible |
| 7 Takeaway | What do I leave with? | — | Ending: forecast-of-attention callout, scope note, sources | the two photos | reveal | E2, E8 | visible |

Rhythm: quiet hero → dense S01 → quiet prose → reveal S02 → breather →
dense/technical S03 → quiet prose → technical S04 → playful lab → quiet S05 →
resolve.

## 4. Scene specifications

### Scene S01 — The raw truth (sticky)

- **Job:** replace "an image" with "a table of numbers".
- **Pattern:** sticky-scene, 5 steps. Stage: big canvas of the photo (or
  zoomed region) + mono readouts. All decorative (`aria-hidden`).
- **States:** 1 grid overlay at 1× ("768 × 576 dots"); 2 zoom 6×, grid
  visible; 3 zoom 48×, one sample enlarged with its real R,G,B values from a
  fixed, deterministic location; 4 readout "442,368 dots × 3 = 1,327,104
  bytes" (computed) with dots count-up; 5 dim photo + verdict line.
- **Data:** pixel values read from the generated ImageData at fixed coords;
  totals computed. Zoom rendering: nearest-neighbor drawImage with smoothing
  off.
- **Fallback:** steps stacked; numbers restated in step paragraphs.
- **390px:** canvas keeps 4:3, readouts above, card bottom-docked (runtime).

### Scene S02 — The color tax (sticky)

- **Job:** show the first real cut — chroma resolution — and that it's invisible.
- **Pattern:** sticky-scene, 5 steps. Stage: three plane panels (Y, Cb, Cr
  as false color) + main canvas.
- **States:** 1 all pixels → Y/Cb/Cr (three panels, computed); 2 Y panel
  alone emphasized ("the black-and-white photo is all here"); 3 chroma
  panels emphasized, shown enlarged/soft; 4 chroma decimated to 4:2:0
  (computed box average), readout "samples 1,327,104 → 663,552 (−50%)";
  5 recombined canvas + computed worst-pixel delta line.
- **Data:** own YCbCr conversion; 2×2 averaging; nearest upsample; max abs
  channel delta vs original computed.
- **Fallback:** conclusions in step text.
- **390px:** panels stack 2+1, keep labels ≥8px.

### Scene S03 — The dictionary of waves (sticky, signature moment)

- **Job:** teach DCT as a fixed dictionary of 64 wave patterns and that a
  block = weights; low frequencies carry the picture.
- **Pattern:** sticky-scene, 6 steps. Stage: cosine dictionary grid (64 real
  cos tiles, mint = in use), a zoomed real block pair (original | rebuilt),
  full-photo canvas for the final sweep.
- **States:** 1 grid overlay 8×8 on photo ("4,608 blocks"); 2 dictionary
  grid appears, DC tile marked; 3 a mid-frequency tile pulses, axis labels
  u→v ("rough → fine"); 4 real block rebuilt with k=1 (readout MSE,
  computed); 5 k=15; 6 full photo reconstruction with k sweeping 1→64
  scroll-linked within the step (incremental basis adds; fallback k=64 =
  original, identical by construction).
- **Data:** own DCT-II, precomputed 8×8 cos table; all 4,608 luminance
  blocks' coefficients precomputed once (Float32Array); reconstruction
  incremental.
- **Fallback:** stacked steps; the sweep rests at k=64.
- **390px:** dictionary grid 4×16 or scaled; block pair stacks.

### Scene S04 — The rounding (sticky)

- **Job:** locate the loss precisely: divide-by-table + round; zeros.
- **Pattern:** sticky-scene, 4 steps. Stage: 8×8 coefficient wall (the
  busiest luminance block, found by scan), quant table ghost, result wall.
- **States:** 1 coefficient values (signed, mono); 2 table appears over
  (Annex K luminance), division arrows; 3 quantized wall — zeros dimmed,
  survivors mint, readout "N of 64 survive; X.X% of the whole plane is now
  zeros (q=75)" computed; 4 reconstructed block vs original pair ("the
  missing waves don't come back smaller — they don't come back").
- **Data:** own DCT + E5 tables at q=75; zeros % over all luminance blocks.
- **Fallback:** stacked steps with the numbers in prose.

### Scene LAB — The quality dial (interactive)

- **Job:** stress the system; connect dial → table → artifacts → bytes.
- **Pattern:** full scene (not sticky). Slider 5–100 (default 75), keyboard
  accessible, labeled. Panels: original vs encoded 3× crop (nearest
  upscale), measured bytes + ratio (toBlob), table heat-map (E5 scaling),
  zeros %.
- **Data:** browser encoder for the file (labeled "measured — your
  browser's JPEG encoder"); own DCT for table/zeros stats.
- **Fallback:** renders q=75 on load; works without scroll. Reduced motion:
  no count-up animations, instant numbers.

### Scene S05 — The last squeeze (split, loop)

- **Job:** show why zeros are cheap: zigzag run-length + Huffman symbols.
- **Pattern:** split scene; left prose, right small canvas loop: quantized
  block from S04, zigzag cursor walks, zeros collapse into run tokens,
  symbol chips accumulate; byte tally ticks (computed symbol stream, not
  real file bytes — labeled).
- **Fallback:** static frame of the final symbol chips; conclusion in prose
  ("the measured sizes above already include this stage").

## 5. Visual direction

- **Aesthetic:** darkroom / light-table instrument. The article inspects a
  photograph in the dark: near-black surfaces, the photo as a luminous
  object, mono instrument labels, serif display for verdicts.
- **Tokens:** bg #0d0d0f, stage #0a0a0c + faint grid, ink #ece9e2, muted
  #98948b, mint #5fe0c0 = kept/present/active, coral #ff6b4a =
  discarded/loss/watch. Type roles unchanged from house (Unbounded display,
  Instrument Serif italics/numerals, Newsreader body, DM Mono labels).
- **Avoid:** red-vs-green danger coding, camera skeuomorphism, glossy
  gradients beyond the photo itself, any implication the visuals are camera
  samples.

## 6. Build handoff

- **Target:** ships directly at `blog/how-jpeg-works.html`.
- **Ladder:** semantic HTML → CSS (dark skin, states via
  `[data-active-step]`) → inlined scaffold runtimes (steps, reveals,
  reduced-motion collapse) → canvases with cached, deterministic renders;
  one scroll-linked k-sweep inside S03 step 6 with stable fallback.
- **State source of truth:** `data-active-step` (runtime) + named render
  functions per scene; lab state from slider input.
- **Dependencies:** only the two shared components
  (`../css|js/post-progress.*`, `../css|js/post-nav.*`) + Google Fonts.
- **Perf:** canvases render on activation (cached per state); loops pause
  offscreen via IntersectionObserver; DPR capped at 2; DCT work is
  one-shot at load (<150 ms).
- **No-JS/reduced motion:** full article text in DOM; stages collapse to
  stacked document; canvases render their settled states on load.
- **Mobile:** 4:3 canvases scale; step cards bottom-dock (runtime);
  dictionary grid scales; lab stacks vertically; slider full-width.
- **Open questions:** none.

## 7. Publishing handoff

| Field | Value |
| --- | --- |
| Slug | `how-jpeg-works` |
| Search title | How JPEG Compression Works — Víctor Busqué |
| H1 / shelf title | A photograph, mostly deleted. |
| Meta description / deck | Watch a photo become numbers, lose its color detail, dissolve into waves, and rebuild tiny — the real math of JPEG, computed live in your browser. |
| Topic | Media · Compression |
| Tags | JPEG, DCT, Compression, Images |
| Canonical | https://engineering.victorbusque.com/blog/how-jpeg-works.html |
| Date | 2026-09 |
| Manifest no | 10 |
