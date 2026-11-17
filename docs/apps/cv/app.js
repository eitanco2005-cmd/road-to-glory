/* תכנון פלוס — Hebrew/English CV builder (client-side only; data in localStorage "tp-cv-v1").
 * Free: full editing + live preview + watermarked print/PDF. Paid (product "cv-builder"): clean PDF + DOCX.
 */
(function () {
  "use strict";
  var SLUG = "cv-builder";
  var KEY = "tp-cv-v1";
  var TEMPLATES = [
    { id: "classic", name: "קלאסי" }, { id: "modern", name: "מודרני" },
    { id: "minimal", name: "מינימלי" }, { id: "executive", name: "בכיר" }
  ];
  var ACCENTS = ["#0e6b63", "#1f4e8c", "#7a2e5a", "#9a5b00", "#333a40"];
  var L = {
    he: { summary: "תמצית", experience: "ניסיון תעסוקתי", military: "שירות צבאי / לאומי", education: "השכלה", skills: "כישורים", languages: "שפות", present: "היום", cvOf: "קורות חיים" },
    en: { summary: "Summary", experience: "Experience", military: "Military Service", education: "Education", skills: "Skills", languages: "Languages", present: "Present", cvOf: "CV" }
  };
  var UNLOCK_FEATS = ["PDF נקי בלי סימן מים: טקסט אמיתי שמערכות סינון (ATS) קוראות", "קובץ Word (DOCX) לעריכה ולשליחה למשרות שמבקשות Word", "כל 4 התבניות, בעברית ובאנגלית", "תשלום חד-פעמי: כל הגרסאות שתייצאו בדפדפן הזה"];

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function emptyContent() {
    return { name: "", title: "", phone: "", email: "", city: "", links: "", summary: "", experience: [], military: [], education: [], skills: "", languages: "", extra: [] };
  }
  function blank() { return { v: 1, lang: "he", template: "classic", accent: ACCENTS[0], he: emptyContent(), en: emptyContent() }; }
  var S = (function () {
    try {
      var s = JSON.parse(localStorage.getItem(KEY) || "null");
      if (s && s.he && s.en) return s;
    } catch (e) {}
    return blank();
  })();
  function C() { return S[S.lang]; }
  var t;
  function save() { clearTimeout(t); t = setTimeout(function () { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }, 200); }

  var LISTS = {
    experience: { fields: [["role", "תפקיד", "Role"], ["org", "חברה / ארגון", "Company"], ["place", "עיר", "City"], ["start", "מ-", "From"], ["end", "עד (ריק = היום)", "To (empty = present)"]], text: ["bullets", "הישגים ותחומי אחריות (שורה לכל נקודה)", "Achievements (one per line)"], addLabel: "+ הוספת תפקיד" },
    military: { fields: [["role", "תפקיד / דרגה", "Role / rank"], ["org", "יחידה", "Unit"], ["start", "מ-", "From"], ["end", "עד", "To"]], text: ["bullets", "מה עשיתם (שורה לכל נקודה)", "What you did (one per line)"], addLabel: "+ הוספת שירות" },
    education: { fields: [["degree", "תואר / תעודה", "Degree"], ["school", "מוסד", "Institution"], ["start", "מ-", "From"], ["end", "עד", "To"]], text: ["notes", "פירוט (ממוצע, פרויקט, הצטיינות)", "Details (GPA, project, honours)"], addLabel: "+ הוספת לימודים" },
    extra: { fields: [["title", "כותרת המדור (התנדבות, קורסים, פרסומים…)", "Section title (Volunteering, Courses…)"]], text: ["text", "תוכן (שורה לכל פריט)", "Content (one item per line)"], addLabel: "+ מדור נוסף" }
  };

  /* ---------- form ---------- */
  function lbl(he, en) { return S.lang === "en" ? en + " · " + he : he; }
  function renderForm() {
    var c = C(), dir = S.lang === "en" ? "ltr" : "rtl";
    $$("[data-field]").forEach(function (el) {
      var k = el.getAttribute("data-field");
      if (document.activeElement !== el) el.value = c[k] || "";
      el.dir = dir;
    });
    Object.keys(LISTS).forEach(function (k) {
      var spec = LISTS[k], box = $("#list-" + k);
      box.innerHTML = c[k].map(function (it, i) {
        return '<div class="item" data-list="' + k + '" data-i="' + i + '"><div class="item-bar"><strong>' + esc(itemTitle(k, it) || "פריט " + (i + 1)) + '</strong><span>' +
          '<button type="button" class="ib" data-move="-1" aria-label="למעלה" title="למעלה">↑</button><button type="button" class="ib" data-move="1" aria-label="למטה" title="למטה">↓</button><button type="button" class="ib del" data-del aria-label="מחיקה" title="מחיקה">×</button></span></div>' +
          '<div class="fields cols-2">' + spec.fields.map(function (f) {
            return '<div class="field"><label>' + esc(lbl(f[1], f[2])) + '</label><input type="text" dir="' + dir + '" data-k="' + f[0] + '" value="' + esc(it[f[0]] || "") + '" maxlength="120"></div>';
          }).join("") + "</div>" +
          '<div class="field"><label>' + esc(lbl(spec.text[1], spec.text[2])) + '</label><textarea rows="3" dir="' + dir + '" data-k="' + spec.text[0] + '" maxlength="2000">' + esc(it[spec.text[0]] || "") + "</textarea></div></div>";
      }).join("") + '<button type="button" class="btn ghost small" data-add="' + k + '">' + spec.addLabel + "</button>";
    });
    $$(".lang-switch button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-lang") === S.lang ? "true" : "false"); });
    $$(".tpl-pick button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-tpl") === S.template ? "true" : "false"); });
    $$(".accent-pick button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-accent") === S.accent ? "true" : "false"); });
    $("#copy-he").hidden = !(S.lang === "en" && isEmpty(S.en) && !isEmpty(S.he));
  }
  function itemTitle(k, it) {
    if (k === "education") return [it.degree, it.school].filter(Boolean).join(" · ");
    if (k === "extra") return it.title;
    return [it.role, it.org].filter(Boolean).join(" · ");
  }
  function isEmpty(c) { return !c.name && !c.summary && !c.experience.length && !c.education.length; }
  function renderPlan() {
    var un = AppUnlock.isUnlocked(SLUG);
    $("#plan").className = "plan-pill" + (un ? " full" : "");
    $("#plan").innerHTML = un ? "✓ גרסה מלאה פעילה" : 'גרסה חינמית · <button type="button" data-act="unlock">מה בגרסה המלאה?</button>';
    $$("[data-paid] .lock").forEach(function (l) { l.hidden = un; });
  }

  /* ---------- preview ---------- */
  function lines(s) { return String(s || "").split(/\r?\n/).map(function (x) { return x.replace(/^\s*[-•*·]\s*/, "").trim(); }).filter(Boolean); }
  function dates(it) {
    var l = L[S.lang];
    if (!it.start && !it.end) return "";
    return (it.start || "") + (it.start ? " – " : "") + (it.end || (it.start ? l.present : ""));
  }
  function cvHtml() {
    var c = C(), l = L[S.lang];
    var contact = [c.phone, c.email, c.city].concat(lines(c.links)).filter(Boolean);
    var h = '<header class="cv-head"><h1 class="cv-name">' + esc(c.name || (S.lang === "en" ? "Your Name" : "השם שלכם")) + "</h1>" +
      (c.title ? '<p class="cv-title">' + esc(c.title) + "</p>" : "") +
      (contact.length ? '<p class="cv-contact">' + contact.map(function (x) { return '<span dir="auto">' + esc(x) + "</span>"; }).join('<span class="sep" aria-hidden="true"> | </span>') + "</p>" : "") +
      "</header>";
    if (c.summary.trim()) h += sec(l.summary, '<p class="cv-summary">' + esc(c.summary).replace(/\n/g, "<br>") + "</p>");
    if (c.experience.length) h += sec(l.experience, c.experience.map(function (it) { return entry(it.role, [it.org, it.place].filter(Boolean).join(", "), dates(it), lines(it.bullets)); }).join(""));
    if (c.military.length) h += sec(l.military, c.military.map(function (it) { return entry(it.role, it.org, dates(it), lines(it.bullets)); }).join(""));
    if (c.education.length) h += sec(l.education, c.education.map(function (it) { return entry(it.degree, it.school, dates(it), lines(it.notes)); }).join(""));
    var sk = String(c.skills || "").split(/[\n,•·]+/).map(function (x) { return x.trim(); }).filter(Boolean);
    if (sk.length) h += sec(l.skills, '<p class="cv-skills">' + sk.map(esc).join(" · ") + "</p>");
    if (lines(c.languages).length) h += sec(l.languages, '<p class="cv-langs">' + lines(c.languages).map(esc).join(" · ") + "</p>");
    c.extra.forEach(function (x) { if (x.title || x.text) h += sec(x.title || "", '<ul class="cv-bullets">' + lines(x.text).map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("") + "</ul>"); });
    return h;
  }
  function sec(title, body) { return '<section class="cv-sec"><h2>' + esc(title) + "</h2>" + body + "</section>"; }
  function entry(a, b, d, bullets) {
    return '<div class="cv-entry"><div class="cv-entry-head"><div><strong>' + esc(a || "") + "</strong>" + (b ? '<span class="cv-org">' + (a ? ", " : "") + esc(b) + "</span>" : "") + "</div>" +
      (d ? '<span class="cv-dates" dir="auto">' + esc(d) + "</span>" : "") + "</div>" +
      (bullets.length ? '<ul class="cv-bullets">' + bullets.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>" : "") + "</div>";
  }
  function applyPage(el) {
    el.className = "cv tpl-" + S.template;
    el.dir = S.lang === "en" ? "ltr" : "rtl";
    el.lang = S.lang;
    el.style.setProperty("--cv-accent", S.accent);
    el.innerHTML = cvHtml();
  }
  function renderPreview() {
    var page = $("#cv-page");
    applyPage(page);
    fit();
  }
  function fit() {
    var wrap = $("#cv-scale"), page = $("#cv-page");
    if (!wrap.offsetWidth) return;
    var s = Math.min(1, wrap.offsetWidth / page.offsetWidth);
    page.style.transform = "scale(" + s + ")";
    wrap.style.height = page.offsetHeight * s + "px";
  }
  function renderAll() { renderForm(); renderPreview(); renderPlan(); }

  /* ---------- export ---------- */
  function printCv(clean) {
    var area = $("#print-area");
    if (!area) { area = document.createElement("div"); area.id = "print-area"; document.body.appendChild(area); }
    var page = document.createElement("div");
    applyPage(page);
    area.innerHTML = clean ? "" : '<div class="wm" aria-hidden="true">' + new Array(16).join("<span>תכנון פלוס · גרסה חינמית</span>") + '</div><div class="wm-foot">נוצר בגרסה החינמית של תכנון פלוס · tichnun.netlify.app/apps/cv</div>';
    area.appendChild(page);
    var oldTitle = document.title;
    document.title = fileBase(); // Chrome uses the title as the default PDF file name
    document.body.classList.add("printing");
    var done = function () { document.body.classList.remove("printing"); document.title = oldTitle; window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    setTimeout(function () { window.print(); setTimeout(done, 500); }, 60);
  }
  function fileBase() {
    var n = (C().name || "cv").trim();
    return ((S.lang === "en" ? "CV - " : "קורות חיים - ") + n).replace(/[\\\/:*?"<>|]+/g, "").slice(0, 70);
  }

  /* DOCX: real Word paragraphs (bidi for Hebrew), single column, standard headings = ATS friendly */
  function docx() {
    var c = C(), l = L[S.lang], rtl = S.lang === "he";
    var x = AppZip.xmlEscape, acc = S.accent.replace("#", "").toUpperCase();
    function run(text, o) {
      o = o || {};
      var rp = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>' + (o.b ? "<w:b/><w:bCs/>" : "") + (o.color ? '<w:color w:val="' + o.color + '"/>' : "") +
        '<w:sz w:val="' + (o.sz || 21) + '"/><w:szCs w:val="' + (o.sz || 21) + '"/>' + (rtl ? "<w:rtl/>" : "");
      return "<w:r><w:rPr>" + rp + '</w:rPr><w:t xml:space="preserve">' + x(text) + "</w:t></w:r>";
    }
    function para(runs, o) {
      o = o || {};
      var pp = (o.style ? '<w:pStyle w:val="' + o.style + '"/>' : "") + (o.border ? '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="' + acc + '"/></w:pBdr>' : "") +
        '<w:spacing w:before="' + (o.before || 0) + '" w:after="' + (o.after == null ? 60 : o.after) + '"/>' +
        (rtl ? "<w:bidi/>" : "") + (o.center ? '<w:jc w:val="center"/>' : "");
      return "<w:p><w:pPr>" + pp + "</w:pPr>" + runs + "</w:p>";
    }
    var body = "";
    var center = S.template === "classic";
    body += para(run(c.name || "", { b: true, sz: 40, color: acc }), { center: center, after: 40 });
    if (c.title) body += para(run(c.title, { sz: 24 }), { center: center, after: 40 });
    var contact = [c.phone, c.email, c.city].concat(lines(c.links)).filter(Boolean);
    if (contact.length) body += para(run(contact.join("  |  "), { sz: 19, color: "555555" }), { center: center, after: 120 });
    function heading(t) { body += para(run(t, { b: true, sz: 25, color: acc }), { style: "Heading2", border: true, before: 200, after: 80 }); }
    function ent(a, b, d, bl) {
      var head = run(a || "", { b: true }) + (b ? run((a ? ", " : "") + b) : "") + (d ? run("   |   " + d, { color: "555555", sz: 19 }) : "");
      body += para(head, { before: 80, after: 30 });
      bl.forEach(function (t) { body += para(run("• " + t), { after: 20 }); });
    }
    if (c.summary.trim()) { heading(l.summary); lines(c.summary).forEach(function (s) { body += para(run(s)); }); }
    if (c.experience.length) { heading(l.experience); c.experience.forEach(function (it) { ent(it.role, [it.org, it.place].filter(Boolean).join(", "), dates(it), lines(it.bullets)); }); }
    if (c.military.length) { heading(l.military); c.military.forEach(function (it) { ent(it.role, it.org, dates(it), lines(it.bullets)); }); }
    if (c.education.length) { heading(l.education); c.education.forEach(function (it) { ent(it.degree, it.school, dates(it), lines(it.notes)); }); }
    var sk = String(c.skills || "").split(/[\n,•·]+/).map(function (s) { return s.trim(); }).filter(Boolean);
    if (sk.length) { heading(l.skills); body += para(run(sk.join(" · "))); }
    if (lines(c.languages).length) { heading(l.languages); body += para(run(lines(c.languages).join(" · "))); }
    c.extra.forEach(function (e) { if (!e.title && !e.text) return; heading(e.title || ""); lines(e.text).forEach(function (s) { body += para(run("• " + s), { after: 20 }); }); });
    var sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="1134" w:bottom="1000" w:left="1134" w:header="567" w:footer="567" w:gutter="0"/>' + (rtl ? "<w:bidi/>" : "") + "</w:sectPr>";
    var doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + body + sect + "</w:body></w:document>";
    var styles = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Arial"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="' + (rtl ? "he-IL" : "en-US") + '" w:bidi="he-IL"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="60" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>' +
      '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>' +
      '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:bCs/></w:rPr></w:style></w:styles>';
    var files = [
      { name: "[Content_Types].xml", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>' },
      { name: "_rels/.rels", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>' },
      { name: "word/_rels/document.xml.rels", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>' },
      { name: "word/document.xml", data: doc },
      { name: "word/styles.xml", data: styles },
      { name: "docProps/core.xml", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>' + x(fileBase()) + "</dc:title><dc:creator>" + x(c.name || "") + '</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">' + new Date().toISOString().slice(0, 19) + "Z</dcterms:created></cp:coreProperties>" }
    ];
    var blob = new Blob([AppZip.write(files)], { type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" });
    AppZip.download(blob, fileBase() + ".docx");
    toast("קובץ ה-Word ירד");
  }

  /* ---------- sample ---------- */
  function sample() {
    if ((!isEmpty(S.he) || !isEmpty(S.en)) && !confirm("לטעון דוגמה? מה שכתבתם יוחלף.")) return;
    S.he = {
      name: "מיכל לוי", title: "מנהלת שיווק דיגיטלי", phone: "050-0000000", email: "michal.levi@example.com", city: "תל אביב",
      links: "linkedin.com/in/michal-levi-example",
      summary: "מנהלת שיווק דיגיטלי עם 6 שנות ניסיון בחברות B2C. מובילה קמפיינים ממומנים בתקציבים של מאות אלפי שקלים, בונה תהליכי אוטומציה ומודדת כל שקל. מחפשת תפקיד ניהולי בחברה צומחת.",
      experience: [
        { role: "מנהלת שיווק דיגיטלי", org: "חברת דוגמה בע\"מ", place: "תל אביב", start: "2022", end: "", bullets: "ניהול צוות של 4 אנשי שיווק ותקציב מדיה שנתי של כ-1.2 מיליון ₪\nהורדת עלות לליד ב-35% תוך שנה באמצעות בדיקות A/B ודפי נחיתה חדשים\nהקמת מערך דיוור אוטומטי שמייצר כ-18% מהמכירות" },
        { role: "מנהלת קמפיינים", org: "סוכנות פרסום לדוגמה", place: "רמת גן", start: "2019", end: "2022", bullets: "ניהול קמפיינים בגוגל ובמטא ל-12 לקוחות במקביל\nבניית דוחות ביצועים חודשיים ללקוחות ולהנהלה" }
      ],
      military: [{ role: "מש\"קית הדרכה", org: "חיל המודיעין", start: "2015", end: "2017", bullets: "הדרכת קורסים של 30 חיילים בכל מחזור" }],
      education: [{ degree: "B.A. בתקשורת ומנהל עסקים", school: "אוניברסיטה לדוגמה", start: "2016", end: "2019", notes: "בהצטיינות" }],
      skills: "Google Ads, Meta Ads, Google Analytics 4, HubSpot, Excel מתקדם, ניהול צוות, כתיבה שיווקית",
      languages: "עברית – שפת אם\nאנגלית – ברמה גבוהה מאוד",
      extra: [{ title: "התנדבות", text: "חונכת בתוכנית ליווי לסטודנטיות מהפריפריה (2021–היום)" }]
    };
    S.en = {
      name: "Michal Levi", title: "Digital Marketing Manager", phone: "+972-50-000-0000", email: "michal.levi@example.com", city: "Tel Aviv, Israel",
      links: "linkedin.com/in/michal-levi-example",
      summary: "Digital marketing manager with 6 years of B2C experience. Runs paid campaigns with six-figure budgets, builds automation flows and measures every shekel. Looking for a leadership role in a growing company.",
      experience: [
        { role: "Digital Marketing Manager", org: "Example Ltd.", place: "Tel Aviv", start: "2022", end: "", bullets: "Lead a team of 4 and an annual media budget of about ILS 1.2M\nCut cost per lead by 35% in one year with A/B tests and new landing pages\nBuilt automated email flows that drive about 18% of sales" },
        { role: "Campaign Manager", org: "Example Agency", place: "Ramat Gan", start: "2019", end: "2022", bullets: "Managed Google and Meta campaigns for 12 clients\nBuilt monthly performance reports for clients and management" }
      ],
      military: [{ role: "Training NCO", org: "IDF Intelligence Corps", start: "2015", end: "2017", bullets: "Trained cohorts of 30 soldiers" }],
      education: [{ degree: "B.A. Communication and Business", school: "Example University", start: "2016", end: "2019", notes: "Cum laude" }],
      skills: "Google Ads, Meta Ads, Google Analytics 4, HubSpot, Advanced Excel, Team leadership, Copywriting",
      languages: "Hebrew – native\nEnglish – full professional proficiency",
      extra: [{ title: "Volunteering", text: "Mentor in a programme for students from Israel's periphery (2021–present)" }]
    };
    save(); renderAll();
    toast("נטענה דוגמה (פרטים בדויים). החליפו לאנגלית כדי לראות גם את הגרסה באנגלית.");
  }

  /* ---------- misc ---------- */
  var toastTimer;
  function toast(msg) { var el = $("#toast"); el.textContent = msg; el.classList.add("show"); clearTimeout(toastTimer); toastTimer = setTimeout(function () { el.classList.remove("show"); }, 3600); }
  function paid(fn, reason) {
    return function () { if (AppUnlock.require(SLUG, { title: "הגרסה המלאה של בונה קורות החיים · ₪19", reason: reason, features: UNLOCK_FEATS })) fn(); };
  }

  function init() {
    if (!$("#toast")) { var tt = document.createElement("div"); tt.id = "toast"; tt.className = "toast"; tt.setAttribute("role", "status"); document.body.appendChild(tt); }
    $(".tpl-pick").innerHTML = TEMPLATES.map(function (t) { return '<button type="button" data-tpl="' + t.id + '" aria-pressed="false"><span class="tpl-thumb tpl-' + t.id + '" aria-hidden="true"><i></i><i></i><i></i></span>' + t.name + "</button>"; }).join("");
    $(".accent-pick").innerHTML = ACCENTS.map(function (a) { return '<button type="button" data-accent="' + a + '" style="--c:' + a + '" aria-label="צבע ' + a + '" aria-pressed="false"></button>'; }).join("");
    var form = $("#cv-form");
    form.addEventListener("input", function (e) {
      var el = e.target, c = C();
      if (el.hasAttribute("data-field")) c[el.getAttribute("data-field")] = el.value;
      else if (el.hasAttribute("data-k")) {
        var item = el.closest("[data-list]");
        var it = c[item.getAttribute("data-list")][+item.getAttribute("data-i")];
        it[el.getAttribute("data-k")] = el.value;
        var bar = item.querySelector(".item-bar strong");
        bar.textContent = itemTitle(item.getAttribute("data-list"), it) || "פריט " + (+item.getAttribute("data-i") + 1);
      }
      save(); renderPreview();
    });
    form.addEventListener("click", function (e) {
      var add = e.target.closest("[data-add]");
      if (add) {
        var k = add.getAttribute("data-add"), it = {};
        LISTS[k].fields.forEach(function (f) { it[f[0]] = ""; }); it[LISTS[k].text[0]] = "";
        C()[k].push(it); save(); renderForm(); renderPreview();
        var items = $$("#list-" + k + " .item"); var last = items[items.length - 1]; if (last) last.querySelector("input").focus();
        return;
      }
      var item = e.target.closest("[data-list]"); if (!item) return;
      var list = C()[item.getAttribute("data-list")], i = +item.getAttribute("data-i");
      if (e.target.closest("[data-del]")) { if (!confirm("למחוק את הפריט?")) return; list.splice(i, 1); }
      else if (e.target.closest("[data-move]")) {
        var j = i + +e.target.closest("[data-move]").getAttribute("data-move");
        if (j < 0 || j >= list.length) return;
        var tmp = list[i]; list[i] = list[j]; list[j] = tmp;
      } else return;
      save(); renderForm(); renderPreview();
    });
    document.addEventListener("click", function (e) {
      var b;
      if ((b = e.target.closest(".lang-switch [data-lang]"))) { S.lang = b.getAttribute("data-lang"); save(); renderAll(); }
      else if ((b = e.target.closest(".tpl-pick [data-tpl]"))) { S.template = b.getAttribute("data-tpl"); save(); renderAll(); }
      else if ((b = e.target.closest(".accent-pick [data-accent]"))) { S.accent = b.getAttribute("data-accent"); save(); renderAll(); }
      else if ((b = e.target.closest("[data-act]"))) {
        var menu = b.closest("details"); if (menu) menu.open = false;
        var act = b.getAttribute("data-act");
        ({
          print: function () { printCv(AppUnlock.isUnlocked(SLUG)); },
          "pdf-clean": paid(function () { printCv(true); }, "PDF נקי בלי סימן מים, עם טקסט אמיתי שמערכות סינון קוראות."),
          docx: paid(docx, "קובץ Word לעריכה ולמשרות שמבקשות קורות חיים ב-Word."),
          sample: sample,
          "copy-he": function () { S.en = JSON.parse(JSON.stringify(S.he)); save(); renderAll(); toast("הועתק מהעברית: עכשיו מתרגמים כל שדה לאנגלית"); },
          backup: function () { AppZip.download(new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }), "cv-backup.json"); },
          restore: function () { $("#file-json").click(); },
          reset: function () { if (confirm("למחוק את כל מה שכתבתם (בעברית ובאנגלית)?")) { S = blank(); save(); renderAll(); } },
          unlock: function () { AppUnlock.open(SLUG, { title: "הגרסה המלאה של בונה קורות החיים · ₪19", features: UNLOCK_FEATS }); }
        }[act] || function () {})();
      }
      $$("details.menu[open]").forEach(function (m) { if (!m.contains(e.target)) m.open = false; });
    });
    $("#file-json").addEventListener("change", function (e) {
      var f = e.target.files[0]; e.target.value = "";
      if (!f) return;
      f.text().then(function (txt) {
        var d = JSON.parse(txt);
        if (!d || !d.he || !d.en) throw new Error("bad");
        if (!confirm("לשחזר מהגיבוי? מה שכתוב עכשיו יוחלף.")) return;
        S = d; save(); renderAll(); toast("הגיבוי שוחזר");
      }).catch(function () { toast("זה לא קובץ גיבוי של בונה קורות החיים"); });
    });
    $$(".app-tabs [data-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".app-tabs [data-tab]").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
        $(".cv-layout").setAttribute("data-show", b.getAttribute("data-tab"));
        fit();
      });
    });
    window.addEventListener("resize", fit);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    AppUnlock.onChange(renderPlan);
    renderAll();
    if (new URLSearchParams(location.search).get("demo") === "1" && isEmpty(S.he)) sample();
  }
  window.CvApp = { state: function () { return S; }, render: renderAll };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
