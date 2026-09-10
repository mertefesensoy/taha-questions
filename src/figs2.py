# -*- coding: utf-8 -*-
"""Figures for the second solution document (problems 9-26)."""
import math
from figs import svg, line, node, text, poly_pts, INK, ACC, ACC2, GREY, FILL

GREEN = "#2e6b45"
GOLD  = "#b8860b"

def _lbl(p, s, size=11.5, col=INK, w=700):
    return text(p, s, size, col, style=f'font-weight="{w}"')

# ---------------------------------------------------------------- Problem 9
def fig_p9():
    b = []; w = 470
    for k, (cx, lab, hi) in enumerate([(120, "degree 0", 0), (330, "degree n&#8722;1", 4)]):
        pts = poly_pts(5, cx, 92, 58)
        if k == 1:
            for i in range(1, 5): b.append(line(pts[0], pts[i], ACC2, 1.8))
        for i, p in enumerate(pts):
            fill = "#f4d9d3" if i == hi else FILL
            b.append(node(p, 12, fill, INK, 1.6))
        b.append(text((cx, 176), lab, 11, ACC))
    b.append(text((235, 92), "vs.", 12, GREY, style='font-style="italic"'))
    b.append(text((235, 200), "one vertex isolated, another joined to everyone &#8212; including the isolated one", 10.5, ACC2))
    return svg(w, 214, "".join(b))

# ---------------------------------------------------------------- Problem 10
def fig_p10():
    b = []
    P = {'x': (110, 46), 'y': (250, 46), 'a': (40, 150), 'b': (120, 150), 'c': (200, 150), 'd': (290, 150)}
    for u in ('a', 'b', 'c', 'd'):
        b.append(line(P['x'], P[u], INK, 1.5)); b.append(line(P['y'], P[u], INK, 1.5))
    b.append(line(P['x'], P['y'], INK, 1.5))
    for k, p in P.items():
        hi = "#f4d9d3" if k == 'd' else ("#dbe6f0" if k in 'xy' else FILL)
        b.append(node(p, 15, hi, INK, 1.8)); b.append(_lbl(p, k, 12))
    for k, dgt in [('x', 5), ('y', 5), ('a', 2), ('b', 2), ('c', 2)]:
        dy = -25 if k in 'xy' else 27
        b.append(text((P[k][0], P[k][1] + dy), f"d = {dgt} &#10003;", 9.5, GREEN))
    b.append(text((P['d'][0] + 4, P['d'][1] + 27), "needs d = 4,", 9.5, ACC2))
    b.append(text((P['d'][0] + 4, P['d'][1] + 39), "but has only 2", 9.5, ACC2))
    b.append(text((165, 200), "a, b, c have used up their degree on x and y &#8212; d has no partner left", 10.5, GREY))
    return svg(350, 214, "".join(b))

# ---------------------------------------------------------------- Problem 12
def fig_p12():
    b = []
    P = [(50, 110), (130, 46), (210, 46), (290, 110), (210, 172), (130, 172)]
    tree = [(0, 1), (1, 2), (2, 3), (1, 5), (2, 4)]
    for k, (i, j) in enumerate(tree):
        b.append(line(P[i], P[j], INK, 1.9))
        mx, my = (P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2
        b.append(node((mx, my), 9, "#eef2f7", ACC, 1.2)); b.append(text((mx, my), str(k + 1), 9, ACC))
    b.append(line(P[0], P[5], ACC2, 2.0, "5 4"))
    mx, my = (P[0][0] + P[5][0]) / 2, (P[0][1] + P[5][1]) / 2
    b.append(node((mx - 6, my + 6), 9, "#f9ece8", ACC2, 1.2)); b.append(text((mx - 6, my + 6), "6", 9, ACC2))
    for p in P: b.append(node(p, 12, FILL, INK, 1.7))
    b.append(text((170, 210), "n = 6: five safe moves build a spanning tree; move 6 must close a cycle", 10.5, GREY))
    return svg(340, 224, "".join(b))

# ---------------------------------------------------------------- Problems 13 / 20
def fig_components(cap, big, small, w=430):
    b = []
    b.append(f'<ellipse cx="130" cy="88" rx="98" ry="58" fill="#eef2f7" stroke="{ACC}" stroke-width="1.4"/>')
    b.append(f'<ellipse cx="330" cy="88" rx="72" ry="48" fill="#faf1ec" stroke="{ACC2}" stroke-width="1.4"/>')
    b.append(text((130, 88), big, 11.5, ACC))
    b.append(text((330, 88), small, 11.5, ACC2))
    b.append(text((228, 172), cap, 10.5, GREY))
    return svg(w, 188, "".join(b))

# ---------------------------------------------------------------- Problem 15
def _small(pos, edges, cx, cy, s=1.0, lab=None, r=8):
    b = []
    P = [(cx + x * s, cy + y * s) for x, y in pos]
    for i, j in edges: b.append(line(P[i], P[j], INK, 1.6))
    for p in P: b.append(node(p, r, FILL, INK, 1.5))
    if lab: b.append(text((cx, cy + 52), lab, 10.5, ACC, style='font-style="italic"'))
    return "".join(b)

def fig_p15(which):
    """which in {'a','b','c'}"""
    if which == 'a':
        specs = [([(-34,-12),(0,-12),(34,-12),(-17,26),(17,26)], [(0,1),(1,2)], "P&#8323; &#8746; 2K&#8321;"),
                 ([(-34,-12),(0,-12),(34,-12),(-17,26),(17,26)], [(0,1),(3,4)], "2K&#8322; &#8746; K&#8321;")]
        w = 250
    elif which == 'c':
        specs = [([(-30,-14),(30,-14),(0,26),(-40,30),(40,30)], [(0,1),(0,2),(1,2)], "K&#8323; &#8746; 2K&#8321;"),
                 ([(-42,-10),(-14,-10),(14,-10),(42,-10),(0,30)], [(0,1),(1,2),(2,3)], "P&#8324; &#8746; K&#8321;"),
                 ([(-16,-18),(-48,20),(-16,20),(16,20),(52,2)], [(0,1),(0,2),(0,3)], "K&#8321;,&#8323; &#8746; K&#8321;"),
                 ([(-40,-12),(-12,-12),(16,-12),(-14,28),(28,28)], [(0,1),(1,2),(3,4)], "P&#8323; &#8746; K&#8322;")]
        w = 480
    else:
        specs = [(None, "K&#8325; &#8722; P&#8323;", [(0,1),(0,2)]), (None, "K&#8325; &#8722; 2K&#8322;", [(0,1),(2,3)])]
        b = []; w = 300
        for k, (_, lab, missing) in enumerate(specs):
            cx = 80 + k * 150; pts = poly_pts(5, cx, 78, 50)
            miss = {tuple(sorted(m)) for m in missing}
            for i in range(5):
                for j in range(i + 1, 5):
                    if (i, j) in miss:
                        b.append(line(pts[i], pts[j], "#d8b4a8", 1.4, "3 4"))
                    else:
                        b.append(line(pts[i], pts[j], INK, 1.6))
            for p in pts: b.append(node(p, 8, FILL, INK, 1.5))
            b.append(text((cx, 148), lab, 10.5, ACC, style='font-style="italic"'))
        b.append(text((w/2, 172), "dashed = the two removed edges", 10, GREY))
        return svg(w, 186, "".join(b))
    b = []
    step = w / len(specs)
    for k, (pos, edges, lab) in enumerate(specs):
        b.append(_small(pos, edges, step * (k + 0.5), 62, 1.0, lab))
    return svg(w, 132, "".join(b))

# ---------------------------------------------------------------- Problem 16
def fig_p16():
    b = []; 
    for k, (cx, edges, lab) in enumerate([
            (110, [(0,1),(1,2),(2,3),(3,4),(4,0)], "C&#8325;"),
            (300, [(0,2),(2,4),(4,1),(1,3),(3,0)], "its complement &#8212; again a 5-cycle")]):
        pts = poly_pts(5, cx, 82, 54)
        for i, j in edges: b.append(line(pts[i], pts[j], INK if k == 0 else ACC2, 1.8))
        for i, p in enumerate(pts):
            b.append(node(p, 11, FILL, INK, 1.6)); b.append(text(p, str(i), 10))
        b.append(text((cx, 158), lab, 10.5, ACC))
    return svg(430, 174, "".join(b))

# ---------------------------------------------------------------- Problem 24
def fig_p24():
    COL = {0: ACC2, 1: ACC, 2: GREEN}
    def panel(cx, classes, lab):
        b = []; pts = poly_pts(4, cx, 82, 52)
        for ci, cls in enumerate(classes):
            for i, j in cls: b.append(line(pts[i], pts[j], COL[ci], 2.6))
        for i, p in enumerate(pts):
            b.append(node(p, 11, FILL, INK, 1.6)); b.append(text(p, str(i), 10))
        b.append(text((cx, 160), lab, 10.5, ACC))
        return "".join(b)
    a = panel(110, [[(0,1),(2,3)], [(0,2),(1,3)], [(0,3),(1,2)]],
              "three perfect matchings (2K&#8322; each)")
    z = panel(340, [[(0,1),(1,2)], [(0,2),(2,3)], [(0,3),(1,3)]],
              "three paths (P&#8323; + K&#8321; each)")
    return svg(460, 176, a + z)

# ---------------------------------------------------------------- Problem 25
def fig_p25():
    b = []
    for k, cx in ((0, 110), (1, 320)):
        pts = poly_pts(6, cx, 88, 56)
        for i in range(6):
            for j in range(i + 1, 6): b.append(line(pts[i], pts[j], INK, 1.3))
        for p in pts: b.append(node(p, 9, FILL, INK, 1.5))
        b.append(text((cx, 168), "K&#8326;", 11.5, ACC, style='font-style="italic"'))
    b.append(text((215, 192), "12 people: everyone knows exactly 5, and any 3 contain 2 acquaintances", 10.5, GREY))
    return svg(430, 206, "".join(b))

# ---------------------------------------------------------------- Problem 26
def fig_p26_local():
    """the five local pictures around an interior corner point"""
    cases = [("no corner", 0, "one tile"), ("no corner", 0, "two tiles, split"),
             ("2 corners", 2, "T-junction"), ("4 corners", 4, "cross")]
    b = []; s = 34
    for k, (ttl, t, sub) in enumerate(cases):
        cx = 70 + k * 118; cy = 74
        b.append(f'<rect x="{cx-s}" y="{cy-s}" width="{2*s}" height="{2*s}" fill="#f7f9fb" stroke="{GREY}" stroke-width="1"/>')
        if k == 1:
            b.append(line((cx - s, cy), (cx + s, cy), INK, 2.0))
        elif k == 2:
            b.append(line((cx - s, cy), (cx + s, cy), INK, 2.0))
            b.append(line((cx, cy), (cx, cy + s), INK, 2.0))
        elif k == 3:
            b.append(line((cx - s, cy), (cx + s, cy), INK, 2.0))
            b.append(line((cx, cy - s), (cx, cy + s), INK, 2.0))
        b.append(node((cx, cy), 5.5, ACC2, ACC2, 1))
        b.append(text((cx, cy + s + 16), sub, 9.5, GREY))
        b.append(text((cx, cy + s + 30), f"t(p) = {t}", 10, ACC if t % 2 == 0 else ACC2,
                      style='font-weight="700"'))
    b.append(text((248, 158), "at an interior point t(p) is always even", 10.5, GREY))
    return svg(500, 172, "".join(b))

def fig_p26_frame():
    b = []; x0, y0, W, H = 60, 30, 230, 118
    b.append(f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="#f7f9fb" stroke="{INK}" stroke-width="1.8"/>')
    for (px, py, filled, lab) in [(x0, y0 + H, True, "(0, 0)"), (x0 + W, y0 + H, False, "(w, 0)"),
                                  (x0, y0, False, "(0, h)"), (x0 + W, y0, False, "(w, h)")]:
        b.append(node((px, py), 6, ACC2 if filled else FILL, ACC2 if filled else GREY, 1.6))
        dx = -30 if px == x0 else 30; dy = 16 if py == y0 + H else -12
        b.append(text((px + dx, py + dy), lab, 9.5, ACC2 if filled else GREY))
    b.append(text((x0 + W / 2, y0 + H / 2), "w &#8713; &#8484;,  h &#8713; &#8484;", 11, GREY, style='font-style="italic"'))
    b.append(text((x0 + W / 2, y0 + H + 42), "exactly one integral corner &#8212; an odd number", 10.5, ACC2))
    return svg(360, 204, "".join(b))

# ---------------------------------------------------------------- starred
def fig_star():
    COL = [ACC2, ACC, GREEN]
    n = 8; b = []; pts = poly_pts(n, 130, 100, 74)
    def ham(k):
        seq = [k]; lo = hi = k
        for t in range(1, n):
            if t % 2: hi = (hi + 1) % n; seq.append(hi)
            else:     lo = (lo - 1) % n; seq.append(lo)
        return seq
    for c in range(3):
        s = ham(c)
        for i in range(n - 1): b.append(line(pts[s[i]], pts[s[i+1]], COL[c], 2.0))
    for i, p in enumerate(pts):
        b.append(node(p, 10, FILL, INK, 1.5)); b.append(text(p, str(i), 9.5))
    b.append(text((130, 196), "n = 8 shown: three edge-disjoint spanning paths", 10.5, GREY))
    return svg(270, 212, "".join(b))
