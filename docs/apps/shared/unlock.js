/* תכנון פלוס — pay-to-export unlock for the web apps.
 *
 * Purchases of products with "unlock": true are stored by assets/checkout.js (and the thanks page) in
 * localStorage "tp-unlocks" = {slug: {o: orderId, t: time, test: bool}} and announced with the window event
 * "site:unlocked". This is a client-side convenience, not DRM: it is honest and simple on purpose.
 * Test-mode unlocks (?test=1 purchases) only count while the page itself runs with ?test=1.
 *
 *   AppUnlock.isUnlocked(slug)
 *   AppUnlock.require(slug, opts) -> true if unlocked, else opens the purchase dialog and returns false
 *   AppUnlock.onChange(fn)         -> fn(slug) after a purchase in this or another tab
 */
(function () {
  "use strict";
  var KEY = "tp-unlocks";
  var TEST = new URLSearchParams(location.search).get("test") === "1";
  var EN = /^en/i.test(document.documentElement.lang || "");
  function L(he, en) { return EN ? en : he; }
  var listeners = [];

  function all() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function isUnlocked(slug) {
    var u = all()[slug];
    return !!(u && u.o && (!u.test || TEST));
  }
  function emit(slug) { listeners.forEach(function (fn) { try { fn(slug); } catch (e) { if (window.console) console.error(e); } }); }
  window.addEventListener("site:unlocked", function (e) { emit(e.detail && e.detail.slug); });
  window.addEventListener("storage", function (e) { if (e.key === KEY) emit(null); });

  var dlg = null;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function open(slug, opts) {
    opts = opts || {};
    if (dlg) dlg.remove();
    dlg = document.createElement("dialog");
    dlg.className = "app-dialog unlock-dialog";
    dlg.setAttribute("aria-labelledby", "unlock-title");
    var feats = (opts.features || []).map(function (f) { return "<li>" + esc(f) + "</li>"; }).join("");
    dlg.innerHTML =
      '<form method="dialog" class="dlg-close-row"><button class="dlg-x" aria-label="' + L("סגירה", "Close") + '" value="close">×</button></form>' +
      '<h2 id="unlock-title">' + esc(opts.title || L("פתיחת הגרסה המלאה", "Unlock the full version")) + "</h2>" +
      (opts.reason ? '<p class="muted">' + esc(opts.reason) + "</p>" : "") +
      (feats ? '<ul class="unlock-feats">' + feats + "</ul>" : "") +
      '<div class="buy" data-product="' + esc(slug) + '" data-compact="1"></div>' +
      '<p class="small muted mt-2">' + L("התשלום חד-פעמי. אחריו הייצוא הנקי נפתח מיד בדפדפן הזה, בלי הרשמה. " +
      "הנתונים שלכם לא נשלחים אלינו: הכל נשמר רק במכשיר שלכם. " +
      "כבר קניתם במכשיר אחר? פתחו כאן את קישור דף התודה שקיבלתם אחרי התשלום והגרסה המלאה תיפתח גם בדפדפן הזה.",
      "One-time payment. Clean exports unlock right away in this browser, no sign-up. " +
      "Your data is never sent to us: everything stays on your device. " +
      "Bought on another device? Open the order confirmation link you got after paying, here, and the full version unlocks in this browser too.") + "</p>";
    document.body.appendChild(dlg);
    dlg.addEventListener("close", function () { if (dlg) { dlg.remove(); dlg = null; } });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    if (window.SiteCheckout) window.SiteCheckout.render();
  }

  listeners.push(function (slug) {
    if (dlg && (!slug || isUnlocked(slug))) {
      var box = dlg.querySelector(".buy");
      var note = document.createElement("div");
      note.className = "callout success-callout mt-2";
      note.setAttribute("role", "status");
      note.innerHTML = L("<strong>תודה! הגרסה המלאה פתוחה.</strong> אפשר לסגור את החלון ולייצא.", "<strong>Thank you! The full version is unlocked.</strong> Close this window and export.") +
        (slug && all()[slug] ? ' <a href="' + esc(thanksUrl(slug)) + '" target="_blank" rel="noopener">' + L("דף אישור ההזמנה", "Order confirmation page") + "</a> " + L("(שמרו אותו כדי לפתוח את הגרסה המלאה גם במכשיר אחר).", "(keep it to unlock on another device).") : "");
      if (box) box.after(note);
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn block mt-2"; b.textContent = L("סגירה והמשך", "Close and continue");
      b.addEventListener("click", function () { dlg.close(); });
      note.after(b);
    }
  });

  function thanksUrl(slug) {
    var u = all()[slug] || {};
    return new URL((EN ? "en/" : "") + "thanks/?p=" + encodeURIComponent(slug) + "&o=" + encodeURIComponent(u.o || "") + (u.test ? "&test=1" : ""), ROOT).href;
  }
  var ROOT = new URL("../../", (document.currentScript && document.currentScript.src) || location.href).href;

  window.AppUnlock = {
    isUnlocked: isUnlocked,
    require: function (slug, opts) { if (isUnlocked(slug)) return true; open(slug, opts); return false; },
    open: open,
    onChange: function (fn) { listeners.push(fn); },
    thanksUrl: thanksUrl,
    isTest: TEST
  };
})();
