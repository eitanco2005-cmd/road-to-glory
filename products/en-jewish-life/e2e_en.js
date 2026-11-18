// E2E for the English section (Stream A). Serves docs/ at the domain root and checks, in TEST mode (no payment):
//  - every docs/en/**/index.html at 375px and 1280px: lang/dir, English header + language switch + footer,
//    no horizontal overflow, no JS errors, single <h1>, meta description, canonical
//  - USD buy boxes; test purchase of a planner and of the bundle -> en/thanks/ with working downloads
//  - the 3 calculators produce sane numbers
//  - Hebrew regression: Hebrew product page still ILS + Hebrew, header shows the English switch
//  - live PayPal SDK renders in USD on an English page (skipped if paypal.com is unreachable)
//   node products/en-jewish-life/e2e_en.js [--shots <dir>]
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const args = process.argv.slice(2);
const SHOTS = args.includes("--shots") ? path.resolve(REPO, args[args.indexOf("--shots") + 1]) : null;
const PORT = 8791, BASE = `http://127.0.0.1:${PORT}/`;
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

function enPages(dir = path.join(DOCS, "en"), out = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    if (fs.statSync(p).isDirectory()) { if (!/en[\\/]embed[\\/][^\\/]+$/.test(path.relative(DOCS, p))) enPages(p, out); } // iframe widgets (no site chrome) are tested by tools/site/e2e_embed.js
    else if (f === "index.html") out.push(path.relative(DOCS, path.dirname(p)).replace(/\\/g, "/") + "/");
  }
  return out.sort();
}
function head(url) {
  return new Promise(res => http.get(url, r => { r.resume(); res(r.statusCode); }).on("error", () => res(0)));
}
async function waitUp() { for (let i = 0; i < 50; i++) { if (await head(BASE)) return; await new Promise(r => setTimeout(r, 200)); } }

(async () => {
  const web = spawn("python3", ["-m", "http.server", String(PORT), "--bind", "127.0.0.1"], { cwd: DOCS, stdio: "ignore" });
  await waitUp();
  const browser = await chromium.launch();
  try {
    const pages = enPages();
    ok(pages.length >= 20, `found ${pages.length} English pages`);
    for (const width of [375, 1280]) {
      const ctx = await browser.newContext({ viewport: { width, height: 900 } });
      for (const p of pages) {
        const page = await ctx.newPage();
        const errors = [];
        page.on("pageerror", e => errors.push(e.message));
        page.on("console", m => { if (m.type() === "error" && !/fonts\.g|paypal|ERR_NAME|ERR_INTERNET|net::/.test(m.text())) errors.push(m.text()); });
        const q = p.startsWith("en/thanks/") ? "?p=passover-seder-planner&o=TEST-X&test=1" : "?test=1";
        await page.goto(BASE + p + q, { waitUntil: "networkidle" }).catch(() => {});
        await page.waitForTimeout(150);
        const r = await page.evaluate(() => ({
          lang: document.documentElement.lang, dir: document.documentElement.dir,
          over: document.documentElement.scrollWidth - window.innerWidth,
          h1: document.querySelectorAll("h1:not([hidden] h1)").length,
          desc: (document.querySelector('meta[name="description"]') || {}).content || "",
          canon: !!document.querySelector('link[rel="canonical"]'),
          sw: (document.querySelector(".lang-switch") || {}).textContent || "",
          nav: (document.querySelector(".site-header .nav") || {}).textContent || "",
          foot: (document.querySelector(".site-footer") || {}).textContent || "",
          heb: /[֐-׿]/.test((document.querySelector("main") || document.body).innerText),
          prices: [...document.querySelectorAll(".buy-price")].map(e => e.textContent)
        }));
        const where = `${p} @${width}`;
        const bad = [];
        if (r.lang !== "en" || r.dir !== "ltr") bad.push("lang/dir " + r.lang + "/" + r.dir);
        if (r.over > 1) bad.push("horizontal overflow " + r.over + "px");
        if (!/עברית/.test(r.sw)) bad.push("no language switch");
        if (!/Planners.*Free tools.*Guides/.test(r.nav)) bad.push("nav not English");
        if (!/Terms of sale/.test(r.foot)) bad.push("footer not English");
        if (!p.startsWith("en/thanks/") && (r.h1 !== 1 || r.desc.length < 50 || !r.canon)) bad.push(`seo h1=${r.h1} desc=${r.desc.length} canon=${r.canon}`);
        if (r.prices.some(x => !/^\$\d/.test(x))) bad.push("non-USD price " + r.prices.join(","));
        if (errors.length) bad.push("errors: " + errors.join(" | "));
        ok(!bad.length, where + (bad.length ? " -> " + bad.join("; ") : ""));
        if (SHOTS && (p === "en/" || p === "en/p/bar-mitzvah-planner/" || p === "en/tools/seder-shopping-calculator/")) {
          fs.mkdirSync(SHOTS, { recursive: true });
          await page.screenshot({ path: path.join(SHOTS, `${p.replace(/\//g, "_") || "home"}${width}.png`), fullPage: width === 375 ? false : true });
        }
        await page.close();
      }
      await ctx.close();
    }

    // ---- test purchase: single planner and bundle
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    for (const [pg, slug, n, price] of [["en/p/bar-mitzvah-planner/", "bar-mitzvah-planner-en", 2, "$19"],
                                        ["en/planners/", "jewish-life-bundle", 8, "$49"]]) {
      await page.goto(BASE + pg + "?test=1", { waitUntil: "networkidle" });
      const btn = page.locator(`[data-test-pay="${slug}"]`).first();
      ok(await btn.count() === 1, `${pg}: test pay button for ${slug}`);
      ok((await btn.textContent()).includes(price), `${slug}: button shows ${price}`);
      const legal = await page.locator(`.buy[data-product="${slug}"] .buy-legal a`).first().getAttribute("href");
      ok(/en\/legal\/terms\/$/.test(legal), `${slug}: legal link -> English terms (${legal})`);
      await btn.click();
      await page.waitForURL(/en\/thanks\/\?p=/, { timeout: 10000 });
      ok(page.url().includes("p=" + slug) && page.url().includes("test=1"), `${slug}: redirected to en/thanks (${page.url().replace(BASE, "")})`);
      await page.waitForSelector("#ok:not([hidden])", { timeout: 10000 });
      const links = await page.$$eval("#downloads a.dl", as => as.map(a => a.href));
      ok(links.length === n, `${slug}: ${links.length} download links (want ${n})`);
      const codes = await Promise.all(links.map(head));
      ok(codes.every(c => c === 200), `${slug}: downloads respond 200 (${codes.join(",")})`);
      ok((await page.textContent("#r-price")).startsWith("$"), `${slug}: receipt in USD (${await page.textContent("#r-price")})`);
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `thanks-${slug}.png`), fullPage: true });
    }

    // ---- calculators
    await page.goto(BASE + "en/tools/bar-mitzvah-gift/", { waitUntil: "networkidle" });
    let a = await page.textContent("#amount");
    ok(/^\$\d+$/.test(a) && Number(a.slice(1)) % 18 === 0, `gift calculator default ${a} is a chai multiple`);
    await page.check('input[name="rel"][value="relative"]');
    await page.check('input[name="who"][value="2"]');
    const a2 = await page.textContent("#amount");
    ok(Number(a2.slice(1)) > Number(a.slice(1)) && Number(a2.slice(1)) % 18 === 0, `gift: relative couple ${a2} > ${a}`);
    await page.goto(BASE + "en/tools/bar-mitzvah-budget/", { waitUntil: "networkidle" });
    const t1 = await page.textContent("#total");
    await page.fill("#adults", "200");
    const t2 = await page.textContent("#total");
    const num = s => Number(s.replace(/[^0-9]/g, ""));
    ok(num(t1) > 5000 && num(t2) > num(t1), `budget: ${t1} -> ${t2} with more guests`);
    ok(await page.locator("#breakdown tbody tr").count() >= 8, "budget: breakdown rows");
    await page.goto(BASE + "en/tools/seder-shopping-calculator/", { waitUntil: "networkidle" });
    ok((await page.textContent("#k-matzah")) === "50", `seder: default shmurah matzot = ${await page.textContent("#k-matzah")} (want 50)`);
    ok((await page.textContent("#k-seats")) === "24", "seder: 24 place settings");
    await page.selectOption("#seders", "1");
    ok((await page.textContent("#k-matzah")) === "25", "seder: one seder halves matzah");

    // ---- Hebrew regression
    await page.goto(BASE + "p/bar-mitzvah-planner/?test=1", { waitUntil: "networkidle" });
    const he = await page.evaluate(() => ({
      price: (document.querySelector(".buy-price") || {}).textContent, btn: (document.querySelector("[data-test-pay]") || {}).textContent,
      sw: (document.querySelector(".lang-switch") || {}).getAttribute && document.querySelector(".lang-switch").getAttribute("href"),
      over: document.documentElement.scrollWidth - window.innerWidth
    }));
    ok(he.price === "₪39" && /תשלום בדיקה/.test(he.btn), `Hebrew page unchanged: ${he.price} / ${he.btn}`);
    ok(/\/en\//.test(he.sw || ""), `Hebrew header has English switch -> ${he.sw}`);
    for (const w of [375, 320]) {
      await page.setViewportSize({ width: w, height: 800 });
      const over = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      ok(over <= 1, `Hebrew header fits at ${w}px (overflow ${over})`);
    }
    await page.setViewportSize({ width: 1280, height: 900 });

    // ---- live PayPal SDK in USD
    const live = await ctx.newPage();
    let sdkUrl = "";
    live.on("request", r => { if (r.url().includes("paypal.com/sdk/js")) sdkUrl = r.url(); });
    await live.goto(BASE + "en/p/passover-seder-planner/", { waitUntil: "domcontentloaded" });
    try {
      await live.waitForSelector(".buy-buttons iframe, .buy-msg.error", { timeout: 20000 });
      const fr = await live.locator(".buy-buttons iframe").count();
      ok(/currency=USD/.test(sdkUrl) && /locale=en_US/.test(sdkUrl), `SDK requested with USD/en_US (${sdkUrl.split("?")[1] ? "ok" : sdkUrl})`);
      if (fr) ok(true, "live PayPal buttons rendered (USD)");
      else console.log("SKIP live PayPal buttons: SDK not reachable from this sandbox");
    } catch (e) { console.log("SKIP live PayPal check: " + e.message); }
  } finally {
    await browser.close();
    web.kill();
  }
  console.log(failures ? `\n${failures} FAILURE(S)` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})();
