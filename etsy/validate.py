#!/usr/bin/env python3
"""Validate the Etsy kit:  python3 etsy/validate.py [--no-recalc]
Checks per listing: title <=140, exactly 13 tags each <=20 chars (letters, numbers, spaces), price, description,
1-5 files each <=20MB, every file opens (xlsx: LibreOffice recalc -> 0 formula errors; pdf: renders; zip: contents ok),
no website/PayPal links inside files or images' source text, 7-10 images, each exactly 3000x2250 JPG, files/images listed
in listing.md exist."""
import pathlib
import re
import subprocess
import sys
import tempfile
import zipfile

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "_build"))
from clean import offending  # noqa: E402

ERR_RE = re.compile(r"#(REF!|VALUE!|DIV/0!|NAME\?|N/A|NUM!|NULL!)|Err:\d+")
TAG_RE = re.compile(r"^[A-Za-z0-9 ]+$")
problems = []


def bad(msg):
    problems.append(msg)
    print("  ✗", msg)


def block(md, heading):
    m = re.search(rf"## {re.escape(heading)}[^\n]*\n```\n(.*?)\n```", md, re.S)
    return m.group(1) if m else None


def check_xlsx_text(path, z=None):
    z = z or zipfile.ZipFile(path)
    for n in z.namelist():
        if n.endswith((".xml", ".rels")):
            o = offending(z.read(n).decode("utf-8", "ignore"))
            if o:
                bad(f"{path.name}: link in {n}: {o[0]!r}")


def recalc(path, tmp):
    """LibreOffice converts to csv per sheet would be slow; convert to xlsx (recalculates) and scan cached values."""
    out = pathlib.Path(tmp)
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", str(out),
                    str(path)], check=True, capture_output=True, timeout=300)
    import openpyxl
    wb = openpyxl.load_workbook(out / path.name, data_only=True)
    errs = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and ERR_RE.search(c.value):
                    errs += 1
                    if errs <= 3:
                        bad(f"{path.name}: {ws.title}!{c.coordinate} = {c.value}")
    return errs


def check_pdf(path):
    r = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True)
    pages = re.search(r"Pages:\s+(\d+)", r.stdout)
    if r.returncode or not pages:
        bad(f"{path.name}: pdf does not open")
        return 0
    with tempfile.TemporaryDirectory() as t:
        n = int(pages.group(1))
        for p in sorted({1, n}):
            subprocess.run(["pdftoppm", "-r", "20", "-png", "-f", str(p), "-l", str(p), str(path), f"{t}/x"], check=True)
        if len(list(pathlib.Path(t).glob("*.png"))) < 1:
            bad(f"{path.name}: pdf does not render")
    txt = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    o = offending(txt)
    if o:
        bad(f"{path.name}: link in pdf text {o[0]!r}")
    return int(pages.group(1))


def main(do_recalc=True):
    listings = sorted(p for p in (HERE / "listings").iterdir() if p.is_dir())
    for d in listings:
        print(f"[{d.name}]")
        md_p = d / "listing.md"
        if not md_p.exists():
            bad(f"{d.name}: listing.md missing")
            continue
        md = md_p.read_text(encoding="utf-8")
        title = block(md, "Title")
        if not title or len(title) > 140:
            bad(f"title length {len(title or '')}")
        for ch in "%:&":
            if title and title.count(ch) > 1:
                bad(f"title: Etsy allows {ch!r} only once")
        tags = (block(md, "Tags") or "").splitlines()
        if len(tags) != 13:
            bad(f"{len(tags)} tags (need 13)")
        if len(set(t.lower() for t in tags)) != len(tags):
            bad("duplicate tags")
        for t in tags:
            if len(t) > 20 or not TAG_RE.match(t):
                bad(f"tag {t!r} ({len(t)} chars)")
        price = block(md, "Price (USD)")
        try:
            assert 1 <= float(price) <= 100
        except Exception:
            bad(f"price {price!r}")
        desc = block(md, "Description") or ""
        for need in ["WHAT YOU GET", "HOW IT WORKS", "INSTANT DOWNLOAD", "No physical item", "AI"]:
            if need.lower() not in desc.lower():
                bad(f"description lacks {need!r}")
        o = offending(md)
        if o:
            bad(f"listing.md has link: {o[0]!r}")
        files = sorted((d / "files").iterdir()) if (d / "files").exists() else []
        if not 1 <= len(files) <= 5:
            bad(f"{len(files)} files (Etsy: 1-5)")
        for f in files:
            if f.stat().st_size > 20 * 1024 * 1024:
                bad(f"{f.name} > 20MB")
            if f"files/{f.name}" not in md:
                bad(f"{f.name} not listed in listing.md")
        with tempfile.TemporaryDirectory() as tmp:
            for f in files:
                if f.suffix == ".xlsx":
                    check_xlsx_text(f)
                    e = recalc(f, tmp) if do_recalc else 0
                    print(f"  {f.name}: {'recalc ' + str(e) + ' errors' if do_recalc else 'text ok'}")
                elif f.suffix == ".pdf":
                    print(f"  {f.name}: {check_pdf(f)} pages")
                elif f.suffix == ".zip":
                    z = zipfile.ZipFile(f)
                    if z.testzip():
                        bad(f"{f.name}: corrupt zip")
                    for n in z.namelist():
                        sub = pathlib.Path(tmp) / n
                        sub.write_bytes(z.read(n))
                        if sub.suffix == ".xlsx":
                            check_xlsx_text(sub)
                            e = recalc(sub, pathlib.Path(tmp) / "r") if do_recalc else 0
                            print(f"  {f.name}/{n}: recalc {e} errors")
                        elif sub.suffix == ".pdf":
                            check_pdf(sub)
                else:
                    bad(f"{f.name}: unexpected type")
        imgs = sorted((d / "images").glob("*.jpg"))
        if not 7 <= len(imgs) <= 10:
            bad(f"{len(imgs)} images (need 7-10)")
        for im in imgs:
            with Image.open(im) as I:
                if I.size != (3000, 2250) or I.format != "JPEG":
                    bad(f"{im.name}: {I.format} {I.size}")
            if im.stat().st_size > 20 * 1024 * 1024:
                bad(f"{im.name} too big")
            if f"images/{im.name}" not in md:
                bad(f"{im.name} not listed in listing.md")
        print(f"  title {len(title or '')}/140 · {len(tags)} tags · ${price} · {len(files)} files · {len(imgs)} images")
    for p in ["GUIDE-he.md", "CHECKLIST.md", "shop/shop.md", "shop/faq.md", "shop/reply-templates.md"]:
        if not (HERE / p).exists():
            bad(f"missing {p}")
    print("\nRESULT:", "ALL PASSED" if not problems else f"{len(problems)} PROBLEMS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main("--no-recalc" not in sys.argv))
