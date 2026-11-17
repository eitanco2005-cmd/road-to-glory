/* 50/30/20 budget calculator (client-side only, nothing is sent anywhere). */
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var fmt = new Intl.NumberFormat("he-IL", { maximumFractionDigits: 0 });
  var ils = function (n) { return "₪" + fmt.format(Math.round(n)); };
  var MODELS = { "50-30-20": [0.5, 0.3, 0.2], "60-20-20": [0.6, 0.2, 0.2], "70-20-10": [0.7, 0.2, 0.1] };
  var NAMES = ["צרכים", "רצונות", "חיסכון וחובות"];

  function num(id) {
    var v = parseFloat(String($(id).value).replace(/[^\d.]/g, ""));
    return isFinite(v) && v > 0 ? v : 0;
  }
  function model() {
    var r = document.querySelector('input[name="model"]:checked');
    return r ? r.value : "50-30-20";
  }
  function bar(label, actual, target) {
    var ratio = target > 0 ? actual / target : 0;
    var cls = "meter" + (ratio > 1.1 ? " danger" : ratio > 1 ? " warn" : "");
    var w = Math.min(100, Math.round(ratio * 100));
    var diff = actual - target;
    var txt = Math.abs(diff) < 1 ? "בדיוק ביעד" : (diff > 0 ? ils(diff) + " מעל היעד" : ils(-diff) + " מתחת ליעד");
    return '<div class="w3-row"><strong>' + label + '</strong><span>' + ils(actual) + " מתוך " + ils(target) + " · " + txt + "</span></div>" +
      '<div class="' + cls + '" role="img" aria-label="' + label + ": " + Math.round(ratio * 100) + '% מהיעד"><span style="width:' + w + '%"></span></div>';
  }

  function calc() {
    var inc = num("income");
    var m = model();
    var p = MODELS[m];
    if (!inc) { $("out").hidden = true; $("empty").hidden = false; return; }
    $("out").hidden = false; $("empty").hidden = true;
    var a = [inc * p[0], inc * p[1], inc * p[2]];
    ["n", "w", "s"].forEach(function (k, i) {
      $("v" + k).textContent = ils(a[i]);
      $("p" + k).textContent = "(" + Math.round(p[i] * 100) + "%)";
      $("y" + k).textContent = ils(a[i] * 12) + " בשנה";
    });
    $("ef").textContent = ils(a[0] * 3) + " – " + ils(a[0] * 6);
    var months = Math.ceil((a[0] * 3) / a[2]);
    $("efm").textContent = "אם כל סכום החיסכון החודשי (" + ils(a[2]) + ") יופנה לקרן חירום, תגיעו ל-3 חודשי צרכים בתוך כ-" + months + " חודשים.";

    var needs = num("needs"), wants = num("wants"), saves = num("saves"), housing = num("housing");
    var any = needs || wants || saves || housing;
    $("cmp").hidden = !any;
    if (any) {
      var html = "";
      if (needs) html += bar(NAMES[0], needs, a[0]);
      if (wants) html += bar(NAMES[1], wants, a[1]);
      if (saves) html += bar(NAMES[2], saves, a[2]);
      $("bars").innerHTML = html;
      var msgs = [];
      var spent = needs + wants + saves;
      if (spent > inc * 1.001) msgs.push("סך ההוצאות שרשמתם (" + ils(spent) + ") גבוה מההכנסה. ההפרש מגיע כנראה ממינוס או מאשראי. זה המקום הראשון לטפל בו.");
      if (housing) {
        var hp = housing / inc;
        msgs.push("הדיור לוקח " + Math.round(hp * 100) + "% מההכנסה." + (hp > 0.35 && m === "50-30-20" ? " זה גבוה, ולכן שיטת 60/20/20 תהיה יעד מציאותי יותר." : ""));
      }
      if (wants && wants > a[1]) msgs.push("הכי קל להתחיל מהרצונות: קיצוץ של " + ils(Math.min(wants - a[1], wants * 0.15)) + " בחודש הוא צעד ראשון סביר.");
      if (saves && saves < a[2]) msgs.push("כדי להגיע ליעד החיסכון חסרים " + ils(a[2] - saves) + " בחודש. נסו להעביר סכום קבוע לחיסכון ביום המשכורת, לפני שמתחילים להוציא.");
      $("cmpmsg").textContent = msgs.join(" ");
    }
    try {
      var q = new URLSearchParams();
      q.set("income", Math.round(inc));
      if (m !== "50-30-20") q.set("model", m);
      history.replaceState(null, "", "?" + q.toString());
    } catch (e) { /* ignore */ }
  }

  function init() {
    var q = new URLSearchParams(location.search);
    if (q.get("income")) $("income").value = q.get("income");
    if (q.get("model") && MODELS[q.get("model")]) {
      var r = document.querySelector('input[name="model"][value="' + q.get("model") + '"]');
      if (r) r.checked = true;
    }
    $("calc").addEventListener("input", calc);
    $("calc").addEventListener("change", calc);
    $("share").addEventListener("click", function (e) {
      e.preventDefault();
      var done = function () { $("copied").hidden = false; setTimeout(function () { $("copied").hidden = true; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
    });
    calc();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
