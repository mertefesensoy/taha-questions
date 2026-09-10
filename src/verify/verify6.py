import json, itertools
from itertools import combinations, permutations
G = json.load(open('graphs.json'))
graphs = {k:(v[0], set(map(tuple, map(sorted, v[1])))) for k,v in G.items()}

def circ(n, S):
    E=set()
    for i in range(n):
        for s in S: E.add(tuple(sorted((i,(i+s)%n))))
    return E

print("Identification as circulant graphs:")
for k,(n,E) in graphs.items():
    for S in [(1,2),(1,3),(1,4)]:
        if E == circ(n,S): print(f"  {k} = C_9({S[0]},{S[1]})  |V|={n} |E|={len(E)}")

def tri(n,E):
    return [c for c in combinations(range(n),3)
            if all(tuple(sorted(p)) in E for p in combinations(c,2))]
def c4(n,E):
    cnt=0
    for q in combinations(range(n),4):
        for perm in [(0,1,2,3),(0,1,3,2),(0,2,1,3)]:
            cyc=[q[i] for i in perm]
            if all(tuple(sorted((cyc[i],cyc[(i+1)%4]))) in E for i in range(4)): cnt+=1
    return cnt
def deg(n,E):
    d=[0]*n
    for a,b in E: d[a]+=1; d[b]+=1
    return sorted(d)

print("\nInvariants:")
for k,(n,E) in graphs.items():
    T=tri(n,E)
    print(f"  {k}: |V|={n} |E|={len(E)} degseq={deg(n,E)} triangles={len(T)} C4s={c4(n,E)}")
    print(f"        triangles: {T}")

def iso(A,B):
    nA,EA=A; nB,EB=B
    if nA!=nB or len(EA)!=len(EB) or deg(nA,EA)!=deg(nB,EB): return None
    for p in permutations(range(nA)):
        if all(tuple(sorted((p[a],p[b]))) in EB for a,b in EA): return p
    return None

print("\nBrute-force isomorphism tests (all 9! = 362880 permutations):")
for a,b in combinations(graphs,2):
    p = iso(graphs[a],graphs[b])
    print(f"  {a} vs {b}: {'ISOMORPHIC, phi = '+str(p) if p else 'NOT isomorphic'}")

n=9
print("\nCount of all isomorphisms G1 -> G3 (= |Aut|):")
EA=graphs['G1'][1]; EB=graphs['G3'][1]
alliso=[p for p in permutations(range(n)) if all(tuple(sorted((p[a],p[b]))) in EB for a,b in EA)]
print(f"  {len(alliso)} isomorphisms; e.g. {alliso[0]}")
mult4 = tuple((4*i)%9 for i in range(9))
print(f"  is phi(i)=4i mod 9 = {mult4} among them? {mult4 in alliso}")
# verify mult-by-4 map explicitly edge by edge
print("\n  Explicit check of phi(i) = 4i mod 9 : C_9(1,2) -> C_9(1,4)")
ok=True
for a,b in sorted(EA):
    img=tuple(sorted((mult4[a],mult4[b])))
    d=min((img[1]-img[0])%9,(img[0]-img[1])%9)
    good = img in EB
    ok &= good
    print(f"    {{{a},{b}}} (dist {min((b-a)%9,(a-b)%9)}) -> {{{img[0]},{img[1]}}} (dist {d})  in G3: {good}")
print("  all 18 edges map to edges:", ok, "| bijection + |E| equal => isomorphism")

# complement check
allpairs=set(tuple(sorted(p)) for p in combinations(range(9),2))
comp1 = allpairs-EA
print("\nComplement of G1 vs G2:", "isomorphic" if iso((9,comp1),graphs['G2']) else "not isomorphic")
