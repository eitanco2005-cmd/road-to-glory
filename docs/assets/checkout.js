/* תכנון פלוס checkout — renders PayPal buttons into every <div class="buy" data-product="<slug>"></div>.
 *
 * Flow: read data/products/<slug>.json (+ members for bundles) -> PayPal JS SDK (client id from config.js,
 * product currency, intent capture) -> createOrder with title/price from the JSON -> onApprove: capture ->
 * recordSale() -> redirect to thanks/?p=<slug>&o=<orderId>.
 *
 * TEST mode: add ?test=1 to the page URL. PayPal is skipped and a simulated success is used
 * (order id TEST-..., sale logged with test:true, thanks page opened with &test=1).
 *
 * Optional attributes on the .buy div:
 *   data-compact="1"   smaller box without the title line
 *   data-label="..."   override the title line
 * A product is purchasable only if it is not a placeholder and has files or a Sheets copy link
 * (bundles: every member must be purchasable). Otherwise a "בקרוב" box is shown.
 *
 * Unlock products ("unlock": true in the JSON, used by the web apps under apps/): no redirect after capture;
 * the purchase is saved in localStorage "tp-unlocks" and the event "site:unlocked" is dispatched on window.
 * Currency: per product. JSON "currency" (default "ILS") + "price" (falls back to "price_ils"). The PayPal SDK is
 * loaded once per page with the currency of the first product rendered, so keep one currency per page; a product
 * in another currency on the same page shows an error instead of a wrong charge.
 * Language: pages with <html lang="en"> (or products with "lang":"en") get English UI, en_US PayPal locale,
 * en/legal/ links and the en/thanks/ download page.
 *
 * Apple Pay / Google Pay: config ENABLE_APPLEPAY / ENABLE_GOOGLEPAY (default false) only load the SDK components.
 * Rendering those buttons is NOT implemented yet: it needs merchant eligibility in the PayPal account,
 * Apple Pay domain verification and the separate Google Pay JS. See ops/reports/W1-platform.md.
 */
(function () {
  "use strict";
  var me = document.currentScript || document.querySelector('script[src*="assets/checkout.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var ROOT = new URL("../", ASSETS).href;
  var params = new URLSearchParams(location.search);
  var TEST = params.get("test") === "1";
  var EN = /^en/i.test(document.documentElement.getAttribute("lang") || "");
  var T = EN ? {
    soon: "Coming soon", soonBtn: "Coming soon: in preparation", price: "Price",
    secure: "Secure checkout with PayPal or any debit/credit card. No PayPal account needed",
    notes: ["One-time payment", "Instant download", "No sign-up"],
    legal: function (t, r) { return 'By purchasing you agree to the <a href="' + t + '">Terms</a> and the <a href="' + r + '">Refund policy</a>. Prices in US dollars.'; },
    paid: "Payment received! Taking you to your download page…", unlocked: "Payment received! The full version is now unlocked in this browser.", orderLink: "Order confirmation page", testFlag: "TEST mode: no charge will be made",
    testPay: "Test payment", loading: "Loading payment options…", unavailable: "Payment is not available right now. Please try again later.",
    confirming: "Confirming your payment…", declined: "Your payment method was declined. Please try another one.",
    cancelled: "Payment cancelled. You can try again any time.", error: "Something went wrong and you were not charged. Please refresh and try again.",
    loadFail: "We couldn't load the payment system. Check your connection or turn off your ad blocker for this site, then try again.",
    retry: "Try again", notFound: "Product not found.", mixed: "This page can only take one currency at a time. Open the product page to buy this item."
  } : {
    soon: "בקרוב", soonBtn: "בקרוב — המוצר בהכנה", price: "מחיר",
    secure: "תשלום מאובטח ב-PayPal או בכרטיס אשראי — אין צורך בחשבון PayPal",
    notes: ["תשלום חד-פעמי", "הורדה מיידית", "בלי הרשמה"],
    legal: function (t, r) { return 'ברכישה הנך מאשר/ת את <a href="' + t + '">התקנון</a> ואת <a href="' + r + '">מדיניות הביטולים</a>. המחיר סופי.'; },
    paid: "התשלום התקבל! מעבירים אותך לדף ההורדה…", unlocked: "התשלום התקבל! הגרסה המלאה נפתחה בדפדפן הזה.", orderLink: "לדף אישור ההזמנה", testFlag: "מצב בדיקה (TEST) — לא יתבצע חיוב",
    testPay: "תשלום בדיקה", loading: "טוען את אפשרויות התשלום…", unavailable: "התשלום אינו זמין כרגע. נסו שוב מאוחר יותר.",
    confirming: "מאשרים את התשלום…", declined: "אמצעי התשלום נדחה. נסו אמצעי אחר.",
    cancelled: "התשלום בוטל. אפשר לנסות שוב בכל רגע.", error: "משהו השתבש בתשלום ולא בוצע חיוב. רעננו את הדף ונסו שוב.",
    loadFail: "לא הצלחנו לטעון את מערכת התשלום. בדקו את החיבור לאינטרנט, או כבו חוסם פרסומות לאתר זה, ונסו שוב.",
    retry: "לנסות שוב", notFound: "המוצר לא נמצא.", mixed: "בדף זה אפשר לשלם במטבע אחד בלבד. לרכישת המוצר עברו לדף המוצר."
  };
  function currencyOf(p) { return String((p && p.currency) || "ILS").toUpperCase(); }
  function priceOf(p) { return Number(p && p.price != null ? p.price : p && p.price_ils); }
  function isEn(p) { return EN || (p && p.lang === "en"); }

  var loaded = {};
  function loadScript(src) {
    if (!loaded[src]) {
      loaded[src] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = src; s.async = true;
        s.setAttribute("data-site-sdk", "1");
        s.onload = function () { resolve(); };
        s.onerror = function () { delete loaded[src]; s.remove(); reject(new Error("load failed")); };
        document.head.appendChild(s);
      });
    }
    return loaded[src];
  }
  function config() {
    if (window.SITE_CONFIG) return Promise.resolve(window.SITE_CONFIG);
    return loadScript(ASSETS + "config.js").then(function () { return window.SITE_CONFIG || {}; });
  }
  function sales() {
    if (window.recordSale) return Promise.resolve();
    return loadScript(ASSETS + "sales.js");
  }
  var cache = {};
  function getProduct(slug) {
    if (!/^[a-z0-9-]+$/.test(slug)) return Promise.reject(new Error("bad slug"));
    if (!cache[slug]) {
      cache[slug] = fetch(ROOT + "data/products/" + slug + ".json", { cache: "no-cache" }).then(function (r) {
        if (!r.ok) throw new Error("product " + slug + " " + r.status);
        return r.json();
      });
    }
    return cache[slug];
  }
  function isDeliverable(p) {
    return !!p && !p.placeholder && ((p.files && p.files.length > 0) || !!p.sheets_copy_url || !!p.unlock);
  }
  /* -> {product, members[], available} */
  function resolve(slug) {
    return getProduct(slug).then(function (p) {
      var ids = p.bundle_of || [];
      if (!ids.length) return { product: p, members: [], available: isDeliverable(p) };
      return Promise.all(ids.map(function (id) { return getProduct(id).catch(function () { return null; }); })).then(function (ms) {
        return { product: p, members: ms, available: !p.placeholder && ms.every(isDeliverable) };
      });
    });
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function money(n, cur) {
    var v = Number(n) % 1 === 0 ? String(Number(n)) : Number(n).toFixed(2);
    cur = cur || "ILS";
    return cur === "ILS" ? "₪" + v : cur === "USD" ? "$" + v : cur === "EUR" ? "€" + v : v + " " + cur;
  }
  function price2(n) { return (Math.round(Number(n) * 100) / 100).toFixed(2); }

  function thanksUrl(slug, orderId, test, en) {
    return ROOT + (en ? "en/" : "") + "thanks/?p=" + encodeURIComponent(slug) + "&o=" + encodeURIComponent(orderId) + (test ? "&test=1" : "");
  }
  /* Products with "unlock": true (web apps: pay to export) do not redirect: the purchase is stored in
   * localStorage "tp-unlocks" and the page is told via the window event "site:unlocked" (see apps/shared/unlock.js). */
  var UNLOCK_KEY = "tp-unlocks";
  function storeUnlock(slug, orderId, test) {
    try {
      var all = JSON.parse(localStorage.getItem(UNLOCK_KEY) || "{}") || {};
      if (!all[slug] || all[slug].test || !test) all[slug] = { o: orderId, t: Date.now(), test: !!test };
      localStorage.setItem(UNLOCK_KEY, JSON.stringify(all));
    } catch (e) {}
  }
  function unlocked(box, slug, orderId, amount, currency, status, test, en) {
    storeUnlock(slug, orderId, test);
    setMsg(box, "info", T.unlocked);
    var m = box.querySelector(".buy-msg");
    if (m) {
      m.appendChild(document.createTextNode(" "));
      var a = document.createElement("a");
      a.href = thanksUrl(slug, orderId, test, en); a.target = "_blank"; a.rel = "noopener";
      a.textContent = T.orderLink;
      m.appendChild(a);
    }
    var btns = box.querySelector(".buy-buttons");
    if (btns) btns.hidden = true;
    sales().then(function () {
      return window.recordSale({ orderId: orderId, slug: slug, amount: amount, currency: currency, status: status, test: test });
    }).catch(function () {});
    try { window.dispatchEvent(new CustomEvent("site:unlocked", { detail: { slug: slug, orderId: orderId, test: !!test } })); } catch (e) {}
  }
  function finish(box, slug, orderId, amount, currency, status, test, en, product) {
    if (product && product.unlock) return unlocked(box, slug, orderId, amount, currency, status, test, en);
    setMsg(box, "info", T.paid);
    var go = function () { location.href = thanksUrl(slug, orderId, test, en); };
    var timer = setTimeout(go, 2500); // never block the buyer on the sales log
    sales().then(function () {
      return window.recordSale({ orderId: orderId, slug: slug, amount: amount, currency: currency, status: status, test: test });
    }).catch(function () {}).then(function () { clearTimeout(timer); go(); });
  }
  function setMsg(box, kind, text) {
    var m = box.querySelector(".buy-msg");
    if (!m) { m = document.createElement("div"); m.setAttribute("role", "status"); box.appendChild(m); }
    m.className = "buy-msg " + kind;
    m.textContent = text;
  }

  function shell(el, info) {
    var p = info.product;
    var compact = el.getAttribute("data-compact") === "1";
    var label = el.getAttribute("data-label") || p.title;
    var lg = ROOT + (isEn(p) ? "en/" : "") + "legal/";
    el.innerHTML =
      '<div class="buy-box">' +
      (TEST ? '<div class="test-flag">' + T.testFlag + "</div>" : "") +
      '<div class="buy-head">' +
      (compact ? "" : '<div class="buy-title">' + esc(label) + "</div>") +
      '<div class="buy-price" aria-label="' + T.price + '">' + money(priceOf(p), currencyOf(p)) + "</div></div>" +
      '<div class="buy-buttons"></div>' +
      '<p class="buy-secure">' + T.secure + "</p>" +
      '<p class="buy-note"><span>' + T.notes.join("</span><span>") + "</span></p>" +
      '<p class="buy-legal">' + T.legal(lg + "terms/", lg + "refund/") + "</p>" +
      "</div>";
    return el.querySelector(".buy-box");
  }

  function renderSoon(el, info) {
    var box = shell(el, info);
    box.querySelector(".buy-buttons").innerHTML =
      '<button type="button" class="btn block" disabled aria-disabled="true">' + T.soonBtn + "</button>";
    box.querySelector(".buy-note").remove();
    box.querySelector(".buy-secure").remove();
    box.querySelector(".buy-legal").remove();
  }

  function renderTest(el, info) {
    var box = shell(el, info);
    var p = info.product;
    var b = document.createElement("button");
    b.type = "button"; b.className = "btn block accent"; b.setAttribute("data-test-pay", p.slug);
    b.textContent = T.testPay + " " + money(priceOf(p), currencyOf(p)) + " (TEST)";
    b.addEventListener("click", function () {
      b.disabled = true;
      var id = "TEST-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
      finish(box, p.slug, id, priceOf(p), currencyOf(p), "COMPLETED", true, isEn(p), p);
    });
    box.querySelector(".buy-buttons").appendChild(b);
  }

  var sdkPromise = null, sdkCurrency = null;
  function loadSdk(cfg, CURRENCY) {
    if (sdkCurrency && sdkCurrency !== CURRENCY) return Promise.reject(new Error("mixed currency"));
    if (window.paypal && window.paypal.Buttons && sdkCurrency === CURRENCY) return Promise.resolve(window.paypal);
    if (!sdkPromise) {
      sdkCurrency = CURRENCY;
      // enable-funding=card: show the guest "Debit or Credit Card" button (no PayPal account needed).
      // No disable-funding: every source PayPal offers the buyer stays available.
      var comps = ["buttons"];
      if (cfg.ENABLE_APPLEPAY) comps.push("applepay");
      if (cfg.ENABLE_GOOGLEPAY) comps.push("googlepay");
      var base = "https://www.paypal.com/sdk/js?client-id=" + encodeURIComponent(cfg.PAYPAL_CLIENT_ID) +
        "&currency=" + CURRENCY + "&intent=capture&enable-funding=card&components=" + comps.join(",");
      sdkPromise = loadScript(base + (EN ? "&locale=en_US" : "&locale=he_IL"))
        .catch(function () { return loadScript(base); }) // unsupported locale -> retry without it
        .then(function () {
          if (!window.paypal || !window.paypal.Buttons) throw new Error("paypal sdk missing");
          return window.paypal;
        });
      sdkPromise.catch(function () { sdkPromise = null; sdkCurrency = null; });
    }
    return sdkPromise;
  }

  function renderPayPal(el, info, cfg) {
    var box = shell(el, info);
    var p = info.product;
    var holder = box.querySelector(".buy-buttons");
    var CURRENCY = currencyOf(p), en = isEn(p);
    holder.innerHTML = '<div class="buy-loading" role="status"><div class="spinner" aria-hidden="true"></div>' + T.loading + "</div>";
    if (!cfg.PAYPAL_CLIENT_ID) { holder.innerHTML = ""; setMsg(box, "error", T.unavailable); return; }
    if (sdkCurrency && sdkCurrency !== CURRENCY) { holder.innerHTML = ""; setMsg(box, "error", T.mixed); return; }
    var value = price2(priceOf(p));
    var name = String(p.title || p.slug).slice(0, 127);
    loadSdk(cfg, CURRENCY).then(function (paypal) {
      holder.innerHTML = "";
      return paypal.Buttons({
        style: { layout: "vertical", shape: "pill", label: "pay", height: 48, tagline: false },
        createOrder: function (data, actions) {
          return actions.order.create({
            intent: "CAPTURE",
            purchase_units: [{
              reference_id: p.slug,
              custom_id: p.slug,
              description: name,
              amount: { currency_code: CURRENCY, value: value, breakdown: { item_total: { currency_code: CURRENCY, value: value } } },
              items: [{ name: name, sku: p.slug, quantity: "1", category: "DIGITAL_GOODS", unit_amount: { currency_code: CURRENCY, value: value } }]
            }],
            application_context: { shipping_preference: "NO_SHIPPING", brand_name: (en ? cfg.BRAND_LATIN : cfg.BRAND) || cfg.BRAND || "תכנון פלוס", user_action: "PAY_NOW" }
          });
        },
        onApprove: function (data, actions) {
          setMsg(box, "info", T.confirming);
          return actions.order.capture().then(function (det) {
            var err = det && det.details && det.details[0];
            if (err && err.issue === "INSTRUMENT_DECLINED") {
              setMsg(box, "error", T.declined);
              return actions.restart();
            }
            var cap = det && det.purchase_units && det.purchase_units[0] && det.purchase_units[0].payments &&
              det.purchase_units[0].payments.captures && det.purchase_units[0].payments.captures[0];
            var amt = cap && cap.amount ? Number(cap.amount.value) : Number(value);
            var cur = cap && cap.amount ? cap.amount.currency_code : CURRENCY;
            var status = (cap && cap.status) || det.status || "";
            finish(box, p.slug, det.id || data.orderID, amt, cur, status, false, en, p);
          });
        },
        onCancel: function () { setMsg(box, "info", T.cancelled); },
        onError: function (e) {
          if (window.console) console.error("PayPal error", e);
          setMsg(box, "error", T.error);
        }
      }).render(holder);
    }).catch(function (e) {
      if (window.console) console.error(e);
      if (e && e.message === "mixed currency") { holder.innerHTML = ""; setMsg(box, "error", T.mixed); return; }
      holder.innerHTML = '<div class="buy-msg error" role="alert" style="margin-top:0">' + T.loadFail + "</div>";
      var retry = document.createElement("button");
      retry.type = "button"; retry.className = "btn block mt-2"; retry.textContent = T.retry;
      retry.addEventListener("click", function () { renderPayPal(el, info, cfg); });
      holder.appendChild(retry);
    });
  }

  function renderOne(el, cfg) {
    var slug = el.getAttribute("data-product");
    if (!slug || el.getAttribute("data-buy-ready")) return;
    el.setAttribute("data-buy-ready", "1");
    resolve(slug).then(function (info) {
      if (TEST) return renderTest(el, info);
      if (!info.available) return renderSoon(el, info);
      renderPayPal(el, info, cfg);
    }).catch(function (e) {
      if (window.console) console.error(e);
      el.innerHTML = '<div class="buy-box"><div class="buy-msg error">' + T.notFound + "</div></div>";
    });
  }

  function init() {
    config().then(function (cfg) {
      var els = document.querySelectorAll(".buy[data-product]");
      for (var i = 0; i < els.length; i++) renderOne(els[i], cfg);
    });
  }
  window.SiteCheckout = { render: init, resolve: resolve, isTest: TEST, storeUnlock: storeUnlock };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
