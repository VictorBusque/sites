#!/usr/bin/env python3
"""Build the Eixample street graph from the Overpass extract and compute
the article's honest demo numbers. Everything the page shows at runtime is
recomputed there from the same embedded data; this script verifies the
values and picks the demo origin/destination."""
import json, math, heapq
from collections import defaultdict

LAT0, LON0, LAT1, LON1 = 41.387, 2.142, 41.404, 2.178
M_PER_DEG_LAT = 111132.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians((LAT0 + LAT1) / 2))

SPEED = {  # illustrative free-flow km/h by class (stated on the page)
    'primary': 50, 'primary_link': 40, 'secondary': 50, 'secondary_link': 40,
    'tertiary': 40, 'residential': 30, 'living_street': 20, 'unclassified': 30,
}
ARTERIAL = {'primary', 'primary_link', 'secondary', 'secondary_link'}
VMAX = max(SPEED.values()) * 1000.0 / 3600.0  # m/s, for the A* heuristic

data = json.load(open('eixample.json'))
ways = []
for el in data['elements']:
    if el['type'] != 'way' or 'geometry' not in el:
        continue
    hw = el['tags'].get('highway')
    if hw not in SPEED:
        continue
    ow = el['tags'].get('oneway')
    ways.append({
        'cls': hw,
        'name': el['tags'].get('name', ''),
        'oneway': (ow == 'yes'),
        'rev': (ow == '-1'),
        'pts': [(round(g['lat'], 5), round(g['lon'], 5)) for g in el['geometry']],
    })

# ── points, dedupe across ways ────────────────────────────────────────────
pid = {}
P = []          # (lat, lon)
def get_pid(lat, lon):
    k = (lat, lon)
    if k not in pid:
        pid[k] = len(P); P.append(k)
    return pid[k]

use_count = defaultdict(int)
endpoint_ids = set()
for w in ways:
    ids = [get_pid(*p) for p in w['pts']]
    w['ids'] = ids
    endpoint_ids.add(ids[0]); endpoint_ids.add(ids[-1])
    for i in ids:
        use_count[i] += 1

# junction = shared by >1 way occurrence OR an endpoint
junction = set()
for i, c in use_count.items():
    if c > 1 or i in endpoint_ids:
        junction.add(i)

# vertices
vid_of = {}
V = []         # vertex -> point id
for i in sorted(junction):
    vid_of[i] = len(V); V.append(i)

# ── edges between consecutive junction vertices along each way ────────────
E = []         # (u, v, length_m, arterial, shape=[pid,...])
def dist(a, b):
    la, lo = P[a]; lb, lob = P[b]
    return math.hypot((lb - la) * M_PER_DEG_LAT, (lob - lo) * M_PER_DEG_LON)

for w in ways:
    shape = [w['ids'][0]]
    acc = 0.0
    for a, b in zip(w['ids'], w['ids'][1:]):
        seg = dist(a, b)
        acc += seg
        shape.append(b)
        if b in junction:
            u, v = vid_of[shape[0]], vid_of[b]
            if u != v and acc > 0.5:
                E.append((u, v, acc, w['cls'] in ARTERIAL, list(shape),
                          w['oneway'] and not w['rev'],
                          (w['oneway'] and w['rev'])))
            shape = [b]; acc = 0.0
    # (way ends at a junction by construction of junction set)

# ── largest weakly connected component ────────────────────────────────────
adj = defaultdict(list)
for idx, (u, v, *_r) in enumerate(E):
    adj[u].append(idx); adj[v].append(idx)
seen = set(); best = set()
for s in range(len(V)):
    if s in seen:
        continue
    comp = {s}; stack = [s]; seen.add(s)
    while stack:
        x = stack.pop()
        for e in adj[x]:
            for y in (E[e][0], E[e][1]):
                if y not in seen:
                    seen.add(y); comp.add(y); stack.append(y)
    if len(comp) > len(best):
        best = comp
remap = {old: new for new, old in enumerate(sorted(best))}
V = [V[old] for old in sorted(best)]
E = [(remap[u], remap[v], l, a, sh, od, rv)
     for (u, v, l, a, sh, od, rv) in E if u in remap and v in remap]

# keep exact class: rebuild with class kept
E2 = []
for w in ways:
    shape = [w['ids'][0]]
    acc = 0.0
    for a, b in zip(w['ids'], w['ids'][1:]):
        acc += dist(a, b)
        shape.append(b)
        if b in junction:
            u, v = vid_of.get(shape[0]), vid_of[b]
            if u is not None and v is not None and u in remap and v in remap and acc > 0.5:
                E2.append((remap[u], remap[v], acc, w['cls'], w['name'],
                           list(shape), w['oneway'] and not w['rev'],
                           w['oneway'] and w['rev']))
            shape = [b]; acc = 0.0
E = E2

G = defaultdict(list)
GR = defaultdict(list)  # reverse, for nothing yet
for idx, (u, v, l, cls, name, sh, od, rv) in enumerate(E):
    s = SPEED[cls] * 1000.0 / 3600.0
    t = l / s
    art = cls in ARTERIAL
    if od:
        G[u].append((v, l, t, art, idx))
    elif rv:
        G[v].append((u, l, t, art, idx))
    else:
        G[u].append((v, l, t, art, idx))
        G[v].append((u, l, t, art, idx))

def haversine_m(a, b):
    (la1, lo1), (la2, lo2) = P[a], P[b]
    R = 6371000.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = p2 - p1; dl = math.radians(lo2 - lo1)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(x))

def dijkstra(src, dst, use_a_star=False):
    INF = float('inf')
    dist = [INF]*len(V); prev = [-1]*len(V)
    target = V[dst]
    h0 = haversine_m(V[src], target) / VMAX if use_a_star else 0.0
    dist[src] = 0.0
    pq = [(h0, 0.0, src)]
    settled = []
    done = [False]*len(V)
    while pq:
        f, d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True; dist[u] = d; settled.append(u)
        if u == dst:
            break
        for (v, l, t, art, eidx) in G[u]:
            if done[v]:
                continue
            nd = d + t
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u
                hf = haversine_m(V[v], target) / VMAX if use_a_star else 0.0
                heapq.heappush(pq, (nd + hf, nd, v))
    path = []
    x = dst
    while x != -1:
        path.append(x); x = prev[x]
    return settled, path, dist[dst]

def nearest_vertex(lat, lon):
    best, bi = 1e18, 0
    for i, pid_ in enumerate(V):
        la, lo = P[pid_]
        d = (la-lat)**2 + ((lo-lon) * 0.75)**2
        if d < best:
            best, bi = d, i
    return bi

# Demo origin/destination: SW corner area → NE corner area
O = nearest_vertex(41.3903, 2.1503)
D = nearest_vertex(41.4022, 2.1753)

set_d, path_d, t_d = dijkstra(O, D, False)
set_a, path_a, t_a = dijkstra(O, D, True)
assert path_d == list(reversed(path_a)) or path_d == path_a
assert abs(t_d - t_a) < 1e-9

route_len = 0.0; route_art = 0.0
for u, v in zip(path_d, path_d[1:]):   # path runs dst→src; real edges live in G[v] (u→v)
    for (w, l, t, art, eidx) in G[v]:
        if w == u:
            route_len += l; route_art += l if art else 0
            break

names = defaultdict(set)
for (u, v, l, cls, name, sh, od, rv) in E:
    names[u].add(name); names[v].add(name)

print(f"vertices={len(V)} edges={len(E)} (directed arcs={sum(len(v) for v in G.values())})")
print(f"arterial edges={sum(1 for e in E if e[3] in ARTERIAL)}")
print(f"O vertex {O}: {sorted(names[O])}")
print(f"D vertex {D}: {sorted(names[D])}")
print(f"Dijkstra settled={len(set_d)}  A* settled={len(set_a)}  ratio={len(set_d)/len(set_a):.1f}x")
print(f"route vertices={len(path_d)}  length={route_len:.0f} m  arterial share={route_art/route_len:.0%}")
print(f"route time={t_d/60:.1f} min")
haversine_OD = haversine_m(V[O], V[D])
print(f"straight-line O-D={haversine_OD:.0f} m")

# hierarchy experiment: local roads usable only within R of O/D
def scoped_dijkstra(src, dst, R_m):
    INF = float('inf')
    dist = [INF]*len(V); prev = [-1]*len(V)
    near_o = [haversine_m(V[O], p) <= R_m for p in V]
    near_d = [haversine_m(V[D], p) <= R_m for p in V]
    dist[src] = 0.0
    pq = [(0.0, src)]
    settled = []
    done = [False]*len(V)
    while pq:
        d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True; settled.append(u)
        if u == dst:
            break
        for (v, l, t, art, eidx) in G[u]:
            if done[v] or (not art and not near_o[v] and not near_d[v]):
                continue
            nd = d + t
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd, v))
    return settled, prev, dist[dst]

for R in (250, 400, 600):
    s2, prev2, t2 = scoped_dijkstra(O, D, R)
    print(f"hierarchy R={R}m: settled={len(s2)} time={'inf' if t2==float('inf') else '%.1fmin' % (t2/60)} reachable={t2 < 1e9}")

json.dump({'V': V, 'P': P, 'E': E, 'O': O, 'D': D,
           'stats': {'set_d': len(set_d), 'set_a': len(set_a),
                     'route_len': route_len, 'route_time': t_d,
                     'route_art': route_art, 'h_OD': haversine_OD}},
          open('graph.json', 'w'))
