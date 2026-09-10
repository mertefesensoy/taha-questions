# -*- coding: utf-8 -*-
"""Re-read the three drawings from the image with different parameters than the
original detector, and report the SEPARATION between edges and non-edges."""
from PIL import Image
from itertools import combinations
from collections import deque
import math
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = next((p for p in (os.path.join(_HERE, "..", "..", "problem-set.jpg"),
                          "/root/.claude/uploads/64ad73c0-31f2-5c61-a3f4-35a349eafe52/fce6c035-image.jpg")
              if os.path.exists(p)), None)


im = Image.open(IMAGE).convert('L')
px = im.load()
BOX = {'G1': (250,485,520,770), 'G2': (535,485,800,770), 'G3': (810,485,1080,770)}

def vertices(box, thr):
    """Vertex disks = light regions enclosed by ink; measured, never guessed."""
    x0,y0,x1,y1 = box; w,h = x1-x0, y1-y0
    dark = [[px[x0+i, y0+j] < thr for i in range(w)] for j in range(h)]
    seen = [[False]*w for _ in range(h)]; holes = []
    for j in range(h):
        for i in range(w):
            if not dark[j][i] and not seen[j][i]:
                q=deque([(i,j)]); seen[j][i]=True; cells=[]; touch=False
                while q:
                    a,b=q.popleft(); cells.append((a,b))
                    if a in (0,w-1) or b in (0,h-1): touch=True
                    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                        na,nb=a+da,b+db
                        if 0<=na<w and 0<=nb<h and not dark[nb][na] and not seen[nb][na]:
                            seen[nb][na]=True; q.append((na,nb))
                if not touch: holes.append(cells)
    cands=[]
    for cells in holes:
        xs=[c[0] for c in cells]; ys=[c[1] for c in cells]
        bw=max(xs)-min(xs)+1; bh=max(ys)-min(ys)+1; a=len(cells)
        if 90 <= a <= 420 and a/(bw*bh) > 0.62 and 0.7 < bw/bh < 1.45:
            cands.append((sum(xs)/a, sum(ys)/a))
    cx=sum(c[0] for c in cands)/len(cands); cy=sum(c[1] for c in cands)/len(cands)
    rmax=max(math.hypot(c[0]-cx,c[1]-cy) for c in cands)
    keep=[c for c in cands if math.hypot(c[0]-cx,c[1]-cy) > 0.6*rmax]
    cx=sum(c[0] for c in keep)/len(keep); cy=sum(c[1] for c in keep)/len(keep)
    keep.sort(key=lambda c: math.atan2(c[1]-cy, c[0]-cx))          # clockwise, y down
    s=min(range(len(keep)), key=lambda i: keep[i][1])              # start at the top vertex
    return [keep[(s+i)%len(keep)] for i in range(len(keep))], dark, w, h, (cx,cy,rmax)

def darkfrac(dark,w,h,p,q,thr_skip):
    (ax,ay),(bx,by)=p,q; L=math.hypot(bx-ax,by-ay); n=int(L*4); hit=tot=0
    for k in range(n+1):
        t=k/n; x=ax+(bx-ax)*t; y=ay+(by-ay)*t
        if math.hypot(x-ax,y-ay)<thr_skip or math.hypot(x-bx,y-by)<thr_skip: continue
        tot+=1
        if any(0<=int(round(x))+dx<w and 0<=int(round(y))+dy<h and dark[int(round(y))+dy][int(round(x))+dx]
               for dx in (-1,0,1) for dy in (-1,0,1)): hit+=1
    return hit/tot if tot else 0.0

def circ(S): return {tuple(sorted((i,(i+s)%9))) for i in range(9) for s in S}

if __name__ == "__main__":
    print("Re-reading the three drawings: ink threshold 120 (was 140), 4x sampling (was 3x),")
    print("vertex-disk area window 90-420 px (was 100-400). Vertex centres are measured.\n")
    ok = True
    for name, S in [('G1',(1,2)), ('G2',(1,3)), ('G3',(1,4))]:
        V, dark, w, h, geo = vertices(BOX[name], 120)
        scores = {}
        for i, j in combinations(range(9), 2):
            scores[(i,j)] = darkfrac(dark, w, h, V[i], V[j], 14)
        E = {p for p, s in scores.items() if s > 0.97}
        want = circ(S)
        lo_edge  = min(scores[p] for p in want)                 # weakest edge
        hi_nonedge = max(s for p, s in scores.items() if p not in want)   # strongest non-edge
        match = (E == want)
        ok &= match
        print(f"{name}: {len(V)} vertices found, centre=({geo[0]:.1f},{geo[1]:.1f}) r={geo[2]:.1f}")
        print(f"    edges read: {len(E)};  matches C_9{S}: {match}")
        print(f"    weakest true edge scores {lo_edge:.3f};  strongest non-edge scores {hi_nonedge:.3f}"
              f";  separation gap = {lo_edge - hi_nonedge:.3f}")
        if not match:
            print("    differences:", sorted(E ^ want))
    print("\nRESULT:", "all three drawings re-read identically" if ok else "MISMATCH -- investigate")
