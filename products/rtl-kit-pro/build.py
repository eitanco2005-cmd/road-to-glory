#!/usr/bin/env python3
"""Build RTL Landing Kit Pro and publish the free kit demos.

    python3 products/rtl-kit-pro/build.py [--no-shots]

1. Free kit: devkit/ (templates, css, js) -> docs/devkit/demos/  (live demos)
              and docs/devkit/rtl-landing-kit-free.zip
2. Pro pack:  12 templates + components gallery -> build/rtl-landing-kit-pro/ -> zip into
              docs/dl/<folder from docs/data/products/rtl-kit-pro.json>/rtl-landing-kit-pro-v1.0.zip
3. Screenshots (Playwright, needs `node` with playwright): docs/devkit/img/*.jpg + devkit/screenshots/*.png
The Pro source is not published as live pages (only screenshots), so the zip is what buyers pay for.
"""
import html
import json
import pathlib
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
DEVKIT = REPO / "devkit"
DOCS = REPO / "docs"
sys.path.insert(0, str(HERE / "src"))
import components  # noqa: E402
import pages  # noqa: E402

VERSION = "1.0"
FONTS = ("https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800"
         "&family=Noto+Kufi+Arabic:wght@400;500;700;800&family=Inter:wght@400;500;700;800&display=swap")
PRODUCT = json.loads((DOCS / "data/products/rtl-kit-pro.json").read_text(encoding="utf-8"))


def shell(title, body, theme="", depth=1, dir_toggle=True):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | RTL Landing Kit Pro</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{up}css/rtl-kit.css">
<link rel="stylesheet" href="{up}css/pro.css">
{f"<style>:root{{{theme}}}</style>" if theme else ""}
</head>
<body>
<a class="skip" href="#main">דילוג לתוכן</a>
{body}
{'<button class="btn sm ghost dir-toggle" type="button" data-dir-toggle title="Preview the page left-to-right (development helper — delete in production)">LTR ⇄</button>' if dir_toggle else ""}
<script src="{up}js/pro.js"></script>
</body>
</html>
"""


def build_pro(out):
    if out.exists():
        shutil.rmtree(out)
    (out / "css").mkdir(parents=True)
    (out / "js").mkdir()
    (out / "templates").mkdir()
    (out / "components").mkdir()
    shutil.copy(DEVKIT / "css/rtl-kit.css", out / "css/rtl-kit.css")
    shutil.copy(HERE / "src/css/pro.css", out / "css/pro.css")
    shutil.copy(HERE / "src/js/pro.js", out / "js/pro.js")
    listing = []
    for fn in pages.TEMPLATES:
        slug, title, theme, body = fn()
        (out / "templates" / f"{slug}.html").write_text(shell(title, body, theme), encoding="utf-8")
        listing.append((slug, title))
    (out / "components/index.html").write_text(shell("רכיבים", '<main id="main"><section class="hero" style="padding-block:48px 0"><div class="container"><h1 style="font-size:2.2rem">רכיבים להעתקה</h1>'
                                                     '<p class="lead">כל בלוק עומד בפני עצמו: מעתיקים את ה-HTML, ו-rtl-kit.css + pro.css עושים את השאר. כפתור LTR בפינה מראה איך הכול מתהפך.</p></div></section>'
                                                     + components.page() + "</main>"), encoding="utf-8")
    # free templates are included too, so the pack is complete on its own
    free = out / "free"
    shutil.copytree(DEVKIT / "templates", free / "templates")
    shutil.copytree(DEVKIT / "css", free / "css")
    shutil.copytree(DEVKIT / "js", free / "js")
    cards = "".join(f'<a class="card" href="templates/{s}.html" style="text-decoration:none;color:inherit"><h3 class="mb-0">{html.escape(t)}</h3><span class="muted" dir="ltr">templates/{s}.html</span></a>' for s, t in listing)
    index = (f'<main id="main" class="section"><div class="container"><h1 style="font-size:2.4rem">RTL Landing Kit Pro <bdi>v{VERSION}</bdi></h1>'
             '<p class="lead">12 תבניות, ספריית רכיבים, ו-3 התבניות החינמיות. פתחו כל קובץ בדפדפן — אין צורך בהתקנה.</p>'
             '<p><a class="btn" href="components/index.html">לספריית הרכיבים</a> <a class="btn ghost" href="free/templates/launch/index.html">תבניות חינמיות</a></p>'
             f'<div class="grid c3 mt-2">{cards}</div><p class="muted mt-2">README.md מסביר את המבנה, ההתאמה לערבית ואת הרישיון.</p></div></main>')
    (out / "index.html").write_text(shell("RTL Landing Kit Pro", index, depth=0, dir_toggle=False), encoding="utf-8")
    (out / "README.md").write_text((HERE / "src/README-PRO.md").read_text(encoding="utf-8"), encoding="utf-8")
    (out / "LICENSE-PRO.txt").write_text((HERE / "src/LICENSE-PRO.txt").read_text(encoding="utf-8"), encoding="utf-8")
    return listing


def zipdir(src, dest, prefix):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file():
                zi = zipfile.ZipInfo(f"{prefix}/{f.relative_to(src).as_posix()}", date_time=(2026, 11, 17, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, f.read_bytes())


def publish_free():
    demos = DOCS / "devkit/demos"
    if demos.exists():
        shutil.rmtree(demos)
    for d in ("templates", "css", "js"):
        shutil.copytree(DEVKIT / d, demos / d)
    stage = HERE / "build/free"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for d in ("templates", "css", "js", "tailwind", "tools"):
        shutil.copytree(DEVKIT / d, stage / d, ignore=shutil.ignore_patterns("__pycache__"))
    for f in ("README.md", "LICENSE", "package.json"):
        shutil.copy(DEVKIT / f, stage / f)
    zipdir(stage, DOCS / "devkit/rtl-landing-kit-free.zip", "rtl-landing-kit")


def main():
    publish_free()
    out = HERE / "build/rtl-landing-kit-pro"
    listing = build_pro(out)
    path = PRODUCT["files"][0]["path"]  # dl/<folder>/rtl-landing-kit-pro-v1.0.zip
    zipdir(out, DOCS / path, "rtl-landing-kit-pro")
    (HERE / "build/listing.json").write_text(json.dumps(listing, ensure_ascii=False), encoding="utf-8")
    print("pro templates:", len(listing), "->", path)
    if "--no-shots" not in sys.argv:
        subprocess.run(["node", str(HERE / "shots.js")], check=True)


if __name__ == "__main__":
    main()
