// End-to-end check of the platform in TEST mode (no real payment).
//   node tools/site/e2e_test.js [--shots ops/reports/w1]
// Copies docs/ to a temp dir, adds a fixture product (files + page), points config.js at a local
// sales endpoint (tools/site/sales_endpoint, needs fastapi+uvicorn), serves under /road-to-glory/,
// then: home renders -> product ?test=1 -> pay -> thanks page -> download -> summary shows sale + visits.
// Also checks the live PayPal SDK renders buttons when not in test mode (skipped if paypal.com unreachable).
const { chromium } = require("playwright");
const { spawn, execSync } = require("child_process");
const fs = require("fs");
const os = require("os");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(REPO, args[args.indexOf("--shots") + 1]) : null;
const WEB = 8765, API = 8766, TOKEN = "e2e-token";
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

function waitFor(url, ms = 15000) {
  const t0 = Date.now();
  return new Promise((res, rej) => {
    (function poll() {
      http.get(url, r => { r.resume(); res(); }).on("error", () => Date.now() - t0 > ms ? rej(new Error("timeout " + url)) : setTimeout(poll, 200));
    })();
  });
}

(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "glory-e2e-"));
  const site = path.join(tmp, "road-to-glory");
  execSync(`cp -r "${REPO}/docs" "${site}"`);
  // fixture: make wedding-planner + bar-mitzvah deliverable, give wedding-planner a page and a file
  const dl = path.join(site, "dl", "e2eFixture000001");
  fs.mkdirSync(dl, { recursive: true });
  fs.writeFileSync(path.join(dl, "wedding-planner.xlsx"), "fixture");
  for (const slug of ["wedding-planner", "bar-mitzvah-planner"]) {
    const f = path.join(site, "data/products", slug + ".json");
    const p = JSON.parse(fs.readFileSync(f));
    delete p.placeholder;
    p.files = [{ label: "מתכנן החתונה (Excel)", path: "dl/e2eFixture000001/wedding-planner.xlsx" }];
    p.sheets_copy_url = "https://docs.google.com/spreadsheets/d/EXAMPLE/copy";
    fs.writeFileSync(f, JSON.stringify(p));
  }
  fs.mkdirSync(path.join(site, "p/wedding-planner"), { recursive: true });
  fs.writeFileSync(path.join(site, "p/wedding-planner/index.html"), `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>fixture</title><link rel="stylesheet" href="../../assets/site.css"></head>
<body><header id="site-header"></header><main><div class="container section"><h1>מתכנן חתונה</h1>
<div class="buy" data-product="wedding-planner"></div></div></main><footer id="site-footer"></footer>
<script src="../../assets/site.js"></script><script src="../../assets/checkout.js"></script></body></html>`);
  const cfgPath = path.join(site, "assets/config.js");
  fs.writeFileSync(cfgPath, fs.readFileSync(cfgPath, "utf8")
    .replace('SALES_ENDPOINT: ""', `SALES_ENDPOINT: "http://127.0.0.1:${API}/sale"`)
    .replace('VISITS_ENDPOINT: ""', `VISITS_ENDPOINT: "http://127.0.0.1:${API}/visit"`)
    .replace('SELLER_EMAIL: "SELLER_EMAIL"', 'SELLER_EMAIL: "help@example.com"'));

  const web = spawn("python3", ["-m", "http.server", String(WEB), "--bind", "127.0.0.1"], { cwd: tmp, stdio: "ignore" });
  const api = spawn("python3", ["-m", "uvicorn", "app:app", "--port", String(API), "--host", "127.0.0.1"], {
    cwd: path.join(REPO, "tools/site/sales_endpoint"), stdio: "ignore",
    env: { ...process.env, DATA_DIR: path.join(tmp, "data"), SUMMARY_TOKEN: TOKEN, HF_TOKEN: "", PAYPAL_SECRET: "" },
  });
  const BASE = `http://127.0.0.1:${WEB}/road-to-glory/`;
  const browser = await chromium.launch();
  try {
    await waitFor(BASE); await waitFor(`http://127.0.0.1:${API}/health`);
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    const errors = [];
    page.on("pageerror", e => errors.push(e.message));

    // 1. home
    await page.goto(BASE, { waitUntil: "networkidle" });
    ok(await page.locator("#site-header .brand").count() === 1, "header injected");
    ok(await page.locator("#site-footer a[href$='legal/refund/']").count() === 1, "footer with legal links");
    ok(await page.locator('[data-catalog="products"][data-rendered="1"] .product-card').count() === 6, "home grid has 6 products");
    ok(await page.locator('.product-card[data-slug="wedding-planner"] h3 a').count() === 1, "live product links to its page");
    ok(await page.locator('.product-card[data-slug="household-budget"].is-soon').count() === 1, "placeholder product shows 'soon'");
    ok(await page.locator('[data-catalog="tools"] .tool-card').count() === 6, "home lists 6 tools");
    if (SHOTS) {
      fs.mkdirSync(SHOTS, { recursive: true });
      await page.screenshot({ path: path.join(SHOTS, "home-1280.png"), fullPage: true });
      const m = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 });
      const mp = await m.newPage();
      await mp.goto(BASE, { waitUntil: "networkidle" });
      const overflow = await mp.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      ok(!overflow, "no horizontal scroll at 375px");
      await mp.screenshot({ path: path.join(SHOTS, "home-375.png"), fullPage: true });
      await mp.emulateMedia({ colorScheme: "dark" });
      await mp.goto(BASE + "products/", { waitUntil: "networkidle" });
      await mp.screenshot({ path: path.join(SHOTS, "products-375-dark.png"), fullPage: true });
      await m.close();
    }

    // 2. product page, TEST mode purchase
    await page.goto(BASE + "p/wedding-planner/?test=1", { waitUntil: "networkidle" });
    const btn = page.locator('[data-test-pay="wedding-planner"]');
    ok(await btn.count() === 1, "test pay button rendered");
    ok((await page.locator(".buy-price").innerText()).includes("49"), "price from JSON (₪49)");
    if (SHOTS) await page.locator(".buy").screenshot({ path: path.join(SHOTS, "buybox-test.png") });
    await Promise.all([page.waitForURL(/thanks\/\?p=wedding-planner&o=TEST-/), btn.click()]);
    await page.waitForSelector("#ok:not([hidden])");
    ok(true, "redirected to thanks page");
    const dlLink = page.locator("a.dl").first();
    ok(await page.locator("a.dl").count() === 2, "thanks shows file + Sheets copy link");
    const href = await dlLink.getAttribute("href");
    const res = await page.request.get(href);
    ok(res.ok() && (await res.text()) === "fixture", "download link serves the file");
    ok((await page.locator("#r-order").innerText()).startsWith("TEST-"), "receipt shows order id");
    ok(await page.locator("#test-flag:not([hidden])").count() === 1, "test flag visible");
    ok((await page.locator("#support").innerText()).includes("help@example.com"), "support email from config");
    if (SHOTS) await page.screenshot({ path: path.join(SHOTS, "thanks-1280.png"), fullPage: true });

    // 3. bundle via catalogue (TEST): event bundle deliverable (both members fixture'd)
    await page.goto(BASE + "products/?test=1", { waitUntil: "networkidle" });
    ok(await page.locator('.buy[data-product="event-bundle"] [data-test-pay]').count() === 1, "bundle test button");
    await Promise.all([page.waitForURL(/thanks\/\?p=event-bundle/), page.locator('[data-test-pay="event-bundle"]').click()]);
    await page.waitForSelector("#ok:not([hidden])");
    ok(await page.locator("#downloads h3").count() === 2, "bundle thanks lists both member products");

    // 4. non-test: placeholder bundle shows 'soon'; deliverable bundle loads real PayPal buttons
    await page.goto(BASE + "products/", { waitUntil: "domcontentloaded" });
    await page.waitForSelector('.buy[data-product="money-bundle"] .buy-box');
    ok(await page.locator('.buy[data-product="money-bundle"] button[disabled]').count() === 1, "non-deliverable bundle disabled ('soon')");
    try {
      await page.waitForSelector('.buy[data-product="event-bundle"] iframe, .buy[data-product="event-bundle"] .buy-msg.error', { timeout: 20000 });
      const iframes = await page.locator('.buy[data-product="event-bundle"] iframe').count();
      if (iframes) ok(true, "live PayPal buttons rendered (" + iframes + " iframe)");
      else console.log("SKIP live PayPal: " + await page.locator('.buy[data-product="event-bundle"] .buy-msg').innerText());
    } catch (e) { console.log("SKIP live PayPal: timeout"); }
    if (SHOTS) await page.locator("#bundles").screenshot({ path: path.join(SHOTS, "bundles-live.png") });

    // 5. tools, legal, 404
    for (const p of ["tools/", "legal/terms/", "legal/refund/", "legal/privacy/", "legal/accessibility/"]) {
      const r = await page.goto(BASE + p, { waitUntil: "networkidle" });
      ok(r.ok() && await page.locator("#site-header .brand").count() === 1, "page ok: " + p);
    }

    // 6. sales log summary
    await new Promise(r => setTimeout(r, 500));
    const sum = await (await page.request.get(`http://127.0.0.1:${API}/summary`, { headers: { Authorization: "Bearer " + TOKEN } })).json();
    ok(sum.money.test_sales === 2, "endpoint recorded 2 test sales (got " + sum.money.test_sales + ")");
    ok(sum.traffic.visits >= 5, "endpoint recorded visits (" + sum.traffic.visits + ")");
    ok(errors.length === 0, "no page JS errors" + (errors.length ? ": " + errors.join(" | ") : ""));
  } catch (e) {
    console.error(e); failures++;
  } finally {
    await browser.close(); web.kill(); api.kill();
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
