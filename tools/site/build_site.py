#!/usr/bin/env python3
"""Pre-render catalogue cards into the static HTML (for crawlers / no-JS), then rebuild sitemap + robots.

Fills the regions between markers in docs/*.html:
    <!-- catalog:products -->…<!-- /catalog -->            all products (with category badge)
    <!-- catalog:products:<category> -->…<!-- /catalog -->  one category
    <!-- catalog:bundles -->…<!-- /catalog -->             bundle cards with buy boxes
    <!-- catalog:tools -->…<!-- /catalog -->               free tools
Markup mirrors docs/assets/catalog.js (which refreshes it live). Run after merging product work:
    python3 tools/site/build_site.py [--base https://example.com/]
"""
import argparse
import html
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_sitemap  # noqa: E402

ICONS = {
    "events": '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="30" r="10"/><circle cx="30" cy="30" r="10"/><path d="M20 12l4-5 4 5-4 4z"/></svg>',
    "money": '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="13" width="36" height="25" rx="4"/><path d="M6 20h36M32 29h4"/><path d="M12 13l18-6 3 6"/></svg>',
    "business": '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="15" width="36" height="24" rx="4"/><path d="M18 15v-4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4M6 25h36M22 25v3h4v-3"/></svg>',
}
MARK = re.compile(r"<!-- catalog:([a-z]+)(?::([a-z-]+))? -->.*?<!-- /catalog -->", re.S)


def e(s):
    return html.escape("" if s is None else str(s), quote=True)


def ils(n):
    n = float(n or 0)
    return "₪" + (f"{int(n):,}" if n.is_integer() else f"{n:,.2f}")


def load(slug):
    p = DOCS / "data" / "products" / f"{slug}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def rel(page: pathlib.Path, target: str) -> str:
    """Relative URL from a docs page to a docs-root path like 'p/x/'."""
    depth = len(page.relative_to(DOCS).parts) - 1
    return "../" * depth + target


def product_card(page, p, cat, cat_label):
    live = (DOCS / "p" / p["slug"] / "index.html").exists() and not p.get("placeholder")
    url = rel(page, f"p/{p['slug']}/")
    thumb = (f'<img src="{e(rel(page, p["image"]))}" alt="" loading="lazy" width="640" height="360">'
             if p.get("image") else ICONS.get(cat, ICONS["money"]))
    title = f'<a href="{url}">{e(p["title"])}</a>' if live else e(p["title"])
    return (f'<article class="card product-card{"" if live else " is-soon"}" data-slug="{e(p["slug"])}">'
            f'<div class="thumb {e(cat)}">{thumb}</div><div class="body">'
            + (f'<span class="badge">{e(cat_label)}</span>' if cat_label else "")
            + f'<h3>{title}</h3><p class="sub">{e(p.get("subtitle"))}</p>'
            f'<div class="meta"><span class="price">{ils(p["price_ils"])}</span>'
            + (f'<span class="badge accent">{e(p.get("badge") or "אקסל + Google Sheets")}</span>' if live else '<span class="badge soon">בקרוב</span>')
            + "</div></div></article>")


def bundle_card(b):
    members = [load(s) for s in b.get("bundle_of", [])]
    total = sum(float(m["price_ils"]) for m in members if m)
    save = total - float(b["price_ils"])
    items = "".join(
        f'<li>{e(m["title"] if m else s)}' + (f' <span class="muted num">({ils(m["price_ils"])})</span>' if m else "") + "</li>"
        for m, s in zip(members, b.get("bundle_of", [])))
    return (f'<article class="card pad-lg" id="{e(b["slug"])}" data-slug="{e(b["slug"])}">'
            '<div class="btn-row" style="justify-content:space-between;align-items:center">'
            f'<h3 class="mb-0">{e(b["title"])}</h3>'
            + (f'<span class="badge success">חוסכים {ils(save)}</span>' if save > 0 else "") + "</div>"
            f'<p class="muted mt-1">{e(b.get("subtitle"))}</p><ul class="small">{items}</ul>'
            + (f'<p class="small muted">במקום <s class="num">{ils(total)}</s> בנפרד</p>' if save > 0 else "")
            + f'<div class="buy" data-product="{e(b["slug"])}" data-compact="1"></div></article>')


def tool_card(page, t):
    live = (DOCS / "tools" / t["slug"] / "index.html").exists()
    inner = (f'<span class="ic" aria-hidden="true">{e(t.get("icon") or "🧮")}</span><div><h3>{e(t["title"])}</h3>'
             f'<p>{e(t.get("description"))}</p>' + ("" if live else '<span class="badge soon mt-1">בקרוב</span>') + "</div>")
    if live:
        return f'<a class="card tool-card" href="{rel(page, "tools/" + t["slug"] + "/")}" data-slug="{e(t["slug"])}">{inner}</a>'
    return f'<div class="card tool-card" data-slug="{e(t["slug"])}">{inner}</div>'


def render(page, kind, arg, idx, tools):
    if kind == "products":
        out = []
        for x in idx["products"]:
            if arg and x["category"] != arg:
                continue
            p = load(x["slug"])
            if p:
                out.append(product_card(page, p, x["category"], "" if arg else idx.get("categories", {}).get(x["category"], "")))
        return "".join(out)
    if kind == "bundles":
        return "".join(bundle_card(b) for b in map(load, idx["bundles"]) if b)
    if kind == "tools":
        return "".join(tool_card(page, t) for t in tools.get("tools", []))
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=build_sitemap.DEFAULT_BASE)
    a = ap.parse_args()
    idx = json.loads((DOCS / "data/products/index.json").read_text(encoding="utf-8"))
    tools = json.loads((DOCS / "data/tools.json").read_text(encoding="utf-8"))
    changed = 0
    for page in DOCS.rglob("*.html"):
        if "/dl/" in page.as_posix():
            continue
        src = page.read_text(encoding="utf-8")
        if "<!-- catalog:" not in src:
            continue
        new = MARK.sub(lambda m: m.group(0).split("-->")[0] + "-->" + render(page, m.group(1), m.group(2), idx, tools) + "<!-- /catalog -->", src)
        if new != src:
            page.write_text(new, encoding="utf-8")
            changed += 1
            print("rendered", page.relative_to(REPO))
    print(f"{changed} page(s) updated")
    build_sitemap.build(a.base)


if __name__ == "__main__":
    main()
