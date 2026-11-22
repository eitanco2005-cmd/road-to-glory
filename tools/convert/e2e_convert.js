// End-to-end test of R6B conversion readiness (TEST mode, no real payment).
//   node tools/convert/e2e_convert.js [--shots DIR]
// Free samples download (xlsx formulas + RTL, PDF, PNG) from product pages and the hub -> "before you buy" blocks on the
// 5 wedding product pages (what you get, fit / not fit, refund link, secure payment, 3 steps, no reviews/countdowns) ->
// bundle page (compare table = JSON prices, one buy box, test purchase -> thanks next steps + all 3 apps unlocked) ->
// RSVP 80 limit + seating watermark export show the upgrade message with the bundle as best value (dialog swaps buy box)
// -> gift calculator "מתחתנים בעצמכם?" box -> PayPal order description (stubbed SDK) -> 375/1280 layout.
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
const PORT = 8783, BASE = `http://localhost:${PORT}/`;
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "tp-convert-e2e-"));
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };
const prod = s => JSON.parse(fs.readFileSync(path.join(DOCS, "data/products", s + ".json"), "utf8"));

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".pdf": "application/pdf",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});

async function newCtx(browser, vp, paypalStub) {
  const ctx = await browser.newContext({ viewport: vp || { width: 1280, height: 900 }, acceptDownloads: true, locale: "he-IL" });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com/, r => r.abort());
  await ctx.route(/paypal\.com/, r => paypalStub ? r.fulfill({ status: 200, contentType: "text/javascript", body: "" }) : r.abort());
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
async function shot(page, name, full) { if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await page.screenshot({ path: path.join(SHOTS, name + ".png"), fullPage: !!full }); } }
async function download(page, sel) {
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click(sel)]);
  const f = path.join(TMP, dl.suggestedFilename()); await dl.saveAs(f);
  return f;
}

const PAGES = [
  ["p/wedding-planner/", "wedding-planner", "budget"],
  ["p/seating-chart/", "seating-chart", "seating"],
  ["p/invitation-maker/", "invitation-maker", "invite"],
  ["p/rsvp-tracker/", "rsvp-tracker", null],
  ["p/wedding-bundle/", "wedding-bundle", "budget"],
];
const BANNED = /ביקורות|דירוג|★|נשארו רק|מוגבל בזמן!|הצעה מסתיימת|countdown|לקוחות מרוצים|נמכרו/;

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  try {
    /* ---------- sample files themselves ---------- */
    {
      const x = path.join(DOCS, "samples/mini-wedding-budget.xlsx");
      const info = JSON.parse(execFileSync("python3", ["-c", `
import json,sys,openpyxl
wb=openpyxl.load_workbook(sys.argv[1]);ws=wb.active
f=[c.value for r in ws.iter_rows() for c in r if isinstance(c.value,str) and c.value.startswith("=")]
links=[c.hyperlink.target for r in ws.iter_rows() for c in r if c.hyperlink]
print(json.dumps({"sheets":len(wb.sheetnames),"rtl":bool(ws.sheet_view.rightToLeft),"formulas":len(f),"links":links,"dv":len(ws.data_validations.dataValidation)}))`, x]).toString());
      ok(info.sheets === 1, "sample xlsx: exactly 1 sheet");
      ok(info.rtl, "sample xlsx: right-to-left sheet");
      ok(info.formulas >= 20, `sample xlsx: real formulas (${info.formulas})`);
      ok(info.links.some(l => /p\/wedding-planner\//.test(l)), "sample xlsx: links to the full planner");
      ok(info.dv >= 1, "sample xlsx: input validation");
      // recalculated values (LibreOffice): plan total = sum of rows, venue row = guests x plate
      try {
        execFileSync("soffice", ["--headless", "--convert-to", "csv", "--outdir", TMP, x], { stdio: "ignore" });
        const rows = fs.readFileSync(path.join(TMP, "mini-wedding-budget.csv"), "utf8").split("\n").map(l => l.split(","));
        const venue = rows.find(r => /אולם וקייטרינג/.test(r[1])), tot = rows.find(r => /^סה"*כ/.test((r[1] || "").replace(/"/g, "")));
        ok(venue && Number(venue[2]) === 250 * 380, "sample xlsx: venue = guests x plate after recalculation");
        ok(tot && Number(tot[2]) > Number(venue[2]), "sample xlsx: total recalculates (" + (tot && tot[2]) + ")");
      } catch (e) { console.log("SKIP xlsx recalculation (no LibreOffice)"); }
      const pdf = fs.readFileSync(path.join(DOCS, "samples/seating-chart-sample.pdf"));
      ok(pdf.slice(0, 5).toString() === "%PDF-" && pdf.length > 20000, "sample seating PDF is a real PDF");
      const png = fs.readFileSync(path.join(DOCS, "samples/invitation-sample.png"));
      ok(png.readUInt32BE(16) === 1200 && png.readUInt32BE(20) > 1500, "sample invitation PNG is 1200px wide portrait");
    }

    /* ---------- product pages: before-you-buy block + sample download ---------- */
    for (const [url, slug, sample] of PAGES) {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + url + "?test=1");
      const b = page.locator("#before-buy");
      ok(await b.count() === 1, `${slug}: before-you-buy block present`);
      const t = await b.innerText();
      ok(/מה מקבלים|מה כלול/.test(await page.locator("main").innerText()), `${slug}: what-you-get list`);
      ok(/למי (זה מתאים|החבילה מתאימה)/.test(await page.locator("main").innerText()), `${slug}: who it fits`);
      ok(/פחות/.test(await page.locator("main").innerText()), `${slug}: who it doesn't fit`);
      ok(await page.locator('#before-buy a[href$="legal/refund/"], main a[href$="legal/refund/"]').count() >= 1, `${slug}: refund link`);
      ok(/PayPal/.test(t) && /חשבון PayPal/.test(t), `${slug}: secure payment line (PayPal or card, no account)`);
      ok(/מיד/.test(t), `${slug}: instant delivery explained`);
      ok(await page.locator("main ol.steps.compact li").count() === 3, `${slug}: 3-step strip`);
      ok(!BANNED.test(await page.locator("main").innerText()), `${slug}: no reviews / scarcity / countdown wording`);
      await page.locator(`.buy[data-product="${slug}"] [data-test-pay]`).first().waitFor({ timeout: 8000 });
      ok(true, `${slug}: buy box renders (test mode)`);
      const ld = await page.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { JSON.parse(s.textContent); return true; } catch (e) { return false; } }));
      ok(ld.length && ld.every(Boolean), `${slug}: JSON-LD parses`);
      if (sample) {
        const f = await download(page, `[data-sample-dl="${sample}"] >> nth=0`);
        ok(fs.statSync(f).size > 5000, `${slug}: free sample downloads (${path.basename(f)}, ${fs.statSync(f).size} B)`);
      }
      const broken = await page.evaluate(() => Promise.all([...document.querySelectorAll("main img")].map(i => i.complete ? i.naturalWidth > 0 : new Promise(r => { i.onload = () => r(true); i.onerror = () => r(false); i.loading = "eager"; }))));
      ok(broken.every(Boolean), `${slug}: all images load (${broken.length})`);
      ok(page.errors.length === 0, `${slug}: no JS errors ${page.errors.join(" | ")}`);
      await shot(page, "page-" + slug, true);
      await ctx.close();
    }

    /* ---------- bundle page: compare table + single buy box + test purchase ---------- */
    {
      const b = prod("wedding-bundle"), total = b.bundle_of.reduce((a, s) => a + prod(s).price_ils, 0);
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "p/wedding-bundle/?test=1");
      const foot = await page.locator(".cmp-table tfoot").innerText();
      ok(foot.includes("₪" + total) && foot.includes("₪" + b.price_ils), `bundle: compare table total ₪${total} vs ₪${b.price_ils}`);
      ok(await page.locator(".cmp-table tbody tr").count() === b.bundle_of.length, "bundle: one row per included product");
      ok(await page.locator(".buy[data-product]").count() === 1, "bundle: single buy box");
      await page.locator("[data-test-pay]").click();
      await page.waitForURL(/thanks\/\?p=wedding-bundle/, { timeout: 10000 });
      await page.locator("#next-steps li").first().waitFor({ timeout: 8000 });
      const ns = await page.locator("#next-steps").innerText();
      ok(/מה עכשיו/.test(ns) && /apps\/rsvp/.test(await page.locator("#next-steps").innerHTML()), "thanks: next steps for the bundle");
      ok(/צריכים עזרה/.test(await page.locator("#ok").innerText()), "thanks: how to get help");
      ok(await page.locator("#downloads .dl").count() >= 3, "thanks: planner files listed for the bundle");
      const un = await page.evaluate(() => ["seating-chart", "rsvp-tracker", "invitation-maker"].map(s => !!localStorage.getItem("tp-unlock:" + s)));
      ok(un.every(Boolean), "thanks: bundle unlocks all three apps in this browser");
      await shot(page, "thanks-bundle", true);
      await ctx.close();
    }

    /* ---------- RSVP: 80 limit -> upgrade message with bundle best value ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "apps/rsvp/?test=1");
      await page.evaluate(() => { const rows = []; for (let i = 1; i <= 85; i++) rows.push("אורח " + i); document.querySelector('[data-act="paste"]').click(); document.querySelector("dialog .pv-text").value = rows.join("\n"); document.querySelector("dialog [data-ok]").click(); });
      await page.click('dialog [data-pv="all"]'); await page.click('dialog [data-pv="add"]');
      const dlg = page.locator("dialog.unlock-dialog");
      await dlg.waitFor();
      ok(await page.locator("#limit [data-bundle-link]").isVisible(), "rsvp limit: banner offers the bundle");
      ok(await dlg.locator(".up-opt.best").count() === 1 && /הכי משתלם/.test(await dlg.locator(".up-opt.best").innerText()), "rsvp limit: dialog shows bundle as best value");
      await page.waitForFunction(() => /₪79/.test(document.querySelector("[data-price-of=wedding-bundle]").textContent));
      ok(/₪126/.test(await dlg.locator(".up-opt.best").innerText()), "rsvp limit: bundle shows price vs separate total");
      ok(await dlg.locator('.up-opts input[value="rsvp-tracker"]').isChecked(), "rsvp limit: single product pre-selected (no pressure)");
      await shot(page, "rsvp-limit-dialog");
      await dlg.locator('.up-opts input[value="wedding-bundle"]').check();
      await dlg.locator('.buy[data-product="wedding-bundle"] [data-test-pay]').waitFor({ timeout: 8000 });
      ok(true, "rsvp limit: choosing the bundle swaps the buy box");
      ok(await dlg.locator(".up-bundle-note").isVisible(), "rsvp limit: explains what happens after a bundle purchase");
      await dlg.locator('.up-opts input[value="rsvp-tracker"]').check();
      await dlg.locator('.buy[data-product="rsvp-tracker"] [data-test-pay]').waitFor({ timeout: 8000 });
      ok(true, "rsvp limit: switching back restores the single product");
      ok(page.errors.length === 0, "rsvp: no JS errors " + page.errors.join(" | "));
      await ctx.close();
    }

    /* ---------- seating: free watermarked export -> upgrade note ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "apps/seating/?demo=1&test=1");
      await page.evaluate(() => document.querySelector('[data-act="print"]').click());
      await page.locator(".upgrade-note[data-nudge]").waitFor({ timeout: 5000 });
      ok(await page.evaluate(() => window.__printed) >= 1, "seating: free export still prints (watermarked)");
      const n = page.locator(".upgrade-note[data-nudge]");
      ok(/סימן מים/.test(await n.innerText()), "seating: upgrade message explains the watermark");
      ok(await n.locator('a[href$="p/wedding-bundle/"]').count() === 1, "seating: upgrade message offers the bundle");
      await shot(page, "seating-nudge");
      await n.locator("[data-nudge-open]").click();
      const dlg = page.locator("dialog.unlock-dialog");
      await dlg.waitFor();
      ok(await dlg.locator(".up-opt.best").count() === 1, "seating: dialog offers bundle as best value");
      await dlg.locator(".dlg-x").click();
      await n.locator("[data-nudge-x]").click();
      ok(await page.locator(".upgrade-note[data-nudge]").count() === 0, "seating: upgrade message can be dismissed");
      ok(page.errors.length === 0, "seating: no JS errors " + page.errors.join(" | "));
      await ctx.close();
      // English seating app: no Hebrew bundle offer
      const c2 = await newCtx(browser); const p2 = await newPage(c2);
      await p2.goto(BASE + "en/apps/seating/?demo=1&test=1");
      await p2.evaluate(() => document.querySelector('[data-act="print"]').click());
      await p2.locator(".upgrade-note[data-nudge]").waitFor({ timeout: 5000 });
      ok(await p2.locator(".upgrade-note a[href*=wedding-bundle]").count() === 0, "seating (en): no Hebrew bundle in the upgrade note");
      ok(p2.errors.length === 0, "seating (en): no JS errors " + p2.errors.join(" | "));
      await c2.close();
    }

    /* ---------- gift calculator funnel + hub samples ---------- */
    {
      const ctx = await newCtx(browser); const page = await newPage(ctx);
      await page.goto(BASE + "tools/wedding-gift/");
      const fb = page.locator(".funnel-box");
      ok(await fb.count() === 1 && /מתחתנים בעצמכם/.test(await fb.innerText()), "gift calculator: 'מתחתנים בעצמכם?' box");
      ok(await fb.locator('a[href$="chatuna/#mitchatnim"]').count() === 1, "gift calculator: box links to the couple path");
      const order = await page.evaluate(() => { const r = document.querySelector(".result"), f = document.querySelector(".funnel-box"); return !!(r.compareDocumentPosition(f) & Node.DOCUMENT_POSITION_FOLLOWING); });
      ok(order, "gift calculator: box comes after the result");
      await page.goto(BASE + "chatuna/");
      ok(await page.locator("#dugmaot [data-sample-dl]").count() === 3, "hub: 3 free samples");
      const f = await download(page, '#dugmaot [data-sample-dl="seating"]');
      ok(fs.readFileSync(f).slice(0, 5).toString() === "%PDF-", "hub: seating sample downloads");
      ok(await page.locator('#dugmaot a[href$="p/wedding-bundle/"]').count() === 1, "hub: link to bundle comparison");
      ok(page.errors.length === 0, "hub/gift: no JS errors " + page.errors.join(" | "));
      await ctx.close();
    }

    /* ---------- PayPal order description (stubbed SDK, live mode) ---------- */
    {
      const ctx = await newCtx(browser, null, true); const page = await newPage(ctx);
      await page.addInitScript(() => {
        window.paypal = { Buttons: o => ({ render: () => { window.__order = o.createOrder({}, { order: { create: x => x } }); return Promise.resolve(); } }) };
      });
      await page.goto(BASE + "p/wedding-bundle/");
      await page.waitForFunction(() => window.__order, null, { timeout: 8000 });
      const o = await page.evaluate(() => window.__order);
      const pu = o.purchase_units[0];
      ok(pu.items[0].name === prod("wedding-bundle").title, "paypal: item name = Hebrew product title");
      ok(/מוצר דיגיטלי/.test(pu.description) && pu.description.length <= 127, "paypal: description says digital product + brand (" + pu.description + ")");
      ok(pu.amount.value === "79.00" && pu.amount.currency_code === "ILS", "paypal: ₪79.00 ILS");
      await ctx.close();
    }

    /* ---------- layout 375 / 1280 ---------- */
    for (const vp of [{ width: 375, height: 800 }, { width: 1280, height: 900 }]) {
      const ctx = await newCtx(browser, vp); const page = await newPage(ctx);
      for (const u of ["p/wedding-bundle/", "p/rsvp-tracker/", "p/wedding-planner/", "p/seating-chart/", "p/invitation-maker/", "chatuna/", "tools/wedding-gift/"]) {
        await page.goto(BASE + u + "?test=1");
        await page.waitForTimeout(150);
        await noOverflow(page, `${u} @${vp.width}`);
      }
      await ctx.close();
    }
  } catch (e) {
    console.error(e); failures++;
  } finally {
    await browser.close(); server.close();
    fs.rmSync(TMP, { recursive: true, force: true });
  }
  console.log(failures ? `\n${failures} FAILURE(S)` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
