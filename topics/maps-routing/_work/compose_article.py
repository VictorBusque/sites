#!/usr/bin/env python3
"""Compose the final article by injecting generated assets into
article_src.html. The authored fallback values and the runtime-computed
values come from the same verified engine, so they agree by construction."""
import json

src = open('article_src.html', encoding='utf-8').read()
A = json.load(open('assets.json'))
G = json.load(open('graph_embed.json'))

# compact runtime dataset: no shapes (geometry lives in the static defs)
MAP = {
    'X': G['X'], 'Y': G['Y'], 'V': G['V'],
    'E': [[u, v, l, f] for (u, v, l, f, sh) in G['E']],
    'JAM': A['JAM'], 'O': G['O'], 'D': G['D'],
}

vb = lambda k: ' '.join(str(v) for v in A[k])
ox, oy = A['O_pt']; dx, dy = A['D_pt']
rlx, rly = A['ROS_LAB']; vx, vy = A['VAL_LAB']

rep = {
    '%%DEFS_LOC%%': A['DEFS']['loc'],
    '%%DEFS_TER%%': A['DEFS']['ter'],
    '%%DEFS_ART%%': A['DEFS']['art'],
    '%%MAP%%': json.dumps(MAP, separators=(',', ':')),
    '%%VB_FULL%%': vb('FULL'),
    '%%VB_CORR%%': vb('CORR'),
    '%%VB_CORR_N%%': vb('CORR_N'),
    '%%ROUTE%%': A['ROUTE_EXACT'],
    '%%ROUTE_JAM%%': A['ROUTE_JAM'],
    '%%ROSSELLO%%': A['ROSSELLO'],
    '%%EX_EDGE%%': A['EX_EDGE'],
    '%%DOTS_ALL%%': A['DOTS']['all'],
    '%%DJ_S1%%': A['DOTS']['dj_s1'],
    '%%DJ_S2%%': A['DOTS']['dj_s2'],
    '%%DJ_S3%%': A['DOTS']['dj_s3'],
    '%%DJ_ALL%%': A['DOTS']['dj_all'],
    '%%AS_S1%%': A['DOTS']['as_s1'],
    '%%AS_S2%%': A['DOTS']['as_s2'],
    '%%AS_S3%%': A['DOTS']['as_s3'],
    '%%H_ALL%%': A['DOTS']['h_all'],
    '%%J_ALL%%': A['DOTS']['j_all'],
    '%%OX%%': str(ox), '%%OY%%': str(oy),
    '%%DX%%': str(dx), '%%DY%%': str(dy),
    '%%OYB%%': str(oy + 40),      # origin label below the pin
    '%%DYT%%': str(dy - 24),      # target label above the pin
    '%%DXL%%': str(dx - 640),     # target label anchored left of the pin
    '%%ROSLX%%': str(rlx - 60), '%%ROSLY%%': str(rly - 28),
    '%%VALLX%%': str(vx - 80), '%%VALLY%%': str(vy + 56),
}
for k, v in rep.items():
    src = src.replace(k, v)

leftover = [t for t in rep if t in src]
assert not leftover, f'unreplaced tokens? (may just be repeated ok): {leftover}'
out = '/root/web/sites/blog/not-ready/how-google-maps-routes.html'
open(out, 'w', encoding='utf-8').write(src)
print('wrote', out, len(src), 'bytes')
