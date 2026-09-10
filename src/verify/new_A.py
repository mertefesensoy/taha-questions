# -*- coding: utf-8 -*-
"""Verification, part A: problems 9, 10, 15, 16, 17, 24."""
from itertools import combinations, permutations
from collections import deque
FAIL=[]
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+name+(("  -- "+detail) if detail else ""))
    if not cond: FAIL.append(name)

def graphs(n):
    P=list(combinations(range(n),2))
    for msk in range(1<<len(P)):
        yield frozenset(p for i,p in enumerate(P) if msk>>i&1)
def deg(n,E):
    d=[0]*n
    for a,b in E: d[a]+=1; d[b]+=1
    return d
def canon(n,E):
    return min(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in E)) for p in permutations(range(n)))
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
def has_cycle(n,E): return len(E) > n - ncomp(n,E)

print("="*74); print("PROBLEM 9 -- graphs with no two vertices of equal degree"); print("="*74)
found=[]
for n in range(1,8):
    if n<=6:
        hit=[E for E in graphs(n) if len(set(deg(n,E)))==n]
        found.append((n,len(hit)))
    else:
        found.append((n,"(argument: degrees 0..n-1 all attained -> isolated vertex and universal vertex coexist)"))
for n,k in found: print(f"   n={n}: {k} such graph(s)" if isinstance(k,int) else f"   n={n}: {k}")
check("only n=1 admits all-distinct degrees (checked n<=6 exhaustively)",
      [k for n,k in found if isinstance(k,int)]==[1,0,0,0,0,0], "K_1 is the unique such graph")

print(); print("="*74); print("PROBLEM 10 -- degree sequence 2,2,2,4,5,5 on 6 vertices"); print("="*74)
tgt=sorted([2,2,2,4,5,5])
hit=[E for E in graphs(6) if sorted(deg(6,E))==tgt]
check("no SIMPLE graph on 6 vertices has degree sequence 2,2,2,4,5,5",
      not hit, f"exhaustive over all 2^15 = {2**15} graphs; {len(hit)} found")
def havel(seq):
    s=sorted(seq,reverse=True); steps=[list(s)]
    while True:
        s=sorted([x for x in s if x!=0],reverse=True)
        if not s: return True,steps
        d=s[0]; rest=s[1:]
        if d>len(rest): return False,steps+["(leading %d exceeds the %d remaining entries)"%(d,len(rest))]
        for i in range(d): rest[i]-=1
        if any(x<0 for x in rest): return False,steps+[sorted(rest,reverse=True)]
        s=sorted(rest,reverse=True); steps.append(list(s))
ok,steps=havel([5,5,4,2,2,2])
print("   Havel-Hakimi:", " -> ".join(str(x) for x in steps))
check("Havel-Hakimi also rejects it", not ok)
# a loopless multigraph DOES realise it
from collections import Counter
multi=[('x','y'),('x','d'),('x','d'),('x','a'),('x','b'),('y','d'),('y','d'),('y','c'),('y','a'),('b','c')]
dd=Counter()
for a,b in multi: dd[a]+=1; dd[b]+=1
check("a loopless MULTIgraph does realise 2,2,2,4,5,5",
      sorted(dd.values())==tgt and len(multi)==10, f"degrees {sorted(dd.values())}, {len(multi)} edges")

print(); print("="*74); print("PROBLEM 15 -- all 5-vertex graphs with 2, 8 and 3 edges"); print("="*74)
for m in (2,3,8):
    cl={}
    for E in graphs(5):
        if len(E)==m: cl.setdefault(canon(5,E),E)
    print(f"   n=5, m={m}: {len(cl)} graph(s) up to isomorphism")
    for c,E in sorted(cl.items()):
        d=sorted(deg(5,E),reverse=True)
        print(f"      edges {sorted(tuple(e) for e in E)}   degrees {d}   components {ncomp(5,E)}")
counts={m:len({canon(5,E) for E in graphs(5) if len(E)==m}) for m in (2,3,8)}
check("counts are 2, 4, 2 for m = 2, 3, 8", counts=={2:2,3:4,8:2}, str(counts))
check("m=2 and m=8 counts agree (complementation is a bijection)", counts[2]==counts[8])

print(); print("="*74); print("PROBLEM 16 -- self-complementary graphs"); print("="*74)
for n in (4,5,6,8):
    allp={tuple(sorted(p)) for p in combinations(range(n),2)}
    sc=set()
    if n<=6:
        for E in graphs(n):
            if canon(n,E)==canon(n,frozenset(allp-set(E))): sc.add(canon(n,E))
        print(f"   n={n}: {len(sc)} self-complementary graph(s); n(n-1)/2 = {n*(n-1)//2}"
              f" is {'even' if (n*(n-1)//2)%2==0 else 'ODD -> impossible'}")
    else:
        print(f"   n={n}: n(n-1)/2 = {n*(n-1)//2} is {'even' if (n*(n-1)//2)%2==0 else 'odd'}")
sc5={canon(5,E) for E in graphs(5) if canon(5,E)==canon(5,frozenset({tuple(sorted(p)) for p in combinations(range(5),2)}-set(E)))}
sc6={canon(6,E) for E in graphs(6) if canon(6,E)==canon(6,frozenset({tuple(sorted(p)) for p in combinations(range(6),2)}-set(E)))}
check("there ARE self-complementary graphs on 5 vertices", len(sc5)>0, f"{len(sc5)} of them")
check("there are NONE on 6 vertices", len(sc6)==0, "15 edges total is odd, so |E(G)| = |E(Gbar)| is impossible")
C5=frozenset({(0,1),(1,2),(2,3),(3,4),(0,4)})
allp5={tuple(sorted(p)) for p in combinations(range(5),2)}
check("C_5 is self-complementary", canon(5,C5)==canon(5,frozenset(allp5-set(C5))))

print(); print("="*74); print("PROBLEM 17 -- connected => m >= n-1;  m = n => a cycle"); print("="*74)
a=b=True
for n in range(1,7):
    for E in graphs(n):
        if ncomp(n,E)==1 and len(E)<n-1: a=False
        if len(E)>=n and not has_cycle(n,E): b=False
check("every connected graph has at least n-1 edges", a, "all graphs n <= 6")
check("every graph with n edges contains a cycle", b, "all graphs n <= 6")

print(); print("="*74); print("PROBLEM 24 -- 3-colouring the edges of K4"); print("="*74)
E4=sorted(combinations(range(4),2)); good=[]
for assign in range(3**6):
    col=[]; a=assign
    for _ in range(6): col.append(a%3); a//=3
    cls=[frozenset(E4[i] for i in range(6) if col[i]==c) for c in range(3)]
    cn=[canon(4,c) for c in cls]
    if cn[0]==cn[1]==cn[2]: good.append(cls)
print(f"   {len(good)} of the 3^6 = 729 colourings make all three colour classes isomorphic")
shapes={tuple(sorted(len(c) for c in cls)) for cls in good}
kinds={canon(4,good[0][0])}
for cls in good: kinds.add(canon(4,cls[0]))
check("such a colouring EXISTS", len(good)>0, f"{len(good)} colourings")
check("every solution splits 6 edges as 2+2+2", shapes=={(2,2,2)}, str(shapes))
print(f"   the common shape of a colour class: {len(kinds)} isomorphism type(s)")
for k in kinds:
    E=frozenset(k); print(f"      {sorted(tuple(e) for e in E)}  degrees {sorted(deg(4,E),reverse=True)}"
                          f"  -> {'perfect matching 2K_2' if sorted(deg(4,E))==[1,1,1,1] else 'P_3 + K_1'}")
M=[frozenset({(0,1),(2,3)}), frozenset({(0,2),(1,3)}), frozenset({(0,3),(1,2)})]
check("the three perfect matchings of K4 give such a colouring",
      len(set().union(*M))==6 and len({canon(4,m) for m in M})==1)
print(); print("="*74); print("PART A RESULT:", "ALL PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
