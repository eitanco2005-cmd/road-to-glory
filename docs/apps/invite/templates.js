/* תכנון פלוס — invitation templates + canvas renderer.
 * 12 original designs drawn with the Canvas 2D API (no images, no third-party art).
 * Coordinate space: 1000 x 1414 units (A-series ratio 1:√2). B = bleed in units (0 on screen).
 * window.Invite = { W, H, FONTS, CATS, TEMPLATES, byId, render(canvas, state, opts), composeDate }
 */
(function () {
  "use strict";
  var W = 1000, H = 1414;

  /* Free OFL Hebrew fonts from Google Fonts (all support Hebrew). */
  var FONTS = [
    { id: "Frank Ruhl Libre", label: "פרנק רוהל (קלאסי)", w: [400, 700] },
    { id: "David Libre", label: "דוד (ספרותי)", w: [400, 700] },
    { id: "Bellefair", label: "בלפייר (אלגנטי)", w: [400] },
    { id: "Noto Rashi Hebrew", label: "כתב רש״י", w: [400, 700] },
    { id: "Suez One", label: "סואץ (מודגש)", w: [400] },
    { id: "Secular One", label: "סקולר (מודרני)", w: [400] },
    { id: "Karantina", label: "קרנטינה (צר)", w: [400, 700] },
    { id: "Amatic SC", label: "אמטיק (כתב יד)", w: [400, 700] },
    { id: "Varela Round", label: "ורלה (עגול)", w: [400] },
    { id: "Rubik", label: "רוביק (נקי)", w: [400, 700] },
    { id: "Heebo", label: "היבו (נקי)", w: [400, 700] },
    { id: "Assistant", label: "אסיסטנט (קריא)", w: [400, 700] }
  ];
  function fontWeight(family, want) {
    for (var i = 0; i < FONTS.length; i++) if (FONTS[i].id === family) {
      var ws = FONTS[i].w;
      return ws.indexOf(want) >= 0 ? want : ws[ws.length - 1] >= want ? ws[ws.length - 1] : ws[0];
    }
    return want;
  }

  var CATS = {
    wedding: { label: "חתונה" },
    mitzvah: { label: "בר / בת מצווה" },
    party: { label: "יום הולדת וברית" }
  };

  /* Default texts per category (fictional names). Templates may override with `preset`. */
  var DEFAULTS = {
    wedding: {
      top: "בשמחה ובהודיה לה׳", title: "", names: "נועה ואיתי",
      invite: "אנו שמחים להזמינכם להשתתף\nבשמחת נישואינו",
      times: "קבלת פנים 19:30 · חופה וקידושין 20:30",
      venue: "גן האירועים \"השקד\"", address: "דרך הגפן 12, מושב לדוגמה",
      parentsR: "הורי הכלה\nרחל ודוד כהן", parentsL: "הורי החתן\nמיכל ויוסי לוי", footer: ""
    },
    mitzvah: {
      top: "בשמחה רבה", title: "בר מצווה", names: "יונתן",
      invite: "אנו שמחים להזמינכם לחגוג איתנו\nאת הגיעו של בננו למצוות",
      times: "קבלת פנים 19:00 · ארוחה 20:00",
      venue: "אולם \"הגפן\"", address: "רחוב התאנה 5, עיר לדוגמה",
      parentsR: "באהבה, ההורים שירה ועמית ברק\nוהאחים מאיה ואורי", parentsL: "", footer: ""
    },
    party: {
      top: "בואו לחגוג!", title: "יום הולדת 6", names: "ליה",
      invite: "מסיבת יום הולדת עם הפעלה,\nעוגה והמון כיף",
      times: "16:30–18:30",
      venue: "בגינה של סבא וסבתא", address: "רחוב הרימון 8, עיר לדוגמה",
      parentsR: "מחכים לכם! משפחת אלון", parentsL: "", footer: "אישור הגעה: 050-0000000"
    }
  };
  var DEFAULT_DATES = { wedding: "2027-06-10", mitzvah: "2027-03-18", party: "2027-01-22" };

  /* ---------- seeded random (stable decorations) ---------- */
  function rng(seed) {
    var s = seed >>> 0 || 1;
    return function () { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; };
  }

  /* ---------- drawing helpers ---------- */
  function bg(ctx, B, fill) { ctx.fillStyle = fill; ctx.fillRect(-B, -B, W + 2 * B, H + 2 * B); }
  function gold(ctx, x0, y0, x1, y1, base) {
    var g = ctx.createLinearGradient(x0, y0, x1, y1);
    base = base || ["#a8781f", "#f3dc9b", "#b98a2c", "#e9c873", "#9c6f1c"];
    base.forEach(function (c, i) { g.addColorStop(i / (base.length - 1), c); });
    return g;
  }
  function leaf(ctx, x, y, len, ang, wid) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
    ctx.beginPath(); ctx.moveTo(0, 0);
    ctx.quadraticCurveTo(len * 0.5, -wid, len, 0);
    ctx.quadraticCurveTo(len * 0.5, wid, 0, 0);
    ctx.fill(); ctx.restore();
  }
  /* curved stem with alternating leaves; returns nothing */
  function branch(ctx, x, y, len, ang, n, leafLen, color, curve, opts) {
    opts = opts || {};
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
    ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineCap = "round";
    ctx.lineWidth = opts.stem || Math.max(2, len * 0.01);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(len / 2, -len * curve, len, 0); ctx.stroke();
    for (var i = 1; i <= n; i++) {
      var t = i / (n + 1);
      var px = t * len, py = 2 * (1 - t) * t * (-len * curve);
      var tan = Math.atan2(-2 * len * curve * (1 - 2 * t), len);
      var side = i % 2 ? 1 : -1;
      var l = leafLen * (1 - t * 0.35);
      leaf(ctx, px, py, l, tan + side * (opts.spread || 0.75), l * (opts.wide || 0.28));
      if (opts.berry && i % 3 === 0) {
        ctx.save(); ctx.fillStyle = opts.berry;
        ctx.beginPath(); ctx.ellipse(px + Math.cos(tan - side * 0.9) * l * 0.35, py + Math.sin(tan - side * 0.9) * l * 0.35, l * 0.13, l * 0.18, tan, 0, 7); ctx.fill();
        ctx.restore();
      }
    }
    leaf(ctx, len, 0, leafLen * 0.7, -curve * 0.6, leafLen * 0.7 * (opts.wide || 0.28));
    ctx.restore();
  }
  function mirror4(ctx, fn) { // run fn in the 4 corners (top-right is the reference)
    [[1, 1, 0, 0], [-1, 1, W, 0], [1, -1, 0, H], [-1, -1, W, H]].forEach(function (m) {
      ctx.save(); ctx.translate(m[2], m[3]); ctx.scale(m[0], m[1]); fn(); ctx.restore();
    });
  }
  function mirrorX(ctx, fn) {
    [[1, 0], [-1, W]].forEach(function (m) { ctx.save(); ctx.translate(m[1], 0); ctx.scale(m[0], 1); fn(); ctx.restore(); });
  }
  function sparkle(ctx, x, y, r) {
    ctx.beginPath();
    for (var i = 0; i < 8; i++) {
      var a = i * Math.PI / 4 - Math.PI / 2, rr = i % 2 ? r * 0.22 : r;
      ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
    }
    ctx.closePath(); ctx.fill();
  }
  function starOfDavid(ctx, x, y, r) {
    for (var k = 0; k < 2; k++) {
      ctx.beginPath();
      for (var i = 0; i < 3; i++) {
        var a = -Math.PI / 2 + k * Math.PI + i * 2 * Math.PI / 3;
        ctx.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r);
      }
      ctx.closePath(); ctx.stroke();
    }
  }
  function flower(ctx, x, y, r, petal, center, n) {
    n = n || 5;
    ctx.fillStyle = petal;
    for (var i = 0; i < n; i++) {
      var a = i * 2 * Math.PI / n;
      ctx.beginPath(); ctx.ellipse(x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55, r * 0.5, r * 0.36, a, 0, 7); ctx.fill();
    }
    ctx.fillStyle = center; ctx.beginPath(); ctx.arc(x, y, r * 0.26, 0, 7); ctx.fill();
  }
  function blob(ctx, x, y, r, color, alpha) {
    var g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, hexA(color, alpha)); g.addColorStop(0.6, hexA(color, alpha * 0.55)); g.addColorStop(1, hexA(color, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
  }
  function hexA(hex, a) {
    var m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex);
    if (!m) return hex;
    return "rgba(" + parseInt(m[1], 16) + "," + parseInt(m[2], 16) + "," + parseInt(m[3], 16) + "," + a + ")";
  }
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function divider(ctx, P, y, w, kind) {
    var cx = W / 2;
    ctx.save(); ctx.strokeStyle = P.accent; ctx.fillStyle = P.accent; ctx.lineWidth = 2;
    if (kind === "diamond") {
      ctx.beginPath(); ctx.moveTo(cx - w / 2, y); ctx.lineTo(cx - 14, y); ctx.moveTo(cx + 14, y); ctx.lineTo(cx + w / 2, y); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(cx, y - 8); ctx.lineTo(cx + 8, y); ctx.lineTo(cx, y + 8); ctx.lineTo(cx - 8, y); ctx.closePath(); ctx.fill();
    } else if (kind === "dots") {
      for (var i = -2; i <= 2; i++) { ctx.beginPath(); ctx.arc(cx + i * 22, y, i === 0 ? 5 : 3, 0, 7); ctx.fill(); }
    } else if (kind === "star") {
      ctx.beginPath(); ctx.moveTo(cx - w / 2, y); ctx.lineTo(cx - 24, y); ctx.moveTo(cx + 24, y); ctx.lineTo(cx + w / 2, y); ctx.stroke();
      ctx.lineWidth = 2.5; starOfDavid(ctx, cx, y, 14);
    } else if (kind === "sparkle") {
      sparkle(ctx, cx, y, 14); sparkle(ctx, cx - 40, y, 7); sparkle(ctx, cx + 40, y, 7);
    } else if (kind === "leaf") {
      ctx.beginPath(); ctx.moveTo(cx - w / 2, y); ctx.lineTo(cx - 30, y); ctx.moveTo(cx + 30, y); ctx.lineTo(cx + w / 2, y); ctx.stroke();
      leaf(ctx, cx, y, 26, -2.6, 8); leaf(ctx, cx, y, 26, -0.55, 8);
    } else {
      ctx.beginPath(); ctx.moveTo(cx - w / 2, y); ctx.lineTo(cx + w / 2, y); ctx.stroke();
    }
    ctx.restore();
  }

  /* ---------- the 12 templates ---------- */
  var T = [];

  /* 1. Classic gold frame */
  T.push({
    id: "w-classic", cat: "wedding", name: "קלאסי זהב",
    fonts: { display: "Frank Ruhl Libre", body: "Frank Ruhl Libre" },
    palettes: [
      { bg: "#fbf6ec", ink: "#3b3226", accent: "#9a6d1e", soft: "#7d6b4f", goldy: true },
      { bg: "#ffffff", ink: "#2a2a2a", accent: "#8a6a2a", soft: "#6b6253", goldy: true },
      { bg: "#f3f0ea", ink: "#2f3b36", accent: "#3f6b5c", soft: "#5f6f69" }
    ],
    box: [170, 200, 830, 1230], div: "diamond",
    sizes: { top: 34, title: 60, names: 112, invite: 36, date: 38, greg: 30, times: 32, venue: 40, address: 28, parents: 28, footer: 26 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var g = P.goldy ? gold(ctx, 0, 0, W, H) : P.accent;
      ctx.strokeStyle = g; ctx.fillStyle = g;
      ctx.lineWidth = 6; ctx.strokeRect(60, 60, W - 120, H - 120);
      ctx.lineWidth = 2; ctx.strokeRect(84, 84, W - 168, H - 168);
      mirror4(ctx, function () {
        ctx.lineWidth = 3; ctx.beginPath();
        ctx.moveTo(84, 230); ctx.bezierCurveTo(150, 220, 170, 160, 130, 135);
        ctx.bezierCurveTo(100, 115, 80, 150, 110, 165);
        ctx.moveTo(230, 84); ctx.bezierCurveTo(220, 150, 160, 170, 135, 130);
        ctx.bezierCurveTo(115, 100, 150, 80, 165, 110);
        ctx.stroke();
        ctx.beginPath(); ctx.arc(150, 150, 9, 0, 7); ctx.fill();
        leaf(ctx, 160, 160, 60, 0.78, 14);
      });
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(W / 2 - 90, 140); ctx.lineTo(W / 2 + 90, 140); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(W / 2 - 90, H - 140); ctx.lineTo(W / 2 + 90, H - 140); ctx.stroke();
      sparkle(ctx, W / 2, 140, 16); sparkle(ctx, W / 2, H - 140, 16);
    }
  });

  /* 2. Olive branches */
  T.push({
    id: "w-olive", cat: "wedding", name: "ענפי זית",
    fonts: { display: "David Libre", body: "David Libre" },
    palettes: [
      { bg: "#f7f5ee", ink: "#2f3a2c", accent: "#5d7148", soft: "#6f7a64", leaf: "#7f9068", berry: "#4b5a3a" },
      { bg: "#fffdf8", ink: "#34392f", accent: "#7a6a3c", soft: "#7a7563", leaf: "#9aa680", berry: "#6a6040" },
      { bg: "#eef1ea", ink: "#26322a", accent: "#2f5a46", soft: "#4f6458", leaf: "#5f8a70", berry: "#2f5a46" }
    ],
    box: [150, 300, 850, 1150], div: "leaf",
    sizes: { top: 32, title: 56, names: 104, invite: 34, date: 36, greg: 30, times: 31, venue: 38, address: 27, parents: 27, footer: 25 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      ctx.globalAlpha = 0.9;
      branch(ctx, W / 2 - 10, 250, 330, Math.PI + 0.18, 9, 70, P.leaf, 0.18, { berry: P.berry });
      branch(ctx, W / 2 + 10, 250, 330, -0.18, 9, 70, P.leaf, 0.18, { berry: P.berry });
      branch(ctx, W / 2 - 10, H - 210, 260, Math.PI - 0.12, 7, 58, P.leaf, -0.15, { berry: P.berry });
      branch(ctx, W / 2 + 10, H - 210, 260, 0.12, 7, 58, P.leaf, -0.15, { berry: P.berry });
      ctx.globalAlpha = 1;
      ctx.strokeStyle = P.leaf; ctx.lineWidth = 1.5;
      roundRect(ctx, 70, 70, W - 140, H - 140, 26); ctx.stroke();
    }
  });

  /* 3. Boho arch */
  T.push({
    id: "w-arch", cat: "wedding", name: "קשת בוהו",
    fonts: { display: "Suez One", body: "Assistant" },
    palettes: [
      { bg: "#efe2d3", panel: "#fbf6ef", ink: "#4a2f22", accent: "#b0603b", soft: "#8a6a58", leaf: "#c99a6b" },
      { bg: "#e7e4dc", panel: "#fbfaf6", ink: "#3c3a33", accent: "#7c6a4a", soft: "#7d776a", leaf: "#b5a585" },
      { bg: "#e9d6d3", panel: "#fdf7f5", ink: "#4a2a2e", accent: "#a2475a", soft: "#866068", leaf: "#d39aa5" }
    ],
    box: [200, 330, 800, 1220], div: "dots",
    sizes: { top: 30, title: 52, names: 100, invite: 32, date: 34, greg: 28, times: 30, venue: 36, address: 26, parents: 26, footer: 24 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var r = rng(7);
      for (var i = 0; i < 6; i++) blob(ctx, r() * W, r() * H, 300 + r() * 200, P.leaf, 0.18);
      ctx.fillStyle = P.panel;
      ctx.beginPath(); ctx.moveTo(130, H - 110); ctx.lineTo(130, 480); ctx.arc(W / 2, 480, W / 2 - 130, Math.PI, 0); ctx.lineTo(W - 130, H - 110); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = P.accent; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(155, H - 135); ctx.lineTo(155, 480); ctx.arc(W / 2, 480, W / 2 - 155, Math.PI, 0); ctx.lineTo(W - 155, H - 135); ctx.closePath(); ctx.stroke();
      // pampas / dried leaves on the arch shoulders
      mirrorX(ctx, function () {
        ctx.save(); ctx.globalAlpha = 0.85;
        branch(ctx, 120, 470, 240, -1.25, 10, 46, P.leaf, 0.12, { spread: 0.5, wide: 0.22 });
        branch(ctx, 150, 520, 200, -0.85, 8, 40, P.accent, 0.1, { spread: 0.55, wide: 0.22 });
        ctx.restore();
      });
    }
  });

  /* 4. Gilded night */
  T.push({
    id: "w-night", cat: "wedding", name: "לילה מוזהב",
    fonts: { display: "Bellefair", body: "Assistant" },
    palettes: [
      { bg: "#14213d", bg2: "#1d2f55", ink: "#f4ecd8", accent: "#e2c47a", soft: "#c8bfa8", goldy: true },
      { bg: "#1f2a24", bg2: "#2c3b33", ink: "#efe9da", accent: "#d9be82", soft: "#c2bba8", goldy: true },
      { bg: "#2b1630", bg2: "#3d2244", ink: "#f6e9f0", accent: "#e8c3a0", soft: "#cbb6c3" }
    ],
    box: [160, 330, 840, 1180], div: "sparkle",
    sizes: { top: 32, title: 56, names: 118, invite: 34, date: 36, greg: 30, times: 31, venue: 38, address: 27, parents: 27, footer: 25 },
    decor: function (ctx, P, B) {
      var g = ctx.createLinearGradient(0, -B, 0, H + B); g.addColorStop(0, P.bg2); g.addColorStop(1, P.bg);
      bg(ctx, B, g);
      var r = rng(42);
      ctx.fillStyle = hexA(P.accent, 0.8);
      for (var i = 0; i < 70; i++) {
        var x = r() * W, y = r() * H;
        if (x > 140 && x < W - 140 && y > 300 && y < H - 200) continue;
        sparkle(ctx, x, y, 3 + r() * 9);
      }
      var ac = P.goldy ? gold(ctx, 0, 0, W, 300) : P.accent;
      ctx.strokeStyle = ac; ctx.fillStyle = ac; ctx.lineWidth = 2;
      // art-deco fan
      for (var k = 0; k < 4; k++) { ctx.beginPath(); ctx.arc(W / 2, 290, 60 + k * 38, Math.PI, 0); ctx.stroke(); }
      for (var j = 0; j <= 12; j++) {
        var a = Math.PI + j * Math.PI / 12;
        ctx.beginPath(); ctx.moveTo(W / 2 + Math.cos(a) * 60, 290 + Math.sin(a) * 60); ctx.lineTo(W / 2 + Math.cos(a) * 174, 290 + Math.sin(a) * 174); ctx.stroke();
      }
      ctx.beginPath(); ctx.moveTo(110, 290); ctx.lineTo(W - 110, 290); ctx.stroke();
      ctx.lineWidth = 3; ctx.strokeRect(70, 70, W - 140, H - 140);
      ctx.lineWidth = 1.2; ctx.strokeRect(90, 90, W - 180, H - 180);
      mirror4(ctx, function () {
        ctx.beginPath(); ctx.moveTo(90, 150); ctx.lineTo(150, 90); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(90, 180); ctx.lineTo(180, 90); ctx.stroke();
      });
      ctx.beginPath(); ctx.moveTo(W / 2 - 120, H - 150); ctx.lineTo(W / 2 + 120, H - 150); ctx.stroke();
      sparkle(ctx, W / 2, H - 150, 14);
    }
  });

  /* 5. Blush watercolour */
  T.push({
    id: "w-blush", cat: "wedding", name: "אקוורל ורוד",
    fonts: { display: "Noto Rashi Hebrew", body: "Assistant" },
    palettes: [
      { bg: "#fffaf8", ink: "#4b3a3c", accent: "#b25b6e", soft: "#8c7376", wash: ["#f2b8c0", "#f7d4c4", "#c9d8c0"] },
      { bg: "#fbfcff", ink: "#33384a", accent: "#5568a8", soft: "#6f7488", wash: ["#b9c8f0", "#e0d4f2", "#c7e3e8"] },
      { bg: "#fffcf5", ink: "#4a3f2c", accent: "#b07a2e", soft: "#867a62", wash: ["#f4d7a0", "#f2c5b0", "#d6e2b8"] }
    ],
    box: [150, 300, 850, 1170], div: "dots",
    sizes: { top: 32, title: 54, names: 106, invite: 34, date: 36, greg: 30, times: 31, venue: 38, address: 27, parents: 27, footer: 25 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var r = rng(11);
      var spots = [[0, 0], [W, 0], [0, H], [W, H], [W * 0.15, H * 0.12], [W * 0.88, H * 0.9]];
      spots.forEach(function (s, i) {
        for (var k = 0; k < 7; k++) blob(ctx, s[0] + (r() - 0.5) * 260, s[1] + (r() - 0.5) * 260, 120 + r() * 170, P.wash[(i + k) % 3], 0.45);
      });
      ctx.save(); ctx.globalAlpha = 0.85;
      [[70, 120, 0.5], [W - 70, H - 120, Math.PI + 0.5]].forEach(function (c) {
        for (var i = 0; i < 5; i++) {
          var a = c[2] + (i - 2) * 0.32;
          flower(ctx, c[0] + Math.cos(a) * (90 + i * 6), c[1] + Math.sin(a) * (90 + i * 6), 26 + (i % 2) * 10, hexA(P.accent, 0.55), hexA(P.ink, 0.5), 5);
        }
        ctx.fillStyle = hexA(P.wash[2] === "#c9d8c0" ? "#7f9a76" : P.soft, 0.7);
        for (var j = 0; j < 4; j++) leaf(ctx, c[0], c[1], 120, c[2] - 0.9 + j * 0.6, 26);
      });
      ctx.restore();
    }
  });

  /* 6. Tallit stripes */
  T.push({
    id: "m-tallit", cat: "mitzvah", name: "פסי טלית",
    fonts: { display: "Frank Ruhl Libre", body: "Heebo" },
    palettes: [
      { bg: "#ffffff", ink: "#1b2a44", accent: "#1d4e89", soft: "#55657d", stripe: "#1d4e89", stripe2: "#6f93c4" },
      { bg: "#fdfbf6", ink: "#222222", accent: "#222222", soft: "#5d5d5d", stripe: "#1f1f1f", stripe2: "#8a8a8a" },
      { bg: "#ffffff", ink: "#16353a", accent: "#0f6b73", soft: "#4f6a6d", stripe: "#0f6b73", stripe2: "#c09a3c" }
    ],
    box: [130, 330, 870, 1120], div: "star",
    sizes: { top: 32, title: 64, names: 120, invite: 34, date: 36, greg: 30, times: 31, venue: 38, address: 27, parents: 27, footer: 25 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      function band(y, dir) {
        ctx.fillStyle = P.stripe2; ctx.fillRect(-B, y, W + 2 * B, 10);
        ctx.fillStyle = P.stripe; ctx.fillRect(-B, y + dir * 24, W + 2 * B, 44 * dir);
        ctx.fillStyle = P.stripe2; ctx.fillRect(-B, y + dir * 80, W + 2 * B, 10);
        ctx.fillStyle = P.stripe; ctx.fillRect(-B, y + dir * 102, W + 2 * B, 14 * dir);
      }
      band(110, 1); band(H - 120, -1);
      // fringes (tzitzit-like) at the very edges
      ctx.strokeStyle = hexA(P.stripe, 0.35); ctx.lineWidth = 2;
      for (var x = -B; x < W + B; x += 14) {
        ctx.beginPath(); ctx.moveTo(x, -B); ctx.lineTo(x, 60); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x, H - 60); ctx.lineTo(x, H + B); ctx.stroke();
      }
      ctx.strokeStyle = P.accent; ctx.lineWidth = 3; starOfDavid(ctx, W / 2, 290, 40);
    }
  });

  /* 7. Jerusalem stone */
  T.push({
    id: "m-jerusalem", cat: "mitzvah", name: "אבן ירושלמית",
    fonts: { display: "Suez One", body: "Assistant" },
    palettes: [
      { bg: "#efe3cc", stone: "#e4d4b5", line: "#cdb88f", panel: "#fbf7ee", ink: "#3d3020", accent: "#8c5a1c", soft: "#6e604a" },
      { bg: "#e9e6df", stone: "#dcd7cc", line: "#bfb7a6", panel: "#fbfaf7", ink: "#2c2f36", accent: "#2c4f7c", soft: "#5c6370" },
      { bg: "#efe0d8", stone: "#e5d0c4", line: "#cfb2a1", panel: "#fdf8f5", ink: "#3a2a26", accent: "#7a3b2e", soft: "#6c5651" }
    ],
    box: [190, 360, 810, 1170], div: "star",
    sizes: { top: 30, title: 60, names: 110, invite: 32, date: 34, greg: 28, times: 30, venue: 36, address: 26, parents: 26, footer: 24 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var r = rng(5), rowH = 70;
      for (var y = -B, row = 0; y < H + B; y += rowH, row++) {
        var x = -B - (row % 2 ? 60 : 0);
        while (x < W + B) {
          var w = 120 + r() * 90;
          ctx.fillStyle = r() > 0.5 ? P.stone : P.bg;
          roundRect(ctx, x + 3, y + 3, w - 6, rowH - 6, 8); ctx.fill();
          ctx.strokeStyle = P.line; ctx.lineWidth = 1.5; ctx.stroke();
          x += w;
        }
      }
      // gate-shaped panel
      ctx.fillStyle = P.panel;
      ctx.beginPath(); ctx.moveTo(150, H - 120); ctx.lineTo(150, 420); ctx.quadraticCurveTo(150, 200, W / 2, 170); ctx.quadraticCurveTo(W - 150, 200, W - 150, 420); ctx.lineTo(W - 150, H - 120); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = P.accent; ctx.lineWidth = 3; ctx.stroke();
      ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(172, H - 142); ctx.lineTo(172, 422); ctx.quadraticCurveTo(172, 222, W / 2, 194); ctx.quadraticCurveTo(W - 172, 222, W - 172, 422); ctx.lineTo(W - 172, H - 142); ctx.closePath(); ctx.stroke();
      ctx.lineWidth = 2.5; starOfDavid(ctx, W / 2, 290, 34);
    }
  });

  /* 8. Pastel flowers (bat mitzvah) */
  T.push({
    id: "m-flowers", cat: "mitzvah", name: "פרחים בפסטל",
    fonts: { display: "Varela Round", body: "Varela Round" },
    palettes: [
      { bg: "#fff8fa", ink: "#4a3443", accent: "#c0507a", soft: "#8a6f80", petals: ["#f5b5c8", "#d9c2f0", "#ffd9a8"], center: "#f0c24b", leaf: "#9cc59a" },
      { bg: "#f8fbff", ink: "#2f3b55", accent: "#5a6fc0", soft: "#6c7690", petals: ["#bcd0f5", "#f3c6dd", "#cfe8d6"], center: "#f3d36b", leaf: "#8fbf9f" },
      { bg: "#fffdf6", ink: "#40392a", accent: "#c27a1a", soft: "#7e7560", petals: ["#ffd18a", "#f6b7a5", "#e3d6f5"], center: "#d98b2b", leaf: "#a3c48a" }
    ],
    box: [140, 330, 860, 1130], div: "dots",
    sizes: { top: 32, title: 60, names: 110, invite: 32, date: 34, greg: 28, times: 30, venue: 36, address: 26, parents: 26, footer: 24 },
    preset: { title: "בת מצווה", names: "תמר", invite: "אנו שמחים להזמינכם לחגוג איתנו\nאת הגיעה של בתנו למצוות", parentsR: "באהבה, ההורים שירה ועמית ברק\nוהאחים מאיה ואורי" },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var r = rng(23);
      function cluster(cx, cy, n, spread) {
        ctx.fillStyle = P.leaf;
        for (var i = 0; i < n; i++) leaf(ctx, cx + (r() - 0.5) * spread, cy + (r() - 0.5) * spread * 0.6, 50 + r() * 40, r() * 6.28, 13);
        for (var j = 0; j < n; j++) flower(ctx, cx + (r() - 0.5) * spread, cy + (r() - 0.5) * spread * 0.6, 26 + r() * 26, P.petals[j % 3], P.center, 5 + (j % 2));
      }
      cluster(W / 2, 90, 14, 900);
      cluster(W / 2, H - 80, 12, 860);
      cluster(40, H / 2, 4, 120); cluster(W - 40, H / 2 + 120, 4, 120);
    }
  });

  /* 9. Modern colour blocks */
  T.push({
    id: "m-modern", cat: "mitzvah", name: "מודרני צבעוני",
    fonts: { display: "Secular One", body: "Rubik" },
    palettes: [
      { bg: "#ffffff", ink: "#1e2b33", accent: "#0f7b74", soft: "#5a6870", c1: "#0f7b74", c2: "#f2b134", c3: "#ef6f53" },
      { bg: "#ffffff", ink: "#1d2140", accent: "#3b3fb6", soft: "#5c6079", c1: "#3b3fb6", c2: "#ff8fa3", c3: "#ffd166" },
      { bg: "#111827", ink: "#f9fafb", accent: "#fbbf24", soft: "#cbd5e1", c1: "#fbbf24", c2: "#38bdf8", c3: "#f472b6" }
    ],
    box: [130, 360, 870, 1150], div: "line",
    sizes: { top: 32, title: 70, names: 130, invite: 32, date: 34, greg: 28, times: 30, venue: 36, address: 26, parents: 26, footer: 24 },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      ctx.fillStyle = P.c1; ctx.beginPath(); ctx.moveTo(-B, -B); ctx.lineTo(W + B, -B); ctx.lineTo(W + B, 160); ctx.lineTo(-B, 300); ctx.closePath(); ctx.fill();
      ctx.fillStyle = P.c2; ctx.beginPath(); ctx.moveTo(-B, 300); ctx.lineTo(W * 0.45, 258); ctx.lineTo(-B, 360); ctx.closePath(); ctx.fill();
      ctx.fillStyle = P.c3; ctx.beginPath(); ctx.arc(W - 120, 250, 70, 0, 7); ctx.fill();
      ctx.fillStyle = P.c2; ctx.beginPath(); ctx.moveTo(-B, H + B); ctx.lineTo(W + B, H + B); ctx.lineTo(W + B, H - 150); ctx.lineTo(-B, H - 60); ctx.closePath(); ctx.fill();
      ctx.fillStyle = P.c1; ctx.beginPath(); ctx.moveTo(W + B, H - 150); ctx.lineTo(W * 0.5, H - 105); ctx.lineTo(W + B, H - 210); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = P.bg; ctx.lineWidth = 6; ctx.globalAlpha = 0.9; starOfDavid(ctx, 150, 140, 46); ctx.globalAlpha = 1;
      ctx.fillStyle = P.c3;
      for (var i = 0; i < 5; i++) { ctx.beginPath(); ctx.arc(820 - i * 34, H - 245, 7, 0, 7); ctx.fill(); }
    }
  });

  /* 10. Balloons (kids birthday) */
  T.push({
    id: "p-balloons", cat: "party", name: "בלונים וקונפטי",
    fonts: { display: "Varela Round", body: "Rubik" },
    palettes: [
      { bg: "#fffdf7", ink: "#2b2d42", accent: "#e4572e", soft: "#5c5f77", balloons: ["#e4572e", "#29a19c", "#f3c623", "#7b5ea7"] },
      { bg: "#f6fbff", ink: "#1f3a5f", accent: "#2f80ed", soft: "#5a6f8a", balloons: ["#2f80ed", "#56ccf2", "#f2c94c", "#27ae60"] },
      { bg: "#fff7fb", ink: "#4a2340", accent: "#d63384", soft: "#7d5a72", balloons: ["#d63384", "#f8a5c2", "#c9b6f2", "#ffd166"] }
    ],
    box: [140, 330, 860, 1220], div: "dots",
    sizes: { top: 40, title: 92, names: 120, invite: 34, date: 36, greg: 30, times: 34, venue: 36, address: 27, parents: 28, footer: 26 },
    order: ["top", "names", "title", "|", "invite", "date", "times", "venue", "address", "|", "parents", "footer"],
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var r = rng(99);
      for (var i = 0; i < 140; i++) {
        var x = r() * (W + 2 * B) - B, y = r() * (H + 2 * B) - B;
        if (x > 120 && x < W - 120 && y > 320 && y < H - 160) continue;
        ctx.save(); ctx.translate(x, y); ctx.rotate(r() * 6.28);
        ctx.fillStyle = P.balloons[i % 4];
        if (i % 3) ctx.fillRect(-7, -3, 14, 6); else { ctx.beginPath(); ctx.arc(0, 0, 5, 0, 7); ctx.fill(); }
        ctx.restore();
      }
      function balloon(x, y, rx, c, sway) {
        ctx.strokeStyle = hexA(P.ink, 0.45); ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x, y + rx * 1.22); ctx.bezierCurveTo(x + sway, y + rx * 2, x - sway, y + rx * 2.6, x + sway * 0.5, y + rx * 3.4); ctx.stroke();
        ctx.fillStyle = c;
        ctx.beginPath(); ctx.ellipse(x, y, rx, rx * 1.2, 0, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.moveTo(x, y + rx * 1.15); ctx.lineTo(x - 9, y + rx * 1.3); ctx.lineTo(x + 9, y + rx * 1.3); ctx.closePath(); ctx.fill();
        ctx.fillStyle = "rgba(255,255,255,0.45)";
        ctx.beginPath(); ctx.ellipse(x - rx * 0.35, y - rx * 0.4, rx * 0.16, rx * 0.3, -0.5, 0, 7); ctx.fill();
      }
      balloon(130, 170, 68, P.balloons[0], 20); balloon(250, 120, 56, P.balloons[1], -16); balloon(870, 160, 70, P.balloons[2], -20);
      balloon(760, 110, 52, P.balloons[3], 14);
      // bunting
      ctx.strokeStyle = hexA(P.ink, 0.4); ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(300, 40); ctx.quadraticCurveTo(W / 2, 150, 700, 40); ctx.stroke();
      for (var k = 0; k < 7; k++) {
        var t = (k + 0.5) / 7, bx = (1 - t) * (1 - t) * 300 + 2 * (1 - t) * t * (W / 2) + t * t * 700, by = (1 - t) * (1 - t) * 40 + 2 * (1 - t) * t * 150 + t * t * 40;
        ctx.fillStyle = P.balloons[k % 4]; ctx.beginPath(); ctx.moveTo(bx - 22, by); ctx.lineTo(bx + 22, by); ctx.lineTo(bx, by + 46); ctx.closePath(); ctx.fill();
      }
    }
  });

  /* 11. Brit / naming: soft dots and olive sprig */
  T.push({
    id: "p-brit", cat: "party", name: "ברית / בריתה",
    fonts: { display: "Frank Ruhl Libre", body: "Assistant" },
    palettes: [
      { bg: "#f4f9fd", ink: "#23384d", accent: "#3a77a8", soft: "#5d7186", dot: "#cfe3f3", leaf: "#8fb3a0" },
      { bg: "#fdf6f8", ink: "#4a2e39", accent: "#b85c7c", soft: "#8a6a76", dot: "#f6d9e3", leaf: "#a9bf9b" },
      { bg: "#fbfaf4", ink: "#36392c", accent: "#7d8a3a", soft: "#6e705f", dot: "#eae7cf", leaf: "#9aaa6c" }
    ],
    box: [150, 330, 850, 1180], div: "leaf",
    sizes: { top: 32, title: 72, names: 84, invite: 34, date: 36, greg: 30, times: 31, venue: 38, address: 27, parents: 28, footer: 25 },
    order: ["top", "title", "names", "|", "invite", "date", "times", "venue", "address", "|", "parents", "footer"],
    preset: {
      top: "בשמחה ובהודיה לה׳", title: "ברית מילה", names: "לבננו היקר",
      invite: "אנו שמחים להזמינכם להשתתף\nבשמחתנו בהיכנס בננו בבריתו של אברהם אבינו",
      times: "קבלת פנים 8:30 · הברית 9:00", venue: "בית הכנסת \"אהל משה\"", address: "רחוב הזית 3, עיר לדוגמה",
      parentsR: "ההורים: נוי ויואב אלון", parentsL: "", footer: "הסעודה תתקיים לאחר הברית"
    },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      ctx.fillStyle = P.dot;
      for (var y = -B + 20, row = 0; y < H + B; y += 46, row++) {
        for (var x = -B + (row % 2 ? 23 : 0); x < W + B; x += 46) {
          if (x > 110 && x < W - 110 && y > 110 && y < H - 110) continue;
          ctx.beginPath(); ctx.arc(x, y, 6, 0, 7); ctx.fill();
        }
      }
      ctx.fillStyle = P.bg; roundRect(ctx, 100, 100, W - 200, H - 200, 40); ctx.fill();
      ctx.strokeStyle = P.accent; ctx.lineWidth = 2; roundRect(ctx, 120, 120, W - 240, H - 240, 30); ctx.stroke();
      branch(ctx, W / 2 - 150, 250, 300, 0, 9, 50, P.leaf, 0.12, { berry: P.accent });
      ctx.fillStyle = P.accent; ctx.beginPath(); ctx.arc(W / 2, H - 175, 6, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(W / 2 - 26, H - 175, 4, 0, 7); ctx.fill(); ctx.beginPath(); ctx.arc(W / 2 + 26, H - 175, 4, 0, 7); ctx.fill();
    }
  });

  /* 12. Black & gold milestone birthday */
  T.push({
    id: "p-gold", cat: "party", name: "יום הולדת חגיגי",
    fonts: { display: "Bellefair", body: "Heebo" },
    palettes: [
      { bg: "#121212", ink: "#f5f0e6", accent: "#e0bf6e", soft: "#bdb5a5", goldy: true },
      { bg: "#0f2a2a", ink: "#eef6f3", accent: "#e6c27a", soft: "#a9bfb9", goldy: true },
      { bg: "#fbf7ef", ink: "#2a2420", accent: "#a6772a", soft: "#6f655a", goldy: true }
    ],
    box: [150, 230, 850, 1210], div: "sparkle",
    sizes: { top: 40, title: 260, names: 100, invite: 34, date: 36, greg: 30, times: 32, venue: 36, address: 27, parents: 28, footer: 26 },
    order: ["top", "title", "names", "|", "invite", "date", "times", "venue", "address", "|", "parents", "footer"],
    preset: {
      top: "חוגגים", title: "50", names: "לדנה",
      invite: "הצטרפו אלינו לערב של אוכל טוב,\nמוזיקה וחברים", times: "החל מ-20:30",
      venue: "בר \"הגפן\"", address: "רחוב הנמל 4, עיר לדוגמה",
      parentsR: "באהבה, המשפחה", parentsL: "", footer: "נשמח לאישור הגעה עד שבוע לפני"
    },
    decor: function (ctx, P, B) {
      bg(ctx, B, P.bg);
      var g = gold(ctx, 0, 0, W, H);
      var r = rng(314);
      for (var i = 0; i < 180; i++) {
        var x = r() * (W + 2 * B) - B, y = r() * (H + 2 * B) - B;
        var d = Math.min(x, W - x, y, H - y);
        if (d > 70 + r() * 120) continue;
        ctx.save(); ctx.translate(x, y); ctx.rotate(r() * 6.28); ctx.fillStyle = g;
        if (i % 4 === 0) sparkle(ctx, 0, 0, 6 + r() * 8);
        else if (i % 2) { ctx.fillRect(-8, -2.5, 16, 5); }
        else { ctx.beginPath(); ctx.arc(0, 0, 3 + r() * 5, 0, 7); ctx.fill(); }
        ctx.restore();
      }
      ctx.strokeStyle = g; ctx.lineWidth = 2; ctx.strokeRect(110, 110, W - 220, H - 220);
    },
    titleGold: true
  });

  var ORDER = ["top", "title", "names", "|", "invite", "date", "times", "venue", "address", "|", "parents", "footer"];

  function byId(id) {
    for (var i = 0; i < T.length; i++) if (T[i].id === id) return T[i];
    return T[0];
  }

  /* ---------- text layout ---------- */
  function fontStr(weight, size, family) {
    return weight + " " + size.toFixed(1) + 'px "' + family + '", "Assistant", "Heebo", sans-serif';
  }
  function wrap(ctx, text, maxW) {
    var out = [];
    String(text || "").split("\n").forEach(function (para) {
      para = para.trim();
      if (!para) return;
      var words = para.split(/\s+/), line = "";
      words.forEach(function (w) {
        var test = line ? line + " " + w : w;
        if (line && ctx.measureText(test).width > maxW) { out.push(line); line = w; } else line = test;
      });
      if (line) out.push(line);
    });
    return out;
  }
  function composeDate(s) {
    var lines = [];
    var hd = window.HebDate && s.date ? window.HebDate.hebrew(s.date, { evening: !!s.evening }) : null;
    if (!hd) return lines;
    var heb = "";
    if (s.showDay) heb += "ב" + hd.weekday + ", ";
    if (s.showHeb) heb += (s.evening ? "אור ל" : "") + hd.text;
    heb = heb.replace(/, $/, "");
    if (heb) lines.push({ text: heb, role: "date" });
    if (s.showGreg) lines.push({ text: hd.greg, role: "greg" });
    return lines;
  }

  /* Build the stack of text items. Each item: {lines[], size, family, weight, color, gap} or {cols:[a,b]} or {div:true} */
  function blocks(ctx, tpl, P, st, scale, maxW) {
    var f = st.fonts || tpl.fonts, S = tpl.sizes, t = st.texts || {};
    var disp = f.display, body = f.body;
    var nameScale = (st.nameScale || 100) / 100;
    var items = [];
    function add(key, text, size, family, weight, color, gap, opts) {
      if (!text || !String(text).trim()) return;
      size *= scale;
      ctx.font = fontStr(weight, size, family);
      var lines = wrap(ctx, text, maxW);
      // shrink single long words / names to fit width
      var widest = Math.max.apply(null, lines.map(function (l) { return ctx.measureText(l).width; }));
      if (widest > maxW) { size *= maxW / widest; ctx.font = fontStr(weight, size, family); lines = wrap(ctx, text, maxW); }
      items.push({ key: key, lines: lines, size: size, family: family, weight: weight, color: color, gap: gap * scale, gold: opts && opts.gold });
    }
    var order = tpl.order || ORDER;
    order.forEach(function (k) {
      if (k === "|") { items.push({ div: true, gap: 34 * scale, h: 20 * scale }); return; }
      if (k === "top") add(k, t.top, S.top, body, fontWeight(body, 400), P.soft, 18);
      else if (k === "title") add(k, t.title, S.title, disp, fontWeight(disp, 700), P.accent, 14, { gold: tpl.titleGold && P.goldy });
      else if (k === "names") add(k, t.names, S.names * nameScale, disp, fontWeight(disp, 700), P.accent, 22, { gold: P.goldy && !tpl.titleGold });
      else if (k === "invite") add(k, t.invite, S.invite, body, fontWeight(body, 400), P.ink, 22);
      else if (k === "date") {
        composeDate(st).forEach(function (d) {
          add(d.role, d.text, d.role === "date" ? S.date : S.greg, d.role === "date" ? body : body, fontWeight(body, d.role === "date" ? 700 : 400), d.role === "date" ? P.ink : P.soft, 10);
        });
        if (items.length) items[items.length - 1].gap += 8 * scale;
      }
      else if (k === "times") add(k, t.times, S.times, body, fontWeight(body, 700), P.ink, 12);
      else if (k === "venue") add(k, t.venue, S.venue, disp, fontWeight(disp, 400), P.accent, 8);
      else if (k === "address") add(k, t.address, S.address, body, fontWeight(body, 400), P.soft, 14);
      else if (k === "parents") {
        var a = (t.parentsR || "").trim(), b = (t.parentsL || "").trim();
        if (a && b) {
          var size = S.parents * scale, fam = body, wt = fontWeight(body, 400);
          ctx.font = fontStr(wt, size, fam);
          var colW = maxW / 2 - 20 * scale;
          var la = wrap(ctx, a, colW), lb = wrap(ctx, b, colW);
          items.push({ key: k, cols: [la, lb], size: size, family: fam, weight: wt, color: P.ink, gap: 14 * scale, colW: colW });
        } else add(k, a || b, S.parents, body, fontWeight(body, 400), P.ink, 14);
      }
      else if (k === "footer") add(k, t.footer, S.footer, body, fontWeight(body, 400), P.soft, 0);
    });
    // drop dividers at the start/end or doubled
    var clean = [];
    items.forEach(function (it, i) {
      if (it.div && (!clean.length || clean[clean.length - 1].div || i === items.length - 1)) return;
      clean.push(it);
    });
    while (clean.length && clean[clean.length - 1].div) clean.pop();
    return clean;
  }
  function lineH(it) { return it.size * 1.28; }
  function itemH(it) {
    if (it.div) return it.h;
    if (it.cols) return Math.max(it.cols[0].length, it.cols[1].length) * lineH(it);
    return it.lines.length * lineH(it);
  }
  function totalH(items) {
    return items.reduce(function (s, it, i) { return s + itemH(it) + (i < items.length - 1 ? it.gap : 0); }, 0);
  }

  function drawText(ctx, tpl, P, st) {
    var bx = tpl.box, maxW = bx[2] - bx[0], boxH = bx[3] - bx[1];
    var scale = 1, items;
    for (var it = 0; it < 8; it++) {
      items = blocks(ctx, tpl, P, st, scale, maxW);
      var h = totalH(items);
      if (h <= boxH) break;
      scale *= Math.max(0.6, (boxH / h) * 0.995);
    }
    var y = bx[1] + Math.max(0, (boxH - totalH(items)) / 2);
    ctx.direction = "rtl"; ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";
    var cx = (bx[0] + bx[2]) / 2;
    items.forEach(function (it) {
      if (it.div) { divider(ctx, P, y + it.h / 2, Math.min(260, maxW * 0.5), tpl.div); y += it.h + it.gap; return; }
      ctx.font = fontStr(it.weight, it.size, it.family);
      var lh = lineH(it), base = it.size * 1.0;
      if (it.cols) {
        ctx.fillStyle = it.color;
        var off = maxW / 4 + 4;
        it.cols[0].forEach(function (l, i) { ctx.fillText(l, cx + off, y + base + i * lh, it.colW); });
        it.cols[1].forEach(function (l, i) { ctx.fillText(l, cx - off, y + base + i * lh, it.colW); });
      } else {
        ctx.fillStyle = it.gold ? gold(ctx, cx - 300, y, cx + 300, y + lh * it.lines.length) : it.color;
        it.lines.forEach(function (l, i) { ctx.fillText(l, cx, y + base + i * lh, maxW); });
      }
      y += itemH(it) + it.gap;
    });
  }

  function watermark(ctx, B) {
    ctx.save();
    ctx.translate(W / 2, H / 2); ctx.rotate(-Math.PI / 6);
    ctx.direction = "rtl"; ctx.textAlign = "center";
    ctx.font = '700 46px "Assistant", "Heebo", sans-serif';
    ctx.fillStyle = "rgba(120,120,120,0.22)";
    for (var y = -1100; y <= 1100; y += 170) {
      for (var x = -900; x <= 900; x += 620) ctx.fillText("תצוגה מקדימה · תכנון פלוס", x + (y / 170 % 2 ? 310 : 0), y);
    }
    ctx.restore();
    ctx.fillStyle = "rgba(20,20,20,0.72)"; ctx.fillRect(-B, H - 78, W + 2 * B, 78 + B);
    ctx.fillStyle = "#fff"; ctx.direction = "rtl"; ctx.textAlign = "center";
    ctx.font = '600 30px "Assistant", "Heebo", sans-serif';
    ctx.fillText("תצוגה מקדימה – גרסה נקייה ב-tichnun.netlify.app", W / 2, H - 30);
  }

  /* render(canvas, state, {width: px, bleedMm: mm, trimMm: mm (width of trim, for bleed calc), watermark: bool}) */
  function render(canvas, st, opts) {
    opts = opts || {};
    var tpl = byId(st.template);
    var P = Object.assign({}, tpl.palettes[st.palette || 0] || tpl.palettes[0]);
    if (st.accent) { P.accent = st.accent; P.goldy = false; }
    var B = 0;
    if (opts.bleedMm && opts.trimMm) B = W * opts.bleedMm / opts.trimMm;
    var pxPerUnit = (opts.width || 600) / (W + 2 * B);
    canvas.width = Math.round((W + 2 * B) * pxPerUnit);
    canvas.height = Math.round((H + 2 * B) * pxPerUnit);
    var ctx = canvas.getContext("2d");
    ctx.setTransform(pxPerUnit, 0, 0, pxPerUnit, B * pxPerUnit, B * pxPerUnit);
    ctx.clearRect(-B, -B, W + 2 * B, H + 2 * B);
    ctx.save(); tpl.decor(ctx, P, B); ctx.restore();
    ctx.save(); drawText(ctx, tpl, P, st); ctx.restore();
    if (opts.watermark) { ctx.save(); watermark(ctx, B); ctx.restore(); }
    return canvas;
  }

  function fontsFor(st) {
    var tpl = byId(st.template), f = st.fonts || tpl.fonts;
    return [f.display, f.body, "Assistant"];
  }

  window.Invite = {
    W: W, H: H, FONTS: FONTS, CATS: CATS, TEMPLATES: T, DEFAULTS: DEFAULTS, DEFAULT_DATES: DEFAULT_DATES,
    byId: byId, render: render, composeDate: composeDate, fontsFor: fontsFor, fontWeight: fontWeight
  };
})();
