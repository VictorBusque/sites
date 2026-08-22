// Canonical verification engine — the exact code the page will inline.
// Binary heap, monotone insertion counter as tie-break, one speed table.
const g = require('./graph_embed.json');
const SPEED = [50, 40, 50, 40, 40, 30, 20, 30]; // km/h by speed index
const VMAX = 50 * 1000 / 3600;

const { X, Y, V, E, O, D } = g;
const N = V.length;
const G = Array.from({ length: N }, () => []);
E.forEach(([u, v, l, flag]) => {
  const t = l / (SPEED[flag & 7] * 1000 / 3600);
  const fwd = !(flag & 16), bwd = !(flag & 8), art = !!(flag & 32);
  if (fwd) G[u].push([v, l, t, art]);
  if (bwd) G[v].push([u, l, t, art]);
});
const hav = (a, b) => Math.hypot((X[V[b]] - X[V[a]]) * 0.8346, (Y[V[b]] - Y[V[a]]) * 1.1132);

function search(astar) {
  const dist = new Array(N).fill(Infinity);
  const prev = new Array(N).fill(-1);
  const done = new Array(N).fill(false);
  const settled = [];
  // binary heap of [f, counter, u]
  const hf = [], hc = [], hu = [];
  let ctr = 0;
  const push = (f, u) => { hf.push(f); hc.push(ctr++); hu.push(u); sift(hf.length - 1); };
  const less = (i, j) => hf[i] < hf[j] || (hf[i] === hf[j] && hc[i] < hc[j]);
  const sift = (i) => { while (i > 0) { const p = (i - 1) >> 1; if (less(i, p)) swap(i, p), i = p; else break; } };
  const swap = (i, j) => { [hf[i], hf[j]] = [hf[j], hf[i]]; [hc[i], hc[j]] = [hc[j], hc[i]]; [hu[i], hu[j]] = [hu[j], hu[i]]; };
  const pop = () => { const top = [hf[0], hc[0], hu[0]]; const lf = hf.pop(), lc = hc.pop(), lu = hu.pop();
    if (hf.length) { hf[0] = lf; hc[0] = lc; hu[0] = lu; let i = 0;
      for (;;) { const l = 2*i+1, r = l+1; let m = i;
        if (l < hf.length && less(l, m)) m = l;
        if (r < hf.length && less(r, m)) m = r;
        if (m === i) break; swap(i, m); i = m; } }
    return top; };
  dist[O] = 0;
  push(astar ? hav(O, D) / VMAX : 0, O);
  while (hf.length) {
    const [, , u] = pop();
    if (done[u]) continue;
    done[u] = true; settled.push(u);
    if (u === D) break;
    for (const [v, l, t] of G[u]) {
      if (done[v]) continue;
      const nd = dist[u] + t;
      if (nd < dist[v]) { dist[v] = nd; prev[v] = u; push(nd + (astar ? hav(v, D) / VMAX : 0), v); }
    }
  }
  const path = []; let x = D;
  while (x !== -1) { path.push(x); x = prev[x]; }
  return { settled, path, t: dist[D] };
}

const dj = search(false), as = search(true);
let len = 0, artLen = 0;
for (const [a, b] of dj.path.slice(1).map((p, i) => [p, dj.path[i]])) {
  const e = G[a].find(([w]) => w === b); len += e[1]; artLen += e[3] ? e[1] : 0;
}
console.log('dijkstra settled', dj.settled.length, '/', N);
console.log('astar settled', as.settled.length, '/', N);
console.log('route', len.toFixed(0), 'm', (dj.t / 60).toFixed(2), 'min verts', dj.path.length,
  'arterial', (artLen / len * 100).toFixed(0) + '%');
console.log('same path:', JSON.stringify(dj.path) === JSON.stringify(as.path));
console.log('straight-line', hav(O, D).toFixed(0), 'm');
