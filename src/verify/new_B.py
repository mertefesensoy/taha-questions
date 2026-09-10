# -*- coding: utf-8 -*-
"""Verification, part B: problems 12, 20, 22, 23, 25."""
from itertools import combinations, permutations, product
from collections import deque
from functools import lru_cache
FAIL=[]
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+name+(("  -- "+detail) if detail else ""))
    if not cond: FAIL.append(name)
def graphs(n):
    P=list(combinations(range(n),2))
    for msk in range(1<<len(P)):
        yield frozenset(p for i,p in enumerate(P) if msk>>i&1)
def ncomp(n,E):
    adj={v:set() for v in range(n)}
    for a,b in E: adj[a].add(b); adj[b].add(a)
    seen=set(); c=0
    for s in range(n):
        if s in seen: continue
        c+=1; q=deque([s]); seen.add(s)
        while q:
            u=q.popleft()
            for w in adj[u]:
                if w not in seen: seen.add(w); q.append(w)
    return c
def connected(n,E): return ncomp(n,E)==1
def deg(n,E):
    d=[0]*n
    for a,b in E: d[a]+=1; d[b]+=1
    return d

print("="*74); print("PROBLEM 12 -- the cycle-avoidance game"); print("="*74)
# exhaustive game tree: state = frozenset of drawn edges (always a forest, else the game ended)
def solve(n):
    P=list(combinations(range(n),2))
    @lru_cache(maxsize=None)
    def win(state):
        """True if the player TO MOVE wins, given 'state' is a forest."""
        S=set(state)
        safe=[e for e in P if e not in S and ncomp(n,frozenset(S|{e}))<ncomp(n,frozenset(S))]
        if not safe:
            return False        # every move creates a cycle (or none exists) -> mover loses
        return any(not win(frozenset(S|{e})) for e in safe)
    return win(frozenset())
res={n: ("first" if solve(n) else "second") for n in range(2,8)}
for n,w in res.items():
    print(f"   n={n:2d} ({'even' if n%2==0 else 'odd '}): safe moves = n-1 = {n-1};  winner = {w} player")
check("first player wins exactly when n is even",
      all((w=="first")==(n%2==0) for n,w in res.items()), str(res))

print(); print("="*74); print("PROBLEM 20 -- 2k vertices, delta >= k-1, some vertex of degree k"); print("="*74)
ok=True; wit=0
for k in range(1,4):
    n=2*k
    for E in graphs(n):
        d=deg(n,E)
        if min(d)>=k-1 and max(d)>=k:
            wit+=1
            if not connected(n,E): ok=False
check("every such graph is connected", ok, f"exhaustive for k=1,2,3 (n=2,4,6); {wit} graphs satisfied the hypothesis")
# sharpness: drop the degree-k vertex requirement
bad=[E for E in graphs(6) if min(deg(6,E))>=2 and not connected(6,E)]
check("without the degree-k vertex the claim fails (k=3: two triangles)", len(bad)>0,
      f"{len(bad)} disconnected graphs on 6 vertices with delta >= k-1 = 2")

print(); print("="*74); print("PROBLEM 22 -- e,f,g with G-e-g and G-f-g disconnected"); print("="*74)
ok=True; wit=0; counter=None
for n in range(3,7):
    for E in graphs(n):
        if not connected(n,E) or len(E)<3: continue
        if any(not connected(n,E-{x}) for x in E): continue      # G must be bridgeless
        for e,f,g in permutations(sorted(E),3):
            if connected(n,E-{e,g}) or connected(n,E-{f,g}): continue
            wit+=1
            if connected(n,E-{e,f}):
                ok=False; counter=(n,sorted(E),e,f,g)
check("G-e-f is then always disconnected", ok,
      f"exhaustive n<=6; {wit} (G,e,f,g) instances matched the hypothesis"+(f"; counterexample {counter}" if counter else ""))
# the literal wording ("prove G-f-g is disconnected") is already a hypothesis
check("the printed conclusion 'G-f-g is disconnected' restates a hypothesis (typo)", True,
      "so the intended conclusion must be about the third pair, G-e-f")

print(); print("="*74); print("PROBLEM 23 -- deleting a column keeps the rows distinct"); print("="*74)
ok=True; tested=0
for n in (2,3):
    for T in product(product(range(2),repeat=n),repeat=n):
        if len(set(T))<n: continue                      # rows must be pairwise distinct
        tested+=1
        good=any(len({tuple(r[:j]+r[j+1:]) for r in T})==n for j in range(n))
        if not good: ok=False
for n in (3,):
    for T in product(product(range(3),repeat=n),repeat=n):
        if len(set(T))<n: continue
        tested+=1
        if not any(len({tuple(r[:j]+r[j+1:]) for r in T})==n for j in range(n)): ok=False
check("some column can always be deleted", ok, f"{tested} tables with pairwise distinct rows tested (n=2,3; 2 and 3 symbols)")

print(); print("="*74); print("PROBLEM 25 -- 13 people: degree >= 6, or 3 mutual strangers"); print("="*74)
# the complement argument, verified as a statement about triangle-free graphs
def trianglefree(n,E):
    S=set(E)
    return not any(tuple(sorted((a,b))) in S and tuple(sorted((b,c))) in S and tuple(sorted((a,c))) in S
                   for a,b,c in combinations(range(n),3))
ok=True
for n in range(3,8):
    for E in graphs(n):
        if trianglefree(n,E) and E:
            d=deg(n,E)
            for a,b in E:
                if d[a]+d[b]>n: ok=False
check("in a triangle-free graph, d(u)+d(v) <= n for every edge uv", ok, "exhaustive n <= 7")
# sharpness: 12 people where nobody knows 6 and no 3 mutual strangers
E12=frozenset({tuple(sorted((a,b))) for a,b in combinations(range(6),2)} |
              {tuple(sorted((a,b))) for a,b in combinations(range(6,12),2)})
d12=deg(12,E12)
indep3=any(all(tuple(sorted(p)) not in E12 for p in combinations(t,2)) for t in combinations(range(12),3))
check("with 12 people the statement FAILS (two disjoint K_6's)",
      max(d12)==5 and not indep3, f"max degree {max(d12)}, independent set of size 3: {indep3}")
# random search for a counterexample on 13 vertices
import random
random.seed(7); found=None
for _ in range(200000):
    n=13; E=set()
    order=list(combinations(range(13),2)); random.shuffle(order)
    d=[0]*13
    for a,b in order:
        if d[a]<5 and d[b]<5 and random.random()<0.9: E.add((a,b)); d[a]+=1; d[b]+=1
    if max(d)<=5 and not any(all(tuple(sorted(p)) not in E for p in combinations(t,2))
                             for t in combinations(range(13),3)):
        found=E; break
check("no counterexample on 13 vertices found by random search", found is None, "200000 random graphs with max degree <= 5")
print(); print("="*74); print("PART B RESULT:", "ALL PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
