/* Savings goal calculator (client-side only, nothing is sent anywhere). */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var fmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 0 });
  var ils = function (n) { return "₪" + fmt.format(Math.round(n)); };
  var MONTHS = ["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"];
  function num(id) { var v = parseFloat(String($(id).value).replace(/[^\d.]/g, "")); return isFinite(v) && v > 0 ? v : 0; }
  function mode() { var r = document.querySelector('input[name="mode"]:checked'); return r ? r.value : "date"; }
  function when(n) { var d = new Date(); d.setDate(1); d.setMonth(d.getMonth() + n); return MONTHS[d.getMonth()] + " " + d.getFullYear(); }
  function fv(pv, pmt, r, n) { if (!r) return pv + pmt * n; var g = Math.pow(1 + r, n); return pv * g + pmt * (g - 1) / r; }

  function calc() {
    var m = mode();
    $("f-months").hidden = m !== "date"; $("f-pmt").hidden = m !== "pmt";
    var T = num("target"), PV = num("current"), a = num("rate") / 100, r = a ? Math.pow(1 + a, 1 / 12) - 1 : 0;
    if (!T) { $("out").hidden = true; $("empty").hidden = false; return; }
    $("out").hidden = false; $("empty").hidden = true;
    var n, pmt, msg = "";
    if (PV >= T) {
      n = 0; pmt = 0;
      $("big-l").textContent = "כבר הגעתם ליעד"; $("big").textContent = "✓";
      $("sub").textContent = "החיסכון הנוכחי (" + ils(PV) + ") כבר מכסה את היעד.";
      $("tbl").innerHTML = ""; $("k-dep").textContent = ils(0); $("k-int").textContent = ils(0); $("k-end").textContent = ils(PV); $("k-date").textContent = "היום";
      save(); return;
    }
    if (m === "date") {
      n = Math.max(1, Math.round(num("months") || 12));
      var g = Math.pow(1 + r, n);
      pmt = r ? (T - PV * g) * r / (g - 1) : (T - PV) / n;
      pmt = Math.max(0, pmt);
      $("big-l").textContent = "צריך לחסוך בכל חודש";
      $("big").textContent = ils(Math.ceil(pmt));
      $("sub").textContent = "במשך " + n + " חודשים, עד " + when(n) + ".";
    } else {
      pmt = num("pmt");
      if (!pmt && !r) { $("big-l").textContent = "רשמו סכום חודשי"; $("big").textContent = "—"; $("sub").textContent = ""; $("tbl").innerHTML = ""; return; }
      n = 0; var bal = PV;
      while (bal < T && n < 1200) { bal = bal * (1 + r) + pmt; n++; }
      if (n >= 1200) { $("big-l").textContent = "בקצב הזה היעד רחוק מאוד"; $("big").textContent = "100+ שנים"; $("sub").textContent = "נסו להגדיל את הסכום החודשי."; $("tbl").innerHTML = ""; return; }
      $("big-l").textContent = "תגיעו ליעד בעוד";
      var y = Math.floor(n / 12), mm = n % 12;
      $("big").textContent = (y ? y + (y === 1 ? " שנה" : " שנים") : "") + (y && mm ? " ו-" : "") + (mm ? mm + (mm === 1 ? " חודש" : " חודשים") : "");
      $("sub").textContent = "בערך ב" + when(n) + ", אם תפקידו " + ils(pmt) + " בכל חודש.";
    }
    var end = fv(PV, pmt, r, n), deposits = pmt * n;
    $("k-dep").textContent = ils(deposits);
    $("k-int").textContent = ils(Math.max(0, end - PV - deposits));
    $("k-end").textContent = ils(end);
    $("k-date").textContent = when(n);
    // yearly table
    var rows = "", bal2 = PV, dep = PV;
    for (var i = 1; i <= n; i++) {
      bal2 = bal2 * (1 + r) + pmt; dep += pmt;
      if (i % 12 === 0 || i === n) rows += "<tr><td>" + (i % 12 === 0 ? "סוף שנה " + (i / 12) : "חודש " + i) + "</td><td class=\"num\">" + ils(dep) + "</td><td class=\"num\">" + ils(bal2 - dep) + "</td><td class=\"num\">" + ils(bal2) + "</td></tr>";
    }
    $("tbl").innerHTML = rows;
    var tips = [];
    if (r && n <= 24) tips.push("ליעד של פחות משנתיים, התשואה משנה מעט. מה שקובע הוא הסכום החודשי והעקביות.");
    if (a > 0.06) tips.push("הנחת תשואה של " + Math.round(a * 1000) / 10 + "% בשנה היא אופטימית לחיסכון בטוח. תשואה כזו אפשרית רק עם סיכון, וזה לא מתאים לכסף שתצטרכו בקרוב.");
    if (m === "date" && pmt > 0) tips.push("טיפ: הגדירו הוראת קבע של " + ils(Math.ceil(pmt / 50) * 50) + " ליום שאחרי המשכורת, כדי שהחיסכון יקרה לפני שהכסף מתפזר.");
    $("tips").innerHTML = tips.map(function (t) { return "<li>" + t + "</li>"; }).join("");
    save();
  }
  function save() {
    var p = new URLSearchParams({ t: num("target"), c: num("current"), r: $("rate").value, m: mode(), n: num("months"), p: num("pmt") });
    try { history.replaceState(null, "", "?" + p.toString()); } catch (e) {}
  }
  function load() {
    var p = new URLSearchParams(location.search), map = { t: "target", c: "current", r: "rate", n: "months", p: "pmt" };
    Object.keys(map).forEach(function (k) { if (p.has(k) && p.get(k) !== "0") $(map[k]).value = p.get(k); });
    if (p.get("m") === "pmt") $("m-pmt").checked = true;
  }
  document.querySelectorAll("[data-goal]").forEach(function (b) {
    b.addEventListener("click", function () { $("target").value = b.getAttribute("data-goal"); $("months").value = b.getAttribute("data-months"); $("m-date").checked = true; calc(); });
  });
  load();
  $("calc").addEventListener("input", calc);
  $("calc").addEventListener("change", calc);
  calc();
})();
