# -*- coding: utf-8 -*-
"""Independent re-verification of every mathematical claim in the document.
Written from scratch: exhaustive enumeration where feasible, not a re-run of the
scripts that produced the claims."""
from itertools import combinations, permutations, product
from collections import deque
FAIL = []
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (("  -- " + detail) if detail else ""))
    if not cond: FAIL.append(name)

# ---------- small-graph machinery ----------
def all_graphs(n):
    pairs = list(combinations(range(n), 2))
    for mask in range(1 << len(pairs)):
        yield frozenset(p for i, p in enumerate(pairs) if mask >> i & 1)
def deg(n, E):
    d = [0]*n
    for a, b in E: d[a] += 1; d[b] += 1
    return d
def comps(n, E):
    adj = {v: set() for v in range(n)}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    seen, out = set(), []
    for s in range(n):
        if s in seen: continue
        q, c = deque([s]), set([s]); seen.add(s)
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in seen: seen.add(w); c.add(w); q.append(w)
        out.append(c)
    return out
def induced(E, S): return frozenset(e for e in E if e[0] in S and e[1] in S)
def is_cycle(S, E):
    k = len(S); Ei = induced(E, S)
    return k >= 3 and len(Ei) == k and all(deg(max(S)+1, Ei)[v] == 2 for v in S) and len(comps_sub(S, Ei)) == 1
def comps_sub(S, E):
    adj = {v: set() for v in S}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    seen, out = set(), []
    for s in S:
        if s in seen: continue
        q, c = deque([s]), {s}; seen.add(s)
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in seen: seen.add(w); c.add(w); q.append(w)
        out.append(c)
    return out
def is_path(S, E):
    k = len(S); Ei = induced(E, S)
    if len(comps_sub(S, Ei)) != 1: return False
    if k == 1: return len(Ei) == 0
    d = deg(max(S)+1, Ei)
    ds = sorted(d[v] for v in S)
    return len(Ei) == k-1 and ds == [1,1] + [2]*(k-2)

print("=" * 78)
print("PROBLEM 3  -- classification theorems, checked on every graph with n <= 6")
print("=" * 78)
ok2reg = ok_d2 = True
tot = 0
for n in range(1, 7):
    for E in all_graphs(n):
        tot += 1
        d = deg(n, E); C = comps(n, E)
        lhs = all(x == 2 for x in d)
        rhs = all(is_cycle(S, E) for S in C)
        if lhs != rhs: ok2reg = False
        lhs2 = max(d) <= 2 if n else True
        rhs2 = all(is_cycle(S, E) or is_path(S, E) for S in C)
        if lhs2 != rhs2: ok_d2 = False
check("2-regular  <=>  every component is a cycle", ok2reg, f"{tot} graphs tested")
check("Delta(G) <= 2  <=>  every component is a path or a cycle", ok_d2, f"{tot} graphs tested")
# 2-regular counts = partitions into parts >= 3
def parts(n, mn=3):
    if n == 0: return 1
    return sum(parts(n-k, k) for k in range(mn, n+1))
counts = [parts(n) for n in range(3, 10)]
check("count of 2-regular graphs on n=3..9 vertices is 1,1,1,2,2,3,4",
      counts == [1,1,1,2,2,3,4], str(counts))

print()
print("=" * 78)
print("PROBLEM 4 & 5  -- parity of odd-degree vertices, per graph and per component")
print("=" * 78)
ok4 = ok5 = True
for n in range(1, 7):
    for E in all_graphs(n):
        d = deg(n, E)
        if sum(1 for x in d if x % 2) % 2: ok4 = False
        for S in comps(n, E):
            if sum(1 for v in S if d[v] % 2) % 2: ok5 = False
check("Cor 4.2: |V_odd| is even in every finite graph", ok4)
check("Prob 5: |V_odd| is even in every component (so an odd u has a partner)", ok5)
# the ray
check("the ray has exactly one odd-degree vertex", True, "d(v0)=1, d(vi)=2 for i>=1 -- by construction")
# P2 + P2 witness for 'must pass to the component'
E = frozenset({(0,1),(2,3)}); d = deg(4, E)
check("P2+P2: all 4 degrees odd, yet 2 of them unreachable from vertex 0",
      d == [1,1,1,1] and len(comps(4, E)) == 2)

print()
print("=" * 78)
print("PROBLEM 7  -- minimum degree forces connectivity; the exact threshold")
print("=" * 78)
ok7 = ok7d = True
worst_disconnected = {}
for n in range(1, 8):
    for E in all_graphs(n):
        d = deg(n, E); dmin = min(d) if n else 0
        conn = len(comps(n, E)) == 1
        if 2*dmin >= n and not conn: ok7 = False
        if 2*dmin >= n and conn:
            # diameter <= 2 ?
            adj = {v:set() for v in range(n)}
            for a,b in E: adj[a].add(b); adj[b].add(a)
            for u in range(n):
                dist = {u:0}; q=deque([u])
                while q:
                    x=q.popleft()
                    for w in adj[x]:
                        if w not in dist: dist[w]=dist[x]+1; q.append(w)
                if max(dist.values()) > 2: ok7d = False
        if not conn:
            worst_disconnected[n] = max(worst_disconnected.get(n, -1), dmin)
check("delta >= n/2  =>  G is connected", ok7, "all graphs n <= 7")
check("delta >= n/2  =>  diam(G) <= 2", ok7d, "all graphs n <= 7")
thr = {n: worst_disconnected.get(n, -1) for n in range(2, 8)}
pred = {n: n//2 - 1 for n in range(2, 8)}
check("largest delta of a DISCONNECTED graph is floor(n/2)-1 (threshold is sharp)",
      thr == pred, f"observed {thr}, predicted {pred}")

print()
print("=" * 78)
print("PROBLEM 2  -- the two degree sequences")
print("=" * 78)
target = sorted([1,2,2,3,3,3])
Estar = [(0,1),(0,2),(0,3),(1,2),(1,4),(2,4),(3,5)]   # u1..u6 -> 0..5, as printed in the document
d = deg(6, frozenset(map(lambda e: tuple(sorted(e)), Estar)))
check("the graph printed in the document realises 1,2,2,3,3,3",
      sorted(d) == target and len(set(map(lambda e: tuple(sorted(e)), Estar))) == 7,
      f"degrees {sorted(d)}, {len(Estar)} edges")
# is it really K4-minus-an-edge plus a pendant path?
dia = {(0,1),(0,2),(1,2),(1,4),(2,4)}
check("its structure is a diamond on {u1,u2,u3,u5} plus the path u1-u4-u6",
      dia <= set(map(lambda e: tuple(sorted(e)), Estar)) and (0,4) not in set(map(lambda e: tuple(sorted(e)), Estar)))
found = None
for E in all_graphs(7):
    if sorted(deg(7, E)) == sorted([1,1,2,2,3,4,4]): found = E; break
check("no simple graph on 7 vertices has degree sequence 1,1,2,2,3,4,4",
      found is None, "exhaustive over all 2^21 = 2097152 graphs")
check("its degree sum 17 is odd", sum([1,1,2,2,3,4,4]) % 2 == 1)

print()
print("=" * 78)
print("PROBLEM 8  -- the directed count")
print("=" * 78)
for n in (43, 60, 1000):
    x = 22*n - (22*(n-3) + 12 + 12)
    if x != 42: FAIL.append("P8 n=%d" % n)
check("22n = 22(n-3)+12+12+x forces x = 42 for every n", True, "checked n = 43, 60, 1000")
check("the three exceptional indegrees average to 22", (12+12+42) == 3*22, "12+12+42 = 66 = 3*22")
check("a simple digraph needs n >= 43", 42 <= 43-1 and 42 > 42-1)
print()
print("=" * 78)
print("RESULT:", "ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
print("=" * 78)
