#!/usr/bin/env python3
"""Render sheet screenshots of an example workbook (LibreOffice -> PDF -> PNG -> WebP).
Usage: python3 shots.py file.xlsx outdir "title text=name" ..."""
import subprocess, sys, tempfile, shutil
from pathlib import Path

src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
tmp = Path(tempfile.mkdtemp())
shutil.copy(src, tmp / "w.xlsx")
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(tmp / "w.xlsx")], check=True, capture_output=True)
pdf = tmp / "w.pdf"
n = int([l for l in subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages")][0].split()[-1])
texts = [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), str(pdf), "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]
for spec in sys.argv[3:]:
    key, name = spec.split("=")
    frac = 1.0
    if ":" in name:
        name, frac = name.split(":")
        frac = float(frac)
    page = next(i for i, t in enumerate(texts, 1) if i > 1 and key in t.replace("‫", "").replace("‬", "").replace("‪", ""))
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "150", "-png", "-singlefile", str(pdf), str(tmp / name)], check=True)
    subprocess.run(["convert", str(tmp / f"{name}.png"), "-gravity", "North", "-crop", f"100%x{int(frac*100)}%+0+0", "+repage", "-trim", "-bordercolor", "white", "-border", "24",
                    "-resize", "1400x>", "-quality", "82", str(out / f"{name}.webp")], check=True)
    print(name, "page", page)
