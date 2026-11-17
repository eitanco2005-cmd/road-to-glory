/* תכנון פלוס PayKit: a small PayPal primitive for payments whose amount is decided on the page
 * (tips, the one-time thanks-page offer, USD products such as the RTL Landing Kit Pro).
 * The fixed-price Hebrew product flow stays in checkout.js; this file does not change it.
 *
 *   PayKit.render(holder, {
 *     amount: Number | function () -> Number,   // read at click time (so a custom amount can change)
 *     currency: "ILS" | "USD",                   // one currency per page (PayPal SDK limitation)
 *     sku: "tip",                                // product slug, sent as reference_id/custom_id/sku and to the sales log
 *     name: "Tip",                               // line item name
 *     locale: "he_IL" | "en_US",
 *     lang: "he" | "en",                         // UI text language
 *     validate: function () -> "" | "error text",
 *     test: Boolean,                             // optional: force TEST mode (default: ?test=1 in the URL)
 *     onPaid: function ({orderId, amount, currency, status, test}) {}
 *   }) -> Promise
 *
 * TEST mode (?test=1 on the page URL): no PayPal, a single simulated "pay" button instead.
 * Every successful payment is sent to recordSale() (sales.js) with the real captured amount.
 */
(function () {
  "use strict";
  if (window.PayKit) return;
  var me = document.currentScript || document.querySelector('script[src*="assets/paykit.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var TEST = new URLSearchParams(location.search).get("test") === "1";

  var T = {
    he: {
      loading: "טוען את אפשרויות התשלום…",
      fail: "לא הצלחנו לטעון את מערכת התשלום. בדקו את החיבור לאינטרנט או כבו חוסם פרסומות לאתר זה.",
      retry: "לנסות שוב", confirming: "מאשרים את התשלום…", cancelled: "התשלום בוטל. אפשר לנסות שוב בכל רגע.",
      error: "משהו השתבש בתשלום ולא בוצע חיוב. נסו שוב.", declined: "אמצעי התשלום נדחה. נסו אמצעי אחר.",
      unavailable: "התשלום אינו זמין כרגע.", testPay: "תשלום בדיקה (TEST)"
    },
    en: {
      loading: "Loading payment options…",
      fail: "Couldn't load the payment system. Check your connection or disable the ad blocker for this site.",
      retry: "Try again", confirming: "Confirming your payment…", cancelled: "Payment cancelled. You can try again any time.",
      error: "Something went wrong and you were not charged. Please try again.", declined: "Your card was declined. Try another payment method.",
      unavailable: "Payment is not available right now.", testPay: "Test payment (TEST)"
    }
  };

  var loaded = {};
  function loadScript(src) {
    if (!loaded[src]) {
      loaded[src] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = src; s.async = true; s.setAttribute("data-site-sdk", "1");
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
  var sdk = null;
  function loadSdk(cfg, currency, locale) {
    if (window.paypal && window.paypal.Buttons) return Promise.resolve(window.paypal);
    if (!sdk) {
      var base = "https://www.paypal.com/sdk/js?client-id=" + encodeURIComponent(cfg.PAYPAL_CLIENT_ID) +
        "&currency=" + currency + "&intent=capture&enable-funding=card&components=buttons";
      sdk = loadScript(base + (locale ? "&locale=" + locale : ""))
        .catch(function () { return loadScript(base); })
        .then(function () {
          if (!window.paypal || !window.paypal.Buttons) throw new Error("paypal sdk missing");
          return window.paypal;
        });
      sdk.catch(function () { sdk = null; });
    }
    return sdk;
  }
  function price2(n) { return (Math.round(Number(n) * 100) / 100).toFixed(2); }
  function msg(holder, kind, text) {
    var box = holder.parentNode || holder;
    var m = box.querySelector(":scope > .pk-msg");
    if (!m) { m = document.createElement("div"); m.setAttribute("role", "status"); box.appendChild(m); }
    m.className = "pk-msg buy-msg " + kind;
    m.textContent = text;
  }
  function amountOf(o) { return Number(typeof o.amount === "function" ? o.amount() : o.amount); }
  function paid(o, info) {
    // record the sale (never block the buyer on it), then hand over to the page
    var done = false, go = function () { if (!done) { done = true; o.onPaid && o.onPaid(info); } };
    var timer = setTimeout(go, 2500);
    sales().then(function () {
      return window.recordSale({ orderId: info.orderId, slug: o.sku, amount: info.amount, currency: info.currency, status: info.status, test: info.test });
    }).catch(function () {}).then(function () { clearTimeout(timer); go(); });
  }

  function render(holder, o) {
    var t = T[o.lang] || T.he;
    var currency = o.currency || "ILS";
    // callers may pass test (captured when they loaded): some tools rewrite the URL and drop ?test=1
    if (o.test != null ? o.test : TEST) {
      holder.innerHTML = "";
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn block accent"; b.setAttribute("data-test-pay", o.sku);
      b.textContent = o.testLabel || t.testPay;
      b.addEventListener("click", function () {
        var err = o.validate ? o.validate() : "";
        if (err) { msg(holder, "error", err); return; }
        b.disabled = true;
        var id = "TEST-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
        paid(o, { orderId: id, amount: amountOf(o), currency: currency, status: "COMPLETED", test: true });
      });
      holder.appendChild(b);
      return Promise.resolve();
    }
    holder.innerHTML = '<div class="buy-loading" role="status"><div class="spinner" aria-hidden="true"></div>' + t.loading + "</div>";
    return config().then(function (cfg) {
      if (!cfg.PAYPAL_CLIENT_ID) throw new Error("no client id");
      return loadSdk(cfg, currency, o.locale).then(function (paypal) {
        holder.innerHTML = "";
        var name = String(o.name || o.sku).slice(0, 127);
        return paypal.Buttons({
          style: { layout: "vertical", shape: "pill", label: "pay", height: 45, tagline: false },
          onClick: function (data, actions) {
            var err = o.validate ? o.validate() : "";
            if (err) { msg(holder, "error", err); return actions.reject(); }
            return actions.resolve();
          },
          createOrder: function (data, actions) {
            var value = price2(amountOf(o));
            return actions.order.create({
              intent: "CAPTURE",
              purchase_units: [{
                reference_id: o.sku, custom_id: o.sku, description: name,
                amount: { currency_code: currency, value: value, breakdown: { item_total: { currency_code: currency, value: value } } },
                items: [{ name: name, sku: o.sku, quantity: "1", category: "DIGITAL_GOODS", unit_amount: { currency_code: currency, value: value } }]
              }],
              application_context: { shipping_preference: "NO_SHIPPING", brand_name: o.brand || cfg.BRAND || "תכנון פלוס", user_action: "PAY_NOW" }
            });
          },
          onApprove: function (data, actions) {
            msg(holder, "info", t.confirming);
            return actions.order.capture().then(function (det) {
              var e = det && det.details && det.details[0];
              if (e && e.issue === "INSTRUMENT_DECLINED") { msg(holder, "error", t.declined); return actions.restart(); }
              var cap = det && det.purchase_units && det.purchase_units[0] && det.purchase_units[0].payments &&
                det.purchase_units[0].payments.captures && det.purchase_units[0].payments.captures[0];
              paid(o, {
                orderId: det.id || data.orderID,
                amount: cap && cap.amount ? Number(cap.amount.value) : amountOf(o),
                currency: cap && cap.amount ? cap.amount.currency_code : currency,
                status: (cap && cap.status) || det.status || "", test: false
              });
            });
          },
          onCancel: function () { msg(holder, "info", t.cancelled); },
          onError: function (e) { if (window.console) console.error("PayPal error", e); msg(holder, "error", t.error); }
        }).render(holder);
      });
    }).catch(function (e) {
      if (window.console) console.error(e);
      holder.innerHTML = '<div class="buy-msg error" role="alert" style="margin-top:0">' + (e && e.message === "no client id" ? t.unavailable : t.fail) + "</div>";
      var r = document.createElement("button");
      r.type = "button"; r.className = "btn block small secondary mt-1"; r.textContent = t.retry;
      r.addEventListener("click", function () { render(holder, o); });
      holder.appendChild(r);
    });
  }

  window.PayKit = { render: render, isTest: TEST, loadScript: loadScript, config: config };
})();
