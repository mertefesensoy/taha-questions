from collections import deque
from itertools import permutations
# squares 1..9 laid out  1 2 3 / 4 5 6 / 7 8 9
coord = {s: ((s-1)//3, (s-1)%3) for s in range(1,10)}
adj = {s: [] for s in range(1,10)}
for a in range(1,10):
    for b in range(1,10):
        if a==b: continue
        (r1,c1),(r2,c2)=coord[a],coord[b]
        if sorted((abs(r1-r2),abs(c1-c2)))==[1,2]: adj[a].append(b)
print("Knight-move graph of the 3x3 board:")
for s in range(1,10): print(f"   square {s}: neighbours {sorted(adj[s])}  (degree {len(adj[s])})")

# confirm the 8 non-central squares form a single cycle
non = [s for s in range(1,10) if adj[s]]
print("\n squares with at least one move:", non, " -> all have degree 2:", all(len(adj[s])==2 for s in non))
cyc=[1]; prev=None; cur=1
while True:
    nxt=[x for x in adj[cur] if x!=prev][0]
    if nxt==1: break
    cyc.append(nxt); prev,cur=cur,nxt
print(" the cycle:", " - ".join(map(str,cyc)), "- 1   (length %d)"%len(cyc))

# exhaustive BFS over states. state = (posW1,posW2,posD1,posD2) as frozenset pairs
CORNERS=(1,3,7,9)
def norm(st):
    W,D = st
    return (tuple(sorted(W)), tuple(sorted(D)))
start = norm(((1,9),(3,7)))     # white on 1,9 ; dark on 3,7  (same colours diametrically opposite)
seen={start}; q=deque([start]); parent={start:None}
while q:
    (W,D)=q.popleft()
    occ=set(W)|set(D)
    for who in range(4):
        pieces=list(W)+list(D)
        p=pieces[who]
        for nx in adj[p]:
            if nx in occ: continue
            np_=pieces[:]; np_[who]=nx
            ns=norm((tuple(np_[:2]),tuple(np_[2:])))
            if ns not in seen:
                seen.add(ns); parent[ns]=(W,D); q.append(ns)
print(f"\n total reachable states from the start position: {len(seen)}")
final=[s for s in seen if set(s[0])|set(s[1])==set(CORNERS)]
print(f" reachable states with all four knights on corners: {len(final)}")
for s in sorted(final):
    lab={}
    for c in s[0]: lab[c]='W'
    for c in s[1]: lab[c]='D'
    opp = "same" if lab[1]==lab[9] and lab[3]==lab[7] else ("mixed" if (lab[1]!=lab[9])!=(lab[3]!=lab[7]) else "different")
    print(f"   1={lab[1]} 3={lab[3]} 7={lab[7]} 9={lab[9]}   diagonal pairs (1,9),(3,7): {opp}")
target_ok=any((({s[0][0],s[0][1]}=={1,3} or {s[0][0],s[0][1]}=={3,9} or {s[0][0],s[0][1]}=={9,7} or {s[0][0],s[0][1]}=={7,1})) for s in final)
print("\n Is ANY corner position with diametrically opposite knights of DIFFERENT colour reachable?", target_ok)
# also count total states of 4 knights on the 8-cycle to show reachable fraction
tot=0
for W in permutations(non,2):
    for D in permutations([x for x in non if x not in W],2):
        tot+=1
tot//=4
print(f" (out of {tot} conceivable placements of the 4 knights on the 8 usable squares)")
