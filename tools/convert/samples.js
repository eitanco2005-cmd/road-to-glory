// Free samples + 2x product previews for the wedding conversion round (R6B).
//   node tools/convert/samples.js     (serves docs/ on a local port; needs python3 + Pillow, pdftoppm)
// Writes:
//   docs/samples/seating-chart-sample.pdf   clean seating PDF from apps/seating demo data (fake names) + "sample" banner
//   docs/samples/invitation-sample.png      clean invitation PNG from apps/invite (fake names), 1200px wide
//   docs/samples/img/*.webp                 previews of the 3 samples for product pages / hub
//   docs/p/rsvp-tracker/img/screen-*.{png,webp}  RSVP app screenshots at 2x (product page)
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const http = require("http");

const REPO = path.resolve(__dirname, "../..");
const DOCS = path.join(REPO, "docs");
const SAMPLES = path.join(DOCS, "samples"), IMG = path.join(SAMPLES, "img"), RS = path.join(DOCS, "p/rsvp-tracker/img");
const SCRATCH = fs.mkdtempSync(path.join(require("os").tmpdir(), "tp-samples-"));
const PORT = 8781, BASE = `http://localhost:${PORT}/`;
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, BASE).pathname);
  if (p.endsWith("/")) p += "index.html";
  const f = path.join(DOCS, p);
  if (!f.startsWith(DOCS) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
const py = (code, ...args) => execFileSync("python3", ["-c", code, ...args]);
const toWebp = (png, out, width) => py(
  "import sys;from PIL import Image;im=Image.open(sys.argv[1]).convert('RGB');w=int(sys.argv[3]);" +
  "im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS) if w and im.width>w else im;im.save(sys.argv[2],'WEBP',quality=82,method=6)",
  png, out || png.replace(/\.png$/, ".webp"), String(width || 0));

async function ctx(browser, vp, scale) {
  const c = await browser.newContext({ viewport: vp, deviceScaleFactor: scale || 2, locale: "he-IL", acceptDownloads: true });
  await c.route(/paypal\.com/, r => r.abort());
  const p = await c.newPage();
  await p.addInitScript(() => { window.print = () => {}; });
  return p;
}
const hideChrome = p => p.addStyleTag({ content: ".site-header,.toast,.site-footer,.buy-bar{display:none!important}" });

(async () => {
  [SAMPLES, IMG, RS].forEach(d => fs.mkdirSync(d, { recursive: true }));
  await new Promise(r => server.listen(PORT, r));
  const browser = await chromium.launch();

  // ---- seating sample PDF (clean export of the demo event, fake names) ----
  let p = await ctx(browser, { width: 1100, height: 900 }, 1);
  await p.addInitScript(() => localStorage.setItem("tp-unlock:seating-chart", JSON.stringify({ o: "SAMPLE", t: 1, test: false })));
  await p.goto(BASE + "apps/seating/?demo=1");
  await p.evaluate(() => { const S = SeatingApp.state(); S.date = "2027-06-17"; SeatingApp.autoSeat(false); SeatingApp.render(); });
  await p.evaluate(() => document.querySelector("[data-act=pdf-clean]").click());
  await p.waitForSelector("#print-area .p-tables", { state: "attached" }); await p.waitForTimeout(700);
  await p.evaluate(() => {
    const b = document.createElement("p");
    b.style.cssText = "margin:0 0 10px;padding:6px 10px;border:1px dashed #0e6b63;color:#0e6b63;font:600 12px Assistant,Arial,sans-serif;text-align:center";
    b.textContent = "קובץ לדוגמה (שמות בדויים) · כך נראה PDF נקי מהגרסה המלאה של כלי סידורי ההושבה · tichnun.netlify.app/apps/seating";
    document.getElementById("print-area").prepend(b); document.body.classList.add("printing");
  });
  await p.emulateMedia({ media: "print" });
  await p.waitForTimeout(400);
  const pdf = path.join(SAMPLES, "seating-chart-sample.pdf");
  await p.pdf({ path: pdf, format: "A4", printBackground: true, margin: { top: "12mm", bottom: "12mm", left: "10mm", right: "10mm" } });
  await p.context().close();
  execFileSync("pdftoppm", ["-png", "-r", "110", "-f", "1", "-l", "1", "-singlefile", pdf, path.join(SCRATCH, "seating")]);
  toWebp(path.join(SCRATCH, "seating.png"), path.join(IMG, "seating-chart-sample.webp"), 900);

  // ---- invitation sample PNG (clean, fake names) ----
  p = await ctx(browser, { width: 1280, height: 900 }, 1);
  await p.addInitScript(() => { localStorage.setItem("tp-unlock:invitation-maker", JSON.stringify({ o: "SAMPLE", t: 1, test: false })); localStorage.removeItem("tp-invite-v1"); });
  await p.goto(BASE + "apps/invite/?t=w-olive");
  await p.waitForFunction(() => window.InviteApp && InviteApp.unlocked());
  await p.waitForTimeout(800);
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#dl-png")]);
  const rawInv = path.join(SCRATCH, "invite.png");
  await dl.saveAs(rawInv);
  await p.context().close();
  py("import sys;from PIL import Image;im=Image.open(sys.argv[1]).convert('RGB');w=1200;im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS);im.save(sys.argv[2],'PNG',optimize=True)",
    rawInv, path.join(SAMPLES, "invitation-sample.png"));
  toWebp(path.join(SAMPLES, "invitation-sample.png"), path.join(IMG, "invitation-sample.webp"), 700);

  // ---- mini budget xlsx preview (LibreOffice -> PDF -> PNG) ----
  try {
    execFileSync("soffice", ["--headless", "--convert-to", "pdf", "--outdir", SCRATCH, path.join(SAMPLES, "mini-wedding-budget.xlsx")], { stdio: "ignore" });
    execFileSync("pdftoppm", ["-png", "-r", "120", "-f", "1", "-l", "1", "-singlefile", path.join(SCRATCH, "mini-wedding-budget.pdf"), path.join(SCRATCH, "budget")]);
    py("import sys;from PIL import Image,ImageChops;im=Image.open(sys.argv[1]).convert('RGB');bg=Image.new('RGB',im.size,(255,255,255));" +
      "b=ImageChops.difference(im,bg).getbbox();im=im.crop((max(0,b[0]-20),max(0,b[1]-20),min(im.width,b[2]+20),min(im.height,b[3]+20)));im.save(sys.argv[1])",
      path.join(SCRATCH, "budget.png"));
    toWebp(path.join(SCRATCH, "budget.png"), path.join(IMG, "mini-wedding-budget.webp"), 900);
  } catch (e) { console.warn("budget preview skipped:", e.message); }

  // ---- RSVP app screenshots at 2x ----
  p = await ctx(browser, { width: 1280, height: 860 }, 2);
  await p.goto(BASE + "apps/rsvp/?demo=1");
  await p.waitForTimeout(500); await hideChrome(p);
  await p.evaluate(() => window.scrollTo(0, document.getElementById("app").offsetTop - 8));
  await p.screenshot({ path: path.join(RS, "screen-1.png") });
  await p.context().close();
  p = await ctx(browser, { width: 390, height: 844 }, 2);
  await p.goto(BASE + "apps/rsvp/?demo=1");
  await p.waitForTimeout(500); await hideChrome(p);
  await p.evaluate(() => document.getElementById("app").scrollIntoView());
  await p.screenshot({ path: path.join(RS, "screen-2.png") });
  await p.context().close();
  ["screen-1", "screen-2"].forEach(n => toWebp(path.join(RS, n + ".png"), null, n === "screen-1" ? 1600 : 0));

  await browser.close(); server.close();
  fs.rmSync(SCRATCH, { recursive: true, force: true });
  console.log("samples + previews written");
})().catch(e => { console.error(e); process.exit(1); });
