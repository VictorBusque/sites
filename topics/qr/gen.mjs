// QR byte-mode encoder — build-time generator + test harness for the article.
// Implements ISO/IEC 18004 model-2 essentials: byte mode, versions 1-5,
// EC levels L/M/Q/H, Reed-Solomon over GF(2^8) (poly 0x11D), block
// interleaving, function patterns, zigzag placement, 8 masks + penalty
// election, BCH(15,5) format info.

// ── GF(256) ──────────────────────────────────────────────────────────
const EXP = new Uint8Array(512), LOG = new Uint8Array(256);
(function () {
  let x = 1;
  for (let i = 0; i < 255; i++) {
    EXP[i] = x; LOG[x] = i;
    x <<= 1;
    if (x & 0x100) x ^= 0x11d; // x^8 + x^4 + x^3 + x^2 + 1
  }
  for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
})();
const gmul = (a, b) => (a === 0 || b === 0) ? 0 : EXP[LOG[a] + LOG[b]];

function rsGenerator(degree) {
  let poly = [1];
  for (let i = 0; i < degree; i++) {
    const next = new Array(poly.length + 1).fill(0);
    for (let j = 0; j < poly.length; j++) {
      next[j] ^= gmul(poly[j], 1);          // × x^1 shift
      next[j + 1] ^= gmul(poly[j], EXP[i]); // × α^i
    }
    poly = next;
  }
  // poly is big-endian [1, ...coeffs]; remainder division uses it directly
  return poly;
}

function rsRemainder(data, degree) {
  const gen = rsGenerator(degree);
  const res = data.concat(new Array(degree).fill(0));
  for (let i = 0; i < data.length; i++) {
    const factor = res[i];
    if (factor === 0) continue;
    for (let j = 0; j < gen.length; j++) {
      res[i + j] ^= gmul(gen[j], factor);
    }
  }
  return res.slice(data.length);
}

// ── Block tables (Thonky / ISO): [ecPerBlock, [ [blocks, dataCw], ... ]] ──
const BLOCKS = {
  1: { L: [7, [[1, 19]]], M: [10, [[1, 16]]], Q: [13, [[1, 13]]], H: [17, [[1, 9]]] },
  2: { L: [10, [[1, 34]]], M: [16, [[1, 28]]], Q: [22, [[1, 22]]], H: [28, [[1, 16]]] },
  3: { L: [15, [[1, 55]]], M: [26, [[1, 44]]], Q: [18, [[2, 17]]], H: [22, [[2, 13]]] },
  4: { L: [20, [[1, 80]]], M: [18, [[2, 32]]], Q: [26, [[2, 24]]], H: [16, [[4, 9]]] },
  5: { L: [26, [[1, 108]]], M: [24, [[2, 43]]], Q: [18, [[2, 15], [2, 16]]], H: [22, [[2, 11], [2, 12]]] },
};
const ALIGN = { 1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30] };

function dataCodewords(v, lvl) {
  const [ec, groups] = BLOCKS[v][lvl];
  let n = 0; groups.forEach(([b, d]) => { n += b * d; });
  return n;
}

function pickVersion(byteCount, lvl) {
  for (let v = 1; v <= 5; v++) {
    const bits = 4 + 8 + byteCount * 8 + 4;
    if (bits <= dataCodewords(v, lvl) * 8) return v;
  }
  throw new Error('message too long for encoder (v1-5, ' + lvl + ')');
}

// ── Bitstream ─────────────────────────────────────────────────────────
function buildCodewords(text, v, lvl) {
  const bytes = Array.from(new TextEncoder().encode(text));
  const total = dataCodewords(v, lvl);
  const bits = [];
  const push = (val, n) => { for (let i = n - 1; i >= 0; i--) bits.push((val >> i) & 1); };
  push(0b0100, 4);                 // byte mode
  push(bytes.length, 8);           // count (v1-9)
  bytes.forEach(b => push(b, 8));
  const room = total * 8 - bits.length;
  if (room < 0) throw new Error('message does not fit: needs ' + (bits.length / 8) + ' codewords, capacity ' + total);
  const term = Math.min(4, room);
  push(0, term);                   // terminator
  while (bits.length % 8) bits.push(0);
  const data = [];
  for (let i = 0; i < bits.length; i += 8) {
    data.push(bits.slice(i, i + 8).reduce((a, b) => (a << 1) | b, 0));
  }
  let pad = 0xec;
  while (data.length < total) { data.push(pad); pad = pad === 0xec ? 0x11 : 0xec; }
  return data;
}

function interleave(data, v, lvl) {
  const [ecPer, groups] = BLOCKS[v][lvl];
  const blocks = [];
  let idx = 0;
  groups.forEach(([count, dLen]) => {
    for (let b = 0; b < count; b++) {
      const d = data.slice(idx, idx + dLen); idx += dLen;
      blocks.push({ data: d, ec: rsRemainder(d, ecPer) });
    }
  });
  const maxD = Math.max(...blocks.map(b => b.data.length));
  const out = [];
  for (let i = 0; i < maxD; i++) blocks.forEach(b => { if (i < b.data.length) out.push(b.data[i]); });
  for (let i = 0; i < ecPer; i++) blocks.forEach(b => out.push(b.ec[i]));
  return { blocks, final: out };
}

// ── Matrix ────────────────────────────────────────────────────────────
function baseMatrix(v) {
  const size = v * 4 + 17;
  const m = Array.from({ length: size }, () => new Array(size).fill(null)); // null = free
  const set = (r, c, val) => { m[r][c] = val; };
  // finder + separators
  const fp = (r0, c0) => {
    for (let r = -1; r <= 7; r++) for (let c = -1; c <= 7; c++) {
      const rr = r0 + r, cc = c0 + c;
      if (rr < 0 || cc < 0 || rr >= size || cc >= size) continue;
      const inSep = r === -1 || r === 7 || c === -1 || c === 7;
      const ring = Math.max(Math.abs(r - 3), Math.abs(c - 3)); // 3=border, 2=white ring, ≤1=center
      set(rr, cc, inSep ? 0 : (ring !== 2 ? 1 : 0));
    }
  };
  fp(0, 0); fp(0, size - 7); fp(size - 7, 0);
  // timing
  for (let i = 8; i < size - 8; i++) { set(6, i, i % 2 === 0 ? 1 : 0); set(i, 6, i % 2 === 0 ? 1 : 0); }
  // alignment
  const coords = ALIGN[v];
  for (const r of coords) for (const c of coords) {
    if (m[r][c] !== null) continue; // overlapping finder: skipped
    for (let dr = -2; dr <= 2; dr++) for (let dc = -2; dc <= 2; dc++) {
      set(r + dr, c + dc, Math.max(Math.abs(dr), Math.abs(dc)) !== 1 ? 1 : 0);
    }
  }
  // dark module
  set(size - 8, 8, 1);
  // reserve format areas
  const reserve = (r, c) => { if (m[r][c] === null) m[r][c] = 0; };
  for (let i = 0; i <= 8; i++) { if (i !== 6) { reserve(i, 8); reserve(8, i); } }
  for (let i = 0; i < 8; i++) { reserve(8, size - 1 - i); reserve(size - 1 - i, 8); }
  return m;
}

function placement(size) {
  const seq = [];
  let col = size - 1, up = true;
  while (col > 0) {
    if (col === 6) col--; // never cross vertical timing
    for (let i = 0; i < size; i++) {
      const r = up ? size - 1 - i : i;
      seq.push([r, col]); seq.push([r, col - 1]);
    }
    up = !up; col -= 2;
  }
  return seq;
}

function placeData(m, finalBits) {
  const size = m.length, seq = placement(size);
  const bits = [];
  finalBits.forEach(b => { for (let i = 7; i >= 0; i--) bits.push((b >> i) & 1); });
  const seatOf = new Map(); // "r,c" -> bit index (for damage mapping)
  let bi = 0;
  seq.forEach(([r, c]) => {
    if (m[r][c] !== null || bi >= bits.length) return;
    m[r][c] = bits[bi]; seatOf.set(r + ',' + c, bi); bi++;
  });
  return { m, bits, seatOf, seq };
}

const MASKS = [
  (r, c) => (r + c) % 2 === 0,
  (r) => r % 2 === 0,
  (r, c) => c % 3 === 0,
  (r, c) => (r + c) % 3 === 0,
  (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0,
  (r, c) => ((r * c) % 2) + ((r * c) % 3) === 0,
  (r, c) => (((r * c) % 2) + ((r * c) % 3)) % 2 === 0,
  (r, c) => (((r + c) % 2) + ((r * c) % 3)) % 2 === 0,
];

function isFunction(v, r, c) {
  const probe = baseMatrix(v);
  return probe[r][c] !== null || (r === 6) || (c === 6);
}

function applyMask(m, v, k, isFn) {
  const out = m.map(row => row.slice());
  const size = m.length;
  for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) {
    if (isFn(r, c) || out[r][c] === null) continue;
    if (MASKS[k](r, c)) out[r][c] ^= 1;
  }
  return out;
}

function penalty(m) {
  const size = m.length; let score = 0;
  // rule 1: runs ≥ 5
  for (let r = 0; r < size; r++) {
    let run = 1;
    for (let c = 1; c < size; c++) {
      if (m[r][c] === m[r][c - 1]) run++; else { if (run >= 5) score += 3 + run - 5; run = 1; }
    }
    if (run >= 5) score += 3 + run - 5;
  }
  for (let c = 0; c < size; c++) {
    let run = 1;
    for (let r = 1; r < size; r++) {
      if (m[r][c] === m[r - 1][c]) run++; else { if (run >= 5) score += 3 + run - 5; run = 1; }
    }
    if (run >= 5) score += 3 + run - 5;
  }
  // rule 2: 2×2 blocks
  for (let r = 0; r < size - 1; r++) for (let c = 0; c < size - 1; c++) {
    if (m[r][c] === m[r][c + 1] && m[r][c] === m[r + 1][c] && m[r][c] === m[r + 1][c + 1]) score += 3;
  }
  // rule 3: finder-like 1011101 with 4 light on a side
  const pat = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0];
  const patR = pat.slice().reverse();
  const match = (line, i) => pat.every((b, j) => line[i + j] === b) || patR.every((b, j) => line[i + j] === b);
  for (let r = 0; r < size; r++) for (let i = 0; i + 11 <= size; i++) {
    const line = m[r]; if (match(line, i)) score += 40;
  }
  for (let c = 0; c < size; c++) {
    const line = m.map(row => row[c]);
    for (let i = 0; i + 11 <= size; i++) if (match(line, i)) score += 40;
  }
  // rule 4: dark proportion
  let dark = 0; m.forEach(row => row.forEach(b => { if (b === 1) dark++; }));
  const pct = (dark * 100) / (size * size);
  score += Math.floor(Math.abs(pct - 50) / 5) * 10;
  return score;
}

function formatBits(lvl, mask) {
  const ecBits = { L: 0b01, M: 0b00, Q: 0b11, H: 0b10 }[lvl];
  let data = (ecBits << 3) | mask;
  let rem = data;
  for (let i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >> 9) * 0x537);
  const code = ((data << 10) | rem) ^ 0x5412;
  return code & 0x7fff;
}

function writeFormat(m, lvl, mask) {
  const size = m.length, bits = formatBits(lvl, mask);
  const get = i => (bits >> i) & 1;
  // copy 1: around top-left
  for (let i = 0; i <= 5; i++) m[i][8] = get(i);
  m[7][8] = get(6); m[8][8] = get(7); m[8][7] = get(8);
  for (let i = 9; i < 15; i++) m[8][14 - i] = get(i);
  // copy 2
  for (let i = 0; i < 8; i++) m[8][size - 1 - i] = get(i);
  for (let i = 8; i < 15; i++) m[size - 15 + i][8] = get(i);
  // dark module (re-assert)
  m[size - 8][8] = 1;
}

// ── Full encode ───────────────────────────────────────────────────────
function encode(text, lvl = 'L', forceV = null) {
  const bytes = Array.from(new TextEncoder().encode(text));
  const v = forceV || pickVersion(bytes.length, lvl);
  const data = buildCodewords(text, v, lvl);
  const { blocks, final } = interleave(data, v, lvl);
  const { m, bits, seatOf } = placeData(baseMatrix(v), final);
  const size = v * 4 + 17;
  const fnMap = [];
  const probe = baseMatrix(v);
  const isFn = (r, c) => probe[r][c] !== null;
  const candidates = MASKS.map((_, k) => penalty(applyMask(m, v, k, isFn)));
  let best = 0; candidates.forEach((s, k) => { if (s < candidates[best]) best = k; });
  const masked = applyMask(m, v, best, isFn);
  writeFormat(masked, lvl, best);
  return {
    text, version: v, lvl, size, data, blocks, final, candidates, mask: best,
    matrix: masked, unmasked: m, seatOf, bits,
    correctable: Math.floor(BLOCKS[v][lvl][0] / 2),
  };
}

// ── SVG ───────────────────────────────────────────────────────────────
function svg(matrix, { scale = 8, quiet = 4, light = '#fff', dark = '#0d0f14', pad = 0 } = {}) {
  const n = matrix.length, dim = (n + quiet * 2) * scale;
  let out = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${dim} ${dim}" role="img" aria-label="QR code">`;
  out += `<rect width="${dim}" height="${dim}" fill="${light}"/>`;
  let path = '';
  matrix.forEach((row, r) => row.forEach((b, c) => {
    if (b === 1) path += `M${(c + quiet) * scale + pad} ${(r + quiet) * scale + pad}h${scale - pad * 2}v${scale - pad * 2}h${-(scale - pad * 2)}z`;
  }));
  out += `<path fill="${dark}" d="${path}"/></svg>`;
  return out;
}

// ── Tests ─────────────────────────────────────────────────────────────
if (import.meta.url === `file://${process.argv[1]}`) {
  // 1) Published vector: "www.wikipedia.org" V1-L (Wikipedia, QR code article)
  const wiki = buildCodewords('www.wikipedia.org', 1, 'L');
  const expectData = [0x41, 0x17, 0x77, 0x77, 0x72, 0xE7, 0x76, 0x96, 0xB6, 0x97, 0x06, 0x56, 0x46, 0x96, 0x12, 0xE6, 0xF7, 0x26, 0x70];
  const expectEC = [0xAE, 0xAD, 0xEF, 0x06, 0x97, 0x8F, 0x25];
  const ec = rsRemainder(wiki, 7);
  const okD = wiki.length === expectData.length && wiki.every((b, i) => b === expectData[i]);
  const okE = ec.length === expectEC.length && ec.every((b, i) => b === expectEC[i]);
  console.log('wiki data codewords match:', okD);
  console.log('wiki EC codewords match:  ', okE);
  if (!okD || !okE) { console.log('got data:', wiki.map(x => x.toString(16)).join(' ')); console.log('got ec:  ', ec.map(x => x.toString(16)).join(' ')); process.exit(1); }

  // 2) HELLO WORLD V1-L — the article's worked example
  const hw = encode('HELLO WORLD', 'L', 1);
  console.log('\nHELLO WORLD · V1-L · size', hw.size);
  console.log('data cw:', hw.data.map(x => x.toString(16).padStart(2, '0')).join(' '));
  console.log('ec cw:  ', hw.blocks[0].ec.map(x => x.toString(16).padStart(2, '0')).join(' '));
  console.log('total cw:', hw.final.length, '· correctable:', hw.correctable);
  console.log('penalties:', hw.candidates.join(' / '), '→ mask', hw.mask);
  console.log('dark modules in result:', hw.matrix.flat().filter(Boolean).length, 'of', hw.size * hw.size);

  // 3) structural sanity: no null cells, all bits seated, format written twice
  const flat = hw.matrix.flat();
  console.log('no unresolved cells:', flat.every(b => b === 0 || b === 1));
  console.log('bits seated:', hw.bits.length, '(expect 208)');

  // 4) round-trip: unmask the winner and recover the codeword stream
  const seq = placement(hw.size);
  const probe2 = baseMatrix(1);
  const recovered = [];
  let cur = 0, nbits = 0;
  seq.forEach(([r, c]) => {
    if (probe2[r][c] !== null) return; // function/reserved cells hold no bits
    let bit = hw.matrix[r][c];
    if (MASKS[hw.mask](r, c)) bit ^= 1;
    cur = (cur << 1) | bit; nbits++;
    if (nbits === 8) { recovered.push(cur); cur = 0; nbits = 0; }
  });
  console.log('round-trip codewords equal:', recovered.length === hw.final.length && recovered.every((b, i) => b === hw.final[i]));

  // 5) other levels at V1 + multi-block V3-H, with RS syndrome zero-check.
  //    HELLO WORLD (11 bytes) does not fit V1-H (9 data cw) — it needs V2.
  ['L', 'M', 'Q'].forEach(l => {
    const e = encode('HELLO WORLD', l, 1);
    e.blocks.forEach(b => {
      const syn = rsRemainder(b.data.concat(b.ec), b.ec.length);
      if (syn.some(x => x !== 0)) throw new Error('RS syndrome nonzero for V1-' + l);
    });
    console.log(`V1-${l}: data ${e.data.length} · ec ${e.blocks[0].ec.length} · corrects ${e.correctable} · mask ${e.mask} · syndromes 0`);
  });
  const h7 = encode('HELLO W', 'H', 1);
  console.log(`V1-H (7 chars): data ${h7.data.length} · ec 17 · corrects ${h7.correctable} · mask ${h7.mask}`);
  const hwH = encode('HELLO WORLD', 'H', 2);
  console.log(`V2-H HELLO WORLD: data ${hwH.data.length} · ec 28 · corrects ${hwH.correctable} · size ${hwH.size}`);
  try {
    encode('HELLO WORLD', 'H', 1);
    console.log('V1-H overflow guard: UNEXPECTED SUCCESS (BUG)');
  } catch (err) {
    console.log('V1-H overflow guard: correctly rejects →', err.message);
  }

  // 6) URL code for the hero + static no-JS figures
  const fs = await import('fs');
  const url = 'https://engineering.victorbusque.com/blog/how-qr-codes-work.html';
  const hero = encode(url, 'L');
  console.log('\nhero URL payload:', url.length, 'bytes → V' + hero.version + '-' + hero.lvl, hero.size + '×' + hero.size, '· mask', hero.mask);
  fs.writeFileSync('/tmp/hero.svg', svg(hero.matrix, { scale: 10 }));
  console.log('hero svg → /tmp/hero.svg');

  // 7) static no-JS scene states
  fs.writeFileSync('/tmp/furniture.svg', svg(baseMatrix(1).map(r => r.map(c => c === null ? 0 : c)), { scale: 10, light: '#0d0f14', dark: '#e8e6df' }));
  const seatedM = (() => { const bm = baseMatrix(1); placeData(bm, hw.final); return bm.map(r => r.map(c => c === null ? 0 : c)); })();
  fs.writeFileSync('/tmp/seated.svg', svg(seatedM, { scale: 10, light: '#0d0f14', dark: '#e8e6df' }));
  console.log('static states → /tmp/furniture.svg, /tmp/seated.svg');
}
export { encode, buildCodewords, rsRemainder, baseMatrix, placement, placeData, applyMask, penalty, formatBits, svg, BLOCKS, dataCodewords, MASKS };
