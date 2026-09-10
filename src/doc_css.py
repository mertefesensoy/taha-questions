CSS = r"""
:root{
  --ink:#1b1b1b; --soft:#4a4a4a; --acc:#1f4e79; --acc2:#a33a2a;
  --rule:#d5d8dc; --tint:#f4f7fa; --tint2:#fbf6ef;
}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact; print-color-adjust:exact;}
body{
  font-family:'Bitstream Charter','Charter','DejaVu Serif','Liberation Serif',Georgia,serif;
  font-size:10.4pt; line-height:1.52; color:var(--ink); margin:0; background:#fff;
  text-rendering:optimizeLegibility;
}
p{margin:0 0 .62em 0; text-align:justify; hyphens:auto}
h1,h2,h3,h4{font-family:inherit; color:var(--acc); font-weight:700; break-after:avoid; margin:0}
h2{font-size:15.5pt; margin:0 0 .1em 0; letter-spacing:.1px}
h3{font-size:11.6pt; margin:1.15em 0 .38em 0; color:#123c60}
h4{font-size:10.6pt; margin:.95em 0 .3em 0; color:#2f2f2f; font-weight:700}

/* ---- title block ---- */
.title-wrap{text-align:center; padding:6mm 0 3mm 0; border-bottom:2.2pt solid var(--acc); margin-bottom:4mm}
.title-wrap .kicker{font-size:9pt; letter-spacing:2.2px; text-transform:uppercase; color:var(--acc2); margin-bottom:2.5mm}
.title-wrap h1{font-size:24pt; line-height:1.16; color:var(--acc); margin-bottom:2mm}
.title-wrap .sub{font-size:11pt; color:var(--soft); font-style:italic}
.meta{display:flex; justify-content:center; gap:26px; font-size:8.6pt; color:var(--soft); margin-top:3.2mm; letter-spacing:.3px}

/* ---- problem headers ---- */
.problem{margin-top:8mm; break-inside:auto}
.problem:first-of-type{margin-top:6mm}
.phead{break-after:avoid; break-inside:avoid}
h3,h4{break-after:avoid}
.nb{white-space:nowrap}
.phead{display:flex; align-items:baseline; gap:10px; border-bottom:1.4pt solid var(--acc); padding-bottom:1.6mm; margin-bottom:2.6mm}
.pnum{font-size:9pt; font-weight:700; color:#fff; background:var(--acc); border-radius:3px; padding:1.6px 7px; letter-spacing:.6px; white-space:nowrap}
.ptag{margin-left:auto; padding-left:6px; font-size:8.2pt; color:var(--soft); font-style:italic; white-space:nowrap}

/* ---- boxes ---- */
.statement{background:var(--tint); border-left:3pt solid var(--acc); padding:2.6mm 4mm; margin:0 0 3.6mm 0; font-size:10.1pt; break-inside:avoid}
.statement .lab{font-size:8pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--acc); font-weight:700; display:block; margin-bottom:1mm}
.statement p{margin-bottom:.35em}
.statement p:last-child{margin-bottom:0}

.answer{background:var(--tint2); border:1pt solid #e0cfae; border-left:3pt solid var(--acc2);
  padding:2.6mm 4mm; margin:3.4mm 0; break-inside:avoid}
.answer .lab{font-size:8pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--acc2); font-weight:700; display:block; margin-bottom:1mm}
.answer p:last-child{margin-bottom:0}

.env{margin:.75em 0; break-inside:avoid-page; display:flow-root}
.env .h{font-weight:700; color:#123c60}
.env.thm .h,.env.lem .h,.env.cor .h,.env.defn .h{color:var(--acc)}
.env.thm, .env.lem, .env.cor{border-left:2pt solid #c9d6e2; padding-left:3.2mm}
.env.thm .body,.env.lem .body,.env.cor .body{font-style:italic}
.prf{margin:.6em 0 .9em 0; display:flow-root}
.prf .h{font-style:italic; color:var(--soft); font-weight:400}
.qed{float:right; color:var(--soft)}
.step{margin-top:.85em}
.step .h{font-weight:700; color:#123c60}

ul,ol{margin:.35em 0 .7em 0; padding-left:5.2mm}
li{margin-bottom:.24em; text-align:justify}
ul.tight li,ol.tight li{margin-bottom:.1em}

/* ---- tables ---- */
table.rule-top tbody tr:first-child td{border-top:1.1pt solid var(--ink)}
table{border-collapse:collapse; margin:0 auto 1.4mm auto; font-size:9.1pt; break-inside:avoid}
table.wide{width:100%}
th,td{padding:1.35mm 2.6mm; text-align:center}
thead th{border-top:1.1pt solid var(--ink); border-bottom:.6pt solid var(--ink); font-weight:700; background:#fafbfc}
tbody tr:last-child td{border-bottom:1.1pt solid var(--ink)}
tbody td{border-bottom:.35pt solid #e6e8ea}
td.l,th.l{text-align:left}
.tblock{break-inside:avoid; margin:2.6mm 0}
.tcap{font-size:8.5pt; color:var(--soft); text-align:center; margin:0 0 2.6mm 0; font-style:italic}
.hl{background:#fdf3ee}
code,.mono{font-family:'DejaVu Sans Mono','Liberation Mono',monospace; font-size:8.8pt}

/* ---- figures ---- */
figure{margin:3.2mm 0; text-align:center; break-inside:avoid}
figcaption{font-size:8.5pt; color:var(--soft); margin-top:1.2mm; font-style:italic}
.figrow{display:flex; gap:6px; justify-content:center; align-items:flex-start; flex-wrap:wrap}
svg.fig{max-width:100%; height:auto}
.board{font-family:'DejaVu Sans Mono',monospace; font-size:11pt; line-height:1.35; text-align:center; letter-spacing:3px; margin:2mm 0}

/* ---- misc ---- */
.note{font-size:9.3pt; color:var(--soft); border-top:.5pt solid var(--rule); padding-top:1.6mm; margin-top:3mm}
.note .h{font-weight:700; color:var(--acc); font-style:normal}
.toc{background:var(--tint); border:1pt solid var(--rule); padding:3mm 5mm; margin:4mm 0 0 0; break-inside:avoid}
.toc h3{margin-top:0}
.toc ol{columns:2; column-gap:9mm; padding-left:4.6mm; margin-bottom:0}
.toc li{font-size:9.4pt; margin-bottom:.22em; text-align:left}
.toc .a{color:var(--acc2); font-weight:700}
mjx-container{overflow-x:visible !important}
mjx-container[display="true"]{margin:.55em 0 !important}
.small{font-size:9.2pt}
"""
