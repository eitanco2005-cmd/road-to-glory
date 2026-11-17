# RTL Landing Kit Pro v1.0

Thanks for buying! Open `index.html` in a browser to browse everything. No install, no build step, no framework.

## What's inside

```
index.html               overview of the pack
templates/               12 complete pages
  restaurant.html        restaurant / café: menu with prices, hours, table booking form
  real-estate.html       real estate: search form, listing cards, pagination, buy/sell/rent form
  clinic.html            clinic: services, team, 3-step booking form (date, time, ID number)
  law-firm.html          law firm / consultants: practice areas, tabs, timeline, consultation form
  course.html            online course: video modal, syllabus accordion, instructor, single price
  conference.html        conference / event: agenda table, speakers, ticket tiers, venue
  product.html           single product store: gallery, size choice, quantity stepper, spec tabs
  nonprofit.html         nonprofit: impact stats, donation form (monthly/one-off), volunteer form
  waitlist.html          coming soon / waitlist: one centred screen with email capture
  portfolio.html         photographer / designer: masonry gallery, packages, contact
  fitness.html           gym / studio (dark navbar): weekly schedule table, monthly/yearly pricing toggle
  dashboard.html         SaaS app shell: sidebar (drawer on mobile), KPI cards, SVG chart, orders table
components/index.html    copy-paste components:
                         navbars (simple, mega dropdown, centred logo + announcement bar, dark + side drawer)
                         forms (contact with +972 prefix, login with error state, multi-step signup, Israeli checkout/address)
                         pricing (3 tiers, monthly/yearly toggle, comparison table)
                         dashboards (KPI cards, SVG chart, data table + pagination)
                         more (tabs, timeline, quote, breadcrumbs, <dialog> modal, toast)
css/rtl-kit.css          base styles (same as the free kit)
css/pro.css              Pro components
js/pro.js                ~4 KB of optional interactions (dropdowns, drawer, tabs, steps, toggle, modal, toast)
free/                    the 3 free MIT templates (plain CSS + Tailwind) with the language switcher
```

## How it works

* **Logical properties only.** `margin-inline-start`, `padding-inline`, `inset-inline-end`, `border-start-start-radius`…
  There is not a single `left`/`right` in the CSS. Change `<html dir="rtl">` to `dir="ltr"` and the whole page mirrors.
  Every Pro page has an **LTR ⇄** button (bottom corner) to preview this — delete it before going live.
* **Direction-aware icons** get `class="flip"` (arrows, chevrons) and mirror in RTL. Icons that must not flip
  (play, phone, cart) simply don't have the class.
* **Numbers, prices, phones, emails** sit in `<bdi>` or in `dir="ltr"` inputs aligned to the end, so `₪1,250`,
  `050-000-0000` and `you@example.com` never scramble inside Hebrew or Arabic text.
* **Fonts per language** via `:lang()`: Heebo for Hebrew, Noto Kufi Arabic for Arabic (with taller line height),
  Inter for Latin. Change the `--font-*` variables in `css/rtl-kit.css`.
* **Theme** = CSS custom properties. Each template sets `--c-primary`, `--c-primary-soft`, `--c-accent` in a
  `<style>` block in its `<head>`; dark mode follows the visitor's system setting (`prefers-color-scheme`).

## Arabic

All templates ship with Hebrew placeholder copy. To make a page Arabic: set `<html lang="ar" dir="rtl">` and replace
the text. Fonts and line height switch automatically. For a page with a language switcher (he/ar/en from one file),
see the free templates in `free/` and `free/js/rtl-kit.js`.

## Forms

Forms with `data-demo` only show their success message. Point them at your backend (or Formspree, Netlify Forms,
Basin…) and remove `data-demo`. Field `autocomplete` attributes are set for Israeli addresses and phones.

## Browser support

Current Chrome, Edge, Firefox and Safari (logical properties, `:dir()`, `color-mix()`, `<dialog>`).

## License

See `LICENSE-PRO.txt`: unlimited personal and client projects; no reselling or redistributing the templates themselves.
Free templates in `free/` are MIT.

## Help

Something unclear, or a refund within 14 days: reply to your PayPal receipt. Updates to v1.x are free — keep your
download link.
