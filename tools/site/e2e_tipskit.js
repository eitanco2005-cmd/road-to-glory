// End-to-end check of Streams C+D in TEST mode (no real payment).
//   node tools/site/e2e_tipskit.js
// Serves docs/ at the domain root and checks, at 375px and 1280px:
//  C1 tip jar: hidden before use, shown after a result on every free tool, test tip -> inline thank-you, no overflow
//  C2 product pages: bundle upsell with real savings under the buy box
//  C3 thanks page: one-time 20% offer, pays in TEST, goes to the offered product's thanks page, never shown twice
//  D  devkit: landing renders, demos load (he/ar/en switch flips dir), free zip + Pro zip exist, TEST purchase -> download
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");

const DOCS = path.resolve(__dirname, "../../docs");
const PORT = 8798;
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".zip": "application/zip", ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".xlsx": "application/octet-stream" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
const TOOLS = JSON.parse(fs.readFileSync(path.join(DOCS, "data/tools.json"))).tools.map(t => t.slug)
  .filter(s => fs.existsSync(path.join(DOCS, "tools", s, "index.html")));

(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const B = `http://127.0.0.1:${PORT}`;
  const b = await chromium.launch();
  const errors = [];
  const newPage = async (w) => {
    const ctx = await b.newContext({ viewport: { width: w, height: 850 } });
    // block PayPal so the test never touches real payments (TEST mode doesn't load it anyway)
    await ctx.route(/paypal(objects)?\.com/, r => r.abort());
    const p = await ctx.newPage();
    p.on("pageerror", e => errors.push(p.url() + " " + e.message));
    return p;
  };
  const overflow = p => p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);

  // ---------- C1 tip jar ----------
  for (const w of [375, 1280]) {
    for (const t of TOOLS) {
      const p = await newPage(w);
      await p.goto(`${B}/tools/${t}/?test=1`);
      await p.waitForTimeout(700);
      const before = await p.locator(".tip-jar:visible").count();
      const inp = p.locator("main input[type=number]:visible").first();
      if (await inp.count()) await inp.fill("300");
      const btn = p.locator("main form button:visible").first();
      if (await btn.count()) await btn.click().catch(() => {});
      await p.waitForTimeout(2600);
      const after = await p.locator(".tip-jar:visible").count();
      ok(before === 0 && after === 1, `${w}px ${t}: tip jar hidden before use (${before}), shown after a result (${after})`);
      ok(!(await overflow(p)), `${w}px ${t}: no horizontal overflow`);
      if (w === 1280 && t === TOOLS[0]) {
        await p.fill("#tip-amt", "3");
        await p.click('[data-test-pay="tip"]');
        ok(/בין ₪5/.test(await p.locator(".tip-jar .pk-msg").textContent()), "custom tip below ₪5 is refused");
        await p.fill("#tip-amt", "15");
        await p.click('[data-test-pay="tip"]');
        await p.waitForSelector(".tip-thanks", { timeout: 6000 });
        ok(true, "test tip ₪15 -> inline thank-you");
        await p.goto(`${B}/tools/${TOOLS[1]}/`);
        await p.waitForTimeout(600);
        const inp2 = p.locator("main input[type=number]:visible").first();
        if (await inp2.count()) await inp2.fill("300");
        await p.waitForTimeout(2600);
        ok(await p.locator(".tip-jar").count() === 0, "after tipping, the jar is not shown again (outside test mode)");
      }
      if (w === 375 && t === TOOLS[0]) {
        await p.click(".tip-x");
        await p.goto(`${B}/tools/${TOOLS[0]}/`);
        await p.waitForTimeout(500);
        const i3 = p.locator("main input[type=number]:visible").first();
        if (await i3.count()) await i3.fill("500");
        await p.waitForTimeout(2600);
        ok(await p.locator(".tip-jar").count() === 0, "dismissed (×) tip jar stays hidden");
      }
      await p.context().close();
    }
  }

  // ---------- C2 product page upsell ----------
  for (const w of [375, 1280]) {
    for (const [slug, bundle] of [["household-budget", "money-bundle"], ["wedding-planner", "event-bundle"], ["osek-patur-tracker", "freelancer-bundle"]]) {
      const p = await newPage(w);
      await p.goto(`${B}/p/${slug}/`);
      await p.waitForSelector(".upsell-box", { timeout: 5000 }).catch(() => {});
      const box = p.locator(".upsell-box");
      const txt = (await box.count()) ? await box.textContent() : "";
      ok(/חוסכים ₪\d+/.test(txt) && (await box.getAttribute("data-upsell-bundle")) === bundle, `${w}px ${slug}: upsell shows ${bundle} with savings`);
      ok(!(await overflow(p)), `${w}px ${slug}: no overflow`);
      await p.context().close();
    }
  }

  // ---------- C3 thanks-page offer ----------
  {
    const p = await newPage(1280);
    await p.goto(`${B}/thanks/?p=osek-patur-tracker&o=TEST-E2E-1&test=1`);
    await p.waitForSelector(".offer-box", { timeout: 5000 }).catch(() => {});
    const offer = p.locator(".offer-box");
    ok(await offer.count() === 1 && (await offer.getAttribute("data-offer")) === "price-quote-pack", "thanks page offers the complementary product");
    const price = await p.locator(".offer-price .num").first().textContent();
    ok(price.trim() === "₪23", `20% off ₪29 -> ${price.trim()} (rounded to whole shekels)`);
    ok(!/\d{1,2}:\d{2}/.test(await offer.textContent()), "no countdown timer in the offer");
    await p.click('[data-test-pay="price-quote-pack"]');
    await p.waitForURL(/thanks\/\?p=price-quote-pack/, { timeout: 8000 });
    await p.waitForSelector("#ok:not([hidden])");
    ok(true, "offer paid in TEST -> thanks page of price-quote-pack");
    await p.waitForTimeout(1500);
    ok(await p.locator(".offer-box").count() === 0, "offer is not shown again after use");
    await p.goto(`${B}/thanks/?p=household-budget&o=TEST-E2E-2&test=1`);
    await p.waitForTimeout(1500);
    ok(await p.locator(".offer-box").count() === 0, "one offer per browser (none on a later order)");
    await p.context().close();
  }

  // ---------- D devkit ----------
  ok(fs.existsSync(path.join(DOCS, "devkit/rtl-landing-kit-free.zip")), "free zip published");
  const pro = JSON.parse(fs.readFileSync(path.join(DOCS, "data/products/rtl-kit-pro.json")));
  ok(fs.existsSync(path.join(DOCS, pro.files[0].path)) && pro.price_usd === 24, "Pro zip exists, price $24");
  for (const w of [375, 1280]) {
    const p = await newPage(w);
    await p.goto(`${B}/devkit/?test=1`);
    ok((await p.locator("h1").textContent()).includes("right-to-left"), `${w}px devkit landing renders`);
    ok(!(await overflow(p)), `${w}px devkit landing: no overflow`);
    for (const n of ["launch", "studio", "pocket"]) {
      for (const v of ["index", "tailwind"]) {
        await p.goto(`${B}/devkit/demos/templates/${n}/${v}.html`);
        const he = await p.evaluate(() => document.documentElement.dir);
        await p.goto(`${B}/devkit/demos/templates/${n}/${v}.html?lang=en`);
        const en = await p.evaluate(() => [document.documentElement.dir, document.documentElement.lang, document.querySelector("h1").textContent]);
        ok(he === "rtl" && en[0] === "ltr" && en[1] === "en" && /[a-z]/i.test(en[2]), `${w}px demo ${n}/${v}: rtl by default, ?lang=en -> ltr English`);
        ok(!(await overflow(p)), `${w}px demo ${n}/${v} (en): no overflow`);
      }
    }
    if (w === 1280) {
      await p.goto(`${B}/devkit/?test=1`);
      await p.click('[data-test-pay="rtl-kit-pro"]');
      await p.waitForURL(/devkit\/thanks\//, { timeout: 8000 });
      await p.waitForSelector("#ok:not([hidden])");
      const href = await p.getAttribute("#files a.dl", "href");
      const r = await p.request.get(href);
      ok(r.status() === 200 && (await r.body()).length > 50000, "Pro TEST purchase -> thanks -> zip downloads");
    }
    await p.context().close();
  }

  ok(errors.length === 0, "no page errors" + (errors.length ? ": " + errors.join(" | ") : ""));
  await b.close();
  server.close();
  console.log(failures ? `\n${failures} FAILED` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
