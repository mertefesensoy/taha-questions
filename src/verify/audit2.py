# -*- coding: utf-8 -*-
"""Independent audit of Problems 1 and 6, by methods different from those used
to derive the claims in the first place."""
from itertools import combinations, permutations, product
from collections import deque
FAIL = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not cond: FAIL.append(name)

print("="*78); print("PROBLEM 1  -- knights on the 3x3 board"); print("="*78)
# knight graph, rebuilt from the move vectors rather than from a hand-written table
MOVES = [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
sq = {(r,c): 3*r+c+1 for r in range(3) for c in range(3)}
adj = {s: set() for s in range(1,10)}
for (r,c), s in sq.items():
    for dr, dc in MOVES:
        if (r+dr, c+dc) in sq: adj[s].add(sq[(r+dr, c+dc)])
check("square 5 is isolated", adj[5] == set(), f"neighbours of 5: {adj[5] or 'none'}")
check("the other eight squares all have degree 2",
      all(len(adj[s]) == 2 for s in range(1,10) if s != 5),
      str({s: len(adj[s]) for s in range(1,10)}))
# the 8 usable squares form ONE cycle: connected + 2-regular
usable = [s for s in range(1,10) if adj[s]]
seen, q = {usable[0]}, deque([usable[0]])
while q:
    u = q.popleft()
    for w in adj[u]:
        if w not in seen: seen.add(w); q.append(w)
check("they form a single connected 2-regular graph, i.e. C_8", seen == set(usable), f"|V|={len(seen)}")
cyc, prev, cur = [1], None, 1
while True:
    nxt = [x for x in adj[cur] if x != prev][0]
    if nxt == 1: break
    cyc.append(nxt); prev, cur = cur, nxt
doc = [1,6,7,2,9,4,3,8]
def same_cycle(a, b):
    """equal up to rotation and reflection -- a cycle has no distinguished direction"""
    rots = [b[i:]+b[:i] for i in range(len(b))]
    return a in rots or a[::-1] in rots
check("the cycle order matches the document's 1-6-7-2-9-4-3-8 (up to direction)",
      same_cycle(cyc, doc), " - ".join(map(str,cyc)) + "  (document: " + " - ".join(map(str,doc)) + ")")
check("every edge of the document's cycle is a genuine knight move",
      all(doc[(i+1)%8] in adj[doc[i]] for i in range(8)) and sorted(doc)==[1,2,3,4,6,7,8,9])
pos = {v:i for i,v in enumerate(cyc)}
check("the four corners sit at alternate vertices of the cycle",
      sorted(pos[c] for c in (1,3,7,9)) == [0,2,4,6],
      f"corner positions {[(c,pos[c]) for c in (1,7,9,3)]}")

def word(state):
    W, D = state; lab = {}
    for s in W: lab[s]='W'
    for s in D: lab[s]='D'
    occ = sorted(lab, key=lambda s: pos[s])
    w = ''.join(lab[s] for s in occ)
    return max(w[i:]+w[:i] for i in range(4))          # canonical rotation, W > D
def norm(W,D): return (tuple(sorted(W)), tuple(sorted(D)))
def moves(st):
    W,D = st; occ = set(W)|set(D); pieces = list(W)+list(D); out=[]
    for k in range(4):
        for nx in adj[pieces[k]]:
            if nx in occ: continue
            p = pieces[:]; p[k] = nx
            out.append(norm(tuple(p[:2]), tuple(p[2:])))
    return out
start = norm((1,9),(3,7))
check("the start position's cyclic colour word is WDWD", word(start) == "WDWD", word(start))
# INVARIANCE: verify directly that no legal move from any reachable state changes the word
seen, q, bad = {start}, deque([start]), 0
while q:
    st = q.popleft()
    for nx in moves(st):
        if word(nx) != word(st): bad += 1
        if nx not in seen: seen.add(nx); q.append(nx)
check("no legal move ever changes the cyclic colour word", bad == 0,
      f"{len(seen)} states, every outgoing move checked")
corner = [s for s in seen if set(s[0])|set(s[1]) == {1,3,7,9}]
def opp_differ(st):
    lab = {}
    for s in st[0]: lab[s]='W'
    for s in st[1]: lab[s]='D'
    return lab[1] != lab[9] and lab[3] != lab[7]
check("no reachable corner position has opposite corners of different colours",
      not any(opp_differ(s) for s in corner), f"{len(corner)} reachable corner positions, 0 of the required kind")
# every target colouring really does read WWDD
tgt = []
for c1 in "WD":
    for c3 in "WD":
        c9 = "D" if c1=="W" else "W"; c7 = "D" if c3=="W" else "W"
        lab = {1:c1,3:c3,7:c7,9:c9}
        W = tuple(k for k,v in lab.items() if v=="W"); D = tuple(k for k,v in lab.items() if v=="D")
        tgt.append(word(norm(W,D)))
check("all four admissible target positions read WWDD", set(tgt) == {"WWDD"}, str(tgt))
# completeness of the invariant
allst = set()
for p4 in combinations(usable,4):
    for W in combinations(p4,2):
        allst.add(norm(W, tuple(x for x in p4 if x not in W)))
check("the invariant is complete: reachable == exactly the WDWD placements",
      seen == {s for s in allst if word(s)=="WDWD"},
      f"{len(seen)} reachable of {len(allst)} placements")
# Guarini
g0, g1 = norm((1,3),(7,9)), norm((7,9),(1,3))
seen2, par, q = {g0}, {g0:None}, deque([g0])
while q:
    st=q.popleft()
    for nx in moves(st):
        if nx not in seen2: seen2.add(nx); par[nx]=st; q.append(nx)
L=0; cur=g1
while par[cur] is not None: L+=1; cur=par[cur]
check("Guarini's puzzle (W on 1,3 <-> D on 7,9) IS solvable, in 16 moves",
      g1 in seen2 and L == 16 and word(g0)=="WWDD", f"{L} moves, start word {word(g0)}")

print(); print("="*78); print("PROBLEM 6  -- the three drawings"); print("="*78)
def circ(S): return {tuple(sorted((i,(i+s)%9))) for i in range(9) for s in S}

# re-read the picture with a DIFFERENT threshold and sampling density, measuring
# the vertex centres rather than assuming the nonagon's geometry
import audit_img
for name, S in [('G1',(1,2)), ('G2',(1,3)), ('G3',(1,4))]:
    V, dark, w, h, geo = audit_img.vertices(audit_img.BOX[name], 120)
    E = {p for p in combinations(range(9), 2)
         if audit_img.darkfrac(dark, w, h, V[p[0]], V[p[1]], 14) > 0.97}
    want = {tuple(sorted((i,(i+s)%9))) for i in range(9) for s in S}
    check(f"{name} re-read from the image is C_9{S}", E == want and len(V) == 9,
          f"{len(V)} vertices, {len(E)} edges")

# isomorphism, by canonical form rather than by trying all 9! permutations
def canon(E):
    best = None
    for p in permutations(range(9)):
        f = tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in E))
        if best is None or f < best: best = f
    return best
c1, c2, c3 = canon(circ((1,2))), canon(circ((1,3))), canon(circ((1,4)))
check("G1 and G3 have the same canonical form (isomorphic)", c1 == c3)
check("G2's canonical form differs from both (not isomorphic)", c2 != c1 and c2 != c3)
# the explicit map really is an isomorphism
phi = lambda i: (4*i) % 9
img = {tuple(sorted((phi(a), phi(b)))) for a,b in circ((1,2))}
check("phi(i)=4i maps E(G1) exactly onto E(G3)", img == circ((1,4)),
      f"{len(img)} images, {len(circ((1,4)))} edges in G3")
check("phi is a bijection with inverse 7i", sorted(phi(i) for i in range(9)) == list(range(9))
      and all((7*phi(i)) % 9 == i for i in range(9)))
# triangle multisets, enumerated independently of the hand argument
for name, S, expect_sum9, expect_count in [
        ('G1', {1,2,7,8}, {(1,1,7)}, 9), ('G2', {1,3,6,8}, {(3,3,3)}, 3), ('G3', {1,4,5,8}, {(1,4,4)}, 9)]:
    sols9  = {tuple(sorted(t)) for t in product(S, repeat=3) if sum(t) == 9}
    sols18 = {tuple(sorted(t)) for t in product(S, repeat=3) if sum(t) == 18}
    negs   = {tuple(sorted(9-x for x in t)) for t in sols9}
    E = circ({s for s in S if s <= 4})
    tris = [c for c in combinations(range(9),3) if all(tuple(sorted(p)) in E for p in combinations(c,2))]
    check(f"{name}: the only multiset with sum 9 is {sorted(expect_sum9)[0]}", sols9 == expect_sum9, str(sols9))
    check(f"{name}: the sum-18 multisets are exactly the negatives of the sum-9 ones", sols18 == negs, str(sols18))
    check(f"{name}: triangle count is {expect_count}", len(tris) == expect_count, f"{len(tris)} triangles")
# 4-cycle counts
def c4(E):
    n=0
    for q in combinations(range(9),4):
        for p in [(0,1,2,3),(0,1,3,2),(0,2,1,3)]:
            cy=[q[i] for i in p]
            if all(tuple(sorted((cy[i],cy[(i+1)%4]))) in E for i in range(4)): n+=1
    return n
check("4-cycle counts are 9, 18, 9", [c4(circ(s)) for s in ((1,2),(1,3),(1,4))] == [9,18,9],
      str([c4(circ(s)) for s in ((1,2),(1,3),(1,4))]))
# |Aut(G1)| = 18, and complement of G1 is isomorphic to G2
aut = sum(1 for p in permutations(range(9))
          if {tuple(sorted((p[a],p[b]))) for a,b in circ((1,2))} == circ((1,2)))
check("|Aut(G1)| = 18 (the dihedral group of the nonagon)", aut == 18, str(aut))
allp = {tuple(sorted(p)) for p in combinations(range(9),2)}
check("the complement of G1 is isomorphic to G2", canon(allp - circ((1,2))) == c2)
print(); print("="*78)
print("RESULT:", "ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
print("="*78)
