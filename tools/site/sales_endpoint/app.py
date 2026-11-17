"""Tichnun Plus (תכנון פלוס) sales log + visit counter.

Tiny FastAPI app (Hugging Face Docker Space friendly) that appends sales and visits to JSON-lines files
and serves a token-protected summary. See README.md for deploy steps.

Endpoints
  POST /sale       body: {"orderId","slug","amount","currency","test","status","ts","page"}   (any content type)
  POST /visit      body: {"path","ref","device","lang","ts"}
  GET  /summary    Authorization: Bearer <SUMMARY_TOKEN>  (or ?token=)  -> money + traffic numbers
  GET  /export/{sales|visits|verifications}  same auth -> raw JSON lines
  GET  /health

Environment
  SUMMARY_TOKEN       required for /summary and /export (if unset those endpoints are disabled)
  DATA_DIR            where the .jsonl files live (default /data if it exists, else ./data)
  ALLOWED_ORIGINS     comma-separated CORS origins (default "*")
  FEE_PCT, FEE_FIXED  PayPal fee estimate per sale (default 0.054 and 1.20 ILS)
  PAYPAL_CLIENT_ID, PAYPAL_SECRET, PAYPAL_ENV(live|sandbox)
                      optional: verify each order against the PayPal Orders API (secret stays server-side)
  HF_TOKEN, HF_DATASET_REPO
                      optional: back up the .jsonl files to a private HF dataset repo (free Spaces lose disk on restart)
  BACKUP_EVERY_SEC    visit backup interval (default 600). Sales are backed up right away.
"""
from __future__ import annotations

import base64
import collections
import datetime as dt
import json
import os
import pathlib
import re
import threading
import time
import urllib.error
import urllib.request
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

# ---------------------------------------------------------------- config
_default_dir = "/data" if os.path.isdir("/data") and os.access("/data", os.W_OK) else "./data"
DATA_DIR = pathlib.Path(os.environ.get("DATA_DIR", _default_dir))
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILES = {k: DATA_DIR / f"{k}.jsonl" for k in ("sales", "visits", "verifications")}
SUMMARY_TOKEN = os.environ.get("SUMMARY_TOKEN", "")
FEE_PCT = float(os.environ.get("FEE_PCT", "0.054"))
FEE_FIXED = float(os.environ.get("FEE_FIXED", "1.20"))
ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "*").split(",") if o.strip()]
PP_ID = os.environ.get("PAYPAL_CLIENT_ID", "")
PP_SECRET = os.environ.get("PAYPAL_SECRET", "")
PP_API = "https://api-m.sandbox.paypal.com" if os.environ.get("PAYPAL_ENV") == "sandbox" else "https://api-m.paypal.com"
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_REPO = os.environ.get("HF_DATASET_REPO", "")
BACKUP_EVERY = int(os.environ.get("BACKUP_EVERY_SEC", "600"))
MAX_BODY = 4096

SLUG_RE = re.compile(r"^[a-z0-9-]{1,64}$")
ORDER_RE = re.compile(r"^[A-Za-z0-9_-]{4,64}$")
lock = threading.Lock()
dirty = {"visits": False}

app = FastAPI(title="Tichnun Plus sales log", docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(CORSMiddleware, allow_origins=ORIGINS, allow_methods=["GET", "POST", "OPTIONS"],
                   allow_headers=["Content-Type", "Authorization"], allow_credentials=False, max_age=86400)


# ---------------------------------------------------------------- storage
def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def append(kind: str, rec: dict) -> None:
    line = json.dumps(rec, ensure_ascii=False, separators=(",", ":"))
    with lock, FILES[kind].open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def read(kind: str) -> list[dict]:
    p = FILES[kind]
    if not p.exists():
        return []
    out = []
    with lock, p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def hf_restore() -> None:
    if not (HF_TOKEN and HF_REPO):
        return
    try:
        from huggingface_hub import hf_hub_download
        for kind, path in FILES.items():
            if path.exists() and path.stat().st_size > 0:
                continue
            try:
                src = hf_hub_download(HF_REPO, f"{kind}.jsonl", repo_type="dataset", token=HF_TOKEN, force_download=True)
                path.write_bytes(pathlib.Path(src).read_bytes())
                print(f"restored {kind}.jsonl from {HF_REPO}")
            except Exception as e:  # file may not exist yet
                print(f"restore {kind}: {type(e).__name__}")
    except ImportError:
        print("huggingface_hub not installed; backup disabled")


def hf_backup(kind: str) -> None:
    if not (HF_TOKEN and HF_REPO) or not FILES[kind].exists():
        return
    try:
        from huggingface_hub import HfApi
        HfApi(token=HF_TOKEN).upload_file(path_or_fileobj=str(FILES[kind]), path_in_repo=f"{kind}.jsonl",
                                          repo_id=HF_REPO, repo_type="dataset", commit_message=f"backup {kind}")
    except Exception as e:
        print(f"backup {kind} failed: {type(e).__name__}: {e}")


def backup_loop() -> None:
    while True:
        time.sleep(BACKUP_EVERY)
        if dirty["visits"]:
            dirty["visits"] = False
            hf_backup("visits")


hf_restore()
if HF_TOKEN and HF_REPO:
    threading.Thread(target=backup_loop, daemon=True).start()


def sale_ids() -> set[str]:
    return {s.get("orderId") for s in read("sales")}


# ---------------------------------------------------------------- helpers
async def body_json(request: Request) -> dict:
    raw = await request.body()
    if len(raw) > MAX_BODY:
        raise HTTPException(413, "too large")
    try:
        data = json.loads(raw.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(400, "bad json")
    if not isinstance(data, dict):
        raise HTTPException(400, "bad json")
    return data


def clip(v: Any, n: int = 200) -> str:
    return str(v if v is not None else "")[:n]


_hits: dict[str, collections.deque] = {}


def rate_ok(key: str, limit: int, per: float = 60.0) -> bool:
    q = _hits.setdefault(key, collections.deque())
    t = time.monotonic()
    while q and t - q[0] > per:
        q.popleft()
    if len(q) >= limit:
        return False
    q.append(t)
    if len(_hits) > 5000:
        _hits.clear()
    return True


def client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return (fwd.split(",")[0].strip() if fwd else (request.client.host if request.client else "?"))


def check_token(request: Request) -> None:
    if not SUMMARY_TOKEN:
        raise HTTPException(503, "SUMMARY_TOKEN not configured")
    auth = request.headers.get("authorization", "")
    tok = auth[7:] if auth.lower().startswith("bearer ") else request.query_params.get("token", "")
    import hmac
    if not hmac.compare_digest(tok.encode(), SUMMARY_TOKEN.encode()):
        raise HTTPException(401, "unauthorized")


def paypal_verify(order_id: str, slug: str, amount: float) -> None:
    """Background: look the order up at PayPal and record whether it is a real, completed payment."""
    rec: dict[str, Any] = {"orderId": order_id, "slug": slug, "checked": now()}
    try:
        tok_req = urllib.request.Request(
            PP_API + "/v1/oauth2/token", data=b"grant_type=client_credentials",
            headers={"Authorization": "Basic " + base64.b64encode(f"{PP_ID}:{PP_SECRET}".encode()).decode(),
                     "Content-Type": "application/x-www-form-urlencoded"})
        token = json.load(urllib.request.urlopen(tok_req, timeout=15))["access_token"]
        req = urllib.request.Request(PP_API + f"/v2/checkout/orders/{order_id}", headers={"Authorization": f"Bearer {token}"})
        order = json.load(urllib.request.urlopen(req, timeout=15))
        pu = (order.get("purchase_units") or [{}])[0]
        caps = (pu.get("payments") or {}).get("captures") or []
        cap = caps[0] if caps else {}
        breakdown = cap.get("seller_receivable_breakdown") or {}
        rec.update({
            "status": order.get("status"),
            "capture_status": cap.get("status"),
            "amount": float((cap.get("amount") or pu.get("amount") or {}).get("value", 0) or 0),
            "currency": (cap.get("amount") or pu.get("amount") or {}).get("currency_code"),
            "paypal_fee": float((breakdown.get("paypal_fee") or {}).get("value", 0) or 0) or None,
            "net": float((breakdown.get("net_amount") or {}).get("value", 0) or 0) or None,
            "reference_id": pu.get("reference_id"),
        })
        rec["verified"] = (order.get("status") == "COMPLETED" and cap.get("status") in ("COMPLETED", "PENDING")
                           and abs(rec["amount"] - amount) < 0.01)
    except urllib.error.HTTPError as e:
        rec.update({"verified": False, "error": f"HTTP {e.code}"})
    except Exception as e:  # network etc.
        rec.update({"verified": None, "error": type(e).__name__})
    append("verifications", rec)
    hf_backup("verifications")


# ---------------------------------------------------------------- routes
@app.get("/health")
def health():
    return {"ok": True, "time": now(), "paypal_verify": bool(PP_ID and PP_SECRET), "backup": bool(HF_TOKEN and HF_REPO)}


@app.post("/sale")
async def sale(request: Request, bg: BackgroundTasks):
    if not rate_ok("sale:" + client_key(request), 20):
        raise HTTPException(429, "slow down")
    d = await body_json(request)
    order_id, slug = clip(d.get("orderId"), 64), clip(d.get("slug"), 64)
    if not ORDER_RE.match(order_id) or not SLUG_RE.match(slug):
        raise HTTPException(400, "bad order or slug")
    try:
        amount = round(float(d.get("amount", 0)), 2)
    except (TypeError, ValueError):
        raise HTTPException(400, "bad amount")
    if not (0 <= amount < 100000):
        raise HTTPException(400, "bad amount")
    if order_id in sale_ids():
        return {"ok": True, "duplicate": True}
    test = bool(d.get("test")) or order_id.startswith("TEST-")
    rec = {"orderId": order_id, "slug": slug, "amount": amount, "currency": clip(d.get("currency") or "ILS", 3).upper(),
           "test": test, "status": clip(d.get("status"), 20), "client_ts": clip(d.get("ts"), 40),
           "page": clip(d.get("page"), 200), "origin": clip(request.headers.get("origin"), 100), "ts": now()}
    append("sales", rec)
    bg.add_task(hf_backup, "sales")
    if PP_ID and PP_SECRET and not test:
        bg.add_task(paypal_verify, order_id, slug, amount)
    return {"ok": True}


@app.post("/visit")
async def visit(request: Request):
    if not rate_ok("visit:" + client_key(request), 120):
        return JSONResponse({"ok": False}, status_code=429)
    d = await body_json(request)
    path = clip(d.get("path"), 200)
    if not path.startswith("/"):
        raise HTTPException(400, "bad path")
    append("visits", {"path": path, "ref": clip(d.get("ref"), 100), "device": clip(d.get("device"), 10),
                      "lang": clip(d.get("lang"), 8), "ts": now()})
    dirty["visits"] = True
    return {"ok": True}


def _summary(days: int | None = None) -> dict:
    sales, visits, ver = read("sales"), read("visits"), read("verifications")
    if days:
        cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).isoformat()
        sales = [s for s in sales if s.get("ts", "") >= cutoff]
        visits = [v for v in visits if v.get("ts", "") >= cutoff]
    vmap = {v["orderId"]: v for v in ver}
    real = [s for s in sales if not s.get("test")]
    rejected = [s for s in real if vmap.get(s["orderId"], {}).get("verified") is False]
    counted = [s for s in real if s not in rejected]

    by_cur: dict[str, dict] = {}
    by_product: dict[str, dict] = {}
    by_day_sales: dict[str, dict] = {}
    for s in counted:
        v = vmap.get(s["orderId"], {})
        fee = v.get("paypal_fee") if v.get("paypal_fee") is not None else round(s["amount"] * FEE_PCT + FEE_FIXED, 2)
        c = by_cur.setdefault(s["currency"], {"sales": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
        c["sales"] += 1
        c["gross"] += s["amount"]
        c["fees"] += fee
        c["net"] += s["amount"] - fee
        p = by_product.setdefault(s["slug"], {"sales": 0, "gross": 0.0})
        p["sales"] += 1
        p["gross"] += s["amount"]
        day = by_day_sales.setdefault(s["ts"][:10], {"sales": 0, "gross": 0.0})
        day["sales"] += 1
        day["gross"] += s["amount"]
    for c in by_cur.values():
        for k in ("gross", "fees", "net"):
            c[k] = round(c[k], 2)

    paths = collections.Counter(v.get("path") for v in visits)
    refs = collections.Counter(v.get("ref") or "(direct/none)" for v in visits)
    devices = collections.Counter(v.get("device") or "?" for v in visits)
    vdays = collections.Counter((v.get("ts") or "")[:10] for v in visits)
    return {
        "generated": now(),
        "window_days": days,
        "money": {
            "currencies": by_cur,
            "fee_model": {"pct": FEE_PCT, "fixed": FEE_FIXED, "note": "estimate unless PayPal verification gave the real fee"},
            "by_product": dict(sorted(by_product.items(), key=lambda kv: -kv[1]["sales"])),
            "by_day": dict(sorted(by_day_sales.items())),
            "verified": sum(1 for s in counted if vmap.get(s["orderId"], {}).get("verified")),
            "unverified": sum(1 for s in counted if not vmap.get(s["orderId"], {}).get("verified")),
            "rejected_by_paypal_check": [s["orderId"] for s in rejected],
            "test_sales": len(sales) - len(real),
        },
        "traffic": {
            "visits": len(visits),
            "by_day": dict(sorted(vdays.items())),
            "top_pages": dict(paths.most_common(50)),
            "referrers": dict(refs.most_common(30)),
            "devices": dict(devices),
        },
        "conversion": round(len(counted) / len(visits), 4) if visits else None,
    }


@app.get("/summary")
def summary(request: Request, days: int | None = None):
    check_token(request)
    return _summary(days)


@app.get("/export/{kind}")
def export(kind: str, request: Request):
    check_token(request)
    if kind not in FILES:
        raise HTTPException(404, "unknown")
    p = FILES[kind]
    return PlainTextResponse(p.read_text(encoding="utf-8") if p.exists() else "", media_type="application/x-ndjson")
