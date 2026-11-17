/* Glory checkout — renders PayPal buttons into every <div class="buy" data-product="<slug>"></div>.
 *
 * Flow: read data/products/<slug>.json (+ members for bundles) -> PayPal JS SDK (client id from config.js,
 * currency ILS, intent capture) -> createOrder with title/price from the JSON -> onApprove: capture ->
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
 */
(function () {
  "use strict";
  var me = document.currentScript || document.querySelector('script[src*="assets/checkout.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var ROOT = new URL("../", ASSETS).href;
  var params = new URLSearchParams(location.search);
  var TEST = params.get("test") === "1";
  var CURRENCY = "ILS";

  var loaded = {};
  function loadScript(src) {
    if (!loaded[src]) {
      loaded[src] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = src; s.async = true;
        s.setAttribute("data-glory", "1");
        s.onload = function () { resolve(); };
        s.onerror = function () { delete loaded[src]; s.remove(); reject(new Error("load failed")); };
        document.head.appendChild(s);
      });
    }
    return loaded[src];
  }
  function config() {
    if (window.GLORY_CONFIG) return Promise.resolve(window.GLORY_CONFIG);
    return loadScript(ASSETS + "config.js").then(function () { return window.GLORY_CONFIG || {}; });
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
    return !!p && !p.placeholder && ((p.files && p.files.length > 0) || !!p.sheets_copy_url);
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
  function money(n) { return "₪" + (Number(n) % 1 === 0 ? Number(n) : Number(n).toFixed(2)); }
  function price2(n) { return (Math.round(Number(n) * 100) / 100).toFixed(2); }

  function thanksUrl(slug, orderId, test) {
    return ROOT + "thanks/?p=" + encodeURIComponent(slug) + "&o=" + encodeURIComponent(orderId) + (test ? "&test=1" : "");
  }
  function finish(box, slug, orderId, amount, currency, status, test) {
    setMsg(box, "info", "התשלום התקבל! מעבירים אותך לדף ההורדה…");
    var go = function () { location.href = thanksUrl(slug, orderId, test); };
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
    el.innerHTML =
      '<div class="buy-box">' +
      (TEST ? '<div class="test-flag">מצב בדיקה (TEST) — לא יתבצע חיוב</div>' : "") +
      '<div class="buy-head">' +
      (compact ? "" : '<div class="buy-title">' + esc(label) + "</div>") +
      '<div class="buy-price" aria-label="מחיר">' + money(p.price_ils) + "</div></div>" +
      '<div class="buy-buttons"></div>' +
      '<p class="buy-note"><span>תשלום מאובטח ב-PayPal</span><span>אפשר בכרטיס אשראי, בלי חשבון</span><span>הורדה מיידית</span></p>' +
      '<p class="buy-legal">ברכישה הנך מאשר/ת את <a href="' + ROOT + 'legal/terms/">התקנון</a> ואת <a href="' + ROOT + 'legal/refund/">מדיניות הביטולים</a>. המחיר סופי.</p>' +
      "</div>";
    return el.querySelector(".buy-box");
  }

  function renderSoon(el, info) {
    var box = shell(el, info);
    box.querySelector(".buy-buttons").innerHTML =
      '<button type="button" class="btn block" disabled aria-disabled="true">בקרוב — המוצר בהכנה</button>';
    box.querySelector(".buy-note").remove();
    box.querySelector(".buy-legal").remove();
  }

  function renderTest(el, info) {
    var box = shell(el, info);
    var p = info.product;
    var b = document.createElement("button");
    b.type = "button"; b.className = "btn block accent"; b.setAttribute("data-test-pay", p.slug);
    b.textContent = "תשלום בדיקה " + money(p.price_ils) + " (TEST)";
    b.addEventListener("click", function () {
      b.disabled = true;
      var id = "TEST-" + Date.now().toString(36).toUpperCase() + "-" + Math.random().toString(36).slice(2, 6).toUpperCase();
      finish(box, p.slug, id, Number(p.price_ils), CURRENCY, "COMPLETED", true);
    });
    box.querySelector(".buy-buttons").appendChild(b);
  }

  var sdkPromise = null;
  function loadSdk(cfg) {
    if (window.paypal && window.paypal.Buttons) return Promise.resolve(window.paypal);
    if (!sdkPromise) {
      var base = "https://www.paypal.com/sdk/js?client-id=" + encodeURIComponent(cfg.PAYPAL_CLIENT_ID) +
        "&currency=" + CURRENCY + "&intent=capture&components=buttons";
      sdkPromise = loadScript(base + "&locale=he_IL")
        .catch(function () { return loadScript(base); }) // unsupported locale -> retry without it
        .then(function () {
          if (!window.paypal || !window.paypal.Buttons) throw new Error("paypal sdk missing");
          return window.paypal;
        });
      sdkPromise.catch(function () { sdkPromise = null; });
    }
    return sdkPromise;
  }

  function renderPayPal(el, info, cfg) {
    var box = shell(el, info);
    var p = info.product;
    var holder = box.querySelector(".buy-buttons");
    holder.innerHTML = '<div class="spinner" aria-label="טוען אפשרויות תשלום"></div>';
    if (!cfg.PAYPAL_CLIENT_ID) { holder.innerHTML = ""; setMsg(box, "error", "התשלום אינו זמין כרגע. נסו שוב מאוחר יותר."); return; }
    var value = price2(p.price_ils);
    var name = String(p.title || p.slug).slice(0, 127);
    loadSdk(cfg).then(function (paypal) {
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
            application_context: { shipping_preference: "NO_SHIPPING", brand_name: cfg.BRAND || "Glory", user_action: "PAY_NOW" }
          });
        },
        onApprove: function (data, actions) {
          setMsg(box, "info", "מאשרים את התשלום…");
          return actions.order.capture().then(function (det) {
            var err = det && det.details && det.details[0];
            if (err && err.issue === "INSTRUMENT_DECLINED") {
              setMsg(box, "error", "אמצעי התשלום נדחה. נסו אמצעי אחר.");
              return actions.restart();
            }
            var cap = det && det.purchase_units && det.purchase_units[0] && det.purchase_units[0].payments &&
              det.purchase_units[0].payments.captures && det.purchase_units[0].payments.captures[0];
            var amt = cap && cap.amount ? Number(cap.amount.value) : Number(value);
            var cur = cap && cap.amount ? cap.amount.currency_code : CURRENCY;
            var status = (cap && cap.status) || det.status || "";
            finish(box, p.slug, det.id || data.orderID, amt, cur, status, false);
          });
        },
        onCancel: function () { setMsg(box, "info", "התשלום בוטל. אפשר לנסות שוב בכל רגע."); },
        onError: function (e) {
          if (window.console) console.error("PayPal error", e);
          setMsg(box, "error", "משהו השתבש בתשלום ולא בוצע חיוב. רעננו את הדף ונסו שוב.");
        }
      }).render(holder);
    }).catch(function (e) {
      if (window.console) console.error(e);
      holder.innerHTML = "";
      setMsg(box, "error", "לא הצלחנו לטעון את PayPal. ייתכן שחוסם פרסומות מונע זאת — כבו אותו לאתר זה ורעננו.");
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
      el.innerHTML = '<div class="buy-box"><div class="buy-msg error">המוצר לא נמצא.</div></div>';
    });
  }

  function init() {
    config().then(function (cfg) {
      var els = document.querySelectorAll(".buy[data-product]");
      for (var i = 0; i < els.length; i++) renderOne(els[i], cfg);
    });
  }
  window.GloryCheckout = { render: init, resolve: resolve, isTest: TEST };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
