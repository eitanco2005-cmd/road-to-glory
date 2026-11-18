/* תכנון פלוס (Tichnun Plus) site configuration. Public values only: never put a secret here.
 * PAYPAL_CLIENT_ID is copied from config/paypal.json (Live, receive-only).
 * SALES_ENDPOINT / VISITS_ENDPOINT: URLs of tools/site/sales_endpoint (empty = no-op).
 * SELLER_NAME / SELLER_EMAIL: filled in by the manager.
 * SITE_URL: canonical public base URL; must equal BASE_URL in tools/site/site_config.py
 *   (change both with: python3 tools/site/set_base_url.py <url>). */
window.SITE_CONFIG = {
  PAYPAL_CLIENT_ID: "BAA7ZWdWb42j_Gm270pywGmY5BNeKEGZAqRpJ25YepvKg5437Dwn8ye_yDsAlrJkqu9JbAHIQeWIbwrT8I",
  PAYPAL_ENV: "live",
  CURRENCY: "ILS",
  SALES_ENDPOINT: "/api/hit",
  VISITS_ENDPOINT: "/api/hit",
  SELLER_NAME: "איתן כהן",
  SELLER_EMAIL: "eitanco2005@gmail.com",
  SITE_URL: "https://tichnun.netlify.app/",
  BRAND: "תכנון פלוס",
  BRAND_LATIN: "Tichnun Plus",
  /* Apple Pay / Google Pay via PayPal: keep false until the PayPal account is eligible and the domain is
     registered (see ops/reports/W1-platform.md). true only loads the SDK component; buttons are not rendered yet. */
  ENABLE_APPLEPAY: false,
  ENABLE_GOOGLEPAY: false
};
