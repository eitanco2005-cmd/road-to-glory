// Private visit/sale counter: the site POSTs tiny anonymous events here (no cookies, no IPs, no names).
// Each event is stored as its own blob (race-free), grouped by day: ev/YYYY-MM-DD/<time>-<rand>.
import { getStore } from "@netlify/blobs";

const BOT = /bot|crawl|spider|slurp|preview|headless|lighthouse|facebookexternalhit|whatsapp|telegram/i;
const clip = (v, n) => String(v ?? "").slice(0, n);

export default async (req) => {
  if (req.method !== "POST") return new Response("ok");
  let d;
  try { d = JSON.parse(await req.text()); } catch { return new Response("bad", { status: 400 }); }
  const ua = req.headers.get("user-agent") || "";
  if (BOT.test(ua)) return new Response("ok");
  const now = new Date();
  const day = now.toISOString().slice(0, 10);
  const ev = d.type === "sale"
    ? { t: "sale", slug: clip(d.slug, 60), amount: Math.max(0, Math.min(10000, Number(d.amount) || 0)),
        cur: clip(d.currency, 3).toUpperCase(), test: !!d.test, status: clip(d.status, 20), order: clip(d.orderId, 40) }
    : { t: "visit", path: clip(d.path, 160), ref: clip(d.ref, 80), device: clip(d.device, 10), lang: clip(d.lang, 5) };
  if (ev.t === "sale" && ev.test) return new Response("ok"); // test purchases are never counted
  const key = `ev/${day}/${now.toISOString().slice(11, 23)}-${Math.random().toString(36).slice(2, 8)}`;
  await getStore("counter").setJSON(key, ev);
  return new Response("ok", { headers: { "access-control-allow-origin": "*" } });
};

export const config = { path: "/api/hit" };
