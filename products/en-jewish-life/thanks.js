<script>
(function () {
  "use strict";
  var G = window.SITE, esc = G.escape;
  var q = new URLSearchParams(location.search);
  var slug = q.get("p") || "", order = q.get("o") || "", test = q.get("test") === "1";
  var $ = function (id) { return document.getElementById(id); };
  var FILE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>';
  function fail() { $("loading").hidden = true; $("error").hidden = false; }
  function ext(path) { var m = /\.([a-z0-9]+)(?:$|\?)/i.exec(path || ""); return m ? m[1].toUpperCase() : ""; }
  function fileUrl(path) { return /^https?:\/\//.test(path) ? path : G.url(String(path).replace(/^\/+/, "").replace(/^docs\//, "")); }
  function money(p) {
    var n = Number(p.price != null ? p.price : p.price_ils), c = (p.currency || "ILS").toUpperCase();
    return c === "USD" ? "$" + n.toFixed(2) : c === "ILS" ? "₪" + n : n + " " + c;
  }
  function list(p) {
    var items = (p.files || []).map(function (f) {
      return '<li><a class="dl" href="' + esc(fileUrl(f.path)) + '" download><span class="ic">' + FILE + "</span><span>" + esc(f.label) + '</span><span class="ext">' + esc(ext(f.path)) + "</span></a></li>";
    });
    if (p.sheets_copy_url) items.push('<li><a class="dl sheets" href="' + esc(p.sheets_copy_url) + '" target="_blank" rel="noopener"><span class="ic">' + FILE + '</span><span>Make a copy in Google Sheets</span><span class="ext">SHEETS</span></a></li>');
    if (!items.length) return '<p class="callout warn">The files for this product are still being prepared. Email us your order number and we will send them as soon as they are ready, or refund you.</p>';
    return '<ul class="downloads">' + items.join("") + "</ul>";
  }
  if (!/^[a-z0-9-]+$/.test(slug) || !order || order.length > 64) return fail();
  Promise.all([G.getJSON("data/products/" + slug + ".json"), G.config()]).then(function (r) {
    var p = r[0], cfg = r[1];
    return Promise.all((p.bundle_of || []).map(function (s) { return G.getJSON("data/products/" + s + ".json").catch(function () { return null; }); }))
      .then(function (ms) { return { p: p, ms: ms.filter(Boolean), cfg: cfg }; });
  }).then(function (d) {
    var p = d.p, cfg = d.cfg;
    document.title = "Thank you! Download " + p.title + " | Tichnun Plus";
    $("downloads").innerHTML = d.ms.length
      ? d.ms.map(function (m) { return '<h3 class="mt-2">' + esc(m.title) + "</h3>" + list(m); }).join("")
      : list(p);
    $("r-title").textContent = p.title;
    $("r-price").textContent = money(p);
    $("r-order").textContent = order;
    $("r-date").textContent = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    $("test-flag").hidden = !test;
    var email = cfg.SELLER_EMAIL && cfg.SELLER_EMAIL !== "SELLER_EMAIL" ? cfg.SELLER_EMAIL : "";
    if (email) {
      $("support").innerHTML = 'File won\'t open, or something isn\'t clear? Email <a href="mailto:' + esc(email) + "?subject=" +
        encodeURIComponent("Help with order " + order) + '">' + esc(email) + '</a> with your order number and we\'ll help. See our <a href="' +
        G.url("en/legal/refund/") + '">refund policy</a>.';
    }
    $("loading").hidden = true; $("ok").hidden = false;
    try {
      var k = "tp-orders", arr = JSON.parse(localStorage.getItem(k) || "[]");
      if (!arr.some(function (x) { return x.o === order; })) { arr.push({ p: slug, o: order, t: Date.now(), test: test }); localStorage.setItem(k, JSON.stringify(arr.slice(-30))); }
    } catch (e) {}
  }).catch(fail);
  $("copy-link").addEventListener("click", function () {
    var b = this, done = function () { b.textContent = "Link copied ✓"; };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, function () { prompt("Copy this link:", location.href); });
    else prompt("Copy this link:", location.href);
  });
  $("print").addEventListener("click", function () { window.print(); });
})();
</script>
