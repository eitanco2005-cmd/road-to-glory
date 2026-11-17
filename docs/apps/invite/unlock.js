/* תכנון פלוס — tiny client-side unlock store for pay-to-export apps.
 * checkout.js (product JSON "unlock": true) calls TPUnlock.set(slug, orderId, test) after a captured payment and
 * fires a "tp:unlocked" event on window. Apps call TPUnlock.has(slug).
 * Honest note: this is a browser-only flag (localStorage). It is bypassable by design; there is no backend.
 * Test unlocks (?test=1 purchases) only count on pages opened with ?test=1, so they never leak into real use.
 */
(function () {
  "use strict";
  if (window.TPUnlock) return;
  var PREFIX = "tp-unlock:";
  var TEST = new URLSearchParams(location.search).get("test") === "1";
  function read(slug) {
    try { return JSON.parse(localStorage.getItem(PREFIX + slug) || "null"); } catch (e) { return null; }
  }
  window.TPUnlock = {
    get: read,
    has: function (slug) {
      var r = read(slug);
      return !!(r && r.o && (!r.test || TEST));
    },
    set: function (slug, orderId, test) {
      var rec = { o: String(orderId || ""), t: Date.now(), test: !!test };
      try { localStorage.setItem(PREFIX + slug, JSON.stringify(rec)); } catch (e) {}
      try { window.dispatchEvent(new CustomEvent("tp:unlocked", { detail: { slug: slug, orderId: rec.o, test: rec.test } })); } catch (e) {}
      return rec;
    },
    clear: function (slug) { try { localStorage.removeItem(PREFIX + slug); } catch (e) {} }
  };
})();
