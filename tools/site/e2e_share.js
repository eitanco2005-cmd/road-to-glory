// End-to-end test of calculator sharing (docs/assets/share.js).
//   node tools/site/e2e_share.js
// For every free calculator: change a few inputs -> the share bar shows a WhatsApp link (wa.me, message + link)
// -> the link holds only the changed numeric/choice inputs (no free text) -> opening that link in a FRESH browser
// context shows the same result -> the copy/share button and the og:image (top calculators) exist.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const PORT = 8774;
const BASE = `http://localhost:${PORT}/`;
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});

// set: [selector, value] for fill, or [selector] for check/click. result: selectors whose text must match after reopening.
const CASES = [
  { url: "tools/wedding-gift/", set: [['input[name=closeness][value=close]'], ['input[name=adults][value="1"]'], ["#kids", "2"], ["#region", "other"], ['input[name=chai]']], result: ["#r-amount", "#r-range", "#r-who"], og: true },
  { url: "tools/bar-mitzvah-cost/", set: [['input[name=who][value=bat]'], ["#adults", "200"], ["#plate", "320"], ['input[name=use_magnets]']], result: ["#r-total", "#r-per", "#r-net"], og: true },
  { url: "tools/vat-calculator/", set: [['input[name=mode][value=remove]'], ["#amount", "2360"]], result: ["#v-big", "#v-before", "#v-vat"], og: true },
  { url: "tools/osek-patur-ceiling/", set: [["#income", "64000"], ["#month", "6"]], result: ["#r-used", "#r-left", "#r-proj"], og: true, sel: true },
  { url: "tools/budget-503020/", set: [["#income", "18000"], ['input[name=model][value="60-20-20"]']], result: ["#vn", "#vw", "#ef"] },
  { url: "tools/net-salary-budget/", set: [["#income", "21000"], ["#housing", "6000"], ["#kids", "2"], ["#c-food", "4000"]], result: ["#k-left", "#sum-m", "#r-housing"] },
  { url: "tools/renovation-cost/", set: [["#area", "110"], ['input[name=level][value="2"]'], ['input[name=w][value=elec]'], ["#baths", "2"]], result: ["#total", "#sub"] },
  { url: "tools/savings-goal/", set: [["#target", "40000"], ["#current", "5000"], ["#months", "18"], ["#rate", "3"]], result: ["#big", "#k-end"] },
  { url: "tools/sufganiyot-calculator/", set: [["#adults", "14"], ["#kids", "9"], ['input[name=mode][value=make]']], result: ["#v-suf", "#v-lat", "#v-oil"] },
  { url: "en/tools/bar-mitzvah-budget/", set: [["#adults", "150"], ['input[name=area][value=high]'], ["#ent", "7000"]], result: ["#total", "#perguest"] },
  { url: "en/tools/bar-mitzvah-gift/", set: [['input[name=rel][value=close]'], ['input[name=who][value="2"]'], ['input[name=area][value="1.2"]']], result: ["#amount", "#range"] },
  { url: "en/tools/seder-shopping-calculator/", set: [["#adults", "12"], ["#kids", "6"], ["#seders", "1"]], result: ["#k-seats", "#k-wine", "#k-matzah"] },
  { url: "en/hanukkah/latke-calculator/", set: [["#adults", "10"], ["#kids", "8"], ['input[name=appetite][value=hungry]']], result: ["#v-lat", "#v-suf"] },
];

async function ctxPage(browser, mobile) {
  const ctx = await browser.newContext(mobile ? { viewport: { width: 375, height: 800 }, hasTouch: true, isMobile: true } : { viewport: { width: 1280, height: 900 } });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|paypal\.com/, r => r.abort());
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(e.message));
  return { ctx, page, errs };
}
const texts = (page, sels) => page.evaluate(s => s.map(x => { const el = document.querySelector(x); return el ? el.textContent.replace(/\s+/g, " ").trim() : null; }), sels);

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  for (const c of CASES) {
    const A = await ctxPage(browser);
    await A.page.goto(BASE + c.url, { waitUntil: "load" });
    await A.page.waitForSelector("[data-share] [data-share-wa]", { state: "attached" });
    const before = await texts(A.page, c.result);
    for (const [sel, val] of c.set) {
      const el = A.page.locator(sel).first();
      const tag = await el.evaluate(e => e.tagName + ":" + (e.type || ""));
      if (tag.startsWith("SELECT")) await el.selectOption(val);
      else if (val !== undefined) await el.fill(val);
      else if (tag.endsWith("checkbox")) await el.setChecked(!(await el.isChecked()));
      else await el.check();
    }
    await A.page.waitForTimeout(150);
    const after = await texts(A.page, c.result);
    ok(JSON.stringify(after) !== JSON.stringify(before), `${c.url}: inputs change the result (${after[0]})`);
    const wa = await A.page.locator("[data-share-wa]").first();
    ok(await wa.isVisible(), `${c.url}: WhatsApp button visible after a result`);
    await wa.focus();
    const href = await wa.getAttribute("href");
    const url = await A.page.locator("[data-share]").first().getAttribute("data-share-url");
    ok(href.startsWith("https://wa.me/?text=") && decodeURIComponent(href.slice(20)).endsWith(url), `${c.url}: wa.me link = message + share link`);
    const msg = decodeURIComponent(href.slice(20));
    ok(!/\{result\d?\}/.test(msg) && msg.length < 400, `${c.url}: message is filled and short: "${msg.split("\n")[0]}"`);
    ok(url.startsWith(BASE + c.url + "#c&"), `${c.url}: link points at the same page with the inputs in the hash`);
    ok(A.errs.length === 0, `${c.url}: no page errors ${A.errs.join(" | ")}`);
    const more = A.page.locator("[data-share-more]").first();
    await more.click();
    await A.page.waitForTimeout(100);
    ok(await A.page.locator("[data-share-ok]").first().isVisible(), `${c.url}: desktop copy-link fallback confirms`);
    if (c.og) {
      const og = await A.page.locator('meta[property="og:image"]').getAttribute("content");
      const local = path.join(DOCS, og.replace(/^https:\/\/tichnun\.netlify\.app\//, ""));
      ok(/\/og\/[a-z0-9-]+\.png$/.test(og) && fs.existsSync(local), `${c.url}: own og:image ${og.split("/").pop()}`);
    }
    await A.ctx.close();

    // reopen in a fresh context (no storage, no history), as the friend on WhatsApp would
    const B = await ctxPage(browser, true);
    await B.page.goto(url, { waitUntil: "load" });
    await B.page.waitForSelector("[data-share] [data-share-wa]", { state: "attached" });
    await B.page.waitForTimeout(150);
    const reopened = await texts(B.page, c.result);
    ok(JSON.stringify(reopened) === JSON.stringify(after), `${c.url}: shared link reopens the same result (${reopened.join(" / ").slice(0, 80)})`);
    ok(B.errs.length === 0, `${c.url}: no page errors on reopen ${B.errs.join(" | ")}`);
    const mobileBtn = await B.page.locator("[data-share-more]").first().textContent();
    ok(mobileBtn.length > 0, `${c.url}: mobile secondary button "${mobileBtn}"`);
    const overflow = await B.page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ok(overflow <= 1, `${c.url}: no horizontal overflow at 375px`);
    await B.ctx.close();
  }
  // free text in another panel (VAT quote builder) never goes into the link
  const V = await ctxPage(browser);
  await V.page.goto(BASE + "tools/vat-calculator/", { waitUntil: "load" });
  await V.page.fill("#amount", "100");
  const textInputs = await V.page.locator('input[type=text]').count();
  if (textInputs) await V.page.locator("input[type=text]").first().fill("Private Name");
  await V.page.locator("[data-share-wa]").focus();
  const vurl = await V.page.locator("[data-share]").getAttribute("data-share-url");
  ok(!/Private|Name/.test(decodeURIComponent(vurl)), `vat: free text never in the share link (${vurl.split("#")[1]})`);
  await V.ctx.close();
  // a page opened without a hash keeps its defaults (no stray state)
  const D = await ctxPage(browser);
  await D.page.goto(BASE + "tools/wedding-gift/", { waitUntil: "load" });
  await D.page.waitForSelector("[data-share-wa]", { state: "attached" });
  const durl = await D.page.locator("[data-share]").getAttribute("data-share-url");
  ok(durl === BASE + "tools/wedding-gift/", `defaults share the plain page URL (${durl})`);
  await D.ctx.close();

  await browser.close();
  server.close();
  console.log(failures ? `\n${failures} FAILURE(S)` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
