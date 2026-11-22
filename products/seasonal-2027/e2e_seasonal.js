// Seasonal 2027 stream (budget 2027, Purim, Pesach) end-to-end checks (TEST mode, no real payment).
//   node products/seasonal-2027/e2e_seasonal.js [--shots <dir>]
// Every new page at 375px and 1280px: loads without JS errors, no horizontal scroll, one <h1>, canonical + JSON-LD, no broken images.
// TEST purchases (purim-planner, seder-planner, spring bundle) reach the thanks page with real .xlsx downloads.
// Calculators compute known values; free PDFs download; hreflang links to the English Passover pages exist.
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(REPO, args[args.indexOf("--shots") + 1]) : null;
const PORT = 8773;
const BASE = `http://127.0.0.1:${PORT}/`;
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

const PAGES = [
  "budget-2027/", "budget-2027/what-changes-2027/", "budget-2027/savings-challenge/",
  "purim/", "p/purim-planner/", "tools/mishloach-manot-budget/", "purim/mishloach-manot-ideas/", "purim/purim-halacha/", "purim/class-mishloach-manot/",
  "pesach/", "pesach/cleaning-checklist/", "p/seder-planner/", "tools/matza-wine-calculator/", "pesach/seder-night-guide/", "pesach/pesach-2027-dates/", "pesach/pesach-budget/",
];


function waitFor(url, ms = 15000) {
  const t0 = Date.now();
  return new Promise((res, rej) => {
    (function poll() {
      http.get(url, r => { r.resume(); res(); }).on("error", () => Date.now() - t0 > ms ? rej(new Error("timeout")) : setTimeout(poll, 200));
    })();
  });
}

async function buyFlow(browser, pagePath, slug, thanksRe, expectPrice, expectFiles) {
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(e.message));
  await page.goto(BASE + pagePath + "?test=1", { waitUntil: "networkidle" });
  const btn = page.locator(`[data-test-pay="${slug}"]`).first();
  ok(await btn.count() === 1, `${slug}: test pay button`);
  const price = await page.locator(`.buy[data-product="${slug}"] .buy-price`).first().innerText();
  ok(price.trim() === expectPrice, `${slug}: price shows ${expectPrice} (got ${price.trim()})`);
  await Promise.all([page.waitForURL(thanksRe), btn.click()]);
  await page.waitForSelector("#ok:not([hidden])", { timeout: 10000 });
  const links = page.locator("a.dl");
  ok(await links.count() === expectFiles, `${slug}: thanks page lists ${expectFiles} files (got ${await links.count()})`);
  for (let i = 0; i < await links.count(); i++) {
    const href = await links.nth(i).getAttribute("href");
    const r = await page.request.get(href);
    const body = await r.body();
    const magic = body.slice(0, 4).toString("latin1");
    ok(r.ok() && (magic === "%PDF" || magic === "PK\u0003\u0004"), `${slug}: download ${path.basename(href)} (${magic.replace(/[^\x20-\x7e]/g, "")})`);
  }
  const recPrice = await page.locator("#r-price").innerText();
  ok(recPrice.includes(expectPrice.replace(/[^\d]/g, "")), `${slug}: receipt amount ${recPrice}`);
  ok(errs.length === 0, `${slug}: no JS errors ${errs.join(" | ")}`);
  if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `thanks-${slug}.png`), fullPage: true });
  await ctx.close();
}


(async () => {
  const web = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"], { cwd: path.join(REPO, "docs"), stdio: "ignore" });
  const browser = await chromium.launch();
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  try {
    await waitFor(BASE);
    for (const [w, h] of [[375, 812], [1280, 900]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h } });
      await ctx.route(/paypal\.com|fonts\.(googleapis|gstatic)\.com/, r => r.abort());
      const page = await ctx.newPage();
      for (const p of PAGES) {
        const errs = [];
        page.removeAllListeners("pageerror");
        page.on("pageerror", e => errs.push(e.message));
        const r = await page.goto(BASE + p, { waitUntil: "load" });
        await page.waitForTimeout(150);
        const info = await page.evaluate(() => ({
          over: document.documentElement.scrollWidth > window.innerWidth + 1,
          h1: document.querySelectorAll("h1").length,
          canon: !!document.querySelector('link[rel="canonical"]'),
          ld: [...document.querySelectorAll('script[type="application/ld+json"]')].every(s => { try { JSON.parse(s.textContent); return true; } catch (e) { return false; } }) ? document.querySelectorAll('script[type="application/ld+json"]').length : -1,
          brokenImg: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute("src")),
          raw: /\{up\}|\{CRUMBS\}/.test(document.documentElement.innerHTML),
          lang: document.documentElement.lang, dir: document.documentElement.dir,
        }));
        ok(r.ok() && !info.over && info.h1 === 1 && info.canon && info.ld >= 1 && !info.brokenImg.length && !info.raw && info.lang === "he" && info.dir === "rtl" && !errs.length,
          `${w}px ${p}` + (info.over ? " [horizontal scroll]" : "") + (info.h1 !== 1 ? ` [h1=${info.h1}]` : "") + (info.ld < 1 ? " [json-ld]" : "") +
          (info.raw ? " [unfilled placeholder]" : "") + (info.brokenImg.length ? ` [broken img ${info.brokenImg}]` : "") + (errs.length ? ` [js: ${errs.join("|")}]` : ""));
        if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${w}-${p.replace(/\//g, "_")}.png`), fullPage: true });
      }
      await ctx.close();
    }

    // TEST purchases
    await buyFlow(browser, "p/purim-planner/", "purim-planner", /\/thanks\/\?p=purim-planner&o=TEST-/, "₪19", 2);
    await buyFlow(browser, "p/seder-planner/", "seder-planner", /\/thanks\/\?p=seder-planner&o=TEST-/, "₪19", 2);
    await buyFlow(browser, "pesach/", "spring-holidays-bundle", /\/thanks\/\?p=spring-holidays-bundle&o=TEST-/, "₪29", 4);

    // calculators
    {
      const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
      const page = await ctx.newPage();
      await page.goto(BASE + "tools/mishloach-manot-budget/", { waitUntil: "load" });
      let v = await page.evaluate(() => ["r-total", "r-pk", "r-avg", "r-all"].map(id => document.getElementById(id).textContent));
      ok(v.join("|") === "₪395|15|₪26|₪495", `mishloach-manot: defaults -> ₪395, 15 packages, ₪26 avg, ₪495 with matanot (got ${v})`);
      await page.fill("#budget", "450");
      const msg = await page.locator("#r-bud").textContent();
      ok(/חריגה של ₪45/.test(msg), `mishloach-manot: budget 450 -> over by ₪45 (${msg})`);
      await page.fill("#n-cls", "30");
      v = await page.evaluate(() => document.getElementById("r-pk").textContent);
      ok(v === "45", `mishloach-manot: +30 class kids -> 45 packages (got ${v})`);
      const share = await page.locator("[data-share]").count();
      ok(share === 1, "mishloach-manot: WhatsApp share bar present");
      await page.goto(BASE + "tools/matza-wine-calculator/", { waitUntil: "load" });
      v = await page.evaluate(() => ["k-hand", "k-wine", "k-juice", "k-box"].map(id => document.getElementById(id).textContent));
      ok(v.join("|") === "20|4|3|7", `matza-wine: 10 adults + 4 kids (86 ml) -> 20 hand matzot, 4 bottles, 3 L juice, 7 boxes (got ${v})`);
      await page.fill("#adults", "12"); await page.fill("#kids", "6"); await page.check('input[name="reviit"][value="150"]');
      v = await page.evaluate(() => ["k-hand", "k-wine", "k-juice"].map(id => document.getElementById(id).textContent));
      ok(v.join("|") === "25|8|6.5", `matza-wine: 12 adults + 6 kids (150 ml) -> 25 / 8 / 6.5 (got ${v})`);
      ok(await page.locator("[data-share]").count() === 1, "matza-wine: WhatsApp share bar present");
      await ctx.close();
    }

    // free PDFs, hreflang, sitemap
    for (const f of ["pesach/files/pesach-cleaning-checklist-2027.pdf", "budget-2027/files/savings-challenge-2027.pdf"]) {
      const body = fs.readFileSync(path.join(REPO, "docs", f));
      ok(body.slice(0, 4).toString("latin1") === "%PDF" && body.length > 20000, `free printable ${f} (${body.length} bytes)`);
    }
    const sm = fs.readFileSync(path.join(REPO, "docs/sitemap.xml"), "utf8");
    // R6A audit: thin seasonal articles/hubs are noindexed (docs/data/seo.json); the rest must stay in the sitemap
    const NOINDEX = JSON.parse(fs.readFileSync(path.join(REPO, "docs/data/seo.json"), "utf8")).noindex;
    const inSm = p => sm.includes(`<loc>https://tichnun.netlify.app/${p}</loc>`);
    ok(PAGES.every(p => NOINDEX.includes(p) ? !inSm(p) : inSm(p)), `sitemap lists the ${PAGES.filter(p => !NOINDEX.includes(p)).length} indexable seasonal pages and none of the noindexed ones`);
    ok(/hreflang="he" href="[^"]+\/p\/seder-planner\/"/.test(sm) && sm.includes("en/p/passover-seder-planner/"), "sitemap pairs seder planner he<->en");
    const seder = fs.readFileSync(path.join(REPO, "docs/p/seder-planner/index.html"), "utf8");
    ok(/hreflang="en" href="[^"]+en\/p\/passover-seder-planner\/"/.test(seder), "seder planner page has hreflang=en to the English planner");
  } catch (e) {
    console.error(e); failures++;
  } finally {
    await browser.close(); web.kill();
  }
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
