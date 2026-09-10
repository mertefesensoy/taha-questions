# -*- coding: utf-8 -*-
"""Inline-SVG figure generators for the graph-theory solution document."""
import math

INK   = "#1b1b1b"
ACC   = "#1f4e79"
ACC2  = "#a33a2a"
GREY  = "#8a8a8a"
FILL  = "#ffffff"

def svg(w, h, body, cls="fig"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">'
            f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>')

def line(p, q, col=INK, w=1.6, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    o = f' stroke-opacity="{op}"' if op != 1.0 else ''
    return (f'<line x1="{p[0]:.2f}" y1="{p[1]:.2f}" x2="{q[0]:.2f}" y2="{q[1]:.2f}" '
            f'stroke="{col}" stroke-width="{w}"{d}{o}/>')

def node(p, r=11, fill=FILL, col=INK, w=1.6):
    return f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r}" fill="{fill}" stroke="{col}" stroke-width="{w}"/>'

def text(p, s, size=12, col=INK, anchor="middle", style="", dy=0.36):
    return (f'<text x="{p[0]:.2f}" y="{p[1]+size*dy:.2f}" font-size="{size}" fill="{col}" '
            f'stroke="none" text-anchor="{anchor}" {style}>{s}</text>')

def poly_pts(n, cx, cy, r, start=-math.pi/2, clockwise=True):
    pts = []
    for i in range(n):
        a = start + (1 if clockwise else -1) * 2*math.pi*i/n
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return pts

# ---------------------------------------------------------------- Problem 1
BOARD_ADJ = [(1,6),(1,8),(2,7),(2,9),(3,4),(3,8),(4,9),(6,7)]

def fig_board():
    cs, ox, oy = 62, 26, 14
    b = []
    for r in range(3):
        for c in range(3):
            s = 3*r + c + 1
            x, y = ox + c*cs, oy + r*cs
            shade = "#eef2f7" if (r+c) % 2 == 0 else "#ffffff"
            b.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" fill="{shade}" stroke="{INK}" stroke-width="1.3"/>')
            b.append(text((x+cs-11, y+13), str(s), 10.5, GREY))
    ctr = lambda s: (ox + ((s-1) % 3)*cs + cs/2, oy + ((s-1)//3)*cs + cs/2)
    for a, z in BOARD_ADJ:
        b.append(line(ctr(a), ctr(z), ACC, 1.7))
    for s in range(1, 10):
        p = ctr(s)
        fill = "#f4d9d3" if s == 5 else FILL
        b.append(node(p, 13.5, fill, INK, 1.5))
        b.append(text(p, str(s), 12, INK, style='font-weight="600"'))
    return svg(2*ox + 3*cs, oy + 3*cs + 12, "".join(b))

CYC = [1,6,7,2,9,4,3,8]

def fig_cycle(labels=None, caption=None, w=300, corner_ring=True):
    cx, cy, r = w/2, 132, 92
    pts = poly_pts(8, cx, cy, r, start=-math.pi/2)
    b = []
    for i in range(8):
        b.append(line(pts[i], pts[(i+1) % 8], INK, 1.7))
    for i, s in enumerate(CYC):
        p = pts[i]
        corner = s in (1,3,7,9)
        if labels:
            col = labels.get(s)
            if col == 'W':
                b.append(node(p, 15, "#ffffff", INK, 2.2)); b.append(text(p, "W", 11.5, INK, style='font-weight="700"'))
            elif col == 'D':
                b.append(node(p, 15, "#33383d", INK, 2.2)); b.append(text(p, "D", 11.5, "#ffffff", style='font-weight="700"'))
            else:
                b.append(node(p, 9, "#ffffff", GREY, 1.4))
            b.append(text((cx + (r+27)*(p[0]-cx)/r, cy + (r+27)*(p[1]-cy)/r), str(s), 10.5, GREY))
        else:
            b.append(node(p, 14, "#dbe6f0" if corner else FILL, INK, 1.7))
            b.append(text(p, str(s), 12, INK, style='font-weight="600"'))
    if caption:
        b.append(text((cx, cy + r + 46), caption, 11, GREY))
    return svg(w, 292, "".join(b))

def fig_p1_pair():
    a = fig_cycle({1:'W',9:'W',3:'D',7:'D'}, "start: W&#8211;D&#8211;W&#8211;D (alternating)")
    z = fig_cycle({1:'W',7:'W',9:'D',3:'D'}, "target: W&#8211;W&#8211;D&#8211;D (not alternating)")
    return f'<div class="figrow">{a}{z}</div>'

# ---------------------------------------------------------------- Problem 2
def fig_p2():
    P = {'u6':(46,52),'u4':(126,52),'u1':(206,52),'u2':(160,132),'u3':(252,132),'u5':(206,206)}
    E = [('u6','u4'),('u4','u1'),('u1','u2'),('u1','u3'),('u2','u3'),('u2','u5'),('u3','u5')]
    deg = {'u1':3,'u2':3,'u3':3,'u4':2,'u5':2,'u6':1}
    b = [line(P[a], P[z]) for a, z in E]
    for k, p in P.items():
        b.append(node(p, 15, FILL, INK, 1.7))
        b.append(text(p, k[0] + '<tspan font-size="8.5" dy="2.5">' + k[1] + '</tspan>', 12, INK))
        offs = {'u6':(0,-26),'u4':(0,-26),'u1':(0,-26),'u2':(-36,-14),'u3':(38,-14),'u5':(0,30)}
        dx, dy = offs[k]
        b.append(text((p[0]+dx, p[1]+dy), f'd = {deg[k]}', 10, ACC2))
    return svg(322, 250, "".join(b))

# ---------------------------------------------------------------- Problem 3
def _cyc_at(cx, cy, r, n, lab=None, start=-math.pi/2):
    pts = poly_pts(n, cx, cy, r, start)
    b = []
    for i in range(n):
        b.append(line(pts[i], pts[(i+1) % n]))
    for p in pts:
        b.append(node(p, 8, FILL, INK, 1.6))
    if lab:
        b.append(text((cx, cy + 4), lab, 12.5, ACC, style='font-style="italic"'))
    return "".join(b)

def _path_at(x, y, n, gap=46, lab=None):
    b = []
    pts = [(x + i*gap, y) for i in range(n)]
    for i in range(n-1):
        b.append(line(pts[i], pts[i+1]))
    for p in pts:
        b.append(node(p, 8, FILL, INK, 1.6))
    if lab:
        b.append(text((x + (n-1)*gap/2, y + 30), lab, 12.5, ACC, style='font-style="italic"'))
    return "".join(b)

def fig_2regular():
    b = _cyc_at(72, 84, 46, 3, "C&#8323;") + _cyc_at(210, 84, 50, 4, "C&#8324;") + _cyc_at(360, 84, 54, 5, "C&#8325;")
    return svg(460, 172, b)

def fig_delta2():
    b = _cyc_at(70, 74, 40, 5, None) + text((70, 140), "C&#8325; (a cycle)", 12.5, ACC, style='font-style="italic"')
    b += _path_at(150, 60, 4, 44, "P&#8324; (a path)")
    b += _path_at(150, 128, 2, 44, "P&#8322;")
    b += node((330, 128), 8, FILL, INK, 1.6) + text((330, 158), "K&#8321;", 12.5, ACC, style='font-style="italic"')
    return svg(460, 178, b)

def fig_ray():
    b = []
    pts = [(46 + i*62, 52) for i in range(6)]
    for i in range(5):
        b.append(line(pts[i], pts[i+1]))
    b.append(line(pts[5], (pts[5][0]+34, 52), INK, 1.6, "3 5"))
    for i, p in enumerate(pts):
        b.append(node(p, 11, "#dbe6f0" if i == 0 else FILL, INK, 1.7))
        b.append(text(p, f'v<tspan font-size="8.5" dy="2.5">{i}</tspan>', 11.5))
    b.append(text((pts[5][0]+56, 56), "&#8943;", 15, INK))
    b.append(text((pts[0][0], 92), "degree 1 (odd)", 10.5, ACC2))
    b.append(text((pts[3][0], 92), "every other vertex has degree 2", 10.5, GREY))
    return svg(470, 108, "".join(b))

# ---------------------------------------------------------------- Problem 6
def circulant_edges(n, S):
    E = set()
    for i in range(n):
        for s in S:
            E.add(tuple(sorted((i, (i+s) % n))))
    return sorted(E)

def fig_circulant(S, title, w=260, placement=None, hl=None):
    n, r = 9, 92
    cx, cy = w/2, 118
    pos = poly_pts(n, cx, cy, r, start=-math.pi/2, clockwise=True)
    place = placement or (lambda v: v)
    P = {v: pos[place(v)] for v in range(n)}
    b = []
    for a, z in circulant_edges(n, S):
        d = min((z-a) % n, (a-z) % n)
        col = INK if not hl else (ACC2 if d in hl else INK)
        b.append(line(P[a], P[z], col, 1.55))
    for v in range(n):
        b.append(node(P[v], 12.5, FILL, INK, 1.7))
        b.append(text(P[v], str(v), 11.5, INK, style='font-weight="600"'))
    b.append(text((cx, cy + r + 44), title, 11.5, ACC))
    return svg(w, 272, "".join(b))

def fig_p6_three():
    a = fig_circulant((1,2), "G&#8321; = C&#8329;(1,2)")
    z = fig_circulant((1,3), "G&#8322; = C&#8329;(1,3)")
    c = fig_circulant((1,4), "G&#8323; = C&#8329;(1,4)")
    return f'<div class="figrow">{a}{z}{c}</div>'

def fig_p6_iso():
    inv = {(4*v) % 9: v for v in range(9)}
    a = fig_circulant((1,2), "G&#8321; drawn as usual", placement=lambda v: v)
    z = fig_circulant((1,2), "the same G&#8321;, vertex i placed at position 4i", placement=lambda v: (4*v) % 9)
    return f'<div class="figrow">{a}{z}</div>'

def fig_p6_triangles():
    def with_tri(S, tri, title):
        n, r, w = 9, 88, 250
        cx, cy = w/2, 114
        pos = poly_pts(n, cx, cy, r, start=-math.pi/2)
        b = []
        for a, z in circulant_edges(n, S):
            b.append(line(pos[a], pos[z], "#c9cdd2", 1.4))
        for t in tri:
            for i in range(3):
                b.append(line(pos[t[i]], pos[t[(i+1) % 3]], ACC2, 2.4))
        for v in range(n):
            b.append(node(pos[v], 11.5, FILL, INK, 1.5))
            b.append(text(pos[v], str(v), 11, INK))
        b.append(text((cx, cy + r + 42), title, 11.5, ACC))
        return svg(w, 264, "".join(b))
    t1 = [(0,1,2),(3,4,5),(6,7,8)]
    t2 = [(0,3,6),(1,4,7),(2,5,8)]
    a = with_tri((1,2), t1, "G&#8321;: 9 triangles (3 of them shown)")
    z = with_tri((1,3), t2, "G&#8322;: only 3 triangles &#8212; all shown")
    return f'<div class="figrow">{a}{z}</div>'

# ---------------------------------------------------------------- Problem 7
def fig_p7():
    b = []
    for k, cx in ((0, 108), (1, 300)):
        pts = poly_pts(4, cx, 100, 52, start=-math.pi/2)
        for i in range(4):
            for j in range(i+1, 4):
                b.append(line(pts[i], pts[j]))
        for p in pts:
            b.append(node(p, 11, FILL, INK, 1.7))
        b.append(text((cx, 178), "K&#8324;", 12.5, ACC, style='font-style="italic"'))
    return svg(410, 196, "".join(b))
