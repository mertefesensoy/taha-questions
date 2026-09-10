#!/usr/bin/env bash
# Rebuild graph-theory-solutions.pdf from the HTML fragments in this directory.
#
#   npm install mathjax@3 puppeteer-core
#   ./build.sh
#
# Rendering uses headless Chromium; adjust CHROME below if yours lives elsewhere.
set -euo pipefail
cd "$(dirname "$0")"
python3 assemble.py solutions.html part0.html part1.html part2.html part3.html \
                                   part4.html part5.html part6.html part7.html part8.html part9.html
node render.js solutions.html ../graph-theory-solutions.pdf pdf
