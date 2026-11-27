#!/usr/bin/env python3
"""Build the Etsy download files (no website links) into etsy/listings/NN-slug/files/.
    python3 etsy/_build/make_files.py [hanukkah|existing|all]
"""
import pathlib
import shutil
import subprocess
import sys
import zipfile

B = pathlib.Path(__file__).resolve().parent
ETSY = B.parent
REPO = ETSY.parent
DL = REPO / "docs" / "dl"
L = ETSY / "listings"
sys.path.insert(0, str(B))
from clean import clean_xlsx, offending  # noqa: E402


def files_dir(slug):
    d = L / slug / "files"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    return d


def pdf_clean_check(p):
    txt = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True, check=True).stdout
    bad = offending(txt)
    if bad:
        raise SystemExit(f"{p}: link left {bad[:2]}")


def hanukkah_pdfs(out):
    sys.path.insert(0, str(REPO / "products" / "hanukkah"))
    import pack
    pack.T["en"]["footer"] = "© 2026 Tichnun Plus · For personal, family and classroom use"
    tmp = B / "_tmp_pack"
    tmp.mkdir(exist_ok=True)
    jobs, res = [], []
    for lang, paper, name in [("en", "Letter", "Hanukkah-Activity-Pack-2026-US-Letter"),
                              ("en", "A4", "Hanukkah-Activity-Pack-2026-A4")]:
        h = tmp / f"{name}.html"
        h.write_text(pack.build_html(lang, paper), encoding="utf-8")
        jobs.append(f"{h}={out / (name + '.pdf')}")
        res.append(out / (name + ".pdf"))
    subprocess.run(["node", str(REPO / "products/hanukkah/print_pdf.js"), *jobs], check=True, capture_output=True)
    shutil.rmtree(tmp)
    for p in res:
        pdf_clean_check(p)
    return res


EXISTING = {  # listing slug -> [(source in docs/dl, etsy file name)]
    "02-hanukkah-party-planner": [("j5skvo4dtz07sz8y/hanukkah-party-planner-en.xlsx", "Hanukkah-Party-Planner.xlsx"),
                                  ("j5skvo4dtz07sz8y/hanukkah-party-planner-en-example.xlsx",
                                   "Hanukkah-Party-Planner-EXAMPLE.xlsx")],
    "04-bar-bat-mitzvah-planner": [("l9e1t1e7ryqmfim5/bar-bat-mitzvah-planner.xlsx", "Bar-Bat-Mitzvah-Planner.xlsx"),
                                   ("l9e1t1e7ryqmfim5/bar-bat-mitzvah-planner-example.xlsx",
                                    "Bar-Bat-Mitzvah-Planner-EXAMPLE.xlsx")],
    "05-jewish-wedding-planner": [("m8gvkisyw6as1zfi/jewish-wedding-planner.xlsx", "Jewish-Wedding-Planner.xlsx"),
                                  ("m8gvkisyw6as1zfi/jewish-wedding-planner-example.xlsx",
                                   "Jewish-Wedding-Planner-EXAMPLE.xlsx")],
    "08-passover-seder-planner": [("2zw7zvvwvjwjx5ut/passover-seder-planner.xlsx", "Passover-Seder-Planner.xlsx"),
                                  ("2zw7zvvwvjwjx5ut/passover-seder-planner-example.xlsx",
                                   "Passover-Seder-Planner-EXAMPLE.xlsx")],
    "09-jewish-holiday-hosting-planner": [("i1rkd4uhly4erf8l/jewish-holiday-planner.xlsx", "Jewish-Holiday-Hosting-Planner.xlsx"),
                                          ("i1rkd4uhly4erf8l/jewish-holiday-planner-example.xlsx",
                                           "Jewish-Holiday-Hosting-Planner-EXAMPLE.xlsx")],
}


def hanukkah():
    a = hanukkah_pdfs(files_dir("01-hanukkah-activity-pack"))
    d = files_dir("02-hanukkah-party-planner")
    x = [clean_xlsx(DL / s, d / n) for s, n in EXISTING["02-hanukkah-party-planner"]]
    b = files_dir("03-hanukkah-bundle")
    for f in a + x:
        shutil.copy(f, b / f.name)


def existing():
    for slug, items in EXISTING.items():
        if slug.startswith("02"):
            continue
        d = files_dir(slug)
        for s, n in items:
            clean_xlsx(DL / s, d / n)


def zip_of(dst, files):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.name)
    return dst


def bundles():
    d = files_dir("10-jewish-life-bundle")
    for slug, name in [("04-bar-bat-mitzvah-planner", "1-Bar-Bat-Mitzvah-Planner.zip"),
                       ("05-jewish-wedding-planner", "2-Jewish-Wedding-Planner.zip"),
                       ("08-passover-seder-planner", "3-Passover-Seder-Planner.zip"),
                       ("09-jewish-holiday-hosting-planner", "4-Jewish-Holiday-Hosting-Planner.zip")]:
        zip_of(d / name, sorted((L / slug / "files").glob("*.xlsx")))
    d = files_dir("11-wedding-planning-bundle")
    for slug, name in [("05-jewish-wedding-planner", "1-Jewish-Wedding-Planner.zip"),
                       ("06-wedding-budget-planner", "2-Wedding-Budget-Planner.zip"),
                       ("07-wedding-seating-chart", "3-Wedding-Seating-Chart.zip")]:
        zip_of(d / name, sorted((L / slug / "files").iterdir()))


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("hanukkah", "all"):
        hanukkah()
    if what in ("existing", "all"):
        existing()
    if what in ("bundles", "all"):
        bundles()
    print("ok", what)
