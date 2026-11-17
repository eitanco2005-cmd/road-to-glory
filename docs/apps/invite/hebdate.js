/* Hebrew date for invitations: "ה׳ בטבת התשפ״ז" from a Gregorian date, using the browser's Hebrew calendar (Intl). */
(function () {
  "use strict";
  var ONES = ["", "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט"];
  var TENS = ["", "י", "כ", "ל", "מ", "נ", "ס", "ע", "פ", "צ"];
  var HUNDREDS = ["", "ק", "ר", "ש", "ת", "תק", "תר", "תש", "תת", "תתק"];
  function letters(n) { // 1..999
    var s = HUNDREDS[Math.floor(n / 100)];
    var r = n % 100;
    if (r === 15) return s + "טו";
    if (r === 16) return s + "טז";
    return s + TENS[Math.floor(r / 10)] + ONES[r % 10];
  }
  function punct(s) { // geresh for one letter, gershayim before the last letter otherwise
    return s.length === 1 ? s + "׳" : s.slice(0, -1) + "״" + s.slice(-1);
  }
  function gematria(n) { return punct(letters(n)); }

  var fmtNum, fmtMonth, fmtDay;
  try {
    fmtNum = new Intl.DateTimeFormat("en-u-ca-hebrew", { day: "numeric", month: "numeric", year: "numeric", timeZone: "UTC" });
    fmtMonth = new Intl.DateTimeFormat("he-u-ca-hebrew", { month: "long", timeZone: "UTC" });
    fmtDay = new Intl.DateTimeFormat("he", { weekday: "long", timeZone: "UTC" });
  } catch (e) {}

  function parse(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return null;
    return new Date(Date.UTC(+m[1], +m[2] - 1, +m[3], 12));
  }
  /* -> {day, month, year, text, weekday, greg} or null.  opts.evening: event after sunset -> next Hebrew day ("אור ל") */
  function hebrew(iso, opts) {
    var d = parse(iso);
    if (!d || !fmtNum) return null;
    opts = opts || {};
    var hd = opts.evening ? new Date(d.getTime() + 864e5) : d;
    var parts = {};
    fmtNum.formatToParts(hd).forEach(function (p) { parts[p.type] = p.value; });
    var day = parseInt(parts.day, 10), year = parseInt(parts.year, 10);
    var month = fmtMonth.format(hd).replace(/^ב/, "") ;
    var yearTxt = "ה" + gematria(year % 1000);
    var text = gematria(day) + " ב" + month + " " + yearTxt;
    return {
      day: day, month: month, year: year, text: text,
      weekday: fmtDay.format(d),
      greg: ("0" + d.getUTCDate()).slice(-2) + "." + ("0" + (d.getUTCMonth() + 1)).slice(-2) + "." + d.getUTCFullYear()
    };
  }
  window.HebDate = { gematria: gematria, hebrew: hebrew };
})();
