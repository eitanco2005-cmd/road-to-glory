/* Glory sales log + visit counter client.
 * recordSale({orderId, slug, amount, currency, test}) -> POST JSON to GLORY_CONFIG.SALES_ENDPOINT
 * recordVisit(path)                                   -> POST JSON to GLORY_CONFIG.VISITS_ENDPOINT
 * Empty endpoint = no-op. Requests use Content-Type text/plain so no CORS preflight is needed.
 * A sale that fails to send is queued in localStorage and retried on the next page load (flushPendingSales).
 * No cookies, no personal data: only order id, product, amount, path, referrer host, coarse device class.
 */
(function () {
  "use strict";
  var PENDING_KEY = "glory-pending-sales";

  function cfg() { return window.GLORY_CONFIG || {}; }
  function endpoint(name) {
    var u = (cfg()[name] || "").trim();
    return u || "";
  }
  function post(url, data, beacon) {
    if (!url) return Promise.resolve(false);
    var body = JSON.stringify(data);
    if (beacon && navigator.sendBeacon) {
      try {
        if (navigator.sendBeacon(url, new Blob([body], { type: "text/plain;charset=UTF-8" }))) return Promise.resolve(true);
      } catch (e) {}
    }
    try {
      return fetch(url, {
        method: "POST", body: body, mode: "cors", keepalive: true, credentials: "omit",
        headers: { "Content-Type": "text/plain;charset=UTF-8" }
      }).then(function (r) { return r.ok; }, function () { return false; });
    } catch (e) {
      return Promise.resolve(false);
    }
  }
  function readPending() {
    try { return JSON.parse(localStorage.getItem(PENDING_KEY) || "[]") || []; } catch (e) { return []; }
  }
  function writePending(list) {
    try {
      if (list.length) localStorage.setItem(PENDING_KEY, JSON.stringify(list.slice(-20)));
      else localStorage.removeItem(PENDING_KEY);
    } catch (e) {}
  }
  function deviceClass() {
    var w = window.innerWidth || 0;
    return w < 600 ? "mobile" : w < 1024 ? "tablet" : "desktop";
  }
  function refHost() {
    try {
      if (!document.referrer) return "";
      var h = new URL(document.referrer).host;
      return h === location.host ? "" : h;
    } catch (e) { return ""; }
  }

  window.recordSale = function (s) {
    s = s || {};
    var data = {
      type: "sale",
      orderId: String(s.orderId || ""),
      slug: String(s.slug || ""),
      amount: Number(s.amount) || 0,
      currency: String(s.currency || cfg().CURRENCY || "ILS"),
      test: !!s.test,
      status: s.status || "",
      ts: new Date().toISOString(),
      page: location.pathname
    };
    var url = endpoint("SALES_ENDPOINT");
    if (!url) return Promise.resolve(false);
    return post(url, data).then(function (ok) {
      if (!ok) { var p = readPending(); p.push(data); writePending(p); }
      return ok;
    });
  };

  window.flushPendingSales = function () {
    var url = endpoint("SALES_ENDPOINT");
    var list = readPending();
    if (!url || !list.length) return Promise.resolve(0);
    writePending([]);
    return Promise.all(list.map(function (d) {
      return post(url, d).then(function (ok) { return ok ? null : d; });
    })).then(function (res) {
      var failed = res.filter(Boolean);
      if (failed.length) writePending(readPending().concat(failed));
      return list.length - failed.length;
    });
  };

  window.recordVisit = function (path) {
    var url = endpoint("VISITS_ENDPOINT");
    if (!url) return Promise.resolve(false);
    var p = String(path || location.pathname);
    try { // one count per page per browser session
      var key = "glory-v:" + p;
      if (sessionStorage.getItem(key)) return Promise.resolve(false);
      sessionStorage.setItem(key, "1");
    } catch (e) {}
    return post(url, {
      type: "visit",
      path: p,
      ref: refHost(),
      device: deviceClass(),
      lang: (navigator.language || "").slice(0, 5),
      ts: new Date().toISOString()
    }, true);
  };
})();
