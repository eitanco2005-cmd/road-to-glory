/* תכנון פלוס upsells (honest: real savings, no timers, no fake scarcity).
 *
 * 1) Product pages (p/<slug>/, loaded automatically by site.js): under the main buy box, show the smallest
 *    bundle that contains this product with the real saving ("חוסכים ₪X") and a link to it.
 * 2) Thanks page (thanks/?p=<slug>&o=<order>, loaded by site.js): offer the complementary product once,
 *    at 20% off, paid right there via paykit.js. Not shown for test orders unless ?test=1 is on, not shown if the
 *    buyer already owns the product (this browser's purchase list), and only once per browser (offer remembered).
 *    The discounted purchase goes to the normal thanks page of that product.
 * Data: data/upsell.json ({"complement": {"<slug>": "<slug>"}, "discount_pct": 20}).
 * Opt out on a page: <html data-upsell="off">.
 */
(function () {
  "use strict";
  if (window.__upsell || document.documentElement.getAttribute("data-upsell") === "off") return;
  window.__upsell = true;
  var me = document.currentScript || document.querySelector('script[src*="assets/upsell.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var ROOT = new URL("../", ASSETS).href;
  var Q = new URLSearchParams(location.search);
  var TEST = Q.get("test") === "1";
  var OFFER_KEY = TEST ? "tp-offer-test" : "tp-offer"; // test orders never use up the real one-time offer

  var CSS =
    ".upsell-box{margin-top:.9rem;border:1.5px solid var(--success,#1d7a46);background:var(--success-soft,#e3f4ea);border-radius:var(--radius-sm,9px);" +
    "padding:.75rem .95rem;font-size:.97rem;color:var(--text,#1d2a2e)}.upsell-box strong.save{color:var(--success,#1d7a46)}" +
    ".upsell-box p{margin:.15rem 0}.upsell-box a{font-weight:700}" +
    ".offer-box{margin-top:2rem;border:1px solid var(--border,#e5ddcf);border-radius:var(--radius,14px);background:var(--surface,#fff);" +
    "padding:1.15rem;box-shadow:var(--shadow)}.offer-box h2{margin-top:0;font-size:1.25rem}" +
    ".offer-price{font-size:1.5rem;font-weight:800}.offer-price s{font-size:1rem;color:var(--muted,#586770);font-weight:400;margin-inline-start:.4rem}" +
    ".offer-pay{max-width:380px;margin-top:.7rem}.offer-box .muted{color:var(--muted,#586770)}";

  var json = {};
  function get(path) {
    if (!json[path]) json[path] = fetch(ROOT + path, { cache: "no-cache" }).then(function (r) { if (!r.ok) throw new Error(path); return r.json(); });
    return json[path];
  }
  function product(slug) { return /^[a-z0-9-]+$/.test(slug) ? get("data/products/" + slug + ".json") : Promise.reject(new Error("slug")); }
  function deliverable(p) { return !!p && !p.placeholder && ((p.files && p.files.length) || !!p.sheets_copy_url); }
  function ils(n) { n = Number(n) || 0; return "₪" + (n % 1 === 0 ? n.toLocaleString("he-IL") : n.toFixed(2)); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }
  function style() {
    if (document.getElementById("upsell-css")) return;
    var s = document.createElement("style"); s.id = "upsell-css"; s.textContent = CSS; document.head.appendChild(s);
  }
  function bundleInfo(b) {
    return Promise.all((b.bundle_of || []).map(function (s) { return product(s).catch(function () { return null; }); })).then(function (ms) {
      var total = ms.reduce(function (a, m) { return a + (m ? Number(m.price_ils) : 0); }, 0);
      return { b: b, ms: ms, total: total, save: total - Number(b.price_ils), ok: !b.placeholder && ms.every(deliverable) };
    });
  }

  /* ---------- 1) product page: matching bundle with savings ---------- */
  function productPage(slug) {
    var anchor = document.querySelector('.buy[data-product="' + slug + '"]');
    if (!anchor) return;
    get("data/products/index.json").then(function (idx) {
      return Promise.all((idx.bundles || []).map(function (s) { return product(s).then(bundleInfo).catch(function () { return null; }); }));
    }).then(function (list) {
      var hits = list.filter(function (x) { return x && x.ok && x.save > 0 && (x.b.bundle_of || []).indexOf(slug) >= 0; });
      if (!hits.length) return;
      hits.sort(function (a, b) { return a.ms.length - b.ms.length; });
      var best = hits[0], all = hits.length > 1 ? hits[hits.length - 1] : null;
      var others = best.ms.filter(function (m) { return m && m.slug !== slug; }).map(function (m) { return m.title; });
      // the bundle may already have a buy box on this page; otherwise link to the bundles section
      var onPage = document.querySelector('.buy[data-product="' + best.b.slug + '"]');
      var href = onPage ? "#upsell-" + best.b.slug : ROOT + "products/#" + best.b.slug;
      if (onPage && !onPage.id) onPage.id = "upsell-" + best.b.slug;
      else if (onPage) href = "#" + onPage.id;
      style();
      var el = document.createElement("div");
      el.className = "upsell-box";
      el.setAttribute("data-upsell-bundle", best.b.slug);
      el.innerHTML =
        "<p>💡 <strong>" + esc(best.b.title) + "</strong>: הקובץ הזה" + (others.length ? " + " + esc(others.join(" + ")) : "") + " " +
        "ב-" + ils(best.b.price_ils) + " במקום " + ils(best.total) + " – <strong class=\"save\">חוסכים " + ils(best.save) + "</strong>.</p>" +
        '<p><a href="' + esc(href) + '">לחבילה ←</a>' +
        (all ? ' <span class="muted small">· או <a href="' + esc(ROOT + "products/#" + all.b.slug) + '">' + esc(all.b.title) + "</a> ב-" + ils(all.b.price_ils) + " (חוסכים " + ils(all.save) + ")</span>" : "") +
        "</p>";
      anchor.parentNode.insertBefore(el, anchor.nextSibling);
    }).catch(function () {});
  }

  /* ---------- 2) thanks page: one-time 20% offer on the complementary product ---------- */
  function owned() {
    try { return (JSON.parse(localStorage.getItem("tp-orders") || "[]") || []).map(function (x) { return x.p; }); } catch (e) { return []; }
  }
  function offerState() { try { return JSON.parse(localStorage.getItem(OFFER_KEY) || "{}") || {}; } catch (e) { return {}; } }
  function saveOffer(s) { try { localStorage.setItem(OFFER_KEY, JSON.stringify(s)); } catch (e) {} }

  function thanksPage() {
    var slug = Q.get("p") || "", order = Q.get("o") || "";
    if (!/^[a-z0-9-]+$/.test(slug) || !order) return;
    var st = offerState();
    // one offer per browser: once it was shown for another order (or used), never again
    if (st.used || (st.order && st.order !== order)) return;
    var ok = document.getElementById("ok");
    if (!ok) return;
    Promise.all([get("data/upsell.json"), product(slug)]).then(function (r) {
      var cfg = r[0], bought = r[1];
      var target = (cfg.complement || {})[slug];
      if (!target) return;
      var have = owned();
      var covered = [slug].concat(bought.bundle_of || []);
      have.forEach(function (s) { covered.push(s); });
      return Promise.all(have.map(function (s) { return product(s).catch(function () { return null; }); })).then(function (ps) {
        ps.forEach(function (p) { if (p) (p.bundle_of || []).forEach(function (s) { covered.push(s); }); });
        if (covered.indexOf(target) >= 0) return;
        return product(target).then(function (t) {
          if (!deliverable(t) && !(t.bundle_of && t.bundle_of.length)) return;
          var pct = Math.min(50, Math.max(1, Number(cfg.discount_pct) || 20));
          var price = Math.round(Number(t.price_ils) * (100 - pct)) / 100;
          price = Math.round(price); // whole shekels, honest rounding
          waitVisible(ok, function () { renderOffer(ok, t, price, pct, order); });
          saveOffer({ order: order, slug: t.slug, shown: Date.now() });
        });
      });
    }).catch(function () {});
  }
  function waitVisible(el, fn) {
    if (!el.hidden) return fn();
    var mo = new MutationObserver(function () { if (!el.hidden) { mo.disconnect(); fn(); } });
    mo.observe(el, { attributes: true, attributeFilter: ["hidden"] });
  }
  function renderOffer(ok, t, price, pct, order) {
    style();
    var box = document.createElement("section");
    box.className = "offer-box";
    box.setAttribute("data-offer", t.slug);
    box.innerHTML =
      '<span class="badge success">הצעה ללקוחות בלבד · ' + pct + "% הנחה</span>" +
      '<h2 class="mt-1">אולי יתאים לכם גם: ' + esc(t.title) + "</h2>" +
      '<p class="muted">' + esc(t.subtitle || "") + "</p>" +
      '<div class="offer-price"><span class="num">' + ils(price) + '</span><s class="num">' + ils(t.price_ils) + "</s></div>" +
      '<p class="small muted mb-0">הצעה חד-פעמית כתודה על הרכישה, מופיעה רק בדף הזה. בלי לחץ ובלי שעון: אפשר גם פשוט לדלג. ' +
      '<a href="' + esc(ROOT + "p/" + t.slug + "/") + '" target="_blank" rel="noopener">מה בדיוק בקובץ?</a></p>' +
      '<div class="offer-pay"></div>';
    var support = document.getElementById("support");
    var anchorH = support && support.previousElementSibling;
    ok.insertBefore(box, anchorH && anchorH.tagName === "H2" ? anchorH : null);
    loadPayKit().then(function () {
      window.PayKit.render(box.querySelector(".offer-pay"), {
        amount: price, currency: "ILS", sku: t.slug, name: String(t.title) + " (" + pct + "% הנחה)", locale: "he_IL", lang: "he",
        testLabel: "תשלום בדיקה " + ils(price) + " (TEST)",
        onPaid: function (info) {
          saveOffer({ order: order, slug: t.slug, used: Date.now() });
          location.href = ROOT + "thanks/?p=" + encodeURIComponent(t.slug) + "&o=" + encodeURIComponent(info.orderId) + (info.test ? "&test=1" : "");
        }
      });
    }).catch(function () { box.remove(); });
  }
  var pk = null;
  function loadPayKit() {
    if (window.PayKit) return Promise.resolve();
    if (!pk) pk = new Promise(function (res, rej) {
      var s = document.createElement("script"); s.src = ASSETS + "paykit.js"; s.async = true;
      s.onload = function () { res(); }; s.onerror = function () { pk = null; rej(new Error("paykit")); };
      document.head.appendChild(s);
    });
    return pk;
  }

  function init() {
    var path = location.pathname;
    var m = /\/p\/([a-z0-9-]+)\/(?:index\.html)?$/.exec(path);
    if (m) return productPage(m[1]);
    if (/\/thanks\/(?:index\.html)?$/.test(path)) return thanksPage();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
