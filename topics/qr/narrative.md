---
topic: "qr"
status: built
language: en
source_context: topics/qr/context.md
created: 2026-02-14
updated: 2026-02-15
intended_slug: how-qr-codes-work
---

# How a QR Code Works

> Build brief for one standalone scrollytelling article. Every number on the
> page is either an E# from `context.md` or computed live by the page's own
> byte-mode QR encoder (versions 1–5, all EC levels, verified against a
> published test vector before shipping).

## 1. Story contract

| Field | Decision |
| --- | --- |
| Reader and assumed knowledge | Tech-savvy: knows bits and bytes, scans QR codes weekly; no coding theory. |
| Central question | How does a square of black-and-white modules carry text, and why does it survive damage? |
| One-sentence answer | A QR code is a fixed choreography: fixed furniture patterns tell the camera where the grid is, your text becomes error-corrected codewords, they are laid down in a zigzag order, and a mask is XORed on top so the result never confuses the scanner. |
| Core takeaway | The square is not a picture — it is a small file with a header, error correction, and a chosen scrambling; every module has one job, decided before anything is drawn. |
| Why it matters | QR codes gate payments, menus, tickets, and logins; knowing the mechanism explains why they scan at odd angles, survive logos printed over them, and how much data can honestly fit. |
| Scope and exclusions | Standard square QR ("model 2", ISO/IEC 18004): byte mode only in the live encoder (other modes named), versions 1–5 encoded live, versions to 40 shown by formula. No decoder is simulated: damage verdicts are computed from error-correction capability, not claimed scans. Variants (Micro QR, rMQR, iQR) get one closing line. |
| Narrative point of view | Follow one thing: the message HELLO WORLD travels the whole pipeline — bits, codewords, insurance, placement, mask — and becomes a scannable square. |
| Reading language | English. |

### Reader journey

```text
Before: "A QR code is a random-looking picture of a link — the phone
somehow reads it."
Bridge:  The square is a choreography with named seats: finder, timing,
         alignment, format; the payload is codewords with insurance;
         the 'randomness' is a chosen, reversible mask.
After:   Module jobs (furniture vs data vs EC), zigzag placement, mask
         election by penalty score, and Reed–Solomon as the reason
         damage and logos don't kill the scan.
```

### Plain-language opening and ending

- **Opening promise:** "This square holds 26 codewords. By the end of the
  page you will know the job of every module in it — and you will watch
  the message HELLO WORLD become one, computed live as you scroll."
- **Ending:** "A QR code is a small machine for surviving being read badly:
  fixed patterns announce the grid, Reed–Solomon insures the payload, a
  zigzag order seats every bit, and a mask chosen by score keeps the noise
  looking like noise. The 1994 design was so spare it now gates payments
  from posters — and it still fits in 441 modules."

## 2. Evidence and editorial boundaries

| ID | Claim or datum that may appear | Type | Source | Caveat | Where used |
| --- | --- | --- | --- | --- | --- |
| E1 | 1994, Masahiro Hara's team, Denso Wave, to label car parts; replaced multiple barcodes per box | verified | context E1 | year precision only | history aside |
| E2 | QR = quick response | verified | context E2 | — | history |
| E3 | Go board influenced design; 1:1:3:1:1 chosen as least-used alternating sequence on printed matter | verified | context E3 | present as design rationale, not measured statistic | S01, history |
| E4 | Standardized AIM 1997 → JIS 1999 → ISO/IEC 18004 (current: 2024 edition) | verified | context E4 | — | history, footer |
| E5 | Versions 1–40; side = 4·V + 17 modules; 21×21 → 177×177 | verified | context E5 | — | versions ladder |
| E6 | Capacity 40-L: 7,089 numeric / 4,296 alnum / 2,953 byte / 1,817 kanji | verified | context E6 | — | capacity table |
| E7 | Modes: numeric 10 bits/3 digits, alnum 11 bits/2 chars, byte 8 bits/char, kanji 13; mode+count header; terminator 0000 | verified | context E7 | — | S02 |
| E8 | EC ≈ 7% (L), 15% (M), 25% (Q), 30% (H); exact = floor(EC cw/2) codeword errors per block | verified + inference | context E8–E9 | page shows "about" % and computes exact correctable count | S03, lab |
| E9 | V1 blocks: L 19+7, M 16+10, Q 13+13, H 9+17; V3-H two blocks 13+22; interleaving spreads local damage | verified | context E9, E11 | — | S03, lab |
| E10 | RS over GF(2^8), poly 0x11D; V1-L generator [1,127,122,154,164,11,68,117] | verified | context E10 | — | S03 |
| E12 | Padding alternates 0xEC, 0x11 | verified | context E12 | — | S02 |
| E13 | Function patterns: 7×7 finders 1:1:3:1:1 + separators, 5×5 alignment (V2+), timing row/col 6, dark module (8, 4V+9), format + version reserves | verified | context E13 | — | S01 |
| E14 | Quiet zone: 4 light modules around the symbol | verified | context E14 | — | S01, synthesis |
| E15 | 8 masks by formula; penalty rules (3/3/40/10 weights); lowest score wins | verified | context E15 | — | S05 |
| E16 | Format info: 5 bits + BCH(15,5), XOR 101010000010010, two copies | verified | context E16 | — | S05 |
| E17 | Placement: bottom-right, 2-wide zigzag columns, skip function patterns, never cross vertical timing | verified | context E17 | — | S04 |
| E18 | Patents held but not enforced for standardized codes; US 5726435 expired 2015-03-14; "QR Code" still a Denso Wave trademark | verified | context E18 | say "held but chose not to enforce", never "never patented" | synthesis |
| E19 | Reader locates 3 finders, normalizes with alignment patterns, then decodes with EC | verified | context E19 | — | S01 intro, synthesis |
| C1–C12 | Bitstream, codeword lists, EC bytes, penalty scores per mask, damaged-codeword verdicts, version ladder values | computed | page encoder (test-vector verified) | labeled "computed by the code on this page" | all scenes |

### Facts to preserve exactly

- 1:1:3:1:1 ratio wording; 7×7 finder, 5×5 alignment, 4-module quiet zone.
- V1-L arithmetic: 19 data + 7 EC = 26; corrects 2 codeword errors.
- HELLO WORLD byte-mode bitstream: 0100 00001011 + ASCII bytes + 0000 +
  pad EC/11 to 19 codewords (computed; must match encoder output live).

### Claims to avoid or qualify

- Never claim the page "decodes" or "scans" — the encoder is real, the
  damage lab computes EC capability, and any scan claim stays with the
  reader's own camera on the hero code.
- EC percentages are approximate; exact restorability is per-block.
- "Least-used sequence" is the design story, not a measured survey.

### Terminology

| Term | Reader-friendly definition | First use |
| --- | --- | --- |
| module | one square cell of the code; the smallest unit | Act 1 |
| function pattern | fixed furniture: finder, timing, alignment, format areas | Act 2 |
| codeword | one byte-sized group of 8 bits after packaging | Act 3 |
| error correction (EC) codeword | computed insurance bytes appended to data | Act 3 |
| mask | a fixed XOR pattern flipped on data modules to break confusing shapes | Act 5 |
| penalty score | the encoder's cost of a masked grid; lowest wins | Act 5 |

## 3. Narrative architecture

| Act | Reader question | Before → after | Beat | Anchor | Scroll / state | Evidence | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 Hook | What am I looking at? | a poster glyph → a scannable object made of modules | Hero: real QR (this page's URL, generated offline by the same encoder, inline SVG) + opening prose | the scannable square | load-in reveal; scan invitation | C1 | static hero, prose |
| 1 Mental model | What *is* the square? | picture → 21×21 grid, 441 modules, versions to 177 | Prose + versions ladder (computed from 4V+17) | the growing grids | reveal | E5, C2 | visible ladder |
| 2 Mechanism A | Where does the camera look first? | "it just finds it" → three finders + separators + timing + dark module = furniture | S01 sticky anatomy build | the furniture assembling | 5 steps: grid → finders+ratio → separators → timing → dark module + format reserve | E13, E3, E19 | stacked steps |
| 3 Mechanism B | How does text become the pattern? | "the dots are the text" → text → bits → codewords, most modules are not your text | S02 sticky bitstream | the bit ribbon | 5 steps: chars → ASCII bits → header → terminator → padding | E7, E12, C3 | stacked steps |
| breather | — | — | "Half the square was spent before your text arrived." | serif line | reveal | C4 | visible |
| 4 Mechanism C | What if it gets damaged? | "don't scratch it" → insurance codewords are computed and appended | S03 sticky RS | the 26 codeword wall | 5 steps: 19 data → division by generator → 7 EC chips → total 26 / corrects 3 → level trade-off table (L→H computed) | E8–E10, C5 | stacked steps |
| 5 Mechanism D | Where do the bits sit? | "somewhere in the middle" → a strict zigzag from bottom-right, skipping furniture | S04 sticky zigzag (signature) | the snaking codewords | 6 steps: start bottom-right → up the column → turn at top → skip furniture → never cross timing column → all 26 seated | E17, C6 | stacked steps |
| 6 Critical detail | Why does it look random? | "encrypted?" → no: a reversible mask, chosen by penalty election | S05 sticky mask election | the 8 candidates | 5 steps: confusing run unmasked → 8 candidates + computed scores → winner ringed → XOR flips highlighted → format bits (2 copies) | E15, E16, C7 | stacked steps |
| 7 Stress | How much can it survive? | "logos are magic" → computed EC budget | LAB interactive: slider damages codewords; EC-level picker L/M/Q/H | the inked square | continuous; verdict computed (block-aware), never a fake scan claim | E8, E9, E11, C8 | static example state |
| 8 Synthesis | The whole machine? | parts → one choreography | Hero code returns with labeled regions; capacity table (E6); history (E1–E4, E18) | the labeled square | reveal | E1–E6, E18 | visible |
| 9 Takeaway | What do I leave with? | — | Ending prose: the one-paragraph answer + scope note | — | reveal | — | visible |

Rhythm: quiet hero → dense S01 → dense S02 → breather → technical S03 →
signature S04 → dense S05 → playful lab → quiet synthesis.

## 4. Scene specifications

### Scene S01 — The furniture (sticky)

- **Narrative job:** replace "the phone just finds it" with fixed
  announcement patterns; half the square is not data.
- **Placement:** Act 2; follows the versions ladder prose; hands off to
  the bitstream.
- **Pattern:** sticky-scene, 5 steps.
- **Primary visual anchor:** a 21×21 module grid on a dark drafting stage;
  furniture layers assemble.
- **Analogy:** the square as a printed circuit board — fixed landings and
  traces before any chip is placed. Limit: the board doesn't route power,
  it announces position and timing; say so in one clause or cut.
- **On-page prose:** h2 "The furniture comes first". Steps: (1) empty grid,
  441 modules, quiet zone around it; (2) three finders click in, 7×7,
  1:1:3:1:1 in both axes — the ratio a scanner can find at any angle;
  (3) separators: one light module so finders don't bleed into data;
  (4) timing lines on row/column 6 alternate dark/light so any cut through
  the code yields a ruler; (5) dark module + the reserved format strip:
  the two settings every code must announce about itself.
- **Stage inventory:** SVG grid (modules as rects); layer groups
  `g.finder`, `g.sep`, `g.timing`, `g.dark`, `g.fmt`; mono labels and a
  ratio ruler overlay; readout chip (modules used by furniture — computed).
- **State model:**

  | Step | Stage state | Trigger | Visible evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | empty 21×21, dim grid dots | step 1 | "441 modules" | the raw canvas |
  | 2 | 3 finders drawn + ratio ruler | step 2 | "3 × 49 modules" | position/orientation |
  | 3 | separators light up | step 3 | outline ring | isolation |
  | 4 | timing row+col alternate | step 4 | ruler ticks | module clock |
  | 5 | dark module + format reserve | step 5 | reserved cells marked | self-description |
- **Motion choreography:** each layer fades/slides in on its step
  (600 ms, ease-out); ruler overlay pulses once (ambient). Reverse
  scroll removes layers in order.
- **Data / computation:** matrix function-pattern layer from the inlined
  encoder; furniture module count computed by counting set cells.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** stage `aria-hidden`; each step paragraph
  states its conclusion; no-JS: static SVG pre-rendered at build time with
  all furniture placed, followed by stacked steps.
- **Responsive rules:** at 390px the grid stays square, shrinks to ~min(88vw,
  stage height − card reserve); labels ≥ 8px; ruler hidden below 480px.
- **Acceptance check:** with JS off, the placed-furniture SVG is visible
  and every layer's count appears in step text.

### Scene S02 — Your text becomes bits (sticky)

- **Narrative job:** make the bitstream concrete; show header + payload +
  terminator + padding as one ribbon the reader can audit.
- **Placement:** Act 3; follows S01; hands off to RS insurance.
- **Pattern:** sticky-scene, 5 steps.
- **Primary visual anchor:** a horizontal bit ribbon (groups of 4/8),
  becoming codeword chips.
- **Analogy:** an envelope: mode+count is the address, data the letter,
  terminator the signature, padding the filler. Limit: an envelope's
  filler isn't standardized — this padding is; one clause.
- **On-page prose:** h2 "HELLO WORLD becomes 104 bits". Steps: (1) eleven
  characters; (2) each becomes its 8-bit ASCII byte (H = 48 hex shown);
  (3) a header goes in front: mode 0100 (byte) + 8-bit count
  00001011 = 11; (4) terminator 0000 closes the message; (5) the leftover
  room is filled with alternating 0xEC/0x11 until 19 codewords exactly.
- **Stage inventory:** bit ribbon of chips (0/1), segment braces labeled
  MODE / COUNT / DATA / TERM / PAD; a codeword rack below; live readout of
  bits and codewords.
- **State model:**

  | Step | Stage state | Trigger | Evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | 11 character tiles | step 1 | "11 chars" | the input |
  | 2 | tiles flip to 8-bit rows | step 2 | "H → 01001000" | text is numbers |
  | 3 | header chips prepend, brace labels | step 3 | "4 + 8 bits" | self-describing |
  | 4 | terminator chips | step 4 | "0000" | message end |
  | 5 | pad chips fill, rack = 19 cw | step 5 | "EC 11 EC 11 EC 11" | capacity exactly used |
- **Motion choreography:** chips flip (rotateX 300ms) as their step
  activates; braces draw in (scaleX); rack fills sequentially (staggered
  40ms); reverse un-fills.
- **Data / computation:** the page encoder builds the V1-L bitstream for
  "HELLO WORLD"; every displayed bit comes from it.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** step text contains the same values
  (0100, 00001011, H=01001000, EC/11 pads); no-JS shows the full ribbon
  as static markup (generated at build time).
- **Responsive rules:** ribbon wraps 4 rows at 390px; chips shrink to
  16px with 9px numerals; braces become row labels.
- **Acceptance check:** chip count per segment matches readout; 19
  codewords on the rack at step 5.

### Scene S03 — The insurance policy (sticky)

- **Narrative job:** demystify error correction as arithmetic you can
  watch: divide, keep the remainder, append it.
- **Placement:** Act 4; follows breather; hands off to placement.
- **Pattern:** sticky-scene, 5 steps.
- **Primary visual anchor:** 19 data codeword chips; 7 EC chips appear and
  dock behind them; a small division scratchpad.
- **Analogy:** a checksum with a repair kit. Limit: a checksum detects,
  Reed–Solomon repairs — say exactly that in one sentence, then drop the
  analogy.
- **On-page prose:** h2 "19 codewords buy 7 more". Steps: (1) 19 data
  codewords on the wall; (2) the encoder divides them, as one long
  number, by a fixed degree-7 generator over GF(2^8); (3) the remainder
  is 7 bytes — shown as computed chips; (4) 19 + 7 = 26: the full
  payload; this code can correct any 3 damaged codewords (floor(7/2));
  (5) the trade-off: L/M/Q/H computed from the block table (19/16/13/9
  data, 7/10/13/17 EC, corrects 3/5/6/8) — insurance costs capacity.
- **Stage inventory:** codeword wall (hex chips), generator strip
  [1,127,122,154,164,11,68,117] as a mono row, remainder dock, level
  trade-off mini-table, readout (data/EC/total).
- **State model:**

  | Step | Stage state | Trigger | Evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | 19 chips lit | step 1 | "19 DATA" | payload |
  | 2 | generator strip slides in, division ticks | step 2 | "÷ g(x), degree 7" | the machinery |
  | 3 | 7 EC chips emerge orange | step 3 | hex values | the remainder |
  | 4 | wall completes, lock badge | step 4 | "26 TOTAL · CORRECTS 2" | insured |
  | 5 | trade-off table L→H | step 5 | computed rows | cost of safety |
- **Motion choreography:** chips stagger in; EC chips glow orange on
  arrival; division ticks are ambient (a caret stepping along the
  strip); table rows count up once (C8 in prose too).
- **Data / computation:** RS remainder computed in-page by the encoder;
  trade-off table from E9 block data; "corrects N" = floor(EC/2).
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** all values in step prose + a static
  full-wall SVG in the no-JS document.
- **Responsive rules:** wall wraps to 2 rows; trade-off table keeps 4
  columns at 390px (numbers only); hex chips 24px min.
- **Acceptance check:** EC chips equal the encoder's remainder for the
  live bitstream; corrects-2 badge matches floor(7/2).

### Scene S04 — The zigzag (sticky, signature)

- **Narrative job:** seat every bit; show placement is a rule, not
  filler; the reader should be able to predict the next module.
- **Placement:** Act 5; follows S03; hands off to masking.
- **Pattern:** sticky-scene, 6 steps.
- **Primary visual anchor:** the 21×21 grid; codeword chips fly from a
  tray and land bottom-right→up in 2-wide zigzag columns.
- **Analogy:** none — the literal path is the clearest device.
- **On-page prose:** h2 "Every module has an assigned seat". Steps:
  (1) start at bottom-right, right-to-left pair of columns, moving up;
  (2) at the top, drop down and snake left; (3) furniture seats are
  skipped — bits wait for the next free module; (4) the vertical timing
  column is never crossed; (5) continue to the top-left; (6) all 208
  data bits seated (26 cw × 8) — readout computed.
- **Stage inventory:** the grid (now with furniture dim), a cursor
  chevron showing direction, landed modules in white/acid, a codeword
  tray counting down, path trace overlay.
- **State model:**

  | Step | Stage state | Trigger | Evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | first 2-wide column fills upward from bottom-right | step 1 | cursor ↑ | the rule |
  | 2 | column 2 snakes downward | step 2 | cursor ↓ | the turn |
  | 3 | a skip over the format reserve animates | step 3 | gap highlight | furniture wins |
  | 4 | timing column gap | step 4 | never crossed | one hard exception |
  | 5 | progress toward top-left, half seated | step 5 | "N / 208 bits" | it keeps its promise |
  | 6 | fully seated unmasked matrix | step 6 | "208 bits" | ready to mask |
- **Motion choreography:** modules land with a 120ms ease-out pop,
  staggered; cursor chevron eases between turns; path trace draws
  (stroke-dashoffset); step 6 settles to stillness (no loop).
- **Data / computation:** placement sequence from the encoder's zigzag
  iterator; bit values from the live codewords.
- **Interaction:** none beyond scroll.
- **Accessibility and fallback:** the placement rule and totals in step
  text; no-JS shows the fully seated static matrix (build-time SVG).
- **Responsive rules:** grid square, min(88vw, …); tray hides below
  480px (counts in readout instead); cursor 14px min.
- **Acceptance check:** landed modules count equals readout; skipping
  visibly avoids finder/format/timing cells.

### Scene S05 — The mask election (sticky)

- **Narrative job:** explain the apparent randomness and the format bits;
  the encoder tries all 8 and elects the cheapest.
- **Placement:** Act 6; follows S04; hands off to the lab.
- **Pattern:** sticky-scene, 5 steps.
- **Primary visual anchor:** a 3×3+1 rack of mini QRs (8 masked
  candidates), penalty score under each; the winner ringed in acid.
- **Analogy:** none; "election" is the frame.
- **On-page prose:** h2 "Eight masks, one election". Steps: (1) the
  unmasked code has a problem: long runs and finder-lookalikes confuse
  scanners (show the run highlighted); (2) a mask is a fixed formula —
  if (row+column) is even, flip that module; (3) there are 8 formulas;
  the encoder applies each and scores the grid by penalty rules (runs,
  2×2 blocks, finder-lookalikes, dark share); (4) the lowest score wins
  — computed scores shown; (5) the choice is announced in the format
  strip — 5 bits, BCH-protected, written twice, so the reader knows
  which mask to undo.
- **Stage inventory:** mini-QR rack (8 canvases/SVGs, masked grids),
  score chips, winner ring, a large detail view of the winning flip
  overlay (flips outlined), format strip zoom.
- **State model:**

  | Step | Stage state | Trigger | Evidence | Meaning |
  | --- | --- | --- | --- | --- |
  | 1 | unmasked grid, worst run highlighted orange | step 1 | run length | the problem |
  | 2 | mask 0 formula overlay animates on detail | step 2 | checkerboard | what a mask is |
  | 3 | all 8 candidates appear | step 3 | scores per candidate | the trial |
  | 4 | winner ringed, others dim | step 4 | lowest score | the election |
  | 5 | format strip zoom, 2 copies highlighted | step 5 | 15 bits ×2 | the announcement |
- **Motion choreography:** candidates flip in staggered; scores count up
  (400ms); ring draws around winner; flip overlay pulses once; format
  strip slides from the corner of a mini-QR.
- **Data / computation:** penalties from the encoder's scorer; winner =
  argmin; format bits from the BCH computation — all live.
- **Interaction:** none beyond scroll (hover on a candidate enlarges it —
  enhancement only).
- **Accessibility and fallback:** scores and winner named in step text;
  no-JS shows the winner static QR (build-time) + score table in prose.
- **Responsive rules:** rack becomes 4×2 then 2×4-scroll at 390px;
  scores ≥ 9px; detail view above rack.
- **Acceptance check:** the 8 scores are distinct values summing to a
  computed total; the winner matches the hero code's format bits.

### Scene LAB — The damage lab (interactive)

- **Narrative job:** stress the insurance; connect EC level → correctable
  codewords; honest verdicts only.
- **Placement:** Act 7; follows S05; hands off to synthesis.
- **Pattern:** full-width scene (not sticky). Controls: damage slider
  0–26 codewords (seeded positions, deterministic), EC-level picker
  L/M/Q/H (re-encodes HELLO WORLD at that level), a damage brush toggle.
- **Primary visual anchor:** the finished V1 code with orange ink blobs
  covering damaged modules; verdict chip.
- **On-page prose:** h2 "Break it (on paper)". Paragraphs: how to read
  the lab; the verdict is computed from which codewords were hit vs the
  per-block budget floor(EC/2) — this page encodes, it does not decode;
  your camera is the decoder.
- **State model:**

  | Control | Stage state | Evidence | Meaning |
  | --- | --- | --- | --- |
  | slider N | N codewords inked | "N / budget B codewords" | dose |
  | N ≤ B | verdict chip green: "within correction budget" | computed | survives |
  | N > B | verdict chip orange: "budget exceeded" | computed | fails |
  | level picker | matrix re-encodes; budget changes | data/EC counts | the trade-off, felt |
- **Motion choreography:** ink blobs pop (150ms); verdict chip flips
  color at the threshold; no ambient loops.
- **Data / computation:** encoder re-runs per level; damage maps to
  codeword indices via the placement map; verdict is block-aware
  (V1 is single-block; a footnote says larger codes interleave).
- **Interaction:** slider + picker + optional brush are keyboard
  operable (`<input type="range">`, radio group, button); all state also
  reachable without pointer.
- **Accessibility and fallback:** verdict and counts as live text
  (aria-live polite); no-JS shows a static annotated example (3 inked,
  "within budget") with the same numbers in prose.
- **Responsive rules:** controls full-width stacked at 390px; code
  square min(72vw, 320px); targets ≥ 40px.
- **Acceptance check:** at L with 3 damaged → within budget; at 4 →
  exceeded; at H the same 4 → within budget (budget 8).

## 5. Visual direction

### Chosen aesthetic

- **Named style / theme:** drafting-table spec sheet — the article reads
  like an engineer's blueprint for one QR code: dark blueprint stage,
  hairline grid, mono annotations, layer-colored modules.
- **Why this style fits:** the subject literally is a printed
  specification; callouts, ratio rulers, and layer keys map 1:1 to how
  the standard itself is drawn.
- **Emotional register:** calm, exact, quietly delighted.
- **Avoid:** QR-marketing gloss, scan-lines/"hacker" green CRT, danger
  colors on damage (ink orange is budget, not alarm), skeuomorphic
  paper textures, fake camera viewfinders.

### Design tokens and composition

| Concern | Direction |
| --- | --- |
| Background and surfaces | paper #f2f0e9 for prose; stage #0d0f14 with 32px hairline grid; cards paper with ink border |
| Palette semantics | blue = structure/furniture; paper-white = data; orange = EC/insurance and damage; acid = elected/active/verdict-ok. Never meaning by color alone — labels accompany every key |
| Typography | house roles: Unbounded display, Instrument Serif italic verdicts/numerals, Newsreader body, DM Mono labels/hex |
| Grid and spatial language | one module grid motif recurs: hero, stages, lab; braces and rulers annotate it |
| Shapes / illustration | modules are crisp squares, 1px gap at high zoom only; furniture drawn as layered outlines; no rounded QR modules |
| Annotation language | mono uppercase labels, hex bytes as chips, computed readouts prefixed with the computation ("PENALTY 312 · COMPUTED") |
| Motion character | mechanical clicks (chips flip, modules pop), one drawing motion per scene; nothing floats |

### Asset plan

| Asset | Purpose | Source / license | Inline representation | Alt / text equivalent |
| --- | --- | --- | --- | --- |
| hero QR SVG | scannable proof | generated by this project's encoder from the page URL | inline SVG, quiet zone included | "A QR code that opens this page" |
| stage grids | scene visuals | encoder output, drawn as SVG | inline/generated SVG | conclusions in step prose |
| no-JS static states | fallback | build-time renders | inline SVG | same values in prose |

No third-party assets. Fonts via the accepted Google Fonts stylesheet.

## 6. Build handoff

### Document outline

```text
<title>How a QR Code Works — Víctor Busqué</title>
main
  hero — h1 + dek + real scannable QR (inline SVG, URL payload)
  section 01 — The square is a grid (versions ladder, computed)
  sticky scene S01 — THE FURNITURE (5 steps)
  sticky scene S02 — THE BITSTREAM (5 steps)
  breather
  sticky scene S03 — THE INSURANCE (5 steps)
  sticky scene S04 — THE ZIGZAG (6 steps, signature)
  sticky scene S05 — THE MASK ELECTION (5 steps)
  lab scene — THE DAMAGE LAB (interactive)
  section — synthesis: labeled hero code, capacity table, history, license
  ending prose + scope note + sources
  post navigation (shared component)
```

### Implementation plan

- **Target:** `blog/how-qr-codes-work.html` (ships directly; no wip state).
- **Enhancement ladder:** semantic HTML + static build-time SVGs → CSS
  layer states keyed off `data-active-step` → inlined scaffold runtimes
  (steps, reveals, reduced-motion collapse) → small page script that
  computes encoder state and paints stage layers (no canvas needed;
  SVG DOM writes capped at V1's 441 modules).
- **State source of truth:** `data-active-step` per scene +
  `window.VBScene.onStep` reactions; lab state from its controls.
  The encoder is pure and deterministic; no scroll-linked continuous math.
- **Dependencies:** the two shared components
  (`../css|js/post-progress.*`, `../css|js/post-nav.*`) + Google Fonts;
  nothing else.
- **Performance budget / risks:** 5 sticky scenes × SVG layers — build
  layers once on init, toggle classes only (no per-scroll layout);
  penalty/mask computations are one-shot (<10 ms); no rAF loops except
  the cursor (runtime) — verify none added.
- **No-JS / reduced-motion plan:** every scene ships a build-time static
  SVG of its resolved state inline (decorative, aria-hidden) so the
  no-JS document shows the completed figures; steps stacked carry all
  conclusions; reduced motion collapses to the same document.
- **Mobile plan:** stages hug top, step cards bottom-dock (runtime);
  grids stay square ≥ 260px at 390px; racks reflow 2×4; all labels
  ≥ 9px; lab controls stacked, full-width.
- **Verification:** encoder unit-checked in Node against the published
  Wikipedia V1-L vector for "www.wikipedia.org" (data + EC codewords)
  before its output is embedded anywhere; run `node --check` on the
  inlined script body; run the site checker.
- **Open implementation questions:** none — brush damage is cut if it
  complicates keyboard parity (slider + picker are the contract).

## 7. Publishing handoff

| Field | Proposed value | Evidence / note |
| --- | --- | --- |
| Slug | `how-qr-codes-work` | permanent, lowercase |
| Search title | How a QR Code Works — Víctor Busqué | ≤60 chars |
| H1 / shelf title | 441 modules, 26 codewords, one square. | hero h1 |
| Meta description / deck | Watch HELLO WORLD become a real QR code: finder patterns, a bitstream, Reed–Solomon insurance, the zigzag, and the mask election — every number computed live in your browser. | 155 chars |
| Topic | Codes · Error correction | manifest label |
| Tags | QR codes, Reed–Solomon, Error correction, Barcode | manifest |
| Canonical | https://engineering.victorbusque.com/blog/how-qr-codes-work.html | site domain |
| Date | 2026-10 | publishing month |
| Manifest no | 11 | follows how-jpeg-works (10) |
| Internal links | post navigator (manifest-derived) + optional prose link to how-jpeg-works as sibling "computed live" article | — |

## 8. Definition of ready

- [x] The central question, takeaway, scope, and ending are explicit.
- [x] Every factual claim, number, and visual readout has an evidence ID or is
      labeled illustrative/computed.
- [x] Each scene has a narrative job, state model, motion reason, fallback,
      and mobile rule.
- [x] A named aesthetic is translated into usable visual decisions.
- [x] The document outline and implementation plan name the target file and
      enhancement strategy.
- [x] Publishing fields are drafted; the only unresolved item (brush control)
      has a documented cut line.
