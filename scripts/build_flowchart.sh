#!/bin/bash
set -e

echo "🔧 Step 1: Generating ELK input from CSVs..."
python generate_elk_input.py

echo "🧠 Step 2: Running ELK layout with Node.js..."
node run_elk.js

echo "🖼  Step 3: Generating final SVG from ELK output..."
python generate_svg.py

echo "🖼  Step 4: Copy SVG to decision tree directory..."
cp final_flowchart.svg ../flowchart.svg

echo "✅ All done. Final SVG: final_flowchart.svg"
