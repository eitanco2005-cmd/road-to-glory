// End-to-end test of the web apps (apps/seating, apps/cv) in TEST mode (?test=1, no real payment).
//   node tools/apps/e2e_apps.js [--shots DIR]
// Serves docs/ at the domain root on a local port, then for each app: free use -> watermarked print ->
// locked export opens the purchase dialog -> test payment -> unlock without redirect -> clean exports
// (XLSX / DOCX files are opened with openpyxl / python-docx, PDFs read with pdftotext) -> thanks page ->
// test unlock does not leak into non-test mode -> 375px / 1280px layout has no horizontal overflow.
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(args[args.indexOf("--shots") + 1]) : null;
const PORT = 8771;
const BASE = `http://localhost:${PORT}/`;
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "tp-apps-e2e-"));
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".xml": "application/xml" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});

function pdfText(file) { return execFileSync("pdftotext", ["-nodiag", file, "-"]).toString(); }
function py(code, file) { return execFileSync("python3", ["-c", code, file]).toString(); }

async function newPage(browser, vp) {
  const ctx = await browser.newContext({ viewport: vp || { width: 1280, height: 900 }, acceptDownloads: true, locale: "he-IL" });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|paypal\.com/, r => r.abort());
  const page = await ctx.newPage();
  page.errors = [];
  page.on("pageerror", e => page.errors.push(e.message));
  // capture print instead of opening the dialog
  await page.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
  return page;
}
async function printPdf(page, file) {
  // the app has filled #print-area and set body.printing; render it as the browser would print it
  await page.evaluate(() => document.body.classList.add("printing"));
  await page.pdf({ path: file, format: "A4", printBackground: true });
  await page.evaluate(() => document.body.classList.remove("printing"));
  return pdfText(file);
}
async function noOverflow(page, label) {
  // measured on <main>: the shared site header is W1's (and is wider with the fallback font used offline)
  const w = await page.evaluate(() => [document.getElementById("main").scrollWidth, window.innerWidth]);
  ok(w[0] <= w[1] + 1, `${label}: no horizontal overflow (${w[0]} <= ${w[1]})`);
}
async function testPay(page, slug) {
  const dlg = page.locator("dialog.unlock-dialog");
  await dlg.waitFor({ state: "visible", timeout: 5000 });
  ok(true, `${slug}: locked export opens the purchase dialog`);
  const btn = dlg.locator(`[data-test-pay="${slug}"]`);
  await btn.waitFor({ timeout: 8000 });
  ok((await dlg.textContent()).includes("₪"), `${slug}: dialog shows the price`);
  const url = page.url();
  await btn.click();
  await dlg.locator(".success-callout").waitFor({ timeout: 5000 });
  ok(page.url() === url, `${slug}: no redirect after payment`);
  const stored = await page.evaluate(s => JSON.parse(localStorage.getItem("tp-unlock:" + s) || "null"), slug);
  ok(stored && /^TEST-/.test(stored.o) && stored.test === true, `${slug}: unlock token stored (${stored && stored.o})`);
  ok(await dlg.locator(`a[href*="thanks/?p=${slug}"]`).count() > 0, `${slug}: dialog offers the thanks page link`);
  await dlg.locator("button.btn.block.mt-2").click();
  await page.waitForTimeout(150);
  ok((await page.textContent("#plan")).includes("גרסה מלאה פעילה"), `${slug}: plan badge switches to full version`);
  return stored.o;
}

async function seating(browser) {
  console.log("\n== seating ==");
  const page = await newPage(browser);
  await page.goto(BASE + "apps/seating/?test=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  // add a guest by hand
  await page.fill("#add-guest [name=gname]", "משפחת בדיקה");
  await page.fill("#add-guest [name=gn]", "3");
  await page.fill("#add-guest [name=gside]", "צד החתן");
  await page.click("#add-guest button[type=submit]");
  ok((await page.textContent("#un-count")) === "3", "manual add: 3 people unassigned");
  // paste list
  await page.click(".guest-panel [data-act=paste]");
  await page.fill("#pd-text", "שם\tכמות\tצד\tקבוצה\nדנה כהן\t2\tצד הכלה\tחברים\nיוסי לוי\t1\tצד הכלה\tחברים\nמשפחת אבו (4)");
  await page.click("dialog form.dlg-form button[type=submit]");
  ok((await page.textContent("#un-count")) === "10", "paste with header row + '(4)' count: 10 people unassigned");
  // CSV import (Hebrew header, windows-1255 safe path is utf-8 here)
  const csv = path.join(TMP, "guests.csv");
  fs.writeFileSync(csv, "﻿שם,מספר אנשים,צד,קבוצה\n\"כהן, רותי ודני\",2,צד הכלה,עבודה\nאבי,1,צד החתן,צבא\n");
  await page.setInputFiles("#file-in", csv);
  await page.waitForTimeout(300);
  ok((await page.textContent("#un-count")) === "13", "CSV import with quoted comma: 13 people unassigned");
  // tables
  await page.click(".app-toolbar [data-act=add-tables]");
  await page.fill("#at-count", "2"); await page.fill("#at-seats", "8");
  await page.click("dialog form.dlg-form button[type=submit]");
  ok(await page.locator(".t-card").count() === 2, "2 tables added");
  await page.click(".app-toolbar [data-act=auto]");
  await page.waitForTimeout(200);
  ok((await page.textContent("#un-count")) === "0", "auto-seat seats everyone (13 in 16 seats)");
  ok(await page.isVisible("#ready") && decodeURIComponent(await page.getAttribute("#ready a[data-act=whatsapp]", "href")).includes("tichnun.netlify.app/apps/seating/"), "Hebrew ready banner with WhatsApp share link");
  // drag a chip back to the unassigned list (mouse)
  const chip = page.locator(".t-card .g-chip").first();
  const box = await chip.boundingBox(), tgt = await page.locator("#unassigned").boundingBox();
  await page.mouse.move(box.x + 10, box.y + 8); await page.mouse.down();
  await page.mouse.move(box.x + 40, box.y + 30, { steps: 4 });
  await page.mouse.move(tgt.x + tgt.width / 2, tgt.y + 30, { steps: 8 }); await page.mouse.up();
  await page.waitForTimeout(150);
  ok((await page.textContent("#un-count")) !== "0", "drag & drop moves a guest out of a table");
  await page.click(".app-toolbar [data-act=undo]");
  ok((await page.textContent("#un-count")) === "0", "undo restores the seat");
  // conflict: keep-apart pair placed together
  await page.evaluate(() => {
    const S = SeatingApp.state(); const t = S.tables[0].id;
    const a = S.guests[0], b = S.guests[1]; a.table = t; b.table = t; S.apart.push([a.id, b.id]); SeatingApp.render();
  });
  ok(await page.locator(".t-card.conflict").count() >= 1 && (await page.textContent(".t-card.conflict .t-warn")).includes("ביקשו לא לשבת יחד"), "keep-apart conflict is flagged");
  // free print = watermarked
  await page.click("summary:has-text('הדפסה וייצוא')");
  await page.click("[data-act=print]");
  await page.waitForTimeout(150);
  ok(await page.evaluate(() => window.__printed) === 1 && await page.locator("#print-area .wm").count() === 1, "free print has a watermark");
  let txt = await printPdf(page, path.join(TMP, "seating-free.pdf"));
  ok(/בגרסה החינמית/.test(txt) && /כניסה|הסינכ/.test(txt), "free PDF: watermark text + entrance list present");
  // locked xlsx -> buy -> unlock
  await page.click("summary:has-text('הדפסה וייצוא')");
  await page.click("[data-act=xlsx]");
  const order = await testPay(page, "seating-chart");
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, "seating-unlocked.png") });
  // xlsx download
  await page.click("summary:has-text('הדפסה וייצוא')");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("[data-act=xlsx]")]);
  const xf = path.join(TMP, "seating.xlsx"); await dl.saveAs(xf);
  const out = py("import openpyxl,sys;wb=openpyxl.load_workbook(sys.argv[1]);print(wb.sheetnames);ws=wb.worksheets[0];print(ws.sheet_view.rightToLeft);print(ws.max_row);print([c.value for c in wb.worksheets[1][1]])", xf);
  ok(out.includes("הושבה לפי שולחן") && out.includes("True") && out.includes("'שם', 'אנשים', 'צד', 'קבוצה', 'שולחן'"), "XLSX opens in openpyxl: 3 RTL sheets with headers\n     " + out.trim().replace(/\n/g, "\n     "));
  // clean print + cards
  await page.click("summary:has-text('הדפסה וייצוא')");
  await page.click("[data-act=pdf-clean]");
  ok(await page.locator("#print-area .wm").count() === 0, "clean print has no watermark");
  txt = await printPdf(page, path.join(TMP, "seating-clean.pdf"));
  ok(!/בגרסה החינמית/.test(txt), "clean PDF has no watermark text");
  await page.click("summary:has-text('הדפסה וייצוא')");
  await page.click("[data-act=cards]");
  ok(await page.locator("#print-area .p-card").count() === 2, "table cards: one card per table");
  await printPdf(page, path.join(TMP, "seating-cards.pdf"));
  if (SHOTS) {
    fs.copyFileSync(path.join(TMP, "seating-free.pdf"), path.join(SHOTS, "seating-free.pdf"));
    fs.copyFileSync(path.join(TMP, "seating-cards.pdf"), path.join(SHOTS, "seating-cards.pdf"));
  }
  // import the exported xlsx back (fresh data)
  await page.evaluate(() => { localStorage.removeItem("tp-seating-v1"); });
  await page.reload();
  await page.setInputFiles("#file-in", xf);
  await page.waitForTimeout(500);
  const st = await page.evaluate(() => { const S = SeatingApp.state(); return [S.guests.reduce((s, g) => s + g.n, 0), S.tables.length, S.guests.filter(g => g.table).length]; });
  ok(st[0] === 13 && st[1] === 2 && st[2] > 0, `XLSX re-import restores guests and tables (${st})`);
  // thanks page
  await page.goto(BASE + `thanks/?p=seating-chart&o=${order}&test=1`);
  await page.waitForSelector("#ok:not([hidden])");
  ok((await page.textContent("#downloads")).includes("הגרסה המלאה פתוחה") && await page.locator('#downloads a[href*="apps/seating/"]').count() === 1, "thanks page explains the unlock and links back to the app");
  // non-test mode must not honour a test unlock
  await page.goto(BASE + "apps/seating/");
  ok(!(await page.textContent("#plan")).includes("גרסה מלאה פעילה"), "test unlock is ignored outside ?test=1");
  ok(page.errors.length === 0, "no JS errors" + (page.errors.length ? ": " + page.errors.join(" | ") : ""));
  await page.context().close();

  // a real (non-test) stored unlock works without ?test=1; thanks page link restores on another device
  const p2 = await newPage(browser);
  await p2.goto(BASE + "thanks/?p=seating-chart&o=REALORDER123");
  await p2.waitForSelector("#ok:not([hidden])");
  await p2.goto(BASE + "apps/seating/?demo=1");
  ok((await p2.textContent("#plan")).includes("גרסה מלאה פעילה"), "opening the thanks link unlocks the app in a new browser");
  await p2.context().close();

  for (const vp of [{ width: 375, height: 812 }, { width: 1280, height: 900 }]) {
    const p = await newPage(browser, vp);
    await p.goto(BASE + "apps/seating/?demo=1");
    await p.click(".app-toolbar [data-act=auto]");
    await p.waitForTimeout(200);
    await noOverflow(p, `seating ${vp.width}px (guests)`);
    if (vp.width < 900) { await p.click("[data-tab=tables]"); await noOverflow(p, "seating 375px (tables)"); }
    if (SHOTS) await p.screenshot({ path: path.join(SHOTS, `seating-${vp.width}.png`), fullPage: vp.width < 900 });
    ok(p.errors.length === 0, `seating ${vp.width}px: no JS errors`);
    await p.context().close();
  }
}

async function seatingEn(browser) {
  console.log("\n== seating (English, USD) ==");
  const page = await newPage(browser);
  await page.goto(BASE + "en/apps/seating/?test=1&demo=1");
  await page.waitForTimeout(300);
  ok((await page.textContent("#stats")).includes("guests") && (await page.getAttribute("html", "dir")) === "ltr", "English UI, LTR");
  ok(await page.isHidden("#ready"), "ready banner hidden before seating");
  await page.click(".app-toolbar [data-act=auto]");
  await page.waitForTimeout(200);
  ok(await page.isVisible("#ready") && (await page.textContent("#ready")).includes("$9"), "ready banner appears with the $9 export offer");
  const wa = await page.getAttribute("#ready a[data-act=whatsapp]", "href");
  ok(/^https:\/\/wa\.me\/\?text=/.test(wa) && decodeURIComponent(wa).includes("https://tichnun.netlify.app/en/apps/seating/") && !decodeURIComponent(wa).includes("Perez"), "WhatsApp link: wa.me, prefilled text + tool link, no guest names");
  await page.click("#ready [data-act=print]");
  const txt = await printPdf(page, path.join(TMP, "seating-en-free.pdf"));
  ok(/free version of Tichnun Plus/.test(txt) && /Escort list/.test(txt), "English free PDF: watermark + escort list");
  await page.click("#ready [data-act=pdf-clean]");
  const dlg = page.locator("dialog.unlock-dialog");
  await dlg.locator("[data-test-pay=seating-chart-en]").waitFor({ timeout: 8000 });
  ok((await dlg.textContent()).includes("$9") && (await dlg.textContent()).includes("Prices in US dollars"), "English dialog: USD price and English checkout copy");
  await dlg.locator("[data-test-pay=seating-chart-en]").click();
  await dlg.locator(".success-callout").waitFor({ timeout: 5000 });
  const u = await page.evaluate(() => [localStorage.getItem("tp-unlock:seating-chart-en"), localStorage.getItem("tp-unlock:seating-chart")]);
  ok(u[0] && !u[1], "unlock stored for seating-chart-en only (Hebrew product stays locked)");
  const links = await dlg.locator('a[href*="thanks/"]').evaluateAll(as => as.map(a => a.getAttribute("href")));
  ok(links.length > 0 && links.every(h => h.includes("en/thanks/?p=seating-chart-en")), "order links point to en/thanks/");
  await dlg.locator("button.btn.block.mt-2").click();
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("#ready [data-act=xlsx]")]);
  const xf = path.join(TMP, "seating-en.xlsx"); await dl.saveAs(xf);
  const out = py("import openpyxl,sys;wb=openpyxl.load_workbook(sys.argv[1]);print(wb.sheetnames);print(wb.worksheets[0].sheet_view.rightToLeft)", xf);
  ok(out.includes("By table") && /False|None/.test(out), "English XLSX: English sheets, left-to-right");
  ok(page.errors.length === 0, "no JS errors" + (page.errors.length ? ": " + page.errors.join(" | ") : ""));
  await page.context().close();
  // English thanks page restores the unlock in a fresh browser; legacy "tp-unlocks" object still honoured
  const p3 = await newPage(browser);
  await p3.goto(BASE + "en/thanks/?p=seating-chart-en&o=REALORDER-EN");
  await p3.waitForSelector("#ok:not([hidden])");
  ok((await p3.textContent("#downloads")).includes("unlocked in this browser") && await p3.locator('#downloads a[href*="en/apps/seating/"]').count() === 1, "en/thanks explains the unlock and links back to the tool");
  await p3.goto(BASE + "en/apps/seating/");
  ok((await p3.textContent("#plan")).includes("Full version active"), "en/thanks link unlocks the English tool in a new browser");
  await p3.evaluate(() => { localStorage.clear(); localStorage.setItem("tp-unlocks", JSON.stringify({ "seating-chart-en": { o: "OLD", t: 1, test: false } })); });
  await p3.reload();
  ok((await p3.textContent("#plan")).includes("Full version active"), "legacy tp-unlocks store still honoured (compat alias)");
  await p3.context().close();
  for (const vp of [{ width: 375, height: 812 }, { width: 1280, height: 900 }]) {
    const p = await newPage(browser, vp);
    await p.goto(BASE + "en/apps/seating/?demo=1");
    await p.click(".app-toolbar [data-act=auto]");
    await noOverflow(p, `en seating ${vp.width}px`);
    if (vp.width < 900) { await p.click("[data-tab=tables]"); await noOverflow(p, "en seating 375px (tables)"); }
    ok(p.errors.length === 0, `en seating ${vp.width}px: no JS errors`);
    await p.context().close();
  }
}

async function cv(browser) {
  console.log("\n== cv ==");
  const page = await newPage(browser);
  await page.goto(BASE + "apps/cv/?test=1");
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.fill("#f-name", "ישראלה ישראלי");
  await page.fill("#f-title", "מפתחת תוכנה");
  await page.click("[data-add=experience]");
  await page.locator("#list-experience input[data-k=role]").fill("מפתחת Full Stack");
  await page.locator("#list-experience input[data-k=org]").fill("חברה בע\"מ");
  await page.locator("#list-experience input[data-k=start]").fill("2021");
  await page.locator("#list-experience textarea").fill("פיתוח API\n- שיפור ביצועים ב-40%");
  const prev = await page.textContent("#cv-page");
  ok(prev.includes("ישראלה ישראלי") && prev.includes("2021 – היום") && prev.includes("שיפור ביצועים ב-40%"), "live preview updates (name, 'היום' for open end date, bullets)");
  for (const t of ["modern", "minimal", "executive", "classic"]) {
    await page.click(`[data-tpl=${t}]`);
    ok(await page.locator(`#cv-page.tpl-${t}`).count() === 1, `template ${t} applied`);
  }
  await page.click("[data-lang=en]");
  ok(await page.locator("#copy-he").isVisible(), "English mode offers copying the Hebrew content");
  await page.click("#copy-he");
  ok((await page.getAttribute("#cv-page", "dir")) === "ltr" && (await page.textContent("#cv-page")).includes("Experience"), "English CV is LTR with English headings");
  await page.click("[data-lang=he]");
  // free print
  await page.click("summary:has-text('הורדה')");
  await page.click("[data-act=print]");
  ok(await page.locator("#print-area .wm").count() === 1, "free CV print has a watermark");
  let txt = await printPdf(page, path.join(TMP, "cv-free.pdf"));
  ok(/בגרסה החינמית/.test(txt), "free CV PDF contains watermark text");
  // locked docx -> pay
  await page.click("summary:has-text('הורדה')");
  await page.click("[data-act=docx]");
  await testPay(page, "cv-builder");
  await page.click("summary:has-text('הורדה')");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("[data-act=docx]")]);
  const df = path.join(TMP, "cv.docx"); await dl.saveAs(df);
  const out = py("import docx,sys;d=docx.Document(sys.argv[1]);ps=[p.text for p in d.paragraphs];print(len(ps));print(ps[0]);print('ניסיון תעסוקתי' in ps);print(any('שיפור ביצועים' in p for p in ps));print(d.paragraphs[0]._p.pPr.xml.count('bidi'))", df);
  ok(/ישראלה ישראלי/.test(out) && /True\nTrue\n1/.test(out), "DOCX opens in python-docx: name, Hebrew headings, bullets, bidi paragraphs");
  try {
    execFileSync("soffice", ["--headless", "--convert-to", "pdf", "--outdir", TMP, df], { stdio: "ignore", timeout: 90000 });
    const t2 = pdfText(path.join(TMP, "cv.pdf"));
    ok(t2.includes("ישראלה") || t2.includes("הלארשי"), "DOCX renders in LibreOffice");
  } catch (e) { console.log("SKIP LibreOffice conversion: " + e.message.split("\n")[0]); }
  await page.click("summary:has-text('הורדה')");
  await page.click("[data-act=pdf-clean]");
  ok(await page.locator("#print-area .wm").count() === 0, "clean CV print has no watermark");
  txt = await printPdf(page, path.join(TMP, "cv-clean.pdf"));
  ok(!/בגרסה החינמית/.test(txt) && /ישראלה|הלארשי/.test(txt), "clean CV PDF: real selectable text, no watermark");
  if (SHOTS) { fs.copyFileSync(path.join(TMP, "cv-clean.pdf"), path.join(SHOTS, "cv-clean.pdf")); fs.copyFileSync(df, path.join(SHOTS, "cv.docx")); }
  ok(page.errors.length === 0, "no JS errors" + (page.errors.length ? ": " + page.errors.join(" | ") : ""));
  await page.context().close();

  for (const vp of [{ width: 375, height: 812 }, { width: 1280, height: 900 }]) {
    const p = await newPage(browser, vp);
    await p.goto(BASE + "apps/cv/?demo=1");
    await p.waitForTimeout(200);
    await noOverflow(p, `cv ${vp.width}px (form)`);
    if (vp.width < 900) { await p.click("[data-tab=preview]"); await p.waitForTimeout(100); await noOverflow(p, "cv 375px (preview)"); }
    if (SHOTS) await p.screenshot({ path: path.join(SHOTS, `cv-${vp.width}.png`), fullPage: false });
    ok(p.errors.length === 0, `cv ${vp.width}px: no JS errors`);
    await p.context().close();
  }
}

async function pages(browser) {
  console.log("\n== product pages + guides ==");
  const urls = ["p/seating-chart/", "p/cv-builder/", "p/seating-chart/guides/how-to-seat-guests/", "p/seating-chart/guides/tables-and-seats/",
    "p/cv-builder/guides/how-to-write-cv/", "p/cv-builder/guides/cv-in-english/", "products/", ""];
  for (const vp of [{ width: 375, height: 812 }, { width: 1280, height: 900 }]) {
    const p = await newPage(browser, vp);
    for (const u of urls) {
      const r = await p.goto(BASE + u + "?test=1");
      ok(r.status() === 200, `${u || "home"} ${vp.width}px: 200`);
      await p.waitForTimeout(150);
      await noOverflow(p, `${u || "home"} ${vp.width}px`);
    }
    ok(p.errors.length === 0, `pages ${vp.width}px: no JS errors` + (p.errors.length ? ": " + p.errors.join(" | ") : ""));
    await p.context().close();
  }
  // product page buy box renders and unlocks in test mode
  const p = await newPage(browser);
  await p.goto(BASE + "p/cv-builder/?test=1");
  await p.locator("[data-test-pay=cv-builder]").first().click();
  await p.waitForTimeout(300);
  ok(await p.evaluate(() => !!localStorage.getItem("tp-unlock:cv-builder")), "product page purchase stores the unlock");
  // regression: a normal file product still redirects to the thanks page (checkout.js backward compatible)
  await p.goto(BASE + "p/wedding-planner/?test=1");
  await p.locator("[data-test-pay=wedding-planner]").first().click();
  await p.waitForURL(/thanks\/\?p=wedding-planner&o=TEST-/, { timeout: 8000 });
  await p.waitForSelector("#ok:not([hidden])");
  ok(await p.locator("#downloads a.dl").count() > 0 && await p.isVisible("#howto"), "file product: redirect to thanks page with downloads (unchanged)");
  // catalog shows the apps with their own badge
  await p.goto(BASE + "products/");
  await p.waitForTimeout(400);
  ok((await p.textContent("[data-category=apps]")).includes("כלי אונליין · חינם לשימוש") && await p.locator("[data-category=apps] .product-card:not(.is-soon)").count() === 2, "products page lists both apps as live with the app badge");
  await p.context().close();
}

(async () => {
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  try {
    await seating(browser);
    await seatingEn(browser);
    await cv(browser);
    if (fs.existsSync(path.join(DOCS, "p/cv-builder/index.html"))) await pages(browser);
  } catch (e) { console.error(e); failures++; }
  await browser.close();
  server.close();
  console.log(`\n${failures ? "FAILED: " + failures : "ALL PASSED"}`);
  process.exit(failures ? 1 : 0);
})();
