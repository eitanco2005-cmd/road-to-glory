# No-Account Distribution Channels (only an existing GitHub repo + a free Netlify site)

Research notes, Nov 2026. Constraint: the owner creates no new accounts and posts nowhere. AI agents may only commit to the owner's existing GitHub repo, or open PRs from that account to other repos. Network note: docs.github.com, dev.to and en.wikipedia.org were blocked in this session, so some GitHub and Wikipedia rules come from search-result summaries or mirrors rather than the live pages. Those items are flagged.

## Q1. GitHub as a channel: search, topics, Explore, Trending; README links; SEO value; traffic data

### Takeaway
GitHub is a real discovery surface, but on its own it mostly sends traffic that is already looking for code. Topics (up to 20 per repo) put a repo on topic listing pages. Trending depends on a burst of stars, which in practice comes from off-GitHub promotion that this project cannot do. Links in a README are reported to be nofollow, so they help mainly with crawl discovery and human clicks, not ranking authority. Expect a trickle of visitors, not a flood.

### Cited Findings
- Repo admins can add any topics. GitHub suggests topics based on repo content. Clicking a topic opens a page listing every repo with that tag, and popular topics are browsable at github.com/topics. Featured topics can be proposed through the github/explore repo. — [GitHub Docs: Classifying your repository with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) (read via search summary; the page itself was blocked here)
- Topic limits: lowercase letters, numbers and hyphens, at most 50 characters each, at most 20 per repo. These limits come from the GitHub Enterprise Server versions of the same docs. — [GHES 3.19 docs](https://docs.github.com/en/enterprise-server@3.19/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
- GitHub's topic-suggestion system pulls candidate topics from README text and filters them with a classifier. This shows README wording affects which topic suggestions you get. — [GitHub Engineering blog: Topic Suggestions for Millions of Repositories](https://github.blog/engineering/user-experience/topics/)
- I found no official GitHub documentation on how repository search ranks results.
- Trending: GitHub does not publish the algorithm. Most observers say it ranks by recent star growth within a time window (daily, weekly, monthly) rather than total stars. One 2026 blog guesses it compares the last 24 hours of stars against the prior 7 days. It also says coordinated star-buying is flagged and blocked. Both claims are unconfirmed. — [DEV: How to get on GitHub Trending](https://dev.to/iris1031/how-to-get-on-github-trending-the-algorithm-the-tactics-and-the-real-data-o5b); [Gingiris: How AFFiNE hit GitHub Trending 28 times (2026)](https://gingiris.github.io/growth-tools/blog/2026/05/01/affine-github-trending-playbook/); [OSS Insight on Trending](https://ossinsight.io/blog/introducing-trending-page). Figures like "80–150 stars/day needed" come from vendor and SEO blogs and are not verified.
- Repo traffic case studies show stars and visits spike when an external source links to the repo: Skyvern traced a jump of about 1,200 stars through the Referring sites panel, and a small npm project went from 1 to 6 stars after a mention on Echo JS. Froala found that its own website was the top referrer to its GitHub repo, which means traffic often runs from the site to GitHub rather than the other way. — [Skyvern blog](https://www.skyvern.com/blog/analytics-and-attribution-for-an-open-source-project-a-k-a-story-of-how-we-tracked-an-unexpected-burst-of-traffic/); [DEV: ckmtools, 6 stars without a launch](https://dev.to/ckmtools/how-i-got-6-github-stars-without-a-launch-event-4df0); [Froala](https://froala.com/?p=3105)
- GitHub's Traffic tab (Insights → Traffic) shows the top 10 referring sites and content over the last 14 days only, so the data has to be exported regularly to keep a history. — [GitHub Docs: Viewing traffic to a repository](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository); [Grafana Labs on monitoring repo traffic](https://grafana.com/blog/2021/09/20/how-we-use-grafana-and-prometheus-to-monitor-the-traffic-of-our-many-github-repositories)
- Link value: several practitioners report that external links in rendered READMEs and Gists carry rel="nofollow". A 2026 audit confirmed nofollow on Gists, but warns that READMEs, issues, releases, Discussions and profiles each need checking separately. — [DEV: Medium and GitHub both went nofollow](https://dev.to/chetansanghani/medium-and-github-both-went-nofollow-so-i-built-a-40-line-powershell-backlink-verifier-o41); [konabayev.com Backlink Audit 2026](https://konabayev.com/blog/backlink-link-attribute-audit-2026/)
- Google treats nofollow, ugc and sponsored as hints, not strict directives, so a nofollow link can still help Google discover a URL. — [Google Search Central: Qualify outbound links](https://goo.gle/outbound-links); [Search Engine Land guide to rel attributes](https://searchengineland.com/rel-nofollow-ugc-sponsored-links-seo-413534)

### Inferences
- What agents can do for free in the repo: a strong README with a clear H1 and a first paragraph that says what the tool does, a link to the Netlify site at the top, a live-demo badge, a repo description and website field set, up to 20 relevant topics, GitHub Releases, and a social preview image. All of this is allowed and costs nothing. The upside is a modest number of high-intent visitors, plus a fast crawl path to the Netlify site.
- Trending is not realistic without outside promotion, because it needs a star burst and this project cannot drive one. Any star-buying or star-exchange scheme risks being flagged and violates GitHub's rules on inauthentic activity.
- Consider a GitHub Pages site (username.github.io/repo) as a second, crawlable surface that needs no new account. It still has to be weighed against duplicating the Netlify content. Use canonical tags pointing to Netlify.

### Gaps
- I found no quantitative 2024–2026 data on how much traffic a typical small repo sends to an external product site. The case studies are anecdotes.
- I could not open the live GitHub Acceptable Use Policies page (blocked) to quote its text on spam and inauthentic activity. It should be checked directly.
- I did not verify whether GitHub Pages (github.io) pages carry nofollow on outbound links. Since the owner writes the HTML there, they should be followable, but this is unverified.
- I did not research GitHub Discussions as a discovery surface. No data found.

## Q2. Awesome lists and curated repos: PRs from the owner's account, etiquette, spam risk

### Takeaway
Opening a PR to add your own tool to a curated list is the standard way such lists grow. It is allowed by convention, but it is a form of outreach: a human maintainer must read it. Lists increasingly reject AI-generated PRs, and a high-volume campaign from one account would look like spam. Use it sparingly: a few well-chosen lists, one high-quality hand-checked PR each, following each list's contributing.md.

### Cited Findings
- The main sindresorhus/awesome list (for adding whole lists, not tools) requires: the list repo is at least 30 days old; the submitter has reviewed at least 4 other open PRs with substantive comments ("looks good" does not count); the PR is not fully AI-generated; and the list is not AI-generated and reflects considerable effort, or the PR "will be immediately closed." Other requirements include passing awesome-lint, the topics `awesome` and `awesome-list`, a CC0-style license and a contributing.md. — [sindresorhus/awesome pull_request_template.md](https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md)
- In 2026 many projects began restricting AI-written PRs. Ghostty limits AI-assisted contributions to pre-approved issues, tldraw auto-closes all external PRs, and Godot was swamped by more than 4,600 open PRs. In February 2026 GitHub shipped repo settings that limit PRs to collaborators or turn PRs off. These details come from secondary summaries. — [Dev Genius: Open-source projects are now banning AI-generated PRs](https://blog.devgenius.io/open-source-projects-are-now-banning-ai-generated-pull-requests-8e1dd3e8d41c); [The New Stack: AI-generated code crisis](https://thenewstack.io/ai-generated-code-crisis/); [SoftwareSeni: What GitHub is building to protect maintainers](https://www.softwareseni.com/what-github-and-the-oss-ecosystem-are-building-to-protect-maintainers-from-ai-slop); [Stack Junkie on Godot](https://www.stack-junkie.com/blog/ai-code-slop-is-drowning-open-source-the-godot-crisis-explained)
- A RedMonk survey of 77 open-source organizations found some ban AI contributions outright (for example the Linux kernel and curl), while others allow them with disclosure. — [Dev Genius summary](https://blog.devgenius.io/open-source-projects-are-now-banning-ai-generated-pull-requests-8e1dd3e8d41c)

### Inferences
- A PR to a third-party awesome list is permitted, but it counts as outreach: an unsolicited request to a stranger. Whether that breaks the owner's "no outreach" rule is the owner's call. It needs no new account.
- Risk: PRs written by an agent and opened in bulk from the owner's personal account could get the account flagged or blocked by maintainers, and could harm the reputation of the one asset the project has. If this is used at all: at most a few PRs, each to a list that clearly fits, following that list's contributing.md exactly, disclosing AI assistance where the list asks, with a human (the owner) approving each PR.
- Lower-risk alternative: the project can maintain its own curated list in its repo (for example "awesome-israeli-calculators"), which involves no outreach. It only gets traffic if others find or link to it.
- I found no data on acceptance rates or on traffic from a tool-level awesome-list entry. Traffic value is unknown, probably small but long-lasting.

### Gaps
- No acceptance-rate statistics for awesome-list PRs.
- No measured referral traffic from a single entry in an awesome list.
- I did not find an explicit GitHub policy that one PR per list is "spam." GitHub's Acceptable Use Policies (not retrievable here) reportedly ban bulk, unsolicited or inauthentic activity, which must be checked directly.

## Q3. Package registries (npm, PyPI, GitHub Packages, GitHub Marketplace)

### Takeaway
npm and PyPI each need their own account. Even "trusted publishing" from GitHub Actions starts from a PyPI or npm account, so both are ruled out. GitHub-native options (GitHub Packages, GitHub Marketplace for Actions, Releases) need no new account. Marketplace requires 2FA on the existing account and accepting the Marketplace Developer Agreement.

### Cited Findings
- PyPI trusted publishing (OIDC from GitHub Actions) is set up from the publishing page of a PyPI account, including "pending publishers" for new projects. A PyPI account is a prerequisite. — [PyPI Docs: Trusted Publishers](https://docs.pypi.org/trusted-publishers/); [PyPI Docs: Creating a project through OIDC](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/); [pydevtools handbook](https://pydevtools.com/handbook/how-to/how-to-publish-to-pypi-with-trusted-publishing/)
- npm supports requiring 2FA for publishing, which presupposes an npm account. — [npm Docs: Requiring 2FA for package publishing](https://docs.npmjs.com/requiring-2fa-for-package-publishing-and-settings-modification)
- GitHub Marketplace (Actions): to publish, the action must be in a public repo, the publisher must use 2FA, and the repo owner must accept the GitHub Marketplace Developer Agreement. Actions are listed immediately without GitHub review if they meet the requirements. — [GitHub Docs: Publishing actions in GitHub Marketplace](https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace); [GitHub Docs: mandatory 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-mandatory-two-factor-authentication)

### Inferences
- npm and PyPI are ruled out (new accounts). Workaround: users can still install straight from GitHub (`npm install github:owner/repo`, `pip install git+https://github.com/owner/repo`). This is standard tooling behavior, but it gives no registry discoverability.
- GitHub Marketplace is the one registry-like listing with search that is available without a new account. It only applies if the project ships a GitHub Action, so it suits developer kits only. Accepting the Developer Agreement is a ToS step on the existing account, not a new account. Owner sign-off is still needed.
- GitHub Packages (container or npm-scoped packages under the owner's namespace) uses the existing account, but these packages have little public discovery. Not a real discovery channel.

### Gaps
- I did not verify whether jsDelivr/unpkg CDN mirroring of GitHub repos (jsdelivr.com/gh/...) offers any discovery, but it needs no account.

## Q4. AI assistants and LLM citation (GEO): llms.txt, structured data, indexing

### Takeaway
To get cited by AI assistants, a page must first be indexed by the search engines they draw on (Bing and Google) and must answer the query directly, with headings that match it. llms.txt shows no measurable effect so far. IndexNow lets the Netlify site push URLs to Bing and other participating engines without any account, so it is the most useful no-account step.

### Cited Findings
- llms.txt: an Ahrefs-cited study found 97% of llms.txt files get zero AI requests. One analysis found 84 llms.txt requests in more than 62,100 AI bot visits. A Search Atlas study of 13,911 domains found adoption "does not predict LLM citation behavior." Google's Gary Illyes said in July 2025 that Google does not support llms.txt. — [PPC Land: llms.txt adoption rises 8.8x but 97% get zero AI requests](https://ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/); [SEO Sherpa on Ahrefs study](https://seosherpa.com/97-of-llms-txt-files-are-never-read/); [Search Atlas study](https://searchatlas.com/blog/limits-of-llms-txt-for-ai-search-citation-study/); [Search Engine Land: Does llms.txt matter](https://searchengineland.com/does-llms-txt-matter-467740); [Optimizely: Does llms.txt work?](https://www.optimizely.com/field-notes/articles/does-llms-txt-work/)
- Search-index link: Seer Interactive found 87% of SearchGPT citations matched Bing's top results. NP Digital (July 2025, 800 responses) found about 55% of ChatGPT citations came from Google-powered sources and about 45% from Bing. Ahrefs found only 12% of AI-cited URLs rank in Google's top 10 for the original prompt; Perplexity is the most SEO-aligned assistant. Grow & Convert found only 27% of cited sources ranked on Google for ChatGPT's fan-out queries. — [Seer Interactive](https://www.seerinteractive.com/insights/87-percent-of-searchgpt-citations-match-bings-top-results); [Neil Patel / NP Digital](https://neilpatel.com/marketing-stats/google-vs-bing-chatgpt-search-sources/); [Ahrefs: AI search overlap](https://ahrefs.com/blog/ai-search-overlap/); [Grow & Convert fan-out study](https://www.growandconvert.com/ai/fan-out-query-serp-study/)
- AirOps found pages whose headings closely match the user's query were cited 41% of the time, versus 29% for weak matches. — [AirOps: The Fan-Out Effect](https://airops.com/report/the-fan-out-effect-what-happens-between-a-query-and-a-citation)
- IndexNow needs no Bing Webmaster account: generate your own key (8–128 characters), host `<key>.txt` at the site root, and POST URLs to api.indexnow.org. Participating engines include Bing, Yandex, Naver and Seznam. Google is not one of them. — [IndexNow FAQ](https://indexnow.org/faq); [IndexNow documentation](https://www.indexnow.org/documentation); [Trevor Lasn: How to set up IndexNow](https://trevorlasn.com/blog/how-to-setup-indexnow-for-instant-search-engine-indexing)

### Inferences
- No-account GEO checklist for the Netlify site: a sitemap.xml with a `Sitemap:` line in robots.txt; IndexNow key file plus a build-time or GitHub Actions POST on each deploy (submits to Bing, which feeds ChatGPT search and Copilot); schema.org JSON-LD (SoftwareApplication or WebApplication, FAQPage, HowTo) in the page; one page per specific query (for example "מחשבון X 2026") with headings that match the query; visible, quotable answers. llms.txt is cheap to add but should not be counted on.
- Google Search Console needs a Google account. If the owner already has one, it is not a new account, but the owner would still have to do a manual verification step. Without it, Google relies on crawling the sitemap and on links (for example from the GitHub repo).

### Gaps
- No controlled evidence that schema.org markup on its own increases AI citations. The structured-data recommendation rests on general SEO practice, not on studies found here.
- I did not confirm the current status of Google's sitemap "ping" endpoint (my understanding is that it was deprecated in 2023, but I did not verify this here).

## Q5. Platforms that need accounts (rule out)

### Takeaway
Nearly every launch platform or directory needs an account to submit, and some charge fees. Under the constraints, all of these are ruled out.

### Cited Findings
- Chrome Web Store: developer registration plus a one-time $5 fee. — [Chrome for Developers: Register your developer account](https://developer.chrome.com/docs/webstore/register)
- Firefox Add-ons (AMO): needs an AMO developer account (free). This comes from a secondary source. — [extension.js publishing docs](https://extension.js.org/docs/publishing)
- There's An AI For That: a TAAFT account is needed; a listing costs about $49 one-time (sources conflict on whether a free monthly slot exists). — [SaaSCity: TAAFT directory review (Oct 2026)](https://saascity.io/directories/theresanaiforthat); [G2 TAAFT pricing](https://www.g2.com/products/there-s-an-ai-for-that/pricing); conflicting claim of free submissions: [IdeaProof](https://ideaproof.io/launch-directories/there-s-an-ai-for-that)
- Hacker News: posting needs an HN account. HN guidelines discourage creating accounts routinely. New accounts get less lenient ranking, and in March 2026 there was a 600+ upvote thread asking to restrict new accounts from Show HN. Show HN must be something people can try, not a landing page. — [HN Guidelines](https://news.ycombinator.com/newsguidelines.html); [HN FAQ](https://news.ycombinator.com/newsfaq.html); [keydiscussions.com, Mar 2026](https://keydiscussions.com/2026/03/09/hacker-news-moves-toward-restricting-show-hn-posts-amid-the-ai-slop-wave/)
- Product Hunt: launching needs a maker account. Asking for upvotes is against the rules. — [Product Hunt launch guide](https://www.producthunt.com/launch/preparing-for-launch)

| Channel | Account needed? | Verdict |
|---|---|---|
| Chrome Web Store | Yes, plus $5 fee | Ruled out |
| Firefox AMO, Edge Add-ons | Yes | Ruled out |
| Apple App Store / Google Play | Yes, plus paid developer program | Ruled out |
| Product Hunt | Yes | Ruled out |
| Hacker News | Yes, and new accounts are disadvantaged | Ruled out |
| Reddit, Indie Hackers, X, LinkedIn, Facebook groups | Yes | Ruled out |
| TAAFT, Futurepedia, SaaS directories, Hebrew directories | Generally yes (form or account); TAAFT about $49 | Ruled out (a few accept anonymous web-form submissions, but submitting is outreach) |
| npm, PyPI | Yes | Ruled out |
| Bing Webmaster Tools | Yes, but IndexNow does not need one | Use IndexNow |
| GitHub Marketplace, Packages, Pages, Releases, Gists | Existing GitHub account | Allowed |

### Inferences
- The Reddit, Indie Hackers, mobile app store and Hebrew directory rows reflect well-known platform requirements. I did not open an official page for each in this session.

### Gaps
- I did not research Hebrew-specific directories (for example Israeli tool or calculator directories) individually.

## Q6. WhatsApp and organic sharing in Israel

### Takeaway
WhatsApp reaches about 99% of Israelis, so the main no-account channel is users sharing the tool themselves. The project's job is to make sharing a result one tap away. I found no published study showing that calculators specifically spread this way in Israel.

### Cited Findings
- Surveys reported by JPost (2025) and CTech (2026) put WhatsApp use at 99% of Israel's population, ahead of YouTube (98%) and Facebook (90%). Among Arab Israelis, use is 98%, with 99% of users using it daily. The survey methods are not fully described. — [Jerusalem Post](https://www.jpost.com/business-and-innovation/article-871715); [CTech / Calcalist](https://www.calcalistech.com/ctechnews/article/rkqhuhexfl)
- DataReportal counted 6.82 million social media user identities in Israel in January 2025, 72.2% of the population. — [DataReportal Digital 2025: Israel](https://datareportal.com/reports/digital-2025-israel)
- Op-ed arguing that "WhatsApp-first" is now table stakes for Israeli small businesses. — [Times of Israel blog](https://blogs.timesofisrael.com/why-whatsapp-first-is-now-table-stakes-for-israeli-small-businesses/)

### Inferences
- Share design (all static, no account needed): a `https://wa.me/?text=<urlencoded Hebrew summary of the result + URL>` button right next to the result; the Web Share API (`navigator.share`) on mobile; result URLs that encode the inputs as query parameters, so the recipient opens the same calculation; Open Graph tags (og:title, og:description, og:image, with a 1200×630 Hebrew image) so WhatsApp shows a rich preview; short, right-to-left-correct share text that states the result ("I'm entitled to ₪X in severance"); a "send to your accountant or partner" prompt. All of this can be built on the Netlify site.
- Topics with natural reasons to share in Israel (salary, severance, tax refunds, maternity leave, arnona, reserve-duty pay) are good fits. This is inferred; I found no source data.

### Gaps
- No quantitative evidence on how often Israeli users share calculators or tools over WhatsApp, or what conversion rates share buttons achieve.

## Q7. Other legitimate no-account channels and rules

### Takeaway
Wikipedia explicitly forbids linking to a site you own or maintain, so it is ruled out. Other no-account levers are technical: schema.org, sitemap/robots, IndexNow, Open Graph, GitHub Pages, Releases and Gists, and the project's own curated list.

### Cited Findings
- Wikipedia's External links guideline restricts editors from linking to "a website that you own or maintain," without exception. The COI guideline tells conflicted editors to avoid linking to their organization's website. Editing Wikipedia also effectively needs an account (anonymous edits expose your IP and are still covered by these rules). — [Wikipedia: Conflict of interest](https://enwp.org/WP:COI); EL guideline text via mirror: [User:Anon126 guide on linking](https://wiki.riteme.site/wiki/User:Anon126/Guide_for_contributors_with_close_connections/Linking). The live en.wikipedia.org page was blocked in this session.
- SEO sources say all Wikipedia external links are nofollow (secondary claim). — [Search Engine Land rel guide](https://searchengineland.com/rel-nofollow-ugc-sponsored-links-seo-413534)

### Inferences
- Open data portals (for example data.gov.il) are data sources the project can use and credit, not places to publish its own tools. Publishing to them would need an account or government affiliation (not verified).
- Gists are on the existing account and get indexed, but their links are nofollow. They are useful as small, findable code snippets that link back to the site.

### Gaps
- I did not verify whether data.gov.il accepts community-submitted apps or showcases.
- No evidence collected on GitHub Discussions or GitHub Pages traffic specifically.
