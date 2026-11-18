// Renders 1200x630 Hebrew og:image PNGs for the top calculators (WhatsApp / social link previews).
//   node tools/site/make_og.js [slug ...]   -> docs/assets/og/<slug>.png  (needs Google Fonts reachable for Assistant)
//   With slugs, only those cards are rendered (e.g. node tools/site/make_og.js chatuna rsvp).
const { chromium } = require("playwright");
const path = require("path");
const OUT = path.resolve(__dirname, "../../docs/assets/og");

const CARDS = [
  { slug: "wedding-gift", eyebrow: "מחשבון חינם · מעודכן 2026", title: "כמה לשים בחתונה?", hl: "לפי מחיר המנה העדכני",
    rows: [["חבר/ה לבד", "≈ ₪400"], ["זוג חברים", "≈ ₪750"], ["משפחה קרובה", "₪1,000+"]], foot: "לפי קרבה, עונה, אזור ויום · תוצאה בשנייה" },
  { slug: "bar-mitzvah-cost", eyebrow: "מחשבון חינם · 2026", title: "כמה עולה בר מצווה?", hl: "וכמה יישאר מהכיס",
    rows: [["150 אורחים, ערב", "≈ ₪61,000"], ["מתנות צפויות", "≈ ₪24,600"], ["מהכיס", "≈ ₪36,600"]], foot: "מנה, DJ, צילום, עיצוב ומתנות · בר ובת מצווה" },
  { slug: "vat-calculator", eyebrow: "מחשבון חינם · 18% מ-2025", title: "מחשבון מע\"מ 18%", hl: "להוסיף או להוריד מע\"מ",
    rows: [["₪1,000 לפני מע\"מ", "₪1,180"], ["₪1,180 כולל מע\"מ", "₪1,000"], ["מע\"מ", "₪180"]], foot: "כולל בונה הצעת מחיר לעוסק פטור ומורשה" },
  { slug: "osek-patur-ceiling", eyebrow: "מחשבון חינם · תקרה 2026", title: "כמה נשאר לי עד התקרה?", hl: "עוסק פטור 2026",
    rows: [["תקרה שנתית", "₪122,833"], ["קצב חודשי", "מחושב"], ["מתי חוצים", "חודש משוער"]], foot: "לפי ההכנסות שלכם מתחילת השנה · בלי הרשמה" },
  { slug: "chatuna", eyebrow: "מתחתנים או מוזמנים?", title: "הכל לחתונה", hl: "כלים חינם בעברית",
    rows: [["כמה לשים בחתונה", "מחשבון"], ["כמה תעלה החתונה", "מחשבון"], ["אישורי הגעה והושבה", "אונליין"]], foot: "לאורחים ולזוגות · בלי הרשמה, הנתונים נשארים אצלכם" },
  { slug: "wedding-cost", eyebrow: "מחשבון חינם · מחירי 2026", title: "כמה עולה חתונה?", hl: "לפי מוזמנים, אזור ועונה",
    rows: [["קיץ, 250 איש", "≈ ₪185,000"], ["אותה חתונה בחורף", "≈ ₪158,000"], ["מהכיס אחרי מתנות", "≈ ₪82,000"]], foot: "מנה, ספקים, טווח מחירים ומתנות צפויות" },
  { slug: "wedding-timeline", eyebrow: "כלי חינם · להדפסה וליומן", title: "מה לסגור ומתי?", hl: "לוח זמנים לחתונה",
    rows: [["12 חודשים לפני", "תקציב ואולם"], ["6 שבועות לפני", "אישורי הגעה"], ["10 ימים לפני", "הושבה"]], foot: "מזינים תאריך ומקבלים צ'קליסט חודש אחר חודש" },
  { slug: "rsvp", eyebrow: "חינם עד 80 הזמנות", title: "אישורי הגעה לחתונה", hl: "בלי חברה ובלי מנוי",
    rows: [["ייבוא אנשי קשר", "VCF / אקסל"], ["תזכורת לכל אורח", "וואטסאפ"], ["העברה להושבה", "בלחיצה"]], foot: "מי מגיע, כמה ומה אוכלים · הנתונים נשארים אצלכם" },
];
const ONLY = process.argv.slice(2);

const css = `
@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap');
*{box-sizing:border-box;margin:0}
html{overflow:hidden}.bg{position:absolute;inset:0;overflow:hidden}
body{width:1200px;height:630px;overflow:hidden;background:#fbf8f3;font-family:Assistant,sans-serif;color:#1d2a2e;position:relative}
.b1{position:absolute;width:520px;height:520px;border-radius:50%;background:#fcefd6;left:-160px;top:-180px}
.b2{position:absolute;width:420px;height:420px;border-radius:50%;background:#e2f1ee;left:120px;bottom:-260px}
.wrap{position:absolute;inset:0;padding:56px 64px;display:flex;gap:48px;align-items:center}
.txt{flex:1 1 0;min-width:0}
.brand{display:flex;align-items:center;gap:14px;font-weight:800;font-size:34px;margin-bottom:26px}
.logo{width:56px;height:56px;border-radius:14px;background:#0e6b63;display:grid;place-items:center;color:#f0b44c;font-size:34px}
.eyebrow{display:inline-block;background:#e2f1ee;color:#0e6b63;font-weight:700;font-size:26px;padding:6px 18px;border-radius:999px;margin-bottom:18px}
h1{font-size:68px;line-height:1.05;font-weight:800;letter-spacing:-.5px}
.hl{font-size:46px;font-weight:800;color:#0e6b63;margin-top:10px;line-height:1.1}
.foot{font-size:27px;color:#586770;margin-top:22px}
.card{flex:0 0 430px;background:#fff;border:2px solid #e5ddcf;border-radius:22px;box-shadow:0 10px 40px rgba(29,42,46,.12);padding:26px 30px;position:relative;z-index:1}
.row{display:flex;justify-content:space-between;align-items:baseline;padding:14px 0;border-bottom:2px dashed #eee5d6;font-size:26px;gap:16px}
.row:last-child{border:0}
.row b{font-size:32px;color:#0e6b63;font-weight:800;direction:ltr;unicode-bidi:isolate;white-space:nowrap}
.wa{margin-top:16px;display:inline-flex;gap:10px;align-items:center;background:#167a41;color:#fff;font-weight:700;font-size:24px;padding:10px 20px;border-radius:999px}
`;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const c of CARDS.filter(c => !ONLY.length || ONLY.includes(c.slug))) {
    const rows = c.rows.map(r => `<div class="row"><span>${r[0]}</span><b>${r[1]}</b></div>`).join("");
    await page.setContent(`<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>${css}</style></head><body>
<div class="bg"><div class="b1"></div><div class="b2"></div></div><div class="wrap"><div class="txt">
<div class="brand"><span class="logo">★</span>תכנון פלוס</div><span class="eyebrow">${c.eyebrow}</span>
<h1>${c.title}</h1><div class="hl">${c.hl}</div><div class="foot">${c.foot}</div></div>
<div class="card">${rows}<span class="wa">שתפו בוואטסאפ ←</span></div></div></body></html>`, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(OUT, c.slug + ".png") });
    console.log("wrote", c.slug);
  }
  await browser.close();
})();
