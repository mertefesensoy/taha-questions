from PIL import Image
import math
from collections import deque
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = next((p for p in (os.path.join(_HERE, "..", "..", "problem-set.jpg"),
                          "/root/.claude/uploads/64ad73c0-31f2-5c61-a3f4-35a349eafe52/fce6c035-image.jpg")
              if os.path.exists(p)), None)


im = Image.open(IMAGE).convert('L')
px = im.load()
regions = {'G1':(250,485,520,770), 'G2':(535,485,800,770), 'G3':(810,485,1080,770)}
THRESH = 140

def holes(box):
    x0,y0,x1,y1 = box; w,h = x1-x0, y1-y0
    dark = [[px[x0+i,y0+j] < THRESH for i in range(w)] for j in range(h)]
    seen=[[False]*w for _ in range(h)]; out=[]
    for j in range(h):
        for i in range(w):
            if not dark[j][i] and not seen[j][i]:
                q=deque([(i,j)]); seen[j][i]=True; cells=[]; touch=False
                while q:
                    a,b=q.popleft(); cells.append((a,b))
                    if a in(0,w-1) or b in(0,h-1): touch=True
                    for da,db in((1,0),(-1,0),(0,1),(0,-1)):
                        na,nb=a+da,b+db
                        if 0<=na<w and 0<=nb<h and not dark[nb][na] and not seen[nb][na]:
                            seen[nb][na]=True; q.append((na,nb))
                if not touch: out.append(cells)
    return out, dark, w, h

def vertices(box):
    comps, dark, w, h = holes(box)
    cands=[]
    for cells in comps:
        xs=[c[0] for c in cells]; ys=[c[1] for c in cells]
        bw=max(xs)-min(xs)+1; bh=max(ys)-min(ys)+1; area=len(cells)
        if not (100<=area<=400): continue
        if area/(bw*bh) < 0.6: continue
        if not (0.7 < bw/bh < 1.45): continue
        cands.append((sum(xs)/area, sum(ys)/area, area))
    cx = sum(c[0] for c in cands)/len(cands); cy = sum(c[1] for c in cands)/len(cands)
    rad = sorted(math.hypot(c[0]-cx,c[1]-cy) for c in cands)
    rmax = rad[-1]
    keep=[c for c in cands if math.hypot(c[0]-cx,c[1]-cy) > 0.6*rmax]
    cx = sum(c[0] for c in keep)/len(keep); cy = sum(c[1] for c in keep)/len(keep)
    keep.sort(key=lambda c: math.atan2(c[1]-cy, c[0]-cx))
    return keep, dark, w, h, (cx,cy)

def darkness_along(dark,w,h,p,q,skip=13):
    (ax,ay),(bx,by)=p,q
    L=math.hypot(bx-ax,by-ay); n=int(L*3)
    hits=0; tot=0
    for k in range(n+1):
        t=k/n; x=ax+(bx-ax)*t; y=ay+(by-ay)*t
        if math.hypot(x-ax,y-ay)<skip or math.hypot(x-bx,y-by)<skip: continue
        tot+=1
        ok=False
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                xi,yi=int(round(x))+dx,int(round(y))+dy
                if 0<=xi<w and 0<=yi<h and dark[yi][xi]: ok=True
        if ok: hits+=1
    return hits/tot if tot else 0

results={}
for name,box in regions.items():
    V, dark, w, h, ctr = vertices(box)
    n=len(V)
    # order by angle starting from topmost
    start=min(range(n), key=lambda i: V[i][1])
    order=[V[(start+i)%n] for i in range(n)]
    print(f"\n=== {name}: n={n} vertices (cyclic order, 0 = top) ===")
    for i,v in enumerate(order): print(f"   v{i}: ({v[0]:.1f},{v[1]:.1f})")
    edges=[]; scores={}
    for i in range(n):
        for j in range(i+1,n):
            s=darkness_along(dark,w,h,(order[i][0],order[i][1]),(order[j][0],order[j][1]))
            scores[(i,j)]=s
            if s>0.97: edges.append((i,j))
    print(f"   edges found: {len(edges)}")
    deg=[0]*n
    for i,j in edges: deg[i]+=1; deg[j]+=1
    print(f"   degrees: {deg}")
    diffs={}
    for i,j in edges:
        d=min((j-i)%n,(i-j)%n); diffs[d]=diffs.get(d,0)+1
    print(f"   circular differences: {dict(sorted(diffs.items()))}")
    print("   edge list:", edges)
    borderline=[(k,round(v,3)) for k,v in scores.items() if 0.80<v<=0.97]
    print("   borderline (0.80-0.97):", borderline)
    results[name]=(n,edges)
import json
json.dump({k:(v[0],v[1]) for k,v in results.items()}, open('graphs.json','w'))
