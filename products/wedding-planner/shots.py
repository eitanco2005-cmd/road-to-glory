"""Render product screenshots: demo workbook -> limited print areas -> LibreOffice PDF -> PNG pages."""
import os, subprocess, sys, glob, shutil, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from event_engine import build_workbook

AREAS = {"דשבורד": "A1:I39", "תקציב": "A1:I26", "מוזמנים": "A1:N26", "תשלומים": "A1:J16",
         "צ'קליסט": "A1:H24", "הושבה": "A1:I20"}

def render(cfg, outdir, prefix):
    tmp = os.path.join(outdir, "_tmp"); os.makedirs(tmp, exist_ok=True)
    wb = build_workbook(cfg, demo=True)
    for name in list(wb.sheetnames):
        if name not in AREAS:
            wb[name].sheet_state = "hidden"
        else:
            ws = wb[name]; ws.print_area = AREAS[name]
            ws.page_setup.fitToHeight = 1; ws.page_setup.fitToWidth = 1
            ws.print_options.gridLines = False
    wb.active = wb.sheetnames.index("דשבורד")
    x = os.path.join(tmp, "shots.xlsx"); wb.save(x)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, x], check=True, capture_output=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", os.path.join(tmp, "shots.pdf"), os.path.join(tmp, "p")], check=True)
    pages = sorted(glob.glob(os.path.join(tmp, "p-*.png")))
    order = [n for n in wb.sheetnames if n in AREAS]
    out = []
    for name, png in zip(order, pages):
        dst = os.path.join(outdir, f"{prefix}-{list(AREAS).index(name)+1}.png")
        subprocess.run(["convert", png, "-trim", "-bordercolor", "white", "-border", "24", "-resize", "1400x>", dst], check=True)
        out.append(dst)
    shutil.rmtree(tmp)
    return out

if __name__ == "__main__":
    from build import CFG
    print(render(CFG, sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "out"), "wedding"))
