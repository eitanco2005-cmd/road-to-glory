/** RTL Landing Kit — Tailwind config (v3.4). Build: npm run build:tw  (from devkit/) */
module.exports = {
  content: ["./templates/**/tailwind.html", "./js/*.js"], // paths are relative to devkit/ (where npm runs),
  darkMode: "media",
  theme: {
    extend: {
      fontFamily: {
        he: ["Heebo", "sans-serif"],
        ar: ["Noto Kufi Arabic", "sans-serif"],
        en: ["Inter", "sans-serif"],
      },
    },
  },
};
