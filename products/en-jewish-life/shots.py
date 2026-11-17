"""Render product screenshots: example workbook -> chosen print areas -> LibreOffice PDF -> PNG + WebP.
python3 shots.py <slug> <outdir>"""
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

AREAS = {
    "event": [("Dashboard", "A1:I63"), ("Budget", "A1:H20"), ("Guests", "A1:M24"), ("Payments", "A1:I16"),
              ("Checklist", "A1:G26"), (None, "A1:F24")],
    "passover-seder-planner": [("Dashboard", "A1:I51"), ("Shopping List", "A1:O31"), ("Guests", "A1:H13"),
                               ("Haggadah Parts", "A1:E26"), ("Prep Timeline", "A1:F22")],
    "jewish-holiday-planner": [("Dashboard", "A1:E63"), ("Holidays", "A1:J15"), ("Guests", "A1:N15"),
                               ("Traditions", "A1:D30"), ("Shopping", "A1:H21")],
}


def workbook(slug):
    if slug == "passover-seder-planner":
        import seder
        return seder.build(True), AREAS[slug]
    if slug == "jewish-holiday-planner":
        import holidays
        return holidays.build(True), AREAS[slug]
    import event
    from event_configs import BAR_MITZVAH, WEDDING
    cfg = BAR_MITZVAH if slug == "bar-mitzvah-planner" else WEDDING
    areas = [(n or cfg["honors"]["sheet"], a) for n, a in AREAS["event"]]
    return event.build(cfg, True), areas


def render(slug, outdir):
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, "_tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    wb, areas = workbook(slug)
    wanted = dict(areas)
    for ws in wb.worksheets:
        if ws.title not in wanted:
            ws.sheet_state = "hidden"
            continue
        ws.freeze_panes = None
        ws.print_area = wanted[ws.title]
        ws.page_setup.orientation = "landscape"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToHeight = 1
        ws.page_setup.fitToWidth = 1
        ws.print_options.gridLines = False
    wb.active = wb.sheetnames.index(areas[0][0])
    x = os.path.join(tmp, "shots.xlsx")
    wb.save(x)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, x], check=True, capture_output=True,
                   timeout=240)
    subprocess.run(["pdftoppm", "-r", "120", "-png", os.path.join(tmp, "shots.pdf"), os.path.join(tmp, "p")], check=True)
    pages = sorted(glob.glob(os.path.join(tmp, "p-*.png")))
    order = [ws.title for ws in wb.worksheets if ws.title in wanted]
    out = []
    for name, png in zip(order, pages):
        idx = [n for n, _ in areas].index(name) + 1
        dst = os.path.join(outdir, f"screen-{idx}.png")
        subprocess.run(["convert", png, "-trim", "-bordercolor", "white", "-border", "24", "-resize", "1400x>", dst], check=True)
        subprocess.run(["convert", dst, "-quality", "82", dst[:-4] + ".webp"], check=True)
        out.append(dst)
    shutil.rmtree(tmp)
    return out


if __name__ == "__main__":
    print(render(sys.argv[1], sys.argv[2]))
