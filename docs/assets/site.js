/* תכנון פלוס (Tichnun Plus) shared site script.
 * - Injects header/nav into <header id="site-header"> and footer into <footer id="site-footer">
 * - Ensures the Hebrew font + favicon are linked
 * - Light/dark theme toggle (remembered per browser)
 * - Records a privacy-friendly page visit (no cookies) via sales.js -> VISITS_ENDPOINT
 * - Exposes window.SITE helpers: root, url(), loadScript(), getJSON(), config(), formatILS(), productUrl(), toolUrl()
 * - English pages (<html lang="en">, under en/) get an English LTR header/footer. Every header has a language
 *   switch: it follows <link rel="alternate" hreflang="he|en"> when the page declares one, else the other home page.
 * All URLs are derived from this script's own location, so the site works on any host / sub-path.
 */
(function () {
  "use strict";
  // Old GitHub Pages address -> permanent home on Netlify (keeps path + query).
  if (/\.github\.io$/.test(location.hostname)) {
    var rest = location.pathname.replace(/^\/road-to-glory/, "") || "/";
    location.replace("https://tichnun.netlify.app" + rest + location.search + location.hash);
    return;
  }
  var me = document.currentScript || document.querySelector('script[src*="assets/site.js"]');
  var ASSETS = new URL(".", me ? me.src : location.href).href;
  var ROOT = new URL("../", ASSETS).href;

  var EN = /^en/i.test(document.documentElement.getAttribute("lang") || "");
  var BRAND = EN ? "Tichnun Plus" : "תכנון פלוס";
  var G = (window.SITE = window.SITE || {});
  G.lang = EN ? "en" : "he";
  G.root = ROOT;
  G.assets = ASSETS;
  G.url = function (p) { return new URL(p || "", ROOT).href; };

  var scripts = G._scripts || (G._scripts = {});
  G.loadScript = function (src) {
    var abs = new URL(src, ASSETS).href;
    if (!scripts[abs]) {
      scripts[abs] = new Promise(function (resolve, reject) {
        var s = document.createElement("script");
        s.src = abs; s.async = true;
        s.onload = function () { resolve(); };
        s.onerror = function () { delete scripts[abs]; reject(new Error("load failed: " + abs)); };
        document.head.appendChild(s);
      });
    }
    return scripts[abs];
  };
  var json = G._json || (G._json = {});
  G.getJSON = function (path) {
    var abs = new URL(path, ROOT).href;
    if (!json[abs]) {
      json[abs] = fetch(abs, { cache: "no-cache" }).then(function (r) {
        if (!r.ok) throw new Error(r.status + " " + abs);
        return r.json();
      });
    }
    return json[abs];
  };
  G.config = function () {
    if (window.SITE_CONFIG) return Promise.resolve(window.SITE_CONFIG);
    return G.loadScript("config.js").then(function () { return window.SITE_CONFIG || {}; });
  };
  G.formatILS = function (n) {
    var v = Number(n) || 0;
    var s = v % 1 === 0 ? v.toLocaleString("he-IL") : v.toLocaleString("he-IL", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return "₪" + s;
  };
  G.productUrl = function (slug) { return G.url("p/" + slug + "/"); };
  G.toolUrl = function (slug) { return G.url("tools/" + slug + "/"); };
  G.escape = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };

  /* ---------- head: font + favicon ---------- */
  function ensureHead() {
    var head = document.head;
    if (!document.querySelector('link[href*="fonts.googleapis.com"]')) {
      [["preconnect", "https://fonts.googleapis.com"], ["preconnect", "https://fonts.gstatic.com"]].forEach(function (x) {
        var l = document.createElement("link"); l.rel = x[0]; l.href = x[1]; if (x[1].indexOf("gstatic") > 0) l.crossOrigin = "";
        head.appendChild(l);
      });
      var f = document.createElement("link");
      f.rel = "stylesheet";
      f.href = "https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&display=swap";
      head.appendChild(f);
    }
    if (!document.querySelector('link[rel="icon"]')) {
      var i = document.createElement("link"); i.rel = "icon"; i.type = "image/svg+xml"; i.href = ASSETS + "favicon.svg";
      head.appendChild(i);
    }
  }

  /* ---------- theme ---------- */
  var THEME_KEY = "tp-theme";
  function storedTheme() { try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; } }
  function applyTheme(t) {
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    else document.documentElement.removeAttribute("data-theme");
  }
  applyTheme(storedTheme());
  function currentTheme() {
    var t = document.documentElement.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/></svg>';

  /* ---------- header / footer ---------- */
  var LOGO = '<svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="14" fill="#0e6b63"/><path d="M32 12l5.6 12.4 13.4 1.4-10 9.1 2.8 13.2L32 41.4l-11.8 6.7 2.8-13.2-10-9.1 13.4-1.4z" fill="#f0b44c"/></svg>';

  function navLink(href, label) {
    var here = location.href.split(/[?#]/)[0];
    var abs = G.url(href);
    var current = href === "" ? (here === abs || here === abs + "index.html") : here.indexOf(abs) === 0;
    return '<a href="' + abs + '"' + (current ? ' aria-current="page"' : "") + ">" + label + "</a>";
  }

  function altLang() {
    var want = EN ? "he" : "en";
    var l = document.querySelector('link[rel="alternate"][hreflang="' + want + '"]');
    var href = l ? l.getAttribute("href") : G.url(EN ? "" : "en/");
    try { // keep the switch on this host (canonical alternates point at the production domain)
      var u = new URL(href, location.href);
      if (u.host !== location.host) href = G.url(u.pathname.replace(/^\/+/, ""));
    } catch (e) {}
    return EN
      ? '<a class="lang-switch" href="' + href + '" hreflang="he" lang="he" title="לאתר בעברית" aria-label="עברית"><span class="full">עברית</span><span class="short" aria-hidden="true">עב</span></a>'
      : '<a class="lang-switch" href="' + href + '" hreflang="en" lang="en" title="English site" aria-label="English"><span class="full">English</span><span class="short" aria-hidden="true">EN</span></a>';
  }

  function renderHeaderEn(el) {
    el.innerHTML =
      '<a class="skip-link" href="#main">Skip to content</a>' +
      '<div class="container bar">' +
      '<a class="brand" href="' + G.url("en/") + '" aria-label="' + BRAND + ' home">' + LOGO + '<span>' + BRAND + '</span><small>Jewish-life planners</small></a>' +
      '<nav class="nav" aria-label="Main">' +
      navLink("en/planners/", "Planners") + navLink("en/tools/", "Free tools") + navLink("en/guides/", "Guides") +
      "</nav>" + altLang() +
      '<button type="button" class="theme-toggle" aria-label="Toggle light/dark mode"></button>' +
      "</div>";
  }

  function renderHeader() {
    var el = document.getElementById("site-header");
    if (!el || el.getAttribute("data-rendered")) return;
    el.classList.add("site-header");
    el.setAttribute("data-rendered", "1");
    if (EN) renderHeaderEn(el); else el.innerHTML =
      '<a class="skip-link" href="#main">דילוג לתוכן</a>' +
      '<div class="container bar">' +
      '<a class="brand" href="' + G.url("") + '" aria-label="' + BRAND + ' — דף הבית">' + LOGO + '<span>' + BRAND + '</span><small>קבצים ומחשבונים חכמים</small></a>' +
      '<nav class="nav" aria-label="ניווט ראשי">' +
      navLink("chatuna/", "חתונה") + navLink("products/", "מוצרים") + navLink("tools/", "כלים חינם") + navLink("guides/", "מדריכים") +
      "</nav>" + altLang() +
      '<button type="button" class="theme-toggle" aria-label="החלפת מצב תצוגה בהיר/כהה"></button>' +
      "</div>";
    var btn = el.querySelector(".theme-toggle");
    function paint() { btn.innerHTML = currentTheme() === "dark" ? SUN : MOON; }
    paint();
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      paint();
    });
    var main = document.querySelector("main");
    if (main && !main.id) main.id = "main";
  }

  function footerEn(email, year) {
    var u = function (p) { return G.url("en/" + p); };
    return '<div class="container">' +
      '<div class="cols">' +
      "<div><a class=\"brand\" href=\"" + u("") + "\">" + LOGO + "<span>" + BRAND + "</span></a>" +
      '<p class="muted small mt-1">Ready-made Excel and Google Sheets planners for bar and bat mitzvahs, Jewish weddings, Passover and the holidays. Secure PayPal checkout, instant download.</p></div>' +
      "<div><h2 class=\"footer-h\">Planners</h2><ul>" +
      '<li><a href="' + u("p/bar-mitzvah-planner/") + '">Bar/Bat Mitzvah Planner</a></li>' +
      '<li><a href="' + u("p/jewish-wedding-planner/") + '">Jewish Wedding Planner</a></li>' +
      '<li><a href="' + u("p/passover-seder-planner/") + '">Passover Seder Planner</a></li>' +
      '<li><a href="' + u("p/jewish-holiday-planner/") + '">Holiday Hosting Planner</a></li>' +
      '<li><a href="' + u("planners/") + '">All planners &amp; bundle</a></li>' +
      "</ul></div>" +
      "<div><h2 class=\"footer-h\">Free tools</h2><ul>" +
      '<li><a href="' + u("tools/bar-mitzvah-gift/") + '">Bar mitzvah gift calculator</a></li>' +
      '<li><a href="' + u("tools/bar-mitzvah-budget/") + '">Bar mitzvah budget calculator</a></li>' +
      '<li><a href="' + u("tools/seder-shopping-calculator/") + '">Seder shopping calculator</a></li>' +
      '<li><a href="' + u("guides/") + '">Guides</a></li>' +
      "</ul></div>" +
      "<div><h2 class=\"footer-h\">Info</h2><ul>" +
      '<li><a href="' + u("legal/terms/") + '">Terms of sale</a></li>' +
      '<li><a href="' + u("legal/refund/") + '">Refund policy</a></li>' +
      '<li><a href="' + u("legal/privacy/") + '">Privacy policy</a></li>' +
      (email ? '<li><a href="mailto:' + G.escape(email) + '">Contact us</a></li>' : "") +
      '<li><a href="' + G.url("") + '" lang="he" hreflang="he">אתר בעברית</a></li>' +
      "</ul></div>" +
      "</div>" +
      '<p class="fine">© ' + year + " " + BRAND + ". General information only, not financial, legal or religious advice; ask your rabbi about customs. Payments are processed by PayPal; we never see or store card details.</p>" +
      "</div>";
  }

  function renderFooter(cfg) {
    var el = document.getElementById("site-footer");
    if (!el || el.getAttribute("data-rendered")) return;
    el.classList.add("site-footer");
    el.setAttribute("data-rendered", "1");
    var email = cfg && cfg.SELLER_EMAIL && cfg.SELLER_EMAIL !== "SELLER_EMAIL" ? cfg.SELLER_EMAIL : "";
    var year = new Date().getFullYear();
    if (EN) { el.innerHTML = footerEn(email, year); return; }
    el.innerHTML =
      '<div class="container">' +
      '<div class="cols">' +
      "<div><a class=\"brand\" href=\"" + G.url("") + "\">" + LOGO + "<span>" + BRAND + "</span></a>" +
      '<p class="muted small mt-1">כלים בעברית לחתונה: לאורחים (כמה לשים, איך לתת) ולזוגות (תקציב, אישורי הגעה, הושבה והזמנות). תשלום מאובטח ב-PayPal.</p></div>' +
      "<div><h2 class=\"footer-h\">חתונה</h2><ul>" +
      '<li><a href="' + G.url("chatuna/") + '">הכל לחתונה</a></li>' +
      '<li><a href="' + G.toolUrl("wedding-gift") + '">כמה לשים בחתונה</a></li>' +
      '<li><a href="' + G.toolUrl("wedding-cost") + '">כמה עולה חתונה</a></li>' +
      '<li><a href="' + G.toolUrl("wedding-timeline") + '">לוח זמנים לחתונה</a></li>' +
      '<li><a href="' + G.url("apps/rsvp/") + '">רשימת מוזמנים ואישורי הגעה</a></li>' +
      '<li><a href="' + G.url("apps/seating/") + '">סידורי הושבה</a></li>' +
      '<li><a href="' + G.productUrl("wedding-planner") + '">מתכנן חתונה באקסל</a></li>' +
      "</ul></div>" +
      "<div><h2 class=\"footer-h\">עוד באתר</h2><ul>" +
      '<li><a href="' + G.url("products/") + '">כל המוצרים והחבילות</a></li>' +
      '<li><a href="' + G.url("tools/") + '">כל המחשבונים</a></li>' +
      '<li><a href="' + G.url("guides/") + '">מדריכים</a></li>' +
      '<li><a href="' + G.productUrl("household-budget") + '">תקציב משק בית</a></li>' +
      '<li><a href="' + G.productUrl("osek-patur-tracker") + '">מעקב עוסק פטור</a></li>' +
      "</ul></div>" +
      "<div><h2 class=\"footer-h\">מידע</h2><ul>" +
      '<li><a href="' + G.url("legal/terms/") + '">תקנון ותנאי מכירה</a></li>' +
      '<li><a href="' + G.url("legal/refund/") + '">מדיניות ביטולים והחזרים</a></li>' +
      '<li><a href="' + G.url("legal/privacy/") + '">מדיניות פרטיות</a></li>' +
      '<li><a href="' + G.url("legal/accessibility/") + '">הצהרת נגישות</a></li>' +
      (email ? '<li><a href="mailto:' + G.escape(email) + '">צור קשר</a></li>' : "") +
      "</ul></div>" +
      "</div>" +
      '<p class="fine">© ' + year + " " + BRAND + ". המידע באתר הוא כללי ואינו מהווה ייעוץ מס, משפטי או פיננסי. התשלום מתבצע דרך PayPal; איננו שומרים פרטי כרטיס אשראי.</p>" +
      "</div>";
  }

  /* ---------- visits ---------- */
  function recordVisit() {
    G.config().then(function () {
      return G.loadScript("sales.js");
    }).then(function () {
      if (window.flushPendingSales) window.flushPendingSales();
      if (window.recordVisit) window.recordVisit(location.pathname);
    }).catch(function () {});
  }

  /* ---------- a11y: wide tables scroll horizontally, so make the scroll box keyboard-reachable ---------- */
  function a11yTables() {
    var w = document.querySelectorAll(".table-wrap");
    var seen = {};
    for (var i = 0; i < w.length; i++) {
      if (!w[i].hasAttribute("tabindex")) w[i].setAttribute("tabindex", "0");
      if (!w[i].hasAttribute("role")) {
        // label each table by its caption or nearest preceding heading so landmarks stay unique
        var cap = w[i].querySelector("caption"), h = null, el = w[i];
        while (el && !h) { el = el.previousElementSibling || el.parentElement; if (el && /^H[2-4]$/.test(el.tagName)) h = el; }
        var label = (cap && cap.textContent) || (h && h.textContent) || "";
        w[i].setAttribute("role", "region");
        label = (EN ? "Table" : "טבלה") + (label ? ": " + label.trim() : "");
        if (seen[label]) label += " " + (i + 1);
        seen[label] = 1;
        w[i].setAttribute("aria-label", label);
      }
    }
  }

  /* ---------- optional features: tip jar on free tools, upsells on product + thanks pages ---------- */
  function features() {
    var path = location.pathname;
    if ((document.documentElement.lang || "he").slice(0, 2) !== "he") return; // Hebrew site only (not /en/, devkit)
    if (/\/tools\/[a-z0-9-]+\/(?:index\.html)?$/.test(path)) G.loadScript("tip.js").catch(function () {});
    if (/\/p\/[a-z0-9-]+\/(?:index\.html)?$/.test(path) || /\/thanks\/(?:index\.html)?$/.test(path)) G.loadScript("upsell.js").catch(function () {});
  }

  function init() {
    ensureHead();
    features();
    a11yTables();
    renderHeader();
    G.config().then(renderFooter, function () { renderFooter({}); });
    recordVisit();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
