/* Minimal PDF writer for print exports: JPEG images (DCTDecode) placed on pages + optional crop marks.
 * No dependencies. Units in mm. window.TinyPDF.build(pages) -> Blob
 * pages: [{w, h, images:[{jpeg:Uint8Array, pw, ph, x, y, iw, ih}], marks:[[x1,y1,x2,y2], ...]}]   (x,y from top-left)
 */
(function () {
  "use strict";
  var PT = 72 / 25.4;
  function n(v) { return (Math.round(v * 1000) / 1000).toString(); }
  function build(pages, meta) {
    var enc = new TextEncoder();
    var chunks = [], offsets = [], len = 0, objCount = 0;
    function push(data) { var b = typeof data === "string" ? enc.encode(data) : data; chunks.push(b); len += b.length; }
    function obj(id, body, stream) {
      offsets[id] = len;
      push(id + " 0 obj\n");
      if (stream) {
        push(body.replace("%LEN%", stream.length) + "\nstream\n"); push(stream); push("\nendstream\nendobj\n");
      } else push(body + "\nendobj\n");
    }
    // ids: 1 catalog, 2 pages, 3 info, then per unique image, then per page (page + content)
    var images = [];
    pages.forEach(function (p) { p.images.forEach(function (im) { if (images.indexOf(im.jpeg) < 0) images.push(im.jpeg); }); });
    var imgMeta = [];
    pages.forEach(function (p) { p.images.forEach(function (im) { imgMeta[images.indexOf(im.jpeg)] = im; }); });
    var next = 4;
    var imgIds = images.map(function () { return next++; });
    var pageIds = pages.map(function () { var a = next; next += 2; return a; });
    objCount = next - 1;

    push("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n");
    obj(1, "<< /Type /Catalog /Pages 2 0 R >>");
    obj(2, "<< /Type /Pages /Count " + pages.length + " /Kids [" + pageIds.map(function (id) { return id + " 0 R"; }).join(" ") + "] >>");
    var title = (meta && meta.title) || "Invitation";
    obj(3, "<< /Producer (tichnun.netlify.app) /Title (" + title.replace(/[()\\]/g, "") + ") >>");
    images.forEach(function (jpeg, i) {
      var m = imgMeta[i];
      obj(imgIds[i], "<< /Type /XObject /Subtype /Image /Width " + m.pw + " /Height " + m.ph +
        " /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length %LEN% >>", jpeg);
    });
    pages.forEach(function (p, i) {
      var id = pageIds[i], H = p.h * PT;
      var cs = "";
      p.images.forEach(function (im) {
        var k = images.indexOf(im.jpeg);
        cs += "q " + n(im.iw * PT) + " 0 0 " + n(im.ih * PT) + " " + n(im.x * PT) + " " + n(H - (im.y + im.ih) * PT) + " cm /Im" + k + " Do Q\n";
      });
      if (p.marks && p.marks.length) {
        cs += "q 0 0 0 RG 0.3 w\n";
        p.marks.forEach(function (m) { cs += n(m[0] * PT) + " " + n(H - m[1] * PT) + " m " + n(m[2] * PT) + " " + n(H - m[3] * PT) + " l S\n"; });
        cs += "Q\n";
      }
      var xo = images.map(function (_, k) { return "/Im" + k + " " + imgIds[k] + " 0 R"; }).join(" ");
      obj(id, "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 " + n(p.w * PT) + " " + n(H) + "] /Resources << /XObject << " + xo +
        " >> >> /Contents " + (id + 1) + " 0 R >>");
      var csb = enc.encode(cs);
      obj(id + 1, "<< /Length %LEN% >>", csb);
    });
    var xref = len;
    var x = "xref\n0 " + (objCount + 1) + "\n0000000000 65535 f \n";
    for (var i = 1; i <= objCount; i++) x += ("0000000000" + offsets[i]).slice(-10) + " 00000 n \n";
    push(x + "trailer\n<< /Size " + (objCount + 1) + " /Root 1 0 R /Info 3 0 R >>\nstartxref\n" + xref + "\n%%EOF\n");
    return new Blob(chunks, { type: "application/pdf" });
  }
  /* crop marks around a rectangle (mm), outside it */
  function cropMarks(x, y, w, h, len, gap) {
    len = len || 5; gap = gap || 2;
    var m = [];
    [[x, y], [x + w, y], [x, y + h], [x + w, y + h]].forEach(function (c, i) {
      var sx = i % 2 ? 1 : -1, sy = i < 2 ? -1 : 1;
      m.push([c[0] + sx * gap, c[1], c[0] + sx * (gap + len), c[1]]);
      m.push([c[0], c[1] + sy * gap, c[0], c[1] + sy * (gap + len)]);
    });
    return m;
  }
  window.TinyPDF = { build: build, cropMarks: cropMarks };
})();
