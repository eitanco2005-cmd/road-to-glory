---
title: Glory Sales Log
emoji: 📒
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# Glory sales log + visit counter

A tiny FastAPI app that the static site posts to. It appends every sale and page visit to JSON-lines files
and serves a **token-protected** summary (sales, revenue, estimated PayPal fees, profit, visits, conversion).
The YAML block above is the Hugging Face Space config, so this folder can be pushed as a Space as-is.

| Endpoint | Auth | What |
|---|---|---|
| `POST /sale` | none (public, validated, de-duplicated by order id, rate-limited) | called by `docs/assets/sales.js` after PayPal capture |
| `POST /visit` | none (rate-limited) | one per page per browser session |
| `GET /summary[?days=7]` | `Authorization: Bearer $SUMMARY_TOKEN` or `?token=` | JSON numbers for the manager |
| `GET /export/sales` · `/export/visits` · `/export/verifications` | same | raw JSON lines |
| `GET /health` | none | liveness + which optional features are on |

Requests from the site use `Content-Type: text/plain` (no CORS preflight). Test-mode sales (`TEST-…` ids)
are stored but excluded from money totals.

**Trust model.** `/sale` is public, because the browser calls it, so anyone could post a fake sale. Two defenses:
1. Treat PayPal emails / the PayPal dashboard as the official record (PLAN.md section 4).
2. Optional **server-side verification**: set `PAYPAL_CLIENT_ID` + `PAYPAL_SECRET` (Space *secrets*, never in the repo).
   Each sale is then looked up at the PayPal Orders API. The real fee and net amount are recorded, and anything that
   PayPal doesn't confirm is listed under `rejected_by_paypal_check` and left out of the totals.

## Environment variables

| Name | Required | Default | Notes |
|---|---|---|---|
| `SUMMARY_TOKEN` | yes | – | long random string, e.g. `python -c "import secrets;print(secrets.token_urlsafe(32))"` |
| `ALLOWED_ORIGINS` | no | `*` | e.g. `https://eitanco2005-cmd.github.io` |
| `FEE_PCT` / `FEE_FIXED` | no | `0.054` / `1.20` | fee estimate in ILS; replace with the real numbers after the first sale |
| `PAYPAL_CLIENT_ID` / `PAYPAL_SECRET` / `PAYPAL_ENV` | no | – / – / `live` | enables order verification |
| `HF_TOKEN` / `HF_DATASET_REPO` | no, but **recommended on free Spaces** | – | backs the files up to a private dataset repo (e.g. `you/glory-sales-log`); restored on startup |
| `BACKUP_EVERY_SEC` | no | `600` | visit backup interval (sales are backed up immediately) |
| `DATA_DIR` | no | `/app/data` in Docker | `/data` if you bought HF persistent storage |

> Free HF Spaces have **ephemeral disk** and sleep after ~48 h without traffic. Use the dataset backup (free) so a
> restart doesn't wipe the log. A sleeping Space wakes on the next request, but that first request can take
> ~30 s. The site doesn't wait (sales are queued in the buyer's browser and retried on the next page load), but
> a sale can still be missed. PayPal remains the source of truth.

## Deploy to a Hugging Face Docker Space

1. Create the Space: huggingface.co → **New Space** → name `glory-sales-log`, SDK **Docker**, template *Blank*,
   visibility **Public** (the site must reach it; the data is still protected by the token). Or via CLI:
   `huggingface-cli repo create glory-sales-log --type space --space_sdk docker`
2. (Recommended) create a **private dataset** `glory-sales-log-data` for backups, plus a *write* access token.
3. Space → Settings → **Variables and secrets**: add secrets `SUMMARY_TOKEN`, `HF_TOKEN`,
   and optionally `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`. Add variables `HF_DATASET_REPO=<user>/glory-sales-log-data`
   and `ALLOWED_ORIGINS=https://eitanco2005-cmd.github.io`.
4. Push this folder as the Space repo:
   ```bash
   git clone https://huggingface.co/spaces/<user>/glory-sales-log /tmp/space
   cp tools/site/sales_endpoint/{app.py,requirements.txt,Dockerfile,README.md} /tmp/space/
   cd /tmp/space && git add -A && git commit -m "Glory sales log" && git push
   ```
   (or upload the four files with `huggingface_hub.HfApi().upload_folder(...)`).
5. When the build is green, the base URL is `https://<user>-glory-sales-log.hf.space`. Check it with
   `curl https://<user>-glory-sales-log.hf.space/health`.
6. Put the endpoints in `docs/assets/config.js`:
   ```js
   SALES_ENDPOINT: "https://<user>-glory-sales-log.hf.space/sale",
   VISITS_ENDPOINT: "https://<user>-glory-sales-log.hf.space/visit",
   ```
7. Smoke test: open any product page with `?test=1`, click the test pay button, then
   `curl -H "Authorization: Bearer $SUMMARY_TOKEN" https://<user>-glory-sales-log.hf.space/summary` should show
   `test_sales: 1`.

## Run locally

```bash
pip install -r requirements.txt
SUMMARY_TOKEN=dev uvicorn app:app --port 7860
python -m pytest -q test_app.py   # needs pytest + httpx
```
