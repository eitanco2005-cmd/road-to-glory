// Print HTML files to PDF with Chromium (vector output, fonts embedded as subsets).
//   node print_pdf.js in.html=out.pdf [in2.html=out2.pdf ...]
const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const job of process.argv.slice(2)) {
    const [src, dst] = job.split("=");
    await page.goto("file://" + src, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: dst, preferCSSPageSize: true, printBackground: true });
    console.log("pdf", dst);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
