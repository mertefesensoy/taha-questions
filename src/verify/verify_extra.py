from collections import deque
from itertools import combinations
# --- Guarini's classical puzzle: W on 1,3 (top corners), D on 7,9 -> swap
coord={s:((s-1)//3,(s-1)%3) for s in range(1,10)}
adj={s:[b for b in range(1,10) if b!=s and sorted((abs(coord[s][0]-coord[b][0]),abs(coord[s][1]-coord[b][1])))==[1,2]] for s in range(1,10)}
def norm(W,D): return (tuple(sorted(W)),tuple(sorted(D)))
def bfs(start):
    seen={start}; par={start:None}; q=deque([start])
    while q:
        W,D=q.popleft(); occ=set(W)|set(D); pieces=list(W)+list(D)
        for k in range(4):
            for nx in adj[pieces[k]]:
                if nx in occ: continue
                np_=pieces[:]; np_[k]=nx
                ns=norm(tuple(np_[:2]),tuple(np_[2:]))
                if ns not in seen: seen.add(ns); par[ns]=(W,D); q.append(ns)
    return seen,par
start=norm((1,3),(7,9)); goal=norm((7,9),(1,3))
seen,par=bfs(start)
print("Guarini (W on 1,3 <-> D on 7,9): solvable?", goal in seen)
if goal in seen:
    path=[]; cur=goal
    while cur: path.append(cur); cur=par[cur]
    print("   shortest solution length:", len(path)-1, "moves")

# --- P2 remark: repair parity of (b)
def havel(seq):
    s=sorted(seq,reverse=True)
    while True:
        s=sorted([x for x in s if x>0],reverse=True)
        if not s: return True
        d=s[0]
        if d>len(s)-1: return False
        rest=s[1:]
        for i in range(d): rest[i]-=1
        if any(x<0 for x in rest): return False
        s=rest
for sq in [[1,1,2,2,2,4,4],[1,1,2,2,4,4,4],[1,1,2,2,3,4,5]]:
    print(f"P2 remark: {sq} sum={sum(sq)} graphical={havel(sq) if sum(sq)%2==0 else 'N/A (odd sum)'}")

# --- P3: number of 2-regular graphs on n vertices = partitions of n into parts >= 3
def parts_ge3(n, mn=3):
    if n==0: return [[]]
    out=[]
    for k in range(mn, n+1):
        for rest in parts_ge3(n-k, k):
            out.append([k]+rest)
    return out
for n in range(3,13):
    P=parts_ge3(n)
    print(f"P3: n={n}: {len(P)} two-regular graph(s):", ", ".join("+".join("C%d"%x for x in p) for p in P))

# --- P7 sharpness for odd n
def check(n):
    a=n//2; b=n-a
    return f"K_{a} + K_{b}: degrees {a-1} and {b-1}, delta={min(a,b)-1}, floor(n/2)={n//2}"
for n in [8,9,10,11]: print("P7:", f"n={n}:", check(n))
