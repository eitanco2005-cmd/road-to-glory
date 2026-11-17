/* כמה לשים בחתונה – client-side calculator (תכנון פלוס). No data leaves the browser. */
(function () {
  "use strict";
  var f = document.getElementById("gift-form");
  if (!f) return;

  // Price per plate, mid-points of the 2026 ranges reported for Tel Aviv & center (summer 420–550, winter 340–430).
  var PLATE = { summer: 480, winter: 385 };
  var REGION = { center: 1, other: 0.9 };            // other regions reported ~10% cheaper
  var DAY = { weekday: 1, thursday: 1.12, friday: 0.82 }; // Thursday premium reported ~40–70 ₪; Friday noon = our estimate
  var VENUE = { regular: 1, luxury: 1.25, modest: 0.75 };
  // Share of the plate price a guest typically covers, by closeness (our calibration, see the page text)
  var CLOSE = {
    acquaintance: { f: 0.65, label: "מכר/ה" },
    work: { f: 0.75, label: "חבר/ה מהעבודה" },
    friend: { f: 0.85, label: "חבר/ה" },
    close: { f: 1.15, label: "חבר/ה קרוב/ה" },
    family: { f: 1.3, label: "משפחה מורחבת (בני דודים)" },
    nuclear: { f: 2.0, label: "משפחה קרובה (אחים, דודים)" }
  };

  function val(name) {
    var el = f.querySelector('[name="' + name + '"]:checked') || f.elements[name];
    return el ? el.value : null;
  }
  function round(n, step) { return Math.max(step, Math.round(n / step) * step); }
  function ils(n) { return "₪" + Math.round(n).toLocaleString("he-IL"); }

  function plate() {
    var custom = parseFloat(f.elements.plate.value);
    if (custom > 50) return { v: custom, custom: true };
    var p = PLATE[val("season")] * REGION[val("region")] * DAY[val("day")] * VENUE[val("venue")];
    return { v: p, custom: false };
  }

  function amountFor(closeKey, p, adults, kids, attending) {
    var perAdult = p * CLOSE[closeKey].f;
    var people = adults === 1 ? 1 : adults * 0.9;      // couples usually give a bit less than double
    var total = perAdult * people + perAdult * 0.5 * kids;
    if (!attending) total = perAdult * (adults === 1 ? 0.55 : 0.5 * adults); // not coming: no plate to cover
    return total;
  }

  function calc() {
    var p = plate();
    var adults = parseInt(val("adults"), 10) || 1;
    var kids = Math.max(0, Math.min(10, parseInt(f.elements.kids.value, 10) || 0));
    var attending = val("attend") === "yes";
    var chai = f.elements.chai.checked;
    var closeKey = val("closeness");
    var raw = amountFor(closeKey, p.v, adults, kids, attending);
    var step = 50;
    var rec = round(raw, step), lo = round(raw * 0.85, step), hi = round(raw * 1.15, step);
    if (chai) { rec = round(raw, 18); lo = round(raw * 0.85, 18); hi = round(raw * 1.15, 18); }

    document.getElementById("r-amount").textContent = ils(rec);
    document.getElementById("r-range").textContent = ils(lo) + " – " + ils(hi);
    var heads = attending ? adults + kids : 0;
    var cover = p.v * (adults + kids * 0.5);
    document.getElementById("r-plate").textContent = (p.custom ? "מחיר שהזנתם: " : "מחיר מנה משוער: ") + ils(p.v) + " לאדם";
    var note = "";
    if (attending) {
      var ratio = rec / cover;
      note = ratio >= 1 ? "הסכום מכסה את עלות המנות שלכם (" + ils(cover) + ")." :
        "הסכום מכסה כ-" + Math.round(ratio * 100) + "% מעלות המנות שלכם (" + ils(cover) + ") – מקובל למכרים רחוקים.";
    } else {
      note = "כשלא מגיעים אין מנה לכסות, ולכן הסכום נמוך יותר.";
    }
    document.getElementById("r-note").textContent = note;

    // table of all closeness levels for the same settings
    var rows = "";
    Object.keys(CLOSE).forEach(function (k) {
      var a = amountFor(k, p.v, adults, kids, attending);
      var r = chai ? round(a, 18) : round(a, 50);
      rows += "<tr" + (k === closeKey ? ' class="sel"' : "") + "><td>" + CLOSE[k].label + "</td><td class=\"num\">" + ils(r) + "</td></tr>";
    });
    document.getElementById("r-table").innerHTML = rows;
    var who = adults === 1 ? "מגיע/ה לבד" : (adults === 2 ? "זוג" : adults + " מבוגרים");
    if (kids) who += " + " + kids + " ילדים";
    if (!attending) who = "לא מגיעים";
    document.getElementById("r-who").textContent = who;
  }

  f.addEventListener("input", calc);
  f.addEventListener("change", calc);
  f.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
  calc();
})();
