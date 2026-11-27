// node shoot.js jobs.json  — jobs: [[html_path, png_path], ...] ; 1500x1125 @2x
const { chromium } = require("playwright");
const fs = require("fs");
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1500, height: 1125 }, deviceScaleFactor: 2 });
  for (const [h, out] of jobs) {
    await pg.goto("file://" + h, { waitUntil: "load" });
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(100);
    await pg.screenshot({ path: out, type: "png" });
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
