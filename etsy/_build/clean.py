"""Helpers: strip website links from xlsx files at the zip/XML level (keeps charts, styles, formulas intact)."""
import re
import zipfile

LINK = re.compile(r'(?:https?://)?tichnun\.netlify\.app[^\s&<"]*\s*(?:&#183;|·)?\s*')
FORBIDDEN = re.compile(r'netlify|tichnun\.|paypal|https?://(?!schemas\.|purl\.org|www\.w3\.org|schemas)', re.I)


def clean_xlsx(src, dst):
    zin = zipfile.ZipFile(src)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith((".xml", ".rels")):
                s = data.decode("utf-8")
                s = LINK.sub("", s)
                data = s.encode("utf-8")
            zout.writestr(item, data)
    assert_clean_xlsx(dst)
    return dst


def offending(text):
    out = []
    for m in FORBIDDEN.finditer(text):
        out.append(text[max(0, m.start() - 40): m.end() + 40])
    return out


def assert_clean_xlsx(path):
    z = zipfile.ZipFile(path)
    bad = []
    for n in z.namelist():
        if n.endswith((".xml", ".rels")):
            bad += offending(z.read(n).decode("utf-8", "ignore"))
    if bad:
        raise SystemExit(f"{path}: site link left: {bad[:3]}")
