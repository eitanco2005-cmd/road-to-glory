#!/usr/bin/env bash
# Rebuild, QA and publish the household budget files to the unguessable download folder.
set -euo pipefail
cd "$(dirname "$0")"
DL=../../docs/dl/356eeeed31d1ee5e
python3 build.py
for f in household-budget-2027.xlsx household-budget-2027-example.xlsx household-budget-2026.xlsx; do
  python3 qa_recalc.py "$f" 2>/dev/null | grep -q "errors: 0" || { echo "QA failed: $f"; exit 1; }
done
mkdir -p "$DL"
cp household-budget-2027.xlsx household-budget-2027-example.xlsx household-budget-2026.xlsx "$DL/"
echo "published to $DL"
