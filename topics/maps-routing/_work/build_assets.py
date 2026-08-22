#!/usr/bin/env python3
"""Generate the static SVG strings and constants for the article from
graph_embed.json. Output: assets.json, consumed by compose_article.py."""
import json, math

g = json.load(open('graph_embed.json'))
X, Y, V, E, O, D = g['X'], g['Y'], g['V'], g['E'], g['O'], g['D']

def pt(p): return f"{X[p]} {Y[p]}"

def edge_path(e):
    u, v, l, flag, shape = e
    d = f"M{pt(shape[0])}"
    for p in shape[1:]:
        d += f"L{pt(p)}"
    return d

CLS = lambda f: (f >> 0) & 3 if False else ((f & 3) if False else None)
# class from speed index bits 0-2 → stroke class: arterial(0-3) / tertiary(4) / local(5-7)
def stroke_class(flag):
    si = flag & 7
    if si <= 3: return 'art'
    if si == 4: return 'ter'
    return 'loc'

paths = {'art': [], 'ter': [], 'loc': []}
for e in E:
    paths[stroke_class(e[3])].append(edge_path(e))
DEFS = {k: ''.join(v) for k, v in paths.items()}

# engine replicate for route/jam facts
SPEED = [50,40,50,40,40,30,20,30]
VMAX = 50/3.6
N = len(V)
G = [[] for _ in range(N)]
for i,(u,v,l,f,shape) in enumerate(E):
    t = l/(SPEED[f&7]/3.6)
    fwd = not (f & 16); bwd = not (f & 8)
    if fwd: G[u].append([v,l,t,i])
    if bwd: G[v].append([u,l,t,i])
hav = lambda a,b: math.hypot((X[V[b]]-X[V[a]])*0.8346,(Y[V[b]]-Y[V[a]])*1.1132)

def search(astar, mult=None):
    INF=float('inf'); dist=[INF]*N; prev=[-1]*N; done=[False]*N
    settled=[]; dist[O]=0
    hf=[]; hu=[]; hc=[]; c=0
    def push(f,u):
        nonlocal c
        hf.append(f); hu.append(u); hc.append(c); c+=1
        i=len(hf)-1
        while i>0:
            p=(i-1)>>1
            if hf[i]<hf[p] or (hf[i]==hf[p] and hc[i]<hc[p]):
                hf[i],hf[p]=hf[p],hf[i]; hu[i],hu[p]=hu[p],hu[i]; hc[i],hc[p]=hc[p],hc[i]; i=p
            else: break
    def pop():
        t=hu[0]; f=hf.pop(); u=hu.pop(); cc=hc.pop()
        if hf:
            hf[0]=f; hu[0]=u; hc[0]=cc; i=0
            while True:
                l=2*i+1; r=l+1; m=i
                if l<len(hf) and (hf[l]<hf[m] or (hf[l]==hf[m] and hc[l]<hc[m])): m=l
                if r<len(hf) and (hf[r]<hf[m] or (hf[r]==hf[m] and hc[r]<hc[m])): m=r
                if m==i: break
                hf[i],hf[m]=hf[m],hf[i]; hu[i],hu[m]=hu[m],hu[i]; hc[i],hc[m]=hc[m],hc[i]; i=m
        return t
    push(hav(O,D)/VMAX if astar else 0, O)
    while hf:
        u=pop()
        if done[u]: continue
        done[u]=True; settled.append(u)
        if u==D: break
        for v,l,t,i in G[u]:
            if done[v]: continue
            nd=dist[u]+t*(mult[i] if mult and i in mult else 1)
            if nd<dist[v]:
                dist[v]=nd; prev[v]=u
                push(nd+(hav(v,D)/VMAX if astar else 0), v)
    path=[]; x=D
    while x!=-1: path.append(x); x=prev[x]
    return settled, path, dist[D]

# street names for jam edges (Rosselló) — from graph.json order (same edge order)
g0 = json.load(open('graph.json'))
names = [e[4] for e in g0['E']]
JAM = [i for i,nm in enumerate(names) if nm == 'Carrer del Rosselló']

set_d, path_d, t_d = search(False)
set_a, path_a, t_a = search(True)
set_j, path_j, t_j = search(True, {i: 2.5 for i in JAM})

def route_chain(path):
    """vertex chain (dst→src) → forward edge index list"""
    edges=[]
    for a,b in zip(path[::-1], path[::-1][1:]):
        for v,l,t,i in G[a]:
            if v==b: edges.append(i); break
    return edges

edges_d = route_chain(path_d)
edges_j = route_chain(path_j)

def vertex_polyline(path):
    pts = [V[u] for u in path[::-1]]
    d = f"M{pt(pts[0])}"
    for p in pts[1:]: d += f"L{pt(p)}"
    return d

def edge_list_path(idxs):
    parts=[]
    for i in idxs:
        u,v,l,f,shape = E[i]
        d=f"M{pt(shape[0])}"
        for p in shape[1:]: d+=f"L{pt(p)}"
        parts.append(d)
    return ''.join(parts)

ROUTE = vertex_polyline(path_d)          # straight junction polyline (fallback)
ROUTE_EXACT = edge_list_path(edges_d)    # street-following, multiple subpaths
ROUTE_JAM = edge_list_path(edges_j)
ROSSELLO = edge_list_path(JAM)

len_d = sum(E[i][2] for i in edges_d)
len_j = sum(E[i][2] for i in edges_j)
art_d = sum(E[i][2] for i in edges_d if stroke_class(E[i][3])=='art')
ros_on_j = sum(E[i][2] for i in edges_j if i in JAM)
val_on_j = sum(E[i][2] for i in edges_j if names[i]=='Carrer de València')

# example edge for S01: the first edge of the route
ex_i = edges_d[0]
ex = E[ex_i]
ex_t = ex[2]/(SPEED[ex[3]&7]/3.6)
EX_EDGE = edge_path(E[ex_i])

# old route priced under the jam (chip: OLD ROUTE NOW · x MIN)
old_jam_min = sum(E[i][2]/(SPEED[E[i][3]&7]/3.6) * (2.5 if i in JAM else 1) for i in edges_d) / 60

def label_pt_for(name, idxs):
    for i in idxs:
        if names[i] == name:
            sh = E[i][4]
            p = sh[len(sh)//2]
            return [X[p], Y[p]]
    return [0, 0]

ROS_LAB = label_pt_for('Carrer del Rosselló', edges_d)
VAL_LAB = label_pt_for('Carrer de València', edges_j)

# scoped hierarchy (locals within 400 m of O/D)
def scoped(R_m):
    INF=float('inf'); dist=[INF]*N; prev=[-1]*N; done=[False]*N
    settled=[]
    near_o=[hav(O,i)<=R_m for i in range(N)]
    near_d=[hav(D,i)<=R_m for i in range(N)]
    dist[O]=0
    hf=[];hu=[];hc=[];c=0
    def push(f,u):
        nonlocal c
        hf.append(f);hu.append(u);hc.append(c);c+=1
        i=len(hf)-1
        while i>0:
            p=(i-1)>>1
            if hf[i]<hf[p] or (hf[i]==hf[p] and hc[i]<hc[p]):
                hf[i],hf[p]=hf[p],hf[i];hu[i],hu[p]=hu[p],hu[i];hc[i],hc[p]=hc[p],hc[i];i=p
            else: break
    def pop():
        t=hu[0];f=hf.pop();u=hu.pop();cc=hc.pop()
        if hf:
            hf[0]=f;hu[0]=u;hc[0]=cc;i=0
            while True:
                l=2*i+1;r=l+1;m=i
                if l<len(hf) and (hf[l]<hf[m] or (hf[l]==hf[m] and hc[l]<hc[m])): m=l
                if r<len(hf) and (hf[r]<hf[m] or (hf[r]==hf[m] and hc[r]<hc[m])): m=r
                if m==i: break
                hf[i],hf[m]=hf[m],hf[i];hu[i],hu[m]=hu[m],hu[i];hc[i],hc[m]=hc[m],hc[i];i=m
        return t
    push(0,O)
    while hf:
        u=pop()
        if done[u]:continue
        done[u]=True;settled.append(u)
        if u==D:break
        for v,l,t,i in G[u]:
            if done[v]:continue
            si=E[i][3]&7
            art = si<=3
            if not art and not near_o[v] and not near_d[v]:
                continue
            nd=dist[u]+t
            if nd<dist[v]:
                dist[v]=nd;prev[v]=u;push(nd,v)
    pth=[];x=D
    while x!=-1:pth.append(x);x=prev[x]
    return settled,pth,dist[D]

set_h, path_h, t_h = scoped(400)
assert abs(t_h - t_d) < 1e-9, (t_h, t_d)

# viewBoxes
xs=[x for x in X]; ys=[y for y in Y]
FULL = (min(xs)-40, min(ys)-40, max(xs)-min(xs)+80, max(ys)-min(ys)+80)
rpts=[V[u] for u in path_d]
CORR = (min(X[p] for p in rpts)-260, min(Y[p] for p in rpts)-260,
        max(X[p] for p in rpts)-min(X[p] for p in rpts)+520,
        max(Y[p] for p in rpts)-min(Y[p] for p in rpts)+520)
CORR_N = (CORR[0]+90, CORR[1]+90, CORR[2]-180, CORR[3]-180)

# label anchors
def mid_of(idxs):
    e = E[idxs[len(idxs)//2]]
    shape = e[4]
    p = shape[len(shape)//2]
    return X[p], Y[p]

# stroked dot paths — identical format to the page's dotsPath()
def dots_str(vertices):
    return ''.join('M%d %dl1 0' % (X[V[vi]], Y[V[vi]]) for vi in vertices)

all_v = list(range(N))
import math as _m
dj_s1 = set_d[:_m.ceil(.30*len(set_d))]
dj_s2 = set_d[len(dj_s1):_m.ceil(.70*len(set_d))]
dj_s3 = set_d[len(dj_s2):]
as_s1 = set_a[:_m.ceil(.35*len(set_a))]
as_s2 = set_a[len(as_s1):_m.ceil(.70*len(set_a))]
as_s3 = set_a[len(as_s2):]
set_j2, path_j2, t_j2 = search(True, {i: 2.5 for i in JAM})

assets = {
  'DEFS': DEFS,
  'ROUTE': ROUTE, 'ROUTE_EXACT': ROUTE_EXACT, 'ROUTE_JAM': ROUTE_JAM,
  'ROSSELLO': ROSSELLO, 'JAM': JAM,
  'DOTS': {
    'all': dots_str(all_v), 'dj_s1': dots_str(dj_s1), 'dj_s2': dots_str(dj_s2),
    'dj_s3': dots_str(dj_s3), 'dj_all': dots_str(set_d),
    'as_s1': dots_str(as_s1), 'as_s2': dots_str(as_s2), 'as_s3': dots_str(as_s3),
    'h_all': dots_str(set_h), 'j_all': dots_str(set_j2),
  },
  'O_pt': [X[V[O]], Y[V[O]]], 'D_pt': [X[V[D]], Y[V[D]]],
  'EX_EDGE': EX_EDGE, 'ROS_LAB': ROS_LAB, 'VAL_LAB': VAL_LAB,
  'FULL': [round(v) for v in FULL], 'CORR': [round(v) for v in CORR],
  'CORR_N': [round(v) for v in CORR_N],
  'facts': {
    'vertices': N, 'edges': len(E), 'arterial_edges': sum(1 for e in E if stroke_class(e[3])=='art'),
    'set_d': len(set_d), 'set_a': len(set_a), 'set_j': len(set_j), 'set_h': len(set_h),
    'len_d': round(len_d), 'len_j': round(len_j), 'art_share': round(art_d/len_d*100),
    't_d_min': round(t_d/60,2), 't_j_min': round(t_j/60,2),
    'straight': round(hav(O,D)),
    'ex_len': round(ex[2]), 'ex_t': round(ex_t,1),
    'ros_on_j': round(ros_on_j), 'val_on_j': round(val_on_j),
    'ros_on_d': round(sum(E[i][2] for i in edges_d if i in JAM)),
    'old_jam_min': round(old_jam_min, 1),
    'route_verts': len(path_d),
    'slice_d': [math.ceil(.30*len(set_d)), math.ceil(.70*len(set_d)), len(set_d)],
    'slice_a': [math.ceil(.35*len(set_a)), math.ceil(.70*len(set_a)), len(set_a)],
  },
}
json.dump(assets, open('assets.json','w'))
f = assets['facts']
print(json.dumps(f, indent=1))
print('defs sizes:', {k: len(v) for k,v in DEFS.items()})
print('route strings:', len(ROUTE_EXACT), len(ROUTE_JAM), len(ROSSELLO))
