/* Invitation maker UI: template gallery, form, live preview, exports (free watermarked PNG; paid clean PNG + print PDFs). */
(function () {
  "use strict";
  var I = window.Invite, SLUG = "invitation-maker", KEY = "tp-invite-v1";
  var $ = function (id) { return document.getElementById(id); };
  var params = new URLSearchParams(location.search);

  var WORDINGS = {
    wedding: [
      "אנו שמחים להזמינכם להשתתף\nבשמחת נישואינו",
      "בשמחה רבה אנו מזמינים אתכם\nלחגוג איתנו את יום חתונתנו",
      "קול ששון וקול שמחה, קול חתן וקול כלה\nנשמח לראותכם בשמחתנו",
      "אחרי שנים של אהבה, החלטנו שהגיע הזמן.\nבואו לחגוג איתנו!",
      "ההורים שמחים להזמינכם\nלחתונת ילדיהם"
    ],
    mitzvah: [
      "אנו שמחים להזמינכם לחגוג איתנו\nאת הגיעו של בננו למצוות",
      "אנו שמחים להזמינכם לחגוג איתנו\nאת הגיעה של בתנו למצוות",
      "נשמח לראותכם בעלייתו לתורה\nובמסיבת בר המצווה",
      "בואו לחגוג איתנו\nאת בת המצווה!"
    ],
    party: [
      "מסיבת יום הולדת עם הפעלה,\nעוגה והמון כיף",
      "הצטרפו אלינו לערב של אוכל טוב,\nמוזיקה וחברים",
      "אנו שמחים להזמינכם להשתתף\nבשמחתנו בהיכנס בננו בבריתו של אברהם אבינו",
      "אנו שמחים להזמינכם לשמחת\nזבד הבת של בתנו"
    ]
  };

  /* ---------- state ---------- */
  function fresh() {
    var st = { v: 1, template: "w-classic", palette: 0, accent: null, fonts: null, nameScale: 100,
      showDay: true, showHeb: true, showGreg: true, evening: false, texts: {}, edited: {} };
    Object.keys(I.CATS).forEach(function (c) { st.texts[c] = textsFor(c, null); st.edited[c] = false; });
    return st;
  }
  function textsFor(cat, tpl) {
    var t = Object.assign({}, I.DEFAULTS[cat], { date: I.DEFAULT_DATES[cat] });
    if (tpl && tpl.preset) Object.assign(t, tpl.preset);
    return t;
  }
  var S;
  try { S = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { S = null; }
  if (!S || S.v !== 1 || !S.texts) S = fresh();
  Object.keys(I.CATS).forEach(function (c) { if (!S.texts[c]) S.texts[c] = textsFor(c, null); });
  var qt = params.get("t");
  if (qt && I.TEMPLATES.some(function (t) { return t.id === qt; })) selectTemplate(qt, true);
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  function tpl() { return I.byId(S.template); }
  function cat() { return tpl().cat; }
  function renderState(extra) {
    var t = S.texts[cat()];
    return Object.assign({
      template: S.template, palette: S.palette, accent: S.accent, fonts: S.fonts, nameScale: S.nameScale,
      texts: t, date: t.date, showDay: S.showDay, showHeb: S.showHeb, showGreg: S.showGreg, evening: S.evening
    }, extra || {});
  }

  function unlocked() { return !!(window.TPUnlock && window.TPUnlock.has(SLUG)); }

  /* ---------- fonts ---------- */
  var fontReady = {};
  function loadFonts(list) {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    return Promise.all(list.map(function (f) {
      if (!fontReady[f]) {
        fontReady[f] = Promise.all([400, 700].map(function (w) {
          return document.fonts.load(w + ' 40px "' + f + '"', "אבגד שלום 0123").catch(function () {});
        }));
      }
      return fontReady[f];
    }));
  }

  /* ---------- preview ---------- */
  var pending = false;
  function draw() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(function () {
      pending = false;
      var c = $("preview");
      var css = c.getBoundingClientRect().width || 360;
      var dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      var st = renderState();
      I.render(c, st, { width: Math.min(1100, Math.round(css * dpr)), watermark: !unlocked() });
      updateHebDate();
      loadFonts(I.fontsFor(st)).then(function () {
        if (!pending) I.render(c, renderState(), { width: Math.min(1100, Math.round(css * dpr)), watermark: !unlocked() });
      });
    });
  }
  function updateHebDate() {
    var t = S.texts[cat()];
    var lines = I.composeDate(Object.assign(renderState(), { showDay: true, showHeb: true, showGreg: false }));
    $("hebdate").textContent = t.date ? (lines[0] ? "בהזמנה: " + lines[0].text : "") : "בחרו תאריך כדי לקבל תאריך עברי";
  }

  /* ---------- gallery ---------- */
  var filter = params.get("cat") && I.CATS[params.get("cat")] ? params.get("cat") : "all";
  function buildCats() {
    var html = '<button type="button" data-cat="all">הכל</button>' + Object.keys(I.CATS).map(function (c) {
      return '<button type="button" data-cat="' + c + '">' + I.CATS[c].label + "</button>";
    }).join("");
    $("cats").innerHTML = html;
    $("cats").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      filter = b.getAttribute("data-cat"); syncCats();
    });
    syncCats();
  }
  function syncCats() {
    Array.prototype.forEach.call($("cats").children, function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-cat") === filter)); });
    Array.prototype.forEach.call($("gallery").children, function (b) {
      b.hidden = filter !== "all" && b.getAttribute("data-cat") !== filter;
    });
  }
  function buildGallery() {
    var g = $("gallery");
    I.TEMPLATES.forEach(function (t) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("data-id", t.id); b.setAttribute("data-cat", t.cat);
      b.setAttribute("aria-label", "עיצוב " + t.name + " (" + I.CATS[t.cat].label + ")");
      var c = document.createElement("canvas"); c.width = 236; c.height = 334;
      var s = document.createElement("span"); s.textContent = t.name;
      b.appendChild(c); b.appendChild(s); g.appendChild(b);
    });
    g.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      selectTemplate(b.getAttribute("data-id"));
    });
    drawThumbs();
    var all = []; I.TEMPLATES.forEach(function (t) { all.push(t.fonts.display, t.fonts.body); });
    loadFonts(all.filter(function (f, i) { return all.indexOf(f) === i; })).then(drawThumbs);
  }
  function drawThumbs() {
    Array.prototype.forEach.call($("gallery").children, function (b) {
      var t = I.byId(b.getAttribute("data-id"));
      var texts = textsFor(t.cat, t);
      I.render(b.querySelector("canvas"), { template: t.id, palette: 0, texts: texts, date: texts.date, showDay: true, showHeb: true, showGreg: true }, { width: 236 });
      b.setAttribute("aria-pressed", String(t.id === S.template));
    });
  }
  function selectTemplate(id, quiet) {
    var t = I.byId(id);
    S.template = t.id; S.palette = 0; S.accent = null; S.fonts = null;
    if (!S.edited[t.cat]) { var d = S.texts[t.cat] && S.texts[t.cat].date; S.texts[t.cat] = textsFor(t.cat, t); if (d) S.texts[t.cat].date = d; }
    if (quiet) return;
    save(); fillForm(); drawThumbs(); draw();
  }

  /* ---------- form ---------- */
  function fillForm() {
    var t = S.texts[cat()];
    Array.prototype.forEach.call(document.querySelectorAll("[data-k]"), function (el) { el.value = t[el.getAttribute("data-k")] || ""; });
    $("c-day").checked = S.showDay; $("c-heb").checked = S.showHeb; $("c-greg").checked = S.showGreg; $("c-eve").checked = S.evening;
    $("f-namesize").value = S.nameScale || 100;
    var w = WORDINGS[cat()] || [];
    $("f-wording").innerHTML = '<option value="">בחרו נוסח…</option>' + w.map(function (x, i) {
      return '<option value="' + i + '">' + x.replace(/\n/g, " ").replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</option>";
    }).join("");
    var f = S.fonts || tpl().fonts;
    $("f-fd").value = f.display; $("f-fb").value = f.body;
    buildSwatches();
  }
  function buildSwatches() {
    var box = $("swatches"), t = tpl();
    box.innerHTML = "";
    t.palettes.forEach(function (p, i) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("aria-label", "ערכת צבעים " + (i + 1));
      b.style.background = "linear-gradient(135deg," + p.bg + " 50%," + p.accent + " 50%)";
      b.setAttribute("aria-pressed", String(!S.accent && S.palette === i));
      b.addEventListener("click", function () { S.palette = i; S.accent = null; save(); buildSwatches(); draw(); });
      box.appendChild(b);
    });
    var lab = document.createElement("label"); lab.className = "small inv-row";
    var inp = document.createElement("input"); inp.type = "color"; inp.id = "f-accent";
    inp.value = S.accent || t.palettes[S.palette].accent;
    inp.setAttribute("aria-label", "צבע הדגשה מותאם");
    inp.addEventListener("input", function () { S.accent = inp.value; save(); draw(); syncSw(); });
    lab.appendChild(inp); lab.appendChild(document.createTextNode("צבע הדגשה"));
    box.appendChild(lab);
    function syncSw() { Array.prototype.forEach.call(box.querySelectorAll("button"), function (b) { b.setAttribute("aria-pressed", "false"); }); }
  }
  function bindForm() {
    var fd = $("f-fd"), fb = $("f-fb");
    I.FONTS.forEach(function (f) {
      fd.add(new Option(f.label, f.id)); fb.add(new Option(f.label, f.id));
    });
    $("form").addEventListener("input", function (e) {
      var k = e.target.getAttribute("data-k");
      if (k) { S.texts[cat()][k] = e.target.value; S.edited[cat()] = true; save(); draw(); }
    });
    $("f-namesize").addEventListener("input", function () { S.nameScale = +this.value; save(); draw(); });
    [["c-day", "showDay"], ["c-heb", "showHeb"], ["c-greg", "showGreg"], ["c-eve", "evening"]].forEach(function (p) {
      $(p[0]).addEventListener("change", function () { S[p[1]] = this.checked; save(); draw(); });
    });
    $("f-wording").addEventListener("change", function () {
      var w = WORDINGS[cat()][+this.value];
      if (this.value !== "" && w) { S.texts[cat()].invite = w; S.edited[cat()] = true; $("f-invite").value = w; save(); draw(); }
      this.value = "";
    });
    function fontChange() { S.fonts = { display: fd.value, body: fb.value }; save(); draw(); }
    fd.addEventListener("change", fontChange); fb.addEventListener("change", fontChange);
    $("reset-style").addEventListener("click", function () { S.palette = 0; S.accent = null; S.fonts = null; S.nameScale = 100; save(); fillForm(); draw(); });
  }

  /* ---------- exports ---------- */
  function status(t) { $("status").textContent = t || ""; }
  function fileBase() { // ASCII file names: some browsers drop non-Latin download names
    var t = S.texts[cat()];
    return "invitation-" + S.template + (t.date ? "-" + t.date : "");
  }
  function download(blob, name) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 4000);
  }
  function toBlob(canvas, type, q) {
    return new Promise(function (res, rej) { canvas.toBlob(function (b) { b ? res(b) : rej(new Error("toBlob")); }, type, q); });
  }
  function renderTo(opts) {
    var st = renderState();
    return loadFonts(I.fontsFor(st)).then(function () { return I.render(document.createElement("canvas"), st, opts); });
  }
  function track(kind) {
    try { if (window.SITE && window.SITE.track) window.SITE.track("invite-" + kind); } catch (e) {}
  }

  $("dl-free").addEventListener("click", function () {
    status("מכינים תצוגה מקדימה…");
    renderTo({ width: 600, watermark: true }).then(function (c) { return toBlob(c, "image/png"); })
      .then(function (b) { download(b, fileBase() + "-preview.png"); status("התצוגה המקדימה ירדה."); track("free"); })
      .catch(function () { status("לא הצלחנו ליצור את הקובץ. נסו שוב."); });
  });

  function cleanPng() { return renderTo({ width: 2000 }).then(function (c) { return toBlob(c, "image/png"); }); }
  $("dl-png").addEventListener("click", function () {
    if (!unlocked()) return;
    status("מכינים PNG באיכות גבוהה…");
    cleanPng().then(function (b) { download(b, fileBase() + ".png"); status("ה-PNG ירד. אפשר לשלוח אותו בוואטסאפ כ'מסמך' כדי לשמור על האיכות."); track("png"); })
      .catch(function () { status("לא הצלחנו ליצור את הקובץ. נסו שוב."); });
  });
  $("share").addEventListener("click", function () {
    if (!unlocked()) return;
    status("מכינים לשיתוף…");
    cleanPng().then(function (b) {
      var f = new File([b], "invitation.png", { type: "image/png" });
      return navigator.share({ files: [f], title: "הזמנה" });
    }).then(function () { status(""); }, function (e) { status(e && e.name === "AbortError" ? "" : "השיתוף לא זמין בדפדפן הזה. הורידו PNG ושלחו אותו."); });
  });

  /* PDF layouts (mm). Rendered at 300 dpi. */
  var LAYOUTS = {
    a5: { page: [154, 216], trim: [148, 210], bleed: 3, slots: [[0, 0]] },
    a6: { page: [111, 154], trim: [105, 148], bleed: 3, slots: [[0, 0]] },
    a4x2: { page: [297, 210], trim: [134, 189.5], bleed: 0, slots: [[10.5, 10.25], [152.5, 10.25]], marks: true },
    a4x4: { page: [210, 297], trim: [95, 134.35], bleed: 0, slots: [[7.5, 11], [107.5, 11], [7.5, 151.65], [107.5, 151.65]], marks: true }
  };
  function jpegBytes(canvas) {
    return toBlob(canvas, "image/jpeg", 0.93).then(function (b) { return b.arrayBuffer(); }).then(function (ab) { return new Uint8Array(ab); });
  }
  $("dl-pdf").addEventListener("click", function () {
    if (!unlocked()) return;
    var kind = $("pdf-kind").value, L = LAYOUTS[kind];
    status("מכינים PDF להדפסה… (כמה שניות)");
    var wmm = L.trim[0] + 2 * L.bleed;
    var px = Math.round(wmm / 25.4 * 300);
    renderTo({ width: px, bleedMm: L.bleed, trimMm: L.trim[0] }).then(function (c) {
      return jpegBytes(c).then(function (jpeg) {
        var iw = wmm, ih = L.trim[1] + 2 * L.bleed;
        var marks = [];
        var images = L.slots.map(function (s) {
          if (L.marks) marks = marks.concat(window.TinyPDF.cropMarks(s[0], s[1], iw, ih, 4, 1.5));
          return { jpeg: jpeg, pw: c.width, ph: c.height, x: s[0], y: s[1], iw: iw, ih: ih };
        });
        // home sheets: drop marks that would fall on a neighbouring card
        if (L.marks && L.slots.length > 1) marks = marks.filter(function (m) {
          return !L.slots.some(function (s) {
            var x = (m[0] + m[2]) / 2, y = (m[1] + m[3]) / 2;
            return x > s[0] + 0.01 && x < s[0] + iw - 0.01 && y > s[1] + 0.01 && y < s[1] + ih - 0.01;
          });
        });
        return window.TinyPDF.build([{ w: L.page[0], h: L.page[1], images: images, marks: marks }], { title: "Invitation" });
      });
    }).then(function (blob) {
      download(blob, fileBase() + "-" + kind + ".pdf");
      status(L.bleed ? "ה-PDF ירד. לבית הדפוס: הקובץ כולל 3 מ״מ בליד מכל צד, לחיתוך בגודל " + L.trim[0] + "×" + L.trim[1] + " מ״מ." :
        "ה-PDF ירד. הדפיסו ב„גודל אמיתי / 100%“ (לא „התאמה לדף“) וגזרו לפי הסימנים.");
      track("pdf-" + kind);
    }).catch(function (e) { if (window.console) console.error(e); status("לא הצלחנו ליצור PDF. נסו שוב או בחרו גודל אחר."); });
  });

  function syncLock() {
    var u = unlocked();
    $("locked").hidden = u; $("paid").hidden = !u;
    $("preview-note").textContent = u ? "ההורדות הנקיות פתוחות בדפדפן הזה. סימן המים לא יופיע בקבצים." : "תצוגה מקדימה עם סימן מים. ההורדה הנקייה נפתחת אחרי רכישה.";
    $("share").hidden = !(u && navigator.canShare && navigator.canShare({ files: [new File(["x"], "x.png", { type: "image/png" })] }));
    draw();
  }
  window.addEventListener("tp:unlocked", function (e) {
    if (e.detail && e.detail.slug === SLUG) { syncLock(); status("תודה! ההורדות הנקיות פתוחות. בחרו קובץ להורדה."); $("paid").scrollIntoView({ behavior: "smooth", block: "center" }); }
  });
  window.addEventListener("storage", function (e) { if (e.key === "tp-unlock:" + SLUG) syncLock(); });
  var rz; window.addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(draw, 150); });

  buildCats(); buildGallery(); bindForm(); fillForm(); syncCats(); syncLock();
  window.InviteApp = { state: function () { return S; }, draw: draw, unlocked: unlocked };
})();
