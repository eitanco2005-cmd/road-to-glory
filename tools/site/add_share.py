#!/usr/bin/env python3
"""One-off (idempotent) wiring of assets/share.js into the free calculators. Kept for reference / re-runs."""
import html, pathlib, sys
DOCS = pathlib.Path(__file__).resolve().parents[2] / "docs"
NOTE_PRIV = "הקישור כולל את המספרים שהזנתם – שלחו אותו רק למי שתרצו."

def box(depth, scope, result, msg, note=None):
    a = f'<div data-share data-share-scope="{scope}"'
    if result: a += f' data-share-result="{result}"'
    a += f' data-share-msg="{html.escape(msg, quote=True)}"'
    if note: a += f' data-share-note="{html.escape(note, quote=True)}"'
    return a + f'></div>\n<script src="{"../" * depth}assets/share.js"></script>\n'

# page, depth, anchor (insert BEFORE unless after=True), replacements first, scope, result, msg, note
PAGES = [
 ("tools/wedding-gift", 2, '   <div class="table-wrap mt-2">\n    <table><caption class="sr-only">סכום לפי', [], "#gift-form", "#r-amount,#r-who",
  "לפי המחשבון של תכנון פלוס כדאי לשים בחתונה {result} ({result2}). בדקו כמה לשים אתם:", None),
 ("tools/bar-mitzvah-cost", 2, '   <noscript><p class="noscript">המחשבון צריך JavaScript.</p></noscript>\n  </form>', [], "#bm-form", "#r-total,#r-per",
  "עלות משוערת לבר/בת מצווה: {result} ({result2} לאורח). חשבו את שלכם במחשבון החינמי של תכנון פלוס:", None),
 ("tools/budget-503020", 2, '        </div>\n      </div>\n', [('          <p class="w3-note mt-2"><a href="#" id="share">העתיקו קישור לחישוב הזה</a> <span id="copied" hidden>✓ הועתק</span></p>\n', "")],
  "#calc", "", "חילקתי את ההכנסה לפי שיטת 50/30/20 במחשבון החינמי של תכנון פלוס. נסו גם אתם:", NOTE_PRIV),
 ("tools/net-salary-budget", 2, '      </div>\n    </div>\n\n    <div class="cta-box mt-4">', [(' · <a href="#" id="share">העתיקו קישור לחישוב</a> <span id="copied" hidden>✓ הועתק</span>', "")],
  "#calc", "", "בניתי תקציב חודשי לפי המשכורת נטו במחשבון החינמי של תכנון פלוס. נסו גם אתם:", NOTE_PRIV),
 ("tools/osek-patur-ceiling", 2, '   </div>\n   <p class="source mt-2">מקור התקרה', [('  <div class="tool-panel">', '  <div class="tool-panel" id="osek-panel">')],
  "#osek-panel", "", "בדקתי כמה נשאר לי עד תקרת עוסק פטור 2026 במחשבון החינמי של תכנון פלוס. בדקו גם אתם:", NOTE_PRIV),
 ("tools/renovation-cost", 2, '      </div>\n    </div>\n', [], "#calc", "#total",
  "אומדן לשיפוץ (כולל בלת\"מ): {result}. חשבו את השיפוץ שלכם במחשבון החינמי של תכנון פלוס:", None),
 ("tools/savings-goal", 2, '        </div>\n      </div>\n', [('          <p class="small muted mt-1"><a href="#" id="share">העתיקו קישור לחישוב הזה</a> <span id="copied" hidden>✓ הועתק</span></p>\n', "")],
  "#calc", "", "תכננתי יעד חיסכון במחשבון החינמי של תכנון פלוס. נסו גם אתם:", NOTE_PRIV),
 ("tools/sufganiyot-calculator", 2, '</div></div></div>\n<div class="cta-box mt-4">', [], "#calc", "#v-suf,#v-lat",
  "לפי מחשבון חנוכה של תכנון פלוס צריך {result} סופגניות ו-{result2} לביבות. חשבו לאירוח שלכם:", None),
 ("tools/vat-calculator", 2, '   </div>\n  </div>\n', [('  <div class="tool-panel">\n', '  <div class="tool-panel" id="vat-panel">\n', 1)],
  "#vat-panel", "#v-biglabel,#v-big", "{result}: {result2}. חישוב מע\"מ 18% במחשבון החינמי של תכנון פלוס:", None),
 ("en/tools/bar-mitzvah-budget", 3, '    <div class="table-wrap mt-2"><table id="breakdown">', [], "#bud", "#total",
  "Our bar/bat mitzvah budget estimate: {result}. Build yours with this free calculator:", None),
 ("en/tools/bar-mitzvah-gift", 3, '  </form>', [], "#gift-form", "#amount",
  "Suggested bar/bat mitzvah gift: {result}. Work out yours with this free calculator:", None),
 ("en/tools/seder-shopping-calculator", 3, '    <p class="source mt-1">Ritual amounts', [], "#seder", "#k-seats,#k-wine",
  "Our seder shopping list: {result} place settings and {result2} bottles of wine. Make yours:", None),
 ("en/hanukkah/latke-calculator", 3, '</div></div></div>\n<div class="cta-box mt-4">', [], "#calc", "#v-lat,#v-suf",
  "Hanukkah party math: {result} latkes and {result2} doughnuts. Plan yours with this free calculator:", None),
]

for slug, depth, anchor, reps, scope, result, msg, note in PAGES:
    p = DOCS / slug / "index.html"
    s = p.read_text(encoding="utf-8")
    if "data-share " in s or "data-share>" in s:
        print("skip", slug); continue
    for r in reps:
        old, new = r[0], r[1]
        assert old in s, (slug, old[:40])
        s = s.replace(old, new, r[2] if len(r) > 2 else -1)
    assert anchor in s, (slug, anchor[:50])
    s = s.replace(anchor, box(depth, scope, result, msg, note) + anchor, 1)
    p.write_text(s, encoding="utf-8")
    print("wired", slug)
