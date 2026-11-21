// End-to-end test of the wedding focus (round 4) in TEST mode (no real payment).
//   node tools/site/e2e_wedding.js [--shots DIR]
// Hub + home + header/footer links -> wedding cost calculator -> timeline generator (ticks persist, ICS) ->
// RSVP app (free use, CSV/Google-Contacts/VCF import with picker, WhatsApp link, 80-invitation limit, test unlock,
// Excel export read with openpyxl, one-click hand-off to the seating app) -> wedding bundle test purchase unlocks all
// three apps -> 8 gift pages + 3 guest guides (JSON-LD, preset calculator link, hub link) -> R5 vendor price guides
// (hub + 10 pages: JSON-LD, cited sources, WhatsApp share, budget box = calculator total, presets) -> 375/1280 layout.
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
const PORT = 8779;
const BASE = `http://localhost:${PORT}/`;
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "tp-wedding-e2e-"));
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

async function newCtx(browser, vp) {
  const ctx = await browser.newContext({ viewport: vp || { width: 1280, height: 900 }, acceptDownloads: true, locale: "he-IL" });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|paypal\.com/, r => r.abort());
  return ctx;
}
async function newPage(ctx) {
  const page = await ctx.newPage();
  page.errors = [];
  page.on("pageerror", e => page.errors.push(e.message));
  page.on("dialog", d => d.accept());
  await page.addInitScript(() => { window.print = () => { window.__printed = (window.__printed || 0) + 1; }; });
  return page;
}
async function noOverflow(page, label) {
  const w = await page.evaluate(() => [document.getElementById("main").scrollWidth, window.innerWidth]);
  ok(w[0] <= w[1] + 1, `${label}: no horizontal overflow (${w[0]} <= ${w[1]})`);
}
const text = (page, sel) => page.locator(sel).first().innerText();
const money = s => parseInt(String(s).replace(/[^\d]/g, ""), 10);
async function shot(page, name) { if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await page.screenshot({ path: path.join(SHOTS, name + ".png"), fullPage: false }); } }
async function testPay(page) {
  const btn = page.locator("dialog.unlock-dialog [data-test-pay]");
  await btn.waitFor({ timeout: 8000 });
  await btn.click();
  await page.locator("dialog.unlock-dialog .success-callout").waitFor({ timeout: 8000 });
  await page.locator("dialog.unlock-dialog .dlg-x").click();
}
async function upload(page, act, name, content) {
  const file = path.join(TMP, name);
  fs.writeFileSync(file, content);
  const [chooser] = await Promise.all([page.waitForEvent("filechooser"), page.evaluate(a => document.querySelector('.panel [data-act="' + a + '"]').click(), act)]);
  await chooser.setFiles(file);
}

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  try {
    /* ---------- home + header/footer ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE);
      const firstH2 = await page.locator("main h2").first().innerText();
      ok(/אורח/.test(firstH2), "home: first section is the wedding guest/couple paths (" + firstH2 + ")");
      ok(await page.locator('main a[href="chatuna/"]').count() > 0 && await page.locator('main a[href="apps/rsvp/"]').count() > 0, "home: links the hub and the RSVP app");
      ok(await page.locator('#site-header .nav a:has-text("חתונה")').count() === 1, "header: has a חתונה link");
      await page.locator("#site-footer .footer-h").first().waitFor();
      const fh = await page.locator("#site-footer .footer-h").allInnerTexts();
      ok(fh[0] === "חתונה", "footer: first column is חתונה (" + fh.join(", ") + ")");
      ok(await page.locator('#site-footer a[href$="tools/wedding-cost/"]').count() === 1, "footer: links the cost calculator");
      ok(!page.errors.length, "home: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- hub ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "chatuna/");
      ok(/הכל לחתונה/.test(await page.title()), "hub: title");
      for (const href of ["../tools/wedding-gift/", "../tools/wedding-cost/", "../tools/wedding-timeline/", "../apps/rsvp/", "../apps/seating/", "../apps/invite/", "haavarat-kesef/", "ma-lilbosh/", "rayonot-matana/"])
        ok(await page.locator(`main a[href="${href}"]`).count() > 0, "hub: links " + href);
      ok(await page.locator('main a[href^="kama-lasim/"]').count() === 8, "hub: links all 8 gift quick-answer pages");
      const ld = JSON.parse(await page.locator('script[type="application/ld+json"]').innerText());
      ok(ld["@graph"].some(x => x["@type"] === "FAQPage") && ld["@graph"].some(x => x["@type"] === "BreadcrumbList"), "hub: FAQ + Breadcrumb JSON-LD");
      ok(!page.errors.length, "hub: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- cost calculator ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "tools/wedding-cost/");
      ok(await text(page, "#r-total") === "₪185,000", "cost: default scenario (250, center, summer) = ₪185,000 like the page table");
      await page.selectOption("#region", "other");
      ok(await text(page, "#r-total") === "₪165,000", "cost: north/south = ₪165,000 like the page table");
      await page.check('input[name=season][value=winter]'); await page.selectOption("#region", "center");
      ok(await text(page, "#r-total") === "₪158,000", "cost: winter = ₪158,000 like the page table");
      await page.fill("#plate", "300");
      ok((await text(page, "#r-plate")).includes("₪300"), "cost: typed plate price overrides the estimate");
      const t1 = money(await text(page, "#r-total"));
      await page.uncheck('input[name=use_dress]');
      ok(money(await text(page, "#r-total")) < t1, "cost: unticking a vendor lowers the total");
      await page.fill('input[name=amt_photo]', "20000");
      ok((await text(page, "#r-lines")).includes("₪20,000"), "cost: a typed vendor quote is used");
      await page.locator("[data-share] a[href*='wa.me']").focus(); // the share bar refreshes its link on a short debounce
      const wa = await page.locator("[data-share] a[href*='wa.me']").getAttribute("href");
      ok(/wa\.me/.test(wa) && decodeURIComponent(wa).includes("#c&"), "cost: WhatsApp share link carries the inputs");
      const link = decodeURIComponent(wa).match(/https?:\/\/\S+#c&\S+/)[0].replace("https://tichnun.netlify.app/", BASE);
      const p2 = await newPage(await newCtx(browser));
      await p2.goto(link);
      ok(await text(p2, "#r-total") === await text(page, "#r-total"), "cost: shared link reopens the same total");
      ok(await page.locator('meta[property="og:image"][content$="og/wedding-cost.png"]').count() === 1 && fs.existsSync(path.join(DOCS, "assets/og/wedding-cost.png")), "cost: og image");
      await page.goto(BASE + "embed/wedding-cost/");
      ok(await page.locator("#r-total").count() === 1 && /₪\d/.test(await text(page, "#r-total")), "cost: embed computes");
      ok(!page.errors.length && !p2.errors.length, "cost: no page errors " + page.errors.concat(p2.errors).join("; "));
      await ctx.close();
    }

    /* ---------- timeline ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "tools/wedding-timeline/");
      const now = new Date(), y = now.getFullYear() + 1;
      await page.fill("#day", "10"); await page.selectOption("#month", String(now.getMonth() + 1)); await page.selectOption("#year", String(y));
      const months = await page.locator(".tl-month h3").allInnerTexts();
      ok(months.length >= 12 && /אחרי החתונה/.test(months[months.length - 1]), "timeline: ~1 year out gives a month-by-month plan (" + months.length + " groups)");
      ok((await text(page, "#tl-summary")).includes("10." + (now.getMonth() + 1) + "." + y), "timeline: summary shows the wedding date");
      const n0 = await page.locator(".tl-month li").count();
      await page.check('input[name=ceremony][value=other]');
      const items = await page.locator(".tl-month li").allInnerTexts();
      ok(!items.some(t => /פתיחת תיק ברבנות/.test(t)) && items.some(t => /משרד הפנים/.test(t)), "timeline: civil/abroad swaps the rabbinate tasks");
      await page.check('input[name=ceremony][value=rabbanut]');
      ok(await page.locator(".tl-month li").count() === n0, "timeline: back to rabbanut");
      await page.locator('[data-task="photo"]').check();
      await page.reload();
      await page.fill("#day", "10"); await page.selectOption("#month", String(now.getMonth() + 1)); await page.selectOption("#year", String(y));
      ok(await page.locator('[data-task="photo"]').isChecked(), "timeline: ticks persist after reload");
      // short notice: 3 months out -> overdue bucket first
      const s = new Date(now.getTime() + 95 * 864e5);
      await page.fill("#day", String(s.getDate())); await page.selectOption("#year", String(s.getFullYear())); await page.selectOption("#month", String(s.getMonth() + 1));
      ok(/להשלים עכשיו/.test(await page.locator(".tl-month h3").first().innerText()) && await page.locator("#tl-short").isVisible(), "timeline: short notice puts overdue tasks first + compressed-plan tip");
      const [dl] = await Promise.all([page.waitForEvent("download"), page.click("#tl-ics")]);
      const ics = fs.readFileSync(await dl.path(), "utf8");
      ok(/BEGIN:VCALENDAR/.test(ics) && (ics.match(/BEGIN:VEVENT/g) || []).length > 20 && !/UID:photo-/.test(ics), "timeline: ICS has the open tasks (ticked ones left out)");
      await page.click("#tl-print");
      ok(await page.evaluate(() => window.__printed) === 1, "timeline: print button");
      ok(!page.errors.length, "timeline: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- RSVP app ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "apps/rsvp/?test=1");
      ok(/0\/80/.test(await text(page, "#plan")), "rsvp: free plan pill shows 0/80");
      await page.fill("#ev-title", "החתונה של דנה ויואב");
      await page.fill('#add-guest [name=gname]', "משפחת כהן"); await page.fill('#add-guest [name=gn]', "4");
      await page.fill('#add-guest [name=gside]', "צד הכלה"); await page.fill('#add-guest [name=gphone]', "050-123-4567");
      await page.click('#add-guest button[type=submit]');
      ok(await page.locator(".g-row").count() === 1, "rsvp: add an invitation");
      const wa = await page.locator(".g-row .wa").getAttribute("href");
      ok(/^https:\/\/wa\.me\/972501234567\?text=/.test(wa) && decodeURIComponent(wa).includes("משפחת כהן") && decodeURIComponent(wa).includes("החתונה של דנה ויואב"), "rsvp: WhatsApp reminder link (972 number, name, event)");
      await page.locator('.g-row [data-st="yes"]').click();
      ok((await text(page, "#stats")).replace(/\s+/g, " ").includes("אישרו 4"), "rsvp: ✓ confirms the whole invitation (4)");
      await page.locator(".g-row [data-coming]").fill("3"); await page.locator(".g-row [data-coming]").dispatchEvent("change"); await page.waitForTimeout(50);
      ok((await text(page, "#stats")).replace(/\s+/g, " ").includes("אישרו 3"), "rsvp: coming count 3 of 4");
      // edit: meals
      await page.locator(".g-row .g-name").click();
      await page.locator("dialog .eg [name=veg]").fill("1"); await page.locator("dialog .eg [name=kids]").fill("2");
      await page.locator("dialog .eg button[type=submit]").click();
      ok(/רגילה 0 · צמחוני 1 · מנת ילדים 2/.test(await text(page, "#meals")), "rsvp: meal counts (" + await text(page, "#meals") + ")");
      // Google Contacts CSV import with the picker
      await upload(page, "import", "contacts.csv", "Name,Given Name,Family Name,Phone 1 - Type,Phone 1 - Value,Group Membership\nנועה לוי,נועה,לוי,Mobile,+972 52-111-2222,* myContacts\nאבי מזרחי,אבי,מזרחי,Mobile,054-333-4444,* myContacts ::: חברים\nרופא שיניים,,,Work,03-5555555,* myContacts\n");
      await page.locator("dialog .pv-list").waitFor();
      ok(await page.locator("dialog .pv-list li").count() === 3, "rsvp: Google Contacts CSV parsed (3 contacts) into the picker");
      await page.locator("dialog .pv-list input").nth(2).uncheck();
      await page.fill("#pv-side", "צד החתן");
      await page.click('dialog [data-pv="add"]');
      const st = await page.evaluate(() => RsvpApp.state().guests.map(g => [g.name, g.phone, g.side, g.group]));
      ok(st.length === 3 && st.some(g => g[0] === "אבי מזרחי" && g[2] === "צד החתן" && g[3] === "חברים") && !st.some(g => g[0] === "רופא שיניים"), "rsvp: picked contacts added with side; unticked one skipped");
      // VCF
      await upload(page, "import", "contacts.vcf", "BEGIN:VCARD\r\nVERSION:3.0\r\nFN:סבתא רחל\r\nTEL;TYPE=CELL:0507654321\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:3.0\r\nN:שטרן;יעל;;;\r\nitem1.TEL:+972-58-1234567\r\nEND:VCARD\r\n");
      await page.locator("dialog .pv-list").waitFor();
      ok(await page.locator("dialog .pv-list li").count() === 2, "rsvp: VCF parsed (2 contacts)");
      await page.click('dialog [data-pv="add"]');
      ok(await page.evaluate(() => RsvpApp.state().guests.some(g => g.name === "יעל שטרן" && g.phone === "+972-58-1234567")), "rsvp: VCF N: field + item1.TEL");
      // hand-off to seating
      await page.click('#app .app-toolbar [data-act="seating"]');
      await page.locator('dialog input[name=who][value=open]').check();
      await Promise.all([page.waitForURL(/apps\/seating\/\?from=rsvp/), page.click('dialog [data-go="1"]')]);
      await page.waitForFunction(() => window.SeatingApp && SeatingApp.state().guests.length > 0);
      const seat = await page.evaluate(() => SeatingApp.state());
      ok(seat.guests.length === 5 && seat.guests.some(g => g.name === "משפחת כהן" && g.n === 3 && g.side === "צד הכלה"), "seating: received 5 invitations from RSVP (confirmed count 3 for משפחת כהן)");
      ok(seat.title === "החתונה של דנה ויואב", "seating: event title carried over");
      ok(await page.evaluate(() => localStorage.getItem("tp-handoff:seating")) === null, "seating: hand-off key consumed");
      // second hand-off merges instead of duplicating
      await page.goto(BASE + "apps/rsvp/?test=1");
      await page.click('#app .app-toolbar [data-act="seating"]');
      await page.locator('dialog input[name=who][value=open]').check();
      await Promise.all([page.waitForURL(/apps\/seating\//), page.click('dialog [data-go="1"]')]);
      await page.waitForFunction(() => window.SeatingApp && localStorage.getItem("tp-handoff:seating") === null);
      const n2 = await page.evaluate(() => SeatingApp.state().guests.map(g => g.name));
      ok(n2.length === 5, "seating: second hand-off merges by name (still 5: " + n2.join("/") + ")");
      // free limit
      await page.goto(BASE + "apps/rsvp/?test=1");
      await page.evaluate(() => { const rows = []; for (let i = 1; i <= 80; i++) rows.push("אורח " + i); document.querySelector('[data-act="paste"]').click(); document.querySelector("dialog .pv-text").value = rows.join("\n"); document.querySelector("dialog [data-ok]").click(); });
      await page.click('dialog [data-pv="all"]'); await page.click('dialog [data-pv="add"]');
      await page.locator("dialog.unlock-dialog").waitFor();
      ok(await page.evaluate(() => RsvpApp.state().guests.length) === 80, "rsvp: import stops at the free limit (80)");
      ok(await page.locator("#limit").isVisible(), "rsvp: limit banner shown");
      await shot(page, "rsvp-limit");
      await testPay(page);
      ok(/גרסה מלאה/.test(await text(page, "#plan")), "rsvp: unlocked after test payment, no redirect");
      await page.fill('#add-guest [name=gname]', "אורח 81"); await page.click('#add-guest button[type=submit]');
      ok(await page.evaluate(() => RsvpApp.state().guests.length) === 81, "rsvp: 81st invitation allowed after unlock");
      await page.locator('.app-toolbar summary[aria-label="עוד פעולות"]').click();
      const [dl] = await Promise.all([page.waitForEvent("download"), page.click('.app-toolbar [data-act="xlsx"]')]);
      const xf = path.join(TMP, "rsvp.xlsx"); await dl.saveAs(xf);
      const out = execFileSync("python3", ["-c", "import openpyxl,sys;wb=openpyxl.load_workbook(sys.argv[1]);print(wb.sheetnames);ws=wb['מוזמנים'];print(ws.max_row);print(ws.sheet_view.rightToLeft);print([c.value for c in wb['סיכום']['A']][:6])", xf]).toString();
      ok(/'מוזמנים', 'סיכום', 'טרם ענו'/.test(out) && /\n82\n/.test(out) && /True/.test(out), "rsvp: Excel export (3 RTL sheets, 81 rows + header)");
      // test unlock must not leak into non-test mode
      await page.goto(BASE + "apps/rsvp/");
      ok(/גרסה חינמית/.test(await text(page, "#plan")), "rsvp: test unlock does not count outside ?test=1");
      ok(!page.errors.length, "rsvp: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- wedding bundle purchase unlocks the 3 apps ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "chatuna/?test=1");
      const btn = page.locator('#bundle [data-test-pay="wedding-bundle"]');
      await btn.waitFor({ timeout: 8000 });
      await Promise.all([page.waitForURL(/thanks\/\?p=wedding-bundle/, { timeout: 15000 }), btn.click()]);
      await page.locator("#downloads h3").first().waitFor();
      const hs = await page.locator("#downloads h3").allInnerTexts();
      ok(hs.length === 4, "bundle: thanks page lists the 4 members (" + hs.length + ")");
      const un = await page.evaluate(() => ["rsvp-tracker", "seating-chart", "invitation-maker"].map(s => !!localStorage.getItem("tp-unlock:" + s)));
      ok(un.every(Boolean), "bundle: RSVP, seating and invitation unlocked in this browser");
      ok(await page.locator('#downloads a[href*="wedding-planner.xlsx"]').count() === 1, "bundle: planner download link");
      await page.goto(BASE + "apps/rsvp/?test=1");
      ok(/גרסה מלאה/.test(await text(page, "#plan")), "bundle: RSVP app shows the full version");
      ok(!page.errors.length, "bundle: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- gift pages + guest guides ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      const gift = ["gan-eruim", "makom-yukrati", "chatuna-ktana", "yom-shishi", "zug", "ben-dod", "lo-magiim", "tzafon-darom"].map(s => "chatuna/kama-lasim/" + s + "/");
      const guides = ["chatuna/ma-lilbosh/", "chatuna/haavarat-kesef/", "chatuna/rayonot-matana/"];
      const titles = new Set();
      for (const u of gift.concat(guides)) {
        await page.goto(BASE + u);
        titles.add(await page.title());
        const graph = JSON.parse(await page.locator('script[type="application/ld+json"]').first().innerText())["@graph"] || [];
        const faq = graph.find(x => x["@type"] === "FAQPage");
        const visible = await page.locator(".faq summary").allInnerTexts();
        ok(faq && faq.mainEntity.length === visible.length && faq.mainEntity.every((q, i) => q.name === visible[i].trim()), u + ": FAQ JSON-LD matches the visible FAQ");
        ok(await page.locator('a[href="../../"], a[href="../"]').filter({ hasText: "הכל לחתונה" }).count() > 0, u + ": links the hub");
        ok(await page.locator('a[href*="tools/wedding-gift/"]').count() > 0, u + ": links the calculator");
        ok(await page.locator("main table").count() > 0, u + ": has a table");
      }
      ok(titles.size === 11, "gift pages + guides: 11 unique titles");
      // preset link opens the calculator in the page's situation
      await page.goto(BASE + "chatuna/kama-lasim/yom-shishi/");
      const href = await page.locator('a[href*="tools/wedding-gift/#c&"]').first().getAttribute("href");
      await page.goto(new URL(href, BASE + "chatuna/kama-lasim/yom-shishi/").href);
      ok(await page.locator("#day").inputValue() === "friday", "yom-shishi: preset link opens the calculator on Friday");
      ok(!page.errors.length, "gift pages: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- R5: vendor price guides (chatuna/mechirim/) ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      const slugs = ["ulam", "tzalam", "dj", "simlat-kala", "ipur-kala", "rav", "hasaot", "magnetim", "itzuv-prachim", "chalifat-chatan"];
      const titles = new Set();
      await page.goto(BASE + "tools/wedding-cost/");
      const calcTotal = (await text(page, "#r-total")).trim();
      ok(await page.locator('a[href="../../chatuna/mechirim/"]').count() >= 1, "cost calculator: links the price guides");
      await page.goto(BASE + "chatuna/");
      ok(await page.locator('main a[href="mechirim/"]').count() >= 1, "wedding hub: links the price guides");
      await page.goto(BASE + "guides/wedding-vendor-contracts/");
      ok(await page.locator('.wedding-next a[href$="chatuna/mechirim/"]').count() === 1, "vendor-contracts guide: next step links the price guides");
      await page.goto(BASE + "chatuna/mechirim/");
      titles.add(await page.title());
      for (const sl of slugs) ok(await page.locator(`main a[href="${sl}/"]`).count() >= 1, "prices hub: links " + sl);
      ok(await page.locator(".price-table tbody tr").count() === slugs.length, "prices hub: one summary row per vendor");
      for (const u of ["chatuna/mechirim/"].concat(slugs.map(sl => "chatuna/mechirim/" + sl + "/"))) {
        await page.goto(BASE + u);
        if (u !== "chatuna/mechirim/") titles.add(await page.title());
        const graph = JSON.parse(await page.locator('script[type="application/ld+json"]').first().innerText())["@graph"] || [];
        const types = graph.map(x => x["@type"]);
        ok(types.includes("Article") && types.includes("BreadcrumbList") && types.includes("FAQPage"), u + ": Article + BreadcrumbList + FAQPage JSON-LD");
        const crumbs = graph.find(x => x["@type"] === "BreadcrumbList").itemListElement;
        ok(crumbs[crumbs.length - 1].item === "https://tichnun.netlify.app/" + u, u + ": breadcrumb ends at the canonical URL");
        const faq = graph.find(x => x["@type"] === "FAQPage");
        const visible = await page.locator(".faq summary").allInnerTexts();
        ok(faq.mainEntity.length === visible.length && faq.mainEntity.every((q, i) => q.name === visible[i].trim()), u + ": FAQ JSON-LD matches the visible FAQ");
        ok(await page.locator('a[href$="tools/wedding-cost/"], a[href*="tools/wedding-cost/#c&"]').count() > 0, u + ": links the cost calculator");
        ok(await page.locator('main a[href$="p/wedding-planner/"]').count() > 0 && await page.locator('main a[href$="#bundle"]').count() > 0, u + ": links the planner + bundle");
        // WhatsApp share of the page itself
        await page.locator("[data-share] [data-share-wa]").waitFor({ timeout: 5000 });
        const wa = decodeURIComponent(await page.locator("[data-share] [data-share-wa]").getAttribute("href"));
        ok(wa.startsWith("https://wa.me/?text=") && wa.includes(BASE + u), u + ": WhatsApp share links this page");
        // budget box agrees with the calculator's default scenario
        ok((await text(page, ".budget-fit")).includes(calcTotal), u + ": budget box uses the calculator total " + calcTotal);
        if (u === "chatuna/mechirim/") continue;
        // every price row cites at least one source, and every cited source exists with a link and a date line
        const rows = await page.locator(".price-table tbody tr").count();
        const cited = await page.locator(".price-table tbody tr").evaluateAll(trs => trs.map(tr => tr.querySelectorAll("a.ref").length));
        ok(rows >= 3 && cited.every(n => n >= 1), u + ": " + rows + " price rows, each with a source reference");
        const refs = await page.locator("a.ref").evaluateAll(as => [...new Set(as.map(a => a.getAttribute("href")))]);
        const srcOk = await page.evaluate(ids => ids.every(id => { const li = document.querySelector(id); return li && li.querySelector('a[href^="https://"]') && /20\d\d|ללא תאריך/.test(li.textContent); }), refs);
        ok(srcOk, u + ": all " + refs.length + " cited sources listed with link + date");
        ok(await page.locator(".data-note").count() === 1, u + ": says how strong the data is");
        ok(await page.locator(".price-table bdi[dir=ltr]").count() >= rows * 3, u + ": price cells are bidi-isolated (no reversed ranges in RTL)");
        ok(await page.locator('main a[href="../"]').filter({ hasText: "מחירי ספקים" }).count() > 0, u + ": breadcrumb links the prices hub");
      }
      ok(titles.size === 11, "price guides: 11 unique titles");
      // the rabbinate fee is the official 2026 figure
      await page.goto(BASE + "chatuna/mechirim/rav/");
      ok((await text(page, ".price-table")).includes("₪844"), "rav: official 2026 registration fee ₪844");
      // transport page opens the calculator with the transport line switched on
      await page.goto(BASE + "chatuna/mechirim/hasaot/");
      const th = await page.locator('.budget-fit a[href*="tools/wedding-cost/#c&"]').getAttribute("href");
      await page.goto(new URL(th, BASE + "chatuna/mechirim/hasaot/").href);
      await page.waitForTimeout(200);
      ok(await page.locator('[name="use_transport"]').isChecked(), "hasaot: preset link opens the calculator with transport on");
      ok(fs.existsSync(path.join(DOCS, "assets/og/wedding-prices.png")), "price guides: og image exists");
      ok(!page.errors.length, "price guides: no page errors " + page.errors.join("; "));
      await ctx.close();
    }

    /* ---------- older wedding pages link the hub + next step ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      for (const u of ["tools/wedding-gift/", "guides/wedding-checklist/", "p/wedding-planner/", "apps/seating/", "p/invitation-maker/"]) {
        await page.goto(BASE + u);
        ok(await page.locator(".wedding-next a").filter({ hasText: "הכל לחתונה" }).count() === 1 && await page.locator(".wedding-next li a").count() >= 2, u + ": next-step strip with hub link");
      }
      await ctx.close();
    }

    /* ---------- layout ---------- */
    for (const vp of [{ width: 375, height: 800 }, { width: 1280, height: 900 }]) {
      const ctx = await newCtx(browser, vp); const page = await newPage(ctx);
      for (const u of ["", "chatuna/", "tools/wedding-cost/", "tools/wedding-timeline/", "apps/rsvp/?demo=1", "chatuna/kama-lasim/zug/", "chatuna/haavarat-kesef/", "chatuna/mechirim/", "chatuna/mechirim/ulam/", "chatuna/mechirim/rav/"]) {
        await page.goto(BASE + u);
        await page.waitForTimeout(150);
        await noOverflow(page, (u || "home") + " @" + vp.width);
        if (vp.width === 375) await shot(page, "m-" + (u.replace(/[^a-z]+/g, "-") || "home"));
      }
      ok(!page.errors.length, "layout @" + vp.width + ": no page errors " + page.errors.join("; "));
      await ctx.close();
    }
  } catch (e) {
    console.error(e); failures++;
  } finally {
    await browser.close(); server.close();
  }
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
