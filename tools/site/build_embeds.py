#!/usr/bin/env python3
"""Build embeddable (iframe) versions of the strongest calculators + the two "embed on your site" hub pages.

    python3 tools/site/build_embeds.py          (also run by tools/site/build_site.py)

For every entry in EMBEDS the calculator's own markup and script are lifted from its live page, so the embed
always computes exactly like the page:
  * the calculator region (one balanced element, `root`) is copied; share bar, CTA boxes, H1/lead are dropped
  * every inline <style> and calculator <script> (inline, or a local src like calc.js) is inlined
  * docs/assets/site.css is pruned to the rules whose classes appear in the embed (no web font, no site.js)
  * relative links become absolute https links that open in a new tab
  * a visible attribution link "מחשבון: תכנון פלוס" (normal, followed link) + auto-height via postMessage

Outputs:  docs/embed/<slug>/index.html (Hebrew), docs/en/embed/<slug>/index.html (English)   [noindex, follow]
          docs/embed/index.html, docs/en/embed/index.html  (hub: copy-paste code + live preview)  [indexed]
          an "embed this calculator" link right after the calculator on each source page (between
          <!-- embed-link --> markers, idempotent).

Embed URL options: ?theme=dark|auto (default light, so it matches most host pages).
Message to the parent: {type: "tichnun:embed-height", slug, height}.
"""
import html
import json
import pathlib
import re
import sys
from urllib.parse import urljoin

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_config import BASE_URL, BRAND  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
BASE = BASE_URL.rstrip("/") + "/"
MAX_BYTES = 40 * 1024

# root: regex for the start tag of the element to lift (first match after `after`, if given)
# drop: regexes for start tags of elements removed from inside it
COMMON_DROP = [r'<div class="cta-box', r'<h1\b', r'<p class="lead', r'<nav class="breadcrumbs', r'<noscript\b']
EMBEDS = [
    dict(slug="wedding-gift", lang="he", src="tools/wedding-gift/", root=r'<form id="gift-form"',
         title="כמה לשים בחתונה? מחשבון 2026", short="כמה לשים בחתונה",
         desc="לפי קרבה, מספר מוזמנים, עונה, אזור, יום ומקום. מתאים לבלוגים על חתונות, אולמות וספקים.", height=900),
    dict(slug="vat-calculator", lang="he", src="tools/vat-calculator/", root=r'<div class="container narrow">',
         title="מחשבון מע״מ 18%", short="מחשבון מע״מ",
         desc="הוספה והורדה של מע״מ + מחשבון הצעת מחיר מהיר. מתאים לאתרי רואי חשבון, עסקים קטנים ופרילנסרים.", height=1000),
    dict(slug="osek-patur-ceiling", lang="he", src="tools/osek-patur-ceiling/", root=r'<div class="tool-panel" id="osek-panel">',
         title="מחשבון תקרת עוסק פטור 2026", short="מחשבון תקרת עוסק פטור",
         desc="כמה נשאר עד התקרה (122,833 ₪) ומתי צפוי לעבור אותה. מתאים לאתרי הנהלת חשבונות ופרילנסרים.", height=760),
    dict(slug="net-salary-budget", lang="he", src="tools/net-salary-budget/", root=r'<div class="container" id="nsb-tool">',
         title="מחשבון תקציב לפי משכורת נטו", short="תקציב לפי משכורת נטו",
         desc="מכניסים נטו, דיור ומספר נפשות ומקבלים תקציב חודשי מפורט. מתאים לבלוגים על כסף וכלכלת המשפחה.", height=760),
    dict(slug="budget-503020", lang="he", src="tools/budget-503020/", root=r'<div class="split">',
         title="מחשבון תקציב 50/30/20 בשקלים", short="מחשבון 50/30/20",
         desc="חלוקת ההכנסה לצרכים, רצונות וחיסכון + קרן חירום מומלצת. מתאים לאתרי חיסכון ופיננסים.", height=720),
    dict(slug="sufganiyot-calculator", lang="he", src="tools/sufganiyot-calculator/", root=r'<div class="split">',
         title="כמה סופגניות ולביבות צריך? מחשבון לחנוכה", short="מחשבון סופגניות ולביבות",
         desc="כמויות לפי מספר אורחים + רשימת קניות. מתאים לאתרי מתכונים, גנים ובתי ספר לקראת חנוכה.", height=820),
    dict(slug="bar-mitzvah-gift", lang="en", src="en/tools/bar-mitzvah-gift/", root=r'<div class="container narrow">',
         after=r'<section class="section alt">', title="How much to give for a bar mitzvah? Chai calculator",
         short="Bar mitzvah gift calculator",
         desc="Suggested gift in multiples of $18 by closeness, who it's from and attendance. For Jewish-life blogs, synagogues and schools.", height=1050),
    dict(slug="bar-mitzvah-budget", lang="en", src="en/tools/bar-mitzvah-budget/", root=r'<div class="split">',
         title="Bar mitzvah budget calculator", short="Bar mitzvah budget calculator",
         desc="Itemized cost estimate in US dollars by guests, style and area. For event planners, venues and parenting blogs.", height=1000),
    dict(slug="seder-shopping-calculator", lang="en", src="en/tools/seder-shopping-calculator/", root=r'<div class="split">',
         title="Passover seder shopping calculator", short="Seder shopping calculator",
         desc="Matzah, wine, grape juice and seder plate amounts by guests and nights. For synagogues, kosher stores and recipe sites.", height=1000),
    dict(slug="latke-calculator", lang="en", src="en/hanukkah/latke-calculator/", root=r'<div class="split">',
         title="How many latkes per person? Latke & sufganiyot calculator", short="Latke calculator",
         desc="Latkes, doughnuts, potatoes and oil by guest count, with a shopping list. For recipe blogs, schools and synagogues.", height=820),
]

T = {
    "he": dict(credit="מחשבון:", embed_cta="&lt;/&gt; הטמיעו את המחשבון הזה באתר שלכם (חינם)", hub="embed/"),
    "en": dict(credit="Calculator by", embed_cta="&lt;/&gt; Embed this calculator on your site (free)", hub="en/embed/"),
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>", re.S)


def esc(s):
    return html.escape(str(s), quote=True)


def element_span(src, start):
    """(start, end) of the balanced element whose start tag begins at `start`."""
    m = TAG.match(src, start)
    name = m.group(2).lower()
    depth = 0
    pos = start
    while True:
        m = TAG.search(src, pos)
        if not m:
            raise ValueError(f"unbalanced <{name}> at {start}")
        pos = m.end()
        if m.group(2).lower() != name or name in VOID or m.group(3):
            # skip raw-text content of scripts/styles
            if m.group(2).lower() in ("script", "style") and not m.group(1):
                pos = src.find(f"</{m.group(2).lower()}>", pos)
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start, m.end()


def drop_elements(frag, pattern):
    while True:
        m = re.search(pattern, frag)
        if not m:
            return frag
        a, b = element_span(frag, m.start())
        frag = frag[:a] + frag[b:]


def absolutize(frag, page_url):
    def fix(m):
        attr, q, url = m.group(1), m.group(2), m.group(3)
        if url.startswith(("#", "http:", "https:", "mailto:", "tel:", "data:", "javascript:")):
            return m.group(0)
        return f"{attr}={q}{urljoin(page_url, url)}{q}"
    frag = re.sub(r'\b(href|src)=(["\'])(.*?)\2', fix, frag)

    def blank(m):
        tag = m.group(0)
        if re.search(r'href=["\']#', tag) or "target=" in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r"<a\b[^>]*>", blank, frag)


# ---------- CSS pruning ----------
def css_blocks(css):
    """Split CSS into top-level (prelude, body) pairs; comments removed."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth and k < n:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        out.append((prelude, css[j + 1:k - 1]))
        i = k
    return out


def split_selectors(prelude):
    parts, depth, cur = [], 0, ""
    for ch in prelude:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return [p for p in parts if p]


SITE_CHROME = re.compile(r"\b(header|footer)\b|#site-|\.skip-link")


def prune_css(css, words):
    out = []
    for prelude, body in css_blocks(css):
        if prelude.startswith("@media") or prelude.startswith("@supports"):
            inner = prune_css(body, words)
            if inner:
                out.append(f"{prelude}{{{inner}}}")
            continue
        if prelude.startswith("@keyframes"):
            name = prelude.split()[-1]
            if name in words:
                out.append(f"{prelude}{{{body.strip()}}}")
            continue
        if prelude.startswith("@"):
            continue
        keep = []
        for sel in split_selectors(prelude):
            if SITE_CHROME.search(sel):
                continue
            classes = re.findall(r"\.([A-Za-z_][\w-]*)", re.sub(r":not\([^)]*\)", "", sel))
            if all(c in words for c in classes):
                keep.append(sel)
        if keep:
            body = re.sub(r"\s*\n\s*", "", body.strip())
            out.append(f"{','.join(keep)}{{{body}}}")
    return "".join(out)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}").strip()


EMBED_CSS = """
html,body{background:var(--surface)}body{margin:0;overflow-x:hidden;font-size:1rem}
.embed-wrap{padding:12px 12px 8px}.embed-title{font-size:1.25rem;line-height:1.3;margin:0 0 .6rem;color:var(--text)}
.embed-wrap .container{padding:0;max-width:none}.embed-wrap .tool-panel{box-shadow:none}
.embed-credit{margin:.8rem 0 0;font-size:.85rem;color:var(--muted);text-align:center}
.embed-credit a{font-weight:700}
"""

THEME_JS = ("(function(){var t=(location.search.match(/[?&]theme=(dark|light|auto)/)||[])[1]||'light';"
            "if(t!=='auto')document.documentElement.setAttribute('data-theme',t)})();")

HEIGHT_JS = """(function(){
var slug=%s,last=0;
function h(){return Math.ceil(Math.max(document.documentElement.scrollHeight,document.body?document.body.scrollHeight:0,document.querySelector('.embed-wrap').getBoundingClientRect().height))}
function send(){if(window.parent===window)return;var v=Math.ceil(document.querySelector('.embed-wrap').getBoundingClientRect().height)+4;if(v===last)return;last=v;window.parent.postMessage({type:'tichnun:embed-height',slug:slug,height:v},'*')}
window.tichnunEmbedHeight=send;
if(window.ResizeObserver)new ResizeObserver(send).observe(document.querySelector('.embed-wrap'));
['load','resize','input','change','click','toggle'].forEach(function(e){window.addEventListener(e,function(){setTimeout(send,30)},true)});
document.addEventListener('submit',function(e){e.preventDefault()},true);
send();void h;
})();"""


def page_scripts(src, page_dir):
    """Calculator scripts of the page, as inline JS strings in document order."""
    out = []
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", src, re.S):
        attrs, body = m.group(1), m.group(2)
        if "ld+json" in attrs:
            continue
        sm = re.search(r'src=["\']([^"\']+)["\']', attrs)
        if sm:
            s = sm.group(1)
            if "assets/" in s or s.startswith("http"):
                continue  # site.js, share.js, catalog, fonts …
            out.append((page_dir / s).read_text(encoding="utf-8"))
        elif body.strip():
            out.append(body)
    return out


def build_embed(cfg):
    src_dir = DOCS / cfg["src"]
    src = (src_dir / "index.html").read_text(encoding="utf-8")
    src_noembed = re.sub(r"<!-- embed-link -->.*?<!-- /embed-link -->\n?", "", src, flags=re.S)
    page_url = BASE + cfg["src"]
    offset = 0
    if cfg.get("after"):
        offset = re.search(cfg["after"], src_noembed).end()
    m = re.compile(cfg["root"]).search(src_noembed, offset)
    a, b = element_span(src_noembed, m.start())
    frag = src_noembed[a:b]
    for pat in COMMON_DROP + [r"<div data-share\b"]:
        frag = drop_elements(frag, pat)
    frag = re.sub(r'<script src="[^"]*share\.js"></script>\s*', "", frag)
    frag = re.sub(r"<style>.*?</style>", "", frag, flags=re.S)
    frag = absolutize(frag, page_url)
    styles = "".join(re.findall(r"<style>(.*?)</style>", src_noembed, re.S))
    scripts = page_scripts(src_noembed, src_dir)
    lang = cfg["lang"]
    tool_url = page_url
    credit = (f'<p class="embed-credit">{T[lang]["credit"]} <a href="{tool_url}" target="_blank" rel="noopener">{esc(BRAND)}</a>'
              + (' <span lang="en" dir="ltr">(Tichnun Plus)</span>' if lang == "en" else "") + "</p>")
    body = (f'<main class="embed-wrap"><h1 class="embed-title">{esc(cfg["title"])}</h1>\n{frag}\n{credit}</main>')
    words = set(re.findall(r"[A-Za-z_][\w-]*", body + styles + "".join(scripts) + EMBED_CSS)) | {"embed-wrap"}
    css = prune_css((DOCS / "assets/site.css").read_text(encoding="utf-8"), words)
    css = css.replace('"Assistant", "Heebo", ', "")  # no web font in the embed
    css = minify_css(css + styles + EMBED_CSS)
    dir_ = "rtl" if lang == "he" else "ltr"
    out = f"""<!doctype html>
<html lang="{lang}" dir="{dir_}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(cfg["title"])} | {esc(BRAND)}</title>
<meta name="robots" content="noindex, follow">
<meta name="description" content="{esc(cfg["desc"])}">
<script>{THEME_JS}</script>
<style>{css}</style>
</head>
<body>
<!-- Embeddable version of {tool_url} — generated by tools/site/build_embeds.py, do not edit by hand. -->
{body}
<script>{HEIGHT_JS % json.dumps(cfg["slug"])}</script>
{"".join(f"<script>{s}</script>" for s in scripts)}
</body>
</html>
"""
    dest = DOCS / ("embed" if lang == "he" else "en/embed") / cfg["slug"] / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    size = len(out.encode("utf-8"))
    print(f"embed {dest.relative_to(REPO)}  {size/1024:.1f} KB" + ("  ⚠ over 40KB" if size > MAX_BYTES else ""))

    # "embed this" link on the source page, right after the calculator element
    hub = BASE + T[lang]["hub"] + "#" + cfg["slug"]
    link = (f'<!-- embed-link --><p class="small muted mt-1 embed-link"><a href="{hub}">{T[lang]["embed_cta"]}</a></p>'
            "<!-- /embed-link -->\n")
    if src_noembed[b:b + 1] == "\n":
        b += 1
    new = src_noembed[:b] + link + src_noembed[b:]
    if new != src:
        (src_dir / "index.html").write_text(new, encoding="utf-8")
    return size


def snippet(cfg):
    lang = cfg["lang"]
    url = BASE + ("embed/" if lang == "he" else "en/embed/") + cfg["slug"] + "/"
    tool = BASE + cfg["src"]
    d = ' dir="rtl"' if lang == "he" else ""
    credit = (f'<p{d} style="font-size:13px;margin:4px 0 0">מחשבון: <a href="{tool}">{esc(cfg["short"])} – {esc(BRAND)}</a></p>'
              if lang == "he" else
              f'<p style="font-size:13px;margin:4px 0 0">Calculator: <a href="{tool}">{esc(cfg["short"])} by Tichnun Plus</a></p>')
    return (f'<iframe src="{url}" title="{esc(cfg["short"])}" loading="lazy" data-tichnun-embed '
            f'style="width:100%;max-width:760px;border:0;height:{cfg["height"]}px"></iframe>\n'
            f"{credit}\n"
            '<script>window.addEventListener("message",function(e){var d=e.data;'
            f'if(e.origin!=="{BASE.rstrip("/")}"||!d||d.type!=="tichnun:embed-height")return;'
            'document.querySelectorAll("iframe[data-tichnun-embed]").forEach(function(f){'
            'if(f.contentWindow===e.source)f.style.height=d.height+"px"})});</script>')


HUB = {
    "he": dict(
        path="embed/index.html", up="../", other="en/embed/", other_label="English calculators to embed",
        title="הוסיפו מחשבון חינם לאתר שלכם", meta_title="מחשבונים להטמעה באתר – חינם, בעברית | תכנון פלוס",
        desc="הטמיעו באתר, בבלוג או בדף העסק מחשבון חינמי בעברית: כמה לשים בחתונה, מע״מ 18%, תקרת עוסק פטור, תקציב לפי נטו, 50/30/20 וסופגניות. מעתיקים קוד אחד וזהו.",
        lead="מחשבונים בעברית שאפשר להוסיף לכל אתר, בלוג או דף עסקי בהעתקה של קוד אחד. חינם, בלי הרשמה, בלי פרסומות ובלי עוגיות. המחשבון מתאים את הגובה שלו לבד ועובד מצוין בנייד.",
        how=["מעתיקים את הקוד של המחשבון שבחרתם (כפתור «העתקת הקוד»).",
             "מדביקים אותו בעורך האתר כבלוק HTML: בוורדפרס «HTML מותאם אישית», בוויקס «הטמעת קוד / HTML iframe», או ישירות בקוד הדף.",
             "זהו. החישובים מתעדכנים אצלנו (למשל שינוי במע״מ או בתקרת עוסק פטור) בלי שתצטרכו לגעת בקוד."],
        terms="תנאי שימוש פשוטים: מותר להטמיע בכל אתר, גם מסחרי. נבקש להשאיר את שורת הקרדיט «מחשבון: תכנון פלוס» מתחת למחשבון. מצב כהה: הוסיפו <code>?theme=dark</code> לכתובת. המחשבון לא אוסף מידע, הכול מחושב בדפדפן של הגולש.",
        copy="העתקת הקוד", copied="✓ הועתק", preview="תצוגה חיה", code="הקוד להטמעה", open="לעמוד המחשבון המלא",
        crumbs='<a href="../">ראשי</a> <span aria-hidden="true">›</span> <a href="../tools/">כלים חינם</a> <span aria-hidden="true">›</span> <span>מחשבונים להטמעה</span>',
        how_h="איך מטמיעים?", faq_h="שאלות נפוצות",
        faq=[("זה באמת חינם?", "כן. אין תשלום, אין הרשמה ואין פרסומות בתוך המחשבון."),
             ("המחשבון יאט את האתר שלי?", "לא. כל מחשבון הוא דף קטן (פחות מ-40KB, בלי פונטים ובלי ספריות) שנטען רק כשהגולש מגיע אליו (loading=lazy)."),
             ("המחשבון אוסף מידע על הגולשים שלי?", "לא. אין עוגיות ואין מעקב. כל החישוב מתבצע בדפדפן של הגולש."),
             ("אפשר לשנות את העיצוב?", "אפשר לשנות את הרוחב והגובה ההתחלתי של ה-iframe, ולבחור מצב כהה עם ‎?theme=dark‎ או לפי הגדרות הגולש עם ‎?theme=auto‎.")]),
    "en": dict(
        path="en/embed/index.html", up="../../", other="embed/", other_label="מחשבונים בעברית להטמעה",
        title="Add a free calculator to your website", meta_title="Free embeddable Jewish holiday & simcha calculators | Tichnun Plus",
        desc="Embed a free calculator on your site or blog: bar mitzvah gift (chai), bar mitzvah budget, Passover seder shopping and Hanukkah latkes. One copy-paste snippet, no sign-up.",
        lead="Free calculators you can add to any website, blog or synagogue page with one copy-paste snippet. No sign-up, no ads, no cookies. They resize themselves and work well on phones.",
        how=["Copy the snippet for the calculator you want (the “Copy code” button).",
             "Paste it into your site as an HTML block: WordPress “Custom HTML”, Squarespace “Code”, Wix “Embed code”, or straight into the page.",
             "Done. We keep the numbers up to date, so you never have to touch the code again."],
        terms="Simple terms: embed it on any site, commercial ones included. Please keep the “Calculator: … by Tichnun Plus” credit line under it. Dark mode: add <code>?theme=dark</code> to the URL. The calculator collects nothing; everything runs in the visitor’s browser.",
        copy="Copy code", copied="✓ Copied", preview="Live preview", code="Embed code", open="Open the full calculator",
        crumbs='<a href="../">Home</a> <span aria-hidden="true">›</span> <a href="../tools/">Free tools</a> <span aria-hidden="true">›</span> <span>Embed a calculator</span>',
        how_h="How to embed", faq_h="Questions",
        faq=[("Is it really free?", "Yes. No payment, no sign-up and no ads inside the calculator."),
             ("Will it slow my site down?", "No. Each calculator is a small page (under 40KB, no fonts or libraries) that only loads when a visitor scrolls to it (loading=lazy)."),
             ("Does it track my visitors?", "No. No cookies and no tracking. All the math runs in the visitor’s browser."),
             ("Can I change how it looks?", "Set the iframe’s width and starting height, and use ?theme=dark for dark mode or ?theme=auto to follow the visitor’s setting.")]),
}


def build_hub(lang):
    h = HUB[lang]
    items = [c for c in EMBEDS if c["lang"] == lang]
    dest = DOCS / h["path"]
    up = h["up"]
    cards = []
    for c in items:
        code = snippet(c)
        prev = BASE + ("embed/" if lang == "he" else "en/embed/") + c["slug"] + "/"
        local_prev = f'{"" if lang == "he" else ""}{c["slug"]}/'
        cards.append(f"""
  <article class="card pad-lg embed-item" id="{c['slug']}">
   <h2 class="h3 mt-0">{esc(c['title'])}</h2>
   <p class="muted">{esc(c['desc'])} <a href="{up}{c['src']}">{h['open']}</a></p>
   <label class="label" for="code-{c['slug']}">{h['code']}</label>
   <textarea id="code-{c['slug']}" class="embed-code" dir="ltr" readonly rows="5" spellcheck="false">{esc(code)}</textarea>
   <button type="button" class="btn small mt-1" data-copy="code-{c['slug']}">{h['copy']}</button>
   <details class="mt-2"><summary><strong>{h['preview']}</strong></summary>
    <iframe data-src="{local_prev}" data-tichnun-embed title="{esc(c['short'])}" loading="lazy" style="width:100%;border:0;height:{c['height']}px" class="mt-1"></iframe>
   </details>
  </article>""")
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in h["faq"]]}
    list_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": h["title"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": c["short"], "url": BASE + c["src"]} for i, c in enumerate(items)]}
    url = BASE + h["path"].replace("index.html", "")
    dir_ = "rtl" if lang == "he" else "ltr"
    page = f"""<!doctype html>
<html lang="{lang}" dir="{dir_}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(h['meta_title'])}</title>
<meta name="description" content="{esc(h['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="he" href="{BASE}embed/">
<link rel="alternate" hreflang="en" href="{BASE}en/embed/">
<link rel="alternate" hreflang="x-default" href="{BASE}embed/">
<meta property="og:type" content="website">
<meta property="og:locale" content="{'he_IL' if lang == 'he' else 'en_US'}">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(h['title'])}">
<meta property="og:description" content="{esc(h['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og-default.png">
<meta name="theme-color" content="#0e6b63">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="{up}assets/site.css">
<style>
.embed-code{{width:100%;font:13px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;direction:ltr;text-align:left;resize:vertical;min-height:7.5rem}}
.embed-item{{margin-block-end:1.25rem}} .embed-item iframe{{background:var(--surface);border-radius:var(--radius-sm)}}
</style>
<script type="application/ld+json">{json.dumps(list_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">{'דלג לתוכן' if lang == 'he' else 'Skip to content'}</a>
<header id="site-header"></header>
<main id="main">
<!-- Generated by tools/site/build_embeds.py, do not edit by hand. -->
<div class="container"><nav class="breadcrumbs mt-2" aria-label="{'פירורי לחם' if lang == 'he' else 'Breadcrumb'}">{h['crumbs']}</nav></div>
<section class="section mt-0" style="padding-top:.5rem">
 <div class="container narrow">
  <h1>{esc(h['title'])}</h1>
  <p class="lead muted">{esc(h['lead'])}</p>
  <h2 class="h3">{h['how_h']}</h2>
  <ol>{''.join(f'<li>{esc(x)}</li>' for x in h['how'])}</ol>
  <p class="small muted">{h['terms']}</p>
  {''.join(cards)}
  <p class="mt-2"><a href="{up}{h['other']}" hreflang="{'en' if lang == 'he' else 'he'}">{h['other_label']}</a> · <a href="{up}data-il/">{'נתונים פתוחים על ישראל (JSON/CSV)' if lang == 'he' else 'Israeli open data (JSON/CSV)'}</a></p>
  <h2>{h['faq_h']}</h2>
  <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in h['faq'])}</div>
 </div>
</section>
</main>
<footer id="site-footer"></footer>
<script src="{up}assets/site.js" defer></script>
<script>
(function(){{
  document.querySelectorAll("[data-copy]").forEach(function(b){{
    b.addEventListener("click",function(){{
      var t=document.getElementById(b.getAttribute("data-copy")),label=b.textContent;
      t.select();
      (navigator.clipboard?navigator.clipboard.writeText(t.value):Promise.reject()).catch(function(){{document.execCommand("copy")}})
        .then(function(){{b.textContent={json.dumps(h['copied'])};setTimeout(function(){{b.textContent=label}},1800)}});
    }});
  }});
  // previews load when opened (or straight away when the URL points at one)
  function load(d){{var f=d.querySelector("iframe[data-src]");if(f&&!f.src)f.src=f.getAttribute("data-src");}}
  document.querySelectorAll(".embed-item details").forEach(function(d){{d.addEventListener("toggle",function(){{if(d.open)load(d)}})}});
  if(location.hash){{var a=document.getElementById(location.hash.slice(1));if(a&&a.querySelector("details")){{a.querySelector("details").open=true;load(a)}}}}
  window.addEventListener("message",function(e){{var d=e.data;if(!d||d.type!=="tichnun:embed-height")return;
    document.querySelectorAll("iframe[data-tichnun-embed]").forEach(function(f){{if(f.contentWindow===e.source)f.style.height=d.height+"px"}})}});
}})();
</script>
</body>
</html>
"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")
    print("hub", dest.relative_to(REPO))


def main():
    for c in EMBEDS:
        build_embed(c)
    build_hub("he")
    build_hub("en")


if __name__ == "__main__":
    main()
