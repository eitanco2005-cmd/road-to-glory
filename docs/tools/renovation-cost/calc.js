/* Renovation cost estimator (client-side only). Price ranges: see sources on the page (Israeli price guides, 2026). */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var fmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 0 });
  var round = function (n) { return n >= 10000 ? Math.round(n / 500) * 500 : Math.round(n / 100) * 100; };
  var ils = function (n) { return "₪" + fmt.format(round(n)); };
  // portion of each [low, high] range used by finish level: basic / standard / high
  var LEVEL = [[0, 0.4], [0.3, 0.7], [0.6, 1]];
  var KITCHEN = [[15000, 22000], [25000, 40000], [45000, 70000]];
  var KITCHEN_INSTALL = [2500, 5000];

  function pick(lo, hi, lvl) {
    var d = hi - lo, p = LEVEL[lvl];
    return [lo + d * p[0], lo + d * p[1]];
  }
  function num(id, def) {
    var v = parseFloat($(id).value);
    return isFinite(v) && v > 0 ? v : def;
  }

  function calc() {
    var area = Math.min(400, Math.max(20, num("area", 85)));
    var lvlEl = document.querySelector('input[name="level"]:checked');
    var lvl = lvlEl ? +lvlEl.value : 1;
    var cont = parseFloat($("cont").value) || 0.15;
    var on = {};
    document.querySelectorAll('input[name="w"]').forEach(function (c) { on[c.value] = c.checked; });
    var scale = Math.min(2, Math.max(0.6, area / 90));
    var items = [];
    if (on.floor) items.push(["ריצוף (" + area + " מ\"ר)", pick(180 * area, 350 * area, lvl)]);
    if (on.paint) items.push(["צבע כולל תקרות", pick(45 * area, 70 * area, lvl)]);
    if (on.elec) items.push(["החלפת תשתית חשמל", pick(18000 * scale, 45000 * scale, lvl)]);
    if (on.plumb) items.push(["החלפת אינסטלציה", pick(15000 * scale, 35000 * scale, lvl)]);
    if (on.kitchen) {
      var k = KITCHEN[lvl];
      items.push(["מטבח " + ["בסיסי", "סטנדרטי", "פרימיום"][lvl] + " כולל התקנה", [k[0] + KITCHEN_INSTALL[0], k[1] + KITCHEN_INSTALL[1]]]);
    }
    var baths = +$("baths").value || 0;
    if (baths) {
      var b = pick(35000, 75000, lvl);
      items.push([baths === 1 ? "חדר רחצה קומפלט" : baths + " חדרי רחצה קומפלט", [b[0] * baths, b[1] * baths]]);
    }
    if (on.ac) items.push(["מזגן מיני מרכזי", pick(15000, 40000, lvl)]);
    var extra = num("extra", 0);
    if (extra) items.push(["עבודות נוספות (ההערכה שלכם)", [extra, extra]]);

    var lo = 0, hi = 0, rows = "";
    items.forEach(function (it) {
      lo += it[1][0]; hi += it[1][1];
      var r = it[1][0] === it[1][1] ? ils(it[1][0]) : ils(it[1][0]) + " – " + ils(it[1][1]);
      rows += "<tr><td>" + it[0] + '</td><td class="num">' + r + "</td></tr>";
    });
    if (!items.length) {
      $("rows").innerHTML = '<tr><td colspan="2">בחרו לפחות עבודה אחת.</td></tr>';
      $("total").textContent = "–"; $("sub").textContent = ""; $("bench").textContent = "";
      return;
    }
    rows += "<tr><td>בלת\"מ " + Math.round(cont * 100) + '%</td><td class="num">' + ils(lo * cont) + " – " + ils(hi * cont) + "</td></tr>";
    rows += '<tr><th>סה"כ</th><th class="num">' + ils(lo * (1 + cont)) + " – " + ils(hi * (1 + cont)) + "</th></tr>";
    $("rows").innerHTML = rows;
    $("total").textContent = ils(lo * (1 + cont)) + " – " + ils(hi * (1 + cont));
    $("sub").textContent = "בלי בלת\"מ: " + ils(lo) + " – " + ils(hi) + " · כ-" + ils(lo * (1 + cont) / area) + " עד " + ils(hi * (1 + cont) / area) + " למ\"ר";
    $("bench").textContent = "להשוואה: שיפוץ מלא של דירת 3 חדרים (כ-75 מ\"ר) מוערך ב-120,000–200,000 ₪, כלומר כ-1,600–2,700 ₪ למ\"ר. האומדן כולל רק את העבודות שבחרתם.";
    try {
      var q = new URLSearchParams();
      q.set("area", area); q.set("level", lvl);
      history.replaceState(null, "", "?" + q.toString());
    } catch (e) { /* ignore */ }
  }

  function init() {
    var q = new URLSearchParams(location.search);
    if (q.get("area")) $("area").value = q.get("area");
    if (q.get("level") && /^[012]$/.test(q.get("level"))) {
      var r = document.querySelector('input[name="level"][value="' + q.get("level") + '"]');
      if (r) r.checked = true;
    }
    $("calc").addEventListener("input", calc);
    $("calc").addEventListener("change", calc);
    calc();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
