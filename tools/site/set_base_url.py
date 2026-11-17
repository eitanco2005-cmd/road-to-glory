#!/usr/bin/env python3
"""Move the site to a new public base URL in one step.

    python3 tools/site/set_base_url.py https://tichnun.co.il/

Replaces the current site_config.BASE_URL everywhere it is baked in: tools/site/site_config.py,
SITE_URL in docs/assets/config.js, every canonical / og:url / og:image / JSON-LD URL in docs/
(hand-written and generated pages alike), tools/site/templates/ and README.md. Then rebuilds
docs/sitemap.xml + robots.txt. Generators read BASE_URL from site_config.py, so re-running them
afterwards gives the same result. The site must be served from the domain root.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
from site_config import BASE_URL as OLD  # noqa: E402

EXTS = {".html", ".xml", ".txt", ".json", ".js", ".md"}


def main():
    if len(sys.argv) != 2 or not re.match(r"^https://[a-z0-9.-]+/?$", sys.argv[1]):
        sys.exit("usage: set_base_url.py https://host/   (domain root only, no sub-path)")
    new = sys.argv[1].rstrip("/") + "/"
    if new == OLD:
        print("BASE_URL already", new)
    files = [p for p in (REPO / "docs").rglob("*") if p.suffix in EXTS and "/dl/" not in p.as_posix()]
    files += list((HERE / "templates").glob("*.html")) + [REPO / "README.md"]
    n = 0
    for p in files:
        s = p.read_text(encoding="utf-8")
        if OLD in s:
            p.write_text(s.replace(OLD, new), encoding="utf-8")
            n += 1
    cfg = HERE / "site_config.py"
    cfg.write_text(cfg.read_text(encoding="utf-8").replace(f'BASE_URL = "{OLD}"', f'BASE_URL = "{new}"'), encoding="utf-8")
    js = REPO / "docs/assets/config.js"
    js.write_text(re.sub(r'SITE_URL: "[^"]*"', f'SITE_URL: "{new}"', js.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{OLD} -> {new}: {n} file(s) rewritten")
    subprocess.run([sys.executable, str(HERE / "build_site.py"), "--base", new], check=True)


if __name__ == "__main__":
    main()
