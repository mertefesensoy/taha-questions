# -*- coding: utf-8 -*-
"""Tables for the second solution document."""
from tables import T, M

def t_hh10():
    seq=[5,5,4,2,2,2]; rows=[]; s=sorted(seq,reverse=True); k=1
    while True:
        d=s[0]; rest=s[1:]
        if d>len(rest):
            rows.append([k, M("("+", ".join(map(str,s))+")"),
                         f"the leading {d} needs {d} further vertices, but only {len(rest)} remain",
                         "<strong>not graphical &#10007;</strong>"])
            break
        new=[rest[i]-1 if i<d else rest[i] for i in range(len(rest))]
        rows.append([k, M("("+", ".join(map(str,s))+")"),
                     f"delete the leading {d}; subtract 1 from the next {d} entries",
                     M("("+", ".join(map(str,sorted(new,reverse=True)))+")")])
        s=sorted([x for x in new if x!=0],reverse=True); k+=1
        if not s: break
    return T(["round","current sequence","operation","reduced sequence"], rows,
             "Table 10.1 &mdash; the Havel&ndash;Hakimi reduction of 5,&thinsp;5,&thinsp;4,&thinsp;2,&thinsp;2,"
             "&thinsp;2 breaks down, confirming that the sequence is not graphical.", cls="wide", lc=(2,))

def t_answers():
    rows=[
     ["9","All degrees distinct","only <em>K</em><sub>1</sub>"],
     ["10","Degree sequence 2,2,2,4,5,5","no simple graph realises it"],
     ["11","11 vertices, 45 edges","some degree &ge; 9"],
     ["12","Cycle-avoiding game","first player wins &hArr; <em>n</em> even"],
     ["13","100 vertices, one of degree 66","connected"],
     ["14","10 deletions, 33 additions","<strong>42 edges</strong>"],
     ["15","5-vertex graphs, <em>m</em> = 2 / 8 / 3","<strong>2 / 2 / 4</strong> graphs"],
     ["16","Self-complementary","yes for <em>n</em> = 5, no for <em>n</em> = 6"],
     ["17","Connectivity and cycles","<em>m</em> &ge; <em>n</em>&minus;1;  <em>m</em> = <em>n</em> &rArr; a cycle"],
     ["18","Add 1 edge, delete 2","impossible (41 &gt; 24)"],
     ["19","Delete 1 edge, add 2","impossible (31 &gt; 10)"],
     ["20","2<em>k</em> vertices, &delta; &ge; <em>k</em>&minus;1","connected"],
     ["&#9733;","123 edges, three colours","<strong>42 vertices</strong>"],
     ["21","Acyclic orientation","order the vertices, orient upward"],
     ["22","Three edges, three cuts","<em>G</em>&minus;<em>e</em>&minus;<em>f</em> is disconnected"],
     ["23","Deleting a column","always possible"],
     ["24","Colouring <em>K</em><sub>4</sub>","yes &mdash; matchings, or paths"],
     ["25","Thirteen people","true, and 13 is sharp"],
     ["26","Tiling a rectangle","<em>T</em> has an integer side"],
    ]
    return T(["#","problem","answer"], rows,
             "Table B.1 &mdash; the nineteen answers at a glance.", cls="wide", lc=(1,2))

TBL2={'HH10': t_hh10, 'ANSWERS': t_answers}
