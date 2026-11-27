"""Page renders for listing images: PDF pages and xlsx sheets (via LibreOffice) -> trimmed PNGs."""
import pathlib
import subprocess

from PIL import Image, ImageChops

CACHE = pathlib.Path(__file__).resolve().parent / "_cache"


def _texts(pdf):
    import pypdf
    return [(p.extract_text() or "") for p in pypdf.PdfReader(str(pdf)).pages]


def trim(im, pad=20):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).getbbox()
    if not box:
        return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def pdf_page(pdf, n, dpi=110, key=None, crop=None, do_trim=False, xcrop=(0, 1)):
    """Return path to PNG of page n (1-based). crop = (top_frac, bottom_frac)."""
    CACHE.mkdir(exist_ok=True)
    key = key or f"{pathlib.Path(pdf).stem}-{n}-{dpi}"
    out = CACHE / f"{key}.png"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf),
                        str(CACHE / key)], check=True, capture_output=True)
    if crop or do_trim:
        im = Image.open(out).convert("RGB")
        if crop:
            im = im.crop((int(im.width * xcrop[0]), int(im.height * crop[0]), int(im.width * xcrop[1]), int(im.height * crop[1])))
        if do_trim:
            im = trim(im)
        out2 = CACHE / f"{key}-c{crop}{xcrop}-{do_trim}.png".replace(" ", "").replace("(", "").replace(")", "").replace(",", "_")
        im.save(out2)
        return out2
    return out


def xlsx_pdf(xlsx):
    CACHE.mkdir(exist_ok=True)
    xlsx = pathlib.Path(xlsx)
    pdf = CACHE / (xlsx.stem + ".pdf")
    if not pdf.exists():
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(CACHE), str(xlsx)],
                       check=True, capture_output=True, timeout=300)
    return pdf


def xlsx_sheet(xlsx, marker, crop=(0, 1), dpi=260, nth=0, xcrop=(0, 1)):
    """PNG of the printed page whose text starts with/contains marker (trimmed)."""
    pdf = xlsx_pdf(xlsx)
    texts = _texts(pdf)
    hits = [i + 1 for i, t in enumerate(texts) if t.strip().startswith(marker)] or \
           [i + 1 for i, t in enumerate(texts) if marker in t]
    if not hits:
        raise SystemExit(f"{xlsx}: no page with {marker!r}")
    return pdf_page(pdf, hits[nth], dpi=dpi, key=f"{pathlib.Path(xlsx).stem}-{hits[nth]}-{dpi}", crop=crop, do_trim=True, xcrop=xcrop)
