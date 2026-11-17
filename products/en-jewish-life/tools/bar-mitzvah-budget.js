(function () {
  "use strict";
  // Starting assumptions (USD). Clearly labelled on the page as estimates to replace with quotes.
  var AREA = { low: 0.8, avg: 1, high: 1.35 };
  var PARTY_PP = { low: 70, avg: 95, high: 135 };
  var KIDDUSH_PP = { low: 18, avg: 25, high: 35 };
  var VENUE = { low: 1200, avg: 2500, high: 5000 };
  var $ = function (id) { return document.getElementById(id); };
  var form = $("bud");
  function radio(n) { return form.querySelector('input[name="' + n + '"]:checked').value; }
  function num(id, dflt) { var v = $(id).value.trim(); var n = Number(v); return v === "" || !isFinite(n) || n < 0 ? dflt : n; }
  function usd(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function calc() {
    var a = num("adults", 0), k = num("kids", 0), g = a + k, style = radio("style"), area = radio("area"), f = AREA[area];
    var party = style !== "kiddush", kid = style !== "party";
    $("pp").placeholder = PARTY_PP[area]; $("kpp").placeholder = KIDDUSH_PP[area]; $("venue").placeholder = party ? VENUE[area] : 0;
    var pp = num("pp", PARTY_PP[area]), kpp = num("kpp", KIDDUSH_PP[area]);
    var rows = [];
    if (party) {
      rows.push(["Party catering & bar", a * pp + k * pp * 0.45]);
      rows.push(["Venue rental", num("venue", VENUE[area])]);
      rows.push(["Music & entertainment", Number($("ent").value) * f]);
      rows.push(["Décor, flowers & centerpieces", Number($("decor").value) * g * f]);
      rows.push(["Extras (photo booth, games)", Number($("extras").value) * f]);
      rows.push(["Favors / swag", 8 * k]);
    }
    if (kid) rows.push(["Kiddush luncheon", g * kpp]);
    if (!party) rows.push(["Kiddush décor & flowers", Math.min(Number($("decor").value), 10) * g * f]);
    rows.push(["Photo & video", Number($("photo").value) * f * (party ? 1 : 0.5)]);
    rows.push(["Invitations & postage", Math.ceil(g / 2.5) * 4]);
    rows.push(["Clothing (family)", num("attire", 700)]);
    rows.push(["Tutor & synagogue fees", num("tutor", 1500)]);
    var sub = rows.reduce(function (s, r) { return s + r[1]; }, 0);
    rows.push(["Contingency (" + num("cont", 10) + "%)", sub * num("cont", 10) / 100]);
    var total = rows.reduce(function (s, r) { return s + r[1]; }, 0);
    $("total").textContent = usd(total);
    $("perguest").textContent = g ? "About " + usd(total / g) + " per guest (" + g + " guests). Range to plan for: " + usd(total * 0.85) + "–" + usd(total * 1.2) + "." : "Enter your guest count.";
    var tb = document.querySelector("#breakdown tbody"); tb.innerHTML = "";
    rows.sort(function (x, y) { return y[1] - x[1]; }).forEach(function (r) {
      if (r[1] <= 0) return;
      var pct = total ? r[1] / total * 100 : 0;
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + r[0] + '</td><td class="num">' + usd(r[1]) + '</td><td style="min-width:90px"><div class="meter" aria-hidden="true"><span style="width:' +
        pct.toFixed(1) + '%"></span></div><span class="sr-only">' + pct.toFixed(0) + "%</span></td>";
      tb.appendChild(tr);
    });
  }
  form.addEventListener("input", calc);
  form.addEventListener("change", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  calc();
})();
