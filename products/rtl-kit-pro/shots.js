// Screenshots for the RTL Landing Kit landing page + GitHub README.
//   node products/rtl-kit-pro/shots.js     (run by build.py)
// Serves the repo root on a local port, then:
//   devkit/screenshots/<free>-<lang>.png            (README, 1280 wide, top of page)
//   docs/devkit/img/free-<name>.jpg, pro-<slug>.jpg  (landing page cards)
//   docs/devkit/img/pro-components.jpg, pro-dashboard-mobile.jpg
const { chromium } = require("playwright");
const http = require("http");
const fs = require("fs");
const path = require("path");

const REPO = path.resolve(__dirname, "../..");
const PORT = 8799;
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".png": "image/png", ".svg": "image/svg+xml" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(REPO, p);
  if (!f.startsWith(REPO) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(PORT, "127.0.0.1", r));
  const base = `http://127.0.0.1:${PORT}`;
  const img = path.join(REPO, "docs/devkit/img");
  const readme = path.join(REPO, "devkit/screenshots");
  fs.mkdirSync(img, { recursive: true });
  fs.mkdirSync(readme, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1280, height: 800 }, colorScheme: "light" });
  const page = await ctx.newPage();
  const shot = async (url, file, opts = {}) => {
    await page.goto(base + url, { waitUntil: "networkidle" }).catch(() => {});
    await page.evaluate(() => { document.querySelectorAll("[data-dir-toggle]").forEach(b => b.remove()); return document.fonts && document.fonts.ready; });
    await page.waitForTimeout(250);
    await page.screenshot({ path: file, type: file.endsWith(".jpg") ? "jpeg" : "png", quality: file.endsWith(".jpg") ? 78 : undefined, ...opts });
    console.log("shot", path.relative(REPO, file));
  };
  for (const n of ["launch", "studio", "pocket"]) {
    for (const lang of ["he", "ar", "en"]) {
      await shot(`/devkit/templates/${n}/index.html${lang === "he" ? "" : "?lang=" + lang}`, path.join(readme, `${n}-${lang}.png`));
    }
    await shot(`/devkit/templates/${n}/index.html`, path.join(img, `free-${n}.jpg`));
  }
  const listing = JSON.parse(fs.readFileSync(path.join(__dirname, "build/listing.json"), "utf8"));
  for (const [slug] of listing) {
    await shot(`/products/rtl-kit-pro/build/rtl-landing-kit-pro/templates/${slug}.html`, path.join(img, `pro-${slug}.jpg`));
  }
  await shot(`/products/rtl-kit-pro/build/rtl-landing-kit-pro/components/index.html#forms`, path.join(img, `pro-components.jpg`));
  await page.setViewportSize({ width: 390, height: 844 });
  await shot(`/products/rtl-kit-pro/build/rtl-landing-kit-pro/templates/dashboard.html`, path.join(img, `pro-dashboard-mobile.jpg`));
  await b.close();
  server.close();
})().catch(e => { console.error(e); process.exit(1); });
