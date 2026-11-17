/* תכנון פלוס tip jar ("buy us a coffee") for the free tools.
 *
 * Loaded automatically by site.js on every free tool page (tools/<slug>/). Opt out per page with
 * <html data-tip="off"> (e.g. pay-to-export tools). Optional explicit placement: <div data-tip-jar></div>;
 * otherwise the box is inserted right after the block that holds the tool's first .result.
 *
 * It stays hidden until the visitor actually got a result: after they typed/clicked in the tool and a
 * .result / [aria-live] region is visible with content (or the page was opened with a shared result in the URL).
 * Dismiss (×) hides it for 14 days; after a tip it is not shown again for 90 days.
 * Payment: PayPal via paykit.js, product slug "tip", ₪10 / ₪20 / custom (min ₪5, max ₪500), thank-you inline.
 */
(function () {
  "use strict";
  if (window.__tipJar) return;
  window.__tipJar = true;
  var me = document.currentScript || document.querySelector('script[src*="assets/tip.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var KEY = "tp-tip";
  var MIN = 5, MAX = 500, DAY = 864e5;
  var TEST = new URLSearchParams(location.search).get("test") === "1"; // read now: tools may rewrite the URL later

  function state() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  function suppressed() {
    if (document.documentElement.getAttribute("data-tip") === "off") return true;
    if (TEST) return false; // always testable
    var s = state(), now = Date.now();
    return (s.tipped && now - s.tipped < 90 * DAY) || (s.closed && now - s.closed < 14 * DAY);
  }
  if (suppressed()) return;

  var CSS =
    ".tip-jar{margin-block:1.5rem 0;max-width:640px;margin-inline:auto;border:1px dashed var(--border,#e5ddcf);border-radius:var(--radius,14px);" +
    "background:var(--surface,#fff);padding:1rem 1.15rem;position:relative;opacity:0;transform:translateY(6px);transition:opacity .4s,transform .4s}" +
    ".tip-jar.on{opacity:1;transform:none}" +
    ".tip-jar h2{font-size:1.1rem;margin:0 0 .2rem;padding-inline-end:2rem}" +
    ".tip-jar p{margin:.15rem 0 .6rem;color:var(--muted,#586770);font-size:.95rem}" +
    ".tip-x{position:absolute;inset-block-start:.5rem;inset-inline-end:.5rem;border:0;background:transparent;font-size:1.3rem;line-height:1;" +
    "width:36px;height:36px;border-radius:50%;cursor:pointer;color:var(--muted,#586770)}.tip-x:hover{background:var(--surface-2,#f3efe7)}" +
    ".tip-amts{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}" +
    ".tip-amts button{min-height:42px;padding:.4rem 1rem;border-radius:999px;border:1.5px solid var(--border,#e5ddcf);background:var(--bg,#fbf8f3);" +
    "color:var(--text,#1d2a2e);font:inherit;font-weight:700;cursor:pointer}" +
    ".tip-amts button[aria-pressed=true]{border-color:var(--primary,#0e6b63);background:var(--primary-soft,#e2f1ee);color:var(--primary,#0e6b63)}" +
    ".tip-custom{display:inline-flex;align-items:center;gap:.3rem}.tip-custom input{width:7.5rem;min-height:42px;padding:.3rem .6rem;border-radius:999px;" +
    "border:1.5px solid var(--input-border,#d9c9a8);background:var(--input-bg,#fffaf0);color:var(--text,#1d2a2e);font:inherit}" +
    ".tip-pay{margin-top:.8rem;max-width:360px}.tip-pay[hidden]{display:none}.tip-fine{font-size:.82rem!important;margin:.5rem 0 0!important}" +
    ".tip-thanks{font-weight:700;color:var(--success,#1d7a46);margin:0}";

  var box = null, shown = false, interacted = false;

  function place(el) {
    var slot = document.querySelector("[data-tip-jar]");
    if (slot) { slot.appendChild(el); return true; }
    var main = document.querySelector("main") || document.body;
    var r = main.querySelector(".result, [aria-live]");
    if (!r) return false;
    // climb to the direct child of the nearest .container (the tool's whole block), insert after it
    var n = r;
    while (n.parentElement && n.parentElement !== main && !n.parentElement.classList.contains("container")) n = n.parentElement;
    n.parentNode.insertBefore(el, n.nextSibling);
    return true;
  }

  function hasResult() {
    var list = document.querySelectorAll("main .result, main [aria-live]");
    for (var i = 0; i < list.length; i++) {
      var el = list[i];
      if (el.closest("[hidden]") || el.closest(".tip-jar")) continue;
      if (!(el.offsetWidth || el.offsetHeight)) continue;
      if (/\d/.test(el.textContent || "")) return true; // a result shows numbers; empty-state text has none
    }
    return false;
  }

  function build() {
    var st = document.createElement("style");
    st.textContent = CSS;
    document.head.appendChild(st);
    box = document.createElement("aside");
    box.className = "tip-jar";
    box.setAttribute("aria-label", "תמיכה באתר");
    box.hidden = true;
    box.innerHTML =
      '<button type="button" class="tip-x" aria-label="סגירה">×</button>' +
      "<h2>עזר לכם? אפשר להזמין אותנו לקפה ☕</h2>" +
      "<p>הכלים כאן חינמיים ובלי פרסומות. טיפ קטן עוזר לנו להמשיך לעדכן אותם. לגמרי לא חובה.</p>" +
      '<div class="tip-amts" role="group" aria-label="סכום הטיפ">' +
      '<button type="button" data-amt="10" aria-pressed="false">₪10</button>' +
      '<button type="button" data-amt="20" aria-pressed="false">₪20</button>' +
      '<span class="tip-custom"><label for="tip-amt" class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">סכום אחר בשקלים</label>' +
      '<input id="tip-amt" type="number" inputmode="numeric" min="' + MIN + '" max="' + MAX + '" step="1" placeholder="סכום אחר"></span>' +
      "</div>" +
      '<div class="tip-pay" hidden></div>' +
      '<p class="tip-fine">תשלום מאובטח ב-PayPal או בכרטיס אשראי. טיפ אינו רכישה ואינו מקנה מוצר.</p>';
    if (!place(box)) { box = null; return; }

    var amount = 0, payReady = false;
    var pay = box.querySelector(".tip-pay"), input = box.querySelector("#tip-amt");
    var btns = box.querySelectorAll("[data-amt]");
    function select(v, fromInput) {
      amount = v;
      for (var i = 0; i < btns.length; i++) btns[i].setAttribute("aria-pressed", String(Number(btns[i].getAttribute("data-amt")) === v && !fromInput));
      if (!fromInput) input.value = "";
      if (!payReady && v) {
        payReady = true;
        pay.hidden = false;
        PayKitReady().then(function () {
          window.PayKit.render(pay, {
            amount: function () { return amount; }, currency: "ILS", sku: "tip", name: "טיפ – תכנון פלוס",
            locale: "he_IL", lang: "he", test: TEST, testLabel: "טיפ בדיקה (TEST)",
            validate: function () {
              return amount >= MIN && amount <= MAX ? "" : "אפשר לבחור סכום בין ₪" + MIN + " ל-₪" + MAX + ".";
            },
            onPaid: thanks
          });
        }).catch(function () { pay.textContent = "לא הצלחנו לטעון את התשלום."; });
      }
    }
    for (var i = 0; i < btns.length; i++) btns[i].addEventListener("click", function () { select(Number(this.getAttribute("data-amt")), false); });
    input.addEventListener("input", function () {
      var v = Math.round(Number(input.value) || 0);
      select(v, true);
    });
    box.querySelector(".tip-x").addEventListener("click", function () {
      var s = state(); s.closed = Date.now(); save(s);
      box.remove();
    });
  }

  function thanks(info) {
    var s = state(); s.tipped = Date.now(); save(s);
    box.innerHTML = '<p class="tip-thanks" role="status">תודה רבה! ☕ הטיפ התקבל' + (info.test ? " (בדיקה, ללא חיוב)" : "") +
      ". זה באמת עוזר לנו להמשיך.</p>" + '<p class="tip-fine">אישור התשלום נשלח אליכם במייל מ-PayPal.</p>';
  }

  var pk = null;
  function PayKitReady() {
    if (window.PayKit) return Promise.resolve();
    if (!pk) {
      pk = new Promise(function (res, rej) {
        var s = document.createElement("script");
        s.src = ASSETS + "paykit.js"; s.async = true;
        s.onload = function () { res(); }; s.onerror = function () { pk = null; rej(new Error("paykit")); };
        document.head.appendChild(s);
      });
    }
    return pk;
  }

  function maybeShow() {
    if (shown || !interacted) return;
    if (!hasResult()) return;
    if (!box) build();
    if (!box) return;
    shown = true;
    box.hidden = false;
    requestAnimationFrame(function () { requestAnimationFrame(function () { box.classList.add("on"); }); });
  }
  var timer = null;
  function onUse(e) {
    if (e && e.target && e.target.closest && e.target.closest(".tip-jar")) return;
    interacted = true;
    clearTimeout(timer);
    timer = setTimeout(maybeShow, 1800); // let them read the result first
  }
  function init() {
    var main = document.querySelector("main") || document.body;
    ["input", "change"].forEach(function (ev) { main.addEventListener(ev, onUse, true); });
    main.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest("button, [role=radio], input[type=radio], input[type=checkbox], label")) onUse(e);
    }, true);
    if (location.search.replace(/[?&]test=1\b/, "").length > 1 || location.hash.length > 1) { // opened with a shared result
      interacted = true;
      setTimeout(maybeShow, 3000);
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
