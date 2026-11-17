#!/usr/bin/env python3
"""Submit every URL in docs/sitemap.xml to IndexNow (Bing, Yandex, Seznam...; also feeds DuckDuckGo/ChatGPT search).
Run after deploying:  python3 tools/site/indexnow.py
The key file docs/7562c085e83648f8a5a839aa4b234c89.txt must be live first."""
import json, pathlib, re, sys, urllib.parse, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from site_config import BASE_URL as BASE  # noqa: E402
KEY = "7562c085e83648f8a5a839aa4b234c89"
HOST = urllib.parse.urlparse(BASE).hostname
sm = (pathlib.Path(__file__).resolve().parents[2] / "docs/sitemap.xml").read_text(encoding="utf-8")
urls = re.findall(r"<loc>(.*?)</loc>", sm)
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": BASE + KEY + ".txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, f"({len(urls)} urls)")
except urllib.error.HTTPError as e:
    print("IndexNow error:", e.code, e.read()[:200])
