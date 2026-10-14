# Backlog — Price Radar

Prioritised open topics. Stable IDs (`B-n`), never reused. "Where are we?" is answered
here; the chronological *why* lives in `docs/00-development-log.md`.

Source tags: `[user]` asked for by the user · `[agent]` noticed while working · `[plan]`
from `PROJECT_PLAN.md`.

## Open

| ID | Prio | Topic | Source | Notes |
|----|------|-------|--------|-------|
| B-3 | med | Alerts when a marketplace drops below the own price by > X % | [plan] | Phase 5 of the plan. Cheapest route: a step in the daily workflow that compares the newest snapshot against `own_price` and opens a GitHub issue / sends mail. |
| B-10 | high | Marketplace prices for the new Schiesser list | [user] | Direct Amazon, Otto, Zalando, and idealo fetches are bot-walled (2026-10-14). Five Amazon `/dp/` URLs and one new Otto URL are in `matches.csv` but the parser has not extracted a price from them. The 2026-10-14 daily run failed the existing Otto and Galeria fetches with Firecrawl HTTP 402. |
| B-11 | med | Confirm Amazon ASINs `B0DPRB9FST` (183216) and `B0G34NXB6F` (183243) | [agent] | Slugs contain the article number. Colour `-931` and the pack size of B0G34NXB6F were not on the snippet. A 9-pack ASIN for 183243 was deliberately not used. |
| B-12 | med | Otto and Galeria URLs for the articles that have none | [agent] | Candidates skipped because the manufacturer number was missing or the title contradicted the slug. Listed in the README marketplace table. |
| B-4 | med | Own-shop price feed instead of `products.csv` | [plan] | Partially done 2026-10-14: each run reads `og:price:amount` from `shop_url`. The CSV price remains the fallback. Size surcharges above the default variant are not tracked separately. |
| B-5 | low | Custom date range in the dashboard filter (from–to) | [agent] | Presets 1 W … 12 M are in the toolbar. A free range needs two date inputs. |
| B-6 | low | README screenshots via an opt-in Playwright spec | [agent] | Global README rule expects a "Sample Output" table with real screenshots regenerated deliberately (`docs/screenshots/`). |
| B-9 | low | Otto fetch returned `HTTP Error 500` from Firecrawl on 2026-09-03 (manual run) | [agent] | Transient fetch error, not an extraction failure (no `failed-pages` dump). The 2026-10-14 failure is HTTP 402 (credits), tracked as B-10. |

## Decisions so far

- **Marketplaces:** Otto and Galeria stay live for `SCH-173983-803`. Amazon URLs are stored for five new articles but not yet extracted. Zalando has no confirmed row for the current list. *(2026-10-14)*
- **Storage/deploy:** SQLite committed to the repo by the daily GitHub Actions run; dashboard served via GitHub Pages. *(2026-09-01)*
- **Catalog:** adidas Stan Smith demos are inactive. `SCH-173983-803` stays beside the ten new articles; it is not the same article as `183243-908`. *(2026-10-14)*
- **Dashboard:** light card grid, Mein Shop as the reference, marketplace gap in percent, detail chart, German formats. No dark mode, no search field, no day-counter strip, no snapshot table. *(2026-10-14, log entry 2)*

## Done

| ID | Topic | Closed |
|----|-------|--------|
| B-1 | adidas Stan Smith demos removed from the active catalog. Snapshots stay in `pricing.db`. | 2026-10-14 (log entry 2) |
| B-2 | Galeria added as second marketplace for `SCH-173983-803` (first live extraction 37,95 € on 2026-09-03) | 2026-09-03 (log entry 1) |
| B-7 | Cheapest marketplace is the card note and the red gap pill. | 2026-10-14 (log entry 2) |
| B-8 | Dropped with the per-product chart strip. The detail chart draws the points it has. | 2026-10-14 (log entry 2) |
| — | Dashboard redesign: price labels on data points, all marketplaces on one chart, own price prominent, German dates, 1 W–12 M filter, day counter, mobile layout, dark mode | 2026-09-03 (log entry 1) |
