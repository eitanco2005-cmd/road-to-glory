"""Run: pip install fastapi httpx && python -m pytest -q tools/site/sales_endpoint/test_app.py"""
import importlib
import os
import sys
import tempfile

from fastapi.testclient import TestClient


def make_client(tmp):
    os.environ.update(DATA_DIR=tmp, SUMMARY_TOKEN="s3cret", FEE_PCT="0.05", FEE_FIXED="1")
    for k in ("PAYPAL_CLIENT_ID", "PAYPAL_SECRET", "HF_TOKEN", "HF_DATASET_REPO"):
        os.environ.pop(k, None)
    sys.path.insert(0, os.path.dirname(__file__))
    import app as appmod
    importlib.reload(appmod)
    return TestClient(appmod.app)


def test_flow():
    with tempfile.TemporaryDirectory() as tmp:
        c = make_client(tmp)
        assert c.get("/health").json()["ok"]
        h = {"Content-Type": "text/plain;charset=UTF-8"}
        r = c.post("/sale", content='{"orderId":"5O190127TN364715T","slug":"wedding-planner","amount":49,"currency":"ILS"}', headers=h)
        assert r.json() == {"ok": True}
        assert c.post("/sale", content='{"orderId":"5O190127TN364715T","slug":"wedding-planner","amount":49}', headers=h).json()["duplicate"]
        c.post("/sale", content='{"orderId":"TEST-ABC","slug":"wedding-planner","amount":49,"test":true}', headers=h)
        assert c.post("/sale", content='{"orderId":"x","slug":"../etc"}', headers=h).status_code == 400
        assert c.post("/sale", content="not json", headers=h).status_code == 400
        for p in ("/", "/", "/p/wedding-planner/"):
            assert c.post("/visit", content='{"path":"%s","device":"mobile"}' % p, headers=h).json()["ok"]
        assert c.get("/summary").status_code == 401
        assert c.get("/summary?token=wrong").status_code == 401
        s = c.get("/summary", headers={"Authorization": "Bearer s3cret"}).json()
        ils = s["money"]["currencies"]["ILS"]
        assert ils["sales"] == 1 and ils["gross"] == 49 and ils["fees"] == 3.45 and ils["net"] == 45.55
        assert s["money"]["test_sales"] == 1
        assert s["traffic"]["visits"] == 3 and s["traffic"]["top_pages"]["/"] == 2
        assert "TEST-ABC" in c.get("/export/sales?token=s3cret").text
        # CORS preflight-free simple request from the site
        r = c.post("/visit", content='{"path":"/x"}', headers={**h, "Origin": "https://eitanco2005-cmd.github.io"})
        assert r.headers.get("access-control-allow-origin") in ("*", "https://eitanco2005-cmd.github.io")
