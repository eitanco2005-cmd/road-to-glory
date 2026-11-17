/* תכנון פלוס — tiny ZIP writer/reader + XLSX/DOCX helpers for the web apps (no dependencies).
 *   AppZip.write([{name, data: string|Uint8Array}]) -> Blob (stored entries, valid for .xlsx/.docx)
 *   AppZip.read(arrayBuffer) -> Promise<{name: Uint8Array}> (stored or deflate via DecompressionStream)
 *   AppZip.xlsx({sheets:[{name, rows:[[cell]], cols:[widths], rtl:true, bold:[rowIdx]}]}) -> Blob
 *   AppZip.readSheet(arrayBuffer) -> Promise<rows[][]>   (first sheet, strings/numbers)
 *   AppZip.download(blob, filename)
 */
(function () {
  "use strict";
  var enc = new TextEncoder();
  var CRC = (function () {
    var t = new Uint32Array(256);
    for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; }
    return t;
  })();
  function crc32(b) { var c = 0xffffffff; for (var i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
  function u16(v) { return [v & 255, (v >>> 8) & 255]; }
  function u32(v) { return [v & 255, (v >>> 8) & 255, (v >>> 16) & 255, (v >>> 24) & 255]; }

  function write(files) {
    var parts = [], central = [], offset = 0;
    var d = new Date(), time = (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1);
    var date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    files.forEach(function (f) {
      var name = enc.encode(f.name);
      var data = typeof f.data === "string" ? enc.encode(f.data) : f.data;
      var crc = crc32(data);
      var head = [].concat([0x50, 0x4b, 3, 4], u16(20), u16(0x0800), u16(0), u16(time), u16(date), u32(crc), u32(data.length), u32(data.length), u16(name.length), u16(0));
      parts.push(new Uint8Array(head), name, data);
      central.push(new Uint8Array([].concat([0x50, 0x4b, 1, 2], u16(20), u16(20), u16(0x0800), u16(0), u16(time), u16(date), u32(crc), u32(data.length), u32(data.length), u16(name.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(offset))), name);
      offset += head.length + name.length + data.length;
    });
    var cdSize = central.reduce(function (s, p) { return s + p.length; }, 0);
    var end = new Uint8Array([].concat([0x50, 0x4b, 5, 6], u16(0), u16(0), u16(files.length), u16(files.length), u32(cdSize), u32(offset), u16(0)));
    return new Blob(parts.concat(central, [end]), { type: "application/zip" });
  }

  function inflate(bytes) {
    if (typeof DecompressionStream === "undefined") return Promise.reject(new Error("no DecompressionStream"));
    var ds = new DecompressionStream("deflate-raw");
    var stream = new Blob([bytes]).stream().pipeThrough(ds);
    return new Response(stream).arrayBuffer().then(function (b) { return new Uint8Array(b); });
  }
  function read(buf) {
    var b = new Uint8Array(buf), v = new DataView(buf);
    var e = b.length - 22;
    while (e >= 0 && v.getUint32(e, true) !== 0x06054b50) e--;
    if (e < 0) return Promise.reject(new Error("not a zip"));
    var count = v.getUint16(e + 10, true), p = v.getUint32(e + 16, true), out = {}, jobs = [];
    var dec = new TextDecoder();
    for (var i = 0; i < count; i++) {
      if (v.getUint32(p, true) !== 0x02014b50) break;
      var method = v.getUint16(p + 10, true), csize = v.getUint32(p + 20, true);
      var nlen = v.getUint16(p + 28, true), xlen = v.getUint16(p + 30, true), clen = v.getUint16(p + 32, true);
      var lho = v.getUint32(p + 42, true);
      var name = dec.decode(b.subarray(p + 46, p + 46 + nlen));
      var start = lho + 30 + v.getUint16(lho + 26, true) + v.getUint16(lho + 28, true);
      var data = b.subarray(start, start + csize);
      (function (name, method, data) {
        if (method === 0) out[name] = data;
        else if (method === 8) jobs.push(inflate(data).then(function (r) { out[name] = r; }));
      })(name, method, data);
      p += 46 + nlen + xlen + clen;
    }
    return Promise.all(jobs).then(function () { return out; });
  }

  function x(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, ""); }
  function colName(i) { var s = ""; i++; while (i > 0) { var m = (i - 1) % 26; s = String.fromCharCode(65 + m) + s; i = Math.floor((i - 1) / 26); } return s; }

  /* Minimal styled XLSX: style 0 normal, 1 bold header (filled), 2 bold title, 3 wrap */
  function xlsx(book) {
    var sheets = book.sheets;
    var files = [];
    var ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>';
    sheets.forEach(function (s, i) { ct += '<Override PartName="/xl/worksheets/sheet' + (i + 1) + '.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'; });
    ct += "</Types>";
    files.push({ name: "[Content_Types].xml", data: ct });
    files.push({ name: "_rels/.rels", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>' });
    var wb = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView/></bookViews><sheets>';
    var rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">';
    sheets.forEach(function (s, i) {
      var nm = String(s.name || "Sheet" + (i + 1)).replace(/[\\\/\?\*\[\]:]/g, " ").slice(0, 31);
      wb += '<sheet name="' + x(nm) + '" sheetId="' + (i + 1) + '" r:id="rId' + (i + 1) + '"/>';
      rels += '<Relationship Id="rId' + (i + 1) + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet' + (i + 1) + '.xml"/>';
      var ws = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"' + (s.rtl === false ? "" : ' rightToLeft="1"') + (i === 0 ? ' tabSelected="1"' : "") + '>' + (s.freeze ? '<pane ySplit="' + s.freeze + '" topLeftCell="A' + (s.freeze + 1) + '" activePane="bottomLeft" state="frozen"/>' : "") + '</sheetView></sheetViews>';
      if (s.cols && s.cols.length) {
        ws += "<cols>" + s.cols.map(function (w, c) { return '<col min="' + (c + 1) + '" max="' + (c + 1) + '" width="' + w + '" customWidth="1"/>'; }).join("") + "</cols>";
      }
      ws += "<sheetData>";
      (s.rows || []).forEach(function (row, r) {
        var st = (s.header || []).indexOf(r) >= 0 ? 1 : (s.title || []).indexOf(r) >= 0 ? 2 : 0;
        ws += '<row r="' + (r + 1) + '">';
        row.forEach(function (cell, c) {
          if (cell === null || cell === undefined || cell === "") return;
          var ref = colName(c) + (r + 1);
          if (typeof cell === "number" && isFinite(cell)) ws += '<c r="' + ref + '"' + (st ? ' s="' + st + '"' : "") + "><v>" + cell + "</v></c>";
          else ws += '<c r="' + ref + '" t="inlineStr"' + (st ? ' s="' + st + '"' : "") + "><is><t xml:space=\"preserve\">" + x(cell) + "</t></is></c>";
        });
        ws += "</row>";
      });
      ws += "</sheetData>";
      if (s.autoFilter && s.rows && s.rows.length > 1) ws += '<autoFilter ref="A' + (s.autoFilter) + ":" + colName(s.rows[s.autoFilter - 1].length - 1) + s.rows.length + '"/>';
      ws += '<pageMargins left="0.5" right="0.5" top="0.6" bottom="0.6" header="0.3" footer="0.3"/><pageSetup paperSize="9" orientation="portrait"/></worksheet>';
      files.push({ name: "xl/worksheets/sheet" + (i + 1) + ".xml", data: ws });
    });
    wb += "</sheets></workbook>";
    rels += '<Relationship Id="rId' + (sheets.length + 1) + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>';
    files.push({ name: "xl/workbook.xml", data: wb });
    files.push({ name: "xl/_rels/workbook.xml.rels", data: rels });
    files.push({ name: "xl/styles.xml", data: '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="3"><font><sz val="11"/><name val="Arial"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Arial"/></font><font><b/><sz val="14"/><name val="Arial"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0E6B63"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/><xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>' });
    var blob = write(files);
    return new Blob([blob], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
  }

  function readSheet(buf) {
    return read(buf).then(function (z) {
      var dec = new TextDecoder();
      var parse = function (s) { return new DOMParser().parseFromString(s, "application/xml"); };
      var shared = [];
      if (z["xl/sharedStrings.xml"]) {
        var sd = parse(dec.decode(z["xl/sharedStrings.xml"]));
        var sis = sd.getElementsByTagName("si");
        for (var i = 0; i < sis.length; i++) {
          var ts = sis[i].getElementsByTagName("t"), txt = "";
          for (var j = 0; j < ts.length; j++) txt += ts[j].textContent;
          shared.push(txt);
        }
      }
      var sheetName = Object.keys(z).filter(function (n) { return /^xl\/worksheets\/sheet\d+\.xml$/.test(n); }).sort(function (a, b) {
        return parseInt(a.match(/\d+/)[0], 10) - parseInt(b.match(/\d+/)[0], 10);
      })[0];
      if (!sheetName) throw new Error("no sheet");
      var doc = parse(dec.decode(z[sheetName]));
      var rows = [];
      var rs = doc.getElementsByTagName("row");
      for (var r = 0; r < rs.length; r++) {
        var cells = rs[r].getElementsByTagName("c"), row = [];
        for (var c = 0; c < cells.length; c++) {
          var cell = cells[c], ref = cell.getAttribute("r") || "", t = cell.getAttribute("t");
          var col = 0, m = /^([A-Z]+)/.exec(ref);
          if (m) { for (var k = 0; k < m[1].length; k++) col = col * 26 + (m[1].charCodeAt(k) - 64); col--; } else col = row.length;
          var vEl = cell.getElementsByTagName("v")[0], val = "";
          if (t === "s" && vEl) val = shared[parseInt(vEl.textContent, 10)] || "";
          else if (t === "inlineStr") { var tt = cell.getElementsByTagName("t"); for (var q = 0; q < tt.length; q++) val += tt[q].textContent; }
          else if (vEl) val = vEl.textContent;
          row[col] = val;
        }
        for (var f = 0; f < row.length; f++) if (row[f] === undefined) row[f] = "";
        rows.push(row);
      }
      return rows;
    });
  }

  function download(blob, filename) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }

  window.AppZip = { write: write, read: read, xlsx: xlsx, readSheet: readSheet, download: download, xmlEscape: x, crc32: crc32 };
})();
