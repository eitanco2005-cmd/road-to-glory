/* תכנון פלוס — seating chart planner (client-side only; data in localStorage "tp-seating-v1").
 * Free: full on-screen use + watermarked print/PDF. Paid (product "seating-chart"): clean PDF, XLSX, table cards.
 */
(function () {
  "use strict";
  var SLUG = "seating-chart";
  var KEY = "tp-seating-v1";
  var DEFAULT_SIDES = ["צד הכלה", "צד החתן", "משותף"];
  var SIDE_COLORS = { "צד הכלה": "#c2417a", "צד החתן": "#2a6fb0", "משותף": "#0e6b63" };
  var PALETTE = ["#8a5cc2", "#c06a12", "#2f8a3e", "#b3261e", "#1b7f9a", "#7a6a12"];
  var UNLOCK_FEATS = ["PDF נקי בלי סימן מים (מפת שולחנות + רשימת כניסה לפי א-ב)", "ייצוא לאקסל: הושבה לפי שולחן, רשימת מוזמנים ושולחנות", "כרטיסי שולחן מוכנים להדפסה (מספר השולחן ושמות היושבים)", "תשלום חד-פעמי, לכל האירועים שתתכננו בדפדפן הזה"];

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function uid() { return Math.random().toString(36).slice(2, 9); }
  function num(v, d) { var n = parseInt(v, 10); return isFinite(n) && n > 0 ? n : d; }
  function collator() { try { return new Intl.Collator("he"); } catch (e) { return { compare: function (a, b) { return a < b ? -1 : a > b ? 1 : 0; } }; } }
  var coll = collator();

  /* ---------- state ---------- */
  function blank() { return { v: 1, title: "", date: "", guests: [], tables: [], apart: [] }; }
  var S = load();
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (s && Array.isArray(s.guests) && Array.isArray(s.tables)) { s.apart = s.apart || []; return s; }
    } catch (e) {}
    return blank();
  }
  var saveTimer = null;
  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { toast("לא הצלחנו לשמור בדפדפן (אחסון מלא או חסום)"); } }, 150);
  }
  var undoStack = [];
  function mutate(fn) {
    undoStack.push(JSON.stringify(S));
    if (undoStack.length > 40) undoStack.shift();
    fn();
    save(); render();
  }
  function undo() {
    if (!undoStack.length) return toast("אין מה לבטל");
    S = JSON.parse(undoStack.pop()); save(); render(); toast("הפעולה האחרונה בוטלה");
  }

  function guest(id) { for (var i = 0; i < S.guests.length; i++) if (S.guests[i].id === id) return S.guests[i]; return null; }
  function table(id) { for (var i = 0; i < S.tables.length; i++) if (S.tables[i].id === id) return S.tables[i]; return null; }
  function sides() {
    var out = DEFAULT_SIDES.slice();
    S.guests.forEach(function (g) { if (g.side && out.indexOf(g.side) < 0) out.push(g.side); });
    return out;
  }
  function groups() {
    var out = [];
    S.guests.forEach(function (g) { if (g.group && out.indexOf(g.group) < 0) out.push(g.group); });
    return out.sort(coll.compare);
  }
  function sideColor(side) {
    if (!side) return "#8a959b";
    if (SIDE_COLORS[side]) return SIDE_COLORS[side];
    var h = 0; for (var i = 0; i < side.length; i++) h = (h * 31 + side.charCodeAt(i)) >>> 0;
    return PALETTE[h % PALETTE.length];
  }
  function tableGuests(tid) { return S.guests.filter(function (g) { return g.table === tid; }); }
  function load_(tid) { return tableGuests(tid).reduce(function (s, g) { return s + g.n; }, 0); }
  function isApart(a, b) { return S.apart.some(function (p) { return (p[0] === a && p[1] === b) || (p[0] === b && p[1] === a); }); }
  function conflictsOf(t) {
    var gs = tableGuests(t.id), out = [];
    var used = gs.reduce(function (s, g) { return s + g.n; }, 0);
    if (used > t.seats) out.push("חריגה: " + used + " אנשים ב-" + t.seats + " מקומות");
    for (var i = 0; i < gs.length; i++) for (var j = i + 1; j < gs.length; j++) {
      if (isApart(gs[i].id, gs[j].id)) out.push(gs[i].name + " ו" + gs[j].name + " ביקשו לא לשבת יחד");
    }
    return out;
  }
  function tableLabel(t) { return t ? t.name : "ללא שולחן"; }
  function sortedTables() { return S.tables.slice(); }

  /* ---------- parsing ---------- */
  var HEAD = {
    name: /^(שם|שם מלא|שם האורח|שם המוזמן|מוזמן|אורח|name|guest|full name)$/i,
    n: /^(כמות|מספר|מס'|מס׳|מספר אנשים|מוזמנים|מאשרים|אנשים|count|qty|guests|party size|seats)$/i,
    side: /^(צד|side)$/i,
    group: /^(קבוצה|קטגוריה|שיוך|group|category)$/i,
    table: /^(שולחן|מס' שולחן|מספר שולחן|table)$/i
  };
  function mapHeader(row) {
    var map = {}, hit = 0;
    row.forEach(function (cell, i) {
      var c = String(cell || "").trim();
      Object.keys(HEAD).forEach(function (k) { if (map[k] === undefined && HEAD[k].test(c)) { map[k] = i; hit++; } });
    });
    return hit && map.name !== undefined ? map : null;
  }
  function rowsToGuests(rows, defaults) {
    defaults = defaults || {};
    rows = rows.filter(function (r) { return r && r.some(function (c) { return String(c || "").trim(); }); });
    if (!rows.length) return [];
    var map = null;
    for (var h = 0; h < Math.min(3, rows.length) && !map; h++) { map = mapHeader(rows[h]); if (map) rows = rows.slice(h + 1); }
    if (!map) map = { name: 0, n: 1, side: 2, group: 3 };
    var out = [];
    rows.forEach(function (r) {
      var name = String(r[map.name] || "").trim();
      if (!name) return;
      var nRaw = map.n !== undefined ? String(r[map.n] || "").trim() : "";
      var n = num(nRaw, 1);
      // "משפחת כהן 4" / "משפחת כהן (4)" in a single cell
      if (map.n === undefined || !nRaw) {
        var m = /^(.*?)[\s(×x*]+(\d{1,2})\)?$/.exec(name);
        if (m && m[1].trim()) { name = m[1].trim(); n = num(m[2], 1); }
      }
      out.push({
        id: uid(), name: name.slice(0, 80), n: Math.min(n, 60),
        side: String((map.side !== undefined && r[map.side]) || defaults.side || "").trim().slice(0, 40),
        group: String((map.group !== undefined && r[map.group]) || defaults.group || "").trim().slice(0, 40),
        table: null,
        _table: map.table !== undefined ? String(r[map.table] || "").trim().replace(/^ללא שולחן$/, "") : ""
      });
    });
    return out;
  }
  function parseCSV(text) {
    var first = text.split(/\r?\n/)[0] || "";
    var delim = (first.match(/\t/g) || []).length ? "\t" : (first.match(/;/g) || []).length > (first.match(/,/g) || []).length ? ";" : ",";
    var rows = [], row = [], cell = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) {
        if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; }
        else cell += ch;
      } else if (ch === '"' && cell === "") q = true;
      else if (ch === delim) { row.push(cell); cell = ""; }
      else if (ch === "\n" || ch === "\r") {
        if (ch === "\r" && text[i + 1] === "\n") i++;
        row.push(cell); rows.push(row); row = []; cell = "";
      } else cell += ch;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows;
  }
  function parsePaste(text) {
    var lines = text.split(/\r?\n/).filter(function (l) { return l.trim(); });
    var rows = lines.map(function (l) {
      if (l.indexOf("\t") >= 0) return l.split("\t");
      if (/[,;]/.test(l)) return l.split(/\s*[,;]\s*/);
      return [l];
    });
    return rows;
  }
  function addImported(list) {
    if (!list.length) { toast("לא נמצאו שמות לייבוא"); return 0; }
    mutate(function () {
      list.forEach(function (g) {
        if (g._table) {
          var t = S.tables.filter(function (t) { return t.name === g._table || t.name === "שולחן " + g._table; })[0];
          if (!t) { t = { id: uid(), name: /^\d+$/.test(g._table) ? "שולחן " + g._table : g._table, seats: 10, shape: "round" }; S.tables.push(t); }
          g.table = t.id;
        }
        delete g._table;
        S.guests.push(g);
      });
    });
    return list.length;
  }

  /* ---------- auto seat ---------- */
  function autoSeat(all) {
    var placed = 0, left = [];
    mutate(function () {
      if (all) S.guests.forEach(function (g) { g.table = null; });
      var free = {};
      S.tables.forEach(function (t) { free[t.id] = t.seats - load_(t.id); });
      var key = function (g) { return (g.side || "") + "|" + (g.group || ""); };
      var clusters = {};
      S.guests.forEach(function (g) { if (!g.table) (clusters[key(g)] = clusters[key(g)] || []).push(g); });
      var list = Object.keys(clusters).map(function (k) {
        var gs = clusters[k].sort(function (a, b) { return b.n - a.n; });
        return { key: k, side: gs[0].side, gs: gs, total: gs.reduce(function (s, g) { return s + g.n; }, 0) };
      }).sort(function (a, b) { return b.total - a.total; });
      var okWith = function (g, tid) { return tableGuests(tid).every(function (o) { return !isApart(g.id, o.id); }); };
      var okAll = function (gs, tid) { return gs.every(function (g) { return okWith(g, tid); }) && gs.every(function (a, i) { return gs.slice(i + 1).every(function (b) { return !isApart(a.id, b.id); }); }); };
      var affinity = function (tid, k) { return tableGuests(tid).filter(function (o) { return key(o) === k; }).length; };
      var sameSide = function (tid, side) { return tableGuests(tid).filter(function (o) { return o.side === side; }).length; };
      list.forEach(function (c) {
        // 1) whole cluster in one table: prefer a table already holding this cluster, then best fit
        var cands = S.tables.filter(function (t) { return free[t.id] >= c.total && okAll(c.gs, t.id); });
        if (cands.length) {
          cands.sort(function (a, b) { return (affinity(b.id, c.key) - affinity(a.id, c.key)) || (free[a.id] - free[b.id]); });
          var t = cands[0];
          c.gs.forEach(function (g) { g.table = t.id; placed += g.n; });
          free[t.id] -= c.total;
          return;
        }
        // 2) split: fill the emptiest compatible tables, keeping the cluster together as much as possible
        c.gs.forEach(function (g) {
          var opts = S.tables.filter(function (t) { return free[t.id] >= g.n && okWith(g, t.id); });
          if (!opts.length) { left.push(g); return; }
          opts.sort(function (a, b) {
            return (affinity(b.id, c.key) - affinity(a.id, c.key)) || (sameSide(b.id, c.side) - sameSide(a.id, c.side)) || (free[b.id] - free[a.id]);
          });
          g.table = opts[0].id; free[opts[0].id] -= g.n; placed += g.n;
        });
      });
    });
    var missing = left.reduce(function (s, g) { return s + g.n; }, 0);
    if (!S.tables.length) toast("קודם מוסיפים שולחנות");
    else if (missing) toast("שובצו " + placed + " אנשים. " + missing + " נשארו בלי מקום: הוסיפו שולחנות או מקומות.");
    else toast("שובצו " + placed + " אנשים. אפשר לגרור ולתקן ידנית (ובטל מחזיר אחורה).");
  }

  /* ---------- rendering ---------- */
  var filter = { q: "", side: "", group: "" };
  function chip(g, inTable) {
    var hit = filter.q && g.name.toLowerCase().indexOf(filter.q.toLowerCase()) >= 0;
    var hasApart = S.apart.some(function (p) { return p[0] === g.id || p[1] === g.id; });
    return '<button type="button" class="g-chip' + (hit ? " hit" : "") + '" data-gid="' + g.id + '" style="--side:' + sideColor(g.side) + '" title="' + esc(g.name + (g.side ? " · " + g.side : "") + (g.group ? " · " + g.group : "")) + '">' +
      '<span class="g-name">' + esc(g.name) + "</span>" +
      (g.n > 1 ? '<span class="g-n">' + g.n + "</span>" : "") +
      (hasApart ? '<span class="g-apart" title="יש בקשת הרחקה" aria-label="יש בקשת הרחקה">⇹</span>' : "") +
      (inTable ? "" : (g.group ? '<span class="g-group">' + esc(g.group) + "</span>" : "")) +
      "</button>";
  }
  function tableSvg(t, used) {
    var seats = Math.max(1, Math.min(t.seats, 30)), dots = "", i;
    var fill = function (k) { return k < used ? (used > t.seats ? "var(--danger)" : "var(--primary)") : "var(--surface)"; };
    if (t.shape === "rect") {
      var perSide = Math.ceil(seats / 2), w = Math.max(70, perSide * 16 + 10), x0 = (120 - w) / 2;
      var body = '<rect x="' + x0 + '" y="36" width="' + w + '" height="28" rx="5" class="t-top"/>';
      for (i = 0; i < seats; i++) {
        var top = i < perSide, k = top ? i : i - perSide, cnt = top ? perSide : seats - perSide;
        var cx = x0 + (w / (cnt + 1)) * (k + 1), cy = top ? 25 : 75;
        dots += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy + '" r="6" fill="' + fill(i) + '" class="seat"/>';
      }
      return '<svg viewBox="0 0 120 100" class="t-svg" aria-hidden="true">' + body + dots + '<text x="60" y="55" class="t-num">' + esc(shortName(t.name)) + "</text></svg>";
    }
    var R = 40, r = 26;
    for (i = 0; i < seats; i++) {
      var a = (Math.PI * 2 * i) / seats - Math.PI / 2;
      dots += '<circle cx="' + (60 + R * Math.cos(a)).toFixed(1) + '" cy="' + (50 + R * Math.sin(a)).toFixed(1) + '" r="' + (seats > 16 ? 4.5 : 6) + '" fill="' + fill(i) + '" class="seat"/>';
    }
    return '<svg viewBox="0 0 120 100" class="t-svg" aria-hidden="true"><circle cx="60" cy="50" r="' + r + '" class="t-top"/>' + dots + '<text x="60" y="55" class="t-num">' + esc(shortName(t.name)) + "</text></svg>";
  }
  function shortName(n) { var m = /(\d+)\s*$/.exec(n || ""); return m ? m[1] : (n || "").slice(0, 4); }

  function render() {
    var unlocked = window.AppUnlock && AppUnlock.isUnlocked(SLUG);
    $("#plan").className = "plan-pill" + (unlocked ? " full" : "");
    $("#plan").innerHTML = unlocked ? "✓ גרסה מלאה פעילה" : 'גרסה חינמית · <button type="button" data-act="unlock">מה בגרסה המלאה?</button>';
    $$("[data-paid]").forEach(function (b) { var l = b.querySelector(".lock"); if (l) l.hidden = !!unlocked; });
    if (document.activeElement !== $("#ev-title")) $("#ev-title").value = S.title || "";
    if (document.activeElement !== $("#ev-date")) $("#ev-date").value = S.date || "";

    // datalists
    $("#dl-sides").innerHTML = sides().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    $("#dl-groups").innerHTML = groups().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    var fs = $("#f-side"), fg = $("#f-group");
    fs.innerHTML = '<option value="">כל הצדדים</option>' + sides().map(function (s) { return '<option' + (s === filter.side ? " selected" : "") + ">" + esc(s) + "</option>"; }).join("");
    fg.innerHTML = '<option value="">כל הקבוצות</option>' + groups().map(function (s) { return '<option' + (s === filter.group ? " selected" : "") + ">" + esc(s) + "</option>"; }).join("");

    // unassigned list, grouped
    var un = S.guests.filter(function (g) {
      return !g.table && (!filter.side || g.side === filter.side) && (!filter.group || g.group === filter.group) &&
        (!filter.q || g.name.toLowerCase().indexOf(filter.q.toLowerCase()) >= 0);
    });
    var byGroup = {};
    un.forEach(function (g) { var k = g.group || "ללא קבוצה"; (byGroup[k] = byGroup[k] || []).push(g); });
    var keys = Object.keys(byGroup).sort(function (a, b) { return a === "ללא קבוצה" ? 1 : b === "ללא קבוצה" ? -1 : coll.compare(a, b); });
    var unTotal = S.guests.filter(function (g) { return !g.table; }).reduce(function (s, g) { return s + g.n; }, 0);
    $("#un-count").textContent = unTotal;
    $("#unassigned").innerHTML = keys.length ? keys.map(function (k) {
      var gs = byGroup[k].sort(function (a, b) { return coll.compare(a.name, b.name); });
      return '<div class="u-group"><div class="u-head">' + esc(k) + ' <span class="muted">(' + gs.reduce(function (s, g) { return s + g.n; }, 0) + ")</span></div><div class=\"chips\">" + gs.map(function (g) { return chip(g, true); }).join("") + "</div></div>";
    }).join("") : '<p class="empty muted">' + (S.guests.length ? (unTotal ? "אין תוצאות לסינון הזה." : "כל המוזמנים שובצו 🎉") : "עוד אין מוזמנים. הוסיפו שמות למעלה, הדביקו רשימה או ייבאו קובץ.") + "</p>";

    // tables
    var total = S.guests.reduce(function (s, g) { return s + g.n; }, 0);
    var seated = total - unTotal;
    var seatsTotal = S.tables.reduce(function (s, t) { return s + t.seats; }, 0);
    var conflicts = 0;
    $("#tables").innerHTML = S.tables.length ? sortedTables().map(function (t) {
      var gs = tableGuests(t.id).sort(function (a, b) { return coll.compare(a.group || "", b.group || "") || coll.compare(a.name, b.name); });
      var used = gs.reduce(function (s, g) { return s + g.n; }, 0);
      var cf = conflictsOf(t); conflicts += cf.length;
      return '<article class="t-card' + (cf.length ? " conflict" : "") + (used === t.seats ? " full" : "") + '" data-tid="' + t.id + '">' +
        '<header><button type="button" class="t-name" data-edit-table="' + t.id + '" title="עריכת שולחן">' + esc(t.name) + ' <span aria-hidden="true">✎</span></button>' +
        '<span class="t-occ' + (used > t.seats ? " over" : "") + '">' + used + "/" + t.seats + "</span></header>" +
        tableSvg(t, used) +
        '<div class="chips drop" data-drop="' + t.id + '">' + (gs.length ? gs.map(function (g) { return chip(g, false); }).join("") : '<span class="drop-hint">גררו לכאן מוזמנים</span>') + "</div>" +
        (cf.length ? '<ul class="t-warn">' + cf.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul>" : "") +
        "</article>";
    }).join("") : '<div class="empty-tables"><p>עוד אין שולחנות.</p><button type="button" class="btn" data-act="add-tables">הוספת שולחנות</button></div>';

    $("#stats").innerHTML =
      stat(total, "מוזמנים") + stat(seated, "שובצו") + stat(unTotal, "בלי שולחן", unTotal ? "warn" : "") +
      stat(S.tables.length, "שולחנות") + stat(Math.max(0, seatsTotal - seated), "מקומות פנויים") +
      stat(conflicts, "התנגשויות", conflicts ? "bad" : "");
    var need = total - seatsTotal;
    $("#capacity-hint").textContent = need > 0 ? "חסרים " + need + " מקומות לכל המוזמנים (" + Math.ceil(need / 10) + " שולחנות של 10)." : "";
  }
  function stat(v, l, cls) { return '<div class="stat ' + (cls || "") + '"><b class="num">' + v + "</b><span>" + l + "</span></div>"; }

  /* ---------- dialogs ---------- */
  function dialog(html, onSubmit, onReady) {
    var d = document.createElement("dialog");
    d.className = "app-dialog";
    d.innerHTML = '<form method="dialog" class="dlg-close-row"><button class="dlg-x" aria-label="סגירה" value="close">×</button></form>' + html;
    document.body.appendChild(d);
    d.addEventListener("close", function () { d.remove(); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    var f = d.querySelector("form.dlg-form");
    if (f) f.addEventListener("submit", function (e) { e.preventDefault(); if (onSubmit(f, d) !== false) d.close(); });
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
    if (onReady) onReady(d);
    var first = d.querySelector("form.dlg-form input, form.dlg-form textarea");
    if (first) first.focus();
    return d;
  }
  function tableOptions(sel) {
    return '<option value="">ללא שולחן</option>' + S.tables.map(function (t) {
      var used = load_(t.id);
      return '<option value="' + t.id + '"' + (t.id === sel ? " selected" : "") + ">" + esc(t.name) + " (" + used + "/" + t.seats + ")</option>";
    }).join("");
  }

  function editGuest(id) {
    var g = guest(id); if (!g) return;
    var apartList = function () {
      return S.apart.filter(function (p) { return p[0] === id || p[1] === id; }).map(function (p) {
        var o = guest(p[0] === id ? p[1] : p[0]);
        return o ? '<li>' + esc(o.name) + ' <button type="button" class="btn tiny ghost" data-unapart="' + o.id + '">הסרה</button></li>' : "";
      }).join("");
    };
    var others = S.guests.filter(function (o) { return o.id !== id; }).sort(function (a, b) { return coll.compare(a.name, b.name); });
    dialog(
      '<h2>עריכת מוזמן</h2><form class="dlg-form">' +
      '<div class="fields cols-2"><div class="field"><label for="eg-name">שם</label><input id="eg-name" name="name" type="text" required maxlength="80" value="' + esc(g.name) + '"></div>' +
      '<div class="field"><label for="eg-n">מספר אנשים</label><input id="eg-n" name="n" type="number" min="1" max="60" value="' + g.n + '"></div>' +
      '<div class="field"><label for="eg-side">צד</label><input id="eg-side" name="side" type="text" list="dl-sides" maxlength="40" value="' + esc(g.side) + '"></div>' +
      '<div class="field"><label for="eg-group">קבוצה</label><input id="eg-group" name="group" type="text" list="dl-groups" maxlength="40" value="' + esc(g.group) + '"></div></div>' +
      '<div class="field"><label for="eg-table">שולחן</label><select id="eg-table" name="table">' + tableOptions(g.table) + "</select></div>" +
      '<div class="field"><span class="label">לא להושיב באותו שולחן עם</span><ul class="apart-list">' + apartList() + "</ul>" +
      '<div class="btn-row"><select id="eg-apart" aria-label="בחירת מוזמן להרחקה" style="flex:1"><option value="">בחרו מוזמן…</option>' +
      others.map(function (o) { return '<option value="' + o.id + '">' + esc(o.name) + "</option>"; }).join("") +
      '</select><button type="button" class="btn ghost small" id="eg-apart-add">הוספה</button></div></div>' +
      '<div class="dlg-actions"><button class="btn" type="submit">שמירה</button><button class="btn ghost" type="button" data-close>ביטול</button><span class="spacer"></span><button class="btn danger" type="button" id="eg-del">מחיקה</button></div></form>',
      function (f) {
        mutate(function () {
          g.name = f.name.value.trim().slice(0, 80) || g.name;
          g.n = Math.min(num(f.n.value, 1), 60);
          g.side = f.side.value.trim().slice(0, 40);
          g.group = f.group.value.trim().slice(0, 40);
          g.table = f.table.value || null;
        });
      },
      function (d) {
        d.querySelector("[data-close]").addEventListener("click", function () { d.close(); });
        d.querySelector("#eg-del").addEventListener("click", function () {
          if (!confirm("למחוק את " + g.name + "?")) return;
          mutate(function () {
            S.guests = S.guests.filter(function (x) { return x.id !== id; });
            S.apart = S.apart.filter(function (p) { return p[0] !== id && p[1] !== id; });
          });
          d.close();
        });
        d.querySelector("#eg-apart-add").addEventListener("click", function () {
          var o = d.querySelector("#eg-apart").value;
          if (!o || isApart(id, o)) return;
          mutate(function () { S.apart.push([id, o]); });
          d.querySelector(".apart-list").innerHTML = apartList();
        });
        d.querySelector(".apart-list").addEventListener("click", function (e) {
          var b = e.target.closest("[data-unapart]"); if (!b) return;
          var o = b.getAttribute("data-unapart");
          mutate(function () { S.apart = S.apart.filter(function (p) { return !((p[0] === id && p[1] === o) || (p[0] === o && p[1] === id)); }); });
          d.querySelector(".apart-list").innerHTML = apartList();
        });
      });
  }

  function addTables() {
    var total = S.guests.reduce(function (s, g) { return s + g.n; }, 0);
    var seatsTotal = S.tables.reduce(function (s, t) { return s + t.seats; }, 0);
    var suggest = Math.max(1, Math.ceil(Math.max(0, total - seatsTotal) / 10)) || 1;
    var nextNum = S.tables.reduce(function (m, t) { var k = parseInt(shortName(t.name), 10); return isFinite(k) && k > m ? k : m; }, 0) + 1;
    dialog(
      '<h2>הוספת שולחנות</h2><form class="dlg-form">' +
      '<div class="fields cols-3"><div class="field"><label for="at-count">כמה שולחנות</label><input id="at-count" name="count" type="number" min="1" max="100" value="' + suggest + '"></div>' +
      '<div class="field"><label for="at-seats">מקומות בשולחן</label><input id="at-seats" name="seats" type="number" min="1" max="40" value="10"></div>' +
      '<div class="field"><label for="at-shape">צורה</label><select id="at-shape" name="shape"><option value="round">עגול</option><option value="rect">מלבני</option></select></div></div>' +
      '<div class="fields cols-2"><div class="field"><label for="at-prefix">שם</label><input id="at-prefix" name="prefix" type="text" value="שולחן" maxlength="30"></div>' +
      '<div class="field"><label for="at-start">מספור החל מ-</label><input id="at-start" name="start" type="number" min="0" max="999" value="' + nextNum + '"></div></div>' +
      (total ? '<p class="small muted">יש ' + total + " מוזמנים ו-" + seatsTotal + " מקומות. ההצעה מחושבת לשולחנות של 10.</p>" : "") +
      '<p class="small muted">שולחן אבירים או שולחן מיוחד? הוסיפו שולחן אחד ושנו לו את השם והמקומות בלחיצה על השם.</p>' +
      '<div class="dlg-actions"><button class="btn" type="submit">הוספה</button></div></form>',
      function (f) {
        var c = Math.min(num(f.count.value, 1), 100), seats = Math.min(num(f.seats.value, 10), 40), start = parseInt(f.start.value, 10) || 1;
        var prefix = f.prefix.value.trim() || "שולחן";
        mutate(function () {
          for (var i = 0; i < c; i++) S.tables.push({ id: uid(), name: (prefix + " " + (start + i)).slice(0, 40), seats: seats, shape: f.shape.value === "rect" ? "rect" : "round" });
        });
      });
  }

  function editTable(tid) {
    var t = table(tid); if (!t) return;
    dialog(
      '<h2>עריכת שולחן</h2><form class="dlg-form">' +
      '<div class="fields cols-3"><div class="field"><label for="et-name">שם</label><input id="et-name" name="name" type="text" required maxlength="40" value="' + esc(t.name) + '"></div>' +
      '<div class="field"><label for="et-seats">מקומות</label><input id="et-seats" name="seats" type="number" min="1" max="40" value="' + t.seats + '"></div>' +
      '<div class="field"><label for="et-shape">צורה</label><select id="et-shape" name="shape"><option value="round"' + (t.shape !== "rect" ? " selected" : "") + '>עגול</option><option value="rect"' + (t.shape === "rect" ? " selected" : "") + ">מלבני</option></select></div></div>" +
      '<div class="dlg-actions"><button class="btn" type="submit">שמירה</button><button class="btn ghost" type="button" id="et-clear">פינוי השולחן</button><span class="spacer"></span><button class="btn danger" type="button" id="et-del">מחיקת שולחן</button></div></form>',
      function (f) {
        mutate(function () { t.name = f.name.value.trim().slice(0, 40) || t.name; t.seats = Math.min(num(f.seats.value, t.seats), 40); t.shape = f.shape.value === "rect" ? "rect" : "round"; });
      },
      function (d) {
        d.querySelector("#et-clear").addEventListener("click", function () { mutate(function () { tableGuests(tid).forEach(function (g) { g.table = null; }); }); d.close(); });
        d.querySelector("#et-del").addEventListener("click", function () {
          if (!confirm("למחוק את " + t.name + "? היושבים בו יחזרו לרשימת 'בלי שולחן'.")) return;
          mutate(function () { tableGuests(tid).forEach(function (g) { g.table = null; }); S.tables = S.tables.filter(function (x) { return x.id !== tid; }); });
          d.close();
        });
      });
  }

  function pasteDialog() {
    dialog(
      '<h2>הדבקת רשימת מוזמנים</h2><form class="dlg-form">' +
      '<div class="field"><label for="pd-text">שורה לכל הזמנה</label><textarea id="pd-text" name="text" rows="9" placeholder="משפחת כהן, 4&#10;דנה ואורי לוי, 2, צד הכלה, חברים מהצבא&#10;סבתא רחל"></textarea>' +
      '<span class="hint">אפשר להדביק עמודות ישירות מאקסל או מ-Google Sheets. סדר העמודות: שם, מספר אנשים, צד, קבוצה (רק השם חובה). אם יש שורת כותרות (שם, כמות, צד, קבוצה, שולחן) היא תזוהה.</span></div>' +
      '<div class="fields cols-2"><div class="field"><label for="pd-side">צד (לכל מי שאין לו)</label><input id="pd-side" name="side" type="text" list="dl-sides"></div>' +
      '<div class="field"><label for="pd-group">קבוצה (לכל מי שאין לו)</label><input id="pd-group" name="group" type="text" list="dl-groups"></div></div>' +
      '<div class="dlg-actions"><button class="btn" type="submit">הוספה לרשימה</button></div></form>',
      function (f) {
        var n = addImported(rowsToGuests(parsePaste(f.text.value), { side: f.side.value.trim(), group: f.group.value.trim() }));
        if (n) toast("נוספו " + n + " הזמנות");
      });
  }

  function importFile(file) {
    if (!file) return;
    var name = file.name.toLowerCase();
    var rd = file.arrayBuffer ? file.arrayBuffer() : new Response(file).arrayBuffer();
    rd.then(function (buf) {
      if (/\.json$/.test(name)) {
        var data = JSON.parse(new TextDecoder().decode(buf));
        if (!data || !Array.isArray(data.guests) || !Array.isArray(data.tables)) throw new Error("bad backup");
        if (!confirm("לשחזר מהגיבוי? הנתונים הנוכחיים בכלי יוחלפו.")) return;
        mutate(function () { S = data; S.apart = S.apart || []; });
        toast("הגיבוי שוחזר");
        return;
      }
      if (/\.xlsx$/.test(name)) {
        return AppZip.readSheet(buf).then(function (rows) { var n = addImported(rowsToGuests(rows)); if (n) toast("יובאו " + n + " הזמנות מהאקסל"); });
      }
      if (/\.xls$/.test(name)) throw new Error("xls");
      var text;
      try { text = new TextDecoder("utf-8", { fatal: true }).decode(buf); } catch (e) { text = new TextDecoder("windows-1255").decode(buf); }
      text = text.replace(/^﻿/, "");
      var n = addImported(rowsToGuests(parseCSV(text)));
      if (n) toast("יובאו " + n + " הזמנות");
    }).catch(function (e) {
      if (window.console) console.error(e);
      toast(e && e.message === "xls" ? "קובץ XLS ישן: שמרו אותו כ-XLSX או CSV ונסו שוב" : "לא הצלחנו לקרוא את הקובץ. נסו לשמור אותו כ-CSV או להדביק את הרשימה.");
    });
  }

  function demo() {
    if (S.guests.length && !confirm("לטעון דוגמה? הנתונים הנוכחיים יוחלפו (אפשר לבטל עם 'בטל').")) return;
    var rows = [
      ["הורי הכלה", 2, "צד הכלה", "משפחה קרובה"], ["סבתא אסתר", 1, "צד הכלה", "משפחה קרובה"], ["נועה ואיתי (אחות הכלה)", 2, "צד הכלה", "משפחה קרובה"], ["משפחת אברהם", 4, "צד הכלה", "משפחה קרובה"],
      ["דוד ורינה לוי", 2, "צד הכלה", "משפחה מורחבת"], ["משפחת פרץ", 5, "צד הכלה", "משפחה מורחבת"], ["יעל ומשה גבאי", 2, "צד הכלה", "משפחה מורחבת"], ["משפחת חדד", 4, "צד הכלה", "משפחה מורחבת"],
      ["שירה כץ", 1, "צד הכלה", "חברות מהתיכון"], ["מאיה ועידו", 2, "צד הכלה", "חברות מהתיכון"], ["ליאור שמש", 1, "צד הכלה", "חברות מהתיכון"], ["טל וגיא", 2, "צד הכלה", "חברות מהתיכון"], ["רוני אדלר", 1, "צד הכלה", "חברות מהתיכון"],
      ["הילה מהעבודה", 2, "צד הכלה", "עבודה"], ["אורנה (מנהלת)", 2, "צד הכלה", "עבודה"], ["קרן וניר", 2, "צד הכלה", "עבודה"], ["עמית", 1, "צד הכלה", "עבודה"],
      ["הורי החתן", 2, "צד החתן", "משפחה קרובה"], ["סבא יוסף וסבתא מרים", 2, "צד החתן", "משפחה קרובה"], ["אח החתן ומשפחתו", 4, "צד החתן", "משפחה קרובה"],
      ["משפחת מזרחי", 4, "צד החתן", "משפחה מורחבת"], ["דודה שושנה", 1, "צד החתן", "משפחה מורחבת"], ["משפחת ביטון", 5, "צד החתן", "משפחה מורחבת"], ["רפי ודליה", 2, "צד החתן", "משפחה מורחבת"],
      ["יונתן", 1, "צד החתן", "חברים מהצבא"], ["אלון ושני", 2, "צד החתן", "חברים מהצבא"], ["רועי", 1, "צד החתן", "חברים מהצבא"], ["עומר ונגה", 2, "צד החתן", "חברים מהצבא"], ["בן", 1, "צד החתן", "חברים מהצבא"], ["אסף", 1, "צד החתן", "חברים מהצבא"],
      ["דניאל ורותם", 2, "צד החתן", "אוניברסיטה"], ["מתן", 1, "צד החתן", "אוניברסיטה"], ["ספיר ואביב", 2, "צד החתן", "אוניברסיטה"], ["גלעד", 1, "צד החתן", "אוניברסיטה"],
      ["השכנים מהבניין", 2, "משותף", "שכנים"], ["משפחת אוחיון", 3, "משותף", "שכנים"], ["הרב והרבנית", 2, "משותף", "קהילה"]
    ];
    undoStack.push(JSON.stringify(S));
    S = blank();
    S.title = "החתונה של נועם ושירה";
    S.date = "";
    rows.forEach(function (r) { S.guests.push({ id: uid(), name: r[0], n: r[1], side: r[2], group: r[3], table: null }); });
    S.tables.push({ id: uid(), name: "שולחן 1", seats: 12, shape: "rect" });
    for (var i = 2; i <= 8; i++) S.tables.push({ id: uid(), name: "שולחן " + i, seats: 10, shape: "round" });
    var a = S.guests.filter(function (g) { return g.name === "משפחת פרץ"; })[0], b = S.guests.filter(function (g) { return g.name === "משפחת חדד"; })[0];
    if (a && b) S.apart.push([a.id, b.id]);
    save(); render();
    toast("נטענה דוגמה: לחצו 'הושבה אוטומטית' כדי לראות הצעה");
  }

  /* ---------- exports ---------- */
  function guestsAlpha() { return S.guests.slice().sort(function (a, b) { return coll.compare(a.name, b.name); }); }
  function headerBlock() {
    return '<div class="p-head"><h1>' + esc(S.title || "סידור הושבה") + "</h1>" + (S.date ? '<p>' + esc(fmtDate(S.date)) + "</p>" : "") + "</div>";
  }
  function fmtDate(d) { try { return new Date(d + "T12:00:00").toLocaleDateString("he-IL", { weekday: "long", day: "numeric", month: "long", year: "numeric" }); } catch (e) { return d; } }
  function printChart(clean) {
    var total = S.guests.reduce(function (s, g) { return s + g.n; }, 0);
    var html = (clean ? "" : watermark()) + headerBlock() +
      '<p class="p-sum">' + total + " מוזמנים · " + S.tables.length + " שולחנות</p>" +
      '<div class="p-tables">' + S.tables.map(function (t) {
        var gs = tableGuests(t.id).sort(function (a, b) { return coll.compare(a.name, b.name); });
        return '<div class="p-table"><h2>' + esc(t.name) + ' <small>(' + load_(t.id) + "/" + t.seats + ")</small></h2><ul>" +
          gs.map(function (g) { return "<li>" + esc(g.name) + (g.n > 1 ? " <small>(" + g.n + ")</small>" : "") + "</li>"; }).join("") + "</ul></div>";
      }).join("") + "</div>" +
      '<div class="p-index"><h2>רשימת כניסה לפי א-ב</h2><table><thead><tr><th>שם</th><th>אנשים</th><th>שולחן</th></tr></thead><tbody>' +
      guestsAlpha().map(function (g) { return "<tr><td>" + esc(g.name) + "</td><td>" + g.n + "</td><td>" + esc(tableLabel(table(g.table))) + "</td></tr>"; }).join("") +
      "</tbody></table></div>";
    doPrint(html, "chart");
  }
  function printCards() {
    var html = S.tables.map(function (t) {
      var gs = tableGuests(t.id).sort(function (a, b) { return coll.compare(a.name, b.name); });
      return '<section class="p-card"><div class="p-card-in"><div class="p-card-ev">' + esc(S.title || "") + '</div><div class="p-card-num">' + esc(t.name) + "</div>" +
        '<ul class="p-card-names">' + gs.map(function (g) { return "<li>" + esc(g.name) + "</li>"; }).join("") + "</ul></div></section>";
    }).join("");
    doPrint(html || "<p>אין שולחנות.</p>", "cards");
  }
  function watermark() {
    var s = ""; for (var i = 0; i < 18; i++) s += "<span>תכנון פלוס · גרסה חינמית</span>";
    return '<div class="wm" aria-hidden="true">' + s + '</div><div class="wm-foot">נוצר בגרסה החינמית של תכנון פלוס · tichnun.netlify.app/apps/seating · לגרסה נקייה: פתיחת הגרסה המלאה בכלי</div>';
  }
  function doPrint(html, mode) {
    var area = $("#print-area");
    if (!area) { area = document.createElement("div"); area.id = "print-area"; document.body.appendChild(area); }
    area.className = "print-" + mode;
    area.innerHTML = html;
    document.body.classList.add("printing");
    var done = function () { document.body.classList.remove("printing"); window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    setTimeout(function () { window.print(); setTimeout(done, 500); }, 60);
  }
  function exportXlsx() {
    var byTable = [["סידור הושבה: " + (S.title || "")], ["שולחן", "מקומות", "שם", "אנשים", "צד", "קבוצה"]];
    S.tables.forEach(function (t) {
      tableGuests(t.id).sort(function (a, b) { return coll.compare(a.name, b.name); }).forEach(function (g) {
        byTable.push([t.name, t.seats, g.name, g.n, g.side || "", g.group || ""]);
      });
    });
    var un = S.guests.filter(function (g) { return !g.table; });
    un.forEach(function (g) { byTable.push(["ללא שולחן", "", g.name, g.n, g.side || "", g.group || ""]); });
    var guestsSheet = [["שם", "אנשים", "צד", "קבוצה", "שולחן"]].concat(guestsAlpha().map(function (g) { return [g.name, g.n, g.side || "", g.group || "", tableLabel(table(g.table))]; }));
    var tablesSheet = [["שולחן", "צורה", "מקומות", "תפוסה", "פנוי"]].concat(S.tables.map(function (t) { var u = load_(t.id); return [t.name, t.shape === "rect" ? "מלבני" : "עגול", t.seats, u, t.seats - u]; }));
    var blob = AppZip.xlsx({ sheets: [
      { name: "הושבה לפי שולחן", rows: byTable, cols: [14, 9, 28, 8, 12, 18], title: [0], header: [1], freeze: 2, autoFilter: 2 },
      { name: "רשימת כניסה א-ב", rows: guestsSheet, cols: [28, 8, 12, 18, 14], header: [0], freeze: 1, autoFilter: 1 },
      { name: "שולחנות", rows: tablesSheet, cols: [16, 10, 10, 10, 10], header: [0], freeze: 1 }
    ] });
    AppZip.download(blob, fileBase() + ".xlsx");
    toast("קובץ האקסל ירד");
  }
  function fileBase() { return ("seating-" + (S.title || "event")).replace(/[\\\/:*?"<>|]+/g, "").replace(/\s+/g, "-").slice(0, 60); }
  function backup() {
    AppZip.download(new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }), fileBase() + "-backup.json");
    toast("קובץ הגיבוי ירד. שמרו אותו כדי לשחזר בכל דפדפן.");
  }
  function paid(fn, reason) {
    return function () {
      if (AppUnlock.require(SLUG, { title: "הגרסה המלאה של סידור ההושבה · ₪29", reason: reason, features: UNLOCK_FEATS })) fn();
    };
  }

  /* ---------- toast ---------- */
  var toastTimer;
  function toast(msg) {
    var t = $("#toast");
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove("show"); }, 3600);
  }

  /* ---------- drag & drop (pointer events: mouse + touch long-press) ---------- */
  var drag = null;
  function startDrag(ch, x, y) {
    var ghost = ch.cloneNode(true);
    ghost.className += " ghost";
    document.body.appendChild(ghost);
    drag = { id: ch.getAttribute("data-gid"), ghost: ghost, src: ch, over: null };
    ch.classList.add("dragging");
    moveDrag(x, y);
  }
  function moveDrag(x, y) {
    if (!drag) return;
    drag.ghost.style.left = x + "px"; drag.ghost.style.top = y + "px";
    drag.ghost.style.display = "none";
    var el = document.elementFromPoint(x, y);
    drag.ghost.style.display = "";
    var zone = el && el.closest("[data-drop]");
    if (zone !== drag.over) {
      if (drag.over) drag.over.classList.remove("over");
      drag.over = zone; if (zone) zone.classList.add("over");
    }
    // auto-scroll near viewport edges
    if (y < 60) window.scrollBy(0, -12); else if (y > window.innerHeight - 60) window.scrollBy(0, 12);
  }
  function endDrag() {
    if (!drag) return;
    var d = drag; drag = null;
    d.ghost.remove(); d.src.classList.remove("dragging");
    if (d.over) {
      d.over.classList.remove("over");
      var tid = d.over.getAttribute("data-drop") || null;
      var g = guest(d.id);
      if (g && (g.table || null) !== (tid || null)) mutate(function () { g.table = tid || null; });
    }
  }
  function bindDrag(root) {
    var pending = null;
    root.addEventListener("pointerdown", function (e) {
      var ch = e.target.closest(".g-chip");
      if (!ch || e.button > 0) return;
      pending = { ch: ch, x: e.clientX, y: e.clientY, touch: e.pointerType !== "mouse", started: false, id: e.pointerId };
      if (pending.touch) {
        pending.timer = setTimeout(function () {
          if (pending && !pending.started) { pending.started = true; startDrag(pending.ch, pending.x, pending.y); if (navigator.vibrate) navigator.vibrate(15); }
        }, 320);
      }
    });
    document.addEventListener("pointermove", function (e) {
      if (!pending) return;
      if (pending.started) { e.preventDefault(); moveDrag(e.clientX, e.clientY); return; }
      var dist = Math.abs(e.clientX - pending.x) + Math.abs(e.clientY - pending.y);
      if (pending.touch) { if (dist > 10) { clearTimeout(pending.timer); pending = null; } return; }
      if (dist > 6) { pending.started = true; startDrag(pending.ch, e.clientX, e.clientY); }
    }, { passive: false });
    document.addEventListener("touchmove", function (e) { if (drag) e.preventDefault(); }, { passive: false });
    var up = function (e) {
      if (!pending) return;
      clearTimeout(pending.timer);
      var p = pending; pending = null;
      if (p.started) { endDrag(); suppressClick = true; setTimeout(function () { suppressClick = false; }, 50); }
    };
    document.addEventListener("pointerup", up);
    document.addEventListener("pointercancel", function () { if (pending) { clearTimeout(pending.timer); if (pending.started) endDrag(); pending = null; } });
    root.addEventListener("contextmenu", function (e) { if (e.target.closest(".g-chip")) e.preventDefault(); });
  }
  var suppressClick = false;

  /* ---------- wiring ---------- */
  function init() {
    if (!document.getElementById("toast")) { var t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    var app = $("#app");
    bindDrag(app);
    app.addEventListener("click", function (e) {
      if (suppressClick) return;
      var ch = e.target.closest(".g-chip"); if (ch) return editGuest(ch.getAttribute("data-gid"));
      var et = e.target.closest("[data-edit-table]"); if (et) return editTable(et.getAttribute("data-edit-table"));
      var a = e.target.closest("[data-act]"); if (!a) return;
      var act = a.getAttribute("data-act");
      var menu = a.closest("details"); if (menu) menu.open = false;
      ({
        "add-tables": addTables, "paste": pasteDialog, "auto": function () { autoSeat(false); },
        "auto-all": function () { if (confirm("לבטל את כל השיבוצים ולהושיב מחדש את כולם?")) autoSeat(true); },
        "clear-seats": function () { if (confirm("להוציא את כולם מהשולחנות? (אפשר לבטל)")) mutate(function () { S.guests.forEach(function (g) { g.table = null; }); }); },
        "undo": undo, "demo": demo, "backup": backup,
        "restore": function () { $("#file-json").click(); },
        "import": function () { $("#file-in").click(); },
        "reset": function () { if (confirm("למחוק את כל הנתונים בכלי? (מומלץ לשמור גיבוי קודם)")) mutate(function () { S = blank(); }); },
        "print": function () { printChart(AppUnlock.isUnlocked(SLUG)); },
        "pdf-clean": paid(function () { printChart(true); }, "PDF נקי בלי סימן מים, מוכן לשליחה לאולם ולהדפסה."),
        "xlsx": paid(exportXlsx, "ייצוא לאקסל עם הושבה לפי שולחן ורשימת כניסה לפי א-ב."),
        "cards": paid(printCards, "כרטיסי שולחן גדולים להדפסה: מספר השולחן ושמות היושבים."),
        "unlock": function () { AppUnlock.open(SLUG, { title: "הגרסה המלאה של סידור ההושבה · ₪29", features: UNLOCK_FEATS }); }
      }[act] || function () {})();
    });
    $("#plan").addEventListener("click", function (e) { if (e.target.closest("[data-act=unlock]")) AppUnlock.open(SLUG, { title: "הגרסה המלאה של סידור ההושבה · ₪29", features: UNLOCK_FEATS }); });
    $("#add-guest").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, name = f.gname.value.trim();
      if (!name) return;
      var g = { id: uid(), name: name.slice(0, 80), n: Math.min(num(f.gn.value, 1), 60), side: f.gside.value.trim().slice(0, 40), group: f.ggroup.value.trim().slice(0, 40), table: null };
      mutate(function () { S.guests.push(g); });
      f.gname.value = ""; f.gn.value = "1"; f.gname.focus();
    });
    $("#ev-title").addEventListener("input", function (e) { S.title = e.target.value.slice(0, 80); save(); });
    $("#ev-date").addEventListener("change", function (e) { S.date = e.target.value; save(); });
    $("#q").addEventListener("input", function (e) { filter.q = e.target.value.trim(); render(); });
    $("#f-side").addEventListener("change", function (e) { filter.side = e.target.value; render(); });
    $("#f-group").addEventListener("change", function (e) { filter.group = e.target.value; render(); });
    $("#file-in").addEventListener("change", function (e) { importFile(e.target.files[0]); e.target.value = ""; });
    $("#file-json").addEventListener("change", function (e) { importFile(e.target.files[0]); e.target.value = ""; });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !/INPUT|TEXTAREA/.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); undo(); }
    });
    // mobile tabs
    $$(".app-tabs [data-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".app-tabs [data-tab]").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
        $(".seat-layout").setAttribute("data-show", b.getAttribute("data-tab"));
      });
    });
    AppUnlock.onChange(function () { render(); });
    document.addEventListener("click", function (e) { $$("details.menu[open]").forEach(function (m) { if (!m.contains(e.target)) m.open = false; }); });
    render();
    if (new URLSearchParams(location.search).get("demo") === "1" && !S.guests.length) demo();
  }

  window.SeatingApp = { state: function () { return S; }, autoSeat: autoSeat, render: render, demo: demo, parseCSV: parseCSV, rowsToGuests: rowsToGuests };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
