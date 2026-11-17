/* Net salary -> monthly budget calculator (client-side only, nothing is sent anywhere). */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var fmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 0 });
  var ils = function (n) { return (n < 0 ? "−" : "") + "₪" + fmt.format(Math.abs(Math.round(n))); };
  // Starting weights for the money left after housing, debts and savings. Not norms: a starting point to edit.
  var CATS = [
    { k: "bills", n: "חשבונות הבית", h: "ארנונה, חשמל, מים, גז, ועד בית", w: function (s) { return 13 + s.people; } },
    { k: "food", n: "סופר ומזון לבית", h: "קניות שבועיות, שוק, פארם בסיסי", w: function (s) { return 18 + 3 * s.people; } },
    { k: "transport", n: "רכב ותחבורה", h: "דלק, ביטוח רכב, טיפולים, חניה / רב-קו", w: function (s) { return s.car ? 15 : 5; } },
    { k: "health", n: "ביטוחים ובריאות", h: "ביטוח משלים, ביטוח דירה וחיים, תרופות", w: function (s) { return 7; } },
    { k: "kids", n: "ילדים", h: "גן/מעון, צהרון, חוגים, תשלומי הורים", w: function (s) { return s.kids ? 6 + 5 * s.kids : 0; } },
    { k: "comm", n: "תקשורת ומנויים", h: "סלולר, אינטרנט, טלוויזיה, אפליקציות", w: function (s) { return 4; } },
    { k: "clothes", n: "ביגוד והנעלה", h: "", w: function (s) { return 3 + s.people * 0.5; } },
    { k: "fun", n: "פנאי, מסעדות ובילויים", h: "", w: function (s) { return 8; } },
    { k: "gifts", n: "מתנות ושמחות", h: "חתונות, ימי הולדת, אירועים", w: function (s) { return 3; } },
    { k: "annual", n: "הוצאות שנתיות מחולקות ל-12", h: "חגים, חופשה, טסט ואגרה, ציוד לבית הספר", w: function (s) { return 6; } },
    { k: "buffer", n: "בלת״מ", h: "תיקונים ודברים שלא צפיתם", w: function (s) { return 4; } }
  ];
  var edited = {};

  function num(id) {
    var el = $(id); if (!el) return 0;
    var v = parseFloat(String(el.value).replace(/[^\d.]/g, ""));
    return isFinite(v) && v > 0 ? v : 0;
  }
  function state() {
    var adults = Math.max(1, Math.round(num("adults") || 1)), kids = Math.round(num("kids"));
    return { inc: num("income"), housing: num("housing"), debts: num("debts"), savePct: $("savepct").value === "" ? 10 : Math.min(50, num("savepct")),
      adults: adults, kids: kids, people: adults + kids, car: $("car").checked };
  }

  function buildRows() {
    var tb = $("rows"); tb.innerHTML = "";
    CATS.forEach(function (c) {
      var tr = document.createElement("tr");
      tr.innerHTML = '<th scope="row">' + c.n + (c.h ? '<br><span class="small muted">' + c.h + "</span>" : "") + "</th>" +
        '<td><div class="input-affix"><input id="c-' + c.k + '" type="number" inputmode="numeric" min="0" step="50" aria-label="' + c.n + ' בחודש"><span class="affix">₪</span></div></td>' +
        '<td class="num yr" id="y-' + c.k + '"></td>';
      tb.appendChild(tr);
      var inp = tr.querySelector("input");
      inp.addEventListener("input", function () { edited[c.k] = inp.value !== ""; calc(true); });
    });
  }

  function calc(fromRow) {
    var s = state();
    if (!s.inc) { $("out").hidden = true; $("empty").hidden = false; return; }
    $("out").hidden = false; $("empty").hidden = true;
    var save = s.inc * s.savePct / 100;
    var free = s.inc - s.housing - s.debts - save;
    var ws = CATS.map(function (c) { return c.w(s); });
    var wsum = ws.reduce(function (a, b) { return a + b; }, 0);
    // remaining money for non-edited rows
    var editedSum = 0, freeW = 0;
    CATS.forEach(function (c, i) { if (edited[c.k]) editedSum += num("c-" + c.k); else freeW += ws[i]; });
    var pool = Math.max(0, free - editedSum);
    var total = 0, vals = {}, lastFree = null, alloc = 0;
    CATS.forEach(function (c, i) {
      if (edited[c.k]) { vals[c.k] = num("c-" + c.k); return; }
      vals[c.k] = freeW ? Math.round(pool * ws[i] / freeW / 10) * 10 : 0;
      alloc += vals[c.k]; if (ws[i] > 0) lastFree = c.k;
    });
    if (lastFree) vals[lastFree] = Math.max(0, vals[lastFree] + Math.round(pool - alloc));  // rounding remainder goes to the buffer row
    CATS.forEach(function (c, i) {
      var inp = $("c-" + c.k), v = vals[c.k];
      if (!edited[c.k] && document.activeElement !== inp) inp.value = v || "";
      total += v;
      $("y-" + c.k).textContent = ils(v * 12);
    });
    var left = s.inc - s.housing - s.debts - save - total;
    $("k-inc").textContent = ils(s.inc);
    $("k-fixed").textContent = ils(s.housing + s.debts);
    $("k-save").textContent = ils(save);
    $("k-left").textContent = ils(left);
    $("k-left").parentNode.className = "kpi" + (left < -1 ? " danger" : "");
    $("sum-m").textContent = ils(s.housing + s.debts + save + total);
    $("sum-y").textContent = ils((s.housing + s.debts + save + total) * 12);
    $("r-housing").textContent = ils(s.housing); $("ry-housing").textContent = ils(s.housing * 12);
    $("r-debts").textContent = ils(s.debts); $("ry-debts").textContent = ils(s.debts * 12);
    $("r-save").textContent = ils(save); $("ry-save").textContent = ils(save * 12);

    var msgs = [];
    var hp = s.housing / s.inc;
    if (s.housing && hp > 0.4) msgs.push(["warn", "הדיור לוקח " + Math.round(hp * 100) + "% מההכנסה נטו. זה עומס כבד: כל שאר הסעיפים יהיו צפופים, וכדאי לבדוק אם אפשר להגדיל הכנסה או להוזיל דיור בטווח הבינוני."]);
    else if (s.housing && hp > 0.3) msgs.push(["", "הדיור לוקח " + Math.round(hp * 100) + "% מההכנסה נטו. זה נפוץ בישראל, אבל משאיר פחות מרווח לשאר הסעיפים."]);
    if (s.debts / s.inc > 0.2) msgs.push(["warn", "החזרי ההלוואות מעל 20% מההכנסה. שווה לבדוק איחוד או מחזור הלוואות בריבית נמוכה יותר, ולא לקחת הלוואות חדשות."]);
    if (free < 0) msgs.push(["danger", "אחרי דיור, חובות וחיסכון לא נשאר כסף לשאר ההוצאות. נסו להוריד זמנית את אחוז החיסכון, ובמקביל לחפש איפה לקצץ או להגדיל הכנסה."]);
    else if (left < -1) msgs.push(["danger", "הסכומים שרשמתם גבוהים מההכנסה ב-" + ils(-left) + " בחודש. בלי שינוי, ההפרש יגיע מהמינוס או מהאשראי."]);
    else if (left > 1) msgs.push(["success", "נשארו " + ils(left) + " בחודש שלא שובצו. אפשר להוסיף אותם לחיסכון או לסעיף שחסר בו."]);
    $("msgs").innerHTML = msgs.map(function (m) { return '<div class="callout ' + m[0] + '">' + m[1] + "</div>"; }).join("");
    if (!fromRow) save_url(s);
  }

  function save_url(s) {
    var p = new URLSearchParams({ n: s.inc, h: s.housing, d: s.debts, s: s.savePct, a: s.adults, k: s.kids, c: s.car ? 1 : 0 });
    try { history.replaceState(null, "", "?" + p.toString()); } catch (e) {}
  }
  function load_url() {
    var p = new URLSearchParams(location.search);
    var map = { n: "income", h: "housing", d: "debts", s: "savepct", a: "adults", k: "kids" };
    Object.keys(map).forEach(function (k) { if (p.has(k)) $(map[k]).value = p.get(k); });
    if (p.has("c")) $("car").checked = p.get("c") === "1";
  }

  buildRows();
  load_url();
  ["income", "housing", "debts", "savepct", "adults", "kids", "car"].forEach(function (id) {
    $(id).addEventListener("input", function () { calc(false); });
    $(id).addEventListener("change", function () { calc(false); });
  });
  $("reset").addEventListener("click", function (e) { e.preventDefault(); edited = {}; CATS.forEach(function (c) { $("c-" + c.k).value = ""; }); calc(false); });
  $("share").addEventListener("click", function (e) {
    e.preventDefault();
    var done = function () { $("copied").hidden = false; setTimeout(function () { $("copied").hidden = true; }, 2000); };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
  });
  calc(false);
})();
