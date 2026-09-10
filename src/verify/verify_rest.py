from itertools import combinations
# ---------- Problem 1 extra: characterise reachable set exactly ----------
from collections import deque
coord={s:((s-1)//3,(s-1)%3) for s in range(1,10)}
adj={s:[b for b in range(1,10) if b!=s and sorted((abs(coord[s][0]-coord[b][0]),abs(coord[s][1]-coord[b][1])))==[1,2]] for s in range(1,10)}
cycle=[1,6,7,2,9,4,3,8]; idx={v:i for i,v in enumerate(cycle)}
def norm(W,D): return (tuple(sorted(W)),tuple(sorted(D)))
def pattern(st):
    W,D=st; lab={}
    for c in W: lab[c]='W'
    for c in D: lab[c]='D'
    occ=sorted(lab,key=lambda s:idx[s])
    w=''.join(lab[s] for s in occ)
    return min(w[i:]+w[:i] for i in range(4))   # canonical necklace
start=norm((1,9),(3,7)); seen={start}; q=deque([start])
while q:
    W,D=q.popleft(); occ=set(W)|set(D); pieces=list(W)+list(D)
    for k in range(4):
        for nx in adj[pieces[k]]:
            if nx in occ: continue
            np_=pieces[:]; np_[k]=nx
            ns=norm(tuple(np_[:2]),tuple(np_[2:]))
            if ns not in seen: seen.add(ns); q.append(ns)
allst=set()
for pos in combinations(cycle,4):
    for W in combinations(pos,2):
        D=tuple(x for x in pos if x not in W); allst.add(norm(W,D))
alt={s for s in allst if pattern(s)=='DWDW'}
print("P1: start pattern =",pattern(start))
print("   all placements:",len(allst),"| alternating-pattern placements:",len(alt),"| reachable:",len(seen))
print("   reachable == exactly the alternating ones:", seen==alt)

# ---------- Problem 2 ----------
def graphical_bruteforce(seq):
    n=len(seq); pairs=list(combinations(range(n),2))
    for r in range(len(pairs)+1):
        if 2*r != sum(seq): continue
        for E in combinations(pairs,r):
            d=[0]*n
            for a,b in E: d[a]+=1; d[b]+=1
            if sorted(d)==sorted(seq): return E
    return None
def havel(seq):
    s=sorted(seq,reverse=True); steps=[list(s)]
    while True:
        s=[x for x in s if x>0] if all(x>=0 for x in s) else s
        s=sorted(s,reverse=True)
        if not s: return True,steps
        if s[0]<0 or s[0]>len(s)-1: return False,steps
        d=s[0]; rest=s[1:]
        for i in range(d): rest[i]-=1
        if any(x<0 for x in rest): return False,steps
        s=sorted(rest,reverse=True); steps.append(list(s))
        if all(x==0 for x in s): return True,steps
for name,seq in [('a',[1,2,2,3,3,3]),('b',[1,1,2,2,3,4,4])]:
    ok,steps=havel(seq)
    print(f"\nP2({name}): seq={seq} sum={sum(seq)} ({'even' if sum(seq)%2==0 else 'ODD -> impossible'})")
    print("   Havel-Hakimi:", " -> ".join(str(s) for s in steps), "=>", "GRAPHICAL" if ok else "not graphical")
    if sum(seq)%2==0:
        E=graphical_bruteforce(seq)
        print("   brute-force realisation:", E)
# Erdos-Gallai check for (a)
seq=sorted([1,2,2,3,3,3],reverse=True); n=len(seq)
print("\nP2(a) Erdos-Gallai:")
for k in range(1,n+1):
    lhs=sum(seq[:k]); rhs=k*(k-1)+sum(min(d,k) for d in seq[k:])
    print(f"   k={k}: sum_top={lhs} <= {rhs} ? {lhs<=rhs}")

# ---------- Problem 8 ----------
n_special=3
print("\nP8: 22*n = 22*(n-3) + 12 + 12 + x  =>  x = 22*3 - 24 =", 22*3-24)
# explicit realisation attempt for smallest n
def build(n):
    # want outdeg 22 for all, indeg: v0=12, v1=12, v2=42, rest 22
    indeg=[12,12,42]+[22]*(n-3)
    if sum(indeg)!=22*n: return None
    # greedy Kleitman-Wang style: repeatedly pick vertex with largest outdeg remaining
    out=[22]*n; A=[[0]*n for _ in range(n)]
    order=sorted(range(n), key=lambda v:-out[v])
    for u in range(n):
        need=out[u]
        cand=sorted([v for v in range(n) if v!=u], key=lambda v:-indeg[v])[:need]
        if len(cand)<need or indeg[cand[-1]]<=0: return None
        for v in cand:
            A[u][v]=1; indeg[v]-=1
        out[u]=0
    if any(x!=0 for x in indeg): return None
    return A
for n in [43,45,50]:
    A=build(n)
    if A:
        od=[sum(r) for r in A]; ind=[sum(A[i][j] for i in range(n)) for j in range(n)]
        from collections import Counter
        print(f"   n={n}: constructed digraph -> outdeg set {set(od)}, indeg multiset {sorted(Counter(ind).items())}, loops={sum(A[i][i] for i in range(n))}")
    else:
        print(f"   n={n}: greedy construction failed")
