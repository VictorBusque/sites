# QR codes — research context

Question: how does a QR code work — how does a square of black-and-white
modules carry a URL, survive damage, and get read in an instant? Gathered
2026-02. Scope: the standard square QR code ("model 2", ISO/IEC 18004) that
phones read, for a tech-savvous but non-expert reader. Micro QR, rMQR, iQR,
Frame QR, and SQRC variants are out of scope except as a closing aside.

## Verified facts

- **E1 — Origin.** Invented in 1994 by Masahiro Hara's team at Denso Wave
  (then a division of Denso Corporation, a Toyota supplier) to label
  automobile parts. It replaced multiple bar-code labels per box of parts
  with one symbol that consolidated kanji, kana, and alphanumeric data.
  Sources: Denso Wave "History of QR Code" (qrcode.com/en/history/),
  Wikipedia "QR code" (History), accessed 2026-02.
- **E2 — Name.** "QR" stands for quick response, expressing the development
  concept focused on high-speed reading. Source: Denso Wave, History of QR
  Code; Wikipedia.
- **E3 — Go board.** The initial design was influenced by the black and
  white counters on a Go board; the finder pattern's 1:1:3:1:1 ratio was
  chosen as the least-used sequence of alternating black-white areas on
  printed matter. Source: Wikipedia "QR code" (History, citing nippon.com
  interview and Denso Wave).
- **E4 — Standard.** First standardized by AIM International in October
  1997, then JIS X 0510 (January 1999), then ISO/IEC 18004:2000 (June 2000).
  Current edition ISO/IEC 18004:2024 (August 2024). Source: Wikipedia "QR
  code" (Standards), ISO catalog pages.
- **E5 — Grid geometry.** Versions 1–40; module count per side is
  4 × version + 17. Version 1 is 21×21; version 40 is 177×177. Sources:
  Wikipedia; Scandit QR symbology guide; hashitosystem.com spec overview.
- **E6 — Capacity.** Maximum storage at version 40, EC level L: numeric
  7,089 characters (3⅓ bits/char), alphanumeric 4,296 (5½ bits/char), byte
  2,953 (8 bits/char), kanji 1,817 (13 bits/char). Source: Wikipedia
  "Information capacity" table, citing Denso Wave "About 2D Code".
- **E7 — Encoding modes.** Mode indicator (4 bits): numeric 0001 (10 bits
  per 3 digits), alphanumeric 0010 (11 bits per 2 characters, value
  V = 45·C1 + C2 over a 45-character alphabet), byte 0100 (8 bits per
  byte), kanji 1000 (13 bits/char); 0000 terminates. Modes can be mixed
  within one symbol. Character-count indicator length depends on mode and
  version (byte mode: 8 bits for versions 1–9, 16 bits for 10–40).
  Source: Wikipedia "Encoding".
- **E8 — Error correction levels.** Reed–Solomon over GF(2^8). Approximate
  restoration capability: L ≈ 7%, M ≈ 15%, Q ≈ 25%, H ≈ 30% of codewords.
  Source: Wikipedia "Error correction" (table), Denso Wave QR Code
  Essentials.
- **E9 — Version 1 block structure.** V1-L is a single Reed–Solomon block:
  26 total codewords = 19 data + 7 error-correction, correcting up to 2
  byte errors — a (26,19,2) code. Full per-version block tables verified:
  V1: L 19/7, M 16/10, Q 13/13, H 9/17 (data/EC codewords, one block).
  V3-H: two blocks of (13 data + 22 EC). V40-L: 2956 data codewords in 25
  blocks, 30 EC per block. Sources: Thonky "Error correction code words
  and block information"; Wikipedia (V1 example, V3 interleaving example).
- **E10 — Finite field details.** GF(2^8) built on the primitive
  polynomial x^8 + x^4 + x^3 + x^2 + 1 (0x11D, decimal 285); generator
  polynomials ∏(x − α^i) with initial root α^0; the V1-L degree-7 generator
  has decimal coefficients [1, 127, 122, 154, 164, 11, 68, 117]. Source:
  Wikipedia "Error correction".
- **E11 — Interleaving.** In larger symbols the message is split into
  several Reed–Solomon blocks and interleaved, "making it less likely that
  localized damage to a QR symbol will overwhelm the capacity of any single
  block." Block size is chosen so no block corrects more than 15 errors.
  Source: Wikipedia "Error correction".
- **E12 — Padding.** After the terminator, remaining data capacity is
  filled by alternating pad codewords 0xEC and 0x11. Source: Thonky QR
  tutorial ("structure final message" step); also visible in Wikipedia's
  worked V1 example (EC/11 padding noted in decode walk-throughs).
- **E13 — Function patterns.** Finder patterns: three 7×7 concentric
  squares (1:1:3:1:1 ratio) at top-left, top-right, bottom-left, each
  surrounded by a 1-module light separator. Alignment patterns: 5×5
  (dark ring, light ring, dark center) from version 2 up, at coordinates
  from a version-dependent table, omitted where they would overlap finder
  patterns. Timing patterns: alternating dark/light lines on row 6 and
  column 6, always starting and ending dark. Dark module: always dark, at
  (row 8, column 4V+9). Format info: 15-bit strip reserved around the
  top-left and (split) top-right/bottom-left separators. Version info
  (versions 7+): 6×3 and 3×6 blocks near the top-right and bottom-left
  finders. Sources: Thonky "Module placement in matrix"; Wikipedia
  "Design"/structure figure.
- **E14 — Quiet zone.** A margin of light modules (4 modules wide per the
  specification) must surround the symbol. Source: Denso Wave "QR Code
  Essentials" (2011) — "quiet zone" of 4 modules; Wikipedia structure
  figure labels the quiet zone.
- **E15 — Masking.** After placement, data and EC modules are XORed with
  one of 8 mask patterns; the encoder computes a penalty score for each of
  the 8 masks (rule 1: runs of ≥5 same-color modules in row/column,
  3 + (run length − 5) points; rule 2: 2×2 blocks of same color, 3 points
  each; rule 3: finder-like 1:1:3:1:1 patterns with 4 light modules on a
  side, 40 points; rule 4: deviation of dark-module proportion from 50%,
  10 points per 5% step) and picks the lowest. Mask formulas (i = row,
  j = column): 0 (i+j)%2=0; 1 i%2=0; 2 j%3=0; 3 (i+j)%3=0; 4
  (⌊i/2⌋+⌊j/3⌋)%2=0; 5 (i·j)%2 + (i·j)%3 = 0; 6 ((i·j)%2 + (i·j)%3)%2 = 0;
  7 ((i+j)%2 + (i·j)%3)%2 = 0. Sources: Thonky "Data masking" and
  "Code words" penalty rules (N1=3, N2=3, N3=40, N4=10); Wikipedia
  "Format information and masking".
- **E16 — Format information.** 5 data bits (2 EC level + 3 mask id),
  protected by a (15,5) BCH code that corrects up to 3 bit errors, then
  XORed with the fixed pattern 101010000010010; two complete copies are
  placed in each symbol. EC-level indicator bits: L=01, M=00, Q=11, H=10.
  Sources: Wikipedia; Thonky "Format and version information".
- **E17 — Message placement.** Codeword bits are placed from the
  bottom-right corner upward in 2-module-wide zigzag columns, moving left,
  skipping function-pattern and reserved modules, never overlapping the
  vertical timing column. Source: Thonky "Module placement in matrix";
  Wikipedia "Message placement" (zigzag figure).
- **E18 — License.** Denso Wave owns QR patents but chose not to exercise
  them for standardized codes, to promote adoption. US patent 5726435
  expired March 14, 2015. "QR Code" remains a registered trademark of
  Denso Wave Incorporated. Source: Wikipedia "License" (citing qrcode.com
  patent pages).
- **E19 — Reading.** A 2D image sensor captures the code; the processor
  locates the three finder patterns, uses the smaller alignment pattern(s)
  to normalize size, orientation, and viewing angle, then converts modules
  to bits and validates with error correction. Source: Wikipedia "Design"
  (first paragraph).

## Per-version capacity (byte mode, verified against Thonky EC tables)

Data codewords (byte-mode data capacity is data codewords minus the mode +
count + terminator overhead of 2 codewords for versions 1–9):

| Version | Modules | L data cw | M data cw | Q data cw | H data cw |
| --- | --- | --- | --- | --- | --- |
| 1 | 21×21 | 19 | 16 | 13 | 9 |
| 2 | 25×25 | 34 | 28 | 22 | 16 |
| 3 | 29×29 | 55 | 44 | 34 (2 blocks) | 26 (2 blocks) |
| 4 | 33×33 | 80 | 64 (2 blocks) | 48 (2) | 36 (4) |
| 10 | 57×57 | 274 | 216 | 154 | 122 |
| 40 | 177×177 | 2,956 (25 blocks) | 2,334 | 1,666 | 1,276 |

Source: Thonky error-correction table (E9).

## Conflicts, estimates, and caveats

- EC percentages (7/15/25/30%) are the standard's *approximate* codeword
  restoration capability; exact capability depends on block structure
  (floor(EC cw / 2) errors per block). Present as "about", or compute the
  exact per-block correctable byte count in the page.
- "Denso Wave chose not to patent" vs "patented but waived rights": the
  accurate version is that patents were held but not enforced for
  standardized codes (E18). Avoid saying "never patented".
- The 1:1:3:1:1 "least-used sequence" claim is an origin story from Denso
  Wave interviews (E3); present as the design rationale, not as a measured
  statistic.
- Invention-date precision: "1994" is the announced release year (E1). Do
  not invent a month/day.

## Page-computable mechanics (illustrative label not needed — real outputs)

A byte-mode encoder for small versions is fully implementable in-page:
choose version and EC level, build the bitstream (mode 0100 + 8-bit count +
data + terminator 0000 + 0xEC/0x11 padding), generate Reed–Solomon EC bytes
over GF(2^8) with polynomial 0x11D, place bits in zigzag order, apply each
of the 8 masks, compute penalty scores, and render the winner. Every
readout (version, modules, data/EC codewords, mask penalty per mask,
correctable bytes) is computed, not hardcoded. Decoding is not simulated;
the article's final interactive can honestly offer the *encoded* matrix and
its parts, plus a "damage and re-encode" comparison rather than a decoder.

## Sources

- Denso Wave, "History of QR Code" — https://www.qrcode.com/en/history/
- Wikipedia, "QR code" (History, Design, Standards, Error correction,
  Encoding, License) — https://en.wikipedia.org/wiki/QR_code
- Thonky, "QR Code Tutorial" (error correction table, module placement,
  data masking, format/version information) —
  https://www.thonky.com/qr-code-tutorial/
- Scandit, "QR Code symbology guide" — https://www.scandit.com
- ISO/IEC 18004:2024 catalog entry — https://www.iso.org/standard/83389.html
