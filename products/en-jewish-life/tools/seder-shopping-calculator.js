(function () {
  "use strict";
  // [item, category, per adult, per child, per plate (per seder), unit, units per pack, pack label, example price]
  var SHOP = __SHOP__;
  var $ = function (id) { return document.getElementById(id); };
  var form = $("seder");
  function num(id) { var n = Number($(id).value); return isFinite(n) && n > 0 ? n : 0; }
  function radio(n) { return form.querySelector('input[name="' + n + '"]:checked').value; }
  function nice(x) { return x >= 10 ? String(Math.round(x)) : String(Math.round(x * 10) / 10); }
  function calc() {
    var a = num("adults"), k = num("kids"), s = Number($("seders").value), p = Math.max(1, num("plates"));
    var shm = radio("shmurah") === "1", meal = radio("meal") === "1";
    var A = a * s, K = k * s, P = p * s;
    var tb = document.querySelector("#list tbody"); tb.innerHTML = "";
    var out = {};
    var cat = "";
    SHOP.forEach(function (r) {
      var item = r[0], c = r[1], need;
      if (!meal && (c === "Meal" || c === "Dessert")) return;
      if (item.indexOf("Haggadot") === 0) need = a + k;
      else need = r[2] * A + r[3] * K + r[4] * P;
      if (!shm && item.indexOf("shmurah") >= 0) return;
      if (!shm && item.indexOf("machine") >= 0) need += 2 * A + 1.5 * K + 3 * P; // machine matzah covers the mitzvah too
      if (need <= 0) return;
      var packs = Math.ceil(need / (r[6] || 1) - 1e-9);
      out[item] = need;
      if (c !== cat) {
        cat = c;
        var h = document.createElement("tr");
        h.innerHTML = '<th colspan="3" scope="colgroup">' + c + "</th>";
        tb.appendChild(h);
      }
      var tr = document.createElement("tr");
      tr.innerHTML = "<td>" + item + '</td><td class="num">' + nice(need) + " " + r[5] + "</td><td>" +
        (r[6] > 1 || /lb|oz|bottle|box|can|bag|pack|jar|dozen/.test(r[7]) ? packs + " × " + r[7] : "") + "</td>";
      tb.appendChild(tr);
    });
    $("k-seats").textContent = A + K;
    $("k-matzah").textContent = nice(shm ? out["Matzah: shmurah, handmade (for the mitzvah)"] || 0 : 2 * A + 1.5 * K + 3 * P);
    $("k-wine").textContent = Math.ceil(out["Wine (four cups)"] || 0);
    $("k-juice").textContent = Math.ceil(out["Grape juice (four cups)"] || 0);
  }
  form.addEventListener("input", calc);
  form.addEventListener("change", calc);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  $("print").addEventListener("click", function () { window.print(); });
  calc();
})();
