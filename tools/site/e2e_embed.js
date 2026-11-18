// End-to-end test of the embeddable calculators (tools/site/build_embeds.py).
//   node tools/site/e2e_embed.js
// For every embed: page size < 40KB, noindex; rendered inside an <iframe> on a foreign "host" page using the exact
// snippet from the hub -> no JS errors, attribution link inside (followed, opens the full calculator) and under
// the iframe, postMessage auto-height resizes the iframe to the content (and again when content grows),
// same inputs give the same result as the full calculator page, no horizontal scroll at 375px.
// Hubs: every card has code + copy button + a preview that loads; source pages link to their hub card.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const PORT = 8776, HOST_PORT = 8777;
const BASE = `http://localhost:${PORT}/`;
const LIVE = "https://tichnun.netlify.app";
let failures = 0;
const ok = (c, msg) => { console.log((c ? "PASS " : "FAIL ") + msg); if (!c) failures++; };

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png" };
const serve = (root) => http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(root, p);
  if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
const server = serve(DOCS);
let hostHtml = "";
const host = http.createServer((req, res) => { res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" }); res.end(hostHtml); });

const CASES = [
  { slug: "wedding-gift", page: "tools/wedding-gift/", set: [['input[name=closeness][value=close]'], ['input[name=adults][value="1"]'], ["#kids", "2"], ["#region", "other"]], result: ["#r-amount", "#r-range", "#r-who"] },
  { slug: "vat-calculator", page: "tools/vat-calculator/", set: [['input[name=mode][value=remove]'], ["#amount", "2360"]], result: ["#v-big", "#v-before", "#v-vat"] },
  { slug: "osek-patur-ceiling", page: "tools/osek-patur-ceiling/", set: [["#income", "64000"], ["#month", "6"]], result: ["#r-used", "#r-left", "#r-proj"], sel: true },
  { slug: "net-salary-budget", page: "tools/net-salary-budget/", set: [["#income", "21000"], ["#housing", "6000"], ["#kids", "2"]], result: ["#k-left", "#sum-m", "#r-housing"] },
  { slug: "budget-503020", page: "tools/budget-503020/", set: [["#income", "18000"], ['input[name=model][value="60-20-20"]']], result: ["#vn", "#vw", "#ef"] },
  { slug: "sufganiyot-calculator", page: "tools/sufganiyot-calculator/", set: [["#adults", "14"], ["#kids", "9"], ['input[name=mode][value=make]']], result: ["#v-suf", "#v-lat", "#v-oil"] },
  { slug: "bar-mitzvah-gift", en: true, page: "en/tools/bar-mitzvah-gift/", set: [['input[name=rel][value=close]'], ['input[name=who][value="2"]'], ['input[name=area][value="1.2"]']], result: ["#amount", "#range"] },
  { slug: "bar-mitzvah-budget", en: true, page: "en/tools/bar-mitzvah-budget/", set: [["#adults", "150"], ['input[name=area][value=high]'], ["#ent", "7000"]], result: ["#total", "#perguest"] },
  { slug: "seder-shopping-calculator", en: true, page: "en/tools/seder-shopping-calculator/", set: [["#adults", "12"], ["#kids", "6"], ["#seders", "1"]], result: ["#k-seats", "#k-wine", "#k-matzah"] },
  { slug: "latke-calculator", en: true, page: "en/hanukkah/latke-calculator/", set: [["#adults", "10"], ["#kids", "8"], ['input[name=appetite][value=hungry]']], result: ["#v-lat", "#v-suf"] },
];

async function apply(target, set) {
  for (const [sel, val] of set) {
    const el = await target.$(sel);
    const tag = await el.evaluate(e => e.tagName);
    if (val === undefined) await el.check();
    else if (tag === "SELECT") await el.selectOption(val);
    else await el.fill(val);
  }
  await target.waitForTimeout(200);
}
const texts = (t, sels) => t.evaluate(s => s.map(x => { const el = document.querySelector(x); return el ? el.textContent.replace(/\s+/g, " ").trim() : null; }), sels);

async function newPage(browser, opts) {
  const ctx = await browser.newContext(opts || { viewport: { width: 1280, height: 900 } });
  await ctx.route(/fonts\.(googleapis|gstatic)\.com|paypal\.com/, r => r.abort());
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errs.push(m.text()); });
  return { ctx, page, errs };
}

(async () => {
  await new Promise(r => server.listen(PORT, r));
  await new Promise(r => host.listen(HOST_PORT, r));
  const browser = await chromium.launch();

  // hub snippets, keyed by slug, rewritten to point at the local server
  const snippets = {};
  for (const hub of ["embed/index.html", "en/embed/index.html"]) {
    const src = fs.readFileSync(path.join(DOCS, hub), "utf8");
    for (const m of src.matchAll(/<textarea id="code-([\w-]+)"[^>]*>([\s\S]*?)<\/textarea>/g)) {
      const code = m[2].replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#x27;/g, "'").replace(/&amp;/g, "&");
      snippets[m[1]] = code;
    }
  }

  for (const c of CASES) {
    const embedPath = (c.en ? "en/embed/" : "embed/") + c.slug + "/";
    const file = path.join(DOCS, embedPath, "index.html");
    const src = fs.readFileSync(file, "utf8");
    const bytes = Buffer.byteLength(src);
    ok(bytes < 40 * 1024, `${c.slug}: embed is ${(bytes / 1024).toFixed(1)} KB (< 40KB)`);
    ok(/<meta name="robots" content="noindex, follow">/.test(src), `${c.slug}: noindex, follow`);
    ok(!/id="site-header"|id="site-footer"|site\.js/.test(src), `${c.slug}: no site header/footer/site.js`);
    ok(new RegExp(`dir="${c.en ? "ltr" : "rtl"}"`).test(src), `${c.slug}: dir=${c.en ? "ltr" : "rtl"}`);

    const code = snippets[c.slug];
    ok(!!code, `${c.slug}: hub has a snippet`);
    if (!code) continue;
    ok(code.includes(`${LIVE}/${c.page}`) && !/nofollow/.test(code), `${c.slug}: snippet credit links (followed) to ${c.page}`);
    hostHtml = `<!doctype html><html><head><meta charset="utf-8"><title>host</title></head><body style="margin:0;font-family:sans-serif">
      <h1>Some blog</h1><p>Text before.</p>${code.split(LIVE).join(BASE.replace(/\/$/, ""))}<p id="after">Text after.</p></body></html>`;

    const H = await newPage(browser);
    await H.page.goto(`http://localhost:${HOST_PORT}/`, { waitUntil: "load" });
    const iframeEl = await H.page.waitForSelector("iframe[data-tichnun-embed]");
    const frame = await iframeEl.contentFrame();
    await frame.waitForLoadState("load");
    await H.page.waitForTimeout(400);
    const credit = await frame.$eval(".embed-credit a", a => ({ href: a.href, rel: a.rel, text: a.closest("p").textContent.trim(), target: a.target }));
    ok(credit.href === `${LIVE}/${c.page}` && !/nofollow/.test(credit.rel) && credit.target === "_blank", `${c.slug}: attribution link in the iframe → ${credit.href} (${credit.text})`);
    ok(c.en ? /Calculator by/.test(credit.text) : /מחשבון: תכנון פלוס/.test(credit.text), `${c.slug}: attribution text`);
    const sizes = async () => ({ iframe: await iframeEl.evaluate(f => f.getBoundingClientRect().height), content: await frame.evaluate(() => Math.ceil(document.querySelector(".embed-wrap").getBoundingClientRect().height)) });
    let s = await sizes();
    ok(Math.abs(s.iframe - s.content) <= 8, `${c.slug}: auto-height iframe ${s.iframe}px ≈ content ${s.content}px`);
    // grow the content: open every <details> (or add a quote row) and check the iframe follows
    await frame.evaluate(() => { document.querySelectorAll("details").forEach(d => d.open = true); const b = document.getElementById("q-add"); if (b) for (let i = 0; i < 4; i++) b.click(); });
    await H.page.waitForTimeout(400);
    const s2 = await sizes();
    ok(Math.abs(s2.iframe - s2.content) <= 8, `${c.slug}: height follows content change (${s.content}→${s2.content}px, iframe ${s2.iframe}px)`);
    await frame.evaluate(() => { document.querySelectorAll("details").forEach(d => d.open = false); });

    await apply(frame, c.set);
    const got = await texts(frame, c.result);
    const F = await newPage(browser);
    await F.page.goto(BASE + c.page, { waitUntil: "load" });
    await apply(F.page, c.set);
    const want = await texts(F.page, c.result);
    ok(JSON.stringify(got) === JSON.stringify(want) && got.every(x => x), `${c.slug}: same result as the full page ${JSON.stringify(got)}`);
    ok(H.errs.length === 0 && F.errs.length === 0, `${c.slug}: no JS errors ${JSON.stringify(H.errs.concat(F.errs))}`);
    const embedLink = await F.page.$eval(".embed-link a", a => a.getAttribute("href")).catch(() => null);
    ok(embedLink === `${LIVE}/${c.en ? "en/embed/" : "embed/"}#${c.slug}`, `${c.slug}: calculator page links to its embed card (${embedLink})`);
    await H.ctx.close(); await F.ctx.close();

    // phone width: no horizontal scroll
    const M = await newPage(browser, { viewport: { width: 375, height: 800 }, isMobile: true, hasTouch: true });
    await M.page.goto(BASE + embedPath, { waitUntil: "load" });
    const ov = await M.page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    ok(ov <= 1, `${c.slug}: no horizontal scroll at 375px (overflow ${ov}px)`);
    if (process.env.SHOTS) await M.page.screenshot({ path: path.join(process.env.SHOTS, `embed-${c.slug}.png`), fullPage: true });
    await M.ctx.close();
  }

  for (const [hub, n] of [["embed/", (d => fs.readdirSync(path.join(DOCS, d), { withFileTypes: true }).filter(e => e.isDirectory()).length)("embed")], ["en/embed/", (d => fs.readdirSync(path.join(DOCS, d), { withFileTypes: true }).filter(e => e.isDirectory()).length)("en/embed")]]) {
    const P = await newPage(browser);
    await P.page.goto(BASE + hub, { waitUntil: "load" });
    const cards = await P.page.$$eval(".embed-item", els => els.map(e => ({ id: e.id, code: !!e.querySelector("textarea.embed-code"), btn: !!e.querySelector("[data-copy]") })));
    ok(cards.length === n && cards.every(c => c.code && c.btn), `hub ${hub}: ${cards.length} cards with code + copy button`);
    const first = await P.page.$(".embed-item details");
    await first.evaluate(d => d.open = true);
    await P.page.waitForTimeout(800);
    const fr = await (await P.page.$(".embed-item iframe")).contentFrame();
    const has = fr ? await fr.$(".embed-credit a") : null;
    ok(!!has, `hub ${hub}: live preview loads when opened`);
    const ld = await P.page.$$eval('script[type="application/ld+json"]', s => s.map(x => JSON.parse(x.textContent)["@type"]));
    ok(ld.includes("ItemList") && ld.includes("FAQPage"), `hub ${hub}: JSON-LD ${ld}`);
    ok(P.errs.length === 0, `hub ${hub}: no JS errors ${JSON.stringify(P.errs)}`);
    await P.ctx.close();
  }

  // data-il page: every download link resolves and parses, Dataset JSON-LD per dataset, JS helper works in the page
  {
    const P = await newPage(browser);
    await P.page.goto(BASE + "data-il/", { waitUntil: "load" });
    const links = await P.page.$$eval("a[download]", as => as.map(a => a.getAttribute("href")));
    let good = 0;
    for (const l of links) {
      const r = await P.page.request.get(BASE + "data-il/" + l);
      const t = await r.text();
      if (r.ok() && (l.endsWith(".json") ? JSON.parse(t).rows.length > 0 : t.split("\n").length > 2)) good++;
    }
    ok(links.length === 10 && good === links.length, `data-il: ${good}/${links.length} downloads OK`);
    const ld = await P.page.$$eval('script[type="application/ld+json"]', s => s.map(x => JSON.parse(x.textContent)));
    const ds = ld.filter(x => x["@type"] === "Dataset");
    ok(ds.length === 5 && ds.every(d => d.license && d.distribution.length === 2 && d.creator), `data-il: ${ds.length} Dataset JSON-LD blocks with license + distribution`);
    await P.page.addScriptTag({ url: BASE + "data-il/israel-data.js" });
    const js = await P.page.evaluate(() => [IsraelData.isIsraeliHoliday("2026-04-22")[0].id, IsraelData.addVat(1000).gross, IsraelData.removeVat(1180).net, IsraelData.osekPaturCeiling(2026), IsraelData.vatRate("2015-06-01")]);
    ok(JSON.stringify(js) === JSON.stringify(["yom-haatzmaut", 1180, 1000, 122833, 0.18]), `data-il: israel-data.js helpers ${JSON.stringify(js)}`);
    ok(P.errs.length === 0, `data-il: no JS errors ${JSON.stringify(P.errs)}`);
    await P.ctx.close();
  }

  await browser.close(); server.close(); host.close();
  console.log(failures ? `\n${failures} FAILURE(S)` : "\nALL PASSED");
  process.exit(failures ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
