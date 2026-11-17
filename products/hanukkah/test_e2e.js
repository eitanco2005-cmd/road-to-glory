// Hanukkah stream end-to-end checks (TEST mode, no real payment).
//   node products/hanukkah/test_e2e.js [--shots <dir>]
// Serves docs/ at the domain root, then for every Hanukkah page at 375px and 1280px: loads without JS errors,
// no horizontal scroll, one <h1>, canonical + JSON-LD present. Then: buy boxes show the right currency/price,
// TEST purchases (he product, he bundle, en product, en bundle) land on the right thanks page with working downloads,
// both calculators compute, live PayPal SDK loads with the product currency (skipped when paypal.com is unreachable).
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(REPO, args[args.indexOf("--shots") + 1]) : null;
const PORT = 8771;
const BASE = `http://127.0.0.1:${PORT}/`;
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

const PAGES = [
  "hanukkah/", "p/hanukkah-activity-pack/", "p/hanukkah-party-planner/", "tools/sufganiyot-calculator/",
  "hanukkah/hanukkah-2026-dates/", "hanukkah/kids-activities/", "hanukkah/hanukkah-party/",
  "en/hanukkah/", "en/hanukkah/activity-pack/", "en/hanukkah/party-planner/", "en/hanukkah/latke-calculator/",
  "en/hanukkah/when-is-hanukkah-2026/", "en/hanukkah/how-to-play-dreidel/", "en/hanukkah/terms/",
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
    // 1. every page, both widths
    for (const [w, h] of [[375, 812], [1280, 900]]) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h } });
      const page = await ctx.newPage();
      for (const p of PAGES) {
        const errs = [];
        page.removeAllListeners("pageerror");
        page.on("pageerror", e => errs.push(e.message));
        const r = await page.goto(BASE + p, { waitUntil: "networkidle" });
        const info = await page.evaluate(() => ({
          over: document.documentElement.scrollWidth > window.innerWidth + 1,
          h1: document.querySelectorAll("h1").length,
          canon: !!document.querySelector('link[rel="canonical"]'),
          ld: document.querySelectorAll('script[type="application/ld+json"]').length,
          brokenImg: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute("src")),
          lang: document.documentElement.lang, dir: document.documentElement.dir,
        }));
        const want = p.startsWith("en/") ? ["en", "ltr"] : ["he", "rtl"];
        ok(r.ok() && !info.over && info.h1 === 1 && info.canon && info.ld >= 1 && !info.brokenImg.length && info.lang === want[0] && info.dir === want[1] && !errs.length,
          `${w}px ${p}` + (info.over ? " [horizontal scroll]" : "") + (info.h1 !== 1 ? ` [h1=${info.h1}]` : "") +
          (info.brokenImg.length ? ` [broken img ${info.brokenImg}]` : "") + (errs.length ? ` [js: ${errs.join("|")}]` : ""));
        if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `${w}-${p.replace(/\//g, "_") || "root"}.png`), fullPage: w === 375 ? false : true });
      }
      await ctx.close();
    }

    // 2. TEST purchases
    await buyFlow(browser, "p/hanukkah-activity-pack/", "hanukkah-activity-pack", /\/thanks\/\?p=hanukkah-activity-pack&o=TEST-/, "₪19", 1);
    await buyFlow(browser, "p/hanukkah-party-planner/", "hanukkah-party-planner", /\/thanks\/\?p=hanukkah-party-planner&o=TEST-/, "₪19", 2);
    await buyFlow(browser, "hanukkah/", "hanukkah-bundle", /\/thanks\/\?p=hanukkah-bundle&o=TEST-/, "₪29", 3);
    await buyFlow(browser, "en/hanukkah/activity-pack/", "hanukkah-activity-pack-en", /\/en\/hanukkah\/thanks\/\?p=hanukkah-activity-pack-en&o=TEST-/, "$12", 2);
    await buyFlow(browser, "en/hanukkah/party-planner/", "hanukkah-party-planner-en", /\/en\/hanukkah\/thanks\/\?p=hanukkah-party-planner-en&o=TEST-/, "$12", 2);
    await buyFlow(browser, "en/hanukkah/", "hanukkah-bundle-en", /\/en\/hanukkah\/thanks\/\?p=hanukkah-bundle-en&o=TEST-/, "$19", 4);

    // 3. calculators: 10 adults + 4 kids, normal appetite, buy
    for (const [p, pot] of [["tools/sufganiyot-calculator/", "2.4"], ["en/hanukkah/latke-calculator/", "5.4"]]) {
      const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
      const page = await ctx.newPage();
      await page.goto(BASE + p, { waitUntil: "networkidle" });
      await page.fill("#adults", "10");
      await page.fill("#kids", "4");
      await page.waitForTimeout(100);
      const v = await page.evaluate(() => ["v-suf", "v-lat", "v-pot"].map(id => document.getElementById(id).textContent));
      ok(v[0] === "19" && v[1] === "48" && v[2] === pot, `${p}: 10 adults + 4 kids -> 19 doughnuts, 48 latkes, ${pot} potatoes (got ${v})`);
      await page.check('input[name="mode"][value="make"]');
      const rows = await page.locator("#list tr").count();
      ok(rows >= 14, `${p}: homemade mode adds dough ingredients (${rows} rows)`);
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `calc-375-${p.split("/")[0]}.png`), fullPage: true });
      await ctx.close();
    }

    // 4. live PayPal SDK currency per page
    for (const [p, cur] of [["p/hanukkah-activity-pack/", "ILS"], ["en/hanukkah/activity-pack/", "USD"]]) {
      const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
      const page = await ctx.newPage();
      try {
        await page.goto(BASE + p, { waitUntil: "domcontentloaded" });
        await page.waitForSelector(".buy iframe", { timeout: 20000 });
        const src = await page.evaluate(() => [...document.scripts].map(s => s.src).find(s => s.includes("paypal.com/sdk/js")));
        ok(new RegExp("currency=" + cur).test(src), `${p}: live PayPal SDK loaded with currency=${cur}`);
      } catch (e) { console.log(`SKIP live PayPal on ${p}: ${e.message.split("\n")[0]}`); }
      await ctx.close();
    }
  } catch (e) {
    console.error(e); failures++;
  } finally {
    await browser.close(); web.kill();
  }
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
