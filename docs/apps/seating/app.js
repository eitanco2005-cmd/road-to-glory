/* תכנון פלוס / Tichnun Plus — seating chart planner (client-side only; data in localStorage).
 * One codebase, two languages: <html lang="he"> (apps/seating/, ₪29, product "seating-chart") or
 * <html lang="en"> (en/apps/seating/, USD, product "seating-chart-en"). Each language keeps its own saved chart.
 * Free: full on-screen use + watermarked print/PDF. Paid: clean PDF, XLSX, table cards.
 */
(function () {
  "use strict";
  var EN = /^en/i.test(document.documentElement.lang || "");
  function L(he, en) { return EN ? en : he; }
  var SLUG = L("seating-chart", "seating-chart-en");
  var KEY = L("tp-seating-v1", "tp-seating-en-v1");
  var PRICE = L("₪29", "$9");
  var APP_URL = L("https://tichnun.netlify.app/apps/seating/", "https://tichnun.netlify.app/en/apps/seating/");
  var DEFAULT_SIDES = L(["צד הכלה", "צד החתן", "משותף"], ["Bride's side", "Groom's side", "Both"]);
  var SIDE_COLORS = {};
  SIDE_COLORS[DEFAULT_SIDES[0]] = "#c2417a"; SIDE_COLORS[DEFAULT_SIDES[1]] = "#2a6fb0"; SIDE_COLORS[DEFAULT_SIDES[2]] = "#0e6b63";
  var PALETTE = ["#8a5cc2", "#c06a12", "#2f8a3e", "#b3261e", "#1b7f9a", "#7a6a12"];
  var NO_TABLE = L("ללא שולחן", "No table");
  var NO_GROUP = L("ללא קבוצה", "No group");
  var TABLE_WORD = L("שולחן", "Table");
  var UNLOCK_TITLE = L("הגרסה המלאה של סידור ההושבה · ₪29", "Seating chart full version · $9");
  var UNLOCK_FEATS = L(
    ["PDF נקי בלי סימן מים (מפת שולחנות + רשימת כניסה לפי א-ב)", "ייצוא לאקסל: הושבה לפי שולחן, רשימת מוזמנים ושולחנות", "כרטיסי שולחן מוכנים להדפסה (מספר השולחן ושמות היושבים)", "תשלום חד-פעמי, לכל האירועים שתתכננו בדפדפן הזה"],
    ["Clean PDF without watermark (table map + A–Z escort list)", "Excel export: seating by table, guest list and tables", "Printable table cards (table number + guest names)", "One-time payment, for every event you plan in this browser"]);

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function uid() { return Math.random().toString(36).slice(2, 9); }
  function num(v, d) { var n = parseInt(v, 10); return isFinite(n) && n > 0 ? n : d; }
  var coll = (function () { try { return new Intl.Collator(L("he", "en")); } catch (e) { return { compare: function (a, b) { return a < b ? -1 : a > b ? 1 : 0; } }; } })();

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
  function flush() {
    clearTimeout(saveTimer); saveTimer = null;
    try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { toast(L("לא הצלחנו לשמור בדפדפן (אחסון מלא או חסום)", "Couldn't save in this browser (storage full or blocked)")); }
  }
  function save() { clearTimeout(saveTimer); saveTimer = setTimeout(flush, 150); }
  window.addEventListener("pagehide", function () { if (saveTimer) flush(); }); // don't lose the last edit when leaving quickly
  var undoStack = [];
  function mutate(fn) {
    undoStack.push(JSON.stringify(S));
    if (undoStack.length > 40) undoStack.shift();
    fn();
    save(); render();
  }
  function undo() {
    if (!undoStack.length) return toast(L("אין מה לבטל", "Nothing to undo"));
    S = JSON.parse(undoStack.pop()); save(); render(); toast(L("הפעולה האחרונה בוטלה", "Undone"));
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
    if (used > t.seats) out.push(L("חריגה: " + used + " אנשים ב-" + t.seats + " מקומות", "Over capacity: " + used + " people in " + t.seats + " seats"));
    for (var i = 0; i < gs.length; i++) for (var j = i + 1; j < gs.length; j++) {
      if (isApart(gs[i].id, gs[j].id)) out.push(L(gs[i].name + " ו" + gs[j].name + " ביקשו לא לשבת יחד", gs[i].name + " and " + gs[j].name + " should not sit together"));
    }
    return out;
  }
  function tableLabel(t) { return t ? t.name : NO_TABLE; }
  function totals() {
    var total = S.guests.reduce(function (s, g) { return s + g.n; }, 0);
    var un = S.guests.filter(function (g) { return !g.table; }).reduce(function (s, g) { return s + g.n; }, 0);
    return { total: total, un: un, seated: total - un };
  }

  /* ---------- parsing ---------- */
  var HEAD = {
    name: /^(שם|שם מלא|שם האורח|שם המוזמן|מוזמן|אורח|name|guest|guest name|full name|names?)$/i,
    n: /^(כמות|מספר|מס'|מס׳|מספר אנשים|מוזמנים|מאשרים|אנשים|count|qty|quantity|guests|party size|seats|people|#)$/i,
    side: /^(צד|side)$/i,
    group: /^(קבוצה|קטגוריה|שיוך|group|category|relationship)$/i,
    table: /^(שולחן|מס' שולחן|מספר שולחן|table|table number|table #)$/i
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
      // "משפחת כהן 4" / "The Cohens (4)" in a single cell
      if (map.n === undefined || !nRaw) {
        var m = /^(.*?)[\s(×x*]+(\d{1,2})\)?$/.exec(name);
        if (m && m[1].trim()) { name = m[1].trim(); n = num(m[2], 1); }
      }
      var tbl = map.table !== undefined ? String(r[map.table] || "").trim() : "";
      if (tbl === "ללא שולחן" || tbl === "No table") tbl = "";
      out.push({
        id: uid(), name: name.slice(0, 80), n: Math.min(n, 60),
        side: String((map.side !== undefined && r[map.side]) || defaults.side || "").trim().slice(0, 40),
        group: String((map.group !== undefined && r[map.group]) || defaults.group || "").trim().slice(0, 40),
        table: null, _table: tbl
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
    return text.split(/\r?\n/).filter(function (l) { return l.trim(); }).map(function (l) {
      if (l.indexOf("\t") >= 0) return l.split("\t");
      if (/[,;]/.test(l)) return l.split(/\s*[,;]\s*/);
      return [l];
    });
  }
  function addImported(list) {
    if (!list.length) { toast(L("לא נמצאו שמות לייבוא", "No names found to import")); return 0; }
    mutate(function () {
      list.forEach(function (g) {
        if (g._table) {
          var t = S.tables.filter(function (t) { return t.name === g._table || t.name === TABLE_WORD + " " + g._table; })[0];
          if (!t) { t = { id: uid(), name: /^\d+$/.test(g._table) ? TABLE_WORD + " " + g._table : g._table, seats: 10, shape: "round" }; S.tables.push(t); }
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
        var cands = S.tables.filter(function (t) { return free[t.id] >= c.total && okAll(c.gs, t.id); });
        if (cands.length) {
          cands.sort(function (a, b) { return (affinity(b.id, c.key) - affinity(a.id, c.key)) || (free[a.id] - free[b.id]); });
          var t = cands[0];
          c.gs.forEach(function (g) { g.table = t.id; placed += g.n; });
          free[t.id] -= c.total;
          return;
        }
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
    if (!S.tables.length) toast(L("קודם מוסיפים שולחנות", "Add tables first"));
    else if (missing) toast(L("שובצו " + placed + " אנשים. " + missing + " נשארו בלי מקום: הוסיפו שולחנות או מקומות.", "Seated " + placed + " people. " + missing + " still need a seat: add tables or seats."));
    else toast(L("שובצו " + placed + " אנשים. אפשר לגרור ולתקן ידנית (ובטל מחזיר אחורה).", "Seated " + placed + " people. Drag to adjust (Undo goes back)."));
  }

  /* ---------- rendering ---------- */
  var filter = { q: "", side: "", group: "" };
  function chip(g, inUnassigned) {
    var hit = filter.q && g.name.toLowerCase().indexOf(filter.q.toLowerCase()) >= 0;
    var hasApart = S.apart.some(function (p) { return p[0] === g.id || p[1] === g.id; });
    return '<button type="button" class="g-chip' + (hit ? " hit" : "") + '" data-gid="' + g.id + '" style="--side:' + sideColor(g.side) + '" title="' + esc(g.name + (g.side ? " · " + g.side : "") + (g.group ? " · " + g.group : "")) + '">' +
      '<span class="g-name">' + esc(g.name) + "</span>" +
      (g.n > 1 ? '<span class="g-n">' + g.n + "</span>" : "") +
      (hasApart ? '<span class="g-apart" title="' + L("יש בקשת הרחקה", "Keep-apart request") + '" aria-label="' + L("יש בקשת הרחקה", "Keep-apart request") + '">⇹</span>' : "") +
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
    $("#plan").innerHTML = unlocked ? L("✓ גרסה מלאה פעילה", "✓ Full version active") : L("גרסה חינמית", "Free version") + ' · <button type="button" data-act="unlock">' + L("מה בגרסה המלאה?", "What's in the full version?") + "</button>";
    $$("[data-paid]").forEach(function (b) { var l = b.querySelector(".lock"); if (l) l.hidden = !!unlocked; });
    if (document.activeElement !== $("#ev-title")) $("#ev-title").value = S.title || "";
    if (document.activeElement !== $("#ev-date")) $("#ev-date").value = S.date || "";

    $("#dl-sides").innerHTML = sides().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    $("#dl-groups").innerHTML = groups().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    $("#f-side").innerHTML = '<option value="">' + L("כל הצדדים", "All sides") + "</option>" + sides().map(function (s) { return "<option" + (s === filter.side ? " selected" : "") + ">" + esc(s) + "</option>"; }).join("");
    $("#f-group").innerHTML = '<option value="">' + L("כל הקבוצות", "All groups") + "</option>" + groups().map(function (s) { return "<option" + (s === filter.group ? " selected" : "") + ">" + esc(s) + "</option>"; }).join("");

    var un = S.guests.filter(function (g) {
      return !g.table && (!filter.side || g.side === filter.side) && (!filter.group || g.group === filter.group) &&
        (!filter.q || g.name.toLowerCase().indexOf(filter.q.toLowerCase()) >= 0);
    });
    var byGroup = {};
    un.forEach(function (g) { var k = g.group || NO_GROUP; (byGroup[k] = byGroup[k] || []).push(g); });
    var keys = Object.keys(byGroup).sort(function (a, b) { return a === NO_GROUP ? 1 : b === NO_GROUP ? -1 : coll.compare(a, b); });
    var T = totals();
    $("#un-count").textContent = T.un;
    $("#unassigned").innerHTML = keys.length ? keys.map(function (k) {
      var gs = byGroup[k].sort(function (a, b) { return coll.compare(a.name, b.name); });
      return '<div class="u-group"><div class="u-head">' + esc(k) + ' <span class="muted">(' + gs.reduce(function (s, g) { return s + g.n; }, 0) + ')</span></div><div class="chips">' + gs.map(function (g) { return chip(g, true); }).join("") + "</div></div>";
    }).join("") : '<p class="empty muted">' + (S.guests.length ? (T.un ? L("אין תוצאות לסינון הזה.", "No matches for this filter.") : L("כל המוזמנים שובצו 🎉", "Everyone is seated 🎉")) : L("עוד אין מוזמנים. הוסיפו שמות למעלה, הדביקו רשימה או ייבאו קובץ.", "No guests yet. Add names above, paste a list or import a file.")) + "</p>";

    var seatsTotal = S.tables.reduce(function (s, t) { return s + t.seats; }, 0);
    var conflicts = 0;
    $("#tables").innerHTML = S.tables.length ? S.tables.map(function (t) {
      var gs = tableGuests(t.id).sort(function (a, b) { return coll.compare(a.group || "", b.group || "") || coll.compare(a.name, b.name); });
      var used = gs.reduce(function (s, g) { return s + g.n; }, 0);
      var cf = conflictsOf(t); conflicts += cf.length;
      return '<article class="t-card' + (cf.length ? " conflict" : "") + (used === t.seats ? " full" : "") + '" data-tid="' + t.id + '">' +
        '<header><button type="button" class="t-name" data-edit-table="' + t.id + '" title="' + L("עריכת שולחן", "Edit table") + '">' + esc(t.name) + ' <span aria-hidden="true">✎</span></button>' +
        '<span class="t-occ' + (used > t.seats ? " over" : "") + '">' + used + "/" + t.seats + "</span></header>" +
        tableSvg(t, used) +
        '<div class="chips drop" data-drop="' + t.id + '">' + (gs.length ? gs.map(function (g) { return chip(g, false); }).join("") : '<span class="drop-hint">' + L("גררו לכאן מוזמנים", "Drag guests here") + "</span>") + "</div>" +
        (cf.length ? '<ul class="t-warn">' + cf.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul>" : "") +
        "</article>";
    }).join("") : '<div class="empty-tables"><p>' + L("עוד אין שולחנות.", "No tables yet.") + '</p><button type="button" class="btn" data-act="add-tables">' + L("הוספת שולחנות", "Add tables") + "</button></div>";

    $("#stats").innerHTML =
      stat(T.total, L("מוזמנים", "guests")) + stat(T.seated, L("שובצו", "seated")) + stat(T.un, L("בלי שולחן", "unseated"), T.un ? "warn" : "") +
      stat(S.tables.length, L("שולחנות", "tables")) + stat(Math.max(0, seatsTotal - T.seated), L("מקומות פנויים", "free seats")) +
      stat(conflicts, L("התנגשויות", "conflicts"), conflicts ? "bad" : "");
    var need = T.total - seatsTotal;
    $("#capacity-hint").textContent = need > 0 ? L("חסרים " + need + " מקומות לכל המוזמנים (" + Math.ceil(need / 10) + " שולחנות של 10).", need + " more seats needed (" + Math.ceil(need / 10) + " tables of 10).") : "";

    // "chart ready" banner: export + WhatsApp share once everyone is seated without conflicts
    var ready = T.total > 0 && T.un === 0 && S.tables.length > 0 && conflicts === 0;
    var banner = $("#ready");
    banner.hidden = !ready;
    if (ready) {
      banner.innerHTML = '<div><strong>' + L("סידור ההושבה מוכן 🎉", "Your seating chart is ready 🎉") + "</strong> " +
        '<span class="muted">' + L(T.total + " אורחים ב-" + S.tables.length + " שולחנות", T.total + " guests at " + S.tables.length + " tables") + "</span></div>" +
        '<div class="btn-row">' +
        (unlocked
          ? '<button type="button" class="btn small" data-act="pdf-clean">' + L("PDF להדפסה", "Print / PDF") + '</button><button type="button" class="btn small secondary" data-act="xlsx">' + L("אקסל", "Excel") + '</button><button type="button" class="btn small secondary" data-act="cards">' + L("כרטיסי שולחן", "Table cards") + "</button>"
          : '<button type="button" class="btn small accent" data-act="pdf-clean">' + L("PDF נקי + אקסל + כרטיסים · ", "Clean PDF + Excel + cards · ") + PRICE + '</button><button type="button" class="btn small secondary" data-act="print">' + L("PDF חינם (עם סימן מים)", "Free PDF (watermarked)") + "</button>") +
        '<a class="btn small wa" data-act="whatsapp" href="' + esc(waUrl()) + '" target="_blank" rel="noopener">' + WA_ICON + L("שיתוף בוואטסאפ", "Share on WhatsApp") + "</a></div>";
    }
  }
  function stat(v, l, cls) { return '<div class="stat ' + (cls || "") + '"><b class="num">' + v + "</b><span>" + l + "</span></div>"; }

  /* ---------- WhatsApp share (wa.me; text + link to the free tool, never the guest list) ---------- */
  var WA_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3 1 2.5c.1.2 1.6 2.5 4 3.5 1.5.6 2 .7 2.8.6.4-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.4z"/></svg>';
  function waUrl() {
    var T = totals();
    var link = APP_URL + "?utm_source=whatsapp&utm_medium=share&utm_campaign=seating";
    var text = L(
      "סיימנו את סידורי ההושבה" + (S.title ? " ל" + S.title : "") + " 🎉 " + T.total + " אורחים ב-" + S.tables.length + " שולחנות. עשינו את זה בכלי חינמי בעברית, בלי הרשמה: ",
      "Our seating chart" + (S.title ? " for " + S.title : "") + " is done 🎉 " + T.total + " guests at " + S.tables.length + " tables. Made it with this free tool, no sign-up: ");
    return "https://wa.me/?text=" + encodeURIComponent(text + link);
  }

  /* ---------- dialogs ---------- */
  function dialog(html, onSubmit, onReady) {
    var d = document.createElement("dialog");
    d.className = "app-dialog";
    d.innerHTML = '<form method="dialog" class="dlg-close-row"><button class="dlg-x" aria-label="' + L("סגירה", "Close") + '" value="close">×</button></form>' + html;
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
    return '<option value="">' + NO_TABLE + "</option>" + S.tables.map(function (t) {
      return '<option value="' + t.id + '"' + (t.id === sel ? " selected" : "") + ">" + esc(t.name) + " (" + load_(t.id) + "/" + t.seats + ")</option>";
    }).join("");
  }

  function editGuest(id) {
    var g = guest(id); if (!g) return;
    var apartList = function () {
      return S.apart.filter(function (p) { return p[0] === id || p[1] === id; }).map(function (p) {
        var o = guest(p[0] === id ? p[1] : p[0]);
        return o ? "<li>" + esc(o.name) + ' <button type="button" class="btn tiny ghost" data-unapart="' + o.id + '">' + L("הסרה", "Remove") + "</button></li>" : "";
      }).join("");
    };
    var others = S.guests.filter(function (o) { return o.id !== id; }).sort(function (a, b) { return coll.compare(a.name, b.name); });
    dialog(
      "<h2>" + L("עריכת מוזמן", "Edit guest") + '</h2><form class="dlg-form">' +
      '<div class="fields cols-2"><div class="field"><label for="eg-name">' + L("שם", "Name") + '</label><input id="eg-name" name="name" type="text" required maxlength="80" value="' + esc(g.name) + '"></div>' +
      '<div class="field"><label for="eg-n">' + L("מספר אנשים", "Party size") + '</label><input id="eg-n" name="n" type="number" min="1" max="60" value="' + g.n + '"></div>' +
      '<div class="field"><label for="eg-side">' + L("צד", "Side") + '</label><input id="eg-side" name="side" type="text" list="dl-sides" maxlength="40" value="' + esc(g.side) + '"></div>' +
      '<div class="field"><label for="eg-group">' + L("קבוצה", "Group") + '</label><input id="eg-group" name="group" type="text" list="dl-groups" maxlength="40" value="' + esc(g.group) + '"></div></div>' +
      '<div class="field"><label for="eg-table">' + L("שולחן", "Table") + '</label><select id="eg-table" name="table">' + tableOptions(g.table) + "</select></div>" +
      '<div class="field"><span class="label">' + L("לא להושיב באותו שולחן עם", "Keep apart from (not at the same table)") + '</span><ul class="apart-list">' + apartList() + "</ul>" +
      '<div class="btn-row"><select id="eg-apart" aria-label="' + L("בחירת מוזמן להרחקה", "Choose a guest to keep apart") + '" style="flex:1"><option value="">' + L("בחרו מוזמן…", "Choose a guest…") + "</option>" +
      others.map(function (o) { return '<option value="' + o.id + '">' + esc(o.name) + "</option>"; }).join("") +
      '</select><button type="button" class="btn ghost small" id="eg-apart-add">' + L("הוספה", "Add") + "</button></div></div>" +
      '<div class="dlg-actions"><button class="btn" type="submit">' + L("שמירה", "Save") + '</button><button class="btn ghost" type="button" data-close>' + L("ביטול", "Cancel") + '</button><span class="spacer"></span><button class="btn danger" type="button" id="eg-del">' + L("מחיקה", "Delete") + "</button></div></form>",
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
          if (!confirm(L("למחוק את " + g.name + "?", "Delete " + g.name + "?"))) return;
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
    var T = totals();
    var seatsTotal = S.tables.reduce(function (s, t) { return s + t.seats; }, 0);
    var suggest = Math.max(1, Math.ceil(Math.max(0, T.total - seatsTotal) / 10)) || 1;
    var nextNum = S.tables.reduce(function (m, t) { var k = parseInt(shortName(t.name), 10); return isFinite(k) && k > m ? k : m; }, 0) + 1;
    dialog(
      "<h2>" + L("הוספת שולחנות", "Add tables") + '</h2><form class="dlg-form">' +
      '<div class="fields cols-3"><div class="field"><label for="at-count">' + L("כמה שולחנות", "How many") + '</label><input id="at-count" name="count" type="number" min="1" max="100" value="' + suggest + '"></div>' +
      '<div class="field"><label for="at-seats">' + L("מקומות בשולחן", "Seats per table") + '</label><input id="at-seats" name="seats" type="number" min="1" max="40" value="10"></div>' +
      '<div class="field"><label for="at-shape">' + L("צורה", "Shape") + '</label><select id="at-shape" name="shape"><option value="round">' + L("עגול", "Round") + '</option><option value="rect">' + L("מלבני", "Rectangular") + "</option></select></div></div>" +
      '<div class="fields cols-2"><div class="field"><label for="at-prefix">' + L("שם", "Name") + '</label><input id="at-prefix" name="prefix" type="text" value="' + TABLE_WORD + '" maxlength="30"></div>' +
      '<div class="field"><label for="at-start">' + L("מספור החל מ-", "Number from") + '</label><input id="at-start" name="start" type="number" min="0" max="999" value="' + nextNum + '"></div></div>' +
      (T.total ? '<p class="small muted">' + L("יש " + T.total + " מוזמנים ו-" + seatsTotal + " מקומות. ההצעה מחושבת לשולחנות של 10.", "You have " + T.total + " guests and " + seatsTotal + " seats. The suggestion assumes tables of 10.") + "</p>" : "") +
      '<p class="small muted">' + L("שולחן אבירים או שולחן מיוחד? הוסיפו שולחן אחד ושנו לו את השם והמקומות בלחיצה על השם.", "Head table or sweetheart table? Add one table, then click its name to rename it and change the seats.") + "</p>" +
      '<div class="dlg-actions"><button class="btn" type="submit">' + L("הוספה", "Add") + "</button></div></form>",
      function (f) {
        var c = Math.min(num(f.count.value, 1), 100), seats = Math.min(num(f.seats.value, 10), 40), start = parseInt(f.start.value, 10) || 1;
        var prefix = f.prefix.value.trim() || TABLE_WORD;
        mutate(function () {
          for (var i = 0; i < c; i++) S.tables.push({ id: uid(), name: (prefix + " " + (start + i)).slice(0, 40), seats: seats, shape: f.shape.value === "rect" ? "rect" : "round" });
        });
      });
  }

  function editTable(tid) {
    var t = table(tid); if (!t) return;
    dialog(
      "<h2>" + L("עריכת שולחן", "Edit table") + '</h2><form class="dlg-form">' +
      '<div class="fields cols-3"><div class="field"><label for="et-name">' + L("שם", "Name") + '</label><input id="et-name" name="name" type="text" required maxlength="40" value="' + esc(t.name) + '"></div>' +
      '<div class="field"><label for="et-seats">' + L("מקומות", "Seats") + '</label><input id="et-seats" name="seats" type="number" min="1" max="40" value="' + t.seats + '"></div>' +
      '<div class="field"><label for="et-shape">' + L("צורה", "Shape") + '</label><select id="et-shape" name="shape"><option value="round"' + (t.shape !== "rect" ? " selected" : "") + ">" + L("עגול", "Round") + '</option><option value="rect"' + (t.shape === "rect" ? " selected" : "") + ">" + L("מלבני", "Rectangular") + "</option></select></div></div>" +
      '<div class="dlg-actions"><button class="btn" type="submit">' + L("שמירה", "Save") + '</button><button class="btn ghost" type="button" id="et-clear">' + L("פינוי השולחן", "Clear table") + '</button><span class="spacer"></span><button class="btn danger" type="button" id="et-del">' + L("מחיקת שולחן", "Delete table") + "</button></div></form>",
      function (f) {
        mutate(function () { t.name = f.name.value.trim().slice(0, 40) || t.name; t.seats = Math.min(num(f.seats.value, t.seats), 40); t.shape = f.shape.value === "rect" ? "rect" : "round"; });
      },
      function (d) {
        d.querySelector("#et-clear").addEventListener("click", function () { mutate(function () { tableGuests(tid).forEach(function (g) { g.table = null; }); }); d.close(); });
        d.querySelector("#et-del").addEventListener("click", function () {
          if (!confirm(L("למחוק את " + t.name + "? היושבים בו יחזרו לרשימת 'בלי שולחן'.", "Delete " + t.name + "? Its guests go back to the unseated list."))) return;
          mutate(function () { tableGuests(tid).forEach(function (g) { g.table = null; }); S.tables = S.tables.filter(function (x) { return x.id !== tid; }); });
          d.close();
        });
      });
  }

  function pasteDialog() {
    dialog(
      "<h2>" + L("הדבקת רשימת מוזמנים", "Paste a guest list") + '</h2><form class="dlg-form">' +
      '<div class="field"><label for="pd-text">' + L("שורה לכל הזמנה", "One line per invitation") + '</label><textarea id="pd-text" name="text" rows="9" placeholder="' +
      L("משפחת כהן, 4&#10;דנה ואורי לוי, 2, צד הכלה, חברים מהצבא&#10;סבתא רחל", "The Cohen family, 4&#10;Dana &amp; Ori Levy, 2, Bride's side, College friends&#10;Grandma Ruth") + '"></textarea>' +
      '<span class="hint">' + L("אפשר להדביק עמודות ישירות מאקסל או מ-Google Sheets. סדר העמודות: שם, מספר אנשים, צד, קבוצה (רק השם חובה). אם יש שורת כותרות (שם, כמות, צד, קבוצה, שולחן) היא תזוהה.",
        "Paste columns straight from Excel or Google Sheets. Column order: name, party size, side, group (only the name is required). A header row (Name, Count, Side, Group, Table) is detected.") + "</span></div>" +
      '<div class="fields cols-2"><div class="field"><label for="pd-side">' + L("צד (לכל מי שאין לו)", "Side (for rows without one)") + '</label><input id="pd-side" name="side" type="text" list="dl-sides"></div>' +
      '<div class="field"><label for="pd-group">' + L("קבוצה (לכל מי שאין לו)", "Group (for rows without one)") + '</label><input id="pd-group" name="group" type="text" list="dl-groups"></div></div>' +
      '<div class="dlg-actions"><button class="btn" type="submit">' + L("הוספה לרשימה", "Add to list") + "</button></div></form>",
      function (f) {
        var n = addImported(rowsToGuests(parsePaste(f.text.value), { side: f.side.value.trim(), group: f.group.value.trim() }));
        if (n) toast(L("נוספו " + n + " הזמנות", n + " invitations added"));
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
        if (!confirm(L("לשחזר מהגיבוי? הנתונים הנוכחיים בכלי יוחלפו.", "Restore this backup? The current chart will be replaced."))) return;
        mutate(function () { S = data; S.apart = S.apart || []; });
        toast(L("הגיבוי שוחזר", "Backup restored"));
        return;
      }
      if (/\.xlsx$/.test(name)) {
        return AppZip.readSheet(buf).then(function (rows) { var n = addImported(rowsToGuests(rows)); if (n) toast(L("יובאו " + n + " הזמנות מהאקסל", n + " invitations imported from Excel")); });
      }
      if (/\.xls$/.test(name)) throw new Error("xls");
      var text;
      try { text = new TextDecoder("utf-8", { fatal: true }).decode(buf); } catch (e) { text = new TextDecoder(EN ? "windows-1252" : "windows-1255").decode(buf); }
      text = text.replace(/^﻿/, "");
      var n = addImported(rowsToGuests(parseCSV(text)));
      if (n) toast(L("יובאו " + n + " הזמנות", n + " invitations imported"));
    }).catch(function (e) {
      if (window.console) console.error(e);
      toast(e && e.message === "xls" ? L("קובץ XLS ישן: שמרו אותו כ-XLSX או CSV ונסו שוב", "Old .xls file: save it as .xlsx or .csv and try again") : L("לא הצלחנו לקרוא את הקובץ. נסו לשמור אותו כ-CSV או להדביק את הרשימה.", "Couldn't read that file. Try saving it as CSV, or paste the list."));
    });
  }

  function demo() {
    if (S.guests.length && !confirm(L("לטעון דוגמה? הנתונים הנוכחיים יוחלפו (אפשר לבטל עם 'בטל').", "Load the example? Your current chart will be replaced (Undo brings it back)."))) return;
    var rows = EN ? [
      ["Bride's parents", 2, "Bride's side", "Immediate family"], ["Grandma Esther", 1, "Bride's side", "Immediate family"], ["Noa & Ethan (sister)", 2, "Bride's side", "Immediate family"], ["The Abrams family", 4, "Bride's side", "Immediate family"],
      ["David & Rina Levy", 2, "Bride's side", "Extended family"], ["The Perez family", 5, "Bride's side", "Extended family"], ["Yael & Moshe Gabay", 2, "Bride's side", "Extended family"], ["The Hadad family", 4, "Bride's side", "Extended family"],
      ["Shira Katz", 1, "Bride's side", "High school friends"], ["Maya & Ido", 2, "Bride's side", "High school friends"], ["Lior Shemesh", 1, "Bride's side", "High school friends"], ["Tal & Guy", 2, "Bride's side", "High school friends"], ["Roni Adler", 1, "Bride's side", "High school friends"],
      ["Hila from work", 2, "Bride's side", "Work"], ["Orna (manager)", 2, "Bride's side", "Work"], ["Karen & Nir", 2, "Bride's side", "Work"], ["Amit", 1, "Bride's side", "Work"],
      ["Groom's parents", 2, "Groom's side", "Immediate family"], ["Grandpa Joe & Grandma Miriam", 2, "Groom's side", "Immediate family"], ["Groom's brother & family", 4, "Groom's side", "Immediate family"],
      ["The Mizrahi family", 4, "Groom's side", "Extended family"], ["Aunt Susan", 1, "Groom's side", "Extended family"], ["The Bitton family", 5, "Groom's side", "Extended family"], ["Rafi & Dalia", 2, "Groom's side", "Extended family"],
      ["Jonathan", 1, "Groom's side", "Camp friends"], ["Alon & Shani", 2, "Groom's side", "Camp friends"], ["Roy", 1, "Groom's side", "Camp friends"], ["Omer & Noga", 2, "Groom's side", "Camp friends"], ["Ben", 1, "Groom's side", "Camp friends"], ["Asaf", 1, "Groom's side", "Camp friends"],
      ["Daniel & Rotem", 2, "Groom's side", "College"], ["Matan", 1, "Groom's side", "College"], ["Sapir & Aviv", 2, "Groom's side", "College"], ["Gilad", 1, "Groom's side", "College"],
      ["The neighbors", 2, "Both", "Neighbors"], ["The Ohayon family", 3, "Both", "Neighbors"], ["Rabbi & Rebbetzin", 2, "Both", "Community"]
    ] : [
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
    S.title = L("החתונה של נועם ושירה", "Noam & Shira's wedding");
    rows.forEach(function (r) { S.guests.push({ id: uid(), name: r[0], n: r[1], side: r[2], group: r[3], table: null }); });
    S.tables.push({ id: uid(), name: TABLE_WORD + " 1", seats: 12, shape: "rect" });
    for (var i = 2; i <= 8; i++) S.tables.push({ id: uid(), name: TABLE_WORD + " " + i, seats: 10, shape: "round" });
    var a = S.guests[5], b = S.guests[7]; // Perez / Hadad: keep apart
    S.apart.push([a.id, b.id]);
    save(); render();
    toast(L("נטענה דוגמה: לחצו 'הושבה אוטומטית' כדי לראות הצעה", "Example loaded: click 'Auto-seat' to see a suggestion"));
  }

  /* ---------- exports ---------- */
  function guestsAlpha() { return S.guests.slice().sort(function (a, b) { return coll.compare(a.name, b.name); }); }
  function fmtDate(d) { try { return new Date(d + "T12:00:00").toLocaleDateString(L("he-IL", "en-US"), { weekday: "long", day: "numeric", month: "long", year: "numeric" }); } catch (e) { return d; } }
  function printChart(clean) {
    var T = totals();
    var html = (clean ? "" : watermark()) +
      '<div class="p-head"><h1>' + esc(S.title || L("סידור הושבה", "Seating chart")) + "</h1>" + (S.date ? "<p>" + esc(fmtDate(S.date)) + "</p>" : "") + "</div>" +
      '<p class="p-sum">' + L(T.total + " מוזמנים · " + S.tables.length + " שולחנות", T.total + " guests · " + S.tables.length + " tables") + "</p>" +
      '<div class="p-tables">' + S.tables.map(function (t) {
        var gs = tableGuests(t.id).sort(function (a, b) { return coll.compare(a.name, b.name); });
        return '<div class="p-table"><h2>' + esc(t.name) + " <small>(" + load_(t.id) + "/" + t.seats + ")</small></h2><ul>" +
          gs.map(function (g) { return "<li>" + esc(g.name) + (g.n > 1 ? " <small>(" + g.n + ")</small>" : "") + "</li>"; }).join("") + "</ul></div>";
      }).join("") + "</div>" +
      '<div class="p-index"><h2>' + L("רשימת כניסה לפי א-ב", "Escort list (A–Z)") + "</h2><table><thead><tr><th>" + L("שם", "Name") + "</th><th>" + L("אנשים", "Party") + "</th><th>" + L("שולחן", "Table") + "</th></tr></thead><tbody>" +
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
    doPrint(html || "<p>" + L("אין שולחנות.", "No tables.") + "</p>", "cards");
  }
  function watermark() {
    var s = "", w = L("תכנון פלוס · גרסה חינמית", "Tichnun Plus · free version");
    for (var i = 0; i < 18; i++) s += "<span>" + w + "</span>";
    return '<div class="wm" aria-hidden="true">' + s + '</div><div class="wm-foot">' +
      L("נוצר בגרסה החינמית של תכנון פלוס · tichnun.netlify.app/apps/seating · לגרסה נקייה: פתיחת הגרסה המלאה בכלי",
        "Made with the free version of Tichnun Plus · tichnun.netlify.app/en/apps/seating · unlock the full version for a clean copy") + "</div>";
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
    var H = L(["שולחן", "מקומות", "שם", "אנשים", "צד", "קבוצה"], ["Table", "Seats", "Name", "Party", "Side", "Group"]);
    var byTable = [[L("סידור הושבה: ", "Seating chart: ") + (S.title || "")], H];
    S.tables.forEach(function (t) {
      tableGuests(t.id).sort(function (a, b) { return coll.compare(a.name, b.name); }).forEach(function (g) {
        byTable.push([t.name, t.seats, g.name, g.n, g.side || "", g.group || ""]);
      });
    });
    S.guests.filter(function (g) { return !g.table; }).forEach(function (g) { byTable.push([NO_TABLE, "", g.name, g.n, g.side || "", g.group || ""]); });
    var guestsSheet = [L(["שם", "אנשים", "צד", "קבוצה", "שולחן"], ["Name", "Party", "Side", "Group", "Table"])].concat(guestsAlpha().map(function (g) { return [g.name, g.n, g.side || "", g.group || "", tableLabel(table(g.table))]; }));
    var tablesSheet = [L(["שולחן", "צורה", "מקומות", "תפוסה", "פנוי"], ["Table", "Shape", "Seats", "Taken", "Free"])].concat(S.tables.map(function (t) { var u = load_(t.id); return [t.name, t.shape === "rect" ? L("מלבני", "Rectangular") : L("עגול", "Round"), t.seats, u, t.seats - u]; }));
    var blob = AppZip.xlsx({ sheets: [
      { name: L("הושבה לפי שולחן", "By table"), rows: byTable, cols: [14, 9, 28, 8, 14, 18], title: [0], header: [1], freeze: 2, autoFilter: 2, rtl: !EN },
      { name: L("רשימת כניסה א-ב", "Escort list A-Z"), rows: guestsSheet, cols: [28, 8, 14, 18, 14], header: [0], freeze: 1, autoFilter: 1, rtl: !EN },
      { name: L("שולחנות", "Tables"), rows: tablesSheet, cols: [16, 12, 10, 10, 10], header: [0], freeze: 1, rtl: !EN }
    ] });
    AppZip.download(blob, fileBase() + ".xlsx");
    toast(L("קובץ האקסל ירד", "Excel file downloaded"));
  }
  function fileBase() { return ("seating-" + (S.title || "event")).replace(/[\\\/:*?"<>|]+/g, "").replace(/\s+/g, "-").slice(0, 60); }
  function backup() {
    AppZip.download(new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }), fileBase() + "-backup.json");
    toast(L("קובץ הגיבוי ירד. שמרו אותו כדי לשחזר בכל דפדפן.", "Backup downloaded. Keep it to restore in any browser."));
  }
  function paid(fn, reason) {
    return function () { if (AppUnlock.require(SLUG, { title: UNLOCK_TITLE, reason: reason, features: UNLOCK_FEATS })) fn(); };
  }

  var toastTimer;
  function toast(msg) {
    var t = $("#toast");
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove("show"); }, 3600);
  }

  /* ---------- drag & drop (pointer events: mouse + touch long-press) ---------- */
  var drag = null, suppressClick = false;
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
      pending = { ch: ch, x: e.clientX, y: e.clientY, touch: e.pointerType !== "mouse", started: false };
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
    document.addEventListener("pointerup", function () {
      if (!pending) return;
      clearTimeout(pending.timer);
      var p = pending; pending = null;
      if (p.started) { endDrag(); suppressClick = true; setTimeout(function () { suppressClick = false; }, 50); }
    });
    document.addEventListener("pointercancel", function () { if (pending) { clearTimeout(pending.timer); if (pending.started) endDrag(); pending = null; } });
    root.addEventListener("contextmenu", function (e) { if (e.target.closest(".g-chip")) e.preventDefault(); });
  }

  /* ---------- wiring ---------- */
  function init() {
    if (!document.getElementById("toast")) { var t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    var app = $("#app");
    bindDrag(app);
    var unlockDlg = function () { AppUnlock.open(SLUG, { title: UNLOCK_TITLE, features: UNLOCK_FEATS }); };
    var acts = {
      "add-tables": addTables, "paste": pasteDialog, "auto": function () { autoSeat(false); },
      "auto-all": function () { if (confirm(L("לבטל את כל השיבוצים ולהושיב מחדש את כולם?", "Clear all seats and auto-seat everyone again?"))) autoSeat(true); },
      "clear-seats": function () { if (confirm(L("להוציא את כולם מהשולחנות? (אפשר לבטל)", "Unseat everyone? (You can undo)"))) mutate(function () { S.guests.forEach(function (g) { g.table = null; }); }); },
      "undo": undo, "demo": demo, "backup": backup,
      "restore": function () { $("#file-json").click(); },
      "import": function () { $("#file-in").click(); },
      "reset": function () { if (confirm(L("למחוק את כל הנתונים בכלי? (מומלץ לשמור גיבוי קודם)", "Delete everything in the tool? (Save a backup first)"))) mutate(function () { S = blank(); }); },
      "print": function () {
        var full = AppUnlock.isUnlocked(SLUG);
        printChart(full);
        if (!full && AppUnlock.nudge) setTimeout(function () { // R6B: after the free watermarked export, a clear (non-blocking) upgrade message
          AppUnlock.nudge(SLUG, { anchor: "#app > :first-child", title: L("ה-PDF החינמי יוצא עם סימן מים.", "The free PDF has a watermark."),
            text: L("לאולם ולדפוס: PDF נקי, ייצוא לאקסל וכרטיסי שולחן בתשלום חד-פעמי של " + PRICE + ".", "For the venue and printing: a clean PDF, Excel export and table cards for a one-time " + PRICE + "."),
            cta: L("PDF נקי + אקסל + כרטיסים · " + PRICE, "Clean PDF + Excel + cards · " + PRICE),
            dialog: { title: UNLOCK_TITLE, reason: L("PDF נקי בלי סימן מים, מוכן לשליחה לאולם ולהדפסה.", "A clean PDF without watermark, ready for the venue and for printing."), features: UNLOCK_FEATS } });
        }, 700);
      },
      "pdf-clean": paid(function () { printChart(true); }, L("PDF נקי בלי סימן מים, מוכן לשליחה לאולם ולהדפסה.", "A clean PDF without watermark, ready for the venue and for printing.")),
      "xlsx": paid(exportXlsx, L("ייצוא לאקסל עם הושבה לפי שולחן ורשימת כניסה לפי א-ב.", "Excel export with seating by table and an A–Z escort list.")),
      "cards": paid(printCards, L("כרטיסי שולחן גדולים להדפסה: מספר השולחן ושמות היושבים.", "Large printable table cards: table number and guest names.")),
      "unlock": unlockDlg
    };
    document.addEventListener("click", function (e) {
      if (suppressClick) return;
      var inApp = app.contains(e.target);
      if (inApp) {
        var ch = e.target.closest(".g-chip"); if (ch) return editGuest(ch.getAttribute("data-gid"));
        var et = e.target.closest("[data-edit-table]"); if (et) return editTable(et.getAttribute("data-edit-table"));
      }
      var a = e.target.closest("[data-act]");
      if (a && (inApp || a.closest("#plan, .app-info"))) {
        var act = a.getAttribute("data-act");
        var menu = a.closest("details"); if (menu) menu.open = false;
        if (act === "whatsapp") return; // plain link to wa.me
        e.preventDefault();
        (acts[act] || function () {})();
      }
      $$("details.menu[open]").forEach(function (m) { if (!m.contains(e.target)) m.open = false; });
    });
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
    $$(".app-tabs [data-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".app-tabs [data-tab]").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
        $(".seat-layout").setAttribute("data-show", b.getAttribute("data-tab"));
      });
    });
    AppUnlock.onChange(function () { render(); });
    render();
    if (!EN) fromRsvp();
    if (new URLSearchParams(location.search).get("demo") === "1" && !S.guests.length) demo();
  }

  /* Hand-off from the RSVP app (apps/rsvp/): localStorage "tp-handoff:seating" = {from, t, title, date, guests:[{name,n,side,group}]}.
   * Merged by name: existing guests keep their table and get the new count/side/group; new names are added unseated. */
  function fromRsvp() {
    var raw = null;
    try { raw = JSON.parse(localStorage.getItem("tp-handoff:seating") || "null"); localStorage.removeItem("tp-handoff:seating"); } catch (e) {}
    if (!raw || !Array.isArray(raw.guests)) return;
    var added = 0, updated = 0;
    mutate(function () {
      if (!S.title && raw.title) S.title = String(raw.title).slice(0, 80);
      if (!S.date && raw.date) S.date = String(raw.date).slice(0, 10);
      raw.guests.forEach(function (x) {
        var name = String(x.name || "").trim().slice(0, 80); if (!name) return;
        var n = Math.min(num(x.n, 1), 60);
        var g = S.guests.filter(function (y) { return y.name === name; })[0];
        if (g) { g.n = n; if (x.side) g.side = String(x.side).slice(0, 40); if (x.group) g.group = String(x.group).slice(0, 40); updated++; }
        else { S.guests.push({ id: uid(), name: name, n: n, side: String(x.side || "").slice(0, 40), group: String(x.group || "").slice(0, 40), table: null }); added++; }
      });
    });
    $("#ev-title").value = S.title || ""; $("#ev-date").value = S.date || "";
    toast("הגיעו " + (added + updated) + " הזמנות מרשימת המוזמנים" + (updated ? " (" + updated + " עודכנו)" : "") + (S.tables.length ? "" : ". עכשיו מוסיפים שולחנות ולוחצים \"הושבה אוטומטית\"."));
  }

  window.SeatingApp = { state: function () { return S; }, autoSeat: autoSeat, render: render, demo: demo, parseCSV: parseCSV, rowsToGuests: rowsToGuests, waUrl: waUrl };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
