/* מחשבון עלות חתונה (תכנון פלוס) – client-side only, no data leaves the browser.
 * Plate price model is shared with tools/wedding-gift/calc.js (same base prices and factors), so the cost a couple
 * plans with and the gift a guest is told to give agree with each other. */
(function () {
  "use strict";
  var f = document.getElementById("cost-form");
  if (!f) return;

  // Mid-points of the 2026 per-plate ranges reported for Tel Aviv, center & Sharon (summer 420–550, winter 340–430).
  var PLATE = { summer: 480, winter: 385 };
  var REGION = { center: 1, jerusalem: 0.95, other: 0.85 };       // Jerusalem ~95%, north/south ~85% of center (Bizportal calculator)
  var DAY = { weekday: 1, thursday: 1.12, friday: 0.82 };          // Thursday +15–25% reported; Friday noon = our estimate
  var VENUE = { regular: 1, luxury: 1.25, modest: 0.75 };
  var KID = 0.6;                                                   // many venues charge ~50–70% for a child's meal
  var SPREAD = 0.12;                                               // ± range around the plate estimate
  // vendor lines: [key, label, low, mid, high, on by default]
  var LINES = [
    ["photo", "צילום סטילס + וידאו", 6500, 10000, 16000, true],
    ["dj", "DJ והגברה", 4000, 7000, 12000, true],
    ["dress", "שמלת כלה", 2500, 8000, 18000, true],
    ["suit", "חליפה ונעליים לחתן", 1500, 2500, 5000, true],
    ["makeup", "איפור ושיער לכלה", 1500, 3000, 5000, true],
    ["decor", "עיצוב, פרחים וחופה (מעבר למה שכלול)", 2000, 6000, 15000, true],
    ["rings", "טבעות נישואין", 2000, 5000, 12000, true],
    ["rabbi", "רב, רבנות וכתובה", 1500, 2500, 4000, true],
    ["invite", "הזמנות, אישורי הגעה ומגנטים", 1000, 3000, 7000, true],
    ["bar", "בר אלכוהול (אם לא כלול במנה)", 3000, 6000, 12000, false],
    ["transport", "רכב / הסעות לאורחים", 1500, 3000, 6000, false]
  ];
  var TIER = { save: 2, mid: 3, premium: 4 };

  function val(name) {
    var el = f.querySelector('[name="' + name + '"]:checked') || f.elements[name];
    return el ? el.value : null;
  }
  function n(name, d) { var v = parseFloat(f.elements[name].value); return isFinite(v) && v >= 0 ? v : d; }
  function r100(x) { return Math.round(x / 100) * 100; }
  function r1000(x) { return Math.round(x / 1000) * 1000; }
  function ils(x) { return "₪" + Math.round(x).toLocaleString("he-IL"); }
  function $(id) { return document.getElementById(id); }

  function calc() {
    var guests = Math.max(0, Math.min(2000, Math.round(n("guests", 0))));
    var kids = Math.max(0, Math.min(500, Math.round(n("kids", 0))));
    var autoPlate = PLATE[val("season")] * REGION[val("region")] * DAY[val("day")] * VENUE[val("venue")];
    var plateIn = parseFloat(f.elements.plate.value);
    var custom = isFinite(plateIn) && plateIn > 50;
    var plate = custom ? plateIn : autoPlate;
    f.elements.plate.placeholder = String(Math.round(autoPlate / 10) * 10);
    var heads = guests + kids * KID;
    var food = plate * heads;
    var foodLo = custom ? food : food * (1 - SPREAD), foodHi = custom ? food : food * (1 + SPREAD);

    var t = TIER[val("tier")] || 3;
    var vend = 0, vendLo = 0, vendHi = 0, rows = [["אולם / גן ומנות", food]];
    LINES.forEach(function (L) {
      var on = f.elements["use_" + L[0]].checked;
      var input = f.elements["amt_" + L[0]];
      input.placeholder = String(L[t]);
      input.disabled = !on;
      if (!on) return;
      var typed = parseFloat(input.value);
      var amt = isFinite(typed) && typed >= 0 && input.value !== "" ? typed : L[t];
      vend += amt;
      vendLo += input.value !== "" ? amt : L[2];
      vendHi += input.value !== "" ? amt : L[4];
      rows.push([L[1], amt]);
    });
    var reserve = Math.min(30, n("reserve", 0)) / 100;
    var total = (food + vend) * (1 + reserve);
    var lo = (foodLo + vendLo) * (1 + reserve), hi = (foodHi + vendHi) * (1 + reserve);
    if (reserve) rows.push(["רזרבה לבלת\"מ (" + Math.round(reserve * 100) + "%)", (food + vend) * reserve]);

    var giftIn = parseFloat(f.elements.gift.value);
    var giftAuto = Math.round(plate * 0.85 / 10) * 10;            // average gift per adult guest ≈ 85% of a plate (see page)
    f.elements.gift.placeholder = String(giftAuto);
    var gift = isFinite(giftIn) && giftIn >= 0 && f.elements.gift.value !== "" ? giftIn : giftAuto;
    var gifts = gift * guests;
    var net = total - gifts;

    $("r-total").textContent = ils(r1000(total));
    $("r-range").textContent = ils(r1000(lo)) + " – " + ils(r1000(hi));
    $("r-plate").textContent = ils(plate) + (custom ? " (שהזנתם)" : " (משוער)");
    $("r-per").textContent = guests ? ils(total / guests) : "—";
    $("r-gifts").textContent = ils(r1000(gifts));
    $("r-net").textContent = net >= 0 ? ils(r1000(net)) : "+" + ils(r1000(-net)) + " עודף";
    $("r-net-label").textContent = net >= 0 ? "מהכיס אחרי מתנות (הערכה)" : "המתנות צפויות לכסות הכל";
    $("r-venue-share").textContent = total ? Math.round(food / total * 100) + "%" : "—";

    var max = rows.reduce(function (m, r) { return Math.max(m, r[1]); }, 1);
    $("r-lines").innerHTML = rows.map(function (r) {
      return "<li><span>" + r[0] + '</span><span class="lb" aria-hidden="true"><span style="width:' + Math.max(2, Math.round(r[1] / max * 100)) + '%"></span></span><span class="num">' + ils(r100(r[1])) + "</span></li>";
    }).join("");

    var warn = [];
    if (guests && guests < 180 && val("venue") !== "modest") warn.push("באולמות וגנים רבים יש התחייבות למינימום מנות (לרוב 200–300 בעונה). עם " + guests + " מוזמנים כדאי לבדוק את המינימום, או לשקול מקום בוטיק / מסעדה.");
    if (val("day") === "thursday") warn.push("יום חמישי הוא הערב היקר בשבוע: המעבר לראשון–רביעי חוסך כאן כ-" + ils(r1000(food - food / DAY.thursday)) + ".");
    if (val("season") === "summer" && !custom) warn.push("אותה חתונה בחורף (נובמבר–מרץ) יוצאת בערך " + ils(r1000(food - food * PLATE.winter / PLATE.summer)) + " פחות על המנות בלבד.");
    $("r-tips").innerHTML = warn.map(function (w) { return "<li>" + w + "</li>"; }).join("");
    $("r-tips").hidden = !warn.length;
  }

  f.addEventListener("input", calc);
  f.addEventListener("change", calc);
  f.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
  calc();
  window.WeddingCost = { calc: calc };
})();
