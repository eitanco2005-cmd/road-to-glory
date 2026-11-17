# Road to Glory: master plan

*Owner: you. Manager: Claude (this session). Written 2026-11-17, updated as we go.*

---

## 1. The goal in one line

**Earn ₪3,600 (≈ $1,000) profit by selling Hebrew digital products online. Then keep growing past that, with no customer contact or ads from you.**

- Profit = sales − PayPal fees. We have no other costs: hosting is free and we build everything ourselves.
- PayPal Israel takes ≈ 5–6% + a small fixed fee per sale. On a ₪45 sale we keep ≈ ₪41.
- **₪3,600 ÷ ₪41 ≈ 88 sales.** That's the number we're chasing.

---

## 2. Honest forecast (read this first)

We sell only through Google search (people find us, nobody gets contacted). Google takes **2–6 weeks** to start sending traffic to a new site, so sales start slowly and then build up.

| By date | Cautious | Expected | With the optional social boost (section 9) |
|---|---|---|---|
| Dec 6 (original 30-day deadline) | ₪0–200 | ₪200–500 | ₪500–1,500 |
| Dec 31 | ₪300–800 | ₪800–1,800 | ₪1,500–3,600 |
| Jan 31 (budget season peak) | ₪800–2,000 | ₪2,000–3,600 ✅ | ₪3,600+ ✅ |
| Feb 28 | ₪1,500–3,600 | ₪3,600+ ✅ | ₪6,000+ |

**Bottom line:** reaching the goal by Dec 6 is unlikely after the 11-day pause and with search traffic alone. **Late January is realistic.** January is our best month, because people search "תקציב משפחתי 2027" and plan the year. The plan is built to be fully ready before then.

---

## 3. What we sell

Chosen from the research (`research/products.md`). Each product gets a free tool that brings people in from Google, and the free tool leads to the paid product.

| # | Paid product | Price | Free tool that brings traffic | Why it should sell |
|---|---|---|---|---|
| 1 | **Wedding planner** (Excel + Google Sheets): budget, guests, gifts, vendors, timeline | ₪49 | "כמה לשים בחתונה 2026" calculator | Big money event; no Hebrew paid product exists |
| 2 | **Household budget Pro** (Excel + Sheets): monthly + yearly, Israeli categories, dashboard | ₪39 | 50/30/20 budget calculator | Israeli competitor sells at ₪99–120; peak demand in January |
| 3 | **עוסק פטור 2026 tracker**: income, expenses, ₪122,833 ceiling gauge | ₪39 | Ceiling calculator ("כמה נשאר לי עד התקרה") | Every new freelancer needs one; demand all year |
| 4 | **Bar/Bat mitzvah planner** | ₪39 | Cost estimator | Reuses the wedding engine, so it's cheap to build |
| 5 | **Price-quote template pack** (הצעת מחיר): Word + Sheets | ₪29 | VAT 18% calculator | Small businesses search this constantly |
| 6 | **Renovation budget planner** | ₪39 | Renovation cost estimator | High stakes, little Hebrew supply |

**Bundles (higher order value):**
- "Event bundle" (wedding + bar mitzvah) ₪69
- "Money bundle" (household budget + renovation) ₪59
- "Freelancer bundle" (עוסק פטור + quotes) ₪55
- "Everything" ₪129

**Later products (Phase 3):** English versions of the best sellers for worldwide buyers, baby/birth budget, moving-apartment checklist, debt-payoff planner, small-business cash-flow sheet. We pick these from which free tools get the most visits.

---

## 4. How the machine works

```
Google search  →  free tool / guide page (Hebrew)  →  product page
      →  PayPal checkout (your account)  →  instant download page
      →  sale recorded in our sales log  →  manager updates profit
```

- **Website:** Hebrew, right-to-left, fast, mobile-first. One page per product, one page per free tool, plus helpful guide articles.
- **Hosting:** GitHub Pages (free). Fallback: a free Hugging Face Space if Pages can't be turned on.
- **Checkout:** PayPal buttons using your Live Client ID (already saved). Buyers pay **into** your account; nothing can pay out.
- **Delivery:** after payment, the buyer gets a download page plus a Google Sheets "make a copy" link.
- **Sales log:** each completed checkout records the order number, product and amount in a log that only we use. I calculate profit from it. Your PayPal emails are the official record.
- **Legal basics on the site:** terms of sale, digital-goods cancellation policy (as Israeli consumer law requires), privacy policy, accessibility statement.

---

## 5. The team (Claude sessions)

| Worker | Job | Runs |
|---|---|---|
| **Manager** (this session) | Plans, assigns, reviews, merges, tracks money, reports to you | Whole project |
| **W1 Platform** | Site skeleton, Hebrew design, PayPal checkout, download pages, sales log, legal pages | Week 1 |
| **W2 Event products** | Wedding planner, bar mitzvah planner, their calculators | Week 1–2 |
| **W3 Money products** | Household budget, renovation planner, 50/30/20 calculator | Week 1–2 |
| **W4 Freelancer products** | עוסק פטור tracker, quote pack, ceiling + VAT calculators | Week 1–2 |
| **W5 Content / SEO** | 2–3 genuinely useful Hebrew guides per product, internal links, sitemap | Week 2 onward |
| **QA reviewer** | Tests every page on phone + desktop, checks formulas, checkout, Hebrew text | Before each launch |

Workers run in parallel on their own branches. The manager reviews and merges into the live site.

---

## 6. Timeline

### Phase 1: Build (Nov 17 – Nov 24)
- [x] PayPal Business + Live app ready
- [x] Product research done
- [ ] Day 1–2: platform + design + checkout working end to end
- [ ] Day 2–5: products 1–3 built, tested, priced, with free tools
- [ ] Day 5–7: products 4–6 + bundles
- [ ] Day 7: **site live**, sitemap ready, first ₪1 test purchase by the manager's test flow

### Phase 2: Get found (Nov 25 – Dec 31)
- Publish 2 new guide articles every day for the first two weeks, then 3 per week
- Add a new free tool each week (the tools are what Google loves)
- Prepare the **January budget campaign** pages by Dec 20: "תקציב 2027", "איך לחסוך ב-2027"
- Weekly: look at which pages get visits, improve titles, and make more of what works

### Phase 3: Hit the goal (Jan 1 – Feb 28)
- January push on budget products
- Launch English versions of the top 2 products
- Price tests: try ₪49 vs ₪59 on the bestseller, and add bundles at checkout
- **Goal: ₪3,600 profit** 🎯

### Phase 4: Keep going (March onward)
- Every month: add 2 products and 2 free tools in proven categories
- Seasonal calendar: weddings (spring/summer), עוסק פטור annual report (Apr–May), back to school (Aug), holidays
- Bigger "kits" at ₪99–149
- Next goal: ₪3,600 **per month**

---

## 7. Weekly rhythm (what I do without you)

- **Daily:** check workers, merge finished work, update `ops/STATUS.md`
- **Every 2–3 days:** short report to you: what's live, visits, sales, profit, next step
- **Weekly:** review numbers, decide what to build more of and what to drop

**Decision rules:**
- A free tool with traffic but no sales → improve the product page and price
- A product with zero visits after 3 weeks → rewrite its page, or replace the product
- Anything selling → build related products and a bundle around it

---

## 8. Numbers we track

| Metric | Where it comes from |
|---|---|
| Sales, revenue, fees, **profit** | Your PayPal emails: not tracked by us (owner: no public tracking, no questions). Reports cover progress + traffic signals only |
| Visits per page | A simple, privacy-friendly visit counter on the site |
| Conversion (visits → sales) | The two above |
| Google impressions | Only if you verify the site in Google Search Console (optional, about 2 min) |

Live numbers: `ops/STATUS.md`.

---

## 9. Optional boosts (only if you say yes)

None of these are needed. Each one speeds things up.

| Boost | What you'd do | Effect |
|---|---|---|
| **Turn on GitHub Pages** | 1 click: repo → Settings → Pages → `main` / `docs` | Better hosting and Google ranking than the fallback |
| **Google Search Console** | Log in with Google and click "verify" (I give the exact steps) | Google indexes us faster, and I see what people search |
| **Social boost** | Say "yes, you may post to my TikTok/Instagram/YouTube" | I make short, helpful videos ("כמה לשים בחתונה?") and post them to your existing accounts. This is publishing content, not messaging anyone, and could make sales arrive weeks earlier. I'll **never** post there without your explicit yes. |
| **Own domain** (≈ ₪40/year) | Buy it once | More trust and better ranking |

---

## 10. Risks and how we handle them

| Risk | Plan |
|---|---|
| Google traffic slower than expected | More free tools, January campaign, optional social boost |
| A product doesn't sell | Decision rules in section 7: replace it fast |
| Someone shares a download link without paying | Low prices make this a small loss; we'll add stronger protection if it becomes a problem |
| PayPal fees higher than assumed | We'll recalculate once the first sale shows the real fee |
| Tax / legal | Open an **עוסק פטור** once sales start (free, online). I'll walk you through it. Products avoid giving tax advice. |
| Wrong numbers in a spreadsheet | QA reviewer checks every formula. Tax figures cite their official source and date. |

---

## 11. What you need to do

**Nothing is required.** Optional boosts are in section 9, and PayPal will email you when money arrives.
