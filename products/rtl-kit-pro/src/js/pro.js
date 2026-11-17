/*! RTL Landing Kit Pro v1.0 — interactions (no dependencies). Every widget is opt-in via data-attributes.
 *  [data-dropdown]            toggles [data-open] on click, closes on Escape / outside click
 *  [data-drawer-open="id"]    opens off-canvas #id (+ .scrim), [data-drawer-close] closes
 *  [role=tablist]             accessible tabs (arrow keys follow the reading direction)
 *  [data-billing]             pricing toggle: buttons [data-period], prices [data-monthly][data-yearly]
 *  form[data-steps]           multi-step form: fieldsets [data-step], buttons [data-next]/[data-prev]
 *  [data-qty]                 − / + quantity stepper
 *  [data-modal-open="id"]     opens <dialog id>, [data-toast="text"] shows a toast
 *  [data-dir-toggle]          flips the page between RTL and LTR (handy while building)
 *  form[data-demo]            shows [data-ok] instead of submitting
 */
(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var rtl = function () { return document.documentElement.dir === "rtl"; };

  // dropdowns
  $$("[data-dropdown]").forEach(function (d) {
    var b = d.querySelector("button");
    b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = d.hasAttribute("data-open");
      $$("[data-dropdown][data-open]").forEach(function (x) { x.removeAttribute("data-open"); x.querySelector("button").setAttribute("aria-expanded", "false"); });
      if (!open) { d.setAttribute("data-open", ""); b.setAttribute("aria-expanded", "true"); }
    });
  });
  document.addEventListener("click", function () { $$("[data-dropdown][data-open]").forEach(function (x) { x.removeAttribute("data-open"); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    $$("[data-dropdown][data-open], .drawer[data-open], .app-side[data-open], .scrim[data-open]").forEach(function (x) { x.removeAttribute("data-open"); });
  });

  // drawers (also the dashboard sidebar on mobile)
  $$("[data-drawer-open]").forEach(function (b) {
    b.addEventListener("click", function () {
      var d = document.getElementById(b.getAttribute("data-drawer-open"));
      if (!d) return;
      d.setAttribute("data-open", "");
      $$(".scrim").forEach(function (s) { s.setAttribute("data-open", ""); });
      var f = d.querySelector("a, button"); if (f) f.focus();
    });
  });
  $$("[data-drawer-close], .scrim").forEach(function (b) {
    b.addEventListener("click", function () { $$(".drawer, .app-side, .scrim").forEach(function (x) { x.removeAttribute("data-open"); }); });
  });

  // tabs
  $$("[role=tablist]").forEach(function (list) {
    var tabs = $$("[role=tab]", list);
    function select(t) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1;
        var p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on;
      });
      t.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var next = rtl() ? "ArrowLeft" : "ArrowRight", prev = rtl() ? "ArrowRight" : "ArrowLeft";
        if (e.key === next) select(tabs[(i + 1) % tabs.length]);
        if (e.key === prev) select(tabs[(i - 1 + tabs.length) % tabs.length]);
      });
    });
  });

  // billing toggle
  $$("[data-billing]").forEach(function (box) {
    var btns = $$("[data-period]", box);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.getAttribute("data-period");
        btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        $$("[data-monthly]", box).forEach(function (el) { el.textContent = el.getAttribute("data-" + p); });
      });
    });
  });

  // multi-step forms
  $$("form[data-steps]").forEach(function (f) {
    var steps = $$("[data-step]", f), bar = $$(".steps-bar li", f), i = 0;
    function show(n, quiet) {
      i = n;
      steps.forEach(function (s, k) { s.hidden = k !== n; });
      bar.forEach(function (b, k) { b.classList.toggle("done", k < n); if (k === n) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current"); });
      if (quiet) return; // no focus (and no scroll jump) on page load
      var first = steps[n].querySelector("input, select, textarea"); if (first) first.focus();
    }
    $$("[data-next]", f).forEach(function (b) {
      b.addEventListener("click", function () {
        var bad = $$("input, select, textarea", steps[i]).filter(function (x) { return !x.checkValidity(); });
        bad.forEach(function (x) { x.setAttribute("aria-invalid", "true"); });
        if (bad.length) { bad[0].reportValidity(); return; }
        show(Math.min(i + 1, steps.length - 1));
      });
    });
    $$("[data-prev]", f).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(i - 1, 0)); }); });
    show(0, true);
  });

  // quantity
  $$("[data-qty]").forEach(function (q) {
    var input = q.querySelector("input");
    $$("button", q).forEach(function (b) {
      b.addEventListener("click", function () {
        var v = (parseInt(input.value, 10) || 1) + (b.getAttribute("data-d") === "-" ? -1 : 1);
        input.value = Math.max(1, Math.min(99, v));
      });
    });
  });

  // modal + toast
  $$("[data-modal-open]").forEach(function (b) {
    b.addEventListener("click", function () { var d = document.getElementById(b.getAttribute("data-modal-open")); if (d && d.showModal) d.showModal(); });
  });
  $$("dialog [data-close]").forEach(function (b) { b.addEventListener("click", function () { b.closest("dialog").close(); }); });
  $$("[data-toast]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = document.createElement("div");
      t.className = "toast"; t.setAttribute("role", "status"); t.textContent = b.getAttribute("data-toast");
      document.body.appendChild(t);
      setTimeout(function () { t.remove(); }, 3200);
    });
  });

  // direction toggle (development helper)
  $$("[data-dir-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var r = document.documentElement;
      r.dir = rtl() ? "ltr" : "rtl";
      b.textContent = r.dir === "rtl" ? "LTR ⇄" : "⇄ RTL";
    });
  });

  // demo forms
  $$("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = f.querySelector("[data-ok]"); if (ok) { ok.hidden = false; ok.focus(); }
    });
  });
  $$("[aria-invalid]").forEach(function (x) { x.addEventListener("input", function () { x.removeAttribute("aria-invalid"); }); });

  // mobile menu (same API as the free kit)
  $$("[data-menu]").forEach(function (b) {
    b.addEventListener("click", function () {
      var n = b.closest(".nav"), open = n.hasAttribute("data-open");
      if (open) n.removeAttribute("data-open"); else n.setAttribute("data-open", "");
      b.setAttribute("aria-expanded", String(!open));
    });
  });
})();
