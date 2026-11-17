/*! RTL Landing Kit v1.0 — MIT License
 * Tiny helper (no dependencies, ~1 KB):
 *  - Language switch: <select data-lang-switch> + a <script type="application/json" id="i18n">{"he":{…},"ar":{…},"en":{…}}</script>
 *    Elements with data-i18n="key" get their text replaced; data-i18n-attr="placeholder:key,aria-label:key" sets attributes.
 *    <html lang> and <html dir> are updated (he/ar = rtl, everything else = ltr). Choice is kept in the URL (?lang=ar).
 *  - Mobile menu: <button data-menu> toggles [data-open] on the closest .nav.
 *  - Demo forms: <form data-demo> shows its [data-ok] message instead of submitting (replace with your backend).
 * Delete what you don't need — the CSS works without any JavaScript.
 */
(function () {
  "use strict";
  var RTL = { he: 1, ar: 1, fa: 1, ur: 1 };
  var dataEl = document.getElementById("i18n");
  var dict = {};
  try { dict = dataEl ? JSON.parse(dataEl.textContent) : {}; } catch (e) {}

  function setLang(lang) {
    if (!dict[lang]) return;
    var t = dict[lang], root = document.documentElement;
    root.lang = lang;
    root.dir = RTL[lang] ? "rtl" : "ltr";
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var k = el.getAttribute("data-i18n");
      if (t[k] != null) el.innerHTML = t[k];
    });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr").split(",").forEach(function (pair) {
        var p = pair.split(":");
        if (t[p[1]] != null) el.setAttribute(p[0].trim(), t[p[1]]);
      });
    });
    if (t._title) document.title = t._title;
    document.querySelectorAll("[data-lang-switch]").forEach(function (s) { s.value = lang; });
    try {
      var u = new URL(location.href);
      if (lang === (dataEl && dataEl.getAttribute("data-default"))) u.searchParams.delete("lang"); else u.searchParams.set("lang", lang);
      history.replaceState(null, "", u);
    } catch (e) {}
  }

  document.querySelectorAll("[data-lang-switch]").forEach(function (s) {
    s.addEventListener("change", function () { setLang(s.value); });
  });
  var q = new URLSearchParams(location.search).get("lang");
  if (q && dict[q]) setLang(q);

  document.querySelectorAll("[data-menu]").forEach(function (b) {
    b.addEventListener("click", function () {
      var nav = b.closest(".nav");
      var open = nav.hasAttribute("data-open");
      if (open) nav.removeAttribute("data-open"); else nav.setAttribute("data-open", "");
      b.setAttribute("aria-expanded", String(!open));
    });
  });
  document.querySelectorAll(".nav-links a").forEach(function (a) {
    a.addEventListener("click", function () { var n = a.closest(".nav"); if (n) n.removeAttribute("data-open"); });
  });

  document.querySelectorAll("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = f.querySelector("[data-ok]") || f.parentNode.querySelector("[data-ok]");
      if (ok) { ok.hidden = false; ok.focus && ok.focus(); }
      f.reset();
    });
  });

  window.RTLKit = { setLang: setLang };
})();
