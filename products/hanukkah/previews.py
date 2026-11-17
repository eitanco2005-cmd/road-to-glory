#!/usr/bin/env python3
"""Render WebP previews for the product pages from the built PDFs / workbooks.
PDF pages -> pdftoppm PNG -> WebP. Workbooks -> LibreOffice PDF -> cropped sheet images."""
import pathlib
import shutil
import subprocess
import tempfile

from PIL import Image, ImageChops

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
DOCS = HERE.parents[1] / "docs"
HE_IMG = DOCS / "p" / "hanukkah-activity-pack" / "img"
HE_PL_IMG = DOCS / "p" / "hanukkah-party-planner" / "img"
EN_IMG = DOCS / "en" / "hanukkah" / "img"

PACK_PAGES = {1: "cover", 3: "coloring", 10: "maze", 12: "wordsearch", 16: "chart", 17: "blessings", 15: "diy", 13: "dreidel-rules"}


def pdf_pages(pdf, pages, dest, prefix, dpi=70):
    dest.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    for n, name in pages.items():
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(tmp / name)], check=True)
        im = Image.open(tmp / f"{name}.png").convert("RGB")
        im.save(dest / f"{prefix}{name}.webp", "WEBP", quality=82, method=6)
    shutil.rmtree(tmp)


def trim(im, pad=16):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def xlsx_shots(xlsx, dest, prefix, pages):
    """pages: {text that only appears on that sheet's first printed page: (name, crop height fraction)}"""
    dest.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(xlsx)], check=True, capture_output=True, timeout=240)
    pdf = tmp / (xlsx.stem + ".pdf")
    import pypdf
    texts = [(p.extract_text() or "").strip() for p in pypdf.PdfReader(str(pdf)).pages]
    for title, (name, frac) in pages.items():
        n = [i + 1 for i, tx in enumerate(texts) if title in tx][0]
        subprocess.run(["pdftoppm", "-r", "130", "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(tmp / name)],
                       check=True, capture_output=True)
        im = Image.open(tmp / f"{name}.png").convert("RGB")
        im = im.crop((0, 0, im.width, int(im.height * frac)))
        im = trim(im)
        if im.width > 1400:
            im = im.resize((1400, int(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(dest / f"{prefix}{name}.webp", "WEBP", quality=85, method=6)
    shutil.rmtree(tmp)


def main():
    pdf_pages(OUT / "hanukkah-activity-pack-he-A4.pdf", PACK_PAGES, HE_IMG, "")
    pdf_pages(OUT / "hanukkah-activity-pack-en-Letter.pdf", PACK_PAGES, EN_IMG, "pack-")
    import planner
    for lang, dest, prefix in (("he", HE_PL_IMG, ""), ("en", EN_IMG, "planner-")):
        t = planner.TX[lang]
        pages = {t["g_head"][1]: ("guests", .35), t["assump"][3][0]: ("quantities", .55), t["s_total"]: ("shopping", .55),
                 t["gf_head"][7]: ("gifts", .45), t["d_kpi"][0]: ("dashboard", .6)}
        xlsx_shots(OUT / f"hanukkah-party-planner-{lang}-example.xlsx", dest, prefix, pages)


if __name__ == "__main__":
    main()
