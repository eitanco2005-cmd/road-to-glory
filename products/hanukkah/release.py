#!/usr/bin/env python3
"""Rebuild everything for the Hanukkah stream and publish into docs/:
PDFs (pack.py) -> workbooks (planner.py) -> copy deliverables into their docs/dl/<folder>/ (dl_folders.json)
-> previews (previews.py) -> pages (site_pages.py).   Run: python3 release.py"""
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DOCS = HERE.parents[1] / "docs"
for step in ("pack.py", "planner.py"):
    subprocess.run([sys.executable, str(HERE / step)], check=True, cwd=HERE)
for slug, d in json.loads((HERE / "dl_folders.json").read_text()).items():
    for f in d["files"]:
        shutil.copy(HERE / "out" / pathlib.Path(f["path"]).name, DOCS / f["path"])
        print("published", f["path"])
for step in ("previews.py", "site_pages.py"):
    subprocess.run([sys.executable, str(HERE / step)], check=True, cwd=HERE)
