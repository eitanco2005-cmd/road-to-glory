/* תכנון פלוס — pay-to-export unlock for the web apps (seating, CV).
 *
 * Single site-wide mechanism (assets/checkout.js + thanks pages): a purchase of a product with "unlock": true is
 * stored in localStorage "tp-unlock:<slug>" = {o: orderId, t: time, test: bool} and announced with the window
 * event "tp:unlocked". The older "tp-unlocks" object / "site:unlocked" event (first ws/apps build) are still read as
 * a compatibility alias. Client-side convenience, not DRM: honest and simple on purpose.
 * Test-mode unlocks (?test=1 purchases) only count while the page itself runs with ?test=1.
 *
 *   AppUnlock.isUnlocked(slug)
 *   AppUnlock.require(slug, opts) -> true if unlocked, else opens the purchase dialog and returns false
 *   AppUnlock.onChange(fn)         -> fn(slug) after a purchase in this or another tab
 */
(function () {
  "use strict";
  var PREFIX = "tp-unlock:", LEGACY = "tp-unlocks";
  var TEST = new URLSearchParams(location.search).get("test") === "1";
  var EN = /^en/i.test(document.documentElement.lang || "");
  function L(he, en) { return EN ? en : he; }
  var listeners = [];

  function rec(slug) {
    try { var r = JSON.parse(localStorage.getItem(PREFIX + slug) || "null"); if (r && r.o) return r; } catch (e) {}
    try { var all = JSON.parse(localStorage.getItem(LEGACY) || "{}") || {}; if (all[slug] && all[slug].o) return all[slug]; } catch (e) {}
    return null;
  }
  function isUnlocked(slug) {
    var u = rec(slug);
    return !!(u && (!u.test || TEST));
  }
  function emit(slug) { listeners.forEach(function (fn) { try { fn(slug); } catch (e) { if (window.console) console.error(e); } }); }
  window.addEventListener("tp:unlocked", function (e) { emit(e.detail && e.detail.slug); });
  window.addEventListener("site:unlocked", function (e) { emit(e.detail && e.detail.slug); });
  window.addEventListener("storage", function (e) { if (e.key && (e.key.indexOf(PREFIX) === 0 || e.key === LEGACY)) emit(null); });

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
      bundleChoice(slug, opts) +
      '<div class="buy" data-product="' + esc(slug) + '" data-compact="1"></div>' +
      '<p class="small muted mt-2">' + L("התשלום חד-פעמי. אחריו הייצוא הנקי נפתח מיד בדפדפן הזה, בלי הרשמה. " +
      "הנתונים שלכם לא נשלחים אלינו: הכל נשמר רק במכשיר שלכם. " +
      "כבר קניתם במכשיר אחר? פתחו כאן את קישור דף התודה שקיבלתם אחרי התשלום והגרסה המלאה תיפתח גם בדפדפן הזה.",
      "One-time payment. Clean exports unlock right away in this browser, no sign-up. " +
      "Your data is never sent to us: everything stays on your device. " +
      "Bought on another device? Open the order confirmation link you got after paying, here, and the full version unlocks in this browser too.") + "</p>";
    document.body.appendChild(dlg);
    wireBundle(dlg, slug);
    dlg.addEventListener("close", function () { if (dlg) { dlg.remove(); dlg = null; } });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    if (window.SiteCheckout) window.SiteCheckout.render();
  }

  /* R6B: wedding tools offer the wedding bundle (all four tools) next to the single unlock, marked as the best value.
   * The single product stays pre-selected; choosing the bundle swaps the buy box. A bundle purchase goes to the
   * thanks page, which unlocks every member tool in this browser (data stays in localStorage meanwhile). */
  var BUNDLE = "wedding-bundle", BUNDLE_OF = ["seating-chart", "rsvp-tracker", "invitation-maker"];
  function bundleChoice(slug, opts) {
    if (EN || opts.bundle === false || BUNDLE_OF.indexOf(slug) < 0) return "";
    return '<div class="up-opts" role="radiogroup" aria-label="מה לפתוח">' +
      '<label class="up-opt"><input type="radio" name="up-choice" value="' + esc(slug) + '" checked><span><strong>רק הכלי הזה</strong>' +
      '<small>הגרסה המלאה של הכלי שאתם עובדים בו עכשיו</small></span><span class="up-price" data-price-of="' + esc(slug) + '"></span></label>' +
      '<label class="up-opt best"><input type="radio" name="up-choice" value="' + BUNDLE + '"><span><strong>חבילת החתונה · הכי משתלם</strong>' +
      '<small>הכלי הזה + הושבה / אישורי הגעה / הזמנות במלואם + מתכנן החתונה באקסל. <span data-bundle-save></span> ' +
      '<a href="' + esc(ROOT + "p/wedding-bundle/") + '" target="_blank" rel="noopener">מה כלול?</a></small></span>' +
      '<span class="up-price" data-price-of="' + BUNDLE + '"></span></label></div>' +
      '<p class="small muted up-bundle-note" hidden>אחרי תשלום על החבילה תעברו לדף עם כל ארבעת הכלים. מה שהזנתם כאן נשמר בדפדפן ומחכה לכם.</p>';
  }
  function wireBundle(d, slug) {
    var group = d.querySelector(".up-opts");
    if (!group || !window.SiteCheckout || !SiteCheckout.resolve) return;
    SiteCheckout.resolve(BUNDLE).then(function (info) {
      var total = info.members.reduce(function (a, m) { return a + (m ? Number(m.price_ils) : 0); }, 0);
      var price = Number(info.product.price_ils);
      var b = d.querySelector('[data-price-of="' + BUNDLE + '"]'), sv = d.querySelector("[data-bundle-save]");
      if (b) b.textContent = "₪" + price;
      if (sv && total > price) sv.textContent = "₪" + price + " במקום ₪" + total + " בנפרד.";
      info.members.forEach(function (m) { var e = m && d.querySelector('[data-price-of="' + m.slug + '"]'); if (e) e.textContent = "₪" + Number(m.price_ils); });
    }).catch(function () { group.remove(); });
    group.addEventListener("change", function (e) {
      var v = e.target && e.target.value;
      var old = d.querySelector(".buy[data-product]");
      if (!v || !old) return;
      var nb = document.createElement("div");
      nb.className = "buy"; nb.setAttribute("data-product", v); nb.setAttribute("data-compact", "1");
      old.replaceWith(nb);
      var note = d.querySelector(".up-bundle-note");
      if (note) note.hidden = v !== BUNDLE;
      SiteCheckout.render();
    });
  }
  /* Non-blocking upgrade message (e.g. after a free watermarked export). */
  function nudge(slug, opts) {
    opts = opts || {};
    var old = document.querySelector(".upgrade-note[data-nudge]");
    if (old) old.remove();
    var n = document.createElement("div");
    n.className = "upgrade-note"; n.setAttribute("data-nudge", slug); n.setAttribute("role", "status");
    var wedding = !EN && BUNDLE_OF.indexOf(slug) >= 0;
    n.innerHTML = "<p><strong>" + esc(opts.title || L("רוצים גרסה נקייה?", "Want a clean copy?")) + "</strong> " + esc(opts.text || "") + "</p>" +
      '<p class="btn-row"><button type="button" class="btn small accent" data-nudge-open>' + esc(opts.cta || L("לפתיחת הגרסה המלאה", "Unlock the full version")) + "</button>" +
      (wedding ? ' <a class="btn small secondary" href="' + esc(ROOT + "p/wedding-bundle/") + '">כל 4 הכלים בחבילה · הכי משתלם</a>' : "") +
      ' <button type="button" class="btn small secondary" data-nudge-x>' + L("לא עכשיו", "Not now") + "</button></p>";
    var at = opts.anchor && document.querySelector(opts.anchor);
    if (at) at.parentNode.insertBefore(n, at); else document.body.appendChild(n);
    n.querySelector("[data-nudge-open]").addEventListener("click", function () { open(slug, opts.dialog || {}); });
    n.querySelector("[data-nudge-x]").addEventListener("click", function () { n.remove(); });
    return n;
  }

  listeners.push(function (slug) {
    if (dlg && (!slug || isUnlocked(slug))) {
      var box = dlg.querySelector(".buy");
      var note = document.createElement("div");
      note.className = "callout success-callout mt-2";
      note.setAttribute("role", "status");
      note.innerHTML = L("<strong>תודה! הגרסה המלאה פתוחה.</strong> אפשר לסגור את החלון ולייצא.", "<strong>Thank you! The full version is unlocked.</strong> Close this window and export.") +
        (slug && rec(slug) ? ' <a href="' + esc(thanksUrl(slug)) + '" target="_blank" rel="noopener">' + L("דף אישור ההזמנה", "Order confirmation page") + "</a> " + L("(שמרו אותו כדי לפתוח את הגרסה המלאה גם במכשיר אחר).", "(keep it to unlock on another device).") : "");
      if (box) box.after(note);
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn block mt-2"; b.textContent = L("סגירה והמשך", "Close and continue");
      b.addEventListener("click", function () { dlg.close(); });
      note.after(b);
    }
  });

  function thanksUrl(slug) {
    var u = rec(slug) || {};
    return new URL((EN ? "en/" : "") + "thanks/?p=" + encodeURIComponent(slug) + "&o=" + encodeURIComponent(u.o || "") + (u.test ? "&test=1" : ""), ROOT).href;
  }
  var ROOT = new URL("../../", (document.currentScript && document.currentScript.src) || location.href).href;

  window.AppUnlock = {
    isUnlocked: isUnlocked,
    require: function (slug, opts) { if (isUnlocked(slug)) return true; open(slug, opts); return false; },
    open: open,
    nudge: nudge,
    onChange: function (fn) { listeners.push(fn); },
    thanksUrl: thanksUrl,
    isTest: TEST
  };
})();
