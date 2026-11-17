/* Glory site configuration. Public values only: never put a secret here.
 * PAYPAL_CLIENT_ID is copied from config/paypal.json (Live, receive-only).
 * SALES_ENDPOINT / VISITS_ENDPOINT: URLs of tools/site/sales_endpoint (empty = no-op).
 * SELLER_NAME / SELLER_EMAIL: filled in by the manager. */
window.GLORY_CONFIG = {
  PAYPAL_CLIENT_ID: "BAA7ZWdWb42j_Gm270pywGmY5BNeKEGZAqRpJ25YepvKg5437Dwn8ye_yDsAlrJkqu9JbAHIQeWIbwrT8I",
  PAYPAL_ENV: "live",
  CURRENCY: "ILS",
  SALES_ENDPOINT: "",
  VISITS_ENDPOINT: "",
  SELLER_NAME: "איתן כהן",
  SELLER_EMAIL: "eitanco2005@gmail.com",
  BRAND: "Glory",
  /* Apple Pay / Google Pay via PayPal: keep false until the PayPal account is eligible and the domain is
     registered (see ops/reports/W1-platform.md). true only loads the SDK component; buttons are not rendered yet. */
  ENABLE_APPLEPAY: false,
  ENABLE_GOOGLEPAY: false
};
