from collections import deque, Counter
class Dinic:
    def __init__(s,n): s.n=n; s.g=[[] for _ in range(n)]
    def add(s,u,v,c):
        s.g[u].append([v,c,len(s.g[v])]); s.g[v].append([u,0,len(s.g[u])-1])
    def bfs(s,S,T):
        s.lv=[-1]*s.n; s.lv[S]=0; q=deque([S])
        while q:
            u=q.popleft()
            for e in s.g[u]:
                if e[1]>0 and s.lv[e[0]]<0: s.lv[e[0]]=s.lv[u]+1; q.append(e[0])
        return s.lv[T]>=0
    def dfs(s,u,T,f):
        if u==T: return f
        while s.it[u]<len(s.g[u]):
            e=s.g[u][s.it[u]]
            if e[1]>0 and s.lv[e[0]]==s.lv[u]+1:
                d=s.dfs(e[0],T,min(f,e[1]))
                if d>0: e[1]-=d; s.g[e[0]][e[2]][1]+=d; return d
            s.it[u]+=1
        return 0
    def maxflow(s,S,T):
        fl=0
        while s.bfs(S,T):
            s.it=[0]*s.n
            while True:
                f=s.dfs(S,T,10**9)
                if f==0: break
                fl+=f
        return fl

def realise(n, outdeg, indeg):
    S=2*n; T=2*n+1; D=Dinic(2*n+2)
    for u in range(n): D.add(S,u,outdeg[u])
    for v in range(n): D.add(n+v,T,indeg[v])
    ref={}
    for u in range(n):
        for v in range(n):
            if u!=v: ref[(u,v)]=len(D.g[u]); D.add(u,n+v,1)
    f=D.maxflow(S,T)
    if f!=sum(outdeg): return None,f
    A=[[0]*n for _ in range(n)]
    for (u,v),i in ref.items():
        if D.g[u][i][1]==0: A[u][v]=1
    return A,f

import sys
sys.setrecursionlimit(10000)
for n in [42,43,44,60]:
    outdeg=[22]*n
    indeg=[12,12,42]+[22]*(n-3)
    if 42>n-1 or 22>n-1:
        print(f"n={n}: impossible on degree-bound grounds (need indeg 42 <= n-1, so n >= 43)"); continue
    if sum(outdeg)!=sum(indeg): print(f"n={n}: sums differ"); continue
    A,f=realise(n,outdeg,indeg)
    if A is None:
        print(f"n={n}: NOT realisable (maxflow {f} < {sum(outdeg)})")
    else:
        od=[sum(r) for r in A]; ind=[sum(A[i][j] for i in range(n)) for j in range(n)]
        print(f"n={n}: realisable. arcs={sum(od)}, outdeg set={set(od)}, indeg multiset={sorted(Counter(ind).items())}, loops={sum(A[i][i] for i in range(n))}")
