# -*- coding: utf-8 -*-
"""All data tables, generated from the same computations that verified the solutions."""
from itertools import combinations

def T(head, rows, cap=None, cls="", lc=(), hlrows=()):
    h = "".join('<th class="%s">%s</th>' % ("l" if i in lc else "", c) for i, c in enumerate(head))
    body = ""
    for k, r in enumerate(rows):
        tr = ' class="hl"' if k in hlrows else ''
        body += "<tr%s>%s</tr>" % (tr, "".join(
            '<td class="%s">%s</td>' % ("l" if i in lc else "", c) for i, c in enumerate(r)))
    c = '<p class="tcap">%s</p>' % cap if cap else ""
    return ('<div class="tblock"><table class="%s"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table>%s</div>') % (cls, h, body, c)

M = lambda s: '<span class="mono">%s</span>' % s

# ---------------------------------------------------------------- Problem 1
def t_knight():
    coord = {s: ((s-1)//3, (s-1) % 3) for s in range(1, 10)}
    adj = {s: sorted(b for b in range(1, 10) if b != s and
           sorted((abs(coord[s][0]-coord[b][0]), abs(coord[s][1]-coord[b][1]))) == [1, 2])
           for s in range(1, 10)}
    rows = []
    for s in range(1, 10):
        nb = ", ".join(map(str, adj[s])) if adj[s] else "&#8212; (none)"
        rows.append([f"<strong>{s}</strong>", f"({coord[s][0]}, {coord[s][1]})", nb, len(adj[s])])
    return T(["square", "(row, col)", "squares a knight can move to", "degree"], rows,
             "Table 1.1 &mdash; all knight moves on the 3&times;3 board. The centre square 5 is isolated; "
             "every other square has degree exactly 2.", lc=(2,), hlrows=(4,))

def t_p1target():
    rows = []
    for c1 in "WD":
        for c3 in "WD":
            c9 = "D" if c1 == "W" else "W"
            c7 = "D" if c3 == "W" else "W"
            read = [c1, c7, c9, c3]
            w = "".join(read)
            canon = max(w[i:] + w[:i] for i in range(4))   # W > D, so WWDD is the representative
            rows.append([c1, c3, c7, c9, "&#8201;".join(read), canon[0]+canon[1]+canon[2]+canon[3]])
    return T(["colour(1)", "colour(3)", "colour(7)", "colour(9)",
              "read round the cycle: 1, 7, 9, 3", "as a cyclic word"], rows,
             "Table 1.2 &mdash; the four corner positions in which diametrically opposite knights have "
             "different colours. All four give the same cyclic word WWDD.")

def t_p1bfs():
    rows = [
        ["placements of 4 knights on the 8 usable squares (2 white, 2 dark)", "420"],
        ["&#8230; of these, the ones whose colour pattern is W&#8201;D&#8201;W&#8201;D", "<strong>140</strong>"],
        ["positions actually reachable from the start by legal moves", "<strong>140</strong> &#8212; exactly the ones above"],
        ["reachable positions with all four knights on corners", "2"],
        ["&#8230; of these, positions with opposite corners of <em>different</em> colour", "<strong>0</strong>"],
        ["shortest solution of Guarini's puzzle (see remark)", "16 moves"],
    ]
    return T(["quantity", "value"], rows,
             "Table 1.3 &mdash; exhaustive breadth-first search over all positions. The colour pattern is not "
             "merely an obstruction, it is a complete invariant: every position with the right pattern is reachable.",
             cls="wide", lc=(0,), hlrows=(4,))

# ---------------------------------------------------------------- Problem 2
def t_hh():
    seq = [3, 3, 3, 2, 2, 1]
    rows, s, k = [], sorted(seq, reverse=True), 1
    while any(s):
        d = s[0]
        rest = s[1:]
        newrest = [rest[i] - 1 if i < d else rest[i] for i in range(len(rest))]
        act = (f"delete the leading {d}; subtract 1 from the next {d} entr"
               + ("y" if d == 1 else "ies"))
        rows.append([k, M("(" + ", ".join(map(str, s)) + ")"), act,
                     M("(" + ", ".join(map(str, sorted(newrest, reverse=True))) + ")")])
        s = sorted(newrest, reverse=True); k += 1
    rows.append([k, M("(" + ", ".join(map(str, s)) + ")"),
                 "all entries are 0 &#8212; realised by the edgeless graph", "<strong>graphical &#10003;</strong>"])
    return T(["round", "current sequence", "operation", "reduced sequence"], rows,
             "Table 2.1 &mdash; the Havel&ndash;Hakimi reduction of 3,&thinsp;3,&thinsp;3,&thinsp;2,&thinsp;2,&thinsp;1 "
             "terminates in the zero sequence, so the sequence is graphical.", cls="wide", lc=(2,))

def t_p2deg():
    E = [("u1","u2"),("u1","u3"),("u1","u4"),("u2","u3"),("u2","u5"),("u3","u5"),("u4","u6")]
    sub = lambda x: f'{x[0]}<sub>{x[1]}</sub>'
    rows = []
    for v in ["u1","u2","u3","u4","u5","u6"]:
        nb = sorted({a if b == v else b for a, b in E if v in (a, b)})
        rows.append([sub(v), ", ".join(sub(x) for x in nb), len(nb)])
    tot = sum(int(r[2]) for r in rows)
    rows.append(["<strong>total</strong>", "", f"<strong>{tot} = 2 &middot; 7 &#10003;</strong>"])
    return T(["vertex", "its neighbours in <em>G</em>*", "degree"], rows,
             "Table 2.2 &mdash; degrees in the constructed graph. Sorted, they read 1,&thinsp;2,&thinsp;2,&thinsp;"
             "3,&thinsp;3,&thinsp;3, and the degree sum 14 = 2&middot;7 confirms the edge count.",
             lc=(1,), hlrows=(6,))

def t_eg():
    d = sorted([1,2,2,3,3,3], reverse=True); n = len(d); rows = []
    for k in range(1, n+1):
        lhs = sum(d[:k]); rhs1 = k*(k-1); mins = [min(x, k) for x in d[k:]]
        rhs2 = sum(mins)
        ms = " + ".join(map(str, mins)) if mins else "0"
        rows.append([k, lhs, f"{rhs1} + ({ms}) = {rhs1+rhs2}", "&#10003;" if lhs <= rhs1+rhs2 else "&#10007;"])
    return T(["<em>k</em>", "&Sigma;<sub>i&le;k</sub> d<sub>i</sub>",
              "k(k&minus;1) + &Sigma;<sub>i&gt;k</sub> min(d<sub>i</sub>, k)", "holds?"], rows,
             "Table 2.3 &mdash; the six Erd&#337;s&ndash;Gallai inequalities for 3,&thinsp;3,&thinsp;3,&thinsp;2,"
             "&thinsp;2,&thinsp;1. All hold, independently confirming that the sequence is graphical.", lc=(2,))

# ---------------------------------------------------------------- Problem 6
def circ(S):
    E = set()
    for i in range(9):
        for s in S: E.add(tuple(sorted((i, (i+s) % 9))))
    return sorted(E)

def dist(i, j): return min((j-i) % 9, (i-j) % 9)

def t_p6id():
    rows = [
        ["first (left)", "<em>G</em><sub>1</sub>", "the nonagon + the 9 chords skipping one vertex",
         "{1, 2}", "<em>C</em><sub>9</sub>(1,&thinsp;2)"],
        ["second (middle)", "<em>G</em><sub>2</sub>", "the nonagon + the 9 chords skipping two vertices (three triangles)",
         "{1, 3}", "<em>C</em><sub>9</sub>(1,&thinsp;3)"],
        ["third (right)", "<em>G</em><sub>3</sub>", "the nonagon + the 9 long chords skipping three vertices",
         "{1, 4}", "<em>C</em><sub>9</sub>(1,&thinsp;4)"],
    ]
    return T(["drawing", "name", "what the picture shows", "circular distances", "graph"], rows,
             "Table 6.1 &mdash; identifying the three drawings as circulant graphs on ℤ<sub>9</sub>.",
             cls="wide", lc=(2,))

def t_p6edges():
    rows = []
    for name, S in [("<em>G</em><sub>1</sub>", (1,2)), ("<em>G</em><sub>2</sub>", (1,3)), ("<em>G</em><sub>3</sub>", (1,4))]:
        E = circ(S)
        a = [f"{i}{j}" for i, j in E if dist(i, j) == 1]
        b = [f"{i}{j}" for i, j in E if dist(i, j) != 1]
        rows.append([name, M(" ".join(a)), M(" ".join(b)), len(E)])
    return T(["graph", "the 9 edges of distance 1 (the nonagon)", "the 9 chords", "|<em>E</em>|"], rows,
             "Table 6.2 &mdash; complete edge lists; the pair <span class='mono'>ij</span> denotes the edge "
             "{i,&thinsp;j}. Each graph has 18 edges, so each is 4-regular.", cls="wide", lc=(1, 2))

def t_p6inv():
    def tri(E):
        Es = set(E)
        return [c for c in combinations(range(9), 3)
                if all(tuple(sorted(p)) in Es for p in combinations(c, 2))]
    def c4(E):
        Es = set(E); cnt = 0
        for q in combinations(range(9), 4):
            for perm in [(0,1,2,3),(0,1,3,2),(0,2,1,3)]:
                cy = [q[i] for i in perm]
                if all(tuple(sorted((cy[i], cy[(i+1) % 4]))) in Es for i in range(4)): cnt += 1
        return cnt
    rows = []
    for name, S in [("<em>G</em><sub>1</sub> = <em>C</em><sub>9</sub>(1,2)", (1,2)),
                    ("<em>G</em><sub>2</sub> = <em>C</em><sub>9</sub>(1,3)", (1,3)),
                    ("<em>G</em><sub>3</sub> = <em>C</em><sub>9</sub>(1,4)", (1,4))]:
        E = circ(S)
        rows.append([name, 9, len(E), "4-regular", "yes", 3,
                     f"<strong>{len(tri(E))}</strong>", f"<strong>{c4(E)}</strong>"])
    return T(["graph", "|V|", "|E|", "degrees", "connected", "girth", "triangles", "4-cycles"], rows,
             "Table 6.3 &mdash; the first six invariants agree for all three graphs; the triangle count "
             "(and the 4-cycle count) is what finally separates G<sub>2</sub> from the other two.",
             cls="wide", lc=(0,), hlrows=(1,))

def t_p6map():
    rows = [["<em>i</em>"] + [str(i) for i in range(9)],
            ["&phi;(<em>i</em>) = 4<em>i</em> mod 9"] + [f"<strong>{(4*i) % 9}</strong>" for i in range(9)],
            ["&phi;<sup>&minus;1</sup>(<em>i</em>) = 7<em>i</em> mod 9"] + [str((7*i) % 9) for i in range(9)]]
    h = ["", "", "", "", "", "", "", "", "", ""]
    body = "".join("<tr>" + "".join(f'<td class="{"l" if k == 0 else ""}">{c}</td>' for k, c in enumerate(r)) + "</tr>"
                   for r in rows)
    return ('<div class="tblock"><table class="wide rule-top"><tbody>%s</tbody></table>'
            '<p class="tcap">Table 6.4 &mdash; the isomorphism &phi; and its inverse, as permutations of '
            'ℤ<sub>9</sub>. Note &phi; fixes 0, 3 and 6.</p></div>') % body

def t_p6edgemap():
    E = circ((1, 2)); E3 = set(circ((1, 4)))
    f = lambda i: (4*i) % 9
    recs = []
    for i, j in E:
        a, b = sorted((f(i), f(j)))
        recs.append((f"{{{i},{j}}}", dist(i, j), f"{{{a},{b}}}", dist(a, b), (a, b) in E3))
    half = 9
    rows = []
    for k in range(half):
        l, r = recs[k], recs[k+half]
        rows.append([M(l[0]), l[1], "&rarr;", M(l[2]), l[3], "&#10003;" if l[4] else "&#10007;",
                     M(r[0]), r[1], "&rarr;", M(r[2]), r[3], "&#10003;" if r[4] else "&#10007;"])
    head = ["edge of <em>G</em><sub>1</sub>", "d", "", "image", "d", "in <em>G</em><sub>3</sub>?",
            "edge of <em>G</em><sub>1</sub>", "d", "", "image", "d", "in <em>G</em><sub>3</sub>?"]
    return T(head, rows,
             "Table 6.6 &mdash; every one of the 18 edges of G<sub>1</sub>, and its image under &phi;. "
             "Distance 1 becomes distance 4, distance 2 becomes distance 8 &equiv; &minus;1: in all cases an "
             "edge of G<sub>3</sub> = C<sub>9</sub>(1,&thinsp;4).", cls="wide")

def t_p6tris():
    rows = [
        ["<em>G</em><sub>1</sub> = <em>C</em><sub>9</sub>(1,2)", M("{1, 2, 7, 8}"), M("{1, 1, 7}"), M("{2, 8, 8}"),
         "{x, x+1, x+2}", "<strong>9</strong>"],
        ["<em>G</em><sub>2</sub> = <em>C</em><sub>9</sub>(1,3)", M("{1, 3, 6, 8}"), M("{3, 3, 3}"), M("{6, 6, 6}"),
         "{x, x+3, x+6}", "<strong>3</strong>"],
        ["<em>G</em><sub>3</sub> = <em>C</em><sub>9</sub>(1,4)", M("{1, 4, 5, 8}"), M("{1, 4, 4}"), M("{5, 5, 8}"),
         "{x, x+1, x+5}", "<strong>9</strong>"],
    ]
    return T(["graph", "connection set <em>S</em>", "multisets in <em>S</em><br>with sum 9",
              "&#8230; with sum 18", "the triangles", "how many"], rows,
             "Table 6.7 &mdash; solving a + b + c &equiv; 0 (mod 9) with a, b, c &isin; S. In G<sub>2</sub> the "
             "only solution is {3,3,3}, and {x, x+3, x+6} takes just three distinct values &mdash; the cosets of "
             "{0, 3, 6}. In the other two graphs the nine values are all distinct.", cls="wide", lc=(0,), hlrows=(1,))


def t_p6pairs():
    rows = []
    for name, S in [("<em>G</em><sub>1</sub>", (1,2,7,8)),
                    ("<em>G</em><sub>2</sub>", (1,3,6,8)),
                    ("<em>G</em><sub>3</sub>", (1,4,5,8))]:
        sums = sorted({a+b for i, a in enumerate(S) for b in S[i:]})
        rows.append([name, M("{" + ", ".join(map(str, S)) + "}"),
                     M(", ".join(map(str, sums))),
                     M(", ".join(str(9-a) for a in S))])
    return T(["graph", "connection set <em>S</em>",
              "all sums <em>b</em>&thinsp;+&thinsp;<em>c</em> with <em>b</em>,&thinsp;<em>c</em> &isin; <em>S</em>",
              "required partner sums 9&nbsp;&minus;&nbsp;<em>a</em>, <em>a</em> &isin; <em>S</em>"], rows,
             "Table 6.5 &mdash; a triangle needs a + b + c &equiv; 0 (mod 9) with a, b, c &isin; S. Comparing the "
             "third column with the fourth decides every case at a glance.", cls="wide", lc=(2, 3))

TBL = {
    'KNIGHT': t_knight, 'P1TARGET': t_p1target, 'P1BFS': t_p1bfs,
    'HH': t_hh, 'P2DEG': t_p2deg, 'EG': t_eg,
    'P6ID': t_p6id, 'P6EDGES': t_p6edges, 'P6INV': t_p6inv,
    'P6MAP': t_p6map, 'P6PAIRS': t_p6pairs, 'P6EDGEMAP': t_p6edgemap, 'P6TRIS': t_p6tris,
}
