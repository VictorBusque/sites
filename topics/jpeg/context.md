# JPEG — research context

Question: how does JPEG turn a multi-megabyte photo into a few hundred
kilobytes? Gathered 2026-08. Scope: baseline sequential JPEG (the mode every
camera and browser writes and reads), for a tech-savvy but non-expert reader.

## Verified facts

- **E1 — Standardization.** The JPEG group was organized in 1986; the first
  JPEG standard was approved in September 1992 as ITU-T Recommendation T.81
  and published in 1994 as ISO/IEC 10918-1. Source: Wikipedia “JPEG” and
  “Joint Photographic Experts Group”; ITU T.81 cover page (“approved on 18th
  September 1992”, identical text published as ISO/IEC 10918-1),
  https://www.w3.org/Graphics/JPEG/itu-t81.pdf.
- **E2 — Typical ratio.** “JPEG typically achieves 10:1 compression with
  little perceptible loss in image quality.” Source: Wikipedia “JPEG” lead
  (mirrored by DBpedia/computer.fandom, 2026-08). Use as a *typical*, not
  guaranteed, figure; page readouts compute their own ratio live.
- **E3 — Chroma subsampling rationale.** Chroma subsampling encodes less
  resolution for chroma than for luma, “taking advantage of the human visual
  system’s lower acuity for color differences than for luminance.” 4:2:0 is
  the most common setting in JPEG and video. Source: Wikipedia “Chroma
  subsampling”, 2026-08.
- **E4 — 4:2:0 in JPEG.** JPEG uses 4:2:0 as part of its lossy mode (other
  options exist: 4:4:4, 4:2:2, 4:1:1). Source: Educative “What is Chroma
  Subsampling in JPEG?”, Wikipedia “Chroma subsampling”.
- **E5 — Quantization tables.** Annex K of T.81 gives example quantization
  tables (one luminance, one chrominance); libjpeg derives tables from a
  quality knob: quality < 50 → scale 5000/quality, else 200 − 2·quality,
  entries clamped to 1..255 for baseline. Sources: ITU T.81 Annex K;
  libjpeg jcparam.c (ijg/libjpeg-turbo), jpeg.org/jpeg.
- **E6 — Pipeline order (baseline sequential).** RGB → YCbCr color
  transform → chroma subsampling → 8×8 blocks → forward DCT per block →
  quantization → zigzag order → run-length + Huffman entropy coding → bit
  stream. DCT itself is lossless; quantization is the lossy step.
  Sources: T.81; Wikipedia “JPEG” (Discrete cosine transform section).
- **E7 — Where artifacts come from.** Coarse quantization causes blockiness
  (8×8 boundaries) and “mosquito noise” (ringing near sharp edges).
  Source: Wikipedia “Compression artifact”.
- **E8 — Successors.** Modern formats (WebP, HEIF, AVIF, JPEG XL) keep the
  same core idea — transform + quantize + entropy code — with better
  transforms/entropy coders. Source: jpeg.org, Wikipedia. Keep to one line.

## Numbers that must be computed, not asserted

The demo photo is procedurally generated in the reader’s browser
(deterministic, seeded). Every size, ratio, coefficient count, zero count,
and error metric shown on the page is computed from that photo at runtime:

- raw sample count = width × height × 3 bytes;
- bytes after 4:2:0 = width × height × 1.5;
- DCT coefficients, quantized survivors, zeros % (own DCT + E5 tables);
- encoded byte size via the browser’s own JPEG encoder
  (canvas toBlob('image/jpeg', q)) — label as measured, not standard-defined.

## Caveats

- Browser encoders choose their own chroma subsampling and tables; the lab
  must say “your browser’s encoder” rather than implying spec-mandated sizes.
- “Quality” numbers are not standardized across encoders; only the libjpeg
  table-scaling formula (E5) is presented as the classic mapping.
- Progressive JPEG, arithmetic coding, hierarchical mode: out of scope.
- The procedural photo is a synthetic photograph, not a camera sample; grain
  and glitter are added so compression behavior is photographic, but exact
  ratios are illustrative of this image only.
