"""Single source of truth for the site's public base URL and brand.

Every generator (tools/site/*, products/**) imports from here. To move the site to another host run
    python3 tools/site/set_base_url.py https://new-host.example/
which rewrites BASE_URL here, SITE_URL in docs/assets/config.js, every absolute URL already baked into
docs/ (canonicals, og:url, JSON-LD), then rebuilds sitemap.xml + robots.txt.
The site is served from the domain ROOT (Netlify, publish dir docs/).
"""
BASE_URL = "https://tichnun.netlify.app/"
BRAND = "תכנון פלוס"            # Hebrew brand: titles, og:site_name, JSON-LD, files
BRAND_LATIN = "Tichnun Plus"    # Latin contexts (PayPal brand_name, file metadata, ASCII file names)
TAGLINE = "כלים חכמים לתכנון"
