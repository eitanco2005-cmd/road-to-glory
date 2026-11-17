#!/usr/bin/env bash
# Rebuild, QA and publish the renovation planner files to the unguessable download folder.
set -euo pipefail
cd "$(dirname "$0")"
DL=../../docs/dl/1c9ed6b2319083a3
python3 build.py
python3 build_checklist.py
for f in renovation-budget.xlsx renovation-budget-example.xlsx; do
  python3 ../household-budget/qa_recalc.py "$f" 2>/dev/null | grep -q "errors: 0" || { echo "QA failed: $f"; exit 1; }
done
mkdir -p "$DL"
cp renovation-budget.xlsx renovation-budget-example.xlsx renovation-contractor-checklist.docx "$DL/"
echo "published to $DL"
