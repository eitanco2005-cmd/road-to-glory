#!/usr/bin/env python3
"""QA: recalculate an .xlsx with LibreOffice headless and report formula errors + key cells.
Usage: python3 qa_recalc.py file.xlsx [Sheet!A1 ...]"""
import subprocess, sys, tempfile, shutil
from pathlib import Path
from openpyxl import load_workbook

src = Path(sys.argv[1]).resolve()
tmp = Path(tempfile.mkdtemp())
shutil.copy(src, tmp / "in.xlsx")
subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML",
                "--outdir", str(tmp / "out"), str(tmp / "in.xlsx")], check=True, capture_output=True, timeout=180)
wb = load_workbook(tmp / "out" / "in.xlsx", data_only=True)
errs = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#") and c.value[1:4].isupper():
                errs += 1
                if errs <= 20:
                    print("ERROR", ws.title, c.coordinate, c.value)
print("errors:", errs)
for ref in sys.argv[2:]:
    sh, a = ref.split("!")
    print(ref, "=", wb[sh][a].value)
