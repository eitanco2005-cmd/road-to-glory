"""Listing images: HTML templates rendered by Chromium at 1500x1125 CSS px x2 = 3000x2250 px, saved as JPG."""
import html
import io
import pathlib

from PIL import Image

REPO = pathlib.Path(__file__).resolve().parents[2]
FONTS = (REPO / "products" / "hanukkah" / "fonts").as_uri()
W, H = 1500, 1125
e = html.escape

THEMES = {
    "hanukkah": dict(bg="#EAF2FB", ink="#13315C", accent="#1E5AA8", gold="#E8B23A", soft="#FFFFFF", chip="#FFF3D1"),
    "wedding": dict(bg="#F7F1EC", ink="#3B2F2A", accent="#8A6E5A", gold="#C9A227", soft="#FFFFFF", chip="#EFE5DA"),
    "mitzvah": dict(bg="#EEF1F8", ink="#1F2A4A", accent="#3A4F8C", gold="#C9A227", soft="#FFFFFF", chip="#E3E8F4"),
    "passover": dict(bg="#F5EFE6", ink="#3D2B1F", accent="#7A2E2E", gold="#C9A227", soft="#FFFFFF", chip="#EFE2CF"),
    "holiday": dict(bg="#EEF5EF", ink="#1E3A2B", accent="#2E7D4F", gold="#C9A227", soft="#FFFFFF", chip="#DDEEE2"),
}

BASE_CSS = """
@font-face{font-family:Fredoka;src:url(%(f)s/Fredoka-600.ttf);font-weight:600}
@font-face{font-family:Fredoka;src:url(%(f)s/Fredoka-700.ttf);font-weight:700}
@font-face{font-family:Nunito;src:url(%(f)s/Nunito-400.ttf);font-weight:400}
@font-face{font-family:Nunito;src:url(%(f)s/Nunito-700.ttf);font-weight:700}
@font-face{font-family:Nunito;src:url(%(f)s/Nunito-800.ttf);font-weight:800}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{background:%(bg)s;color:%(ink)s;font-family:Nunito,sans-serif;position:relative}
h1,h2,h3{font-family:Fredoka,sans-serif;font-weight:700;line-height:1.05}
.page{background:#fff;box-shadow:0 18px 50px rgba(0,0,0,.18),0 2px 6px rgba(0,0,0,.08);border-radius:6px;overflow:hidden}
.page img{display:block;width:100%%;height:100%%;object-fit:cover;object-position:top}
.chip{display:inline-block;background:%(chip)s;color:%(ink)s;border-radius:999px;padding:12px 26px;font-weight:800;font-size:26px;margin:0 12px 14px 0}
.band{position:absolute;left:0;right:0;bottom:0;height:16px;background:%(accent)s}
.cap{position:absolute;left:70px;right:70px;top:46px}
.cap h2{font-size:64px;color:%(accent)s}
.cap p{font-size:30px;margin-top:12px;font-weight:700;opacity:.85}
"""


def css(theme):
    t = THEMES[theme]
    return BASE_CSS % dict(f=FONTS, w=W, h=H, **t)


def img(p):
    return pathlib.Path(p).resolve().as_uri()


def doc(theme, body, extra=""):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{css(theme)}{extra}</style></head><body>{body}<div class=band></div></body></html>"


# ---------------------------------------------------------------- templates
def hero(theme, title, subtitle, chips, pages, landscape=False, kicker=None):
    """pages: up to 3 image paths fanned on the right."""
    t = THEMES[theme]
    if landscape:
        pw, ph = 600, 450
    else:
        pw, ph = 440, 570
    stack = ""
    pos = ([(-7, -80, 50), (5, 80, -20), (0, 0, 0)] if landscape else [(-8, -110, 40), (6, 100, 10), (0, 0, 0)])[-len(pages):]
    cx = 1070 if landscape else 1120
    for (rot, dx, dy), p in zip(pos, pages):
        stack += (f'<div class=page style="position:absolute;width:{pw}px;height:{ph}px;left:{cx - pw // 2 + dx}px;'
                  f'top:{560 - ph // 2 + dy}px;transform:rotate({rot}deg)"><img src="{img(p)}"></div>')
    k = f'<div style="font-size:30px;font-weight:800;letter-spacing:3px;color:{t["gold"]};text-transform:uppercase;margin-bottom:22px">{e(kicker)}</div>' if kicker else ""
    body = (f'<div style="position:absolute;left:80px;top:0;bottom:0;width:590px;display:flex;flex-direction:column;justify-content:center">'
            f'{k}<h1 style="font-size:84px;color:{t["accent"]}">{e(title)}</h1>'
            f'<p style="font-size:34px;margin:30px 0 40px;font-weight:700;line-height:1.3">{e(subtitle)}</p>'
            f'<div>{"".join(f"<span class=chip>{e(c)}</span>" for c in chips)}</div></div>{stack}')
    return doc(theme, body)


def grid(theme, title, sub, items, cols=5, landscape=False):
    """items: list of (image, label)."""
    rows = (len(items) + cols - 1) // cols
    gap = 26
    avail_w, avail_h = W - 140, H - 230 - 40
    cw = (avail_w - gap * (cols - 1)) / cols
    ratio = 0.75 if landscape else 1.294
    ch = min(cw * ratio, (avail_h - gap * (rows - 1)) / rows - 40)
    cw2 = ch / ratio
    cells = "".join(
        f'<div style="width:{cw}px;display:flex;flex-direction:column;align-items:center">'
        f'<div class=page style="width:{cw2}px;height:{ch}px"><img src="{img(p)}"></div>'
        f'<div style="font-size:22px;font-weight:800;margin-top:10px;text-align:center;white-space:nowrap">{e(lbl)}</div></div>'
        for p, lbl in items)
    body = (f'<div class=cap><h2>{e(title)}</h2><p>{e(sub)}</p></div>'
            f'<div style="position:absolute;left:70px;right:70px;top:220px;display:flex;flex-wrap:wrap;gap:{gap}px;justify-content:center">{cells}</div>')
    return doc(theme, body)


def shot(theme, title, sub, images, bullets=None):
    """One or two big screenshots (contain-fit), optional bullet list on the right."""
    area_l, area_t, area_w, area_h = 70, 230, W - 140, H - 230 - 60
    side = ""
    if bullets:
        area_w = 960
        side = (f'<div style="position:absolute;left:{70 + area_w + 50}px;right:70px;top:250px">' +
                "".join(f'<div style="font-size:30px;font-weight:700;margin-bottom:26px;padding-left:44px;position:relative">'
                        f'<span style="position:absolute;left:0;top:-2px;color:{THEMES[theme]["accent"]};font-size:34px">✓</span>{e(b)}</div>'
                        for b in bullets) + "</div>")
    n = len(images)
    gap = 36
    boxes = ""
    for i, p in enumerate(images):
        w_ = (area_w - gap * (n - 1)) / n
        im = Image.open(p)
        r = im.height / im.width
        bw = w_
        bh = bw * r
        if bh > area_h:
            bh = area_h
            bw = bh / r
        x = area_l + i * (w_ + gap) + (w_ - bw) / 2
        boxes += (f'<div class=page style="position:absolute;left:{x}px;top:{area_t + (area_h - bh) / 2}px;width:{bw}px;height:{bh}px">'
                  f'<img src="{img(p)}" style="object-fit:contain"></div>')
    return doc(theme, f'<div class=cap><h2>{e(title)}</h2><p>{e(sub)}</p></div>{boxes}{side}')


def steps(theme, title, items, footer=None):
    t = THEMES[theme]
    n = len(items)
    cards = "".join(
        f'<div style="flex:1;background:#fff;border-radius:28px;padding:44px 38px;box-shadow:0 10px 30px rgba(0,0,0,.08)">'
        f'<div style="width:92px;height:92px;border-radius:50%;background:{t["accent"]};color:#fff;font-family:Fredoka;font-weight:700;'
        f'font-size:52px;display:flex;align-items:center;justify-content:center;margin-bottom:30px">{i + 1}</div>'
        f'<h3 style="font-size:42px;margin-bottom:18px">{e(h)}</h3><p style="font-size:29px;line-height:1.4;font-weight:700;opacity:.85">{e(p)}</p></div>'
        for i, (h, p) in enumerate(items))
    f = (f'<div style="position:absolute;left:70px;right:70px;bottom:60px;text-align:center;font-size:30px;font-weight:800;'
         f'background:{t["chip"]};border-radius:20px;padding:24px">{e(footer)}</div>') if footer else ""
    body = (f'<div class=cap><h2>{e(title)}</h2></div><div style="position:absolute;left:70px;right:70px;top:210px;'
            f'display:flex;gap:{36 if n < 4 else 26}px">{cards}</div>{f}')
    return doc(theme, body)


def checklist(theme, title, sub, cols):
    """cols: list of (heading, [lines])"""
    t = THEMES[theme]
    blocks = "".join(
        f'<div style="flex:1;background:#fff;border-radius:28px;padding:40px 42px;box-shadow:0 10px 30px rgba(0,0,0,.08)">'
        f'<h3 style="font-size:40px;color:{t["accent"]};margin-bottom:26px">{e(h)}</h3>' +
        "".join(f'<div style="font-size:29px;font-weight:700;margin-bottom:20px;padding-left:44px;position:relative">'
                f'<span style="position:absolute;left:0;color:{t["accent"]}">✓</span>{e(x)}</div>' for x in lines) + "</div>"
        for h, lines in cols)
    body = (f'<div class=cap><h2>{e(title)}</h2><p>{e(sub)}</p></div>'
            f'<div style="position:absolute;left:70px;right:70px;top:240px;bottom:70px;display:flex;gap:36px">{blocks}</div>')
    return doc(theme, body)


# ---------------------------------------------------------------- render
def render_all(jobs):
    """jobs: list of (html, out_jpg). Uses node Playwright (shoot.js)."""
    import json
    import subprocess
    here = pathlib.Path(__file__).resolve().parent
    tmp = here / "_cache" / "html"
    tmp.mkdir(parents=True, exist_ok=True)
    pairs = []
    for i, (h, out) in enumerate(jobs):
        f = tmp / f"_img{i}.html"
        f.write_text(h, encoding="utf-8")
        pairs.append([str(f), str(tmp / f"_img{i}.png")])
    (tmp / "jobs.json").write_text(json.dumps(pairs))
    subprocess.run(["node", str(here / "shoot.js"), str(tmp / "jobs.json")], check=True)
    for (h, out), (_, png) in zip(jobs, pairs):
        im = Image.open(png).convert("RGB")
        assert im.size == (3000, 2250), im.size
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
