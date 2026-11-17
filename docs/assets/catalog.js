/* תכנון פלוס catalogue renderer (needs site.js loaded first).
 * Fills containers from data/products/index.json, data/products/<slug>.json and data/tools.json:
 *   <div class="grid cols-3" data-catalog="products" [data-category="events"] [data-limit="3"] [data-exclude="slug"]></div>
 *   <div class="grid cols-2" data-catalog="bundles"></div>   (buy boxes; load checkout.js on the page)
 *   <div class="grid cols-3" data-catalog="tools" [data-limit="3"]></div>
 * tools/site/build_site.py pre-renders the same markup into the HTML for crawlers; this script refreshes it live.
 * Markup must stay in sync with tools/site/build_site.py.
 */
(function () {
  "use strict";
  var G = window.SITE;
  if (!G) return;
  var esc = G.escape;

  var ICONS = {
    events: '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="30" r="10"/><circle cx="30" cy="30" r="10"/><path d="M20 12l4-5 4 5-4 4z"/></svg>',
    money: '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="13" width="36" height="25" rx="4"/><path d="M6 20h36M32 29h4"/><path d="M12 13l18-6 3 6"/></svg>',
    business: '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="15" width="36" height="24" rx="4"/><path d="M18 15v-4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4M6 25h36M22 25v3h4v-3"/></svg>',
    bundle: '<svg class="icon" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="18" width="34" height="22" rx="3"/><path d="M5 12h38v6H5zM24 12v28M24 12c-3-6-11-6-10 0M24 12c3-6 11-6 10 0"/></svg>'
  };

  var exists = {};
  function pageExists(url) {
    if (!(url in exists)) {
      exists[url] = fetch(url, { method: "HEAD", cache: "no-cache" }).then(function (r) { return r.ok; }, function () { return false; });
    }
    return exists[url];
  }
  function load() {
    return Promise.all([G.getJSON("data/products/index.json"), G.getJSON("data/tools.json").catch(function () { return { tools: [] }; })]);
  }
  function product(slug) { return G.getJSON("data/products/" + slug + ".json").catch(function () { return null; }); }
  function deliverable(p) { return !!p && !p.placeholder && ((p.files && p.files.length) || !!p.sheets_copy_url); }

  function productCard(p, cat, catLabel, live) {
    var url = G.productUrl(p.slug);
    var soon = !live;
    var thumb = p.image
      ? '<img src="' + esc(G.url(p.image)) + '" alt="" loading="lazy" width="640" height="360">'
      : ICONS[cat] || ICONS.money;
    return '<article class="card product-card' + (soon ? " is-soon" : "") + '" data-slug="' + esc(p.slug) + '">' +
      '<div class="thumb ' + esc(cat) + '">' + thumb + "</div>" +
      '<div class="body">' +
      (catLabel ? '<span class="badge">' + esc(catLabel) + "</span>" : "") +
      "<h3>" + (soon ? esc(p.title) : '<a href="' + url + '">' + esc(p.title) + "</a>") + "</h3>" +
      '<p class="sub">' + esc(p.subtitle || "") + "</p>" +
      '<div class="meta"><span class="price">' + G.formatILS(p.price_ils) + "</span>" +
      (soon ? '<span class="badge soon">בקרוב</span>' : '<span class="badge accent">אקסל + Google Sheets</span>') +
      "</div></div></article>";
  }

  function bundleCard(b, members) {
    var sum = members.reduce(function (s, m) { return s + (m ? Number(m.price_ils) || 0 : 0); }, 0);
    var save = sum - Number(b.price_ils);
    var list = members.map(function (m, i) {
      var title = m ? m.title : b.bundle_of[i];
      return "<li>" + esc(title) + (m ? ' <span class="muted num">(' + G.formatILS(m.price_ils) + ")</span>" : "") + "</li>";
    }).join("");
    return '<article class="card pad-lg" id="' + esc(b.slug) + '" data-slug="' + esc(b.slug) + '">' +
      '<div class="btn-row" style="justify-content:space-between;align-items:center">' +
      "<h3 class=\"mb-0\">" + esc(b.title) + "</h3>" +
      (save > 0 ? '<span class="badge success">חוסכים ' + G.formatILS(save) + "</span>" : "") + "</div>" +
      '<p class="muted mt-1">' + esc(b.subtitle || "") + "</p>" +
      '<ul class="small">' + list + "</ul>" +
      (save > 0 ? '<p class="small muted">במקום <s class="num">' + G.formatILS(sum) + "</s> בנפרד</p>" : "") +
      '<div class="buy" data-product="' + esc(b.slug) + '" data-compact="1"></div>' +
      "</article>";
  }

  function toolCard(t, live) {
    var inner = '<span class="ic" aria-hidden="true">' + esc(t.icon || "🧮") + "</span><div><h3>" + esc(t.title) + "</h3><p>" +
      esc(t.description || "") + "</p>" + (live ? "" : '<span class="badge soon mt-1">בקרוב</span>') + "</div>";
    return live
      ? '<a class="card tool-card" href="' + G.toolUrl(t.slug) + '" data-slug="' + esc(t.slug) + '">' + inner + "</a>"
      : '<div class="card tool-card" data-slug="' + esc(t.slug) + '">' + inner + "</div>";
  }

  function limit(list, el) {
    var ex = (el.getAttribute("data-exclude") || "").split(",").filter(Boolean);
    list = list.filter(function (x) { return ex.indexOf(x.slug) < 0; });
    var n = parseInt(el.getAttribute("data-limit") || "0", 10);
    return n > 0 ? list.slice(0, n) : list;
  }

  function renderProducts(el, idx) {
    var cat = el.getAttribute("data-category");
    var items = limit(idx.products.filter(function (x) { return !cat || x.category === cat; }), el);
    return Promise.all(items.map(function (x) {
      return product(x.slug).then(function (p) {
        if (!p) return "";
        return pageExists(G.productUrl(p.slug)).then(function (ok) {
          return productCard(p, x.category, cat ? "" : (idx.categories || {})[x.category], ok && !p.placeholder);
        });
      });
    })).then(function (html) { el.innerHTML = html.join(""); });
  }

  function renderBundles(el, idx) {
    return Promise.all(limit(idx.bundles.map(function (s) { return { slug: s }; }), el).map(function (x) {
      return product(x.slug).then(function (b) {
        if (!b) return "";
        return Promise.all((b.bundle_of || []).map(product)).then(function (ms) { return bundleCard(b, ms); });
      });
    })).then(function (html) {
      el.innerHTML = html.join("");
      if (window.SiteCheckout) window.SiteCheckout.render();
    });
  }

  function renderTools(el, tools) {
    return Promise.all(limit(tools.tools || [], el).map(function (t) {
      return pageExists(G.toolUrl(t.slug)).then(function (ok) { return toolCard(t, ok); });
    })).then(function (html) { el.innerHTML = html.join(""); });
  }

  function init() {
    var els = document.querySelectorAll("[data-catalog]");
    if (!els.length) return;
    load().then(function (r) {
      var idx = r[0], tools = r[1];
      Array.prototype.forEach.call(els, function (el) {
        var kind = el.getAttribute("data-catalog");
        // Pre-rendered bundle cards already hold live PayPal boxes: don't re-render them (avoids loading buttons twice).
        if (kind === "bundles" && el.querySelector(".buy")) return;
        var p = kind === "products" ? renderProducts(el, idx) : kind === "bundles" ? renderBundles(el, idx) : kind === "tools" ? renderTools(el, tools) : null;
        if (p) p.then(function () { el.setAttribute("data-rendered", "1"); }, function (e) { if (window.console) console.error(e); });
      });
    }).catch(function (e) { if (window.console) console.error("catalog", e); });
  }
  G.catalog = { render: init, deliverable: deliverable };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
