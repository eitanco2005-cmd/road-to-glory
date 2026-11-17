#!/usr/bin/env python3
"""Build the three free RTL Landing Kit templates (plain CSS + Tailwind variant each).

    python3 devkit/tools/build_free.py

Writes devkit/templates/<name>/index.html and tailwind.html from the copy in content.py.
After changing Tailwind classes, rebuild css/tailwind.css: `npm install && npm run build:tw` (in devkit/).
The output is plain static HTML (no build step needed to use it); this script only exists so the
three languages stay in sync. Edit the generated HTML directly if you prefer — it is yours.
"""
import html
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
sys.path.insert(0, str(HERE))
from content import COMMON, LAUNCH, POCKET, STUDIO  # noqa: E402

FONTS = ("https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800"
         "&family=Noto+Kufi+Arabic:wght@400;500;700;800&family=Inter:wght@400;500;700;800&display=swap")

ICONS = {
    "board": '<path d="M4 5h16v14H4zM9 5v14M14 5v14"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "plug": '<path d="M9 7V3M15 7V3M7 7h10v4a5 5 0 0 1-10 0zM12 16v5"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "chat": '<path d="M4 5h16v11H8l-4 4z"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "pen": '<path d="M4 20l4-1 11-11-3-3L5 16zM14 6l3 3"/>',
    "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "apple": '<path d="M16 3c-1.2.1-2.6.9-3.3 2-.7.9-1.2 2.3-1 3.5 1.3.1 2.6-.7 3.4-1.7.7-1 1.1-2.3.9-3.8zM19.5 17c-.6 1.4-1 2-1.8 3.2-1.1 1.6-2.7 1.6-3.4 1.6-1 0-1.5-.6-3-.6s-2 .6-3 .6c-.8 0-2.2-.1-3.4-1.7C2.6 17 2.3 12.9 3.9 10.6c1-1.5 2.6-2.4 4.1-2.4s2.5.8 3.8.8 2.1-.8 3.9-.8c1.3 0 2.8.7 3.8 2-3.3 1.8-2.8 6.6 0 6.8z"/>',
    "play": '<path d="M5 3l14 9-14 9z"/>',
}


def icon(name, cls="", flip=False):
    c = (cls + (" flip" if flip else "")).strip()
    return (f'<svg{f" class={chr(34)}{c}{chr(34)}" if c else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


class T:
    """Translation helper: t('key') -> Hebrew text, wrapped so the switcher can replace it."""

    def __init__(self, copy):
        self.d = {lang: {**COMMON[lang], **copy[lang]} for lang in ("he", "ar", "en")}

    def __call__(self, key, tag="span", cls="", attrs=""):
        c = f' class="{cls}"' if cls else ""
        return f'<{tag}{c} data-i18n="{key}"{attrs}>{self.d["he"][key]}</{tag}>'

    def bdi(self, key):
        """Numbers/amounts: isolated from the surrounding text direction, still translatable."""
        return f'<bdi data-i18n="{key}">{self.d["he"][key]}</bdi>'

    def raw(self, key):
        return self.d["he"][key]

    def json(self):
        return json.dumps(self.d, ensure_ascii=False, indent=1).replace("</", "<\\/")


def head(t, title_key, tailwind=False, theme=""):
    css = ('<link rel="stylesheet" href="../../css/tailwind.css">'
           if tailwind else '<link rel="stylesheet" href="../../css/rtl-kit.css">')
    return f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t.raw(title_key))}</title>
<meta name="description" content="{html.escape(t.raw('lead'))}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
{css}{theme}
</head>"""


def lang_select(cls):
    return (f'<label class="sr-only" for="lang">Language / שפה / اللغة</label>'
            f'<select id="lang" class="{cls}" data-lang-switch><option value="he">עברית</option>'
            f'<option value="ar">العربية</option><option value="en">English</option></select>')


def tail(t):
    return (f'<script type="application/json" id="i18n" data-default="he">{t.json()}</script>\n'
            '<script src="../../js/rtl-kit.js"></script>\n</body>\n</html>\n')


# ---------------------------------------------------------------- plain CSS version
def nav(t, links):
    lis = "".join(f'<li><a href="#{a}">{t(k)}</a></li>' for a, k in links)
    return f"""<body>
<a class="skip" href="#main">{t('skip')}</a>
<header class="nav">
 <div class="container">
  <a class="brand" href="#"><span class="brand-mark" aria-hidden="true"></span>{t('brand')}</a>
  <button class="menu-btn" type="button" data-menu aria-expanded="false"><span class="sr-only" data-i18n="menu">{t.raw('menu')}</span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <ul class="nav-links">{lis}</ul>
  <div class="nav-tools">{lang_select('lang-select')}<a class="btn sm" href="#{links[-1][0]}">{t('n_cta')}</a></div>
 </div>
</header>
<main id="main">"""


def footer(t, extra=""):
    return f"""</main>
<footer class="footer">
 <div class="container">
  <div class="cols">
   <div><a class="brand" href="#"><span class="brand-mark" aria-hidden="true"></span>{t('brand')}</a>{extra}</div>
   <div><h4>{t('f_product', 'span')}</h4><ul><li><a href="#">{t('n1')}</a></li><li><a href="#">{t('n3')}</a></li></ul></div>
   <div><h4>{t('f_company', 'span')}</h4><ul><li><a href="#">{t('f_about')}</a></li><li><a href="#">{t('f_jobs')}</a></li><li><a href="#">{t('f_contact')}</a></li></ul></div>
   <div><h4>{t('f_legal', 'span')}</h4><ul><li><a href="#">{t('f_terms')}</a></li><li><a href="#">{t('f_privacy')}</a></li><li><a href="#">{t('f_access')}</a></li></ul></div>
  </div>
  <div class="fine">{t('f_rights')}{t('f_made')}</div>
 </div>
</footer>
"""


def faq(t, n=3):
    return "".join(f'<details><summary>{t(f"q{i}")}</summary><div>{t(f"a{i}", "p", "mb-0")}</div></details>' for i in range(1, n + 1))


def email_form(t, btn, ok, light=False):
    return f"""<form class="form" data-demo>
     <div class="inline-form"><label class="sr-only" for="em">{t.raw('email_l')}</label>
      <input id="em" type="email" dir="ltr" required autocomplete="email" placeholder="{t.raw('email_ph')}">
      <button class="btn{' light' if light else ''}" type="submit">{t(btn)}</button></div>
     <p class="form-ok" data-ok hidden tabindex="-1">{t(ok)}</p>
    </form>"""


def launch_plain(t):
    feats = [("board", 1), ("chart", 2), ("lock", 3), ("plug", 4), ("shield", 5), ("chat", 6)]
    plans = ""
    for i in (1, 2, 3):
        feat = i == 2
        plans += (f'<article class="card plan{" featured" if feat else ""}">' + (t("p2tag", "span", "tag") if feat else "")
                  + f'{t(f"p{i}", "h3")}{t(f"p{i}d", "p", "muted mb-0")}<div class="price">{t(f"p{i}p")} <small>{t(f"p{i}u")}</small></div>'
                  f'<ul><li>{t(f"p{i}a")}</li><li>{t(f"p{i}b")}</li><li>{t(f"p{i}c")}</li></ul>'
                  f'<a class="btn{"" if feat else " ghost"}" href="#signup">{t(f"p{i}btn")}</a></article>')
    return (head(t, "_title") + "\n" + nav(t, [("features", "n1"), ("how", "n2"), ("pricing", "n3"), ("faq", "n4")]) + f"""
<section class="hero">
 <div class="container split">
  <div>
   {t('eyebrow', 'span', 'eyebrow')}
   {t('h1', 'h1')}
   {t('lead', 'p', 'lead')}
   <div class="row"><a class="btn" href="#signup">{t('cta1')} {icon('arrow', flip=True)}</a><a class="btn ghost" href="#how">{t('cta2')}</a></div>
   {t('note', 'p', 'hero-note')}
  </div>
  <div class="mock" aria-hidden="true">
   <div class="mock-bar"><i></i><i></i><i></i></div>
   <div class="mock-body">
    <div class="mock-side"><span></span><span></span><span></span><span></span><span></span></div>
    <div class="mock-main">
     <div class="mock-kpis"><div>{t('k1')}<b><bdi>24</bdi></b></div><div>{t('k2')}<b><bdi>92%</bdi></b></div><div>{t('k3')}<b><bdi>68%</bdi></b></div></div>
     <div class="mock-chart"><i style="block-size:40%"></i><i style="block-size:65%"></i><i style="block-size:50%"></i><i style="block-size:80%"></i><i style="block-size:70%"></i><i style="block-size:95%"></i><i style="block-size:60%"></i></div>
     <span class="mock-line" style="inline-size:80%"></span><span class="mock-line" style="inline-size:55%"></span>
    </div>
   </div>
  </div>
 </div>
</section>
<section class="section alt" id="features">
 <div class="container">
  <div class="section-head center">{t('fh_eyebrow', 'span', 'eyebrow')}{t('fh', 'h2')}{t('fl', 'p', 'lead mb-0')}</div>
  <div class="grid c3">""" + "".join(
        f'<article class="card feature"><div class="icon-tile">{icon(ic)}</div>{t(f"f{n}", "h3")}{t(f"f{n}d", "p")}</article>' for ic, n in feats) + f"""</div>
 </div>
</section>
<section class="section" id="how">
 <div class="container">
  <div class="section-head">{t('sh', 'h2')}</div>
  <div class="steps">""" + "".join(f'<div class="step">{t(f"s{i}", "h3")}{t(f"s{i}d", "p", "muted mb-0")}</div>' for i in (1, 2, 3)) + f"""</div>
 </div>
</section>
<section class="section alt" id="pricing">
 <div class="container">
  <div class="section-head center">{t('ph', 'h2')}{t('pl', 'p', 'lead mb-0')}</div>
  <div class="pricing">{plans}</div>
 </div>
</section>
<section class="section" id="faq">
 <div class="container">
  <div class="section-head center">{t('qh', 'h2')}</div>
  <div class="faq">{faq(t)}</div>
 </div>
</section>
<section class="section" id="signup" style="padding-block-start:0">
 <div class="container">
  <div class="cta-band">
   <div>{t('ch', 'h2')}{t('cl', 'p')}</div>
   {email_form(t, 'cbtn', 'cok', light=True)}
  </div>
 </div>
</section>
""" + footer(t) + tail(t))


def studio_plain(t):
    theme = "\n<style>:root{--c-primary:#0f766e;--c-primary-soft:#d7f2ee;--c-accent:#f97316}@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--c-primary:#2dd4bf;--c-primary-soft:#133b37}}</style>"
    works = [("w1", "#0f766e", "#f97316"), ("w2", "#2563eb", "#22d3ee"), ("w3", "#b45309", "#fde68a"), ("w4", "#334155", "#94a3b8")]
    return (head(t, "_title", theme=theme) + "\n" + nav(t, [("services", "n1"), ("work", "n2"), ("process", "n3"), ("contact", "n4")]) + f"""
<section class="hero center">
 <div class="container">
  {t('eyebrow', 'span', 'eyebrow')}
  {t('h1', 'h1')}
  {t('lead', 'p', 'lead')}
  <div class="row"><a class="btn" href="#contact">{t('cta1')} {icon('arrow', flip=True)}</a><a class="btn ghost" href="#work">{t('cta2')}</a></div>
  <div class="stats mt-2">""" + "".join(f'<div class="stat"><b>{t.bdi(f"st{i}")}</b>{t(f"st{i}l")}</div>' for i in (1, 2, 3, 4)) + f"""</div>
 </div>
</section>
<section class="section alt" id="services">
 <div class="container">
  <div class="section-head">{t('svh', 'h2')}{t('svl', 'p', 'lead mb-0')}</div>
  <div class="grid c3">""" + "".join(
        f'<article class="card raised feature"><div class="icon-tile">{icon(ic)}</div>{t(f"sv{i}", "h3")}{t(f"sv{i}d", "p")}</article>'
        for i, ic in ((1, "spark"), (2, "pen"), (3, "code"))) + f"""</div>
 </div>
</section>
<section class="section" id="work">
 <div class="container">
  <div class="section-head">{t('wh', 'h2')}</div>
  <div class="grid c2">""" + "".join(
        f'<a class="work" href="#" style="text-decoration:none;color:inherit"><div class="tile-art" style="--a:{a};--b:{b}" role="img" aria-label="{html.escape(t.raw(k))}"></div>'
        f'<h3 style="margin-block:1rem .2rem">{t(k)}</h3>{t(k + "t", "p", "muted")}</a>' for k, a, b in works) + f"""</div>
 </div>
</section>
<section class="section alt" id="process">
 <div class="container">
  <div class="section-head">{t('prh', 'h2')}</div>
  <div class="steps">""" + "".join(f'<div class="step">{t(f"pr{i}", "h3")}{t(f"pr{i}d", "p", "muted mb-0")}</div>' for i in (1, 2, 3, 4)) + f"""</div>
 </div>
</section>
<section class="section" id="contact">
 <div class="container split" style="align-items:start">
  <div>{t('coh', 'h2')}{t('col', 'p', 'lead')}
   <ul class="check-list"><li>{t('addr')}</li><li><a href="tel:+97235550123" dir="ltr"><bdi data-i18n="phone">{t.raw('phone')}</bdi></a></li><li><a href="mailto:hello@example.com" dir="ltr">hello@example.com</a></li></ul>
  </div>
  <form class="form card raised" data-demo>
   <div class="field"><label for="fn" data-i18n="fn">{t.raw('fn')}</label><input id="fn" name="name" required autocomplete="name"></div>
   <div class="grid c2" style="gap:1rem">
    <div class="field"><label for="fe" data-i18n="email_l">{t.raw('email_l')}</label><input id="fe" type="email" dir="ltr" required autocomplete="email" placeholder="you@example.com"></div>
    <div class="field"><label for="fp" data-i18n="fp">{t.raw('fp')}</label><input id="fp" type="tel" dir="ltr" autocomplete="tel" placeholder="050-000-0000"></div>
   </div>
   <div class="field"><label for="fm" data-i18n="fm">{t.raw('fm')}</label><textarea id="fm" dir="auto"></textarea></div>
   <button class="btn" type="submit">{t('fsend')} {icon('arrow', flip=True)}</button>
   <p class="form-ok" data-ok hidden tabindex="-1">{t('fok')}</p>
  </form>
 </div>
</section>
""" + footer(t) + tail(t))


def pocket_plain(t):
    theme = "\n<style>:root{--c-primary:#e11d48;--c-primary-soft:#ffe4ea;--c-accent:#8b5cf6}@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--c-primary:#fb7185;--c-primary-soft:#3b1520}}</style>"
    phone = f"""<div class="phone" aria-hidden="true">
     <div class="ph-card primary">{t('ph_bal')}<b>{t.bdi('ph_amt')}</b></div>
     <div class="ph-card row" style="justify-content:space-between">{t('ph_r1')}<bdi>−312</bdi></div>
     <div class="ph-card row" style="justify-content:space-between">{t('ph_r2')}<bdi>−180</bdi></div>
     <div class="ph-card">{t('ph_r3')}<div style="block-size:8px;border-radius:4px;background:var(--c-border);margin-block-start:.5rem"><div style="inline-size:64%;block-size:100%;border-radius:4px;background:var(--c-primary)"></div></div></div>
    </div>"""
    stores = (f'<div class="row"><a class="btn" href="#">{icon("apple")}{t("store1")}</a>'
              f'<a class="btn ghost" href="#">{icon("play")}{t("store2")}</a></div>')
    return (head(t, "_title", theme=theme) + "\n" + nav(t, [("features", "n1"), ("privacy", "n2"), ("faq", "n3"), ("download", "n4")]) + f"""
<section class="hero">
 <div class="container split">
  <div>
   {t('eyebrow', 'span', 'eyebrow')}
   {t('h1', 'h1')}
   {t('lead', 'p', 'lead')}
   {stores}
   {t('note', 'p', 'hero-note')}
  </div>
  {phone}
 </div>
</section>
<section class="section alt" id="features">
 <div class="container">
  <div class="section-head center">{t('fh', 'h2')}</div>
  <div class="grid c3">""" + "".join(
        f'<article class="card feature text-center"><div class="icon-tile" style="margin-inline:auto">{icon(ic)}</div>{t(f"f{i}", "h3")}{t(f"f{i}d", "p")}</article>'
        for i, ic in ((1, "tag"), (2, "bell"), (3, "target"))) + f"""</div>
  <div class="stats mt-2">""" + "".join(f'<div class="stat"><b>{t.bdi(f"st{i}")}</b>{t(f"st{i}l")}</div>' for i in (1, 2, 3)) + f"""</div>
 </div>
</section>
<section class="section" id="privacy">
 <div class="container split">
  <div class="card raised" style="display:grid;place-items:center;min-block-size:240px"><div class="icon-tile" style="inline-size:96px;block-size:96px;border-radius:28px;margin:0">{icon('shield')}</div></div>
  <div>{t('pvh', 'h2')}{t('pvl', 'p', 'lead')}</div>
 </div>
</section>
<section class="section alt" id="faq">
 <div class="container">
  <div class="section-head center">{t('qh', 'h2')}</div>
  <div class="faq">{faq(t)}</div>
 </div>
</section>
<section class="section" id="download">
 <div class="container">
  <div class="cta-band">
   <div>{t('dh', 'h2')}{t('dl', 'p')}</div>
   <div class="row"><a class="btn light" href="#">{icon("apple")}{t("store1")}</a><a class="btn light" href="#">{icon("play")}{t("store2")}</a></div>
  </div>
 </div>
</section>
""" + footer(t) + tail(t))


# ---------------------------------------------------------------- Tailwind version
# Only logical utilities: ms-/me- (margin-inline), ps-/pe-, start-/end-, text-start/end, border-s/e, rounded-s/e.
TW_BTN = "inline-flex items-center justify-center gap-2 min-h-12 px-6 rounded-full font-bold transition hover:-translate-y-px"
TW_PRI = TW_BTN + " bg-{c}-600 text-white hover:bg-{c}-700 dark:bg-{c}-400 dark:text-slate-950"
TW_GHOST = TW_BTN + " border-2 border-slate-200 dark:border-slate-700 hover:border-slate-900 dark:hover:border-slate-200"


def tw_nav(t, links, c):
    lis = "".join(f'<li><a class="block py-3 md:py-0 text-slate-600 dark:text-slate-300 font-semibold hover:text-slate-900 dark:hover:text-white" href="#{a}">{t(k)}</a></li>' for a, k in links)
    return f"""<body class="bg-white text-slate-900 dark:bg-slate-950 dark:text-slate-100 antialiased">
<a class="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:start-4 focus:z-50 focus:bg-slate-900 focus:text-white focus:px-4 focus:py-2 focus:rounded-lg" href="#main">{t('skip')}</a>
<header class="nav sticky top-0 z-40 bg-white/85 dark:bg-slate-950/85 backdrop-blur border-b border-slate-200 dark:border-slate-800">
 <div class="mx-auto max-w-6xl px-4 sm:px-8 flex items-center gap-5 min-h-[68px] relative">
  <a class="flex items-center gap-2 font-extrabold text-lg" href="#"><span class="size-8 rounded-lg bg-gradient-to-br from-{c}-600 to-amber-400" aria-hidden="true"></span>{t('brand')}</a>
  <button class="md:hidden ms-auto size-11 grid place-items-center rounded-xl border border-slate-200 dark:border-slate-700" type="button" data-menu aria-expanded="false"><span class="sr-only" data-i18n="menu">{t.raw('menu')}</span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <ul class="nav-links hidden md:flex md:ms-auto md:gap-6 absolute md:static inset-x-0 top-full flex-col md:flex-row bg-white dark:bg-slate-950 md:bg-transparent px-4 md:px-0 pb-4 md:pb-0 border-b md:border-0 border-slate-200 dark:border-slate-800">{lis}</ul>
  <div class="hidden md:flex items-center gap-3">{lang_select('min-h-10 rounded-full border border-slate-200 dark:border-slate-700 bg-transparent px-3 text-sm')}<a class="{TW_PRI.format(c=c)} min-h-10 px-4 text-sm" href="#{links[-1][0]}">{t('n_cta')}</a></div>
 </div>
</header>
<main id="main">"""


def tw_footer(t):
    a = "text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
    col = lambda h, items: f'<div><h4 class="font-bold mb-3">{t(h)}</h4><ul class="space-y-2">' + "".join(f'<li><a class="{a}" href="#">{t(k)}</a></li>' for k in items) + "</ul></div>"
    return f"""</main>
<footer class="border-t border-slate-200 dark:border-slate-800 py-12 text-[.95rem]">
 <div class="mx-auto max-w-6xl px-4 sm:px-8">
  <div class="grid grid-cols-2 md:grid-cols-5 gap-8">
   <div class="col-span-2"><a class="font-extrabold text-lg" href="#">{t('brand')}</a><div class="mt-3 md:hidden">{lang_select('min-h-10 rounded-full border border-slate-200 dark:border-slate-700 bg-transparent px-3 text-sm').replace('id="lang"', 'id="lang2"').replace('for="lang"', 'for="lang2"')}</div></div>
   {col('f_product', ['n1', 'n3'])}{col('f_company', ['f_about', 'f_jobs', 'f_contact'])}{col('f_legal', ['f_terms', 'f_privacy', 'f_access'])}
  </div>
  <div class="mt-8 pt-5 border-t border-slate-200 dark:border-slate-800 flex flex-wrap justify-between gap-4 text-slate-500">{t('f_rights')}{t('f_made')}</div>
 </div>
</footer>
"""


def tw_section(inner, alt=False, sid=""):
    return (f'<section{f" id={chr(34)}{sid}{chr(34)}" if sid else ""} class="py-16 sm:py-24 {"bg-slate-50 dark:bg-slate-900" if alt else ""}">'
            f'<div class="mx-auto max-w-6xl px-4 sm:px-8">{inner}</div></section>\n')


def tw_head2(t, k, lead=None, center=False, c="indigo", eyebrow=None):
    e = t(eyebrow, "span", f"inline-block rounded-full bg-{c}-50 dark:bg-{c}-950 text-{c}-700 dark:text-{c}-300 text-sm font-bold px-3 py-1 mb-4") if eyebrow else ""
    lead_html = t(lead, "p", "mt-3 text-lg text-slate-500 dark:text-slate-400") if lead else ""
    return f'<div class="max-w-2xl mb-10 {"mx-auto text-center" if center else ""}">{e}{t(k, "h2", "text-3xl sm:text-4xl font-extrabold tracking-tight")}{lead_html}</div>'


def tw_card(ic, h, d, c):
    return (f'<article class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 p-6">'
            f'<div class="size-12 rounded-xl grid place-items-center bg-{c}-50 dark:bg-{c}-950 text-{c}-600 dark:text-{c}-300 mb-4">{icon(ic, "size-6")}</div>'
            f'{h}{d}</article>')


def tw_faq(t):
    return '<div class="max-w-3xl mx-auto space-y-3">' + "".join(
        f'<details class="group rounded-xl border border-slate-200 dark:border-slate-800"><summary class="cursor-pointer list-none flex justify-between gap-4 p-5 font-bold">{t(f"q{i}")}<span class="text-xl leading-none transition group-open:rotate-45" aria-hidden="true">+</span></summary>'
        f'{t(f"a{i}", "p", "px-5 pb-5 text-slate-500 dark:text-slate-400")}</details>' for i in (1, 2, 3)) + "</div>"


def tw_steps(t, prefix, n):
    return '<ol class="grid gap-6 sm:grid-cols-2 lg:grid-cols-' + str(n) + '">' + "".join(
        f'<li class="relative ps-14"><span class="absolute start-0 top-0 size-10 rounded-full grid place-items-center font-extrabold bg-slate-900 text-white dark:bg-white dark:text-slate-900">{i}</span>'
        f'{t(f"{prefix}{i}", "h3", "font-bold text-lg")}{t(f"{prefix}{i}d", "p", "text-slate-500 dark:text-slate-400")}</li>' for i in range(1, n + 1)) + "</ol>"


def tw_h1(t, c):
    return t("h1", "h1", f"text-4xl sm:text-6xl font-extrabold tracking-tight leading-[1.1] [&_.hl]:text-{c}-600 dark:[&_.hl]:text-{c}-400")


def tw_eyebrow(t, c):
    return t("eyebrow", "span", f"inline-block rounded-full bg-{c}-50 dark:bg-{c}-950 text-{c}-700 dark:text-{c}-300 text-sm font-bold px-3 py-1 mb-5")


def launch_tw(t):
    c = "indigo"
    plans = ""
    for i in (1, 2, 3):
        f = i == 2
        plans += (f'<article class="relative flex flex-col gap-2 rounded-2xl p-7 bg-white dark:bg-slate-950 {"border-2 border-indigo-600 shadow-xl" if f else "border border-slate-200 dark:border-slate-800"}">'
                  + (t("p2tag", "span", "absolute -top-3 start-6 rounded-full bg-indigo-600 text-white text-xs font-bold px-3 py-1") if f else "")
                  + t(f"p{i}", "h3", "text-xl font-bold") + t(f"p{i}d", "p", "text-slate-500")
                  + f'<div class="my-2 text-4xl font-extrabold">{t(f"p{i}p")} <small class="text-base font-medium text-slate-500">{t(f"p{i}u")}</small></div>'
                  + '<ul class="space-y-2 mb-6">' + "".join(f'<li class="flex gap-2"><span class="text-indigo-600 font-extrabold" aria-hidden="true">✓</span>{t(f"p{i}{x}")}</li>' for x in "abc") + "</ul>"
                  + f'<a class="mt-auto {TW_PRI.format(c=c) if f else TW_GHOST}" href="#signup">{t(f"p{i}btn")}</a></article>')
    feats = [("board", 1), ("chart", 2), ("lock", 3), ("plug", 4), ("shield", 5), ("chat", 6)]
    return (head(t, "_title", tailwind=True) + "\n" + tw_nav(t, [("features", "n1"), ("how", "n2"), ("pricing", "n3"), ("faq", "n4")], c)
            + tw_section(f"""<div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>{tw_eyebrow(t, c)}{tw_h1(t, c)}{t('lead', 'p', 'mt-5 text-xl text-slate-500 dark:text-slate-400')}
   <div class="mt-8 flex flex-wrap gap-3"><a class="{TW_PRI.format(c=c)}" href="#signup">{t('cta1')} {icon('arrow', 'size-5', flip=True)}</a><a class="{TW_GHOST}" href="#how">{t('cta2')}</a></div>
   {t('note', 'p', 'mt-4 text-sm text-slate-500')}</div>
  <div class="rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden bg-white dark:bg-slate-900" aria-hidden="true">
   <div class="flex gap-1.5 p-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950"><i class="size-2.5 rounded-full bg-slate-300"></i><i class="size-2.5 rounded-full bg-slate-300"></i><i class="size-2.5 rounded-full bg-slate-300"></i></div>
   <div class="grid grid-cols-[30%_1fr] min-h-72"><div class="border-e border-slate-200 dark:border-slate-800 p-4 space-y-3"><div class="h-2.5 rounded bg-indigo-100 dark:bg-indigo-900"></div><div class="h-2.5 rounded bg-slate-100 dark:bg-slate-800"></div><div class="h-2.5 rounded bg-slate-100 dark:bg-slate-800"></div><div class="h-2.5 rounded bg-slate-100 dark:bg-slate-800"></div></div>
    <div class="p-4 space-y-4"><div class="grid grid-cols-3 gap-2 text-xs text-slate-500">""" + "".join(
                f'<div class="rounded-lg border border-slate-200 dark:border-slate-800 p-2">{t(k)}<b class="block text-lg text-slate-900 dark:text-white"><bdi>{v}</bdi></b></div>' for k, v in (("k1", "24"), ("k2", "92%"), ("k3", "68%"))) + """</div>
     <div class="flex items-end gap-2 h-28">""" + "".join(f'<i class="flex-1 rounded-t-md bg-gradient-to-b from-indigo-500 to-indigo-200" style="height:{h}%"></i>' for h in (40, 65, 50, 80, 70, 95, 60)) + """</div></div></div>
  </div></div>""")
            + tw_section(tw_head2(t, "fh", "fl", True, c, "fh_eyebrow") + '<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">' + "".join(
                tw_card(ic, t(f"f{n}", "h3", "text-lg font-bold mb-1"), t(f"f{n}d", "p", "text-slate-500 dark:text-slate-400"), c) for ic, n in feats) + "</div>", True, "features")
            + tw_section(tw_head2(t, "sh", c=c) + tw_steps(t, "s", 3), False, "how")
            + tw_section(tw_head2(t, "ph", "pl", True, c) + f'<div class="grid gap-6 md:grid-cols-3 items-stretch">{plans}</div>', True, "pricing")
            + tw_section(tw_head2(t, "qh", center=True, c=c) + tw_faq(t), False, "faq")
            + tw_section(f"""<div class="rounded-3xl p-8 sm:p-14 bg-gradient-to-br from-indigo-600 to-violet-500 text-white grid md:grid-cols-2 gap-8 items-center">
  <div>{t('ch', 'h2', 'text-3xl font-extrabold')}{t('cl', 'p', 'mt-2 text-white/85')}</div>
  <form data-demo><div class="flex flex-wrap gap-2"><label class="sr-only" for="em">{t.raw('email_l')}</label><input id="em" type="email" dir="ltr" required placeholder="you@example.com" class="flex-1 min-w-52 min-h-12 rounded-xl px-4 text-slate-900 text-end">
   <button class="{TW_BTN} bg-white text-slate-900" type="submit">{t('cbtn')}</button></div><p data-ok hidden tabindex="-1" class="mt-3 rounded-xl bg-white/15 px-4 py-3 font-semibold">{t('cok')}</p></form>
 </div>""", False, "signup")
            + tw_footer(t) + tail(t))


def studio_tw(t):
    c = "teal"
    works = [("w1", "from-teal-600 to-orange-400"), ("w2", "from-blue-600 to-cyan-400"), ("w3", "from-amber-700 to-amber-200"), ("w4", "from-slate-700 to-slate-400")]
    inp = "w-full min-h-12 rounded-xl border-[1.5px] border-slate-200 dark:border-slate-700 bg-transparent px-4 py-2 focus:border-teal-600 focus:outline-none focus:ring-4 focus:ring-teal-100 dark:focus:ring-teal-900"
    return (head(t, "_title", tailwind=True) + "\n" + tw_nav(t, [("services", "n1"), ("work", "n2"), ("process", "n3"), ("contact", "n4")], c)
            + tw_section(f"""<div class="text-center max-w-3xl mx-auto">{tw_eyebrow(t, c)}{tw_h1(t, c)}{t('lead', 'p', 'mt-5 text-xl text-slate-500 dark:text-slate-400')}
   <div class="mt-8 flex flex-wrap gap-3 justify-center"><a class="{TW_PRI.format(c=c)}" href="#contact">{t('cta1')} {icon('arrow', 'size-5', flip=True)}</a><a class="{TW_GHOST}" href="#work">{t('cta2')}</a></div></div>
  <div class="mt-14 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">""" + "".join(
                f'<div><b class="block text-4xl font-extrabold text-teal-600 dark:text-teal-400">{t.bdi(f"st{i}")}</b>{t(f"st{i}l", "span", "text-slate-500")}</div>' for i in (1, 2, 3, 4)) + "</div>")
            + tw_section(tw_head2(t, "svh", "svl", c=c) + '<div class="grid gap-6 md:grid-cols-3">' + "".join(
                tw_card(ic, t(f"sv{i}", "h3", "text-lg font-bold mb-1"), t(f"sv{i}d", "p", "text-slate-500 dark:text-slate-400"), c) for i, ic in ((1, "spark"), (2, "pen"), (3, "code"))) + "</div>", True, "services")
            + tw_section(tw_head2(t, "wh", c=c) + '<div class="grid gap-8 sm:grid-cols-2">' + "".join(
                f'<a href="#" class="group"><div class="aspect-[4/3] rounded-2xl bg-gradient-to-br {g} transition group-hover:scale-[1.01]" role="img" aria-label="{html.escape(t.raw(k))}"></div>'
                f'{t(k, "h3", "mt-4 text-lg font-bold")}{t(k + "t", "p", "text-slate-500")}</a>' for k, g in works) + "</div>", False, "work")
            + tw_section(tw_head2(t, "prh", c=c) + tw_steps(t, "pr", 4), True, "process")
            + tw_section(f"""<div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>{t('coh', 'h2', 'text-3xl sm:text-4xl font-extrabold')}{t('col', 'p', 'mt-3 text-lg text-slate-500')}
   <ul class="mt-6 space-y-2"><li>{t('addr')}</li><li><a class="text-teal-700 dark:text-teal-300" href="tel:+97235550123" dir="ltr"><bdi data-i18n="phone">{t.raw('phone')}</bdi></a></li><li><a class="text-teal-700 dark:text-teal-300" href="mailto:hello@example.com" dir="ltr">hello@example.com</a></li></ul></div>
  <form data-demo class="rounded-2xl shadow-xl border border-slate-100 dark:border-slate-800 p-6 sm:p-8 space-y-4">
   <div><label class="block font-semibold mb-1" for="fn" data-i18n="fn">{t.raw('fn')}</label><input class="{inp}" id="fn" required autocomplete="name"></div>
   <div class="grid sm:grid-cols-2 gap-4"><div><label class="block font-semibold mb-1" for="fe" data-i18n="email_l">{t.raw('email_l')}</label><input class="{inp} text-end" id="fe" type="email" dir="ltr" required placeholder="you@example.com"></div>
   <div><label class="block font-semibold mb-1" for="fp" data-i18n="fp">{t.raw('fp')}</label><input class="{inp} text-end" id="fp" type="tel" dir="ltr" placeholder="050-000-0000"></div></div>
   <div><label class="block font-semibold mb-1" for="fm" data-i18n="fm">{t.raw('fm')}</label><textarea class="{inp} min-h-32" id="fm" dir="auto"></textarea></div>
   <button class="{TW_PRI.format(c=c)} w-full" type="submit">{t('fsend')} {icon('arrow', 'size-5', flip=True)}</button>
   <p data-ok hidden tabindex="-1" class="rounded-xl bg-teal-50 dark:bg-teal-950 px-4 py-3 font-semibold">{t('fok')}</p>
  </form></div>""", False, "contact")
            + tw_footer(t) + tail(t))


def pocket_tw(t):
    c = "rose"
    stores = lambda light: (f'<a class="{TW_BTN} {"bg-white text-slate-900" if light else "bg-slate-900 text-white dark:bg-white dark:text-slate-900"}" href="#">{icon("apple", "size-5")}{t("store1")}</a>'
                            f'<a class="{TW_BTN} {"bg-white/15 text-white" if light else "border-2 border-slate-200 dark:border-slate-700"}" href="#">{icon("play", "size-5")}{t("store2")}</a>')
    phone = f"""<div class="relative mx-auto w-72 aspect-[9/19] rounded-[44px] border-[10px] border-slate-900 bg-white dark:bg-slate-900 shadow-2xl p-4 pt-8 space-y-3" aria-hidden="true">
   <div class="absolute top-2 inset-x-0 mx-auto w-1/3 h-5 rounded-b-xl bg-slate-900"></div>
   <div class="rounded-2xl p-4 bg-rose-600 text-white text-sm">{t('ph_bal')}<b class="block text-2xl">{t.bdi('ph_amt')}</b></div>
   <div class="rounded-2xl p-4 bg-slate-100 dark:bg-slate-800 text-sm flex justify-between">{t('ph_r1')}<bdi>−312</bdi></div>
   <div class="rounded-2xl p-4 bg-slate-100 dark:bg-slate-800 text-sm flex justify-between">{t('ph_r2')}<bdi>−180</bdi></div>
   <div class="rounded-2xl p-4 bg-slate-100 dark:bg-slate-800 text-sm">{t('ph_r3')}<div class="mt-2 h-2 rounded bg-slate-200 dark:bg-slate-700"><div class="h-full w-2/3 rounded bg-rose-600"></div></div></div>
  </div>"""
    return (head(t, "_title", tailwind=True) + "\n" + tw_nav(t, [("features", "n1"), ("privacy", "n2"), ("faq", "n3"), ("download", "n4")], c)
            + tw_section(f"""<div class="grid lg:grid-cols-2 gap-12 items-center"><div>{tw_eyebrow(t, c)}{tw_h1(t, c)}{t('lead', 'p', 'mt-5 text-xl text-slate-500 dark:text-slate-400')}
   <div class="mt-8 flex flex-wrap gap-3">{stores(False)}</div>{t('note', 'p', 'mt-4 text-sm text-slate-500')}</div>{phone}</div>""")
            + tw_section(tw_head2(t, "fh", center=True, c=c) + '<div class="grid gap-6 md:grid-cols-3 text-center">' + "".join(
                tw_card(ic, t(f"f{i}", "h3", "text-lg font-bold mb-1"), t(f"f{i}d", "p", "text-slate-500 dark:text-slate-400"), c).replace("mb-4", "mb-4 mx-auto") for i, ic in ((1, "tag"), (2, "bell"), (3, "target"))) + "</div>"
                + '<div class="mt-12 grid grid-cols-3 gap-6 text-center">' + "".join(
                f'<div><b class="block text-4xl font-extrabold text-rose-600 dark:text-rose-400">{t.bdi(f"st{i}")}</b>{t(f"st{i}l", "span", "text-slate-500")}</div>' for i in (1, 2, 3)) + "</div>", True, "features")
            + tw_section(f"""<div class="grid lg:grid-cols-2 gap-12 items-center"><div class="rounded-2xl shadow-xl grid place-items-center min-h-60"><div class="size-24 rounded-3xl grid place-items-center bg-rose-50 dark:bg-rose-950 text-rose-600">{icon('shield', 'size-12')}</div></div>
  <div>{t('pvh', 'h2', 'text-3xl sm:text-4xl font-extrabold')}{t('pvl', 'p', 'mt-3 text-lg text-slate-500')}</div></div>""", False, "privacy")
            + tw_section(tw_head2(t, "qh", center=True, c=c) + tw_faq(t), True, "faq")
            + tw_section(f"""<div class="rounded-3xl p-8 sm:p-14 bg-gradient-to-br from-rose-600 to-violet-500 text-white grid md:grid-cols-2 gap-8 items-center">
  <div>{t('dh', 'h2', 'text-3xl font-extrabold')}{t('dl', 'p', 'mt-2 text-white/85')}</div><div class="flex flex-wrap gap-3">{stores(True)}</div></div>""", False, "download")
            + tw_footer(t) + tail(t))


TEMPLATES = {
    "launch": (LAUNCH, launch_plain, launch_tw),
    "studio": (STUDIO, studio_plain, studio_tw),
    "pocket": (POCKET, pocket_plain, pocket_tw),
}


def main():
    for name, (copy, plain, tw) in TEMPLATES.items():
        t = T(copy)
        out = KIT / "templates" / name
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(plain(t), encoding="utf-8")
        (out / "tailwind.html").write_text(tw(t), encoding="utf-8")
        print("wrote", out.relative_to(KIT.parent))


if __name__ == "__main__":
    main()
