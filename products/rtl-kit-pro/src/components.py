"""RTL Landing Kit Pro — components gallery (copy-paste blocks). Imported by build.py."""
from pages import ic, chart_svg


def block(title, html, note=""):
    return (f'<section class="section" style="padding-block:40px" id="{title.split(" ")[0].lower()}"><div class="container">'
            f'<h2 style="font-size:1.4rem">{title}</h2>' + (f'<p class="muted">{note}</p>' if note else "") + html + "</div></section>")


def demo(label, inner, pad=True):
    return f'<div class="demo-block" style="margin-block:1.5rem{"" if pad else ";padding:0;overflow:visible"}"><span class="badge">{label}</span>{inner}</div>'


NAV_LINKS = '<ul class="nav-links"><li><a href="#">מוצר</a></li><li><a href="#">מחירים</a></li><li><a href="#">בלוג</a></li></ul>'


def navbars():
    simple = f'''<header class="nav" style="position:relative"><div class="container"><a class="brand" href="#"><span class="brand-mark"></span>מותג</a>
<button class="menu-btn" type="button" data-menu aria-expanded="false"><span class="sr-only">תפריט</span>{ic('menu', size=22)}</button>{NAV_LINKS}<div class="nav-tools"><a class="btn sm ghost" href="#">כניסה</a><a class="btn sm" href="#">הרשמה</a></div></div></header>'''
    dropdown = f'''<header class="nav" style="position:relative"><div class="container"><a class="brand" href="#"><span class="brand-mark"></span>מותג</a>
<button class="menu-btn" type="button" data-menu aria-expanded="false"><span class="sr-only">תפריט</span>{ic('menu', size=22)}</button>
<ul class="nav-links"><li class="dropdown" data-dropdown><button type="button">פתרונות</button><div class="dropdown-menu mega">
<a href="#"><strong>לעסקים קטנים</strong><small>הכול במקום אחד</small></a><a href="#"><strong>לחנויות</strong><small>מלאי, הזמנות ומשלוחים</small></a>
<a href="#"><strong>לנותני שירות</strong><small>זימון תורים ותשלומים</small></a><a href="#"><strong>לארגונים</strong><small>SSO והרשאות</small></a></div></li>
<li class="dropdown" data-dropdown><button type="button">משאבים</button><div class="dropdown-menu"><a href="#">מדריכים</a><a href="#">API</a><a href="#">קהילה</a></div></li><li><a href="#">מחירים</a></li></ul>
<div class="nav-tools"><a class="btn sm" href="#">התחילו</a></div></div></header>'''
    centered = f'''<div class="announce">חדש: גרסה 2.0 יצאה · <a href="#">מה חדש</a></div><header class="nav centered" style="position:relative"><div class="container">
<ul class="nav-links" style="margin-inline-start:0"><li><a href="#">חנות</a></li><li><a href="#">קולקציות</a></li></ul><a class="brand" href="#"><span class="brand-mark"></span>בוטיק</a>
<button class="menu-btn" type="button" data-menu aria-expanded="false"><span class="sr-only">תפריט</span>{ic('menu', size=22)}</button><div class="nav-tools"><a class="btn sm ghost" href="#">{ic('search', size=18)}<span class="sr-only">חיפוש</span></a><a class="btn sm" href="#">{ic('cart', size=18)} סל</a></div></div></header>'''
    drawer = f'''<header class="nav dark" style="position:relative"><div class="container"><button class="menu-btn" style="display:inline-grid;margin:0" type="button" data-drawer-open="drawer1" aria-label="פתיחת תפריט">{ic('menu', size=22)}</button>
<a class="brand" href="#"><span class="brand-mark"></span>מותג</a><div class="nav-tools" style="margin-inline-start:auto"><a class="btn sm" href="#">כניסה</a></div></div></header>
<nav class="drawer" id="drawer1" aria-label="תפריט צד"><button class="btn ghost sm" type="button" data-drawer-close style="justify-self:end">{ic('x', size=16)} סגירה</button><a href="#" aria-current="page">דף הבית</a><a href="#">שירותים</a><a href="#">צוות</a><a href="#">צור קשר</a></nav><div class="scrim"></div>'''
    return block("Navbars · סרגלי ניווט", demo("פשוט + תפריט נייד", simple, False) + demo("תפריט נפתח / מגה-מניו", dropdown, False)
                 + demo("לוגו במרכז + פס הודעה", centered, False) + demo("כהה + מגירת צד (נפתחת מצד ההתחלה)", drawer, False),
                 "כולם עם תפריט נייד. התפריט הנפתח ממוקם ב-inset-inline-start, כך שהוא נפתח לכיוון הנכון בכל שפה.")


def forms():
    contact = '''<form class="form" data-demo style="max-inline-size:560px"><div class="grid c2" style="gap:1rem"><div class="field"><label for="c1">שם פרטי</label><input id="c1" autocomplete="given-name" required></div>
<div class="field"><label for="c2">שם משפחה</label><input id="c2" autocomplete="family-name"></div></div><div class="field"><label for="c3">אימייל</label><input id="c3" type="email" dir="ltr" required placeholder="you@example.com"></div>
<div class="field"><label for="c4">טלפון</label><div class="input-group"><span class="addon" dir="ltr">+972</span><input id="c4" type="tel" dir="ltr" placeholder="50-000-0000"></div></div>
<div class="field"><label for="c5">הודעה</label><textarea id="c5" dir="auto"></textarea></div><button class="btn" type="submit">שליחה</button><p class="form-ok" data-ok hidden tabindex="-1">נשלח ✓</p></form>'''
    login = f'''<form class="form card raised" data-demo style="max-inline-size:400px"><h3 class="mb-0">כניסה לחשבון</h3><button class="btn ghost" type="button">{ic('mail', size=18)} המשך עם Google</button><div class="divider">או</div>
<div class="field"><label for="l1">אימייל</label><input id="l1" type="email" dir="ltr" autocomplete="username" required></div><div class="field"><div class="row" style="justify-content:space-between"><label for="l2">סיסמה</label><a href="#" style="font-size:.9rem">שכחתי סיסמה</a></div><input id="l2" type="password" dir="ltr" autocomplete="current-password" required aria-describedby="l2e" aria-invalid="true"><span class="error-text" id="l2e">הסיסמה צריכה לפחות 8 תווים (דוגמה למצב שגיאה)</span></div>
<label class="check"><input type="checkbox"> לזכור אותי</label><button class="btn" type="submit">כניסה</button><p class="form-ok" data-ok hidden tabindex="-1">נכנסתם ✓</p></form>'''
    steps = f'''<form class="form card" data-steps data-demo style="max-inline-size:620px"><ol class="steps-bar"><li>חשבון</li><li>עסק</li><li>סיום</li></ol>
<fieldset data-step style="border:0;padding:0;margin:0"><div class="field"><label for="s1">אימייל</label><input id="s1" type="email" dir="ltr" required></div><div class="row" style="margin-block-start:1rem"><button class="btn" type="button" data-next>המשך {ic('arrow', True)}</button></div></fieldset>
<fieldset data-step hidden style="border:0;padding:0;margin:0"><div class="field"><label for="s2">שם העסק</label><input id="s2" required></div><div class="field"><span style="font-weight:600">גודל הצוות</span><div class="choice-grid"><label class="choice"><input type="radio" name="sz" checked><span>1–5</span></label><label class="choice"><input type="radio" name="sz"><span>6–20</span></label><label class="choice"><input type="radio" name="sz"><span>21+</span></label></div></div>
<div class="row" style="margin-block-start:1rem"><button class="btn ghost" type="button" data-prev>חזרה</button><button class="btn" type="button" data-next>המשך {ic('arrow', True)}</button></div></fieldset>
<fieldset data-step hidden style="border:0;padding:0;margin:0"><label class="check"><input type="checkbox" required> אני מאשר/ת את התנאים</label><div class="row" style="margin-block-start:1rem"><button class="btn ghost" type="button" data-prev>חזרה</button><button class="btn" type="submit">יצירת חשבון</button></div><p class="form-ok" data-ok hidden tabindex="-1">החשבון נוצר ✓</p></fieldset></form>'''
    checkout = '''<form class="form" data-demo style="max-inline-size:640px"><h3 class="mb-0">פרטי משלוח</h3><div class="grid c2" style="gap:1rem"><div class="field"><label for="k1">שם מלא</label><input id="k1" autocomplete="name" required></div><div class="field"><label for="k2">טלפון</label><input id="k2" type="tel" dir="ltr" autocomplete="tel" required></div></div>
<div class="grid c2" style="gap:1rem"><div class="field"><label for="k3">עיר</label><input id="k3" autocomplete="address-level2" required></div><div class="field"><label for="k4">רחוב ומספר</label><input id="k4" autocomplete="street-address" required></div></div>
<div class="grid c3" style="gap:1rem"><div class="field"><label for="k5">דירה</label><input id="k5" inputmode="numeric"></div><div class="field"><label for="k6">מיקוד</label><input id="k6" inputmode="numeric" dir="ltr" maxlength="7" autocomplete="postal-code"></div><div class="field"><label for="k7">משלוח</label><select id="k7"><option>שליח (₪29)</option><option>איסוף עצמי (חינם)</option></select></div></div>
<h3 class="mb-0">תשלום</h3><div class="field"><label for="k8">מספר כרטיס</label><input id="k8" inputmode="numeric" dir="ltr" autocomplete="cc-number" placeholder="0000 0000 0000 0000"></div>
<div class="grid c3" style="gap:1rem"><div class="field"><label for="k9">תוקף</label><input id="k9" dir="ltr" placeholder="MM/YY" autocomplete="cc-exp"></div><div class="field"><label for="k10">CVV</label><input id="k10" dir="ltr" inputmode="numeric" maxlength="4" autocomplete="cc-csc"></div><div class="field"><label for="k11">תשלומים</label><select id="k11"><option>1</option><option>3</option><option>6</option></select></div></div>
<button class="btn" type="submit">לתשלום <bdi>₪218</bdi></button><p class="form-ok" data-ok hidden tabindex="-1">כאן מחברים את ספק הסליקה ✓</p></form>'''
    return block("Forms · טפסים", demo("יצירת קשר + קידומת טלפון", contact) + demo("כניסה + מצב שגיאה", login) + demo("הרשמה בשלבים", steps) + demo("קופה / כתובת בישראל", checkout),
                 "שדות אימייל, טלפון וכרטיס הם dir=\"ltr\" אבל מיושרים לסוף השדה, כך שהם לא ״קופצים״ בטופס עברי או ערבי.")


def pricing():
    from pages import plans
    tiers = '<div class="pricing">' + plans([("בסיס", "לעצמאים", "<bdi>₪49</bdi>", "לחודש", ["משתמש אחד", "5 פרויקטים"], "בחירה"), ("צוות", "לעסקים", "<bdi>₪149</bdi>", "לחודש", ["10 משתמשים", "פרויקטים ללא הגבלה", "דוחות"], "בחירה"), ("ארגון", "לחברות", "בהתאמה", "", ["SSO", "SLA"], "צרו קשר")]) + "</div>"
    toggle = ('<div data-billing><div class="text-center" style="margin-block-end:2rem"><div class="toggle" role="group" aria-label="תקופת חיוב"><button type="button" data-period="monthly" aria-pressed="true">חודשי</button><button type="button" data-period="yearly" aria-pressed="false">שנתי <span class="save-pill">‎-20%</span></button></div></div><div class="pricing">'
              + plans([("Starter", "", ("$9", "$7"), "/ month", ["1 site", "Basic analytics"], "Choose"), ("Pro", "", ("$29", "$23"), "/ month", ["10 sites", "Advanced analytics", "Priority support"], "Choose")], featured=1) + "</div></div>")
    rows = [("משתמשים", "1", "10", "ללא הגבלה"), ("אחסון", "5GB", "100GB", "1TB"), ("דוחות", "✗", "✓", "✓"), ("SSO", "✗", "✗", "✓"), ("תמיכה", "מייל", "צ'אט", "מנהל ייעודי")]
    cell = lambda v: f'<td class="{"yes" if v == "✓" else "no" if v == "✗" else ""}">' + ({"✓": '<span aria-label="כן">✓</span>', "✗": '<span aria-label="לא">—</span>'}.get(v, f"<bdi>{v}</bdi>")) + "</td>"
    table = ('<div class="table-wrap"><table class="table"><thead><tr><th>יכולת</th><th>בסיס</th><th>צוות</th><th>ארגון</th></tr></thead><tbody>'
             + "".join(f"<tr><th scope=\"row\">{r[0]}</th>" + "".join(cell(v) for v in r[1:]) + "</tr>" for r in rows) + "</tbody></table></div>")
    return block("Pricing · מחירים", demo("שלוש רמות", tiers) + demo("מתג חודשי/שנתי (גם ב-LTR)", toggle) + demo("טבלת השוואה", table))


def dashboards():
    kpis = ('<div class="kpis"><div class="kpi"><div class="label">מכירות היום</div><div class="value"><bdi>₪8,420</bdi></div><span class="delta up">↑ <bdi>8%</bdi></span></div>'
            '<div class="kpi"><div class="label">הזמנות</div><div class="value"><bdi>64</bdi></div><span class="delta down">↓ <bdi>3%</bdi></span></div>'
            '<div class="kpi"><div class="label">סל ממוצע</div><div class="value"><bdi>₪131</bdi></div><span class="delta up">↑ <bdi>5%</bdi></span></div></div>')
    chart = f'<section class="panel"><div class="panel-head"><h2>הכנסות</h2><span class="badge">2026</span></div>{chart_svg()}</section>'
    table = ('<section class="panel"><div class="panel-head"><h2>לקוחות</h2><a class="btn sm" href="#">+ לקוח חדש</a></div><div class="table-wrap" style="border:0"><table class="table"><thead><tr><th>שם</th><th>עיר</th><th class="num">יתרה</th><th>סטטוס</th></tr></thead><tbody>'
             + "".join(f'<tr><td>{n}</td><td>{c}</td><td class="num"><bdi>₪{b}</bdi></td><td><span class="status {s}">{t}</span></td></tr>' for n, c, b, s, t in (("נועה כ׳", "חיפה", "0", "ok", "פעיל"), ("סאמר ח׳", "נצרת", "1,250", "wait", "ממתין"), ("גל ד׳", "אילת", "380", "bad", "חוב")))
             + '</tbody></table></div><nav aria-label="עמודים" style="margin-block-start:1rem"><ol class="pagination"><li><a href="#" aria-current="page">1</a></li><li><a href="#">2</a></li></ol></nav></section>')
    return block("Dashboards · דשבורד", demo("כרטיסי KPI", kpis) + demo("גרף (SVG, ללא ספריות)", chart) + demo("טבלת נתונים", table),
                 "דשבורד מלא עם סרגל צד נמצא ב-templates/dashboard.")


def misc():
    tabs = '''<div class="tabs"><div role="tablist" aria-label="דוגמה"><button role="tab" id="x1" aria-controls="xp1" aria-selected="true">סקירה</button><button role="tab" id="x2" aria-controls="xp2" aria-selected="false" tabindex="-1">מפרט</button><button role="tab" id="x3" aria-controls="xp3" aria-selected="false" tabindex="-1">ביקורות</button></div>
<div role="tabpanel" id="xp1" aria-labelledby="x1"><p class="mb-0">חיצי המקלדת עובדים לפי כיוון הקריאה.</p></div><div role="tabpanel" id="xp2" aria-labelledby="x2" hidden><p class="mb-0">תוכן לשונית 2.</p></div><div role="tabpanel" id="xp3" aria-labelledby="x3" hidden><p class="mb-0">תוכן לשונית 3.</p></div></div>'''
    timeline = '<ol class="timeline"><li><time>2019</time>הקמת החברה</li><li><time>2022</time>1,000 לקוחות</li><li><time>2026</time>השקה בעולם הערבי</li></ol>'
    quote = '<blockquote class="quote">״ציטוט לקוח לדוגמה — החליפו בציטוט אמיתי עם אישור.״<footer>— שם הלקוח, תפקיד</footer></blockquote>'
    crumbs = '<ol class="breadcrumbs"><li><a href="#">ראשי</a></li><li><a href="#">קטגוריה</a></li><li aria-current="page">עמוד נוכחי</li></ol>'
    modal = (f'<div class="row"><button class="btn" type="button" data-modal-open="m1">פתיחת חלון</button><button class="btn ghost" type="button" data-toast="נשמר בהצלחה ✓">הצגת הודעה (toast)</button></div>'
             f'<dialog class="modal" id="m1" aria-labelledby="m1h"><button class="btn ghost sm modal-x" data-close aria-label="סגירה">{ic("x", size=16)}</button><h3 id="m1h">חלון קופץ</h3><p class="muted">משתמש באלמנט &lt;dialog&gt; המובנה: מלכודת פוקוס ו-Escape מגיעים בחינם.</p><button class="btn" data-close>הבנתי</button></dialog>')
    return block("More · עוד רכיבים", demo("לשוניות", tabs) + demo("ציר זמן", timeline) + demo("ציטוט", quote) + demo("פירורי לחם", crumbs) + demo("חלון + הודעה", modal))


def page():
    return navbars() + forms() + pricing() + dashboards() + misc()
