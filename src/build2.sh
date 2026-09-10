#!/usr/bin/env bash
# Rebuild graph-theory-solutions-2.pdf (problems 9-26) from the fragments in this directory.
#
#   npm install mathjax@3 puppeteer-core
#   ./build2.sh
#
set -euo pipefail
cd "$(dirname "$0")"
python3 assemble2.py solutions2.html q0.html q1.html q2.html q3.html q4.html \
                                     q5.html q6.html q7.html
node render2.js solutions2.html ../graph-theory-solutions-2.pdf pdf
