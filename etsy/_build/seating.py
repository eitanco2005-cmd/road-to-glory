#!/usr/bin/env python3
"""Wedding Seating Chart: xlsx (guest list -> tables -> printable seating plan) + printable PDF kit (Letter + A4).
-> etsy/listings/07-wedding-seating-chart/files/"""
import math
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
B = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "products" / "en-jewish-life"))
sys.path.insert(0, str(B))
from xl import *  # noqa: F401,F403,E402
import xl  # noqa: E402
from clean import clean_xlsx  # noqa: E402

OUT = REPO / "etsy" / "listings" / "07-wedding-seating-chart" / "files"
S_SET, S_G, S_T, S_P = "Settings", "Guests", "Tables", "Seating Plan"
N_T, N_G, MAX_SEATS = 40, 400, 14
FONTS = (REPO / "products" / "hanukkah" / "fonts").as_uri()

FIRSTS = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason", "Mia", "Lucas", "Grace", "Leo", "Chloe",
          "Jack", "Lily", "Owen", "Zoe", "Ben", "Nora", "Sam", "Ruth", "David", "Anna", "Mark", "Julia", "Paul", "Sara",
          "Tom", "Hannah", "Adam", "Ella", "Ryan", "Maya", "Josh", "Leah", "Dan", "Rose", "Nick", "Amy", "Eli"]
LASTS = ["Carter", "Nguyen", "Smith", "Garcia", "Klein", "Rossi", "Patel", "Murphy", "Cohen", "Brooks", "Diaz", "Lee",
         "Walsh", "Stone", "Price", "Reed"]


def demo_guests():
    import random
    rnd = random.Random(7)
    rows = [("Emma Carter", "Couple", "Head table", "Chicken", 1), ("James Reed", "Couple", "Head table", "Beef", 1)]
    plan = [(1, 8, "Wedding party"), (2, 10, "Bride's family"), (3, 10, "Groom's family"), (4, 9, "Bride's family"),
            (5, 10, "Groom's family"), (6, 8, "College friends"), (7, 10, "Work friends"), (8, 7, "Neighbors"),
            (9, 6, "Family friends"), (10, 0, "")]
    side = {"Bride's family": "Bride", "Groom's family": "Groom"}
    for t, n, grp in plan:
        for i in range(n if t != 1 else n - 2):
            rows.append((f"{rnd.choice(FIRSTS)} {rnd.choice(LASTS)}", side.get(grp, rnd.choice(["Bride", "Groom", "Both"])),
                         grp, rnd.choice(["Chicken", "Beef", "Fish", "Vegetarian", "Kids meal"]), t))
    for i in range(6):
        rows.append((f"{rnd.choice(FIRSTS)} {rnd.choice(LASTS)}", "Both", "Plus-ones", rnd.choice(["Chicken", "Fish"]), None))
    return rows


def build_xlsx(demo=False):
    wb = new_book()
    ws = sheet(wb, S_SET, "Settings", "Default seats per table and your drop-down lists. Rename anything.", [30, 16, 4, 24, 24, 24], tab="C9A227")
    put(ws, "A4", "Event name", bold=True)
    put(ws, "B4", "Emma & James' Wedding" if demo else None, "input")
    put(ws, "A5", "Default seats per table", bold=True)
    put(ws, "B5", 10, "input", NUM)
    define(wb, "def_seats", f"{q(S_SET)}!$B$5")
    for c, (h, items) in zip("DEF", [("Sides", ["Bride", "Groom", "Both", "Couple", "Partner 1", "Partner 2"]),
                                      ("Groups", ["Head table", "Wedding party", "Bride's family", "Groom's family",
                                                  "College friends", "Work friends", "Family friends", "Neighbors",
                                                  "Plus-ones", "Kids"]),
                                      ("Meals", ["Chicken", "Beef", "Fish", "Vegetarian", "Vegan", "Kids meal", "Gluten-free"])]):
        put(ws, f"{c}3", h, "head")
        for i in range(20):
            put(ws, f"{c}{4 + i}", items[i] if i < len(items) else None, "input")
    define(wb, "sides", f"{q(S_SET)}!$D$4:$D$23")
    define(wb, "groups", f"{q(S_SET)}!$E$4:$E$23")
    define(wb, "meals", f"{q(S_SET)}!$F$4:$F$23")

    # Tables
    wt = sheet(wb, S_T, "Tables", "Name your tables and set seats. Seated / free update from the guest list. Red = too many guests.",
               [9, 26, 10, 10, 10, 16], tab="2E7D32")
    headers(wt, 4, ["Table #", "Table name (optional)", "Seats", "Seated", "Free", "Status"])
    names = {1: "Head table"}
    for i in range(N_T):
        r = FIRST + i
        put(wt, f"A{r}", i + 1, "calc", align="center", bold=True)
        put(wt, f"B{r}", names.get(i + 1) if demo else None, "input")
        put(wt, f"C{r}", None, "input", NUM)
        wt[f"C{r}"] = None
        put(wt, f"D{r}", f"=COUNTIF({col(S_G, 'E', N_G)},A{r})", "calc", NUM, align="center")
        put(wt, f"E{r}", f"=IF(C{r}=\"\",def_seats,C{r})-D{r}", "calc", "#,##0;[Red]-#,##0;0", align="center")
        put(wt, f"F{r}", f"=IF(D{r}=0,\"Empty\",IF(E{r}<0,\"Over by \"&-E{r},IF(E{r}=0,\"Full\",\"OK\")))", "calc", align="center")
    if demo:
        wt[f"C{FIRST}"] = 8
    lt = FIRST + N_T - 1
    cf(wt, f"F{FIRST}:F{lt}", f'LEFT(F{FIRST},4)="Over"', C_BAD, bold=True)
    cf(wt, f"F{FIRST}:F{lt}", f'F{FIRST}="Full"', C_OK)
    put(wt, f"A{lt + 2}", "Total seated", "total")
    put(wt, f"D{lt + 2}", f"=SUM(D{FIRST}:D{lt})", "total", NUM)
    put(wt, f"A{lt + 3}", "Guests without a table", "total")
    put(wt, f"D{lt + 3}", f"=COUNTA({col(S_G, 'A', N_G)})-COUNT({col(S_G, 'E', N_G)})", "total", NUM)
    define(wb, "tbl_nums", f"{q(S_T)}!$A${FIRST}:$A${lt}")

    # Guests
    wg = sheet(wb, S_G, "Guest list", "One row per guest (one person per row). Pick a table number; the Seating Plan fills itself. "
               "Sort by name any time: select the list > Data > Sort.", [28, 13, 20, 14, 9, 24, 8], tab="1565C0")
    headers(wg, 4, ["Guest name", "Side", "Group", "Meal", "Table #", "Notes (allergies, high chair…)", "seat key"])
    blank_rows(wg, FIRST, N_G, ["input"] * 6 + ["calc"])
    for r in range(FIRST, FIRST + N_G):
        wg[f"G{r}"] = f'=IF(OR(A{r}="",E{r}=""),"",E{r}&"-"&COUNTIF($E${FIRST}:E{r},E{r}))'
        wg[f"G{r}"].font = xl.Font(name=FONT, size=8, color="9AA5AE")
    if demo:
        for i, (n, sd, g, m, t) in enumerate(demo_guests()):
            for j, v in enumerate([n, sd, g, m, t]):
                wg.cell(row=FIRST + i, column=j + 1, value=v)
    lg = FIRST + N_G - 1
    dv_list(wg, "=sides", f"B{FIRST}:B{lg}")
    dv_list(wg, "=groups", f"C{FIRST}:C{lg}")
    dv_list(wg, "=meals", f"D{FIRST}:D{lg}")
    dv_list(wg, "=tbl_nums", f"E{FIRST}:E{lg}", prompt="Table number (1–40)")
    cf(wg, f"E{FIRST}:E{lg}", f'AND(A{FIRST}<>"",E{FIRST}="")', C_WARN)

    # Seating plan: blocks of 4 tables across, MAX_SEATS rows each
    wp = sheet(wb, S_P, "Seating plan", "Fills itself from the guest list. Print it, or share it with your venue and planner.",
               [5, 24, 2, 5, 24, 2, 5, 24, 2, 5, 24], tab="C62828")
    wp.freeze_panes = None
    r = 4
    for blk in range(math.ceil(N_T / 4)):
        for k in range(4):
            t = blk * 4 + k + 1
            c0 = 1 + k * 3
            hc = wp.cell(row=r, column=c0)
            wp.merge_cells(start_row=r, start_column=c0, end_row=r, end_column=c0 + 1)
            tr = FIRST + t - 1
            hc.value = (f'="Table {t}"&IF({q(S_T)}!B{tr}="",""," · "&{q(S_T)}!B{tr})&"  ("&{q(S_T)}!D{tr}&")"')
            style(hc, "head")
            for s in range(1, MAX_SEATS + 1):
                a = wp.cell(row=r + s, column=c0, value=s)
                style(a, None, size=8, color="9AA5AE", align="center")
                b = wp.cell(row=r + s, column=c0 + 1,
                            value=f'=IFERROR(INDEX({col(S_G, "A", N_G)},MATCH("{t}-{s}",{col(S_G, "G", N_G)},0)),"")')
                style(b, None, size=10)
                b.border = xl.Border(bottom=xl.Side(style="hair", color="C7CED6"))
        r += MAX_SEATS + 2
    wp.print_area = f"A1:K{r}"
    wp.page_setup.fitToHeight = 0

    for w in wb.worksheets:
        w.page_setup.orientation = "portrait"
        w.page_setup.paperSize = w.PAPERSIZE_LETTER
        w.page_setup.fitToWidth = 1
        w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    instructions(wb, "Wedding Seating Chart",
                 "Type your guest list, give each guest a table number and the Seating Plan builds itself: table by "
                 "table, seat by seat. Warnings show tables that are too full and guests who still need a seat.",
                 ["Settings: default seats per table (for example 8, 10 or 12) and your drop-down lists.",
                  "Guests: one row per guest. Choose side, group, meal and a table number.",
                  "Tables: optional table names (e.g. Head table) and a different seat count per table.",
                  "Seating Plan: check it, print it (File > Print) or share it with the venue.",
                  "Moving someone? Just change their table number. Everything updates."],
                 ["Up to 400 guests, 40 tables and 14 seats per table. Insert more guest rows above the last row if you need them.",
                  "Meal counts per table: filter the Guests sheet by Table # (Data > Filter)."],
                 [("Settings", "Seats per table, sides, groups and meals (rename freely)."),
                  ("Tables", "40 tables: name, seats, seated, free, over-capacity warning."),
                  ("Guests", "400 rows: name, side, group, meal, table #, notes."),
                  ("Seating Plan", "Printable plan, 4 tables across, filled automatically.")])
    st = wb["Start Here"]
    for row in st.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "rabbi" in c.value:
                c.value = "• Works for weddings, bar/bat mitzvahs, galas and any seated event."
            if isinstance(c.value, str) and "Amounts are in US dollars" in c.value:
                c.value = "• Tip: give couples and families consecutive rows so they're easy to move together."
    wb.active = 0
    props(wb, "Wedding Seating Chart", "Seating chart spreadsheet")
    wb.properties.keywords = "wedding seating chart, table plan, Excel, Google Sheets"
    return wb


# ------------------------------------------------------------------ printable PDF kit
def round_table(n, size=330, label="Table"):
    cx = cy = size / 2
    R = size * 0.22
    rr = size * 0.40
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#F6F1EA" stroke="#8A6E5A" stroke-width="2"/>',
             f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" font-family="Caladea" font-size="{size * .07}" fill="#3B2F2A">{label}</text>',
             f'<line x1="{cx - R * .55}" y1="{cy + size * .05}" x2="{cx + R * .55}" y2="{cy + size * .05}" stroke="#B9A797" stroke-width="1"/>']
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        parts.append(f'<circle cx="{x}" cy="{y}" r="{size * .028}" fill="#fff" stroke="#8A6E5A" stroke-width="1.5"/>')
        parts.append(f'<text x="{x}" y="{y + size * .011}" text-anchor="middle" font-size="{size * .03}" font-family="Nunito" fill="#8A6E5A">{i + 1}</text>')
    return f'<svg viewBox="0 0 {size} {size}" width="100%">{"".join(parts)}</svg>'


def pdf_html(paper):
    w, h = ("8.5in", "11in") if paper == "Letter" else ("210mm", "297mm")
    css = f"""
@font-face{{font-family:Nunito;src:url({FONTS}/Nunito-400.ttf)}}@font-face{{font-family:Nunito;font-weight:700;src:url({FONTS}/Nunito-700.ttf)}}
@page{{size:{w} {h};margin:0}}*{{box-sizing:border-box;margin:0}}body{{font-family:Nunito;color:#3B2F2A}}
.pg{{width:{w};height:{h};padding:0.55in 0.6in;page-break-after:always;position:relative;overflow:hidden}}
h1{{font-family:Caladea;font-weight:400;font-size:34pt;text-align:center;letter-spacing:1px}}
h2{{font-family:Caladea;font-weight:400;font-size:24pt;text-align:center;margin-bottom:4pt}}
.sub{{text-align:center;font-size:10.5pt;color:#7a6a5f;margin-bottom:14pt}}
.orn{{text-align:center;color:#C9A227;font-size:14pt;margin:6pt 0}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:10pt 18pt}}
.tbl{{border:1px solid #E5DBD0;border-radius:8pt;padding:6pt 8pt}}
.lines div{{border-bottom:1px solid #CDBFB2;height:17pt;font-size:8pt;color:#a89788;padding-top:5pt}}
.foot{{position:absolute;bottom:.3in;left:0;right:0;text-align:center;font-size:8pt;color:#a89788}}
.card{{height:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;border-bottom:1px dashed #CDBFB2}}
.card .num{{font-family:Caladea;font-size:120pt;line-height:1}}
.card .lbl{{font-family:Caladea;font-size:26pt;letter-spacing:6px;text-transform:uppercase;color:#8A6E5A}}
.az{{display:grid;grid-template-columns:repeat(3,1fr);gap:8pt 14pt}}
.az .l{{font-family:Caladea;font-size:15pt;color:#8A6E5A;border-bottom:1.5px solid #C9A227;margin-top:4pt}}
.dot{{background-image:radial-gradient(#C8BBAE 1px,transparent 1.2px);background-size:0.25in 0.25in;border:1px solid #E5DBD0;height:8.2in;border-radius:6pt}}
"""
    foot = '<div class="foot">© 2026 Tichnun Plus · Printable seating chart kit · personal use</div>'
    pages = []
    pages.append(f"""<div class=pg><div style="height:2.2in"></div><div class=orn>✦ ✦ ✦</div><h1>Wedding Seating Chart</h1>
<div class=orn>✦ ✦ ✦</div><p class=sub style="font-size:13pt;margin-top:10pt">Printable planning kit</p>
<div style="margin:0.5in auto 0;width:5.2in;font-size:11pt;line-height:1.6">
<b>What's inside</b><br>• Round table planners: 8, 10 and 12 seats (4 tables per page)<br>• Long / head table planner (up to 20 seats)
<br>• Floor-plan dot grid to sketch the room<br>• "Find your seat" A–Z guest board (2 pages)<br>• Table number cards 1–30 (cut in half, or fold for a tent card)
<br><br><b>How to use</b><br>1. Print at 100% ("Actual size") on plain paper or card stock.<br>2. Write in pencil first: guests always move!
<br>3. For the digital version, use the Excel / Google Sheets seating chart included in this download.</div>{foot}</div>""")
    for n in (8, 10, 12):
        for pgi in range(2):
            cells = "".join(f'<div class=tbl>{round_table(n, label=f"Table ____")}<div class=lines>' +
                            "".join(f"<div>{i + 1}.</div>" for i in range(0)) + "</div></div>" for _ in range(4))
            pages.append(f'<div class=pg><h2>Round tables · {n} seats</h2><p class=sub>Write the table number in the middle and a name next to each seat number. Page {pgi + 1} of 2.</p>'
                         f'<div class=grid2>{cells}</div>'
                         f'<div style="margin-top:8pt;font-size:9pt;color:#7a6a5f">Seat names: write them right next to each numbered circle, or list them below the table.</div>{foot}</div>')
    head = ('<svg viewBox="0 0 700 140" width="100%"><rect x="60" y="45" width="580" height="50" rx="8" fill="#F6F1EA" stroke="#8A6E5A" stroke-width="2"/>'
            '<text x="350" y="77" text-anchor="middle" font-family="Caladea" font-size="20" fill="#3B2F2A">Head table</text>' +
            "".join(f'<circle cx="{88 + i * 58}" cy="28" r="11" fill="#fff" stroke="#8A6E5A" stroke-width="1.5"/>'
                    f'<text x="{88 + i * 58}" y="32" text-anchor="middle" font-size="11" font-family="Nunito" fill="#8A6E5A">{i + 1}</text>' for i in range(10)) +
            "".join(f'<circle cx="{88 + i * 58}" cy="112" r="11" fill="#fff" stroke="#8A6E5A" stroke-width="1.5"/>'
                    f'<text x="{88 + i * 58}" y="116" text-anchor="middle" font-size="11" font-family="Nunito" fill="#8A6E5A">{i + 11}</text>' for i in range(10)) +
            "</svg>")
    rows = "".join(f'<div style="display:flex;gap:14pt"><div style="flex:1">{i + 1}. </div><div style="flex:1">{i + 11}. </div></div>' for i in range(10))
    pages.append(f'<div class=pg><h2>Long / head table</h2><p class=sub>Up to 20 seats (seats 1–10 on one side, 11–20 on the other). Use only one side for a sweetheart-style head table.</p>'
                 f'{head}<div class=lines style="margin-top:14pt">' +
                 "".join(f'<div style="display:flex"><span style="width:50%">{i + 1}.</span><span>{i + 11}.</span></div>' for i in range(10)) +
                 f'</div><h2 style="margin-top:22pt;font-size:18pt">Notes</h2><div class=lines>' + "<div></div>" * 8 + f'</div>{foot}</div>')
    pages.append(f'<div class=pg><h2>Floor plan</h2><p class=sub>Sketch the room: dance floor, stage / DJ, bar, entrances, and number your tables.</p><div class=dot></div>{foot}</div>')
    letters = [chr(c) for c in range(65, 91)]
    for part, ls in enumerate([letters[:13], letters[13:]]):
        blocks = "".join(f'<div><div class=l>{L}</div><div class=lines>' + "<div>Name · Table</div>" + "<div></div>" * 4 + "</div></div>" for L in ls)
        pages.append(f'<div class=pg><h1 style="font-size:28pt">Find Your Seat</h1><div class=orn>✦</div>'
                     f'<p class=sub>Guests by last name · {ls[0]}–{ls[-1]}</p><div class=az>{blocks}</div>{foot}</div>')
    for i in range(1, 31, 2):
        pages.append('<div class=pg style="padding:0">' + "".join(
            f'<div class=card><div class=lbl>Table</div><div class=num>{n}</div><div class=orn>✦</div></div>' for n in (i, i + 1)) + "</div>")
    return f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


def build_pdfs():
    tmp = B / "_cache"
    tmp.mkdir(exist_ok=True)
    jobs = []
    for paper, name in [("Letter", "Wedding-Seating-Chart-Printables-US-Letter"), ("A4", "Wedding-Seating-Chart-Printables-A4")]:
        h = tmp / f"{name}.html"
        h.write_text(pdf_html(paper), encoding="utf-8")
        jobs.append(f"{h}={OUT / (name + '.pdf')}")
    subprocess.run(["node", str(REPO / "products/hanukkah/print_pdf.js"), *jobs], check=True, capture_output=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.iterdir():
        f.unlink()
    tmp = B / "_cache"
    tmp.mkdir(exist_ok=True)
    for demo, name in [(False, "Wedding-Seating-Chart.xlsx"), (True, "Wedding-Seating-Chart-EXAMPLE.xlsx")]:
        build_xlsx(demo).save(tmp / name)
        clean_xlsx(tmp / name, OUT / name)
    build_pdfs()
    print(sorted(p.name for p in OUT.iterdir()))
