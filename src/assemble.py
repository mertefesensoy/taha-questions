# -*- coding: utf-8 -*-
"""Assemble solutions.html from HTML fragments + generated SVG figures."""
import re, sys, datetime
sys.path.insert(0, '/tmp/claude-0/-home-user-taha-questions/64ad73c0-31f2-5c61-a3f4-35a349eafe52/scratchpad')
import figs
from tables import TBL
from doc_css import CSS

FIG = {
    'BOARD'      : lambda: figs.fig_board(),
    'CYCLE8'     : lambda: figs.fig_cycle(caption=None, w=330),
    'P1PAIR'     : lambda: figs.fig_p1_pair(),
    'P2GRAPH'    : lambda: figs.fig_p2(),
    'TWOREG'     : lambda: figs.fig_2regular(),
    'DELTA2'     : lambda: figs.fig_delta2(),
    'RAY'        : lambda: figs.fig_ray(),
    'P6THREE'    : lambda: figs.fig_p6_three(),
    'P6ISO'      : lambda: figs.fig_p6_iso(),
    'P6TRI'      : lambda: figs.fig_p6_triangles(),
    'P7SHARP'    : lambda: figs.fig_p7(),
}

MJ = r"""
<script>
window.MathJax = {
  tex: { inlineMath: [['\\(','\\)'],['$','$']], displayMath: [['\\[','\\]']], processEscapes: true,
         macros: { Zn: ["\\mathbb{Z}_9"] } },
  chtml: { scale: 1.0, displayAlign: 'center' },
  options: { renderActions: { addMenu: [] } },
  startup: { pageReady: () => MathJax.startup.defaultPageReady().then(() => { window.MJDONE = true; }) }
};
</script>
<script id="MathJax-script" src="node_modules/mathjax/es5/tex-mml-chtml.js"></script>
"""

def build(parts, out):
    body = "\n".join(open(p, encoding='utf-8').read() for p in parts)
    def sub(m):
        key = m.group(1)
        if key not in FIG:
            raise KeyError('unknown figure placeholder: ' + key)
        return FIG[key]()
    body, n = re.subn(r'\{\{FIG:([A-Z0-9]+)\}\}', sub, body)
    def subt(m):
        key = m.group(1)
        if key not in TBL:
            raise KeyError('unknown table placeholder: ' + key)
        return TBL[key]()
    body, nt = re.subn(r'\{\{TBL:([A-Z0-9]+)\}\}', subt, body)
    # keep short inline math glued to the punctuation that follows it, so a line
    # never breaks between "\(K_1\)" and the full stop after it
    body = re.sub(r'(\\\([^()]{0,60}?\\\))([.,;:!?])', r'<span class="nb">\1\2</span>', body)
    left = re.findall(r'\{\{[^}]*\}\}', body)
    if left:
        raise SystemExit('unresolved placeholders: ' + str(set(left)))
    html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<title>Graph Theory - Problem Set Solutions</title>"
            f"<style>{CSS}</style>{MJ}</head><body>{body}</body></html>")
    open(out, 'w', encoding='utf-8').write(html)
    print(f"wrote {out}: {len(html):,} bytes, {n} figures + {nt} tables inlined")

if __name__ == '__main__':
    build(sys.argv[2:], sys.argv[1])
