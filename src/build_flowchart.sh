#!/bin/bash
set -e

echo "🔧 Step 1: Generating ELK input from CSVs..."
python generate_elk_input.py

echo "🧠 Step 2: Running ELK layout with Node.js..."
node run_elk.js

echo "🖼  Step 3: Generating final SVG from ELK output..."
python generate_svg.py

echo "✅ All done. Final SVG: docs/flowchart.svg"
