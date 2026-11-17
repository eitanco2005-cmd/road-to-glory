#!/usr/bin/env python3
"""Hanukkah activity pack (he + en): builds print HTML with inline vector art, then prints vector PDFs
with Chromium (print_pdf.js).  Run:  python3 pack.py   (outputs into products/hanukkah/out/)

Hanukkah 2026 / 5787: first candle on the evening of Friday 4 Dec 2026 (25 Kislev), last (8th) candle on the
evening of Friday 11 Dec, last day Saturday 12 Dec 2026. Verified with a Hebrew-calendar computation
(Dershowitz-Reingold arithmetic, see verify_dates.py); Kislev 5787 has 30 days, so night 6 is 30 Kislev.
"""
import html
import pathlib
import subprocess
import sys

import art
import puzzles

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
FONTS = (HERE / "fonts").as_uri()
SITE = "tichnun.netlify.app"

# ------------------------------------------------------------------ texts
NIGHTS_HE = [  # (night, weekday, gregorian evening, hebrew date of the night)
    (1, "שישי", "4.12.2026", "כ״ה בכסלו"), (2, "מוצאי שבת", "5.12.2026", "כ״ו בכסלו"),
    (3, "ראשון", "6.12.2026", "כ״ז בכסלו"), (4, "שני", "7.12.2026", "כ״ח בכסלו"),
    (5, "שלישי", "8.12.2026", "כ״ט בכסלו"), (6, "רביעי", "9.12.2026", "ל׳ בכסלו"),
    (7, "חמישי", "10.12.2026", "א׳ בטבת"), (8, "שישי", "11.12.2026", "ב׳ בטבת"),
]
NIGHTS_EN = [
    (1, "Friday", "Dec 4"), (2, "Saturday", "Dec 5"), (3, "Sunday", "Dec 6"), (4, "Monday", "Dec 7"),
    (5, "Tuesday", "Dec 8"), (6, "Wednesday", "Dec 9"), (7, "Thursday", "Dec 10"), (8, "Friday", "Dec 11"),
]
# Blessings. The Divine Name is written ה׳ (read as usual when reciting) so the sheet may be discarded normally.
BRACHOT_HE = [
    "בָּרוּךְ אַתָּה ה׳ אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם, אֲשֶׁר קִדְּשָׁנוּ בְּמִצְוֹתָיו וְצִוָּנוּ לְהַדְלִיק נֵר חֲנֻכָּה.",
    "בָּרוּךְ אַתָּה ה׳ אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם, שֶׁעָשָׂה נִסִּים לַאֲבוֹתֵינוּ בַּיָּמִים הָהֵם בַּזְּמַן הַזֶּה.",
    "בָּרוּךְ אַתָּה ה׳ אֱלֹהֵינוּ מֶלֶךְ הָעוֹלָם, שֶׁהֶחֱיָנוּ וְקִיְּמָנוּ וְהִגִּיעָנוּ לַזְּמַן הַזֶּה.",
]
BRACHOT_EN = [
    ("Barukh atah Adonai, Eloheinu melekh ha’olam, asher kid’shanu b’mitzvotav v’tzivanu l’hadlik ner shel Hanukkah.",
     "Blessed are You, Lord our God, Ruler of the universe, who made us holy with His commandments and commanded us to light the Hanukkah light."),
    ("Barukh atah Adonai, Eloheinu melekh ha’olam, she’asah nisim la’avoteinu bayamim haheim bazman hazeh.",
     "Blessed are You, Lord our God, Ruler of the universe, who performed miracles for our ancestors in those days, at this season."),
    ("Barukh atah Adonai, Eloheinu melekh ha’olam, shehecheyanu v’kiy’manu v’higiyanu lazman hazeh.",
     "Blessed are You, Lord our God, Ruler of the universe, who has kept us alive, sustained us and brought us to this season."),
]
WORDS_HE = ["חנוכה", "סביבון", "סופגנייה", "לביבות", "חנוכייה", "שמש", "נרות", "מכבים", "פך", "שמן", "מתנות", "אור", "מקדש"]
WORDS_EN = ["HANUKKAH", "MENORAH", "DREIDEL", "LATKES", "CANDLES", "SHAMASH", "GELT", "MACCABEES", "OIL", "MIRACLE",
            "LIGHT", "GIFTS", "TEMPLE", "SUFGANIYOT"]
HE_ALPHA = "אבגדהוזחטיכלמנסעפצקרשת"
EN_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

T = {
    "he": {
        "dir": "rtl", "lang": "he",
        "title": "חבילת פעילויות לחנוכה", "year": "חנוכה תשפ״ז · 2026",
        "cover_sub": "דפי צביעה, מבוכים, תפזורת, משחק סביבון, לוח הדלקת נרות וברכות",
        "ages": "לגילאי 4–10 · להדפסה בבית ובכיתה",
        "dates": "נר ראשון: יום שישי 4.12.2026 · נר שמיני: שישי 11.12.2026",
        "footer": f"© 2026 תכנון פלוס · לשימוש אישי, משפחתי וכיתתי · {SITE}",
        "toc_h": "מה יש בחבילה", "tips_h": "טיפים להדפסה",
        "tips": ["מדפיסים בגודל A4, «התאמה לעמוד» כבוי (100%).", "דפי הצביעה נראים הכי טוב על נייר רגיל בשחור-לבן.",
                 "הסביבון לגזירה ייצא חזק יותר על בריסטול או נייר עבה.", "אפשר להדפיס שוב ושוב לכל הילדים בבית ובכיתה."],
        "about_h": "על החג בקצרה",
        "about": "לפני יותר מ-2,100 שנה המכבים שחררו את בית המקדש בירושלים. כשרצו להדליק את המנורה מצאו רק פך שמן טהור אחד, "
                 "שהספיק ליום אחד בלבד — והוא דלק שמונה ימים. לכן מדליקים נרות שמונה לילות, ואוכלים מאכלים בשמן כמו סופגניות ולביבות.",
        "pages": {
            "color_hanukkiah": ("צבעו את החנוכייה", "כמה נרות דולקים? צבעו את הלהבות בצהוב וכתום."),
            "color_dreidel": ("צבעו את הסביבונים", "על הסביבון כתוב «נס גדול היה פה». איזו אות חסרה כאן?"),
            "color_food": ("מה אוכלים בחנוכה?", "צבעו את הסופגנייה ואת הלביבות. מה אתם הכי אוהבים?"),
            "color_window": ("חנוכייה בחלון", "מדליקים ליד החלון כדי שכולם יראו את האור. ציירו עוד כוכבים בשמיים."),
            "color_jug": ("פך השמן", "פך קטן אחד של שמן — ושמונה ימים של אור. צבעו וקשטו את הפך."),
            "cbn": ("צביעה לפי מספרים", "צבעו כל משבצת בצבע של המספר שלה."),
            "count": ("כמה נרות?", "ספרו את הנרות בכל חנוכייה (בלי השמש) וכתבו את המספר בריבוע."),
            "maze1": ("מבוך קל: הפך מגיע לחנוכייה", "עזרו לפך השמן למצוא את הדרך אל החנוכייה."),
            "maze2": ("מבוך מאתגר: הסביבון והמטבע", "מתחילים בסביבון ומגיעים אל דמי החנוכה."),
            "ws": ("תפזורת חנוכה", "מצאו את המילים. הן כתובות מימין לשמאל, מלמעלה למטה, ובאלכסון."),
            "rules": ("משחק הסביבון: החוקים", "משחק לכל המשפחה, משחקים עם סוכריות, אגוזים או מטבעות שוקולד."),
            "score": ("דף ניקוד למשחק הסביבון", "רושמים כמה יש לכל שחקן בסוף כל סיבוב."),
            "diy": ("סביבון לגזירה והדבקה", "גוזרים לאורך הקו החיצוני, מקפלים בקווים המקווקווים ומדביקים את הלשוניות."),
            "chart": ("לוח הדלקת נרות – חנוכה 2026", "סמנו ✓ בכל ערב שהדלקתם."),
            "brachot": ("ברכות הדלקת נרות חנוכה", "מברכים לפני ההדלקה. בלילה הראשון מוסיפים את ברכת «שהחיינו»."),
            "kind": ("8 לילות של מעשים טובים", "בכל ערב כותבים או מציירים מעשה טוב אחד שעשיתם."),
            "cards": ("ברכות לחג לגזירה", "צובעים, גוזרים ונותנים למישהו שאוהבים."),
            "answers": ("פתרונות", "למבוגרים: הפתרונות של המבוכים ושל התפזורת."),
        },
        "wordlist": "המילים:",
        "letters": [("נ", "נס", "לא קורה כלום — התור עובר הלאה."), ("ג", "גדול", "לוקחים את כל הקופה!"),
                    ("ה", "היה", "לוקחים חצי מהקופה (מעגלים למטה)."), ("פ", "פה", "מוסיפים פריט אחד לקופה.")],
        "rules_steps": ["כל שחקן מקבל אותו מספר פריטים, למשל 10.", "בתחילת כל סיבוב כל אחד שם פריט אחד בקופה שבאמצע.",
                        "מסובבים את הסביבון בתורות, ופועלים לפי האות שיצאה למעלה.", "כשהקופה מתרוקנת, כולם שמים שוב פריט אחד.",
                        "מי שנגמרו לו הפריטים — יוצא מהמשחק (או מקבל «הלוואה», אם כולם מסכימים).",
                        "המנצח: מי שנשאר עם הכי הרבה פריטים בסוף הזמן שקבעתם."],
        "rules_note": "בסביבון מחוץ לישראל כתוב ש (שם) במקום פ (פה) — והחוק זהה.",
        "player": "שחקן", "round": "סיבוב", "total": "סה״כ", "name": "שם",
        "chart_cols": ["נר", "ערב", "תאריך", "תאריך עברי", "נרות + שמש", "הדלקנו"],
        "chart_notes": ["מוסיפים נר חדש בכל ערב משמאל לקודמים, ומדליקים קודם את החדש (משמאל לימין).",
                        "שישי 4.12 ו-11.12: מדליקים לפני הדלקת נרות שבת, בנרות שידלקו לפחות חצי שעה אחרי צאת הכוכבים.",
                        "מוצאי שבת 5.12: מדליקים אחרי צאת השבת. סדר ההבדלה וההדלקה — לפי מנהג הבית.",
                        "בסך הכול צריך 44 נרות לכל החג (36 נרות + 8 פעמים שמש)."],
        "brachot_note": "בכל ערב מברכים את שתי הברכות הראשונות. בערב הראשון (4.12.2026) מוסיפים גם את הברכה השלישית. "
                        "יש הנוהגים לומר «נֵר שֶׁל חֲנֻכָּה». שם ה׳ נכתב בקיצור כדי שאפשר יהיה להשתמש בדף בלי חשש; בברכה אומרים אותו כרגיל.",
        "brachot_labels": ["ברכה ראשונה", "ברכה שנייה", "ברכה שלישית – בערב הראשון בלבד"],
        "night": "נר", "deed": "המעשה הטוב שלי:",
        "card_texts": ["חג אורים שמח!", "חנוכה שמח!"], "to": "אל:", "frm": "מאת:",
        "cbn_legend": ["1 – תכלת", "2 – כחול", "3 – צהוב", "4 – לבן", "5 – כתום", "6 – אדום"],
        "start": "התחלה", "finish": "סיום",
        "toc_extra": "",
    },
    "en": {
        "dir": "ltr", "lang": "en",
        "title": "Hanukkah Activity Pack", "year": "Hanukkah 2026",
        "cover_sub": "Coloring pages, mazes, word search, dreidel game, candle-lighting chart & blessings",
        "ages": "Ages 4–10 · Print at home or in class",
        "dates": "First candle: Friday, Dec 4, 2026 · Eighth candle: Friday, Dec 11, 2026",
        "footer": f"© 2026 Tichnun Plus · For personal, family and classroom use · {SITE}/en/hanukkah/",
        "toc_h": "What’s inside", "tips_h": "Printing tips",
        "tips": ["Print at 100% (turn off “fit to page” if your printer adds borders).", "Coloring pages look best on plain paper in black & white.",
                 "The cut-and-fold dreidel is sturdier on card stock.", "Print as many copies as you need for your family or class."],
        "about_h": "The story in a nutshell",
        "about": "More than 2,100 years ago the Maccabees freed the Temple in Jerusalem. When they went to light the menorah they found just one "
                 "small jug of pure oil — enough for one day — and it burned for eight. So we light candles for eight nights and eat foods "
                 "fried in oil, like latkes and jelly doughnuts (sufganiyot).",
        "pages": {
            "color_hanukkiah": ("Color the Menorah", "How many candles are lit? Color the flames yellow and orange."),
            "color_dreidel": ("Color the Dreidels", "The letters stand for “Nes Gadol Hayah Sham”: a great miracle happened there."),
            "color_food": ("Hanukkah Treats", "Color the jelly doughnut and the latkes. Which one is your favorite?"),
            "color_window": ("A Menorah in the Window", "We light near a window so everyone can see the light. Draw more stars in the sky!"),
            "color_jug": ("The Little Jug of Oil", "One small jug of oil — eight days of light. Color and decorate the jug."),
            "cbn": ("Color by Number", "Color each square with the color of its number."),
            "count": ("Count the Candles", "Count the candles on each menorah (not the shamash) and write the number in the box."),
            "maze1": ("Easy Maze: Bring the Oil to the Menorah", "Help the jug of oil find its way to the menorah."),
            "maze2": ("Tricky Maze: Dreidel to Gelt", "Start at the dreidel and find the path to the chocolate coins."),
            "ws": ("Hanukkah Word Search", "Find the words. They go across, down and diagonally."),
            "rules": ("How to Play Dreidel", "A game for the whole family. Play with candy, nuts, pennies or chocolate gelt."),
            "score": ("Dreidel Score Sheet", "Write how many pieces each player has at the end of every round."),
            "diy": ("Make Your Own Dreidel", "Cut along the outer line, fold on the dashed lines and glue the tabs."),
            "chart": ("Candle Lighting Chart – Hanukkah 2026", "Check off each night after you light."),
            "brachot": ("Hanukkah Candle Blessings", "Say the blessings before lighting. On the first night add the third blessing."),
            "kind": ("8 Nights of Kindness", "Each night write or draw one kind thing you did."),
            "cards": ("Hanukkah Cards to Cut Out", "Color, cut out and give to someone you love."),
            "answers": ("Answer Key", "For grown-ups: maze and word search solutions."),
        },
        "wordlist": "Words to find:",
        "letters": [("נ", "Nun", "Nothing happens. Next player’s turn."), ("ג", "Gimel", "Take the whole pot!"),
                    ("ה", "Hei", "Take half the pot (round down)."), ("ש", "Shin", "Put one piece into the pot.")],
        "rules_steps": ["Everyone starts with the same number of pieces, for example 10.", "At the start of each round, every player puts one piece in the pot.",
                        "Take turns spinning the dreidel and do what the letter on top says.", "When the pot is empty, everyone adds one piece again.",
                        "If you run out of pieces you are out (or borrow one, if everyone agrees).",
                        "The winner is whoever has the most pieces when time is up."],
        "rules_note": "Dreidels made in Israel have פ (Pe, for “Poh” – here) instead of ש (Shin). Pe works just like Shin.",
        "player": "Player", "round": "Round", "total": "Total", "name": "Name",
        "chart_cols": ["Night", "Day", "Evening of", "Candles + shamash", "Lit"],
        "chart_notes": ["Add each night’s new candle to the left of the others and light the newest one first (left to right).",
                        "Fridays (Dec 4 and Dec 11): light before the Shabbat candles, using candles that will burn until at least 30 minutes after nightfall.",
                        "Saturday night (Dec 5): light after Shabbat ends. Follow your family’s custom for the order of Havdalah and Hanukkah lights.",
                        "You need 44 candles for all eight nights (36 candles + 8 shamash)."],
        "brachot_note": "The first two blessings are said every night. On the first night (Friday, Dec 4, 2026) add the third blessing. "
                        "Some say “l’hadlik ner Hanukkah” in the first blessing. In the Hebrew the Divine Name is abbreviated ה׳; say it as usual when reciting.",
        "brachot_labels": ["First blessing", "Second blessing", "Third blessing – first night only"],
        "night": "Night", "deed": "My kind act:",
        "card_texts": ["Happy Hanukkah!", "Happy Festival of Lights!"], "to": "To:", "frm": "From:",
        "cbn_legend": ["1 – light blue", "2 – blue", "3 – yellow", "4 – white", "5 – orange", "6 – red"],
        "start": "START", "finish": "FINISH",
    },
}
ORDER = ["cover", "toc", "color_hanukkiah", "color_dreidel", "color_food", "color_window", "color_jug", "cbn", "count",
         "maze1", "maze2", "ws", "rules", "score", "diy", "chart", "brachot", "kind", "cards", "answers"]
TOC_SKIP = {"cover", "toc"}

PAPER = {"A4": ("210mm", "297mm"), "Letter": ("215.9mm", "279.4mm")}
CBN_COLORS = {"0": "#cfe2f7", "1": "#cfe2f7", "2": "#2f6db5", "3": "#f2b632", "4": "#ffffff", "5": "#ef7d31", "6": "#d64545"}
CBN_NUM = {"0": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6"}


def e(s):
    return html.escape(str(s), quote=True)


def S(inner, vb, style="width:100%;height:100%"):
    return art.svg(inner, vb, style=style)


# ------------------------------------------------------------------ page parts
def frame(t, key, body, n, cls=""):
    head = ""
    if key not in ("cover",):
        h, sub = t["pages"].get(key, ("", "")) if key in t["pages"] else ({"toc": t["toc_h"]}.get(key, ""), "")
        head = f'<header class="ph"><h1>{e(h)}</h1>{f"<p>{e(sub)}</p>" if sub else ""}</header>'
    foot = f'<footer class="pf"><span>{e(t["footer"])}</span><span class="pn">{n}</span></footer>'
    return f'<section class="page {cls}" data-key="{key}">{head}<div class="pb">{body}</div>{foot}</section>'


def p_cover(t, lang, ctx):
    big = S(art.hanukkiah(color=True, lit=9), "0 0 400 330")
    side = (f'<div class="cov-row"><div>{S(art.dreidel(color=True, letter="ג", side_letter="ה"), "0 0 240 300")}</div>'
            f'<div>{S(art.sufganiyah(color=True), "0 0 260 190")}</div>'
            f'<div>{S(art.coin(40, 40, 34) + art.coin(100, 60, 30) + art.coin(60, 100, 32), "0 0 140 140")}</div></div>')
    return (f'<div class="cover"><div class="cov-year">{e(t["year"])}</div><h1 class="cov-title">{e(t["title"])}</h1>'
            f'<p class="cov-sub">{e(t["cover_sub"])}</p><div class="cov-art">{big}</div>{side}'
            f'<p class="cov-dates">{e(t["dates"])}</p><p class="cov-ages">{e(t["ages"])}</p></div>')


def p_toc(t, lang, ctx):
    items = []
    for i, k in enumerate(ORDER, start=1):
        if k in TOC_SKIP:
            continue
        items.append(f'<li><span>{e(t["pages"][k][0])}</span><b>{i}</b></li>')
    tips = "".join(f"<li>{e(x)}</li>" for x in t["tips"])
    return (f'<div class="toc"><ol class="toc-list">{"".join(items)}</ol>'
            f'<div class="toc-side"><div class="box"><h2>{e(t["about_h"])}</h2><p>{e(t["about"])}</p></div>'
            f'<div class="box"><h2>{e(t["tips_h"])}</h2><ul>{tips}</ul></div>'
            f'<div class="toc-art">{S(art.oil_jug(color=True), "0 0 200 250")}</div></div></div>')


def p_color_hanukkiah(t, lang, ctx):
    return f'<div class="art">{S(art.hanukkiah(color=False, lit=9, sw=4), "0 0 400 330")}</div>'


def p_color_dreidel(t, lang, ctx):
    L = art.DREIDEL_LETTERS[lang]
    a = S(art.dreidel(color=False, letter=L[0], side_letter=L[1], sw=4), "0 0 240 300")
    b = S(art.dreidel(color=False, letter=L[2], side_letter="", sw=4), "0 0 240 300")
    return f'<div class="art two">{a}{b}</div>'


def p_color_food(t, lang, ctx):
    return (f'<div class="art col"><div>{S(art.sufganiyah(color=False, sw=4), "0 0 260 190")}</div>'
            f'<div>{S(art.latkes(color=False, sw=4), "0 0 300 170")}</div></div>')


def p_color_window(t, lang, ctx):
    return f'<div class="art">{S(art.window_scene(color=False, sw=4), "0 0 420 390")}</div>'


def p_color_jug(t, lang, ctx):
    stars = "".join(art.star(x, y, 16, color=False, sw=2.5) for x, y in [(30, 40), (370, 60), (40, 300), (360, 290)])
    jug = '<g transform="translate(100,20)">' + art.oil_jug(color=False, sw=4) + "</g>"
    return f'<div class="art">{S(jug + stars, "0 0 400 280")}</div>'


def p_cbn(t, lang, ctx):
    px = puzzles.CANDLE_PIXELS
    rows, cols = len(px), len(px[0])
    c = 30
    out = []
    for y, row in enumerate(px):
        for x, ch in enumerate(row):
            xx = (cols - 1 - x) if False else x
            num = CBN_NUM.get(ch, "1")
            out.append(f'<rect x="{xx * c}" y="{y * c}" width="{c}" height="{c}" fill="#fff" stroke="#555" stroke-width="1"/>'
                       f'<text x="{xx * c + c / 2}" y="{y * c + c * .68}" text-anchor="middle" font-family="Fredoka" font-size="15" fill="#555">{num}</text>')
    legend = "".join(f'<li><i style="background:{CBN_COLORS[str(i + 1) if i else "1"]}"></i>{e(x)}</li>' for i, x in enumerate(t["cbn_legend"]))
    return (f'<div class="cbn"><div class="art">{S("".join(out), f"-2 -2 {cols * c + 4} {rows * c + 4}")}</div>'
            f'<ul class="legend">{legend}</ul></div>')


def cbn_answer():
    px = puzzles.CANDLE_PIXELS
    c = 10
    out = [f'<rect x="{x * c}" y="{y * c}" width="{c}" height="{c}" fill="{CBN_COLORS[ch]}"/>' for y, row in enumerate(px) for x, ch in enumerate(row)]
    return S("".join(out), f"0 0 {len(px[0]) * c} {len(px) * c}")


def p_count(t, lang, ctx):
    counts = [3, 6, 1, 8, 5, 2]
    cells = []
    for n in counts:
        cells.append(f'<div class="cnt">{S(art.hanukkiah(color=False, lit=n + 1, count=n, sw=3.6), "0 0 400 330")}<div class="ans"></div></div>')
    return f'<div class="grid3">{"".join(cells)}</div>'


def _maze_page(t, lang, cols, rows, seed, start_art, start_box, end_art, end_box, solution=False, cell=24):
    """Start art sits above the entrance (top-left; top-right in Hebrew), finish art below the exit."""
    frag, W, H, _ = puzzles.maze_svg(cols, rows, seed, cell=cell, solution=solution, sw=3 if cell > 16 else 2.4)
    rtl = lang == "he"
    if rtl:  # mirror so the entry is top-right in Hebrew
        frag = f'<g transform="translate({W},0) scale(-1,1)">{frag}</g>'
    A = cell * 3.6  # art height
    def place(box, x_center, y_top, inner):
        k = A / box[1]
        return f'<g transform="translate({x_center - box[0] * k / 2:.1f},{y_top:.1f}) scale({k:.3f})">{inner}</g>'
    sx = (W - cell * .5) if rtl else cell * .5
    ex = cell * .5 if rtl else (W - cell * .5)
    fs = cell * .62
    sa = place(start_box, sx, -A - cell * .4, start_art)
    ea = place(end_box, ex, H + cell * .4, end_art)
    side = 1 if not rtl else -1
    def label(txt, x_art, box, y, sgn):
        half = A * box[0] / box[1] / 2 + cell * .4 + len(txt) * fs * .32
        return (f'<text x="{x_art + sgn * half:.1f}" y="{y:.1f}" text-anchor="middle" font-family="Fredoka" '
                f'font-size="{fs:.1f}" font-weight="700">{e(txt)}</text>')
    lbl = label(t["start"] + " ↓", sx, start_box, -A / 2, side) + label(t["finish"], ex, end_box, H + A / 2 + cell * .4, -side)
    m = cell * .3
    return S(frag + sa + ea + lbl, f"{-m:.0f} {-A - cell * .6:.0f} {W + 2 * m:.0f} {H + 2 * A + cell * 1.2:.0f}")


def maze1(t, lang, solution=False):
    return _maze_page(t, lang, 10, 13, 5787, art.oil_jug(color=False), (200, 250), art.hanukkiah(color=False, lit=9), (400, 330), solution, cell=30)


def maze2(t, lang, solution=False):
    L = art.DREIDEL_LETTERS[lang]
    return _maze_page(t, lang, 16, 22, 2026, art.dreidel(color=False, letter=L[1], side_letter=L[2]), (240, 300),
                      art.coin(40, 40, 34, color=False) + art.coin(100, 70, 30, color=False) + art.coin(50, 110, 32, color=False), (140, 150), solution, cell=22)


def p_maze1(t, lang, ctx):
    return f'<div class="art">{maze1(t, lang)}</div>'


def p_maze2(t, lang, ctx):
    return f'<div class="art">{maze2(t, lang)}</div>'


def wordsearch(lang):
    if lang == "he":
        words = [list(w) for w in WORDS_HE]
        # x grows in reading direction (right-to-left on paper); dirs: across, down, diagonal down-forward
        grid, placed = puzzles.word_search(words, 12, 5787, [(1, 0), (0, 1), (1, 1)], HE_ALPHA)
        return grid, placed, WORDS_HE
    words = [list(w) for w in WORDS_EN]
    grid, placed = puzzles.word_search(words, 14, 2026, [(1, 0), (0, 1), (1, 1)], EN_ALPHA)
    return grid, placed, WORDS_EN


def p_ws(t, lang, ctx):
    grid, placed, words = ctx["ws"]
    frag, size = puzzles.word_search_svg(grid, placed, cell=34, rtl=lang == "he", font="Fredoka" if lang == "en" else "Fredoka")
    wl = "".join(f"<li>{e(w)}</li>" for w in words)
    return (f'<div class="ws"><div class="art">{S(frag, f"-2 -2 {size + 4} {size + 4}")}</div>'
            f'<div class="wl"><b>{e(t["wordlist"])}</b><ul>{wl}</ul></div></div>')


def p_rules(t, lang, ctx):
    L = art.DREIDEL_LETTERS[lang]
    rows = "".join(
        f'<div class="lt"><div class="lt-d">{S(art.dreidel(color=True, letter=a, side_letter="", sw=3), "0 0 240 300")}</div>'
        f'<div><b class="lt-n">{e(n)}</b><p>{e(d)}</p></div></div>' for (a, n, d) in t["letters"])
    steps = "".join(f"<li>{e(s)}</li>" for s in t["rules_steps"])
    deco = (art.coin(60, 70, 50) + art.coin(150, 90, 46) + art.coin(95, 140, 48)
            + '<g transform="translate(230,0) scale(.62)">' + art.dreidel(letter=L[1], side_letter=L[2]) + "</g>"
            + art.gift(420, 80, 120, 100))
    return (f'<div class="rules"><div class="letters">{rows}</div><ol class="steps">{steps}</ol>'
            f'<p class="note">{e(t["rules_note"])}</p>'
            f'<div class="art">{S(deco, "0 0 560 200")}</div></div>')


def p_score(t, lang, ctx):
    players = 5
    head = f'<tr><th>{e(t["round"])}</th>' + "".join(f'<th>{e(t["player"])} {i}<div class="nm">{e(t["name"])}: ______</div></th>' for i in range(1, players + 1)) + "</tr>"
    body = "".join(f"<tr><td>{r}</td>" + "<td></td>" * players + "</tr>" for r in range(1, 13))
    body += f'<tr class="tot"><td>{e(t["total"])}</td>' + "<td></td>" * players + "</tr>"
    return f'<table class="score">{head}{body}</table>'


def p_diy(t, lang, ctx):
    """Cube dreidel net in mm. Faces 42mm: row of 4 side faces, top above face 2, bottom below face 2, glue tabs."""
    L = art.DREIDEL_LETTERS[lang]
    f = 38
    x0, y0 = 4, 50
    tab = 9
    out = []
    dash = 'stroke-dasharray="3 2.4"'
    def face(x, y, letter=None, hole=False, fill="#fff"):
        s = f'<rect x="{x}" y="{y}" width="{f}" height="{f}" fill="{fill}" stroke="#1b1b1b" stroke-width=".5" {dash}/>'
        if letter:
            s += (f'<text x="{x + f / 2}" y="{y + f * .72}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="{f * .62}" '
                  f'fill="#fff" stroke="#1b1b1b" stroke-width=".8" paint-order="stroke">{letter}</text>')
        if hole:
            s += f'<circle cx="{x + f / 2}" cy="{y + f / 2}" r="2.2" fill="none" stroke="#1b1b1b" stroke-width=".5"/><path d="M{x + f / 2 - 4},{y + f / 2}h8M{x + f / 2},{y + f / 2 - 4}v8" stroke="#1b1b1b" stroke-width=".35"/>'
        return s
    def tabs_path(x, y, w, h, side):
        # trapezoid glue tab on given side of rect (x,y,w,h)
        if side == "top":
            return f"M{x},{y} L{x + tab},{y - tab} L{x + w - tab},{y - tab} L{x + w},{y}"
        if side == "bottom":
            return f"M{x},{y + h} L{x + tab},{y + h + tab} L{x + w - tab},{y + h + tab} L{x + w},{y + h}"
        if side == "right":
            return f"M{x + w},{y} L{x + w + tab},{y + tab} L{x + w + tab},{y + h - tab} L{x + w},{y + h}"
    order = L if lang == "en" else L  # letters in spin order
    for i in range(4):
        out.append(face(x0 + i * f, y0 + f, order[i]))
    out.append(face(x0 + f, y0, hole=True))
    out.append(face(x0 + f, y0 + 2 * f, hole=True))
    tabs = [tabs_path(x0 + 3 * f, y0 + f, f, f, "right"), tabs_path(x0, y0 + f, f, f, "top"), tabs_path(x0, y0 + f, f, f, "bottom"),
            tabs_path(x0 + 2 * f, y0 + f, f, f, "top"), tabs_path(x0 + 2 * f, y0 + f, f, f, "bottom"),
            tabs_path(x0 + 3 * f, y0 + f, f, f, "top"), tabs_path(x0 + 3 * f, y0 + f, f, f, "bottom")]
    for p in tabs:
        out.append(f'<path d="{p}" fill="#eef3fa" stroke="#1b1b1b" stroke-width=".5"/>')
    # outer cut outline emphasised
    out.append(f'<text x="{x0 + 3.5 * f}" y="{y0 + .6 * f}" text-anchor="middle" font-size="5" font-family="Fredoka">✂</text>')
    steps_he = ["גוזרים את כל הצורה לאורך הקו החיצוני (כולל הלשוניות הכחולות).", "מקפלים בכל הקווים המקווקווים.",
                "מדביקים את הלשוניות מבפנים וסוגרים לקובייה.", "דוחפים עיפרון קצר או קיסם דרך שני העיגולים (בעזרת מבוגר) — ומסובבים!"]
    steps_en = ["Cut out the whole shape along the outer edge (including the blue tabs).", "Fold along every dashed line.",
                "Glue the tabs on the inside and close the cube.", "Push a short pencil or a skewer through both circles (ask a grown-up) and spin!"]
    steps = "".join(f"<li>{e(s)}</li>" for s in (steps_he if lang == "he" else steps_en))
    W = x0 * 2 + 4 * f + tab
    Hh = 3 * f + 2 * tab + 8
    return (f'<div class="diy"><div class="art">{S("".join(out), f"0 {y0 - tab - 4} {W} {Hh}", style=f"width:{W}mm;height:{Hh}mm")}</div>'
            f'<ol class="steps">{steps}</ol></div>')


def p_chart(t, lang, ctx):
    rows = []
    if lang == "he":
        for n, day, d, hd in NIGHTS_HE:
            mini = S(art.hanukkiah(color=True, lit=n + 1, count=n, sw=4), "20 90 360 240", style="height:11mm;width:auto")
            rows.append(f"<tr><td><b>{n}</b></td><td>{e(day)}</td><td>{d}</td><td>{e(hd)}</td><td>{mini}<span>{n} + 1</span></td><td><span class='chk'></span></td></tr>")
    else:
        for n, day, d in NIGHTS_EN:
            mini = S(art.hanukkiah(color=True, lit=n + 1, count=n, sw=4), "20 90 360 240", style="height:11mm;width:auto")
            rows.append(f"<tr><td><b>{n}</b></td><td>{e(day)}</td><td>{d}, 2026</td><td>{mini}<span>{n} + 1</span></td><td><span class='chk'></span></td></tr>")
    head = "".join(f"<th>{e(c)}</th>" for c in t["chart_cols"])
    notes = "".join(f"<li>{e(x)}</li>" for x in t["chart_notes"])
    return f'<table class="chart"><tr>{head}</tr>{"".join(rows)}</table><ul class="notes">{notes}</ul>'


def p_brachot(t, lang, ctx):
    blocks = []
    for i, b in enumerate(BRACHOT_HE):
        lbl = t["brachot_labels"][i]
        if lang == "he":
            blocks.append(f'<div class="bracha"><span class="bl">{e(lbl)}</span><p class="heb" lang="he" dir="rtl">{e(b)}</p></div>')
        else:
            tr, en = BRACHOT_EN[i]
            blocks.append(f'<div class="bracha"><span class="bl">{e(lbl)}</span><p class="heb sm" lang="he" dir="rtl">{e(b)}</p>'
                          f'<p class="tr">{e(tr)}</p><p class="en">{e(en)}</p></div>')
    return (f'<div class="brachot">{"".join(blocks)}<p class="note">{e(t["brachot_note"])}</p>'
            f'<div class="br-art">{S(art.hanukkiah(color=True, lit=2, count=1), "0 0 400 330")}</div></div>')


def p_kind(t, lang, ctx):
    rows = []
    nights = NIGHTS_HE if lang == "he" else NIGHTS_EN
    for row in nights:
        n, d = row[0], row[2]
        c = S(art.candle(12, 44, w=10, h=26, color=False, sw=2), "0 0 24 50", style="height:12mm;width:auto")
        rows.append(f'<div class="kd">{c}<div><b>{e(t["night"])} {n}</b> · {e(d)}<div class="ln">{e(t["deed"])}</div></div><span class="chk"></span></div>')
    return f'<div class="kind">{"".join(rows)}</div>'


def p_cards(t, lang, ctx):
    a = S(art.hanukkiah(color=False, lit=9, sw=4), "0 0 400 330")
    b = S(art.dreidel(color=False, letter=art.DREIDEL_LETTERS[lang][1], side_letter=art.DREIDEL_LETTERS[lang][3], sw=4) , "0 0 240 300")
    def card(artsvg, txt):
        return (f'<div class="card"><div class="c-art">{artsvg}</div><div class="c-txt">{e(txt)}</div>'
                f'<div class="c-lines"><span>{e(t["to"])} ____________________</span><span>{e(t["frm"])} ____________________</span></div></div>')
    return f'<div class="cards">{card(a, t["card_texts"][0])}<div class="cut">✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -</div>{card(b, t["card_texts"][1])}</div>'


def p_answers(t, lang, ctx):
    grid, placed, words = ctx["ws"]
    frag, size = puzzles.word_search_svg(grid, placed, cell=34, rtl=lang == "he", answers=True)
    return (f'<div class="answers"><div><h3>{e(t["pages"]["maze1"][0])}</h3>{maze1(t, lang, True)}</div>'
            f'<div><h3>{e(t["pages"]["maze2"][0])}</h3>{maze2(t, lang, True)}</div>'
            f'<div><h3>{e(t["pages"]["ws"][0])}</h3>{S(frag, f"-2 -2 {size + 4} {size + 4}")}</div>'
            f'<div><h3>{e(t["pages"]["cbn"][0])}</h3>{cbn_answer()}</div></div>')


PAGES = {k: globals()["p_" + k] for k in ORDER}

CSS = """
@font-face{font-family:Fredoka;src:url(FONTS/Fredoka-600.ttf);font-weight:400 600}
@font-face{font-family:Fredoka;src:url(FONTS/Fredoka-700.ttf);font-weight:700 900}
@font-face{font-family:Assistant;src:url(FONTS/Assistant-400.ttf);font-weight:400}
@font-face{font-family:Assistant;src:url(FONTS/Assistant-700.ttf);font-weight:700}
@font-face{font-family:Nunito;src:url(FONTS/Nunito-400.ttf);font-weight:400}
@font-face{font-family:Nunito;src:url(FONTS/Nunito-700.ttf);font-weight:700}
@font-face{font-family:'Noto Sans Hebrew';src:url(FONTS/NotoSansHebrew-400.ttf);font-weight:400}
@font-face{font-family:'Noto Sans Hebrew';src:url(FONTS/NotoSansHebrew-700.ttf);font-weight:700}
@page{size:PW PH;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:BODY;color:#1b1b1b;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:PW;height:PH;padding:11mm 12mm 8mm;display:flex;flex-direction:column;page-break-after:always;break-after:page;position:relative;overflow:hidden}
.page:before{content:"";position:absolute;inset:6mm;border:1.2mm solid #2f6db5;border-radius:6mm;pointer-events:none}
.page:after{content:"";position:absolute;inset:7.8mm;border:.35mm dashed #f2b632;border-radius:5mm;pointer-events:none}
.ph{text-align:center;padding:2mm 6mm 0}
.ph h1{font-family:Fredoka,sans-serif;font-weight:700;font-size:25pt;margin:1mm 0 1mm;color:#173a66}
.ph p{margin:0 0 1mm;font-size:12.5pt;color:#333}
.pb{flex:1;min-height:0;display:flex;flex-direction:column;padding:3mm 6mm 2mm}
.pf{display:flex;justify-content:space-between;font-size:8pt;color:#666;padding:0 6mm 1mm}
.pn{font-family:Fredoka;font-weight:700;color:#2f6db5;font-size:10pt}
.art{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;gap:6mm}
.art svg{max-height:100%}
.art.two>svg{width:48%!important}
.art.col{flex-direction:column}.art.col>div{flex:1;min-height:0;width:100%;display:flex;justify-content:center}
/* cover */
.cover{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;background:linear-gradient(#173a66,#2f6db5);border-radius:4mm;margin:-1mm -4mm;padding:8mm 8mm 6mm;color:#fff}
.cov-year{font-family:Fredoka;font-weight:600;font-size:15pt;letter-spacing:.04em;color:#fde68a}
.cov-title{font-family:Fredoka;font-weight:700;font-size:40pt;line-height:1.05;margin:3mm 0 2mm}
.cov-sub{font-size:14pt;margin:0 0 3mm;max-width:150mm}
.cov-art{flex:1;min-height:0;width:100%;display:flex;justify-content:center;background:#fff7e6;border-radius:6mm;padding:6mm}
.cov-row{display:flex;gap:6mm;height:42mm;margin:5mm 0 3mm;justify-content:center}.cov-row>div{background:#fff7e6;border-radius:5mm;padding:3mm;width:48mm;display:flex;justify-content:center}
.cov-dates{font-weight:700;font-size:13pt;margin:1mm 0}.cov-ages{margin:0;font-size:12pt;color:#fde68a}
/* toc */
.toc{display:flex;gap:7mm;flex:1}
.toc-list{flex:1;margin:0;padding:0;list-style:none;font-size:12.5pt}
.toc-list li{display:flex;justify-content:space-between;border-bottom:.3mm dotted #999;padding:1.6mm 0}
.toc-list b{font-family:Fredoka;color:#2f6db5}
.toc-side{width:44%;display:flex;flex-direction:column;gap:4mm}
.box{background:#eef4fb;border-radius:4mm;padding:3mm 5mm;font-size:11pt}.box h2{font-family:Fredoka;font-size:14pt;margin:1mm 0;color:#173a66}.box ul{padding-inline-start:5mm;margin:1mm 0}
.toc-art{flex:1;min-height:0;display:flex;justify-content:center}
/* count */
.grid3{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:4mm}
.cnt{border:.5mm solid #cfd8e3;border-radius:4mm;display:flex;align-items:center;gap:3mm;padding:2mm 4mm;min-height:0}
.cnt svg{flex:1;height:100%;min-width:0}
.ans{width:17mm;height:17mm;border:.7mm solid #1b1b1b;border-radius:3mm;flex:none}
/* cbn */
.cbn{flex:1;display:flex;flex-direction:column;min-height:0}
.legend{display:flex;flex-wrap:wrap;gap:2mm 6mm;justify-content:center;list-style:none;padding:0;margin:3mm 0 0;font-size:12pt}
.legend i{display:inline-block;width:5mm;height:5mm;border:.3mm solid #333;border-radius:1mm;vertical-align:middle;margin-inline-end:1.5mm}
/* word search */
.ws{flex:1;display:flex;flex-direction:column;min-height:0}
.wl{margin-top:3mm;font-size:13pt}.wl ul{display:flex;flex-wrap:wrap;gap:1.5mm 5mm;list-style:none;margin:1.5mm 0 0;padding:0}
.wl li{font-family:Fredoka;font-weight:600;letter-spacing:.03em}.wl li:before{content:"☐ ";color:#2f6db5}
/* rules */
.letters{display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.lt{display:flex;gap:3mm;align-items:center;background:#eef4fb;border-radius:4mm;padding:2mm 4mm}
.lt-d{width:20mm;height:25mm;flex:none}.lt-n{font-family:Fredoka;font-size:16pt;color:#173a66}.lt p{margin:.5mm 0 0;font-size:12pt}
.steps{font-size:12.5pt;line-height:1.55;margin:4mm 0 2mm;padding-inline-start:7mm}
.note{font-size:11pt;background:#fff7e6;border-radius:3mm;padding:2.5mm 4mm;margin:2mm 0}
/* tables */
table{border-collapse:collapse;width:100%}
.score{flex:1;font-size:12pt}.score th,.score td{border:.4mm solid #333;padding:1mm 2mm;text-align:center}
.score th{background:#eef4fb;font-family:Fredoka;font-weight:600}.score .nm{font-family:inherit;font-weight:400;font-size:8.5pt;color:#555;margin-top:1mm}
.score td:first-child{width:16mm;font-weight:700;background:#fafafa}.score tr.tot td{background:#fff7e6;font-weight:700;height:12mm}
.score tr td{height:13mm}
.chart{font-size:12pt}.chart th,.chart td{border:.4mm solid #333;padding:1mm 2mm;text-align:center;vertical-align:middle}
.chart th{background:#eef4fb;font-family:Fredoka;font-weight:600}
.chart td svg{vertical-align:middle}.chart td span{display:inline-block;margin-inline-start:2mm;font-weight:700}
.chk{display:inline-block;width:8mm;height:8mm;border:.6mm solid #1b1b1b;border-radius:1.5mm}
.notes{font-size:11pt;line-height:1.5;margin:4mm 0 0;padding-inline-start:5mm}
/* diy */
.diy{flex:1;display:flex;flex-direction:column;justify-content:space-between}
/* brachot */
.brachot{flex:1;display:flex;flex-direction:column;gap:3mm}
.bracha{border:.5mm solid #cfd8e3;border-radius:4mm;padding:2.5mm 5mm;background:#fbfdff}
.bl{font-family:Fredoka;font-weight:600;color:#2f6db5;font-size:11pt}
.heb{font-family:'Noto Sans Hebrew',sans-serif;font-size:21pt;line-height:1.75;margin:1mm 0;text-align:right}
.heb.sm{font-size:16pt;line-height:1.6}
.tr{font-style:italic;font-size:12.5pt;margin:1mm 0}.en{font-size:12pt;margin:1mm 0;color:#333}
.br-art{flex:1;min-height:0;display:flex;justify-content:center}
/* kindness */
.kind{flex:1;display:grid;grid-template-rows:repeat(8,1fr);gap:2.4mm}
.kd{display:flex;align-items:center;gap:3mm;border:.4mm solid #cfd8e3;border-radius:3mm;padding:1mm 4mm;font-size:12pt}
.kd>div{flex:1}.kd .ln{border-bottom:.4mm solid #999;height:8mm;margin-top:1mm;color:#666;font-size:10pt}
/* cards */
.cards{flex:1;display:flex;flex-direction:column}
.card{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;border:.6mm solid #1b1b1b;border-radius:5mm;padding:3mm}
.c-art{flex:1;min-height:0;width:100%;display:flex;justify-content:center}
.c-txt{font-family:Fredoka;font-weight:700;font-size:30pt;color:#fff;-webkit-text-stroke:.5mm #1b1b1b;margin:1mm 0}
.c-lines{display:flex;gap:8mm;font-size:11pt}
.cut{color:#888;white-space:nowrap;overflow:hidden;margin:2mm 0;font-size:11pt}
/* answers */
.answers{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:4mm;min-height:0}
.answers>div{display:flex;flex-direction:column;min-height:0;border:.4mm solid #cfd8e3;border-radius:3mm;padding:2mm}
.answers h3{font-family:Fredoka;font-size:11pt;margin:0 0 1mm;text-align:center}
.answers svg{flex:1;min-height:0;width:100%}

.pb>*{min-height:0}
.rules{flex:1;display:flex;flex-direction:column}
.lt{padding:3mm 4mm}.lt-d{width:24mm;height:30mm}.lt-n{font-size:19pt}.lt p{font-size:13.5pt}
.rules .steps{font-size:14pt;line-height:1.65}
.chart{font-size:13.5pt}.chart td{height:17mm}.chart td svg{height:14mm!important}
.notes{font-size:12.5pt;line-height:1.6}
.kd{font-size:13pt}
.cover{padding:7mm 8mm 5mm}.cov-row{height:38mm;margin:4mm 0 2mm}
.diy .art{flex:none}.diy .steps{font-size:14pt;line-height:1.7}
"""


def build_html(lang, paper):
    t = T[lang]
    pw, ph = PAPER[paper]
    body_font = "Assistant,'Noto Sans Hebrew',sans-serif" if lang == "he" else "Nunito,sans-serif"
    css = CSS.replace("FONTS", FONTS).replace("PW", pw).replace("PH", ph).replace("BODY", body_font)
    ctx = {"ws": wordsearch(lang)}
    pages = []
    for i, k in enumerate(ORDER, start=1):
        pages.append(frame(t, k, PAGES[k](t, lang, ctx), i, cls="cover-page" if k == "cover" else ""))
    title = t["title"] + " – " + t["year"]
    return (f'<!doctype html><html lang="{t["lang"]}" dir="{t["dir"]}"><head><meta charset="utf-8"><title>{e(title)}</title>'
            f"<style>{css}</style></head><body>{''.join(pages)}</body></html>")


BUILDS = [("he", "A4", "hanukkah-activity-pack-he-A4"), ("en", "Letter", "hanukkah-activity-pack-en-Letter"),
          ("en", "A4", "hanukkah-activity-pack-en-A4")]


def main():
    OUT.mkdir(exist_ok=True)
    jobs = []
    for lang, paper, name in BUILDS:
        h = OUT / f"{name}.html"
        h.write_text(build_html(lang, paper), encoding="utf-8")
        jobs.append(f"{h}={OUT / (name + '.pdf')}")
    subprocess.run(["node", str(HERE / "print_pdf.js"), *jobs], check=True)
    print("built", ", ".join(b[2] for b in BUILDS))


if __name__ == "__main__":
    sys.exit(main())
