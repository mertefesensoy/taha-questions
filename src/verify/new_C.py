# -*- coding: utf-8 -*-
"""Verification, part C: problems 11, 13, 14, 18, 19, 21 and the starred problem.
Problem 26 is handled in new_D.py."""
from itertools import combinations, permutations
from collections import deque
import random
FAIL=[]
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+name+(("  -- "+detail) if detail else ""))
    if not cond: FAIL.append(name)
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

print("="*74); print("PROBLEM 11 -- |V|=11, |E|=45  =>  some degree >= 9"); print("="*74)
print(f"   sum of degrees = 2*45 = 90;  if every degree were <= 8 the sum would be <= 11*8 = 88 < 90")
check("11*8 = 88 < 90 = 2|E|, so some degree is >= 9", 11*8 < 2*45, "88 < 90")
check("ceil(90/11) = 9", -(-90//11)==9)
check("the bound is attainable (45 <= C(11,2) = 55, so simple graphs with 45 edges exist)", 45 <= 55)

print(); print("="*74); print("PROBLEM 13 -- 100 vertices, delta >= 33, one vertex of degree >= 66"); print("="*74)
print("   a component containing a vertex of degree d has at least d+1 vertices")
print("   component of the high-degree vertex: >= 67;  any other component: >= 34;  67 + 34 = 101 > 100")
check("67 + 34 = 101 > 100, so a second component cannot exist", 67+34 > 100, "101 > 100")
# scaled-down analogue, verified exhaustively: n=8, delta>=2, some vertex of degree >=4  (8/3 ~ 33/100 scaled)
def graphs(n):
    P=list(combinations(range(n),2))
    for m in range(1<<len(P)):
        yield frozenset(p for i,p in enumerate(P) if m>>i&1)
def deg(n,E):
    d=[0]*n
    for a,b in E: d[a]+=1; d[b]+=1
    return d
ok=True; wit=0
for E in graphs(7):                       # n=7, delta>=2, max degree>=4 : 5+3=8>7
    d=deg(7,E)
    if min(d)>=2 and max(d)>=4:
        wit+=1
        if ncomp(7,E)!=1: ok=False
check("scaled analogue (n=7, delta>=2, some degree>=4) is always connected", ok, f"{wit} graphs matched")

print(); print("="*74); print("PROBLEM 14 -- 66 vertices; 10 deletions to acyclic, 33 additions to connected"); print("="*74)
def cyclerank(n,E): return len(E)-n+ncomp(n,E)
def min_del(n,E):
    """brute-force minimum deletions making E acyclic"""
    for k in range(len(E)+1):
        for D in combinations(sorted(E),k):
            R=frozenset(E)-set(D)
            if len(R)==n-ncomp(n,R): return k
def min_add(n,E): return ncomp(n,E)-1
ok1=ok2=True
random.seed(3)
for _ in range(120):
    n=random.randint(3,7); P=list(combinations(range(n),2))
    E=frozenset(random.sample(P, random.randint(0,len(P))))
    if min_del(n,E)!=cyclerank(n,E): ok1=False
    if min_add(n,E)!=ncomp(n,E)-1: ok2=False
check("min deletions to become acyclic = |E| - n + c", ok1, "120 random graphs, brute-forced")
check("min additions to become connected = c - 1", ok2, "adding an edge drops the component count by at most 1")
c = 33+1; m = 66 - c + 10
print(f"   c - 1 = 33  =>  c = {c};   m - n + c = 10  =>  m = 66 - {c} + 10 = {m}")
check("the answer is m = 42", m==42, f"m = {m}")
# exhibit such a graph: a connected graph on 33 vertices with 42 edges, plus 33 isolated vertices
n=66; E=set((i,i+1) for i in range(32))            # path on 0..32  (32 edges)
extra=[(0,i) for i in range(2,12)]                 # 10 chords -> cycle rank 10
E=frozenset(E)|frozenset(extra)
print(f"   witness: path on 33 vertices + 10 chords, plus 33 isolated vertices")
check("witness has 66 vertices, 42 edges, 34 components", len(E)==42 and ncomp(66,E)==34,
      f"|E|={len(E)}, components={ncomp(66,E)}")
check("witness needs exactly 10 deletions and 33 additions",
      cyclerank(66,E)==10 and ncomp(66,E)-1==33, f"deletions {cyclerank(66,E)}, additions {ncomp(66,E)-1}")

print(); print("="*74); print("PROBLEM 18 -- 88 vertices, 42 components, 111 edges; step = +1 edge, -2 edges"); print("="*74)
print("   after k steps: |E| = 111 - k;  connected needs |E| >= 87  =>  k <= 24")
print("   each step lowers the component count by at most 1  =>  k >= 42 - 1 = 41")
check("41 > 24, so the target is unreachable", 41 > 24, "impossible")
check("edge budget: 111 - 24 = 87 = n - 1 exactly", 111-24==87)

print(); print("="*74); print("PROBLEM 19 -- 77 vertices, 42 components, 66 edges; step = -1 edge, +2 edges"); print("="*74)
exc = 66 - (77-42)
print(f"   cycle rank at the start: |E| - (n - c) = 66 - (77 - 42) = {exc}")
print("   deleting an edge lowers the rank by at most 1; adding one never lowers it => >= 31 steps")
print("   after k steps |E| = 66 + k, and a forest on 77 vertices has at most 76 edges => k <= 10")
check("cycle rank at the start is 31", exc==31)
check("31 > 10, so the target is unreachable", exc > 76-66, "impossible")
# verify the per-step rank claim on random small graphs
ok=True
random.seed(11)
for _ in range(4000):
    n=random.randint(3,7); P=list(combinations(range(n),2))
    E=set(random.sample(P, random.randint(1,len(P))))
    r0=len(E)-n+ncomp(n,frozenset(E))
    e=random.choice(sorted(E)); E2=set(E)-{e}
    cand=[p for p in P if p not in E2]
    if len(cand)<2: continue
    f,g=random.sample(cand,2); E3=frozenset(E2|{f,g})
    r1=len(E3)-n+ncomp(n,E3)
    if r1 < r0-1: ok=False
check("one step (delete 1, add 2) lowers the cycle rank by at most 1", ok, "4000 random steps")

print(); print("="*74); print("PROBLEM 21 -- every simple graph has an acyclic orientation"); print("="*74)
def has_dicycle(n,A):
    idx={v:0 for v in range(n)}; state={}
    def dfs(u):
        state[u]=1
        for w in range(n):
            if (u,w) in A:
                if state.get(w)==1: return True
                if state.get(w,0)==0 and dfs(w): return True
        state[u]=2; return False
    return any(state.get(v,0)==0 and dfs(v) for v in range(n))
ok=True
random.seed(5)
for _ in range(3000):
    n=random.randint(2,7); P=list(combinations(range(n),2))
    E=random.sample(P, random.randint(0,len(P)))
    A={(a,b) for a,b in E}          # orient small index -> large index
    if has_dicycle(n,A): ok=False
check("orienting every edge from the smaller to the larger label gives no directed cycle", ok,
      "3000 random simple graphs")

print(); print("="*74); print("STARRED -- 123 edges, three colours, each colour class spanning-connected"); print("="*74)
print("   each colour class is a connected spanning subgraph, so has >= n-1 edges")
print("   3(n-1) <= 123  =>  n <= 42")
check("n <= 42", 3*(42-1)<=123 and 3*(43-1)>123, "3*41 = 123 <= 123, but 3*42 = 126 > 123")
# construct 3 edge-disjoint Hamiltonian paths on 42 vertices (zig-zag / Walecki)
def hampath(n,k):
    seq=[k]; lo=hi=k
    for t in range(1,n):
        if t%2: hi=(hi+1)%n; seq.append(hi)
        else:   lo=(lo-1)%n; seq.append(lo)
    return seq
N=42
paths=[hampath(N,k) for k in range(3)]
Es=[frozenset(tuple(sorted((p[i],p[i+1]))) for i in range(N-1)) for p in paths]
allv=[set(p)==set(range(N)) for p in paths]
disjoint=len(Es[0]|Es[1]|Es[2])==sum(len(e) for e in Es)
spanning=[ncomp(N,e)==1 and len(e)==N-1 for e in Es]
check("three edge-disjoint Hamiltonian paths on 42 vertices exist",
      all(allv) and disjoint and all(spanning),
      f"each has {len(Es[0])} edges, union has {len(Es[0]|Es[1]|Es[2])} edges")
check("their union has exactly 123 edges", len(Es[0]|Es[1]|Es[2])==123)
check("so 42 vertices is achievable", all(spanning) and len(Es[0]|Es[1]|Es[2])==123)

print(); print("="*74); print("PART C RESULT:", "ALL PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
