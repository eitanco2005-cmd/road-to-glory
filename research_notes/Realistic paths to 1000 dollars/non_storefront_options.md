# Non-storefront ways to earn money (bounties, bug bounties, competitions, contests) for an AI team acting via an Israeli individual's GitHub + PayPal

Research date: 2026-11-17. Note: direct fetches of docs.algora.io, docs.hackerone.com and docs.stripe.com failed (hosts not allowed in this session's network), so platform facts below come from search-result excerpts of those official pages plus secondary sources. Treat as "needs verification on the live page" where flagged.

## GitHub-native bounty platforms (Algora, Opire, IssueHunt, Gitcoin, etc.): payout rails, accounts, earnings, AI-PR problems

### Takeaway
The main GitHub-native bounty platforms (Algora, Opire, huntr) pay through **Stripe Connect, not PayPal**. Login is by GitHub, but getting paid means setting up a Stripe Connect Express account with KYC, which counts as a new account and conflicts with the owner's constraints. Maintainers are also turning hostile to AI-generated PRs, and some projects now ban them or auto-close outside PRs. That makes bounty-chasing with agent-written PRs both hard to get paid for and a reputational risk to the owner's GitHub account.

### Cited Findings
- Algora's docs say payouts go through Stripe Connect, which Algora describes as its widest country coverage; payouts typically arrive 1–3 business days after payment completes. In some countries (e.g., India, UAE), receiving international payments is limited to sole proprietors/LLPs/companies. Algora's pricing page tells earners to "check your country is supported." — [Algora docs: payments](https://docs.algora.io/bounties/payments); [Algora pricing](https://console.algora.io/pricing)
- Opire uses Stripe as its payment platform. The bounty creator pays the Stripe fee ($0.85 + 5.25%) plus a 4% Opire fee, and developers receive 100% of the bounty. Flow: claim by commenting on the issue, open a PR, get paid on merge. — [Opire docs: pricing](https://docs.opire.dev/rewards/pricing); [Opire docs: lifecycle](https://docs.opire.dev/rewards/lifecycle); [dev.to Opire walkthrough (secondary)](https://dev.to/farkharoumy/how-to-use-opire-to-find-unclaimed-github-bounties-with-real-data-from-30-live-bounties-2dj5)
- A dev.to comparison names BountyHub as a PayPal-paying alternative (unverified). — [dev.to Algora vs Opire](https://dev.to/rohan_sharma/get-ready-bounty-huntersss-algora-vs-opire-30jc)
- Israel and Stripe: 2026 guides say Israel is not on Stripe's list of supported countries for account holders, so a business registered in Israel (osek or company) cannot open a Stripe account. Several Stripe Connect platforms (ElevenLabs Voice Actor payouts, Promotekit, Remote) do list Israel as a payout destination for recipients, though. — [Adir CPA: Stripe in Israel 2026](https://adircpa.com/en/guides/stripe-israel-tax); [AgentaOS: Stripe alternatives in Israel](https://agentaos.ai/countries/israel); [ElevenLabs payout countries](https://help.elevenlabs.io/hc/en-us/articles/22975638535185-What-countries-do-you-support-for-Voice-Actor-Payouts-with-Stripe-Connect); [Promotekit Stripe payouts](https://www.promotekit.com/docs/payouts/stripe-payouts); [Remote: Stripe Connect country availability](https://support.remote.com/hc/en-us/articles/7046120384909-Stripe-Connect-Country-Availability-for-Local-Currency-Payouts)
- Gitcoin: the DAO passed a 2026 operations budget, and its governance reports still mention residual bounty payouts (e.g., the "GG24 sensemaking bounty"). The Block reported Gitcoin winding down its software division (date and scope not confirmed). Gitcoin today is mostly grants rounds and crypto public goods, not classic GitHub issue bounties. — [Gitcoin Q1 2026 budget report](https://gov.gitcoin.co/t/gitcoin-dao-q1-2026-budget-report/25247); [Gitcoin 2026 budget request](https://gov.gitcoin.co/t/passed-gitcoin-dao-2026-budget-request/25075); [The Block](https://www.theblock.co/amp/post/352055/ethereum-public-goods-funding-protocol-gitcoin-winding-down-its-software-division)
- IssueHunt: no current (2026) information on operations or payouts was found.
- AI-PR backlash:
  - Godot bans fully AI-generated PRs, and autonomous agents or "vibe-coded" PRs trigger an automatic ban. — [Neowin](https://www.neowin.net/news/godot-gives-vibe-coders-the-middle-finger-as-it-bans-ai-generated-code-contributions/)
  - tldraw began auto-closing external PRs in Jan 2026 after a flood of low-quality AI PRs. — [InfoQ, Feb 2026](https://infoq.com/news/2026/02/ai-floods-close-projects)
  - Ghostty allows AI PRs only for accepted issues. — [DevGenius](https://blog.devgenius.io/open-source-projects-are-now-banning-ai-generated-pull-requests-8e1dd3e8d41c)
  - RPCS3 bans on sight for undisclosed AI PRs. — [devtake](https://devtake.pages.dev/article/rpcs3-ai-slop-pull-requests-policy)
  - cURL shut down its bug bounty in January (2026 per coverage) after AI-generated fake reports, and now requires AI-use disclosure. — [InfoQ](https://infoq.com/news/2026/02/ai-floods-close-projects)
  - GitHub added repo controls to disable PRs, restrict them to collaborators, or cap concurrent outside PRs. — [CryptoBriefing](https://cryptobriefing.com/github-restricts-pull-requests-ai-slop/); [OpenSourceForU](https://www.opensourceforu.com/?p=96618)
  - Counterpoint: the Linux kernel allows any tools as long as the contributor understands and owns the code. — [DEVOPS.com](https://www.devops.com/reddits-r-opensource-ai-ban-targets-the-wrong-problem)

### Inferences
- **Owner constraint conflict:** collecting an Algora or Opire bounty means onboarding to Stripe Connect Express with ID and bank details, which is a new account with KYC. Under "no new accounts," these platforms are effectively unusable, even if Israel turns out to be a supported Connect recipient country.
- Bounties on these platforms are visible to everyone and fill up quickly with competing claimants, many now AI-assisted. Combined with the bans and auto-closing above, the realistic expected earnings within 30–60 days are low, and spam-like PRs could get the owner's GitHub account banned from projects or flagged.
- A safer GitHub-only form of this activity: bounties where the maintainer pays directly by PayPal or GitHub Sponsors after merge (ad hoc "I'll pay $X" issues), with AI use disclosed. These are rare and unstructured.

### Gaps
- Algora's exact payout country list and whether Israel is on it. The docs fetch was blocked, so check docs.algora.io/bounties/payments directly.
- Whether Opire supports any non-Stripe payout. None was found.
- No reliable data on typical Algora/Opire earnings or win rates. Bounty sizes seen anecdotally range from roughly $20 to $5,000, but no source was verified here.
- IssueHunt's 2026 status.

## Bug bounty platforms (HackerOne, Bugcrowd, Intigriti, huntr): KYC, tax forms, PayPal, Israel, timing, ethics

### Takeaway
HackerOne, Bugcrowd and Intigriti all support PayPal payouts, which is fast (same day to 2 days), but every one of them needs its own platform account. Each also requires ID verification and/or a tax form (W-8BEN for non-US individuals) before paying. huntr (AI/ML bounties) pays only via Stripe Connect. Under the owner's no-new-account rule none of these qualifies. They are also high-skill, high-competition, and legally restricted to authorized, in-scope programs.

### Cited Findings
- HackerOne:
  - Payout options include PayPal; HackerOne's main providers are PayPal, Coinbase and Currencycloud.
  - Payouts run Mon–Fri at 12:30 UTC and take 1–2 days, with no minimum.
  - Before any award is paid you need a valid tax form, approved identity verification, and a payment method. Tax forms renew every 3 years, and new ones are reviewed within about 72 business hours.
  - [HackerOne payment preferences](https://docs.hackerone.com/en/articles/8395720-payment-preferences); [HackerOne receiving payments](https://docs.hackerone.com/en/articles/8395706-receiving-payments); [HackerOne tax forms](https://docs.hackerone.com/hackers/tax-forms.html)
- Non-US researchers file a W-8 form (secondary source). — [beancount.io bug bounty tax guide 2026](https://beancount.io/blog/2026/09/13/bug-bounty-income-taxes-hackerone-bugcrowd-1099-hobby-business-guide)
- Bugcrowd: pays by bank transfer (1–2 business days) and PayPal (same day), with Bitcoin for select programs. A tax form must be on file before payout. — [Bugcrowd payment methods](https://docs.bugcrowd.com/researchers/payments/setting-up-payment-methods/); [Bugcrowd payment FAQ](https://docs.bugcrowd.com/researchers/payments/frequently-asked-questions-payment-methods/)
- Intigriti: five payout methods including PayPal, wire, Payoneer and UPI, with self-billing invoices. Identity verification through Onfido (documents plus biometrics) is required before joining programs. — [Intigriti payout methods](https://kb.intigriti.com/en/articles/3379502-payout-methods)
- huntr (Protect AI, AI/ML OSS bounties): payouts via Stripe Connect. If the contributor's country isn't supported, huntr offers to donate the payout to charity. Model-format vulnerability bounties go up to $3,000. — [huntr participation terms](https://huntr.com/participation-terms); [huntr model bounties](https://huntr.com/bounties/disclose/models)
- cURL ended its bug bounty because of AI-generated bogus reports, which shows how programs treat AI slop reports. — [InfoQ](https://infoq.com/news/2026/02/ai-floods-close-projects)

### Inferences
- Even ignoring account constraints, a first valid, paid report usually takes a long time: triage, then fix confirmation, then payout. Getting $1,000 inside 60 days from a new researcher profile is unlikely. AI-generated low-quality reports damage reputation (HackerOne "Signal") and can get the researcher banned.
- Legal: testing is allowed only within a program's published scope and safe-harbor policy. Unauthorized testing of systems can violate computer-misuse laws, including Israel's Computer Law 1995 and the US CFAA. This is general knowledge, not verified in this session.

### Gaps
- Whether HackerOne, Bugcrowd or Intigriti restrict Israel. No country-restriction list was found, and no evidence Israel is excluded.
- Whether PayPal payouts go to Israeli PayPal accounts in USD without issues. Not verified.

## Coding/AI competitions with cash prizes (Kaggle, Devpost, Topcoder, company challenges), Dec 2026–Jan 2027

### Takeaway
Several large Kaggle competitions close in January 2027, but **no competition prize realistically arrives by mid-January 2027**: Kaggle's own timeline is about 2–3 months from close to payment, after winner verification and tax forms. Kaggle and Devpost each need their own account (Kaggle can use Google sign-in; Devpost has its own login with GitHub/Google options per general knowledge). Prizes are top-heavy and extremely competitive.

### Cited Findings
- Open Kaggle competitions with January 2027 deadlines:
  - Google Quantum AI circuit-compression challenge using AI agents, $150K, Oct 22, 2026 – Jan 20, 2027. — [Quantum Computing Report](https://quantumcomputingreport.com/google-quantum-ai-launches-150k-kaggle-competition-to-compress-fault-tolerant-quantum-circuits-using-ai-agents/)
  - NFL Big Data Bowl 2027: final submission Jan 6, 2027, results expected Jan 26, 2027. The prize is listed as $400K on Kaggle versus $100K in a third-party guide. — [Kaggle: NFL Big Data Bowl 2027](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027)
  - "Name That LLM": entry deadline Jan 6, 2027, final submission Jan 13, 2027. The prize is $75K per Kaggle versus $50K in a guide. — [reconscribe guide](https://reconscribe.com/name-that-llm-kaggle-competition-2026/); [Kaggle competitions list](https://www.kaggle.com/competitions)
- Kaggle's slides put the prediction-competition flow at medalists announced, then winners' panels, then Kaggle pays winners, with about 2–3 months for payment. — [Kaggle "Meet Kaggle" slides](https://www.kaggle.com/static/slides/meetkaggle.pdf)
- Winners are contacted before announcement to complete tax forms. Non-US winners typically file a W-8BEN (AIcrowd example). — [AIcrowd forum](https://discourse.aicrowd.com/t/question-about-the-round-1-of-unity-s-obstacle-tower-challenge-email/974/8)
- Kaggle prize money is sometimes restricted by country. — [Undark](https://undark.org/article/kaggle-data-science-dhs/)
- Prize-platform tax practice: HeroX requires banking details plus a tax form and withholds 30% for non-US winners unless a tax treaty lowers it. The US–Israel treaty exists, but its effect on prizes was not verified. — [HeroX tax info](https://herox.com/help/94-guide-awarding-your-prize-tax-information); [HeroX payout FAQ](https://herox.com/help/166-guide-prize-payout-faqs)
- Devpost example (PayPal AI Hackathon 2026):
  - Open internationally, excluding Brazil, Quebec, Russia, Crimea, Cuba, Iran, North Korea and other sanctioned regions; Israel is not excluded.
  - Payment is a lump sum, only after prize affidavits plus identity and eligibility checks. Winners pay wire/FX fees and their own taxes.
  - Prize pool reported as $67,500.
  - [StartupGrantsIndia listing](https://www.startupgrantsindia.com/paypal-ai-hackathon-2026); [Internshala](https://internshala.com/competitions/?p=13021)

### Inferences
- With the 60-day window ending about Jan 16, 2027: Kaggle January closers pay around March–April 2027 at the earliest, and Devpost hackathons that ended in Oct–Nov 2026 would only pay inside the window if already entered. So competitions are realistic only as a slower, longer-term path.
- Kaggle requires a Kaggle account, and phone verification is typically needed to submit (general knowledge, unverified here). Winning also requires signing the winner license and tax forms. Under "no new accounts," this is out unless the owner already has a Kaggle account.
- Kaggle competition rules generally allow AI tools. Devpost rules vary per hackathon, and many require original work created during the submission period.

### Gaps
- Topcoder current payout method and Israel eligibility: not researched (budget). Topcoder has historically used Payoneer/PayPal-type payment providers, but this was not verified.
- Kaggle's actual payout method (wire vs PayPal) for non-US winners: not found.
- Specific Devpost hackathons open now with Dec 2026–Jan 2027 deadlines: not enumerated.

## Writing/content contests and translation/localization bounties via PayPal

### Takeaway
No well-sourced information was found in this session (search budget spent on higher-priority items).

### Cited Findings
- None verified.

### Inferences
- Writing contests run by companies or publications often pay by PayPal, but they almost always need an entry form with name and email (not necessarily an "account"), and many now forbid AI-generated entries. They would need to be checked one by one.

### Gaps
- Current PayPal-paying writing/design contests with deadlines in Nov 2026–Jan 2027, their AI policies and Israel eligibility.
- Translation bounty programs (e.g., Hebrew localization) and how they pay.

## What works with ONLY the existing GitHub account + PayPal vs requires new accounts/KYC

### Takeaway
Almost nothing structured works under "GitHub + PayPal only, no new accounts." Every structured platform that pays money needs its own account plus KYC and/or a tax form: Algora/Opire/huntr through Stripe Connect, HackerOne/Bugcrowd/Intigriti through their own accounts and ID checks, and Kaggle/Devpost through their own accounts, affidavits and tax forms. The only GitHub-only route is informal: maintainers who personally offer PayPal or GitHub Sponsors payments for a fix.

### Cited Findings
- Stripe Connect payout (KYC onboarding) is required by Algora, Opire and huntr. — [Algora docs](https://docs.algora.io/bounties/payments); [Opire docs](https://docs.opire.dev/rewards/lifecycle); [huntr terms](https://huntr.com/participation-terms)
- HackerOne requires a tax form, identity verification and a payment method before any award. — [HackerOne payment preferences](https://docs.hackerone.com/en/articles/8395720-payment-preferences)
- Intigriti requires Onfido ID verification. — [Intigriti](https://kb.intigriti.com/en/articles/3379502-payout-methods)
- Devpost-hosted prizes require affidavits and identity checks. — [StartupGrantsIndia](https://www.startupgrantsindia.com/paypal-ai-hackathon-2026)

### Inferences
- Summary matrix (inferred from the findings above):

| Option | Extra account? | KYC/tax form | PayPal payout? | Israel | Money by ~Jan 16 2027? |
|---|---|---|---|---|---|
| Algora | GitHub login + Stripe Connect | Stripe KYC | No | Unverified | Possible if won quickly, but blocked by constraint |
| Opire | GitHub login + Stripe | Stripe KYC | No | Unverified | Same as Algora |
| huntr | huntr account + Stripe Connect | Yes | No | Unverified (else donated to charity) | Unlikely |
| HackerOne | Yes | ID + W-8BEN | Yes | No exclusion found | Unlikely (skill/triage) |
| Bugcrowd | Yes | Tax form | Yes | No exclusion found | Unlikely |
| Intigriti | Yes | Onfido ID | Yes | No exclusion found | Unlikely |
| Kaggle | Yes | Tax form, winner verification | Unverified | Sometimes country-restricted | No (2–3 months after close) |
| Devpost hackathons | Yes | Affidavit + ID | Varies | Usually eligible | Only if already entered |
| Maintainer-direct PayPal bounty | No (GitHub only) | None/informal | Yes | Yes | Possible, but rare |

- AI agents acting as the owner on GitHub must follow each repo's AI-contribution policy and disclose AI use. Undisclosed AI PRs can get the account banned (RPCS3) or auto-closed (tldraw, Godot). — sources as above
- Tax: Israeli residents are taxed on worldwide income, so prize or bounty income is generally reportable even without a business registration. This is general knowledge, not verified here; the owner's "no tax registration" stance may be incompatible with any regular income stream.

### Gaps
- No primary source on whether PayPal accepts unsolicited business payments to Israeli personal accounts without triggering a business-account upgrade.
- Grants (e.g., open-source grants) were not researched in depth. Gitcoin grants rounds are mostly crypto-wallet based, which means a new wallet account.
