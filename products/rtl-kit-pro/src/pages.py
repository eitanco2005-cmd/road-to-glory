"""RTL Landing Kit Pro — page bodies (Hebrew placeholder copy). Imported by build.py.
Each template = (slug, title, theme css vars, body html). Everything uses rtl-kit.css + pro.css classes."""

I = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "home": '<path d="M3 11l9-8 9 8v10H3z"/><path d="M9 21v-6h6v6"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "users": '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6M16 4a4 4 0 0 1 0 8M22 21c0-3-2-5-4-5.5"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 22s7-6.5 7-12a7 7 0 0 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "heart": '<path d="M12 20s-8-4.7-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6.3-8 11-8 11z"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "scale": '<path d="M12 3v18M5 21h14M4 7h16M7 7l-3 7h6zM17 7l-3 7h6z"/>',
    "book": '<path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-5a3 3 0 0 0-3 3"/><path d="M20 4v14h-6"/>',
    "play": '<path d="M6 4l14 8-14 8z"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 8H6.5"/>',
    "truck": '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "leaf": '<path d="M5 21c0-9 5-15 15-16-1 10-7 15-15 16zM5 21l8-8"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "dumbbell": '<path d="M6 7v10M3 9v6M18 7v10M21 9v6M6 12h12"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "check": '<path d="M5 12l5 5L20 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
}


def ic(name, flip=False, size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg{s}{" class=" + chr(34) + "flip" + chr(34) if flip else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>')


def nav(brand, links, cta, variant=""):
    lis = "".join(f'<li><a href="#{h}">{t}</a></li>' for h, t in links)
    return f"""<header class="nav {variant}">
 <div class="container">
  <a class="brand" href="#"><span class="brand-mark" aria-hidden="true"></span>{brand}</a>
  <button class="menu-btn" type="button" data-menu aria-expanded="false"><span class="sr-only">תפריט</span>{ic('menu', size=22)}</button>
  <ul class="nav-links">{lis}</ul>
  <div class="nav-tools"><a class="btn sm" href="#{links[-1][0]}">{cta}</a></div>
 </div>
</header>"""


def footer(brand, line):
    return f"""<footer class="footer">
 <div class="container">
  <div class="cols">
   <div><a class="brand" href="#"><span class="brand-mark" aria-hidden="true"></span>{brand}</a><p class="muted mt-2" style="margin-block-start:1rem">{line}</p></div>
   <div><h4>ניווט</h4><ul><li><a href="#">דף הבית</a></li><li><a href="#">אודות</a></li><li><a href="#">צור קשר</a></li></ul></div>
   <div><h4>מידע</h4><ul><li><a href="#">שאלות נפוצות</a></li><li><a href="#">בלוג</a></li></ul></div>
   <div><h4>משפטי</h4><ul><li><a href="#">תנאי שימוש</a></li><li><a href="#">פרטיות</a></li><li><a href="#">נגישות</a></li></ul></div>
  </div>
  <div class="fine"><span>© 2026 {brand}. כל הזכויות שמורות.</span><span>טקסט ומספרים לדוגמה בלבד</span></div>
 </div>
</footer>"""


def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><div><p class=\"mb-0\">{a}</p></div></details>" for q, a in items) + "</div>"


def ok(text):
    return f'<p class="form-ok" data-ok hidden tabindex="-1">{text}</p>'


def head2(h, p="", center=False, eyebrow=""):
    return (f'<div class="section-head{" center" if center else ""}">' + (f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else "")
            + f"<h2>{h}</h2>" + (f'<p class="lead mb-0">{p}</p>' if p else "") + "</div>")


def art(a, b, label="", ratio=""):
    st = f"--a:{a};--b:{b}" + (f";aspect-ratio:{ratio}" if ratio else "")
    return f'<div class="tile-art" style="{st}"' + (f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"') + "></div>"


def feature_cards(items, cls="c3"):
    return f'<div class="grid {cls}">' + "".join(
        f'<article class="card feature"><div class="icon-tile">{ic(i)}</div><h3>{h}</h3><p>{d}</p></article>' for i, h, d in items) + "</div>"


def plans(items, featured=1, billing=False):
    out = ""
    for n, (name, sub, price, unit, feats, btn) in enumerate(items):
        f = n == featured
        pr = (f'<span data-monthly="{price[0]}" data-yearly="{price[1]}">{price[0]}</span>' if isinstance(price, tuple) else price)
        out += (f'<article class="card plan{" featured" if f else ""}">' + ('<span class="tag">הכי פופולרי</span>' if f else "")
                + f'<h3>{name}</h3><p class="muted mb-0">{sub}</p><div class="price">{pr} <small>{unit}</small></div><ul>'
                + "".join(f"<li>{x}</li>" for x in feats) + f'</ul><a class="btn{"" if f else " ghost"}" href="#">{btn}</a></article>')
    return out


# ---------------------------------------------------------------------------- templates
def restaurant():
    menu = [("סלט ירוק עם עשבי תיבול", "שמן זית, לימון, שקדים קלויים", "48"), ("פוקאצ'ה מהטאבון", "רוזמרין, מלח ים, ממרח עגבניות", "32"),
            ("דג היום על הגריל", "ירקות שורש, רוטב חמאה ולימון", "128"), ("ניוקי בטטה", "מרווה, חמאה חומה, פרמזן", "74"),
            ("מלבי ורדים", "פיסטוקים וסירופ פטל", "38"), ("קפה ועוגיה", "אספרסו כפול ועוגיית שקדים", "22")]
    row = lambda n, d, p: f'<div class="menu-item"><div><strong>{n}</strong><div class="muted" style="font-size:.92rem">{d}</div></div><span class="dots" aria-hidden="true"></span><span class="p"><bdi>₪{p}</bdi></span></div>'
    col1 = "".join(row(*m) for m in menu[:3])
    col2 = "".join(row(*m) for m in menu[3:])
    return ("restaurant", "מסעדה / בית קפה", "--c-primary:#9a3412;--c-primary-soft:#fdeee4;--c-accent:#eab308", nav("הנמל", [("menu", "תפריט"), ("about", "הסיפור"), ("hours", "שעות"), ("book", "הזמנת שולחן")], "הזמנת שולחן") + f"""
<main id="main">
<section class="hero"><div class="container split">
 <div><span class="eyebrow">מטבח ים-תיכוני · פתוח 7 ימים</span><h1>ארוחה טובה <span class="hl">מול הים</span></h1>
  <p class="lead">חומרי גלם מהשוק, טאבון עצים ויין מקומי. מזמינים שולחן בדקה, בלי לחכות על הקו.</p>
  <div class="row"><a class="btn" href="#book">הזמנת שולחן {ic('arrow', True)}</a><a class="btn ghost" href="#menu">לתפריט</a></div></div>
 {art('#9a3412', '#eab308', 'תמונת המנה המובילה', '5/4')}
</div></section>
<section class="section alt" id="menu"><div class="container">{head2('מהתפריט', 'התפריט משתנה לפי העונה. המחירים בשקלים וכוללים מע״מ.', True)}
 <div class="split" style="align-items:start"><div class="menu-list">{col1}</div><div class="menu-list">{col2}</div></div>
</div></section>
<section class="section" id="about"><div class="container split">
 <div class="gallery" style="columns:2 160px">{art('#7c2d12', '#fb923c', '', '3/4')}{art('#a16207', '#fde68a')}{art('#334155', '#94a3b8')}{art('#9a3412', '#fca5a5', '', '3/4')}</div>
 <div><h2>הסיפור שלנו</h2><p class="lead">התחלנו כדוכן קטן בשוק ב-2012. היום אנחנו מסעדה של 60 מקומות, ועדיין קונים דגים מאותם דייגים כל בוקר.</p>
 <ul class="check-list"><li>מנות טבעוניות ונטולות גלוטן מסומנות בתפריט</li><li>נגיש לכיסאות גלגלים</li><li>חניה בחינם לאורחים</li></ul></div>
</div></section>
<section class="section alt" id="hours"><div class="container split" style="align-items:start">
 <div class="card"><h3>{ic('clock', size=20)} שעות פתיחה</h3><div class="hours"><span>ראשון–חמישי</span><bdi>12:00–23:00</bdi><span>שישי</span><bdi>10:00–16:00</bdi><span>מוצאי שבת</span><bdi>19:30–00:00</bdi></div></div>
 <div class="card"><h3>{ic('pin', size=20)} איך מגיעים</h3><p>שדרות הנמל 4, חיפה</p><p class="mb-0"><a href="tel:+97245550123" dir="ltr">04-555-0123</a></p></div>
</div></section>
<section class="section" id="book"><div class="container" style="max-inline-size:720px">{head2('הזמנת שולחן', 'נאשר את ההזמנה ב-SMS תוך כמה דקות.', True)}
 <form class="form card raised" data-demo>
  <div class="grid c3" style="gap:1rem"><div class="field"><label for="d">תאריך</label><input id="d" type="date" required></div>
  <div class="field"><label for="t">שעה</label><select id="t"><option>19:00</option><option>19:30</option><option>20:00</option><option>20:30</option><option>21:00</option></select></div>
  <div class="field"><label for="g">סועדים</label><select id="g"><option>2</option><option>3</option><option>4</option><option>5</option><option>6+</option></select></div></div>
  <div class="grid c2" style="gap:1rem"><div class="field"><label for="n">שם</label><input id="n" required autocomplete="name"></div>
  <div class="field"><label for="p">טלפון נייד</label><input id="p" type="tel" dir="ltr" required placeholder="050-000-0000" autocomplete="tel"></div></div>
  <div class="field"><label for="r">בקשות מיוחדות</label><textarea id="r" dir="auto" placeholder="יום הולדת, כיסא תינוק, אלרגיות…"></textarea></div>
  <button class="btn" type="submit">שליחת ההזמנה</button>{ok('תודה! קיבלנו את הבקשה ונאשר ב-SMS.')}
 </form></div></section>
</main>
""" + footer("הנמל", "מסעדה ים-תיכונית בחיפה. כשר? לא. טעים? מאוד."))


def real_estate():
    homes = [("דירת 4 חדרים עם מרפסת", "רמת גן · קומה 6", "2,950,000", "4", "105", ("#1d4ed8", "#93c5fd")),
             ("פנטהאוז עם נוף לים", "בת ים · קומה 18", "4,400,000", "5", "160", ("#0f766e", "#5eead4")),
             ("קוטג' עם גינה", "מודיעין · שכונת אבני חן", "3,780,000", "6", "210", ("#a16207", "#fde68a")),
             ("דירת גן משופצת", "חיפה · כרמל", "2,150,000", "3", "88", ("#7c3aed", "#c4b5fd")),
             ("2 חדרים להשקעה", "באר שבע · ליד האוניברסיטה", "980,000", "2", "55", ("#be123c", "#fda4af")),
             ("דופלקס חדש מקבלן", "פתח תקווה · קומה 9", "3,350,000", "5", "140", ("#334155", "#cbd5e1"))]
    cards = "".join(f'<article class="card listing">{art(a, b)}<div class="body"><span class="badge">למכירה</span><h3 style="margin-block:.6rem .2rem">{t}</h3><p class="muted">{ic("pin", size=16)} {loc}</p>'
                    f'<div class="meta"><span><bdi>{r}</bdi> חדרים</span><span><bdi>{s}</bdi> מ״ר</span></div><div class="row" style="justify-content:space-between;margin-block-start:.8rem"><span class="price-tag"><bdi>₪{p}</bdi></span><a href="#">לפרטים {ic("arrow", True, 16)}</a></div></div></article>'
                    for t, loc, p, r, s, (a, b) in homes)
    return ("real-estate", "נדל״ן / תיווך", "--c-primary:#1d4ed8;--c-primary-soft:#e0e9ff;--c-accent:#0ea5e9", nav("בית טוב נכסים", [("search", "חיפוש"), ("listings", "נכסים"), ("sell", "מוכרים?"), ("contact", "צור קשר")], "דברו עם מתווך") + f"""
<main id="main">
<section class="hero center"><div class="container"><span class="eyebrow">מעל 300 נכסים במרכז ובצפון</span><h1>הבית הבא שלכם <span class="hl">מחכה כאן</span></h1>
 <p class="lead">חיפוש לפי עיר, תקציב ומספר חדרים. מתווך אישי מלווה אתכם עד החתימה.</p>
 <form class="form card raised" id="search" data-demo style="max-inline-size:900px;margin-inline:auto;margin-block-start:2rem;text-align:start">
  <div class="grid c4" style="gap:1rem;align-items:end">
   <div class="field"><label for="city">עיר</label><input id="city" list="cities" placeholder="למשל: רמת גן"><datalist id="cities"><option>תל אביב</option><option>רמת גן</option><option>חיפה</option><option>ירושלים</option></datalist></div>
   <div class="field"><label for="rooms">חדרים</label><select id="rooms"><option>הכול</option><option>2+</option><option>3+</option><option>4+</option><option>5+</option></select></div>
   <div class="field"><label for="max">תקציב עד</label><div class="input-group"><input id="max" type="number" inputmode="numeric" placeholder="3,000,000"><span class="addon">₪</span></div></div>
   <button class="btn" type="submit">{ic('search', size=18)} חיפוש</button></div>{ok('נמצאו 24 נכסים מתאימים (דוגמה).')}
 </form></div></section>
<section class="section alt" id="listings"><div class="container">{head2('נכסים חדשים השבוע')}<div class="grid c3">{cards}</div>
 <nav aria-label="עמודים" style="margin-block-start:2rem"><ol class="pagination"><li><a href="#" aria-current="page">1</a></li><li><a href="#">2</a></li><li><a href="#">3</a></li><li><a href="#" aria-label="הבא">{ic('arrow', True, 16)}</a></li></ol></nav>
</div></section>
<section class="section" id="sell"><div class="container split"><div><h2>מוכרים דירה?</h2><p class="lead">הערכת שווי חינם תוך 48 שעות, צילום מקצועי ופרסום בכל האתרים הגדולים.</p>
 <div class="stats" style="text-align:start"><div class="stat"><b><bdi>38</bdi></b>ימים בממוצע עד מכירה</div><div class="stat"><b><bdi>1.5%</bdi></b>עמלה + מע״מ</div></div></div>
 {art('#1d4ed8', '#0ea5e9', 'תמונת נכס', '4/3')}</div></section>
<section class="section alt" id="contact"><div class="container" style="max-inline-size:640px">{head2('נשמח לעזור', 'השאירו פרטים ומתווך יחזור אליכם היום.', True)}
 <form class="form card" data-demo><div class="field"><label for="cn">שם</label><input id="cn" required></div>
 <div class="field"><label for="cp">טלפון</label><input id="cp" type="tel" dir="ltr" required></div>
 <div class="field"><span class="label" style="font-weight:600">אני רוצה</span><div class="choice-grid"><label class="choice"><input type="radio" name="w" checked><span>לקנות</span></label><label class="choice"><input type="radio" name="w"><span>למכור</span></label><label class="choice"><input type="radio" name="w"><span>לשכור</span></label></div></div>
 <button class="btn" type="submit">שליחה</button>{ok('תודה! מתווך יחזור אליכם בהקדם.')}</form></div></section>
</main>
""" + footer("בית טוב נכסים", "תיווך נדל״ן ברישיון. כל הנכסים והמחירים בדף הם לדוגמה."))


def clinic():
    return ("clinic", "קליניקה / מרפאה", "--c-primary:#0e7490;--c-primary-soft:#dff4f8;--c-accent:#10b981", nav("מרפאת שקד", [("services", "טיפולים"), ("team", "הצוות"), ("faq", "שאלות"), ("book", "קביעת תור")], "קביעת תור") + f"""
<main id="main">
<section class="hero"><div class="container split"><div><span class="eyebrow">פיזיותרפיה ושיקום · תל אביב</span><h1>חוזרים לזוז <span class="hl">בלי כאב</span></h1>
 <p class="lead">טיפול אישי של 45 דקות, תוכנית תרגילים לבית ומעקב בווטסאפ. בהסדר עם כל קופות החולים.</p>
 <div class="row"><a class="btn" href="#book">קביעת תור אונליין</a><a class="btn ghost" href="tel:+97235550199" dir="ltr">{ic('phone', size=18)} 03-555-0199</a></div>
 <ul class="check-list"><li>תור תוך 3 ימי עבודה</li><li>חניה צמודה ונגישות מלאה</li></ul></div>
 {art('#0e7490', '#10b981', 'חדר טיפולים', '1/1')}</div></section>
<section class="section alt" id="services"><div class="container">{head2('הטיפולים שלנו', '', True)}
 {feature_cards([('heart', 'כאבי גב וצוואר', 'אבחון, טיפול ידני ותרגול מותאם.'), ('users', 'שיקום אחרי ניתוח', 'ליווי צמוד מהשבוע הראשון.'), ('dumbbell', 'פציעות ספורט', 'חזרה בטוחה לאימונים ולתחרויות.'),
                  ('leaf', 'רצפת אגן', 'טיפול דיסקרטי ע״י מטפלת מוסמכת.'), ('star', 'הליכה ויציבה', 'לגיל השלישי ולאחר אירוע מוחי.'), ('calendar', 'טיפולי המשך', 'מנוי חודשי במחיר מופחת.')])}</div></section>
<section class="section" id="team"><div class="container">{head2('הצוות', 'פיזיותרפיסטים מוסמכים עם ניסיון של 10 שנים ומעלה.', True)}
 <div class="grid c4">""" + "".join(f'<div class="person"><span class="avatar">{a}</span><strong>{n}</strong><span class="muted">{r}</span></div>' for a, n, r in (("ד״ל", "ד״ר דנה לוי", "מנהלת מקצועית"), ("א״כ", "אורי כהן", "שיקום ספורט"), ("ר״ח", "רים חדאד", "רצפת אגן"), ("י״ב", "יואב ברק", "גב וצוואר"))) + f"""</div></div></section>
<section class="section alt" id="faq"><div class="container">{head2('שאלות נפוצות', '', True)}{faq([('צריך הפניה מרופא?', 'בהסדר עם הקופה — כן. בטיפול פרטי — לא.'), ('כמה טיפולים צריך?', 'בדרך כלל 4–8, לפי האבחון בפגישה הראשונה.'), ('אפשר לבטל תור?', 'כן, עד 24 שעות לפני התור ללא חיוב.')])}</div></section>
<section class="section" id="book"><div class="container" style="max-inline-size:760px">{head2('קביעת תור', 'בוחרים טיפול, מועד ופרטים — ונאשר במייל.', True)}
 <form class="form card raised" data-steps data-demo>
  <ol class="steps-bar"><li>טיפול</li><li>מועד</li><li>פרטים</li></ol>
  <fieldset data-step style="border:0;padding:0;margin:0"><legend class="sr-only">סוג הטיפול</legend><div class="choice-grid">
   <label class="choice"><input type="radio" name="s" required checked><span>אבחון ראשוני</span></label><label class="choice"><input type="radio" name="s"><span>טיפול המשך</span></label><label class="choice"><input type="radio" name="s"><span>שיקום ספורט</span></label></div>
   <div class="row" style="margin-block-start:1rem"><button class="btn" type="button" data-next>המשך {ic('arrow', True)}</button></div></fieldset>
  <fieldset data-step style="border:0;padding:0;margin:0" hidden><div class="grid c2" style="gap:1rem"><div class="field"><label for="bd">תאריך</label><input id="bd" type="date" required></div>
   <div class="field"><label for="bt">שעה</label><select id="bt"><option>08:00</option><option>09:00</option><option>12:30</option><option>17:00</option><option>18:00</option></select></div></div>
   <div class="row" style="margin-block-start:1rem"><button class="btn ghost" type="button" data-prev>חזרה</button><button class="btn" type="button" data-next>המשך {ic('arrow', True)}</button></div></fieldset>
  <fieldset data-step style="border:0;padding:0;margin:0" hidden><div class="grid c2" style="gap:1rem"><div class="field"><label for="bn">שם מלא</label><input id="bn" required></div>
   <div class="field"><label for="bi">תעודת זהות</label><input id="bi" inputmode="numeric" dir="ltr" maxlength="9" pattern="[0-9]{{5,9}}" required></div>
   <div class="field"><label for="be">אימייל</label><input id="be" type="email" dir="ltr" required></div><div class="field"><label for="bp">טלפון</label><input id="bp" type="tel" dir="ltr" required></div></div>
   <label class="check" style="margin-block:1rem"><input type="checkbox" required> קראתי ואני מסכים/ה למדיניות הפרטיות</label>
   <div class="row"><button class="btn ghost" type="button" data-prev>חזרה</button><button class="btn" type="submit">אישור התור</button></div>{ok('התור נקבע! אישור נשלח במייל.')}</fieldset>
 </form></div></section>
</main>
""" + footer("מרפאת שקד", "המידע באתר אינו מחליף ייעוץ רפואי."))


def lawyer():
    return ("law-firm", "משרד עורכי דין / יועצים", "--c-primary:#1e3a5f;--c-primary-soft:#e4ebf3;--c-accent:#b08d57", nav("כהן, נסאר ושות׳", [("areas", "תחומים"), ("about", "המשרד"), ("process", "איך זה עובד"), ("consult", "פגישת ייעוץ")], "פגישת ייעוץ", "") + f"""
<main id="main">
<section class="hero"><div class="container split"><div><span class="eyebrow">משרד עורכי דין · מאז 2004</span><h1>ליווי משפטי <span class="hl">בגובה העיניים</span></h1>
 <p class="lead">מקרקעין, דיני עבודה ומשפחה — בעברית, בערבית ובאנגלית. מסבירים כל צעד, בלי הפתעות בחשבון.</p>
 <div class="row"><a class="btn" href="#consult">קביעת פגישת ייעוץ</a><a class="btn ghost" href="#areas">תחומי התמחות</a></div></div>
 <div class="card raised"><blockquote class="quote mb-0">״אנחנו מתחייבים לתשובה בכתב לכל פנייה תוך יום עסקים אחד.״<footer>— עו״ד מיכל כהן, שותפה מנהלת</footer></blockquote></div></div></section>
<section class="section alt" id="areas"><div class="container">{head2('תחומי התמחות')}
 {feature_cards([('home', 'מקרקעין ונדל״ן', 'רכישה, מכירה, תמ״א 38 ופינוי-בינוי.'), ('users', 'דיני עבודה', 'ייצוג עובדים ומעסיקים, הסכמי העסקה.'), ('heart', 'דיני משפחה', 'הסכמי ממון, צוואות וירושות.'), ('scale', 'ליטיגציה אזרחית', 'תביעות כספיות ויישוב סכסוכים.'), ('box', 'חברות ומסחר', 'הקמת חברות, הסכמי מייסדים.'), ('shield', 'נזיקין', 'תאונות דרכים ורשלנות.')])}</div></section>
<section class="section" id="about"><div class="container"><div class="tabs">{head2('המשרד')}
 <div role="tablist" aria-label="על המשרד"><button role="tab" id="t1" aria-controls="p1" aria-selected="true">מי אנחנו</button><button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">ערכים</button><button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">שכר טרחה</button></div>
 <div role="tabpanel" id="p1" aria-labelledby="t1"><p class="lead">12 עורכי דין ושני משרדים — בתל אביב ובנצרת. צוות דו-לשוני שמכיר את המערכת מבפנים.</p></div>
 <div role="tabpanel" id="p2" aria-labelledby="t2" hidden><ul class="check-list"><li>שקיפות מלאה בכל שלב</li><li>זמינות — טלפון ישיר לעורך הדין שלכם</li><li>פתרון מחוץ לבית המשפט כשאפשר</li></ul></div>
 <div role="tabpanel" id="p3" aria-labelledby="t3" hidden><p>פגישת ייעוץ ראשונה: <bdi>₪450</bdi> + מע״מ, מקוזזת מהטיפול אם ממשיכים. אחר כך: מחיר קבוע או לפי שעה — אתם בוחרים.</p></div>
</div></div></section>
<section class="section alt" id="process"><div class="container">{head2('איך זה עובד')}<ol class="timeline"><li><time>יום 1</time>שיחת היכרות קצרה בטלפון, ללא עלות.</li><li><time>תוך שבוע</time>פגישת ייעוץ וחוות דעת בכתב.</li><li><time>בהמשך</time>הצעת שכר טרחה קבועה וליווי עד הסוף.</li></ol></div></section>
<section class="section" id="consult"><div class="container" style="max-inline-size:680px">{head2('פגישת ייעוץ', 'הפרטים חסויים ומשמשים רק לחזרה אליכם.', True)}
 <form class="form card raised" data-demo><div class="grid c2" style="gap:1rem"><div class="field"><label for="ln">שם</label><input id="ln" required></div><div class="field"><label for="lp">טלפון</label><input id="lp" type="tel" dir="ltr" required></div></div>
 <div class="field"><label for="la">תחום</label><select id="la"><option>מקרקעין</option><option>דיני עבודה</option><option>דיני משפחה</option><option>אחר</option></select></div>
 <div class="field"><label for="lm">בקצרה, במה מדובר?</label><textarea id="lm" dir="auto"></textarea></div>
 <label class="check"><input type="checkbox"> מעדיף/ה שיחה בערבית</label>
 <button class="btn" type="submit">שליחה</button>{ok('תודה, נחזור אליכם תוך יום עסקים.')}</form></div></section>
</main>
""" + footer("כהן, נסאר ושות׳", "האמור באתר אינו מהווה ייעוץ משפטי."))


def course():
    mods = [("מבוא ותכנון", "5 שיעורים · 48 דק׳"), ("HTML סמנטי מימין לשמאל", "8 שיעורים · 1:35 ש׳"), ("CSS לוגי ו-Grid", "10 שיעורים · 2:10 ש׳"), ("טיפוגרפיה בעברית ובערבית", "6 שיעורים · 1:05 ש׳"), ("פרויקט גמר", "4 שיעורים · 1:20 ש׳")]
    return ("course", "קורס אונליין", "--c-primary:#7c3aed;--c-primary-soft:#efe7fe;--c-accent:#f43f5e", nav("אקדמיית ימין", [("learn", "מה לומדים"), ("syllabus", "סילבוס"), ("price", "מחיר"), ("faq", "שאלות")], "להרשמה") + f"""
<main id="main">
<div class="announce">ההרשמה למחזור מרץ פתוחה · <a href="#price">לפרטים</a></div>
<section class="hero"><div class="container split"><div><span class="eyebrow">קורס דיגיטלי · 33 שיעורים</span><h1>בונים אתרים <span class="hl">מימין לשמאל</span> כמו מקצוענים</h1>
 <p class="lead">קורס וידאו מעשי: HTML, CSS לוגי ו-Tailwind לאתרים בעברית ובערבית. גישה לכל החיים ותעודת סיום.</p>
 <div class="row"><a class="btn" href="#price">להרשמה {ic('arrow', True)}</a><button class="btn ghost" type="button" data-modal-open="trailer">{ic('play', size=18)} צפייה בטריילר</button></div>
 <p class="hero-note">שיעור ראשון פתוח לכולם, בלי הרשמה</p></div>
 <div class="mock" aria-hidden="true"><div class="mock-bar"><i></i><i></i><i></i></div><div style="display:grid;place-items:center;aspect-ratio:16/9;background:linear-gradient(135deg,#7c3aed,#f43f5e);color:#fff">{ic('play', size=56)}</div></div></div></section>
<dialog class="modal" id="trailer" aria-labelledby="tr-h"><button class="btn ghost sm modal-x" data-close aria-label="סגירה">{ic('x', size=16)}</button><h2 id="tr-h" style="font-size:1.3rem">טריילר הקורס</h2><p class="muted">כאן מטמיעים את הווידאו (YouTube / Vimeo / &lt;video&gt;).</p></dialog>
<section class="section alt" id="learn"><div class="container">{head2('מה תדעו בסוף הקורס', '', True)}{feature_cards([('book', 'לבנות דף נחיתה מאפס', 'מבנה, נגישות וביצועים — בעברית ובערבית.'), ('chart', 'לחשוב בצד ההתחלה והסוף', 'במקום שמאל וימין. קוד אחד לשני הכיוונים.'), ('star', 'טיפוגרפיה נכונה', 'בחירת גופנים, ריווח שורות ומספרים בתוך טקסט.')])}</div></section>
<section class="section" id="syllabus"><div class="container" style="max-inline-size:820px">{head2('סילבוס')}<div class="faq" style="max-inline-size:none">""" + "".join(f"<details{' open' if i == 0 else ''}><summary>פרק {i + 1}: {m} <span class=\"muted\" style=\"font-weight:400;margin-inline-start:auto;padding-inline-end:1rem\">{d}</span></summary><div><p class=\"mb-0\">תיאור הפרק ושיעורי הווידאו יופיעו כאן.</p></div></details>" for i, (m, d) in enumerate(mods)) + f"""</div></div></section>
<section class="section alt" id="price"><div class="container"><div class="split"><div class="person" style="text-align:start;justify-items:start"><span class="avatar">נ״א</span><h3 class="mb-0">נועה אבו-ריא</h3><p class="muted">מפתחת Front-end ומרצה, 12 שנות ניסיון בבניית מוצרים לשוק הישראלי והערבי.</p></div>
 <div class="card plan featured"><span class="tag">גישה לכל החיים</span><h3>הקורס המלא</h3><div class="price"><bdi>₪690</bdi> <small>תשלום אחד</small></div><ul><li>33 שיעורי וידאו</li><li>קבצי תרגול וקוד מלא</li><li>קהילת לומדים</li><li>תעודת סיום</li></ul><a class="btn" href="#">להרשמה</a><p class="muted mb-0" style="font-size:.9rem">14 יום להחזר מלא אם זה לא בשבילכם.</p></div></div></div></section>
<section class="section" id="faq"><div class="container">{head2('שאלות נפוצות', '', True)}{faq([('צריך ניסיון קודם?', 'היכרות בסיסית עם HTML מספיקה.'), ('כמה זמן יש גישה?', 'לכל החיים, כולל עדכונים.'), ('יש חשבונית?', 'כן, נשלחת אוטומטית במייל.')])}</div></section>
</main>
""" + footer("אקדמיית ימין", "קורסים מעשיים לפיתוח אתרים בעברית ובערבית."))


def event():
    agenda = [("09:00", "התכנסות וקפה", ""), ("09:45", "פתיחה: עתיד הרשת בעברית", "מרצה ראשי"), ("10:30", "עיצוב מערכות לשתי כיווניות", "טראק עיצוב"),
              ("12:00", "ארוחת צהריים", ""), ("13:00", "סדנה: Tailwind בפועל", "טראק פיתוח"), ("15:30", "פאנל סיום", "כל הדוברים")]
    rows = "".join(f'<tr><td><bdi>{t}</bdi></td><td><strong>{a}</strong></td><td class="muted">{b}</td></tr>' for t, a, b in agenda)
    return ("conference", "כנס / אירוע", "--c-primary:#db2777;--c-primary-soft:#fde4f1;--c-accent:#6366f1", nav("כנס ימינה 2027", [("agenda", "לו״ז"), ("speakers", "דוברים"), ("tickets", "כרטיסים"), ("venue", "מיקום")], "לכרטיסים") + f"""
<main id="main">
<section class="hero center" style="background:linear-gradient(160deg,var(--c-primary-soft),transparent 60%)"><div class="container"><span class="eyebrow">14.3.2027 · מתחם הנמל, תל אביב</span><h1>הכנס הגדול לפיתוח <span class="hl">מימין לשמאל</span></h1>
 <p class="lead">יום אחד, 18 הרצאות, 2 טראקים ו-600 משתתפים: מעצבים ומפתחים שבונים מוצרים בעברית ובערבית.</p>
 <div class="row"><a class="btn" href="#tickets">לרכישת כרטיס</a><a class="btn ghost" href="#agenda">ללו״ז המלא</a></div>
 <div class="stats mt-2"><div class="stat"><b><bdi>18</bdi></b>הרצאות</div><div class="stat"><b><bdi>2</bdi></b>טראקים</div><div class="stat"><b><bdi>600</bdi></b>משתתפים</div></div></div></section>
<section class="section alt" id="agenda"><div class="container">{head2('לוח זמנים')}<div class="table-wrap"><table class="table"><thead><tr><th>שעה</th><th>מושב</th><th>טראק</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>
<section class="section" id="speakers"><div class="container">{head2('דוברים', '', True)}<div class="grid c4">""" + "".join(f'<div class="person"><span class="avatar">{a}</span><strong>{n}</strong><span class="muted">{r}</span></div>' for a, n, r in (("ש״מ", "שם הדובר/ת", "תפקיד, חברה"), ("ל״ע", "שם הדובר/ת", "תפקיד, חברה"), ("ע״ס", "שם הדובר/ת", "תפקיד, חברה"), ("מ״ד", "שם הדובר/ת", "תפקיד, חברה"))) + f"""</div></div></section>
<section class="section alt" id="tickets"><div class="container">{head2('כרטיסים', 'המחירים כוללים מע״מ. סטודנטים — 50% הנחה עם תעודה.', True)}<div class="pricing">{plans([('כניסה', 'כל ההרצאות', '<bdi>₪290</bdi>', '', ['כל ההרצאות', 'ארוחת צהריים', 'הקלטות'], 'לרכישה'), ('כנס + סדנה', 'הכי משתלם', '<bdi>₪490</bdi>', '', ['כל מה שבכניסה', 'סדנה מעשית', 'תעודת השתתפות'], 'לרכישה'), ('קבוצות', '5 משתתפים ומעלה', '<bdi>₪240</bdi>', 'לאדם', ['חשבונית אחת', 'מושבים יחד', 'הנחה קבוצתית'], 'צרו קשר')])}</div></div></section>
<section class="section" id="venue"><div class="container split"><div><h2>איך מגיעים</h2><p class="lead">מתחם הנמל, האנגר 11, תל אביב. 10 דקות הליכה מתחנת רכבת אוניברסיטה.</p><ul class="check-list"><li>חניה בתשלום במקום</li><li>נגיש לכיסאות גלגלים</li><li>אוכל טבעוני וכשר</li></ul></div>{art('#db2777', '#6366f1', 'מפה', '16/10')}</div></section>
</main>
""" + footer("כנס ימינה 2027", "כנס לדוגמה. התאריכים והמחירים להמחשה."))


def shop():
    return ("product", "חנות / מוצר בודד", "--c-primary:#15803d;--c-primary-soft:#e2f5e8;--c-accent:#ca8a04", nav("שורש", [("product", "המוצר"), ("details", "פרטים"), ("shipping", "משלוח"), ("faq", "שאלות")], f"{ic('cart', size=18)} סל (0)") + f"""
<main id="main">
<section class="section" id="product" style="padding-block-start:2rem"><div class="container">
 <ol class="breadcrumbs"><li><a href="#">ראשי</a></li><li><a href="#">מטבח</a></li><li aria-current="page">קרש חיתוך מעץ זית</li></ol>
 <div class="split" style="align-items:start"><div class="stack">{art('#15803d', '#ca8a04', 'תמונת המוצר', '1/1')}<div class="thumbs">{art('#166534', '#86efac')}{art('#a16207', '#fde68a')}{art('#3f6212', '#bef264')}{art('#713f12', '#fcd34d')}</div></div>
 <form class="stack" data-demo><span class="badge">עבודת יד · גליל</span><h1 style="font-size:clamp(1.8rem,4vw,2.6rem)">קרש חיתוך מעץ זית</h1>
  <p class="row"><span class="price-tag"><bdi>₪189</bdi></span><s class="muted"><bdi>₪229</bdi></s><span class="delta up">חוסכים ₪40</span></p>
  <p class="lead">כל קרש חתוך מגזע אחד של עץ זית שנגדע באישור. הדוגמה בעץ ייחודית, כך שאין שני קרשים זהים.</p>
  <fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-block-end:.5rem">מידה</legend><div class="choice-grid"><label class="choice"><input type="radio" name="sz" checked><span>קטן · 30 ס״מ</span></label><label class="choice"><input type="radio" name="sz"><span>בינוני · 40 ס״מ</span></label><label class="choice"><input type="radio" name="sz"><span>גדול · 50 ס״מ</span></label></div></fieldset>
  <div class="row"><div class="qty" data-qty><button type="button" data-d="-" aria-label="פחות">−</button><label class="sr-only" for="q">כמות</label><input id="q" value="1" inputmode="numeric"><button type="button" data-d="+" aria-label="עוד">+</button></div>
  <button class="btn" type="submit" style="flex:1">{ic('cart', size=18)} הוספה לסל</button></div>
  {ok('נוסף לסל ✓')}
  <ul class="check-list"><li>{ic('truck', size=18)} משלוח חינם מעל ₪250</li><li>החזרה תוך 14 יום</li></ul></form></div></div></section>
<section class="section alt" id="details"><div class="container"><div class="tabs"><div role="tablist" aria-label="פרטי המוצר"><button role="tab" id="pt1" aria-controls="pp1" aria-selected="true">תיאור</button><button role="tab" id="pt2" aria-controls="pp2" aria-selected="false" tabindex="-1">מפרט</button><button role="tab" id="pt3" aria-controls="pp3" aria-selected="false" tabindex="-1">טיפול</button></div>
 <div role="tabpanel" id="pp1" aria-labelledby="pt1"><p class="lead">עץ זית קשה ועמיד, בגימור שמן מאכל. מתאים לחיתוך ולהגשה.</p></div>
 <div role="tabpanel" id="pp2" aria-labelledby="pt2" hidden><div class="table-wrap"><table class="table"><tbody><tr><th>חומר</th><td>עץ זית מלא</td></tr><tr><th>עובי</th><td><bdi>2.5</bdi> ס״מ</td></tr><tr><th>משקל</th><td><bdi>1.1–2.4</bdi> ק״ג</td></tr><tr><th>מקור</th><td>גליל עליון</td></tr></tbody></table></div></div>
 <div role="tabpanel" id="pp3" aria-labelledby="pt3" hidden><p>שוטפים במים חמים וסבון, מייבשים מיד. לא במדיח. פעם בחודש — שכבה דקה של שמן.</p></div></div></div></section>
<section class="section" id="shipping"><div class="container">{feature_cards([('truck', 'משלוח 2–4 ימי עסקים', 'שליח עד הבית או נקודת איסוף.'), ('shield', 'תשלום מאובטח', 'כרטיס אשראי, Bit או PayPal.'), ('heart', 'אריזת מתנה', 'בחינם, עם כרטיס ברכה בכתב יד.')])}</div></section>
<section class="section alt" id="faq"><div class="container">{head2('שאלות', '', True)}{faq([('זה בטוח למגע עם מזון?', 'כן, הגימור הוא שמן מאכל בלבד.'), ('אפשר חריטה?', 'כן, בתוספת ₪35. כתבו לנו אחרי ההזמנה.')])}</div></section>
</main>
""" + footer("שורש", "חנות לדוגמה. המוצר, המחירים והמבצעים להמחשה."))


def nonprofit():
    return ("nonprofit", "עמותה / תרומות", "--c-primary:#c2410c;--c-primary-soft:#ffedd5;--c-accent:#0d9488", nav("עמותת גשר", [("mission", "מה אנחנו עושים"), ("impact", "השפעה"), ("volunteer", "התנדבות"), ("donate", "תרומה")], "לתרומה") + f"""
<main id="main">
<section class="hero"><div class="container split"><div><span class="eyebrow">עמותה רשומה · ע״ר 58-000000-0</span><h1>שיעורי עזר <span class="hl">לכל ילד</span>, בכל שכונה</h1>
 <p class="lead">סטודנטים מתנדבים מלמדים ילדים בעברית ובערבית, פעמיים בשבוע, בחינם. כל תרומה מממנת שעות לימוד.</p>
 <div class="row"><a class="btn" href="#donate">{ic('heart', size=18)} לתרומה</a><a class="btn ghost" href="#volunteer">רוצה להתנדב</a></div></div>
 {art('#c2410c', '#0d9488', 'ילדים לומדים', '4/3')}</div></section>
<section class="section alt" id="impact"><div class="container">{head2('ההשפעה ב-2026', 'נתונים לדוגמה — החליפו בשלכם.', True)}<div class="stats"><div class="stat"><b><bdi>1,240</bdi></b>ילדים</div><div class="stat"><b><bdi>380</bdi></b>מתנדבים</div><div class="stat"><b><bdi>22</bdi></b>יישובים</div><div class="stat"><b><bdi>87%</bdi></b>שיפור בציונים</div></div></div></section>
<section class="section" id="mission"><div class="container">{feature_cards([('book', 'שיעורים קבועים', 'מתנדב קבוע לכל ילד, באותו יום ובאותה שעה.'), ('users', 'קהילה', 'הורים, בתי ספר ומתנדבים עובדים יחד.'), ('chart', 'שקיפות', 'דוח כספי שנתי מלא פתוח לכולם.')])}</div></section>
<section class="section alt" id="donate"><div class="container" style="max-inline-size:640px">{head2('תרומה', 'תרומה מעל ₪200 מזכה בזיכוי מס לפי סעיף 46.', True)}
 <form class="form card raised" data-demo><div class="toggle" role="group" aria-label="תדירות"><button type="button" aria-pressed="true">חודשית</button><button type="button" aria-pressed="false">חד-פעמית</button></div>
 <fieldset style="border:0;padding:0;margin:0"><legend class="sr-only">סכום</legend><div class="choice-grid"><label class="choice"><input type="radio" name="a"><span><bdi>₪50</bdi></span></label><label class="choice"><input type="radio" name="a" checked><span><bdi>₪100</bdi></span></label><label class="choice"><input type="radio" name="a"><span><bdi>₪250</bdi></span></label></div></fieldset>
 <div class="field"><label for="oa">סכום אחר</label><div class="input-group"><input id="oa" type="number" min="10" inputmode="numeric"><span class="addon">₪</span></div></div>
 <p class="muted mb-0">₪100 בחודש = 4 שעות לימוד לילד אחד.</p>
 <button class="btn" type="submit">{ic('heart', size=18)} המשך לתשלום</button>{ok('תודה! כאן מחברים את מערכת הסליקה שלכם.')}</form></div></section>
<section class="section" id="volunteer"><div class="container split"><div><h2>להתנדב איתנו</h2><p class="lead">שעתיים בשבוע, ליד הבית. נותנים הכשרה וליווי. מתאים לסטודנטים ולפנסיונרים.</p></div>
 <form class="form card" data-demo><div class="field"><label for="vn">שם</label><input id="vn" required></div><div class="field"><label for="ve">אימייל</label><input id="ve" type="email" dir="ltr" required></div><div class="field"><label for="vc">יישוב</label><input id="vc"></div><button class="btn" type="submit">אני רוצה להתנדב</button>{ok('איזה כיף! רכזת תחזור אליכם השבוע.')}</form></div></section>
</main>
""" + footer("עמותת גשר", "עמותה לדוגמה. מספר העמותה והנתונים להמחשה."))


def waitlist():
    return ("waitlist", "רשימת המתנה / בקרוב", "--c-primary:#0f172a;--c-primary-soft:#e2e8f0;--c-accent:#22c55e", f"""
<main id="main" style="min-block-size:100vh;display:grid;place-items:center;background:radial-gradient(circle at 50% 0,var(--c-primary-soft),transparent 60%)">
<section class="container text-center" style="max-inline-size:680px;padding-block:64px">
 <a class="brand" href="#" style="justify-content:center;margin-block-end:2rem"><span class="brand-mark" aria-hidden="true"></span>נקודה</a>
 <span class="eyebrow">בקרוב · השקה באביב 2027</span>
 <h1>היומן שמבין <span class="hl" style="color:var(--c-accent)">עברית</span></h1>
 <p class="lead">כותבים ״פגישה עם דנה ביום שלישי בשלוש״ — ונקודה כבר יודעת מה לעשות. הצטרפו לרשימה וקבלו גישה מוקדמת.</p>
 <form class="form" data-demo style="margin-block-start:1.5rem"><div class="inline-form"><label class="sr-only" for="w">אימייל</label><input id="w" type="email" dir="ltr" required placeholder="you@example.com"><button class="btn" type="submit">הצטרפות לרשימה</button></div>
  {ok('נרשמתם! נעדכן אתכם לפני כולם.')}<p class="form-note">בלי ספאם. מייל אחד כשנשיק, ואפשר להסיר בקליק.</p></form>
 <ul class="check-list" style="justify-content:center;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));text-align:start;margin-block-start:2.5rem"><li>תאריכים עבריים ולועזיים</li><li>חגים ושבתות</li><li>סנכרון עם Google</li></ul>
 <p class="muted" style="margin-block-start:3rem;font-size:.9rem">© 2026 נקודה · <a href="#">פרטיות</a></p>
</section></main>
""")


def portfolio():
    tiles = [("#0f172a", "#64748b", "3/4"), ("#b45309", "#fde68a", "1/1"), ("#be123c", "#fecdd3", "4/3"), ("#0369a1", "#bae6fd", "3/4"), ("#4d7c0f", "#d9f99d", "4/3"), ("#6d28d9", "#ddd6fe", "1/1"), ("#334155", "#e2e8f0", "4/5"), ("#c2410c", "#fed7aa", "4/3")]
    return ("portfolio", "תיק עבודות / צלם", "--c-primary:#18181b;--c-primary-soft:#f4f4f5;--c-accent:#e11d48", nav("ליאת שמש · צילום", [("work", "עבודות"), ("about", "אודות"), ("packages", "חבילות"), ("contact", "צור קשר")], "לתיאום") + f"""
<main id="main">
<section class="hero"><div class="container"><h1 style="max-inline-size:14ch">צילום משפחה, <span class="hl" style="color:var(--c-accent)">אור טבעי</span> ורגעים אמיתיים</h1><p class="lead" style="max-inline-size:52ch">צילומי חוץ בשעת זהב, בכל הארץ. בלי פוזות מאולצות — רק אתם.</p></div></section>
<section class="section" id="work" style="padding-block-start:0"><div class="container"><div class="gallery">""" + "".join(f'<a href="#" aria-label="עבודה {n + 1}">{art(a, b, "", r)}</a>' for n, (a, b, r) in enumerate(tiles)) + f"""</div></div></section>
<section class="section alt" id="about"><div class="container split"><div class="person" style="justify-items:start;text-align:start"><span class="avatar" style="inline-size:140px;block-size:140px;font-size:2rem">ל״ש</span></div>
 <div><h2>נעים להכיר</h2><p class="lead">אני ליאת, מצלמת משפחות מ-2015. הצילום מתחיל בשיחה, ממשיך בטיול רגוע ונגמר בגלריה פרטית אונליין.</p></div></div></section>
<section class="section" id="packages"><div class="container">{head2('חבילות', '', True)}<div class="pricing">{plans([('מיני', '30 דקות', '<bdi>₪650</bdi>', '', ['15 תמונות ערוכות', 'גלריה אונליין', 'לוקיישן אחד'], 'לתיאום'), ('משפחה', 'שעה וחצי', '<bdi>₪1,250</bdi>', '', ['40 תמונות ערוכות', '2 לוקיישנים', 'אלבום דיגיטלי'], 'לתיאום'), ('אירוע', 'עד 4 שעות', '<bdi>₪2,900</bdi>', '', ['כל התמונות', 'עריכה מלאה', 'מסירה תוך שבועיים'], 'לתיאום')])}</div></div></section>
<section class="section alt" id="contact"><div class="container" style="max-inline-size:640px">{head2('בואו נצלם', '', True)}<form class="form card" data-demo><div class="field"><label for="pn">שם</label><input id="pn" required></div><div class="field"><label for="pe">אימייל</label><input id="pe" type="email" dir="ltr" required></div>
 <div class="field"><label for="pd">תאריך מועדף</label><input id="pd" type="date"></div><div class="field"><label for="pm">ספרו לי עליכם</label><textarea id="pm" dir="auto"></textarea></div><button class="btn" type="submit">שליחה</button>{ok('תודה! אחזור אליכם תוך יומיים.')}</form></div></section>
</main>
""" + footer("ליאת שמש", "תיק עבודות לדוגמה. התמונות הן מצייני מקום."))


def fitness():
    days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי"]
    sched = [("07:00", ["יוגה", "—", "פילאטיס", "—", "יוגה"]), ("18:00", ["HIIT", "כוח", "HIIT", "כוח", "ריצה"]), ("19:30", ["פילאטיס", "יוגה", "—", "TRX", "—"])]
    rows = "".join(f'<tr><th scope="row"><bdi>{h}</bdi></th>' + "".join(f"<td>{c}</td>" for c in cs) + "</tr>" for h, cs in sched)
    return ("fitness", "סטודיו כושר / חדר כושר", "--c-primary:#ea580c;--c-primary-soft:#ffedd5;--c-accent:#facc15", nav("כוח פנימי", [("classes", "שיעורים"), ("schedule", "מערכת"), ("plans", "מנויים"), ("trial", "שיעור ניסיון")], "שיעור ניסיון חינם", "dark") + f"""
<main id="main">
<section class="hero" style="background:#14161f;color:#fff"><div class="container split"><div><span class="eyebrow">סטודיו בוטיק · עד 12 מתאמנים בשיעור</span><h1>חזקים יותר, <span class="hl">כל שבוע</span></h1>
 <p class="lead" style="color:#cbd0dc">אימוני כוח, HIIT ויוגה בקבוצות קטנות עם מאמן שמכיר אתכם בשם. שיעור ראשון עלינו.</p><div class="row"><a class="btn" href="#trial">לשיעור ניסיון</a><a class="btn ghost" href="#schedule" style="color:#fff;border-color:#343a4d">למערכת השעות</a></div></div>
 {art('#ea580c', '#facc15', 'אימון קבוצתי', '4/3')}</div></section>
<section class="section alt" id="classes"><div class="container">{feature_cards([('dumbbell', 'אימון כוח', 'משקולות חופשיות וטכניקה נכונה.'), ('heart', 'HIIT', '45 דקות אינטנסיביות, מותאם לכל רמה.'), ('leaf', 'יוגה ופילאטיס', 'גמישות, נשימה ויציבה.')])}</div></section>
<section class="section" id="schedule"><div class="container">{head2('מערכת שבועית')}<div class="table-wrap"><table class="table"><thead><tr><th>שעה</th>""" + "".join(f"<th>{d}</th>" for d in days) + f"""</tr></thead><tbody>{rows}</tbody></table></div></div></section>
<section class="section alt" id="plans"><div class="container">{head2('מנויים', '', True)}<div data-billing><div class="text-center" style="margin-block-end:2rem"><div class="toggle" role="group" aria-label="תקופת חיוב"><button type="button" data-period="monthly" aria-pressed="true">חודשי</button><button type="button" data-period="yearly" aria-pressed="false">שנתי <span class="save-pill">חודשיים חינם</span></button></div></div>
 <div class="pricing">{plans([('בסיסי', '2 אימונים בשבוע', ('₪290', '₪242'), 'לחודש', ['כל סוגי השיעורים', 'אפליקציית הרשמה'], 'הצטרפות'), ('ללא הגבלה', 'כמה שרוצים', ('₪420', '₪350'), 'לחודש', ['שיעורים ללא הגבלה', 'הקפאה עד חודש', 'אימון אישי אחד'], 'הצטרפות'), ('כרטיסייה', '10 כניסות', ('₪550', '₪550'), '', ['תוקף 4 חודשים', 'ניתן להעברה'], 'לרכישה')], billing=True)}</div></div></div></section>
<section class="section" id="trial"><div class="container" style="max-inline-size:640px">{head2('שיעור ניסיון חינם', '', True)}<form class="form card raised" data-demo><div class="field"><label for="fn">שם</label><input id="fn" required></div><div class="field"><label for="fp">טלפון</label><input id="fp" type="tel" dir="ltr" required></div>
 <div class="field"><label for="fc">שיעור</label><select id="fc"><option>אימון כוח</option><option>HIIT</option><option>יוגה</option></select></div><button class="btn" type="submit">קביעת שיעור</button>{ok('מעולה! נשלח לכם הודעה עם השעה.')}</form></div></section>
</main>
""" + footer("כוח פנימי", "סטודיו לדוגמה. המחירים והשעות להמחשה."))


def chart_svg():
    pts = [40, 55, 48, 70, 62, 85, 78, 96, 90, 110, 104, 128]
    w, h, n = 600, 220, len(pts)
    xs = [round(20 + i * (w - 40) / (n - 1)) for i in range(n)]
    ys = [round(h - 20 - p * (h - 50) / 130) for p in pts]
    line = " ".join(f"{x},{y}" for x, y in zip(xs, ys))
    grid = "".join(f'<line class="grid-line" x1="20" x2="{w - 20}" y1="{y}" y2="{y}"/>' for y in (40, 90, 140, 190))
    months = ["ינו׳", "פבר׳", "מרץ", "אפר׳", "מאי", "יוני", "יולי", "אוג׳", "ספט׳", "אוק׳", "נוב׳", "דצמ׳"]
    return (f'<div class="chart"><svg viewBox="0 0 {w} {h + 20}" role="img" aria-label="גרף הכנסות חודשיות, עלייה מ-40 ל-128 אלף">{grid}'
            f'<g class="plot"><polygon class="area" points="{xs[0]},{h - 20} {line} {xs[-1]},{h - 20}"/><polyline class="line" points="{line}"/></g>'
            + "".join(f'<text x="{x}" y="{h + 12}" text-anchor="middle">{m}</text>' for i, (x, m) in enumerate(zip(xs, months)) if i % 2 == 0)
            + "</svg></div>")


def dashboard():
    orders = [("#10234", "אחמד ח׳", "חבילת צוות", "1,240", "ok", "שולם"), ("#10233", "מיכל ר׳", "חבילת בסיס", "390", "wait", "ממתין"), ("#10232", "יוסי ב׳", "ארגון", "8,900", "ok", "שולם"),
              ("#10231", "סלמא ע׳", "חבילת צוות", "1,240", "bad", "נכשל"), ("#10230", "דן ל׳", "תוסף אחסון", "120", "ok", "שולם")]
    rows = "".join(f'<tr><td><bdi>{o}</bdi></td><td><span class="row" style="gap:.5rem"><span class="avatar" style="inline-size:28px;block-size:28px;font-size:.7rem">{c[0]}</span>{c}</span></td><td>{p}</td><td class="num"><bdi>₪{a}</bdi></td><td><span class="status {s}">{st}</span></td></tr>' for o, c, p, a, s, st in orders)
    items = [("home", "סקירה", True), ("chart", "דוחות", False), ("users", "לקוחות", False), ("box", "מוצרים", False), ("cog", "הגדרות", False)]
    side = "".join(f'<a class="item" href="#"{" aria-current=" + chr(34) + "page" + chr(34) if cur else ""}>{ic(i)}{t}</a>' for i, t, cur in items)
    return ("dashboard", "דשבורד SaaS (מעטפת אפליקציה)", "", f"""
<div class="app">
 <aside class="app-side" id="side" aria-label="תפריט ראשי"><a class="brand" href="#"><span class="brand-mark" aria-hidden="true"></span>לוח</a>{side}
  <div class="card" style="margin-block-start:2rem;padding:1rem"><strong>שדרוג ל-Pro</strong><p class="muted" style="font-size:.9rem">דוחות מתקדמים וייצוא.</p><a class="btn sm" href="#">שדרוג</a></div></aside>
 <div class="scrim"></div>
 <main class="app-main" id="main">
  <div class="app-top"><div class="row"><button class="menu-btn" style="display:inline-grid;margin:0" type="button" data-drawer-open="side" aria-label="תפריט">{ic('menu', size=22)}</button><h1>סקירה</h1></div>
   <div class="row"><div class="search form"><label class="sr-only" for="s">חיפוש</label>{ic('search')}<input id="s" type="search" placeholder="חיפוש הזמנה, לקוח…"></div>
   <button class="btn ghost sm" type="button" data-toast="אין התראות חדשות" aria-label="התראות">{ic('bell', size=18)}</button><span class="avatar">את</span></div></div>
  <div class="kpis">
   <div class="kpi"><div class="label">הכנסות החודש</div><div class="value"><bdi>₪128,400</bdi></div><span class="delta up">↑ <bdi>12.4%</bdi></span></div>
   <div class="kpi"><div class="label">לקוחות פעילים</div><div class="value"><bdi>2,318</bdi></div><span class="delta up">↑ <bdi>3.1%</bdi></span></div>
   <div class="kpi"><div class="label">נטישה</div><div class="value"><bdi>1.8%</bdi></div><span class="delta down">↑ <bdi>0.2%</bdi></span></div>
   <div class="kpi"><div class="label">הזמנות פתוחות</div><div class="value"><bdi>47</bdi></div><span class="muted" style="font-size:.85rem">12 ממתינות לתשלום</span></div>
  </div>
  <div class="dash-grid">
   <section class="panel"><div class="panel-head"><h2>הכנסות 2026</h2><select class="lang-select" aria-label="טווח"><option>12 חודשים</option><option>6 חודשים</option></select></div>{chart_svg()}</section>
   <section class="panel"><div class="panel-head"><h2>לפי חבילה</h2></div><div class="bar-list">""" + "".join(f'<div><div class="row" style="justify-content:space-between"><span>{n}</span><bdi>{p}%</bdi></div><div class="bar"><i style="inline-size:{p}%"></i></div></div>' for n, p in (("צוות", 54), ("ארגון", 28), ("בסיס", 13), ("תוספים", 5))) + f"""</div></section>
  </div>
  <section class="panel"><div class="panel-head"><h2>הזמנות אחרונות</h2><a href="#">לכל ההזמנות {ic('arrow', True, 16)}</a></div>
   <div class="table-wrap" style="border:0"><table class="table"><thead><tr><th>מספר</th><th>לקוח</th><th>מוצר</th><th class="num">סכום</th><th>סטטוס</th></tr></thead><tbody>{rows}</tbody></table></div></section>
 </main>
</div>
""")


TEMPLATES = [restaurant, real_estate, clinic, lawyer, course, event, shop, nonprofit, waitlist, portfolio, fitness, dashboard]
