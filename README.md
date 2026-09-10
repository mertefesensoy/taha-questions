# taha-questions

Worked solutions to the FCS Practice Session 1 graph theory sheet — all 26 problems, plus the
starred bonus problem.

| Deliverable | Covers | Pages |
|---|---|---|
| **[`graph-theory-solutions.pdf`](graph-theory-solutions.pdf)** | Problems 1–8 | 19 |
| **[`graph-theory-solutions-2.pdf`](graph-theory-solutions-2.pdf)** | Problems 9–26 and the starred problem | 27 |

Both are self-contained: full proofs, explicit constructions, diagrams, and data tables. Every
problem is solved by graph-theoretic means; where a problem is not posed in the language of graphs
— a chess puzzle, a pencil-and-paper game, a table of numbers, a party, a tiled rectangle — the
first step is a reduction, replacing the object by a graph whose structure answers the question.

The original sheet is kept here as [`practice-session-1.pdf`](practice-session-1.pdf), and the photo
of problems 1–8 as [`problem-set.jpg`](problem-set.jpg).

## Answers

### Volume 1 — problems 1–8

| # | Problem | Answer |
|---|---------|--------|
| 1 | Knights on a 3×3 board | **No** — the usable squares form one 8-cycle, and the knights' cyclic order is invariant |
| 2 | Degree sequences 1,2,2,3,3,3 and 1,1,2,2,3,4,4 | **(a) yes**; **(b) no** — the entries sum to 17, which is odd |
| 3 | 2-regular graphs; Δ(G) ≤ 2 | disjoint unions of **cycles**; of **paths and cycles** |
| 4 | Odd-degree vertices | even in number; the **ray** is an infinite counterexample |
| 5 | An odd vertex reaches another | apply the parity count to u's **component** |
| 6 | Which of three drawings are isomorphic | **1st ≅ 3rd** via φ(i)=4i mod 9; the **2nd is neither** (3 triangles vs 9) |
| 7 | d(v) ≥ n/2 ⟹ connected | proved twice; in fact **diam ≤ 2**, and the bound is sharp |
| 8 | Directed degree count | **42** |

### Volume 2 — problems 9–26 and ★

| # | Problem | Answer |
|---|---------|--------|
| 9 | All degrees distinct | only **K₁** |
| 10 | Degree sequence 2,2,2,4,5,5 | no **simple** graph realises it |
| 11 | 11 vertices, 45 edges | some degree **≥ 9** (and 9 is attained) |
| 12 | Cycle-avoiding game | **first player wins ⟺ n is even** |
| 13 | 100 vertices, one of degree 66 | **connected** (67 + 34 > 100) |
| 14 | 10 deletions, 33 additions | **42 edges** |
| 15 | 5-vertex graphs with m = 2 / 8 / 3 | **2 / 2 / 4** graphs, all listed |
| 16 | Self-complementary graphs | **yes** for n = 5 (C₅ and the bull); **no** for n = 6 |
| 17 | Connectivity and cycles | m ≥ n−1; and m = n forces a cycle |
| 18 | Add one edge, delete two | **impossible** (needs ≥ 41 steps, affords ≤ 24) |
| 19 | Delete one edge, add two | **impossible** (needs ≥ 31 steps, affords ≤ 10) |
| 20 | 2k vertices, δ ≥ k−1, one of degree k | **connected** |
| ★ | 123 edges, three connected colour classes | at most **42 vertices**, and 42 is attained |
| 21 | Acyclic orientation | order the vertices, orient each edge upward |
| 22 | Three edges, three cuts | **G−e−f is disconnected** (the printed conclusion is a typo) |
| 23 | Deleting a column keeps rows distinct | always possible |
| 24 | Colouring K₄ in three colours | **yes** — three matchings, or three paths |
| 25 | Thirteen people | true, and **13 is sharp** (12 fails) |
| 26 | Tiling a rectangle | T has an integer side |

## Verification

Every computational claim was checked exhaustively, and then audited a second time by a *different*
method. The scripts live in [`src/verify/`](src/verify) and all pass.

**Volume 1**

* `verify1.py` — breadth-first search over every position of the knights puzzle
* `detect2.py` — recovers the three edge sets of problem 6 from `problem-set.jpg` by pixel sampling
* `verify6.py` — brute force over all 9! = 362,880 vertex bijections; triangle and 4-cycle counts
* `verify8.py` — max-flow realisation showing the digraph of problem 8 exists for every n ≥ 43
* `verify_rest.py`, `verify_extra.py` — degree-sequence realisability, Guarini's puzzle, partition counts
* `audit.py`, `audit2.py`, `audit_img.py` — the independent audit (see below)

**Volume 2**

* `new_A.py` — problems 9, 10, 15, 16, 17, 24 by exhaustive enumeration up to isomorphism
* `new_B.py` — problems 12, 20, 22, 23, 25; includes the complete game tree for problem 12 and all
  35,898 instances of problem 22's hypothesis
* `new_C.py` — problems 11, 13, 14, 18, 19, 21 and the starred problem
* `new_D.py` — problem 26 on randomly generated tilings, and problem 24's second solution
* `audit_new.py` — the independent audit: Erdős–Gallai instead of Havel–Hakimi for problems 9 and 10,
  the "safe move" lemma instead of the game tree for problem 12, the complement bijection for
  problem 15, and the full 21-path Hamiltonian decomposition of K₄₂ for the starred problem

Audits found and fixed two real defects, both recorded in the git history: an incomplete case
analysis in the proof of Theorem 3.2 (volume 1) and a hand-waved edge-disjointness claim in the
starred problem (volume 2).

## Rebuilding the PDFs

```sh
cd src
npm install mathjax@3 puppeteer-core
./build.sh     # volume 1
./build2.sh    # volume 2
```

Each document is authored as HTML fragments (`part0…part9.html` and `q0…q7.html`) with math typeset
by MathJax; figures and tables are generated by `figs*.py` and `tables*.py`, inlined by
`assemble*.py`, and printed to PDF by headless Chromium via `render*.js`. The committed PDFs are
exactly what these scripts produce: rebuilding volume 1 from a clean checkout yields a file whose
pages are byte-identical in both content stream and text layer, differing only in the creation
timestamp Chromium embeds.
