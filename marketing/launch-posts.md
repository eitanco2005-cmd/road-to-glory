# Launch posts — "Local Business Landing Page Pack" (template pack, bet #2)

Owner posts these from their own accounts. Replace `GUMROAD_URL`, `PREVIEW_URL`
(GitHub Pages demo of the templates) and `{name}`. Price assumed $24 (launch $19 for
first 48h — only say this if it's true).

**Honesty rules:** disclose you're the maker in every post. No sockpuppets, no asking
friends to upvote, no fake "I found this cool product". Don't post the same text to
many subreddits on the same day (Reddit treats that as spam) — space them ≥ 2 days apart
and tailor each one.

## Reddit — where it's allowed

Rules below come from third-party guides and Reddit mirrors (Reddit itself wasn't
directly searchable), so **read each sub's sidebar/wiki before posting** — rules change.

| Subreddit | Self-promo stance | How to post | Source |
|---|---|---|---|
| r/SideProject | Most promotion-friendly for makers, but feedback-first: posts that are pure ads get poor reception | Post as "I built X, looking for feedback", answer every comment | [teract.ai][r1], [hiveindex][r2], [IH thread][r3] |
| r/webdev | General commercial promotion banned; 9:1 rule; projects only in **Showoff Saturday** (Saturdays). Even there, purely commercial posts have been removed | Saturday only, lead with the build (no framework, CSS vars, a11y), link to free preview; mention price only in a comment if asked | [r/webdev mirror][r4], [openskillindex][r5], [yomotherboard][r6] |
| r/web_design | Feedback only in the **weekly feedback thread**, using their template (URL / Purpose / Technologies / Feedback requested). Circumventing self-promo rules = ban | Comment in weekly thread asking for design feedback on the templates; no sales link | [r/web_design mirror][r7], [feedback thread][r8] |
| r/EntrepreneurRideAlong | Mods cracking down on promo; value-first write-ups welcome | Post a genuine build log (numbers, what worked); product link at the end, once | [r/ERA snapshot][r9] |
| r/Entrepreneur, r/SaaS | Reported to allow promotion only in specific weekly threads | Use their weekly promo thread only | [teract.ai][r1] |

**Skip:** r/smallbusiness (no clear self-promo allowance found), city subreddits
(local business rules vary, high ban risk).

### Post 1 — r/SideProject

**Title:** `I built 6 no-framework landing page templates for local businesses — would love feedback`

```
Hey all — I've been building one-page websites for small local businesses (plumbers, salons, cafés…) and kept rewriting the same sections. So I turned them into a pack of 6 templates:

• Restaurant/café, salon, trades, dental clinic, gym, real estate agent
• Plain HTML + CSS, no build step, no framework — open in any editor
• Brand colours and fonts are CSS variables at the top of each file
• Mobile-first, accessible (semantic HTML, contrast-checked, keyboard-friendly)
• Deploy free on Netlify or GitHub Pages (guide included)

Live previews: PREVIEW_URL

Disclosure: I sell the pack ($24, GUMROAD_URL) — but I'm mainly after feedback:
1. Which template looks weakest?
2. Anything that would stop you using this for a client?

Happy to answer anything about the build.
```

### Post 2 — r/webdev (Showoff Saturday only)

**Title:** `[Showoff Saturday] 6 single-file landing page templates — zero JS frameworks, theming via CSS custom properties`

```
Built these for local-business sites. Each one is a single HTML file + one CSS file, themed entirely through ~10 custom properties (colours, fonts, radius). No build tools.

Things I'd love critique on:
- Layout: CSS grid + clamp() for fluid type, no media-query soup
- Accessibility: skip link, landmarks, focus styles, prefers-reduced-motion
- Lighthouse: {fill in real scores from previews}

Previews: PREVIEW_URL

(They're part of a paid pack, but the previews are all public and I'm here for the code review.)
```

### Post 3 — r/web_design weekly feedback thread (comment)

```
URL: PREVIEW_URL
Purpose: One-page templates for local businesses (salon, trades, clinic, gym, restaurant, real estate)
Technologies used: HTML, CSS (custom properties, grid), no JS framework
Feedback requested: Visual hierarchy of the hero sections and whether the trades template feels trustworthy enough for an older customer base.
```

### Post 4 — r/EntrepreneurRideAlong (after ~2 weeks, with real numbers)

**Title:** `Selling websites to local businesses with $0 budget: what 2 weeks of walk-ins and cold calls taught me`

Write after the fact with true numbers: contacts made, reply rate, objections heard,
what closed. Mention the template pack once, at the end. Template:

```
Context: I set myself a goal of $1,000 in 30 days selling $149 one-page websites to local businesses, with no ads and no reviews.

What I did:
- {N} businesses found on Google Maps with no website
- {N} calls / {N} walk-ins / {N} emails
- {N} replies, {N} clients

What worked: {…}
What didn't: {…}
Biggest objection: {…} and how I answered it

I also packaged my templates for other freelancers (GUMROAD_URL) — happy to answer questions about either side.
```

## IndieHackers

Post in the main feed (and "Building in Public" / "Show IH" if available). IH culture
rewards numbers and honesty.

**Title:** `Launching a $24 landing page pack built from real local-business work`

```
Hi IH 👋

I'm running a 30-day experiment: make $1,000 profit from scratch by building one-page websites for local businesses (fixed $149/$299, 48h delivery).

Doing the client work, I noticed every site uses the same 6–7 sections. So I packaged them into a template pack for freelancers and small business owners who want to DIY:

- 6 templates: restaurant, salon, trades, dental clinic, gym, real estate
- Plain HTML/CSS, no build step, CSS variables for branding
- Mobile-first and accessible
- Free-hosting deploy guide (Netlify / GitHub Pages)
- License: use for yourself or client projects, no resale

Price: $24 → GUMROAD_URL
Previews: PREVIEW_URL

I'll post the real numbers (sales, clients, what failed) at day 15 and day 30.

Question for you: for a $24 template pack, would you rather see more templates or a video walkthrough?
```

## X (Twitter)

**Launch thread**

```
1/ I just launched a pack of 6 landing page templates for local businesses.

Plain HTML + CSS. No framework. No build step. Change 10 CSS variables → it's your brand.

$24 → GUMROAD_URL

2/ Why: I've been building $149 websites for local businesses (plumbers, salons, cafés). Every site uses the same sections: hero + call button, services, prices, hours/map, reviews, contact.

3/ Templates: restaurant, salon, trades, dental clinic, gym, real estate agent. All mobile-first and accessible.

[attach 4 preview images from product/previews/]

4/ Deploy free on Netlify or GitHub Pages — guide included. Use for your own business or client projects.

5/ Building this in public: 30 days, $1,000 target. I'll share the numbers either way. Follow along 👋
```

**Standalone tweets (one per day for a week)**

- `Most local businesses I talk to don't need a 10-page site. They need: a call button, prices, hours, and 3 reviews. On a phone. That's it.`
- `Before/after: plumber with 40 five-star reviews and no website → one-page site with click-to-call. [image]`
- `Hot take: for a local business, a hand-written HTML page beats a $30/month site builder. Faster, free to host, nothing to break.`
- `Day {n} of trying to make $1,000 selling websites to local businesses: {real stat}.`

## LinkedIn

```
I'm doing a 30-day challenge: earn $1,000 by building simple websites for local businesses.

The surprising part so far: {real observation, e.g. "of 40 local trades businesses I looked up on Google Maps, 11 had no website at all — despite great reviews"}.

A good local business site doesn't need to be complicated:
✅ A clear "Call now" button
✅ Services and prices
✅ Opening hours and a map
✅ Real reviews
✅ Loads fast on a phone

I offer these as a fixed-price service ($149, 48 hours): PORTFOLIO_URL
And for freelancers and DIY-ers, I've packaged my templates: GUMROAD_URL

If you know a small business owner who's been meaning to "sort the website out", I'd be grateful for an intro.
```

## Posting calendar (suggested)

| Day | Channel |
|---|---|
| Launch day (pack live on Gumroad) | X thread, LinkedIn, IndieHackers |
| +1 | r/SideProject |
| next Saturday | r/webdev Showoff Saturday |
| same week | r/web_design weekly feedback thread |
| +14 | r/EntrepreneurRideAlong build log, IH update with numbers |
| +30 | Final IH + X + LinkedIn results post |

Reply to every comment within a few hours on launch day — engagement matters more
than the post itself.

[r1]: https://www.teract.ai/resources/reddit-subreddit-marketing-2026
[r2]: https://thehiveindex.com/communities/side-project/
[r3]: https://www.indiehackers.com/post/what-subreddits-have-you-found-that-actually-allow-and-encourage-self-promotion-864d4da1cd
[r4]: https://r-weld.vercel.app/r/webdev
[r5]: https://openskillindex.com/skills/jonathimer-devmarketing-skills-reddit-engagement
[r6]: https://yomotherboard.com/answer/answer-to-why-was-my-free-front-end-website-removed-from-showoff-saturday/
[r7]: https://reddit.sentinel-team.org/subreddits/web_design/snapshots/2026-04-18T08%3A17%3A29.235978Z
[r8]: https://lr.eu.psf.lt/r/web_design/comments/1jr88ti/feedback_thread
[r9]: https://reddit.sentinel-team.org/subreddits/EntrepreneurRideAlong/snapshots/2026-02-18T19%3A27%3A09.106862Z

Sources: https://www.teract.ai/resources/reddit-subreddit-marketing-2026 ,
https://thehiveindex.com/communities/side-project/ ,
https://www.indiehackers.com/post/what-subreddits-have-you-found-that-actually-allow-and-encourage-self-promotion-864d4da1cd ,
https://r-weld.vercel.app/r/webdev ,
https://openskillindex.com/skills/jonathimer-devmarketing-skills-reddit-engagement ,
https://yomotherboard.com/answer/answer-to-why-was-my-free-front-end-website-removed-from-showoff-saturday/ ,
https://lr.eu.psf.lt/r/web_design/comments/1jr88ti/feedback_thread ,
https://reddit.sentinel-team.org/subreddits/EntrepreneurRideAlong/snapshots/2026-02-18T19%3A27%3A09.106862Z
