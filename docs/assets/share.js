/* תכנון פלוס – share a calculator result (WhatsApp + native share / copy link). No data leaves the browser
 * until the visitor taps a button, and only the calculator's own inputs go into the link (never free text).
 *
 * Usage on a calculator page (load it BEFORE the calculator's own script, so the shared state is read first):
 *   <script src="../../assets/share.js"></script>
 *   <div data-share data-share-scope="#calc" data-share-result="#r-amount"
 *        data-share-msg="יצא לי {result} במחשבון כמה לשים בחתונה. בדקו את שלכם:"></div>
 *
 *   data-share-scope   element whose inputs are encoded in the link (default: closest form, else first .tool-panel)
 *   data-share-result  optional element(s) whose text replaces {result} in the message (comma-separated selectors
 *                      fill {result}, {result2}, …)
 *   data-share-msg     the message; the link is appended on a new line
 *   data-share-note    optional line under the buttons (default: "the link reopens this exact calculation")
 *
 * The link is <page URL>#c&<field>=<value>&… with only the fields that differ from the page defaults.
 * Encoded: number/range inputs, selects, radio groups, checkboxes (single → 1/0, group → comma list).
 * Never encoded: text, email, tel, textarea, hidden, password, file, or anything with data-share-skip.
 * On load, a #c&… hash is applied to the fields and input/change events are fired so the page recomputes.
 */
(function () {
  "use strict";
  if (window.TPShare) return;
  var HASH = location.hash; // read now: some calculators rewrite the URL (and drop the hash) on their first run
  var MARK = "c";
  var HE = (document.documentElement.lang || "he").slice(0, 2) === "he";
  var T = HE
    ? { wa: "שתפו בוואטסאפ", share: "שיתוף…", copy: "העתקת קישור", copied: "✓ הקישור הועתק", note: "הקישור פותח את אותו חישוב בדיוק." }
    : { wa: "Share on WhatsApp", share: "Share…", copy: "Copy link", copied: "✓ Link copied", note: "The link reopens this exact calculation." };
  var SKIP = /^(text|email|tel|url|search|password|hidden|file|submit|button|reset|image|date|time|month|week|color)$/;

  // forRestore: data-share-skip only keeps a field out of NEW links (e.g. rows the page filled in by itself);
  // a link that names such a field may still set it.
  function fields(scope, forRestore) {
    var out = [], seen = {};
    Array.prototype.forEach.call(scope.querySelectorAll("input, select"), function (el) {
      var key = el.name || el.id;
      if (!key || el.closest(".tip-jar, [data-share], [data-share-never]")) return;
      if (!forRestore && el.closest("[data-share-skip]")) return;
      var type = el.tagName === "SELECT" ? "select" : (el.type || "text").toLowerCase();
      if (SKIP.test(type) || /[&=#]/.test(key)) return;
      if (type === "radio" || type === "checkbox") {
        var gkey = type + ":" + key;
        if (seen[gkey]) { seen[gkey].els.push(el); return; }
        seen[gkey] = { key: key, type: type, els: [el] };
        out.push(seen[gkey]);
      } else {
        out.push({ key: key, type: type, els: [el] });
      }
    });
    return out;
  }

  function current(f) {
    if (f.type === "radio") { var r = f.els.filter(function (e) { return e.checked; })[0]; return r ? r.value : ""; }
    if (f.type === "checkbox") {
      if (f.els.length === 1) return f.els[0].checked ? "1" : "0";
      return f.els.filter(function (e) { return e.checked; }).map(function (e) { return e.value; }).join(",");
    }
    return f.els[0].value;
  }
  function initial(f) {
    if (f.type === "radio") { var r = f.els.filter(function (e) { return e.defaultChecked; })[0]; return r ? r.value : ""; }
    if (f.type === "checkbox") {
      if (f.els.length === 1) return f.els[0].defaultChecked ? "1" : "0";
      return f.els.filter(function (e) { return e.defaultChecked; }).map(function (e) { return e.value; }).join(",");
    }
    if (f.type === "select") {
      var o = Array.prototype.filter.call(f.els[0].options, function (x) { return x.defaultSelected; })[0] || f.els[0].options[0];
      return o ? o.value : "";
    }
    return f.els[0].defaultValue;
  }
  function apply(f, v) {
    var changed = [];
    if (f.type === "radio") {
      f.els.forEach(function (e) { if (e.value === v && !e.checked) { e.checked = true; changed.push(e); } });
    } else if (f.type === "checkbox") {
      var want = f.els.length === 1 ? null : v.split(",");
      f.els.forEach(function (e) {
        var on = want ? want.indexOf(e.value) >= 0 : v === "1";
        if (e.checked !== on) { e.checked = on; changed.push(e); }
      });
    } else if (f.type === "select") {
      var ok = Array.prototype.some.call(f.els[0].options, function (o) { return o.value === v; });
      if (ok && f.els[0].value !== v) { f.els[0].value = v; changed.push(f.els[0]); }
    } else {
      if (v !== "" && !isFinite(Number(v))) return changed; // numbers only
      if (f.els[0].value !== v) { f.els[0].value = v; changed.push(f.els[0]); }
    }
    return changed;
  }

  function encode(scope) {
    var p = [];
    fields(scope).forEach(function (f) {
      var v = current(f);
      if (v !== initial(f)) p.push(encodeURIComponent(f.key) + "=" + encodeURIComponent(v));
    });
    return p.length ? "#" + MARK + "&" + p.join("&") : "";
  }
  function decode(hash) {
    if (!hash || hash.indexOf("#" + MARK + "&") !== 0) return null;
    var o = {};
    hash.slice(MARK.length + 2).split("&").forEach(function (kv) {
      var i = kv.indexOf("="); if (i < 1) return;
      try { o[decodeURIComponent(kv.slice(0, i))] = decodeURIComponent(kv.slice(i + 1)); } catch (e) {}
    });
    return o;
  }
  function fire(el) {
    ["input", "change"].forEach(function (t) {
      var ev; try { ev = new Event(t, { bubbles: true }); } catch (e) { ev = document.createEvent("Event"); ev.initEvent(t, true, false); }
      el.dispatchEvent(ev);
    });
  }
  function restore(scope, state) {
    var touched = [];
    fields(scope, true).forEach(function (f) { if (Object.prototype.hasOwnProperty.call(state, f.key)) touched = touched.concat(apply(f, state[f.key])); });
    touched.forEach(fire);
    return touched.length;
  }

  function scopeOf(box) {
    var sel = box.getAttribute("data-share-scope");
    return (sel && document.querySelector(sel)) || box.closest("form") || document.querySelector(".tool-panel") || document.body;
  }
  function pageUrl() { return location.origin + location.pathname; }
  function link(box) { return pageUrl() + encode(scopeOf(box)); }
  function message(box) {
    var msg = box.getAttribute("data-share-msg") || document.title;
    (box.getAttribute("data-share-result") || "").split(",").forEach(function (sel, i) {
      sel = sel.trim(); if (!sel) return;
      var el = document.querySelector(sel);
      var txt = el ? el.textContent.replace(/\s+/g, " ").trim() : "";
      msg = msg.split("{result" + (i ? i + 1 : "") + "}").join(txt);
    });
    return msg.replace(/\s+([.,:!?])/g, "$1").trim();
  }
  function waHref(box) { return "https://wa.me/?text=" + encodeURIComponent(message(box) + "\n" + link(box)); }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function copy(text, done) {
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(text).then(done, function () { legacy(); }); return; }
    legacy();
    function legacy() {
      var ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", "");
      ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); done();
    }
  }

  function build(box) {
    if (box.__share) return; box.__share = true;
    box.classList.add("share-bar");
    var mobile = !!navigator.share && (window.matchMedia ? window.matchMedia("(pointer: coarse)").matches : true);
    box.innerHTML =
      '<div class="btn-row">' +
      '<a class="btn small wa-btn" data-share-wa target="_blank" rel="noopener" href="https://wa.me/">' +
      '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></svg>' +
      "<span>" + T.wa + "</span></a>" +
      '<button type="button" class="btn small secondary" data-share-more>' + (mobile ? T.share : T.copy) + "</button>" +
      "</div>" +
      '<p class="small muted share-note">' + esc(box.getAttribute("data-share-note") || T.note) + ' <span data-share-ok hidden role="status">' + T.copied + "</span></p>";
    var wa = box.querySelector("[data-share-wa]");
    var more = box.querySelector("[data-share-more]");
    var ok = box.querySelector("[data-share-ok]");
    function sync() { wa.href = waHref(box); box.setAttribute("data-share-url", link(box)); }
    wa.addEventListener("click", sync); // fresh even if an update was missed
    wa.addEventListener("focus", sync);
    more.addEventListener("click", function () {
      sync();
      var url = link(box), done = function () { ok.hidden = false; setTimeout(function () { ok.hidden = true; }, 2200); };
      if (mobile) {
        navigator.share({ title: document.title, text: message(box), url: url }).catch(function (e) { if (e && e.name !== "AbortError") copy(url, done); });
      } else copy(url, done);
    });
    var scope = scopeOf(box), t;
    var later = function () { clearTimeout(t); t = setTimeout(sync, 30); };
    scope.addEventListener("input", later);
    scope.addEventListener("change", later);
    scope.addEventListener("click", later);
    sync();
  }

  function start() {
    var boxes = document.querySelectorAll("[data-share]");
    var state = decode(HASH), done = [];
    Array.prototype.forEach.call(boxes, function (box) {
      var scope = scopeOf(box);
      if (state && done.indexOf(scope) < 0) { done.push(scope); restore(scope, state); }
      build(box);
    });
    if (state) document.documentElement.setAttribute("data-shared", "1");
  }
  // After DOMContentLoaded + a tick: the calculator has wired its listeners (and filled any dynamic selects).
  var go = function () { setTimeout(start, 0); };
  if (document.readyState === "complete") go(); else document.addEventListener("DOMContentLoaded", go);

  window.TPShare = { encode: encode, decode: decode, restore: restore, link: link, message: message };
})();
