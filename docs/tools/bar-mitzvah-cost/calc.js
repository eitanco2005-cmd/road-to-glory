/* מחשבון עלות בר/בת מצווה – client-side (Glory). All numbers are editable estimates. */
(function () {
  "use strict";
  var f = document.getElementById("bm-form");
  if (!f) return;
  var TYPES = {
    evening: { plate: 280, label: "אירוע ערב באולם" },
    lunch: { plate: 190, label: "אירוע צהריים / מסעדה" },
    kiddush: { plate: 75, label: "קידוש ומסיבה קטנה" }
  };
  function ils(n) { return "₪" + Math.round(n).toLocaleString("he-IL"); }
  function num(el) { var v = parseFloat(el.value); return isNaN(v) ? 0 : Math.max(0, v); }

  var lastType = null;
  function calc() {
    var type = f.querySelector('[name="type"]:checked').value;
    var plateEl = f.elements.plate;
    if (type !== lastType) { plateEl.value = TYPES[type].plate; lastType = type; }
    var isBat = f.querySelector('[name="who"]:checked').value === "bat";
    var tef = document.getElementById("row-tefillin");
    tef.hidden = isBat;
    var adults = num(f.elements.adults), kids = num(f.elements.kids);
    var plate = num(plateEl);
    var food = plate * (adults + kids * 0.6);
    var lines = [{ k: "מנות (" + Math.round(adults) + " מבוגרים + " + Math.round(kids) + " ילדים)", v: food }];
    var extras = 0;
    f.querySelectorAll(".line").forEach(function (row) {
      if (row.hidden) return;
      var cb = row.querySelector('input[type="checkbox"]'), amt = row.querySelector('input[type="number"]');
      amt.disabled = !cb.checked;
      if (cb.checked) { var v = num(amt); extras += v; lines.push({ k: row.dataset.label, v: v }); }
    });
    var sub = food + extras;
    var reservePct = num(f.elements.reserve) / 100;
    var reserve = sub * reservePct;
    if (reserve > 0) lines.push({ k: "רזרבה לבלתי צפוי", v: reserve });
    var total = sub + reserve;
    var heads = adults + kids;
    var gifts = num(f.elements.giftAdult) * adults + num(f.elements.giftKid) * kids;
    var net = total - gifts;

    document.getElementById("r-total").textContent = ils(total);
    document.getElementById("r-per").textContent = heads ? ils(total / heads) : "—";
    document.getElementById("r-gifts").textContent = ils(gifts);
    var netEl = document.getElementById("r-net");
    netEl.textContent = net >= 0 ? ils(net) : "+" + ils(-net);
    document.getElementById("r-net-label").textContent = net >= 0 ? "מהכיס אחרי מתנות (משוער)" : "עודף משוער אחרי מתנות";
    var max = lines.reduce(function (m, l) { return Math.max(m, l.v); }, 1);
    document.getElementById("r-lines").innerHTML = lines.map(function (l) {
      return '<li><span class="lk">' + l.k + '</span><span class="lb"><span style="width:' + Math.max(2, l.v / max * 100) +
        '%"></span></span><span class="lv num">' + ils(l.v) + "</span></li>";
    }).join("");
  }
  f.addEventListener("input", calc);
  f.addEventListener("change", calc);
  f.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
  calc();
})();
