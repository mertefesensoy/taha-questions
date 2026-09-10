# -*- coding: utf-8 -*-
"""Verification, part D: problem 26 (integer-sided tiling) and problem 24's second solution."""
from fractions import Fraction as F
from itertools import combinations, permutations
import random
FAIL=[]
def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ")+name+(("  -- "+detail) if detail else ""))
    if not cond: FAIL.append(name)

print("="*74); print("PROBLEM 26 -- tiling by rectangles each with an integer side"); print("="*74)
def corners(r):
    (a,c),(b,d)=r
    return [(a,c),(b,c),(a,d),(b,d)]
def integral(p): return p[0].denominator==1 and p[1].denominator==1
def int_side(r):
    (a,c),(b,d)=r
    return (b-a).denominator==1 or (d-c).denominator==1

def gen(rect, depth, out, rng):
    """Guillotine-split, always cutting so that BOTH parts keep an integer side."""
    (a,c),(b,d)=rect
    if depth==0 or rng.random()<0.3: out.append(rect); return
    w,h = b-a, d-c
    cuts=[]
    if h.denominator==1 and w>1:               # integer height: any vertical cut keeps it
        x=a+F(rng.randint(1,4),rng.randint(1,4)+4)*w
        if a<x<b: cuts.append((( (a,c),(x,d) ), ( (x,c),(b,d) )))
    if w.denominator==1 and h>1:               # integer width: any horizontal cut keeps it
        y=c+F(rng.randint(1,4),rng.randint(1,4)+4)*h
        if c<y<d: cuts.append((( (a,c),(b,y) ), ( (a,y),(b,d) )))
    if int(w)>=2:                              # integer-width cut
        k=F(rng.randint(1,int(w)-1)); cuts.append((( (a,c),(a+k,d) ), ( (a+k,c),(b,d) )))
    if int(h)>=2:
        k=F(rng.randint(1,int(h)-1)); cuts.append((( (a,c),(b,c+k) ), ( (a,c+k),(b,d) )))
    cuts=[c2 for c2 in cuts if int_side(c2[0]) and int_side(c2[1])]
    if not cuts: out.append(rect); return
    p,q=rng.choice(cuts)
    gen(p,depth-1,out,rng); gen(q,depth-1,out,rng)

rng=random.Random(20)
ok_even=ok_thm=True; tested=0; sizes=[]
for _ in range(3000):
    w=F(rng.randint(2,7)); h=F(rng.randint(2,7))
    if rng.random()<0.5: w+=F(1,2)            # make the container non-integer in one side sometimes
    if rng.random()<0.5: h+=F(1,3)
    R=((F(0),F(0)),(w,h))
    if not int_side(R): continue              # generator needs a valid seed
    out=[]; gen(R,6,out,rng)
    if not all(int_side(r) for r in out): continue
    tested+=1; sizes.append(len(out))
    for r in out:
        if sum(1 for p in corners(r) if integral(p))%2: ok_even=False
    if not (w.denominator==1 or h.denominator==1): ok_thm=False
check("every tile with an integer side has an EVEN number of integral corners", ok_even,
      f"{tested} random tilings, up to {max(sizes) if sizes else 0} tiles each")
check("no tiling by integer-sided tiles has a container with two non-integer sides", ok_thm,
      f"{tested} random tilings")

print("\n   -- the parity bookkeeping, checked directly --")
for w,h,exp in [(F(3),F(5),4),(F(3),F(5,2),2),(F(5,2),F(3),2),(F(3,2),F(5,2),1)]:
    cs=[(F(0),F(0)),(w,F(0)),(F(0),h),(w,h)]
    got=sum(1 for p in cs if integral(p))
    check(f"container {w} x {h}: {exp} integral corner(s)", got==exp, f"got {got}")
print("   => a container with NO integer side has exactly 1 integral corner, an ODD number")

print("\n   -- t(p) = number of tiles having p as a corner, checked on random tilings --")
def tcount(tiles, p):
    return sum(1 for r in tiles if p in corners(r))
rng=random.Random(77); ok_t=True; checked=0
for _ in range(400):
    w=F(rng.randint(3,6)); h=F(rng.randint(3,6))
    out=[]; gen(((F(0),F(0)),(w,h)),5,out,rng)
    if not all(int_side(r) for r in out): continue
    pts={p for r in out for p in corners(r)}
    Tcorners={(F(0),F(0)),(w,F(0)),(F(0),h),(w,h)}
    for p in pts:
        t=tcount(out,p); checked+=1
        if p in Tcorners:
            if t!=1: ok_t=False
        elif t%2: ok_t=False
check("t(p) = 1 at each corner of the container, and even at every other corner point", ok_t,
      f"{checked} corner points across random tilings")

print(); print("="*74); print("PROBLEM 24 -- the second, path-type solution"); print("="*74)
def canon4(E):
    return min(tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in E)) for p in permutations(range(4)))
A=frozenset({(0,1),(1,2)}); B=frozenset({(0,2),(2,3)}); C=frozenset({(0,3),(1,3)})
E4=set(combinations(range(4),2))
check("{01,12} u {02,23} u {03,13} partitions the 6 edges of K4",
      A|B|C==E4 and len(A)+len(B)+len(C)==6)
check("all three classes are isomorphic (each a path P_3 plus an isolated vertex)",
      canon4(A)==canon4(B)==canon4(C), "P_3 + K_1")
M=[frozenset({(0,1),(2,3)}),frozenset({(0,2),(1,3)}),frozenset({(0,3),(1,2)})]
check("the perfect-matching solution also works",
      set().union(*M)==E4 and len({canon4(m) for m in M})==1, "2K_2")
# how many unordered partitions of each type?
cnt={}
for assign in range(3**6):
    col=[]; a=assign; Es=sorted(E4)
    for _ in range(6): col.append(a%3); a//=3
    cls=[frozenset(Es[i] for i in range(6) if col[i]==c) for c in range(3)]
    if len({canon4(c) for c in cls})==1 and all(len(c)==2 for c in cls):
        cnt[canon4(cls[0])]=cnt.get(canon4(cls[0]),0)+1
for k,v in cnt.items():
    E=frozenset(k); typ="2K_2 (perfect matching)" if sorted(sum(([a,b] for a,b in E),[]))==[0,1,2,3] else "P_3 + K_1"
    print(f"   colour-class type {typ}: {v} ordered colourings = {v//6} unordered partitions")
print(); print("="*74); print("PART D RESULT:", "ALL PASSED" if not FAIL else f"{len(FAIL)} FAILURE(S): {FAIL}")
