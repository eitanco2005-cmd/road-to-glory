#!/usr/bin/env python3
"""WebP previews for the product / printable pages: workbook sheets via LibreOffice PDF (reuses the Hanukkah helpers)
and the free PDFs' pages.   python3 previews.py"""
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("hk_previews", HERE.parent / "hanukkah" / "previews.py")
_hk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hk)
pdf_pages, trim = _hk.pdf_pages, _hk.trim
from PIL import Image  # noqa: E402
import pypdf  # noqa: E402

OUT = HERE / "out"
DOCS = HERE.parents[1] / "docs"


def sheet_pages(xlsx):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(xlsx)], check=True, capture_output=True, timeout=240)
    pdf = tmp / (xlsx.stem + ".pdf")
    return pdf, [(p.extract_text() or "") for p in pypdf.PdfReader(str(pdf)).pages]


def shots(xlsx, dest, wanted):
    """wanted: {name: (page-matcher(text)->bool, crop height fraction)}"""
    dest.mkdir(parents=True, exist_ok=True)
    pdf, texts = sheet_pages(xlsx)
    for name, (match, frac) in wanted.items():
        hits = [i + 1 for i, t in enumerate(texts) if match(t)]
        if not hits:
            raise SystemExit(f"no page for {name} in {xlsx.name}")
        n = hits[0]
        png = pdf.parent / f"{name}"
        subprocess.run(["pdftoppm", "-r", "130", "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(png)], check=True)
        im = Image.open(f"{png}.png").convert("RGB")
        im = trim(im.crop((0, 0, im.width, int(im.height * frac))))
        if im.width > 1300:
            im = im.resize((1300, int(im.height * 1300 / im.width)), Image.LANCZOS)
        im.save(dest / f"{name}.webp", "WEBP", quality=85, method=6)
        print("shot", dest / f"{name}.webp", im.size)


def starts(word):
    return lambda t: t.strip().startswith(word)


def main():
    if "--debug" in sys.argv:
        for x in ("purim-planner-2027-example", "seder-planner-2027-example"):
            _, texts = sheet_pages(OUT / f"{x}.xlsx")
            for i, t in enumerate(texts):
                print(x, i + 1, t[:120].replace("\n", " | "))
        return
    shots(OUT / "purim-planner-2027-example.xlsx", DOCS / "p" / "purim-planner" / "img", {
        "dashboard": (starts("לפי קבוצה"), .62), "recipients": (starts("נמענים"), .5), "packages": (starts("חבילות"), .6), "route": (starts("מסלול חלוקה"), .4)})
    shots(OUT / "seder-planner-2027-example.xlsx", DOCS / "p" / "seder-planner" / "img", {
        "dashboard": (starts("קטגוריה"), .62), "shopping": (starts("כמויות וקניות"), .6), "haggadah": (starts("תפקידים בהגדה"), .7), "guests": (starts("אורחים"), .35)})
    pdf_pages(OUT / "pesach-cleaning-checklist-2027.pdf", {1: "checklist-1", 2: "checklist-2"}, DOCS / "pesach" / "img", "", dpi=80)
    pdf_pages(OUT / "savings-challenge-2027.pdf", {1: "challenge-52", 2: "challenge-12"}, DOCS / "budget-2027" / "img", "", dpi=80)


if __name__ == "__main__":
    main()
