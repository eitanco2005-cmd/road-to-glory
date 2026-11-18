// Private stats for the manager. Requires header X-Stats-Token whose SHA-256 matches TOKEN_SHA256 (token itself is never in the repo).
import { getStore } from "@netlify/blobs";
import { createHash, timingSafeEqual } from "node:crypto";

// Only the SHA-256 of the token is stored here (safe to publish). Env STATS_TOKEN still works as an override.
const TOKEN_SHA256 = "ef3a8d353b78cca64b3d72589ea7452ff4a8d7e8ada8978e0e31eaf401ae679c";
const sha = (s) => createHash("sha256").update(String(s)).digest();
const authed = (given) => {
  const env = process.env.STATS_TOKEN;
  if (env) return given === env;
  if (!given) return false;
  return timingSafeEqual(sha(given), Buffer.from(TOKEN_SHA256, "hex"));
};

const FEE_PCT = 0.054, FEE_FIXED_ILS = 1.2; // rough PayPal estimate; PayPal emails are the real record
const SRC = (ref) => !ref ? "direct" : /google\./.test(ref) ? "google" : /bing\.|duckduckgo|yahoo/.test(ref) ? "bing/ddg"
  : /whatsapp|wa\.me/.test(ref) ? "whatsapp" : /chatgpt|openai|perplexity|copilot|claude/.test(ref) ? "ai" : /github/.test(ref) ? "github" : "other:" + ref;

export default async (req) => {
  if (!authed(req.headers.get("x-stats-token") || "")) return new Response("forbidden", { status: 403 });
  const days = Math.min(90, Math.max(1, Number(new URL(req.url).searchParams.get("days")) || 7));
  const store = getStore("counter");
  const out = { days, byDay: {}, pages: {}, sources: {}, devices: {}, recent: [], browsers: {}, sales: [], totals: { visits: 0, sales: 0, revenue: {}, estProfitILS: 0 } };
  for (let i = 0; i < days; i++) {
    const day = new Date(Date.now() - i * 864e5).toISOString().slice(0, 10);
    const { blobs } = await store.list({ prefix: `ev/${day}/` });
    const row = (out.byDay[day] = { visits: 0, sales: 0 });
    for (const b of blobs) {
      const ev = await store.get(b.key, { type: "json" });
      if (!ev) continue;
      if (ev.t === "visit") {
        row.visits++; out.totals.visits++;
        out.pages[ev.path] = (out.pages[ev.path] || 0) + 1;
        const s = SRC(ev.ref); out.sources[s] = (out.sources[s] || 0) + 1;
        out.devices[ev.device] = (out.devices[ev.device] || 0) + 1;
        if (ev.ua) out.browsers[ev.ua] = (out.browsers[ev.ua] || 0) + 1;
        if (out.recent.length < 30) out.recent.push({ at: day + " " + b.key.split("/")[2].slice(0, 8) + " UTC", path: ev.path, src: SRC(ev.ref), device: ev.device, ua: ev.ua || "?", lang: ev.lang, country: ev.country || "?" });
      } else if (ev.t === "sale") {
        row.sales++; out.totals.sales++;
        out.totals.revenue[ev.cur] = (out.totals.revenue[ev.cur] || 0) + ev.amount;
        if (ev.cur === "ILS") out.totals.estProfitILS += ev.amount * (1 - FEE_PCT) - FEE_FIXED_ILS;
        out.sales.push({ day, slug: ev.slug, amount: ev.amount, cur: ev.cur, status: ev.status });
      }
    }
  }
  out.totals.estProfitILS = Math.round(out.totals.estProfitILS);
  out.pages = Object.fromEntries(Object.entries(out.pages).sort((a, b) => b[1] - a[1]).slice(0, 40));
  return Response.json(out);
};

export const config = { path: "/api/stats" };
