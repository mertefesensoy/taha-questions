# -*- coding: utf-8 -*-
"""Assemble solutions2.html from HTML fragments + generated SVG figures."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs2
from tables2 import TBL2
from doc_css import CSS

FIG2 = {
 'P9'   : figs2.fig_p9,
 'P10'  : figs2.fig_p10,
 'P12'  : figs2.fig_p12,
 'P13'  : lambda: figs2.fig_components(
              "a second component would push the total past 100 vertices",
              "component of v&#8320;: &#8805; 67", "any other: &#8805; 34"),
 'P15A' : lambda: figs2.fig_p15('a'),
 'P15B' : lambda: figs2.fig_p15('b'),
 'P15C' : lambda: figs2.fig_p15('c'),
 'P16'  : figs2.fig_p16,
 'STAR' : figs2.fig_star,
 'P24'  : figs2.fig_p24,
 'P25'  : figs2.fig_p25,
 'P26L' : figs2.fig_p26_local,
 'P26F' : figs2.fig_p26_frame,
}

MJ = r"""
<script>
window.MathJax = {
  tex: { inlineMath: [['\\(','\\)'],['$','$']], displayMath: [['\\[','\\]']], processEscapes: true },
  chtml: { scale: 1.0, displayAlign: 'center' },
  startup: { pageReady: () => MathJax.startup.defaultPageReady().then(() => { window.MJDONE = true; }) }
};
</script>
<script id="MathJax-script" src="node_modules/mathjax/es5/tex-mml-chtml.js"></script>
"""

def build(parts, out):
    body = "\n".join(open(p, encoding='utf-8').read() for p in parts)
    def subf(m):
        k=m.group(1)
        if k not in FIG2: raise KeyError('unknown figure: '+k)
        return FIG2[k]()
    def subt(m):
        k=m.group(1)
        if k not in TBL2: raise KeyError('unknown table: '+k)
        return TBL2[k]()
    body, nf = re.subn(r'\{\{FIG2:([A-Z0-9]+)\}\}', subf, body)
    body, nt = re.subn(r'\{\{TBL2:([A-Z0-9]+)\}\}', subt, body)
    left = re.findall(r'\{\{[^}]*\}\}', body)
    if left: raise SystemExit('unresolved placeholders: '+str(set(left)))
    body = re.sub(r'(\\\([^()]{0,60}?\\\))([.,;:!?])', r'<span class="nb">\1\2</span>', body)
    html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<title>Graph Theory - Problems 9 to 26</title>"
            f"<style>{CSS}</style>{MJ}</head><body>{body}</body></html>")
    open(out,'w',encoding='utf-8').write(html)
    print(f"wrote {out}: {len(html):,} bytes, {nf} figures + {nt} tables inlined")

if __name__ == '__main__':
    build(sys.argv[2:], sys.argv[1])
