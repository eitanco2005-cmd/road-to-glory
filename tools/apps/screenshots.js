// Product screenshots for p/seating-chart/img and p/cv-builder/img (PNG for og:image + WebP for the page).
//   node tools/apps/screenshots.js     (serves docs/ itself on a local port; needs python3 + Pillow for WebP)
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const PORT = 8772, BASE = `http://localhost:${PORT}/`;
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
function webp(png) {
  execFileSync("python3", ["-c", "import sys;from PIL import Image;im=Image.open(sys.argv[1]);im.save(sys.argv[1][:-4]+'.webp','WEBP',quality=82,method=6)", png]);
}
async function page(browser, vp, scale) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: scale || 1, locale: "he-IL" });
  await ctx.route(/paypal\.com/, r => r.abort());
  const p = await ctx.newPage();
  await p.addInitScript(() => { window.print = () => {}; });
  return p;
}
async function hideChrome(p) {
  await p.addStyleTag({ content: ".site-header,.toast{display:none!important}" });
}

(async () => {
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();
  const S = path.join(DOCS, "p/seating-chart/img"), C = path.join(DOCS, "p/cv-builder/img");
  fs.mkdirSync(S, { recursive: true }); fs.mkdirSync(C, { recursive: true });
  const shots = [];

  // ---- seating ----
  let p = await page(browser, { width: 1280, height: 860 });
  await p.goto(BASE + "apps/seating/?demo=1");
  await p.evaluate(() => { const S = SeatingApp.state(); S.date = "2027-06-17"; SeatingApp.autoSeat(false); });
  await p.waitForTimeout(500); await hideChrome(p);
  await p.evaluate(() => window.scrollTo(0, document.getElementById("app").offsetTop - 8));
  await p.screenshot({ path: path.join(S, "screen-1.png") }); shots.push(path.join(S, "screen-1.png"));
  // print layout (as printed, rendered on screen) and table cards: use a stored (fake) unlock in this throwaway context
  await p.evaluate(() => localStorage.setItem("tp-unlocks", JSON.stringify({ "seating-chart": { o: "SCREENSHOT", t: 1, test: false } })));
  const printShot = async (act, file) => {
    await p.evaluate(a => { document.querySelector(`[data-act=${a}]`).click(); document.body.classList.add("printing"); window.scrollTo(0, 0); }, act);
    await p.emulateMedia({ media: "print" });
    await p.setViewportSize({ width: 820, height: 1100 });
    await p.evaluate(() => window.scrollTo(0, 0));
    await p.screenshot({ path: file }); shots.push(file);
    await p.evaluate(() => document.body.classList.remove("printing"));
    await p.emulateMedia({ media: "screen" });
    await p.setViewportSize({ width: 1280, height: 860 });
  };
  await printShot("pdf-clean", path.join(S, "screen-3.png"));
  await printShot("cards", path.join(S, "screen-4.png"));
  // conflict + edit dialog
  await p.evaluate(() => {
    const S = SeatingApp.state(); const a = S.guests.find(g => g.name === "משפחת פרץ"), b = S.guests.find(g => g.name === "משפחת חדד");
    b.table = a.table; SeatingApp.render();
  });
  await p.evaluate(() => document.querySelector(".t-card.conflict").scrollIntoView({ block: "center" }));
  await p.click(".t-card.conflict .g-apart >> nth=0");
  await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(S, "screen-2.png") }); shots.push(path.join(S, "screen-2.png"));
  await p.context().close();
  // mobile
  p = await page(browser, { width: 390, height: 844 }, 2);
  await p.goto(BASE + "apps/seating/?demo=1");
  await p.evaluate(() => SeatingApp.autoSeat(false));
  await p.click("[data-tab=tables]"); await hideChrome(p);
  await p.evaluate(() => document.getElementById("app").scrollIntoView());
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(S, "screen-5.png") }); shots.push(path.join(S, "screen-5.png"));
  await p.context().close();

  // ---- seating, English (og:image + catalog thumb) ----
  const SE = path.join(DOCS, "en/apps/seating/img"); fs.mkdirSync(SE, { recursive: true });
  p = await page(browser, { width: 1280, height: 860 });
  await p.goto(BASE + "en/apps/seating/?demo=1");
  await p.evaluate(() => SeatingApp.autoSeat(false));
  await p.waitForTimeout(400); await hideChrome(p);
  await p.evaluate(() => window.scrollTo(0, document.getElementById("app").offsetTop - 8));
  await p.screenshot({ path: path.join(SE, "screen-1.png") }); shots.push(path.join(SE, "screen-1.png"));
  await p.context().close();

  // ---- cv ----
  p = await page(browser, { width: 1280, height: 860 });
  await p.goto(BASE + "apps/cv/?demo=1");
  await p.waitForTimeout(400); await hideChrome(p);
  await p.evaluate(() => window.scrollTo(0, document.getElementById("app").offsetTop - 8));
  await p.screenshot({ path: path.join(C, "screen-1.png") }); shots.push(path.join(C, "screen-1.png"));
  // the four templates side by side
  const html = await p.evaluate(() => {
    const out = [];
    for (const t of ["classic", "modern", "minimal", "executive"]) { CvApp.state().template = t; CvApp.render(); out.push(document.getElementById("cv-page").outerHTML.replace('id="cv-page"', "").replace(/transform:[^;"]*;?/, "")); }
    CvApp.state().template = "classic"; CvApp.render();
    return out;
  });
  await p.setContent(`<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><link rel="stylesheet" href="${BASE}assets/site.css"><link rel="stylesheet" href="${BASE}apps/cv/app.css"><style>body{background:#e9e4da;margin:0;padding:28px}.g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}.g>div{min-width:0}.w{height:560px;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.15);background:#fff}.w .cv{transform:scale(.5);transform-origin:top right;background:#fff}.l{text-align:center;font:800 20px Assistant,Arial;margin:10px 0 0;color:#1d2a2e}</style></head><body><div class="g">${html.map((h, i) => `<div><div class="w">${h}</div><p class="l">${["קלאסי", "מודרני", "מינימלי", "בכיר"][i]}</p></div>`).join("")}</div></body></html>`);
  await p.setViewportSize({ width: 1640, height: 680 });
  await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(C, "screen-2.png") }); shots.push(path.join(C, "screen-2.png"));
  await p.context().close();
  p = await page(browser, { width: 1280, height: 860 });
  await p.goto(BASE + "apps/cv/?demo=1");
  await p.click("[data-lang=en]"); await p.click("[data-tpl=modern]"); await p.click("[data-accent='#1f4e8c']");
  await p.waitForTimeout(300);
  await p.locator("#cv-page").screenshot({ path: path.join(C, "screen-3.png") }); shots.push(path.join(C, "screen-3.png"));
  await p.evaluate(() => { const s = CvApp.state(); s.lang = "he"; s.template = "classic"; s.accent = "#0e6b63"; CvApp.render(); });
  await p.context().close();
  p = await page(browser, { width: 390, height: 844 }, 2);
  await p.goto(BASE + "apps/cv/?demo=1");
  await hideChrome(p);
  await p.click("[data-tab=preview]");
  await p.evaluate(() => document.getElementById("app").scrollIntoView());
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(C, "screen-4.png") }); shots.push(path.join(C, "screen-4.png"));
  await p.context().close();

  await browser.close(); server.close();
  shots.forEach(webp);
  console.log("wrote", shots.length, "screenshots (+ .webp)");
})();
