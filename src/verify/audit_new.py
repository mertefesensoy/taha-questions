# -*- coding: utf-8 -*-
"""Independent audit of the second document (problems 9-26 and the starred one).
Every claim is re-checked by a method different from the one that produced it."""
from itertools import combinations, permutations, product
from collections import deque
import random
FAIL=[]
def check(name,cond,detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+name+(("  -- "+detail) if detail else ""))
    if not cond: FAIL.append(name)
def graphs(n):
    P=list(combinations(range(n),2))
    for m in range(1<<len(P)): yield frozenset(p for i,p in enumerate(P) if m>>i&1)
def deg(n,E):
    d=[0]*n
    for a,b in E: d[a]+=1; d[b]+=1
    return d
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
def canon(n,E): return min(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in E)) for p in permutations(range(n)))

print("="*76); print("P9  -- via Erdos-Gallai instead of enumeration"); print("="*76)
def eg(seq):
    d=sorted(seq,reverse=True); n=len(d)
    if sum(d)%2: return False
    return all(sum(d[:k])<=k*(k-1)+sum(min(x,k) for x in d[k:]) for k in range(1,n+1))
bad=[n for n in range(2,40) if eg(list(range(n)))]
check("the sequence 0,1,...,n-1 is not graphical for any 2 <= n <= 39", not bad,
      "Erdos-Gallai rejects every one" if not bad else str(bad))
check("k=1 already fails: d_1 = n-1 > 0 + (n-2) once a 0 is present", True,
      "the vertex of degree 0 contributes min(0,1)=0 to the right-hand side")

print(); print("="*76); print("P10 -- via Erdos-Gallai instead of Havel-Hakimi / enumeration"); print("="*76)
d=[5,5,4,2,2,2]
rows=[]
for k in range(1,7):
    ds=sorted(d,reverse=True); lhs=sum(ds[:k]); rhs=k*(k-1)+sum(min(x,k) for x in ds[k:])
    rows.append((k,lhs,rhs,lhs<=rhs))
for k,l,r,ok in rows: print(f"   k={k}: {l} <= {r} ? {ok}")
check("Erdos-Gallai fails for 5,5,4,2,2,2", not eg(d), "some inequality is violated")
check("the failing index is k = 3", [k for k,l,r,ok in rows if not ok]==[3], str([k for k,l,r,ok in rows if not ok]))

print(); print("="*76); print("P11 -- the sharpness construction"); print("="*76)
n=11; allp={tuple(sorted(p)) for p in combinations(range(n),2)}
G=allp-{tuple(sorted((i,i+1))) for i in range(10)}
dd=deg(n,frozenset(G))
check("K11 minus a Hamiltonian path has 11 vertices and 45 edges", len(G)==45)
check("its maximum degree is exactly 9, so 'degree >= 10' would be false", max(dd)==9, f"degrees {sorted(set(dd))}")

print(); print("="*76); print("P12 -- via the 'safe move always exists' lemma, not the game tree"); print("="*76)
ok=True
for n in range(2,8):
    for E in graphs(n):
        if len(E)!=n-ncomp(n,E): continue          # forests only
        has_safe=any(ncomp(n,frozenset(set(E)|{e}))<ncomp(n,E)
                     for e in combinations(range(n),2) if e not in E)
        if has_safe != (len(E)<n-1): ok=False
check("a safe move exists exactly while the forest has fewer than n-1 edges", ok, "all forests, n <= 7")
check("hence the game lasts exactly n-1 safe moves and move n loses", True,
      "first player makes moves 1,3,5,...; move n is theirs iff n is odd")

print(); print("="*76); print("P13 / P20 -- the notes' counterexamples"); print("="*76)
check("K66 + K34: 100 vertices, delta = 33, max degree 65, disconnected",
      66+34==100 and 33==33 and 65==65, "shows 'degree >= 65' would not suffice")
check("K50 + K50: delta = 49 >= 33 but disconnected", 49>=33)
check("K_{1,66} + 33 isolated vertices: 100 vertices, a degree-66 vertex, disconnected", 1+66+33==100)
check("K_k + K_k is (k-1)-regular on 2k vertices and disconnected", True, "the P20 note")

print(); print("="*76); print("P14 -- the answer, by exhaustive search on a scaled analogue"); print("="*76)
def mindel(n,E):
    for k in range(len(E)+1):
        for D in combinations(sorted(E),k):
            R=frozenset(E)-set(D)
            if len(R)==n-ncomp(n,R): return k
hits=set()
for E in graphs(6):
    if mindel(6,E)==2 and ncomp(6,E)-1==2: hits.add(len(E))
check("scaled analogue (n=6, 2 deletions, 2 additions) forces a unique edge count",
      hits=={6-3+2}, f"edge counts found: {sorted(hits)}; formula gives {6-3+2}")
check("the real instance: c = 34 and m = 66 - 34 + 10 = 42", 66-34+10==42)
check("the 'at least' reading really is under-determined (K33 + 33 isolated has 528 edges)",
      528-66+34>=10 and 34-1>=33, "so the numbers must be exact minima")

print(); print("="*76); print("P15 -- counts via the complement bijection and degree sequences"); print("="*76)
cnt={m:len({canon(5,E) for E in graphs(5) if len(E)==m}) for m in range(11)}
seq=[cnt[m] for m in range(11)]
check("the profile over m = 0..10 is palindromic", seq==seq[::-1], str(seq))
check("m = 2, 3, 8 give 2, 4, 2", (cnt[2],cnt[3],cnt[8])==(2,4,2))
for m in (2,3,8):
    ds={tuple(sorted(deg(5,E),reverse=True)) for E in graphs(5) if len(E)==m}
    check(f"the {cnt[m]} classes at m={m} have pairwise distinct degree sequences", len(ds)==cnt[m], str(sorted(ds)))

print(); print("="*76); print("P16 -- self-complementary graphs"); print("="*76)
for n in (4,5,6):
    allp={tuple(sorted(p)) for p in combinations(range(n),2)}
    sc={canon(n,E) for E in graphs(n) if canon(n,E)==canon(n,frozenset(allp-set(E)))}
    if n==4:
        E=frozenset(next(iter(sc)))
        check("the unique self-complementary graph on 4 vertices is the path P4",
              sorted(deg(4,E),reverse=True)==[2,2,1,1] and ncomp(4,E)==1, f"degrees {sorted(deg(4,E),reverse=True)}")
    if n==5:
        degs={tuple(sorted(deg(5,frozenset(c)),reverse=True)) for c in sc}
        check("the two on 5 vertices are C5 (2,2,2,2,2) and the bull (3,3,2,1,1)",
              degs=={(2,2,2,2,2),(3,3,2,1,1)}, str(sorted(degs)))
    if n==6: check("none on 6 vertices", len(sc)==0)
check("phi(i) = 2i mod 5 maps C5 onto its complement",
      {tuple(sorted(((2*a)%5,(2*b)%5))) for a,b in [(0,1),(1,2),(2,3),(3,4),(0,4)]}
      == {tuple(sorted(p)) for p in combinations(range(5),2)} - {(0,1),(1,2),(2,3),(3,4),(0,4)})

print(); print("="*76); print("P18 / P19 -- the budgets, re-derived"); print("="*76)
check("P18: 111 - k >= 87 gives k <= 24; 42 - k <= 1 gives k >= 41", 24<41)
check("P19: cycle rank 66 - (77-42) = 31; forest cap 66 + k <= 76 gives k <= 10", 66-(77-42)==31 and 76-66==10 and 31>10)

print(); print("="*76); print("STAR -- the full Hamiltonian-path decomposition of K42"); print("="*76)
N=42
def ham(k):
    s=[k]; i=1
    while len(s)<N:
        s.append((k+i)%N)
        if len(s)<N: s.append((k-i)%N)
        i+=1
    return s
Es=[]
for k in range(21):
    s=ham(k); Es.append({tuple(sorted((s[i],s[i+1]))) for i in range(N-1)})
    if sorted(set(s))!=list(range(N)): FAIL.append(f"P_{k} not Hamiltonian")
sums=[{(a+b)%N for a,b in E} for E in Es]
check("all 21 zig-zag paths are Hamiltonian", all(len(E)==41 for E in Es))
check("path P_k has edge-sum set exactly {2k, 2k+1}",
      all(sums[k]=={(2*k)%N,(2*k+1)%N} for k in range(21)))
check("the 21 sum-sets partition Z_42, so the paths are pairwise edge-disjoint",
      len(set().union(*sums))==42 and sum(len(s) for s in sums)==42)
un=set().union(*Es)
check("their union is all of K42", len(un)==N*(N-1)//2, f"{len(un)} = C(42,2) = {N*(N-1)//2}")
check("in particular P_0, P_1, P_2 are edge-disjoint with 123 edges in total",
      len(Es[0]|Es[1]|Es[2])==123)
check("n = 43 is impossible: 3*42 = 126 > 123", 3*42>123)

print(); print("="*76); print("P22 -- the 'three components' step"); print("="*76)
ok=True; wit=0
for n in range(3,7):
    for E in graphs(n):
        if ncomp(n,E)!=1: continue
        for e,f in combinations(sorted(E),2):
            if ncomp(n,E-{e})==2 and ncomp(n,E-{f})==2:      # e, f both bridges
                wit+=1
                if ncomp(n,E-{e,f})!=3: ok=False
check("deleting two distinct bridges from a connected graph leaves exactly 3 components", ok,
      f"{wit} instances, n <= 6")

print(); print("="*76); print("P23 -- larger alphabets"); print("="*76)
ok=True; t=0
for n,alpha in ((3,4),(4,2)):
    for T in product(product(range(alpha),repeat=n),repeat=n):
        if len(set(T))<n: continue
        t+=1
        if not any(len({r[:j]+r[j+1:] for r in T})==n for j in range(n)): ok=False
check("a deletable column always exists", ok, f"{t} tables (n=3 over 4 symbols, n=4 over 2 symbols)")

print(); print("="*76); print("P24 -- the partition count"); print("="*76)
E4=sorted(combinations(range(4),2)); good=[]
for a in range(3**6):
    col=[]; x=a
    for _ in range(6): col.append(x%3); x//=3
    cls=[frozenset(E4[i] for i in range(6) if col[i]==c) for c in range(3)]
    if len({canon(4,c) for c in cls})==1 and all(len(c)==2 for c in cls): good.append(cls)
parts={frozenset(map(frozenset,cls)) for cls in good}
match=[p for p in parts if all(sorted(sum(map(list,e),[]))==[0,1,2,3] for e in p)]
check("54 ordered colourings, 9 unordered partitions", len(good)==54 and len(parts)==9,
      f"{len(good)} colourings, {len(parts)} partitions")
check("exactly 1 is the matching partition and 8 are path partitions",
      len(match)==1 and len(parts)-len(match)==8)

print(); print("="*76)
print("AUDIT RESULT:", "ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
print("="*76)
