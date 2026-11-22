/* תכנון פלוס — רשימת מוזמנים ואישורי הגעה (client-side only; data in localStorage "tp-rsvp-v1").
 * Free: up to FREE_MAX invitations (rows), all features incl. WhatsApp reminders, import, backup and one-click
 * hand-off to the seating app. Paid (product "rsvp-tracker", ₪29 one-time): unlimited invitations + Excel export.
 * Hand-off to apps/seating: localStorage "tp-handoff:seating" = {from:"rsvp", t, title, date, guests:[{name,n,side,group}]}
 * then navigate to ../seating/?from=rsvp (the seating app merges it by name and removes the key).
 */
(function () {
  "use strict";
  var SLUG = "rsvp-tracker", KEY = "tp-rsvp-v1", HANDOFF = "tp-handoff:seating", FREE_MAX = 80;
  var DEFAULT_SIDES = ["צד הכלה", "צד החתן", "משותף"];
  var STATUS = { pending: "טרם ענו", yes: "מגיעים", maybe: "אולי", no: "לא מגיעים" };
  var MEALS = [["veg", "צמחוני"], ["vegan", "טבעוני"], ["gf", "ללא גלוטן"], ["kids", "מנת ילדים"]];
  var DEFAULT_MSG = "היי {שם}! מזכירים בשמחה: {אירוע}{תאריך}. נשמח לדעת אם אתם מגיעים ובכמה אנשים 🙏";
  var UNLOCK_TITLE = "רשימת מוזמנים ואישורי הגעה – גרסה מלאה · ₪29";
  var UNLOCK_FEATS = ["מספר הזמנות בלי הגבלה (בחינם: עד " + FREE_MAX + ")", "ייצוא לאקסל: כל הרשימה, סיכום מנות לפי צד, ורשימת מי שעוד לא ענה עם טלפונים", "תשלום חד-פעמי, בלי מנוי ובלי הרשמה", "הנתונים נשארים רק אצלכם בדפדפן"];

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function uid() { return Math.random().toString(36).slice(2, 9); }
  function int(v, d) { var n = parseInt(v, 10); return isFinite(n) && n >= 0 ? n : d; }
  var coll = (function () { try { return new Intl.Collator("he"); } catch (e) { return { compare: function (a, b) { return a < b ? -1 : a > b ? 1 : 0; } }; } })();

  /* ---------- state ---------- */
  function blank() { return { v: 1, title: "", date: "", msg: "", guests: [] }; }
  var S = load();
  function load() {
    try { var s = JSON.parse(localStorage.getItem(KEY) || "null"); if (s && Array.isArray(s.guests)) return s; } catch (e) {}
    return blank();
  }
  var saveTimer = null;
  function flush() {
    clearTimeout(saveTimer); saveTimer = null;
    try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { toast("לא הצלחנו לשמור בדפדפן (אחסון מלא או חסום)"); }
  }
  function save() { clearTimeout(saveTimer); saveTimer = setTimeout(flush, 120); }
  window.addEventListener("pagehide", function () { if (saveTimer) flush(); });
  var undoStack = [];
  function mutate(fn) { undoStack.push(JSON.stringify(S)); if (undoStack.length > 40) undoStack.shift(); fn(); save(); render(); }
  function undo() { if (!undoStack.length) return toast("אין מה לבטל"); S = JSON.parse(undoStack.pop()); save(); render(); toast("הפעולה האחרונה בוטלה"); }
  function guest(id) { for (var i = 0; i < S.guests.length; i++) if (S.guests[i].id === id) return S.guests[i]; return null; }
  function unlocked() { return window.AppUnlock && AppUnlock.isUnlocked(SLUG); }
  function room() { return unlocked() ? Infinity : Math.max(0, FREE_MAX - S.guests.length); }
  function newGuest(o) {
    return { id: uid(), name: String(o.name || "").trim().slice(0, 80), n: Math.min(int(o.n, 1) || 1, 60), side: String(o.side || "").trim().slice(0, 40),
      group: String(o.group || "").trim().slice(0, 40), phone: String(o.phone || "").trim().slice(0, 30), status: o.status || "pending",
      coming: o.coming == null || o.coming === "" ? null : Math.min(int(o.coming, 0), 60), veg: 0, vegan: 0, gf: 0, kids: 0, note: String(o.note || "").slice(0, 200), sent: 0 };
  }
  function coming(g) { return g.status === "yes" ? (g.coming == null ? g.n : g.coming) : 0; }
  function sides() { var out = DEFAULT_SIDES.slice(); S.guests.forEach(function (g) { if (g.side && out.indexOf(g.side) < 0) out.push(g.side); }); return out; }
  function groups() { var out = []; S.guests.forEach(function (g) { if (g.group && out.indexOf(g.group) < 0) out.push(g.group); }); return out.sort(coll.compare); }

  function totals(list) {
    list = list || S.guests;
    var t = { rows: list.length, invited: 0, yes: 0, no: 0, maybe: 0, pending: 0, rowsPending: 0, veg: 0, vegan: 0, gf: 0, kids: 0 };
    list.forEach(function (g) {
      t.invited += g.n;
      if (g.status === "yes") { t.yes += coming(g); MEALS.forEach(function (m) { t[m[0]] += int(g[m[0]], 0); }); }
      else if (g.status === "no") t.no += g.n;
      else if (g.status === "maybe") t.maybe += g.n;
      else { t.pending += g.n; t.rowsPending++; }
    });
    t.regular = Math.max(0, t.yes - t.veg - t.vegan - t.gf - t.kids);
    // expected arrivals: confirmed + half of "maybe" + 75% of no answer yet (typical Israeli arrival rate 70–85%)
    t.expected = Math.round(t.yes + t.maybe * 0.5 + t.pending * 0.75);
    return t;
  }

  /* ---------- parsing ---------- */
  var HEAD = {
    name: /^(שם|שם מלא|שם האורח|שם המוזמן|שם המוזמנים|מוזמן|מוזמנים|אורח|name|full name|guest|guest name|display name)$/i,
    first: /^(שם פרטי|first name|given name)$/i,
    last: /^(שם משפחה|last name|family name)$/i,
    n: /^(כמות|מספר|מס'|מס׳|מספר אנשים|מספר מוזמנים|מוזמנים|אנשים|count|qty|quantity|guests|party size|people|#)$/i,
    phone: /^(טלפון|נייד|פלאפון|סלולרי|טלפון נייד|מספר טלפון|phone|mobile|cell|phone number|phone 1 - value|mobile phone|primary phone)$/i,
    side: /^(צד|side)$/i,
    group: /^(קבוצה|קטגוריה|שיוך|group|category|relationship|labels|group membership)$/i,
    status: /^(סטטוס|אישור|אישור הגעה|מגיע|מגיעים|rsvp|status)$/i,
    coming: /^(מאשרים|אישרו|כמה מגיעים|מגיעים בפועל|confirmed|attending)$/i
  };
  function mapHeader(row) {
    var map = {}, hit = 0;
    row.forEach(function (cell, i) {
      var c = String(cell || "").trim();
      Object.keys(HEAD).forEach(function (k) { if (map[k] === undefined && HEAD[k].test(c)) { map[k] = i; hit++; } });
    });
    return hit && (map.name !== undefined || map.first !== undefined) ? map : null;
  }
  function parseStatus(v) {
    v = String(v || "").trim().toLowerCase();
    if (!v) return "pending";
    if (/^(כן|מגיע|מגיעה|מגיעים|אישר|אישרה|אישרו|yes|y|✓|v|attending|confirmed)/.test(v)) return "yes";
    if (/^(לא|no|n|✗|x|declined)/.test(v)) return "no";
    if (/^(אולי|maybe|\?)/.test(v)) return "maybe";
    return "pending";
  }
  function rowsToGuests(rows) {
    rows = rows.filter(function (r) { return r && r.some(function (c) { return String(c || "").trim(); }); });
    if (!rows.length) return [];
    var map = null;
    for (var h = 0; h < Math.min(3, rows.length) && !map; h++) { map = mapHeader(rows[h]); if (map) rows = rows.slice(h + 1); }
    if (!map) {
      // no header: name, [count], [phone] — a phone-like cell anywhere is the phone
      map = { name: 0, n: 1 };
    }
    var out = [];
    rows.forEach(function (r) {
      var cell = function (k) { return map[k] !== undefined ? String(r[map[k]] == null ? "" : r[map[k]]).trim() : ""; };
      var name = cell("name") || (cell("first") + " " + cell("last")).trim();
      var phone = cell("phone");
      if (!phone) r.forEach(function (c) { if (!phone && /^\+?[\d\s\-()]{9,16}$/.test(String(c || "").trim())) phone = String(c).trim(); });
      if (!name || name === phone) return;
      var nRaw = cell("n");
      if (/^\+?[\d\s\-()]{9,16}$/.test(nRaw)) nRaw = ""; // the "count" column held a phone number
      var n = int(nRaw, 0) || 1;
      if (!nRaw) {
        var m = /^(.*?)[\s(×x*]+(\d{1,2})\)?$/.exec(name); // "משפחת כהן 4" / "משפחת כהן (4)"
        if (m && m[1].trim()) { name = m[1].trim(); n = int(m[2], 1) || 1; }
      }
      var st = parseStatus(cell("status"));
      var co = cell("coming");
      if (co && int(co, -1) >= 0) { if (st === "pending") st = int(co, 0) > 0 ? "yes" : "no"; }
      // Google Contacts "Group Membership": "* myContacts ::: חברים" -> "חברים"
      var grp = cell("group").split(":::").map(function (x) { return x.trim(); }).filter(function (x) { return x && !/^\*?\s*(myContacts|starred)$/i.test(x); }).join(", ");
      out.push(newGuest({ name: name, n: n, side: cell("side"), group: grp, phone: phone, status: st, coming: co === "" ? null : co }));
    });
    return out;
  }
  function parseCSV(text) {
    var first = text.split(/\r?\n/)[0] || "";
    var delim = (first.match(/\t/g) || []).length ? "\t" : (first.match(/;/g) || []).length > (first.match(/,/g) || []).length ? ";" : ",";
    var rows = [], row = [], cell = "", q = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) { if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch; }
      else if (ch === '"' && cell === "") q = true;
      else if (ch === delim) { row.push(cell); cell = ""; }
      else if (ch === "\n" || ch === "\r") { if (ch === "\r" && text[i + 1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += ch;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows;
  }
  function parseVCF(text) {
    var out = [], cur = null;
    text = text.replace(/\r?\n[ \t]/g, ""); // unfold
    text.split(/\r?\n/).forEach(function (line) {
      if (/^BEGIN:VCARD/i.test(line)) cur = { name: "", phone: "" };
      else if (/^END:VCARD/i.test(line)) { if (cur && (cur.name || cur.phone)) out.push(cur); cur = null; }
      else if (cur) {
        var i = line.indexOf(":"); if (i < 0) return;
        var key = line.slice(0, i).toUpperCase(), val = line.slice(i + 1);
        if (/QUOTED-PRINTABLE/.test(key)) { try { val = decodeURIComponent(val.replace(/=([0-9A-F]{2})/gi, "%$1")); } catch (e) {} }
        if (/^FN\b/.test(key) && !cur.name) cur.name = val.replace(/\\,/g, ",").trim();
        else if (/^N\b/.test(key) && !cur.name) { var p = val.split(";"); cur.name = ((p[1] || "") + " " + (p[0] || "")).trim(); }
        else if (/^(ITEM\d+\.)?TEL\b/.test(key) && !cur.phone) cur.phone = val.trim();
      }
    });
    return out.filter(function (c) { return c.name; }).map(function (c) { return newGuest(c); });
  }
  function parsePaste(text) {
    return text.split(/\r?\n/).filter(function (l) { return l.trim(); }).map(function (l) {
      if (l.indexOf("\t") >= 0) return l.split("\t");
      if (/[,;]/.test(l)) return l.split(/\s*[,;]\s*/);
      return [l];
    });
  }

  /* ---------- adding with the free limit ---------- */
  function addMany(list, quiet) {
    if (!list.length) { toast("לא נמצאו שמות"); return 0; }
    var fit = Math.min(list.length, room());
    var added = list.slice(0, fit);
    if (added.length) mutate(function () { S.guests = S.guests.concat(added); });
    if (fit < list.length) {
      limitDialog("נוספו " + fit + " מתוך " + list.length + ". בגרסה החינמית אפשר עד " + FREE_MAX + " הזמנות; בגרסה המלאה אין הגבלה, ואפשר לייבא שוב את הקובץ אחרי הפתיחה.");
    } else if (!quiet) toast("נוספו " + fit + " הזמנות");
    return fit;
  }
  function limitDialog(reason) { AppUnlock.require(SLUG, { title: UNLOCK_TITLE, reason: reason, features: UNLOCK_FEATS }); }

  /* ---------- import preview (pick who to add: useful for a whole phone contact list) ---------- */
  function preview(list, source) {
    if (!list.length) return toast("לא נמצאו שמות בקובץ");
    var existing = {}; S.guests.forEach(function (g) { existing[g.name] = 1; });
    var many = list.length > 40;
    var d = dialog('<h2>בחירת מוזמנים מ' + esc(source) + "</h2>" +
      '<p class="small muted">נמצאו ' + list.length + " אנשי קשר." + (many ? " מסמנים רק את מי שמוזמן." : "") + "</p>" +
      '<input type="search" class="pv-q" placeholder="חיפוש בשם" aria-label="חיפוש">' +
      '<div class="btn-row mt-1"><button type="button" class="btn tiny ghost" data-pv="all">סימון הכל</button><button type="button" class="btn tiny ghost" data-pv="none">ניקוי</button></div>' +
      '<ul class="pv-list">' + list.map(function (g, i) {
        var dup = existing[g.name];
        return '<li><label><input type="checkbox" data-i="' + i + '"' + (!many && !dup ? " checked" : "") + "> <span>" + esc(g.name) + (g.n > 1 ? ' <span class="muted">(' + g.n + ")</span>" : "") +
          (g.phone ? ' <span class="muted ltr small">' + esc(g.phone) + "</span>" : "") + (dup ? ' <span class="badge">כבר ברשימה</span>' : "") + "</span></label></li>";
      }).join("") + "</ul>" +
      '<div class="fields cols-2 mt-1"><div class="field"><label for="pv-side">צד לכל המסומנים</label><input id="pv-side" list="dl-sides" maxlength="40" placeholder="(לפי הקובץ)"></div>' +
      '<div class="field"><label for="pv-group">קבוצה לכל המסומנים</label><input id="pv-group" list="dl-groups" maxlength="40" placeholder="(לפי הקובץ)"></div></div>' +
      '<p class="small muted mb-0"><span class="pv-count">0</span> מסומנים' + (unlocked() ? "" : " · מקום פנוי בגרסה החינמית: " + room()) + "</p>" +
      '<div class="dlg-actions"><button type="button" class="btn accent" data-pv="add">הוספה לרשימה</button><button type="button" class="btn ghost" data-pv="cancel">ביטול</button></div>');
    function count() { $(".pv-count", d).textContent = $$(".pv-list input:checked", d).length; }
    count();
    $(".pv-q", d).addEventListener("input", function (e) {
      var q = e.target.value.trim();
      $$(".pv-list li", d).forEach(function (li) { li.hidden = q && li.textContent.indexOf(q) < 0; });
    });
    d.addEventListener("change", count);
    d.addEventListener("click", function (e) {
      var b = e.target.closest("[data-pv]"); if (!b) return;
      var a = b.getAttribute("data-pv");
      if (a === "all") { $$(".pv-list li:not([hidden]) input", d).forEach(function (c) { c.checked = true; }); count(); }
      if (a === "none") { $$(".pv-list input", d).forEach(function (c) { c.checked = false; }); count(); }
      if (a === "cancel") d.close();
      if (a === "add") {
        var side = $("#pv-side", d).value.trim(), grp = $("#pv-group", d).value.trim();
        var pick = $$(".pv-list input:checked", d).map(function (c) { var g = list[+c.getAttribute("data-i")]; if (side) g.side = side.slice(0, 40); if (grp) g.group = grp.slice(0, 40); return g; });
        d.close();
        if (pick.length) addMany(pick);
      }
    });
  }

  function importFile(file) {
    if (!file) return;
    var name = file.name.toLowerCase();
    var rd = file.arrayBuffer ? file.arrayBuffer() : new Response(file).arrayBuffer();
    rd.then(function (buf) {
      if (/\.json$/.test(name)) {
        var data = JSON.parse(new TextDecoder().decode(buf));
        if (!data || !Array.isArray(data.guests)) throw new Error("bad backup");
        if (!confirm("לשחזר מהגיבוי? הרשימה הנוכחית תוחלף.")) return;
        mutate(function () { S = data; });
        return toast("הגיבוי שוחזר");
      }
      if (/\.xlsx$/.test(name)) return AppZip.readSheet(buf).then(function (rows) { preview(rowsToGuests(rows), "קובץ האקסל"); });
      if (/\.xls$/.test(name)) throw new Error("xls");
      var text;
      try { text = new TextDecoder("utf-8", { fatal: true }).decode(buf); } catch (e) { text = new TextDecoder("windows-1255").decode(buf); }
      text = text.replace(/^﻿/, "");
      if (/\.vcf$/.test(name) || /^BEGIN:VCARD/im.test(text.slice(0, 200))) return preview(parseVCF(text), "אנשי הקשר");
      preview(rowsToGuests(parseCSV(text)), "הקובץ");
    }).catch(function (e) {
      if (window.console) console.error(e);
      toast(e && e.message === "xls" ? "קובץ XLS ישן: שמרו אותו כ-XLSX או CSV ונסו שוב" : "לא הצלחנו לקרוא את הקובץ. נסו לשמור אותו כ-CSV או להדביק את הרשימה.");
    });
  }

  /* ---------- WhatsApp reminder ---------- */
  function intlPhone(p) {
    var d = String(p || "").replace(/[^\d+]/g, "");
    if (!d) return "";
    if (d[0] === "+") return d.slice(1);
    if (/^00/.test(d)) return d.slice(2);
    if (/^0\d{8,9}$/.test(d)) return "972" + d.slice(1);
    return d;
  }
  function fmtDate(iso) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(iso || "")) return "";
    var p = iso.split("-"); return +p[2] + "." + +p[1] + "." + p[0];
  }
  function reminderText(g) {
    var ev = S.title || "החתונה שלנו";
    return (S.msg || DEFAULT_MSG).split("{שם}").join(g.name).split("{אירוע}").join(ev).split("{תאריך}").join(S.date ? " ב-" + fmtDate(S.date) : "");
  }
  function waLink(g) { var p = intlPhone(g.phone); return "https://wa.me/" + p + "?text=" + encodeURIComponent(reminderText(g)); }

  /* ---------- hand-off to the seating app ---------- */
  function toSeating() {
    var T = totals();
    var yes = S.guests.filter(function (g) { return g.status === "yes" && coming(g) > 0; });
    var open = S.guests.filter(function (g) { return g.status === "pending" || g.status === "maybe"; });
    if (!S.guests.length) return toast("קודם מוסיפים מוזמנים");
    var d = dialog("<h2>העברה לסידורי ההושבה</h2>" +
      '<p>מעבירים את הרשימה לכלי סידורי ההושבה החינמי, עם צד, קבוצה ומספר אנשים. מי שכבר נמצא שם (לפי שם) מתעדכן ולא נכפל, והשולחנות שכבר סידרתם נשמרים.</p>' +
      '<div class="choices" role="radiogroup" aria-label="את מי להעביר">' +
      '<label><input type="radio" name="who" value="yes"' + (yes.length ? " checked" : " disabled") + "> רק מי שאישר (" + T.yes + " אנשים)</label>" +
      '<label><input type="radio" name="who" value="open"' + (yes.length ? "" : " checked") + "> מי שאישר + מי שעוד לא ענה (" + (T.yes + T.pending + T.maybe) + " אנשים)</label></div>" +
      '<div class="dlg-actions"><button type="button" class="btn accent" data-go="1">מעבר לסידורי ההושבה ←</button><button type="button" class="btn ghost" data-go="0">ביטול</button></div>');
    d.addEventListener("click", function (e) {
      var b = e.target.closest("[data-go]"); if (!b) return;
      if (b.getAttribute("data-go") !== "1") return d.close();
      var who = ($("input[name=who]:checked", d) || {}).value;
      var list = who === "yes" ? yes : yes.concat(open);
      var payload = { from: "rsvp", t: Date.now(), title: S.title, date: S.date, guests: list.map(function (g) {
        return { name: g.name, n: g.status === "yes" ? coming(g) : g.n, side: g.side, group: g.group };
      }) };
      try { localStorage.setItem(HANDOFF, JSON.stringify(payload)); } catch (err) { return toast("לא הצלחנו להעביר (האחסון בדפדפן חסום)"); }
      flush();
      location.href = "../seating/?from=rsvp" + (AppUnlock.isTest ? "&test=1" : "");
    });
  }

  /* ---------- exports ---------- */
  function fileBase() { return (S.title || "רשימת מוזמנים").replace(/[\\\/:*?"<>|]+/g, " ").trim().slice(0, 60) || "רשימת מוזמנים"; }
  function exportXlsx() {
    var rows = [["שם", "מוזמנים", "צד", "קבוצה", "טלפון", "סטטוס", "מגיעים", "צמחוני", "טבעוני", "ללא גלוטן", "מנת ילדים", "הערה"]];
    sorted(S.guests).forEach(function (g) {
      rows.push([g.name, g.n, g.side, g.group, g.phone, STATUS[g.status], coming(g), int(g.veg, 0) || "", int(g.vegan, 0) || "", int(g.gf, 0) || "", int(g.kids, 0) || "", g.note]);
    });
    var T = totals();
    var sum = [[S.title || "סיכום אישורי הגעה"], [], ["", "אנשים"], ["הוזמנו", T.invited], ["אישרו הגעה", T.yes], ["לא מגיעים", T.no], ["אולי", T.maybe], ["טרם ענו", T.pending], ["צפי הגעה (הערכה)", T.expected], [],
      ["מנות (מתוך המאשרים)", ""], ["רגילה", T.regular]].concat(MEALS.map(function (m) { return [m[1], T[m[0]]]; })).concat([[], ["לפי צד", "הוזמנו", "אישרו", "טרם ענו"]]);
    var header2 = sum.length - 1;
    sides().forEach(function (s) {
      var t = totals(S.guests.filter(function (g) { return g.side === s; })); if (t.rows) sum.push([s, t.invited, t.yes, t.pending]);
    });
    var noSide = totals(S.guests.filter(function (g) { return !g.side; })); if (noSide.rows) sum.push(["ללא צד", noSide.invited, noSide.yes, noSide.pending]);
    var pend = [["שם", "מוזמנים", "טלפון", "צד", "קבוצה"]];
    sorted(S.guests.filter(function (g) { return g.status === "pending" || g.status === "maybe"; })).forEach(function (g) { pend.push([g.name, g.n, g.phone, g.side, g.group]); });
    var blob = AppZip.xlsx({ sheets: [
      { name: "מוזמנים", rows: rows, cols: [26, 9, 12, 16, 15, 11, 9, 8, 8, 9, 9, 24], header: [0], freeze: 1 },
      { name: "סיכום", rows: sum, cols: [24, 12, 12, 12], title: [0], header: [2, 10, header2] },
      { name: "טרם ענו", rows: pend, cols: [26, 9, 15, 12, 16], header: [0], freeze: 1 }
    ] });
    AppZip.download(blob, fileBase() + ".xlsx");
    toast("קובץ האקסל ירד");
  }
  function backup() {
    var blob = new Blob([JSON.stringify(S, null, 1)], { type: "application/json" });
    AppZip.download(blob, fileBase() + " - גיבוי.json");
    toast("קובץ הגיבוי ירד. שמרו אותו במקום בטוח");
  }
  function sorted(list) { return list.slice().sort(function (a, b) { return coll.compare(a.side || "", b.side || "") || coll.compare(a.group || "", b.group || "") || coll.compare(a.name, b.name); }); }

  /* ---------- dialogs ---------- */
  function dialog(inner) {
    var d = document.createElement("dialog");
    d.className = "app-dialog";
    d.innerHTML = '<form method="dialog" class="dlg-close-row"><button class="dlg-x" aria-label="סגירה" value="close">×</button></form>' + inner;
    document.body.appendChild(d);
    d.addEventListener("close", function () { d.remove(); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    if (d.showModal) d.showModal(); else d.setAttribute("open", "");
    return d;
  }
  function editGuest(id) {
    var g = guest(id); if (!g) return;
    var d = dialog("<h2>עריכת הזמנה</h2>" +
      '<form class="eg" autocomplete="off">' +
      '<div class="field"><label for="eg-name">שם</label><input id="eg-name" name="name" maxlength="80" required value="' + esc(g.name) + '"></div>' +
      '<div class="fields cols-2"><div class="field"><label for="eg-n">מוזמנים בהזמנה</label><input id="eg-n" name="n" type="number" min="1" max="60" value="' + g.n + '"></div>' +
      '<div class="field"><label for="eg-phone">טלפון</label><input id="eg-phone" name="phone" type="tel" dir="ltr" maxlength="30" value="' + esc(g.phone) + '"></div></div>' +
      '<div class="fields cols-2"><div class="field"><label for="eg-side">צד</label><input id="eg-side" name="side" list="dl-sides" maxlength="40" value="' + esc(g.side) + '"></div>' +
      '<div class="field"><label for="eg-group">קבוצה</label><input id="eg-group" name="group" list="dl-groups" maxlength="40" value="' + esc(g.group) + '"></div></div>' +
      '<div class="field"><span class="label" id="eg-st">סטטוס</span><div class="choices" role="radiogroup" aria-labelledby="eg-st">' +
      Object.keys(STATUS).map(function (k) { return '<label><input type="radio" name="status" value="' + k + '"' + (g.status === k ? " checked" : "") + "> " + STATUS[k] + "</label>"; }).join("") + "</div></div>" +
      '<div class="field eg-yes"><label for="eg-coming">כמה מגיעים בפועל</label><input id="eg-coming" name="coming" type="number" min="0" max="60" value="' + (g.coming == null ? g.n : g.coming) + '"></div>' +
      '<fieldset class="eg-yes meals"><legend>מנות מיוחדות (השאר רגילות)</legend>' +
      MEALS.map(function (m) { return '<label>' + m[1] + ' <input name="' + m[0] + '" type="number" min="0" max="60" value="' + (int(g[m[0]], 0)) + '"></label>'; }).join("") + "</fieldset>" +
      '<div class="field"><label for="eg-note">הערה</label><input id="eg-note" name="note" maxlength="200" value="' + esc(g.note) + '"></div>' +
      '<div class="dlg-actions"><button class="btn" type="submit">שמירה</button><span class="spacer"></span><button class="btn danger" type="button" data-del>מחיקה</button></div></form>');
    var f = $(".eg", d);
    function vis() { var y = f.status.value === "yes"; $$(".eg-yes", d).forEach(function (x) { x.hidden = !y; }); }
    vis(); f.addEventListener("change", vis);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.name.value.trim()) return;
      mutate(function () {
        g.name = f.name.value.trim().slice(0, 80); g.n = Math.min(int(f.n.value, 1) || 1, 60);
        g.phone = f.phone.value.trim().slice(0, 30); g.side = f.side.value.trim().slice(0, 40); g.group = f.group.value.trim().slice(0, 40);
        g.status = f.status.value; g.coming = g.status === "yes" ? Math.min(int(f.coming.value, g.n), 60) : null;
        MEALS.forEach(function (m) { g[m[0]] = g.status === "yes" ? Math.min(int(f[m[0]].value, 0), 60) : 0; });
        g.note = f.note.value.slice(0, 200);
      });
      d.close();
    });
    $("[data-del]", d).addEventListener("click", function () {
      mutate(function () { S.guests = S.guests.filter(function (x) { return x.id !== id; }); });
      d.close(); toast("נמחק (בטל מחזיר)");
    });
  }
  function pasteDialog() {
    var d = dialog("<h2>הדבקת רשימת מוזמנים</h2>" +
      '<p class="small muted">שורה לכל הזמנה. אפשר: "משפחת כהן, 4, 0501234567" או להעתיק עמודות מאקסל (שם, כמות, טלפון, צד, קבוצה).</p>' +
      '<textarea rows="9" class="pv-text" aria-label="רשימה" style="width:100%"></textarea>' +
      '<div class="dlg-actions"><button type="button" class="btn accent" data-ok>המשך</button></div>');
    $("[data-ok]", d).addEventListener("click", function () {
      var rows = parsePaste($(".pv-text", d).value);
      d.close();
      preview(rowsToGuests(rows), "הרשימה שהדבקתם");
    });
  }
  function msgDialog() {
    var d = dialog("<h2>נוסח הודעת התזכורת בוואטסאפ</h2>" +
      '<p class="small muted">{שם} מוחלף בשם ההזמנה, {אירוע} בשם האירוע, {תאריך} בתאריך. ההודעה נפתחת בוואטסאפ שלכם ואתם לוחצים שליחה; אנחנו לא שולחים כלום.</p>' +
      '<textarea rows="5" class="msg-text" aria-label="נוסח ההודעה" style="width:100%">' + esc(S.msg || DEFAULT_MSG) + "</textarea>" +
      '<p class="small">תצוגה: <span class="msg-prev muted"></span></p>' +
      '<div class="dlg-actions"><button type="button" class="btn" data-ok>שמירה</button><button type="button" class="btn ghost" data-reset>חזרה לנוסח המקורי</button></div>');
    var ta = $(".msg-text", d);
    function prev() { var o = S.msg; S.msg = ta.value; $(".msg-prev", d).textContent = reminderText({ name: "משפחת כהן" }); S.msg = o; }
    prev(); ta.addEventListener("input", prev);
    $("[data-ok]", d).addEventListener("click", function () { S.msg = ta.value.trim() === DEFAULT_MSG ? "" : ta.value.slice(0, 600); save(); d.close(); toast("הנוסח נשמר"); });
    $("[data-reset]", d).addEventListener("click", function () { ta.value = DEFAULT_MSG; prev(); });
  }

  /* ---------- render ---------- */
  var filter = { q: "", side: "", group: "", status: "" };
  function render() {
    var T = totals();
    var full = unlocked();
    var plan = $("#plan");
    plan.className = "plan-pill" + (full ? " full" : "");
    plan.innerHTML = full ? "✓ גרסה מלאה: בלי הגבלה + אקסל" : "גרסה חינמית · " + S.guests.length + "/" + FREE_MAX + ' הזמנות <button type="button" data-act="unlock">לפתיחה</button>';
    $("#stats").innerHTML = [
      ["הזמנות", T.rows], ["הוזמנו", T.invited], ["אישרו", T.yes, "yes"], ["לא מגיעים", T.no, "no"], ["טרם ענו", T.pending + T.maybe, "pending"], ["צפי הגעה", T.expected]
    ].map(function (k) { return '<div class="kpi' + (k[2] ? " st-" + k[2] : "") + '"><div class="k">' + k[0] + '</div><div class="v num">' + k[1].toLocaleString("he-IL") + "</div></div>"; }).join("");
    var meals = MEALS.filter(function (m) { return T[m[0]]; }).map(function (m) { return m[1] + " " + T[m[0]]; });
    $("#meals").textContent = T.yes ? "מנות לפי האישורים: רגילה " + T.regular + (meals.length ? " · " + meals.join(" · ") : "") : "";
    $("#expected-note").hidden = !T.rows;
    // datalists + filters
    $("#dl-sides").innerHTML = sides().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    $("#dl-groups").innerHTML = groups().map(function (s) { return '<option value="' + esc(s) + '">'; }).join("");
    fill($("#f-side"), "כל הצדדים", sides(), filter.side);
    fill($("#f-group"), "כל הקבוצות", groups(), filter.group);
    $$("[data-fstatus]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-fstatus") === filter.status ? "true" : "false"); });
    // list
    var list = sorted(S.guests).filter(function (g) {
      if (filter.q && (g.name + " " + g.phone + " " + g.group).indexOf(filter.q) < 0) return false;
      if (filter.side && g.side !== filter.side) return false;
      if (filter.group && g.group !== filter.group) return false;
      if (filter.status === "pending" && !(g.status === "pending" || g.status === "maybe")) return false;
      if (filter.status && filter.status !== "pending" && g.status !== filter.status) return false;
      return true;
    });
    $("#count-shown").textContent = list.length === S.guests.length ? "" : "מוצגות " + list.length + " מתוך " + S.guests.length;
    var box = $("#list");
    if (!S.guests.length) {
      box.innerHTML = '<div class="empty"><p><strong>הרשימה ריקה.</strong> מוסיפים הזמנה למעלה, מדביקים רשימה, מייבאים אקסל / CSV או אנשי קשר מהטלפון (VCF), או <button type="button" class="linkish" data-act="demo">טוענים דוגמה</button>.</p></div>';
    } else {
      box.innerHTML = list.map(function (g) {
        var c = coming(g);
        return '<div class="g-row st-' + g.status + '" data-gid="' + g.id + '">' +
          '<button type="button" class="g-name" data-edit="' + g.id + '"><strong>' + esc(g.name) + "</strong>" +
          '<span class="g-meta">' + g.n + (g.n > 1 ? " מוזמנים" : " מוזמן/ת") + (g.side ? " · " + esc(g.side) : "") + (g.group ? " · " + esc(g.group) : "") + (g.note ? " · " + esc(g.note) : "") + "</span></button>" +
          '<div class="g-status" role="group" aria-label="סטטוס ' + esc(g.name) + '">' +
          '<button type="button" data-st="yes" aria-pressed="' + (g.status === "yes") + '" title="מגיעים">✓<span class="sr-only"> מגיעים</span></button>' +
          '<button type="button" data-st="maybe" aria-pressed="' + (g.status === "maybe") + '" title="אולי">?<span class="sr-only"> אולי</span></button>' +
          '<button type="button" data-st="no" aria-pressed="' + (g.status === "no") + '" title="לא מגיעים">✗<span class="sr-only"> לא מגיעים</span></button></div>' +
          (g.status === "yes" ? '<label class="g-coming"><span class="sr-only">כמה מגיעים</span><input type="number" min="0" max="60" value="' + c + '" data-coming="' + g.id + '" aria-label="כמה מגיעים מתוך ' + g.n + '"><span class="muted small">/' + g.n + "</span></label>" : '<span class="g-coming"></span>') +
          (g.phone ? '<a class="btn tiny wa" href="' + esc(waLink(g)) + '" target="_blank" rel="noopener" data-wa="' + g.id + '" title="תזכורת בוואטסאפ">' + (g.sent ? "✓ " : "") + "וואטסאפ</a>" : '<button type="button" class="btn tiny ghost" data-edit="' + g.id + '" title="הוספת טלפון">+ טלפון</button>') +
          "</div>";
      }).join("") || '<p class="muted">אין תוצאות לסינון הזה.</p>';
    }
    $("#ev-title").value !== S.title && document.activeElement !== $("#ev-title") && ($("#ev-title").value = S.title || "");
    $("#ev-date").value !== S.date && ($("#ev-date").value = S.date || "");
    $$("[data-paid] .lock").forEach(function (l) { l.hidden = full; });
    var limitBar = $("#limit");
    limitBar.hidden = full || S.guests.length < FREE_MAX - 10;
    if (!limitBar.hidden) limitBar.innerHTML = (S.guests.length >= FREE_MAX ? "<strong>הגעתם ל-" + FREE_MAX + " הזמנות, המקסימום בגרסה החינמית.</strong>" : "<strong>נשארו " + room() + " הזמנות בגרסה החינמית.</strong>") +
      ' כל מה שכבר הוזן נשמר ונשאר זמין. <button type="button" class="btn small accent" data-act="unlock">בלי הגבלה + אקסל · ₪29</button>' +
      ' <a class="btn small secondary" href="../../p/wedding-bundle/" data-bundle-link>או כל 4 כלי החתונה ב-₪79 (הכי משתלם)</a>';
  }
  function fill(sel, all, items, cur) {
    sel.innerHTML = '<option value="">' + all + "</option>" + items.map(function (s) { return '<option' + (s === cur ? " selected" : "") + ' value="' + esc(s) + '">' + esc(s) + "</option>"; }).join("");
  }

  var toastTimer;
  function toast(msg) {
    var t = $("#toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { t.classList.remove("show"); }, 3600);
  }

  function demo() {
    if (S.guests.length && !confirm("לטעון דוגמה? הרשימה הנוכחית תוחלף (בטל מחזיר אותה).")) return;
    var R = [
      ["הורי הכלה", 2, "צד הכלה", "משפחה קרובה", "", "yes"], ["סבתא אסתר", 1, "צד הכלה", "משפחה קרובה", "0521111111", "yes"], ["נועה ואיתי (אחות הכלה)", 2, "צד הכלה", "משפחה קרובה", "0522222222", "yes"],
      ["משפחת פרץ", 5, "צד הכלה", "משפחה מורחבת", "0523333333", "yes", 4], ["דוד ורינה לוי", 2, "צד הכלה", "משפחה מורחבת", "0524444444", "pending"], ["משפחת חדד", 4, "צד הכלה", "משפחה מורחבת", "0525555555", "maybe"],
      ["שירה כץ", 1, "צד הכלה", "חברות מהתיכון", "0526666666", "yes"], ["מאיה ועידו", 2, "צד הכלה", "חברות מהתיכון", "0527777777", "pending"], ["טל וגיא", 2, "צד הכלה", "חברות מהתיכון", "0528888888", "no"],
      ["הילה מהעבודה", 2, "צד הכלה", "עבודה", "0529999999", "pending"], ["קרן וניר", 2, "צד הכלה", "עבודה", "0531111111", "yes"],
      ["הורי החתן", 2, "צד החתן", "משפחה קרובה", "", "yes"], ["אח החתן ומשפחתו", 4, "צד החתן", "משפחה קרובה", "0541111111", "yes"], ["משפחת מזרחי", 4, "צד החתן", "משפחה מורחבת", "0542222222", "pending"],
      ["משפחת ביטון", 5, "צד החתן", "משפחה מורחבת", "0543333333", "yes", 3], ["אלון ושני", 2, "צד החתן", "חברים מהצבא", "0544444444", "yes"], ["רועי", 1, "צד החתן", "חברים מהצבא", "0545555555", "pending"],
      ["דניאל ורותם", 2, "צד החתן", "אוניברסיטה", "0546666666", "maybe"], ["מתן", 1, "צד החתן", "אוניברסיטה", "0547777777", "no"], ["השכנים", 2, "משותף", "שכנים", "0548888888", "pending"]
    ];
    mutate(function () {
      S = { v: 1, title: S.title || "החתונה של נועה ואיתי", date: S.date || "", msg: S.msg || "", guests: R.map(function (r) { return newGuest({ name: r[0], n: r[1], side: r[2], group: r[3], phone: r[4], status: r[5], coming: r[6] }); }) };
      S.guests[2].veg = 1; S.guests[6].vegan = 1; S.guests[3].kids = 2; S.guests[12].kids = 2;
    });
    toast("נטענה רשימת דוגמה. אפשר למחוק אותה מתפריט ⋯");
  }

  /* ---------- wiring ---------- */
  function init() {
    var app = $("#app");
    var acts = {
      add: function () { $("#add-guest [name=gname]").focus(); },
      paste: pasteDialog,
      import: function () { $("#file-in").click(); },
      restore: function () { $("#file-json").click(); },
      backup: backup,
      seating: toSeating,
      msg: msgDialog,
      undo: undo,
      demo: demo,
      xlsx: function () { if (AppUnlock.require(SLUG, { title: UNLOCK_TITLE, reason: "ייצוא לאקסל עם סיכום מנות ורשימת מי שעוד לא ענה.", features: UNLOCK_FEATS })) exportXlsx(); },
      unlock: function () { limitDialog("פותחים פעם אחת ועובדים בלי הגבלה."); },
      reset: function () { if (confirm("למחוק את כל הרשימה מהדפדפן הזה? (בטל מחזיר)")) mutate(function () { S = blank(); }); }
    };
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-act]");
      if (a && (app.contains(a) || a.closest("#plan, .app-info, #limit"))) {
        var menu = a.closest("details"); if (menu) menu.open = false;
        e.preventDefault(); (acts[a.getAttribute("data-act")] || function () {})(); return;
      }
      if (!app.contains(e.target)) return;
      var ed = e.target.closest("[data-edit]"); if (ed) return editGuest(ed.getAttribute("data-edit"));
      var st = e.target.closest("[data-st]");
      if (st) {
        var g = guest(st.closest("[data-gid]").getAttribute("data-gid"));
        var v = st.getAttribute("data-st");
        mutate(function () { g.status = g.status === v ? "pending" : v; if (g.status !== "yes") { g.coming = null; } });
        return;
      }
      var wa = e.target.closest("[data-wa]");
      if (wa) { var gg = guest(wa.getAttribute("data-wa")); if (gg && !gg.sent) { gg.sent = 1; save(); setTimeout(render, 50); } return; }
      var fs = e.target.closest("[data-fstatus]");
      if (fs) { var s = fs.getAttribute("data-fstatus"); filter.status = filter.status === s ? "" : s; render(); }
      $$("details.menu[open]").forEach(function (m) { if (!m.contains(e.target)) m.open = false; });
    });
    app.addEventListener("change", function (e) {
      var c = e.target.closest("[data-coming]");
      // deferred: "change" can fire from the blur caused by a re-render removing this input (nested innerHTML)
      if (c) { var g = guest(c.getAttribute("data-coming")), v = c.value; setTimeout(function () { if (g) mutate(function () { g.coming = Math.min(int(v, g.n), 60); }); }, 0); }
    });
    $("#add-guest").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, name = f.gname.value.trim();
      if (!name) return;
      if (!room()) return limitDialog("בגרסה החינמית אפשר עד " + FREE_MAX + " הזמנות.");
      addMany([newGuest({ name: name, n: f.gn.value, side: f.gside.value, group: f.ggroup.value, phone: f.gphone.value })], true);
      f.gname.value = ""; f.gn.value = "1"; f.gphone.value = ""; f.gname.focus();
    });
    $("#ev-title").addEventListener("input", function (e) { S.title = e.target.value.slice(0, 80); save(); });
    $("#ev-date").addEventListener("change", function (e) { S.date = e.target.value; save(); render(); });
    $("#q").addEventListener("input", function (e) { filter.q = e.target.value.trim(); render(); });
    $("#f-side").addEventListener("change", function (e) { filter.side = e.target.value; render(); });
    $("#f-group").addEventListener("change", function (e) { filter.group = e.target.value; render(); });
    $("#file-in").addEventListener("change", function (e) { importFile(e.target.files[0]); e.target.value = ""; });
    $("#file-json").addEventListener("change", function (e) { importFile(e.target.files[0]); e.target.value = ""; });
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z" && !/INPUT|TEXTAREA/.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); undo(); }
    });
    AppUnlock.onChange(function () { render(); });
    render();
    if (new URLSearchParams(location.search).get("demo") === "1" && !S.guests.length) demo();
  }

  window.RsvpApp = { state: function () { return S; }, totals: totals, rowsToGuests: rowsToGuests, parseCSV: parseCSV, parseVCF: parseVCF, intlPhone: intlPhone, reminderText: reminderText, FREE_MAX: FREE_MAX };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
