/* לוח זמנים אישי לחתונה (תכנון פלוס) – client-side only. Ticks are kept in this browser (localStorage). */
(function () {
  "use strict";
  var f = document.getElementById("tl-form");
  if (!f) return;
  var KEY = "tp-timeline-v1";
  var R = "../../"; // site root from this page
  // [id, days before the wedding (negative = after), title, detail, link, only for: "rabbanut" | "other" | undefined]
  var TASKS = [
    ["budget", 365, "שיחת כסף ותקרת תקציב", "מי משתתף ובכמה, ותקרה כוללת עם רזרבה של 3%–5%.", ["tools/wedding-cost/", "מחשבון עלות חתונה"]],
    ["guests", 360, "רשימת מוזמנים ראשונית", "גם גסה: היא קובעת גודל אולם ומינימום מנות.", ["apps/rsvp/", "רשימת מוזמנים"]],
    ["dates", 350, "עונה, יום בשבוע ו-2–3 תאריכים אפשריים", "חורף ואמצע השבוע זולים בעשרות אחוזים; חמישי בקיץ נתפס ראשון."],
    ["venues", 335, "סיור ב-3–5 אולמות והשוואת הצעות", "שאלו מה כלול במנה, מה המינימום ומה תנאי הביטול.", ["guides/wedding-vendor-contracts/", "בדיקת חוזה עם אולם"]],
    ["venue", 320, "חתימה על חוזה אולם ומקדמה", "רק אחרי שיש רשימה ראשונית ותקרת תקציב."],
    ["photo", 290, "צלם סטילס ווידאו", "בקשו לראות חתונה מלאה ולא רק תמונות נבחרות."],
    ["dj", 280, "DJ או להקה", "בדקו אם הגברה ותאורה כלולות באולם כדי לא לשלם פעמיים."],
    ["rabbi", 270, "מי שיערוך את החופה", "רב מטעם הרבנות או מסדר קידושין מוכר; בררו דמי נסיעה.", null, "rabbanut"],
    ["ceremony", 270, "מי יערוך את הטקס ואיפה", "טקס אזרחי בחו\"ל, זוגיות אחרת או טקס פרטי: בררו מה נדרש לרישום בישראל.", null, "other"],
    ["decor", 250, "עיצוב ופרחים", "רק אם הם לא חלק מהחבילה של האולם."],
    ["dress", 210, "שמלה: תפירה או השכרה", "תפירה דורשת כמה חודשים ומדידות; השכרה אפשר לסגור מאוחר יותר."],
    ["makeup", 180, "איפור ושיער + מועד לניסיון", "מאפרות טובות נתפסות לעונה כולה."],
    ["rings", 150, "טבעות", "לחופה דרך הרבנות הטבעת צריכה לעמוד בדרישות ההלכתיות: שאלו את עורך החופה."],
    ["suit", 120, "חליפה ונעליים", "בדרך כלל מספיקים חודשיים-שלושה כולל תיקונים."],
    ["invite", 110, "עיצוב ההזמנה", "הזמנה לוואטסאפ (PNG) ולדפוס (PDF).", ["p/invitation-maker/", "מעצב ההזמנות"]],
    ["list", 100, "רשימה סופית: שורה לכל הזמנה עם טלפון", "בלי טלפונים אין תזכורות ואין אישורי הגעה.", ["apps/rsvp/", "רשימת מוזמנים"]],
    ["transport", 100, "הסעות לאורחים (אם צריך)", "כשהאולם רחוק או כשיש קבוצה גדולה מעיר אחת."],
    ["register", 90, "פתיחת תיק ברבנות (לשכת רישום הנישואין)", "לרוב בין כ-3 חודשים לכ-45 יום לפני. התקשרו ללשכה ובררו מסמכים ומועדים.", ["guides/wedding-checklist/", "פירוט בצ'קליסט"], "rabbanut"],
    ["kallah", 75, "הדרכת חתנים וכלות", "מתואמת בדרך כלל דרך לשכת הרישום.", null, "rabbanut"],
    ["civil", 75, "מסמכים לטקס בחו\"ל ותכנון הרישום במשרד הפנים", "תהליך נפרד שכדאי לבדוק מראש.", null, "other"],
    ["send", 50, "שליחת ההזמנות", "כחודשיים עד שישה שבועות לפני.", ["p/invitation-maker/", "מעצב ההזמנות"]],
    ["rsvp1", 42, "סבב ראשון של אישורי הגעה", "תזכורת בוואטסאפ בלחיצה לכל מי שלא ענה.", ["apps/rsvp/", "אישורי הגעה"]],
    ["venuemeet", 30, "פגישת תיאום עם האולם", "מבנה הערב, תפריט סופי ומנות מיוחדות (צמחוני, טבעוני, ללא גלוטן, ילדים)."],
    ["songs", 28, "רשימת שירים עם ה-DJ", "כניסה לחופה, שבירת הכוס, ריקוד ראשון."],
    ["dayplan", 25, "לוח זמנים ליום עצמו", "איפור, צילומי זוגיות, קבלת פנים, חופה, ריקודים."],
    ["envelopes", 21, "מעטפות לתשלומים ולטיפים", "עם שם הספק על כל מעטפה."],
    ["insurance", 21, "ביטוח", "בדקו אם האולם מבוטח ומה הביטוח מכסה."],
    ["count", 14, "מספר מנות סופי לאולם", "לפי המאשרים בפועל, לא לפי המוזמנים.", ["apps/rsvp/", "ספירת אישורים"]],
    ["seating", 10, "סידור הושבה + שולחן גמיש למאחרים", "מעבירים את המאשרים מרשימת המוזמנים בלחיצה.", ["apps/seating/", "סידורי הושבה"]],
    ["confirm", 7, "אישור שעות הגעה מכל ספק בכתב", "כולל כתובת מדויקת ואיש קשר ביום."],
    ["pay", 7, "מה נשאר לשלם, למי ובאיזה אמצעי", ""],
    ["pickup", 3, "איסוף לבוש, טבעות ומסמכים", "הכל במקום אחד; אדם קרוב מחזיק את רשימת הספקים והטלפונים."],
    ["day", 0, "ביום: תיק קטן ותיבת צ'קים עם אחראי אחד", "תעודות זהות, מסמכים, מטען, מים ונעליים להחלפה."],
    ["gifts", -1, "רישום מתנות, כולל ביט ופייבוקס", "כבר למחרת, כל עוד הזיכרון טרי.", ["p/wedding-planner/", "מתכנן החתונה"]],
    ["checks", -7, "הפקדת צ'קים", "לצ'ק יש תוקף מוגבל."],
    ["thanks", -14, "הודעות תודה אישיות", "בשבועיים הראשונים."],
    ["cert", -30, "תעודת נישואין ועדכון מרשם האוכלוסין", "התעודה מונפקת אחרי שעורך החופה מחזיר את המסמכים ללשכה.", null, "rabbanut"],
    ["money", -30, "סיכום כספי: עלות מול מתנות", "ומה עושים עם מה שנשאר.", ["tools/savings-goal/", "מחשבון יעד חיסכון"]]
  ];
  var DAY = 86400000;
  var done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || "{}").done || {}; } catch (e) {}
  function persist() { try { localStorage.setItem(KEY, JSON.stringify({ done: done })); } catch (e) {} }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function val(name) { var el = f.querySelector('[name="' + name + '"]:checked') || f.elements[name]; return el ? el.value : null; }
  function today() { var d = new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function fmt(d) { return d.getDate() + "." + (d.getMonth() + 1) + "." + d.getFullYear(); }
  function monthName(d) { return d.toLocaleDateString("he-IL", { month: "long", year: "numeric" }); }
  function $(id) { return document.getElementById(id); }

  function wedding() {
    var y = +val("year"), m = +val("month"), dd = Math.max(1, Math.min(31, parseInt(f.elements.day.value, 10) || 1));
    var d = new Date(y, m - 1, dd);
    if (d.getMonth() !== m - 1) d = new Date(y, m, 0); // 31 in a 30-day month -> last day
    return d;
  }
  function plan() {
    var w = wedding(), t0 = today(), kind = val("ceremony");
    var items = TASKS.filter(function (x) { return !x[5] || x[5] === kind; }).map(function (x) {
      var due = new Date(w.getTime() - x[1] * DAY);
      return { id: x[0], days: x[1], title: x[2], detail: x[3], link: x[4], due: due, late: due < t0 && x[1] > 0 };
    });
    return { w: w, t0: t0, items: items, left: Math.round((w - t0) / DAY) };
  }
  function when(days) {
    if (days <= 0) return days === 0 ? "ביום החתונה" : "אחרי החתונה";
    if (days >= 60) return "לרוב כ-" + Math.round(days / 30) + " חודשים לפני";
    if (days >= 14) return "לרוב כ-" + Math.round(days / 7) + " שבועות לפני";
    return "לרוב " + days + " ימים לפני";
  }

  function render() {
    var P = plan();
    var out = $("tl-out");
    if (P.left < 0) {
      $("tl-summary").textContent = "התאריך שבחרתם כבר עבר. מזל טוב! למטה: מה נשאר לעשות אחרי החתונה.";
    } else {
      var mo = Math.floor(P.left / 30.44), dd = Math.round(P.left - mo * 30.44);
      $("tl-summary").textContent = "עד החתונה (" + fmt(P.w) + "): " + (mo ? mo + " חודשים" + (dd ? " ו-" : "") : "") + (dd || !mo ? dd + " ימים" : "") + ".";
    }
    var late = P.items.filter(function (i) { return i.late; });
    var rest = P.items.filter(function (i) { return !i.late && (P.left >= 0 || i.days <= 0); });
    var short = P.left >= 0 && P.left < 183;
    $("tl-short").hidden = !short;
    var groups = [], cur = null;
    rest.sort(function (a, b) { return a.due - b.due; }).forEach(function (i) {
      var key = i.days < 0 ? "after" : i.days === 0 ? "day" : i.due.getFullYear() + "-" + i.due.getMonth();
      if (!cur || cur.key !== key) {
        cur = { key: key, title: key === "after" ? "אחרי החתונה" : key === "day" ? "ביום החתונה · " + fmt(P.w) : monthName(i.due), items: [] };
        groups.push(cur);
      }
      cur.items.push(i);
    });
    if (late.length && P.left >= 0) groups.unshift({ key: "now", title: "להשלים עכשיו (" + late.length + ")", items: late, late: true });
    var total = 0, ticked = 0;
    out.innerHTML = groups.map(function (g) {
      return '<section class="tl-month' + (g.late ? " late" : "") + '"><h3>' + esc(g.title) + "</h3><ul>" + g.items.map(function (i) {
        total++; if (done[i.id]) ticked++;
        return '<li class="' + (done[i.id] ? "done" : "") + '"><label><input type="checkbox" data-task="' + i.id + '"' + (done[i.id] ? " checked" : "") + "><span><strong>" + esc(i.title) + "</strong>" +
          '<span class="tl-when">' + (i.days > 0 ? "עד " + fmt(i.due) + " · " : i.days < 0 ? "עד " + fmt(i.due) + " · " : "") + when(i.days) + "</span>" +
          (i.detail ? '<span class="tl-detail">' + esc(i.detail) + "</span>" : "") + "</span></label>" +
          (i.link ? '<a class="tl-link" href="' + R + i.link[0] + '">' + esc(i.link[1]) + " ←</a>" : "") + "</li>";
      }).join("") + "</ul></section>";
    }).join("");
    $("tl-progress").textContent = ticked + " מתוך " + total + " משימות סומנו";
    $("tl-bar").style.width = (total ? Math.round(ticked / total * 100) : 0) + "%";
  }

  function ics() {
    var P = plan();
    var d8 = function (d) { return d.getFullYear() + String(d.getMonth() + 1).padStart(2, "0") + String(d.getDate()).padStart(2, "0"); };
    var e = function (s) { return String(s).replace(/[\\;,]/g, function (c) { return "\\" + c; }).replace(/\n/g, "\\n"); };
    var stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
    var lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Tichnun Plus//Wedding timeline//HE", "CALSCALE:GREGORIAN", "X-WR-CALNAME:" + e("לוח זמנים לחתונה")];
    P.items.forEach(function (i) {
      if (done[i.id]) return;
      var d = i.late ? P.t0 : i.due, n = new Date(d.getTime() + DAY);
      lines.push("BEGIN:VEVENT", "UID:" + i.id + "-" + d8(P.w) + "@tichnun.netlify.app", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + d8(d), "DTEND;VALUE=DATE:" + d8(n),
        "SUMMARY:" + e("💍 " + i.title), "DESCRIPTION:" + e(i.detail + (i.link ? "\n" + new URL(R + i.link[0], location.href).href : "")), "END:VEVENT");
    });
    lines.push("END:VCALENDAR");
    var blob = new Blob([lines.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "wedding-timeline.ics";
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  $("tl-out").addEventListener("change", function (e) {
    var c = e.target.closest("[data-task]"); if (!c) return;
    if (c.checked) done[c.getAttribute("data-task")] = 1; else delete done[c.getAttribute("data-task")];
    persist(); render();
  });
  $("tl-print").addEventListener("click", function () { window.print(); });
  $("tl-ics").addEventListener("click", ics);
  f.addEventListener("input", render);
  f.addEventListener("change", render);
  f.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  render();
  window.WeddingTimeline = { plan: plan, render: render, TASKS: TASKS };
})();
