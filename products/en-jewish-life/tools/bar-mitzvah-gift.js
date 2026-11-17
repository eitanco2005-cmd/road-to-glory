(function () {
  "use strict";
  // Base single-giver amount and common range, by relationship (US norms; see sources on the page)
  var BASE = { teen: [36, 18, 54], acq: [54, 36, 72], friend: [72, 54, 108], close: [108, 72, 180],
               relative: [144, 108, 360], family: [360, 180, 1000] };
  var WHO = { "1": 1, "2": 1.6, "3": 2 };
  var ATT = { party: 1, service: 0.85, no: 0.75 };
  var LABEL = { teen: "a classmate or teen friend", acq: "an acquaintance or coworker", friend: "a friend of the family",
                close: "a close friend", relative: "a relative", family: "a grandparent or very close family" };
  var WHOL = { "1": "from you", "2": "from a couple", "3": "from your family" };
  var form = document.getElementById("gift-form");
  function val(n) { var c = form.querySelector('input[name="' + n + '"]:checked'); return c ? c.value : null; }
  function chai(x) { return Math.max(18, Math.round(x / 18) * 18); }
  function fmt(n) { return "$" + n.toLocaleString("en-US"); }
  function calc() {
    var rel = val("rel"), who = val("who"), att = val("att"), area = Number(val("area"));
    var b = BASE[rel], k = WHO[who] * ATT[att] * area;
    if (rel === "teen") k = ATT[att] * area; // teens give individually
    var amt = chai(b[0] * k), lo = chai(b[1] * k), hi = chai(b[2] * k);
    if (lo > amt) lo = amt; if (hi < amt) hi = amt;
    document.getElementById("amount").textContent = fmt(amt);
    document.getElementById("explain").textContent = "That's " + (amt / 18) + " × chai, " + WHOL[who] + " as " + LABEL[rel] +
      (att === "no" ? ", not attending." : att === "service" ? ", attending the service." : ", attending the celebration.");
    document.getElementById("range").textContent = "Common range for this situation: " + fmt(lo) + "–" + fmt(hi) +
      (rel === "family" ? " (grandparents often give far more, or a savings or Israel Bonds gift)." : ".") +
      " Round to whatever multiple of 18 feels right.";
    var rows = document.querySelectorAll("#chai-table tbody tr");
    for (var i = 0; i < rows.length; i++) {
      var v = Number(rows[i].getAttribute("data-v"));
      rows[i].style.background = (v === amt || (v === 540 && amt >= 540)) ? "var(--primary-soft)" : "";
      rows[i].style.fontWeight = (v === amt || (v === 540 && amt >= 540)) ? "700" : "";
    }
  }
  form.addEventListener("change", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  calc();
})();
