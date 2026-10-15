# Development log — Price Radar

Append-only archive of decisions and bugs with their *why*. The current state of the
project lives in `README.md` (setup, marketplaces, workflow) and `BACKLOG.md` (open
topics, decisions digest); this file is history, not status.

## Recurring lessons

- The Claude in-app browser pane renders unreliably while hidden (blank screenshots,
  scroll timeouts). Use the Playwright MCP for screenshots (`.playwright-mcp/*.png`,
  full-page and viewport) and verify DOM measurements with `browser_evaluate` before
  trusting what a screenshot shows.
- Inline SVG charts: never name the x/y scale functions `x`/`y` when the surrounding
  code iterates with `forEach(function(x){…})` — the shadowing produced a silent
  wrong chart before the first render check.
- Third-party skill installers (`npx … init`) are blocked by the auto-mode
  classifier; cloning the repo and copying the skill folder works and keeps the
  install inspectable.

## Entries

| # | Summary | Detail |
|---|---------|--------|
| 1 | Dashboard redesign (2026-09-03): one chart per product with every marketplace as a series, own price as the reference line, price labels, German dates, 1 W–12 M presets, day counter under/over own price, mobile/dark layout; ui-ux-pro-max skill installed user-level and used for the checklist, not for its style pick. | [00-session1-dashboard-redesign.md](00-session1-dashboard-redesign.md) |
| 2 | Dashboard redesign (2026-10-14): light card grid from the approved mockup, wired to `pricing.db`. Own shop price and `og:image` are read from `shop_url` on every run. Catalog is the ten new Schiesser articles plus `SCH-173983-803` (different barcodes from `183243-908`, so not merged). Adidas demos are `active=0`; their snapshots are not deleted. Search was dropped because the catalog is about eleven products. The "unterboten seit > 7 Tagen" KPI counts consecutive observed days of a cheaper best price, ending on the last day that has a price, so a failed recent fetch does not wipe a long streak. | README marketplace table |
| 3 | New Firecrawl key on a separate free account after HTTP 402; Amazon buy-box parser (`source=amazon`); two Amazon links replaced; 7 of 8 matches priced (2026-10-15). | [00-entry3-amazon-buy-box.md](00-entry3-amazon-buy-box.md) |
| 4 | Dashboard copy and toolbar (2026-10-15): marketplace and status filter chips removed (11 products, user: filters make little sense at this size); "dein Shop" phrasing removed from KPIs, notes, subtitle and footer. Sort, time range and view toggle stay. | — |
| 5 | Galeria links for five articles without a marketplace, matched by the shop's variant EANs (`shop_url` + `.json`); Galeria read by plain fetch with Firecrawl fallback (`DIRECT_MARKETPLACES`); dead Amazon link for `205159-100` removed. Otto candidate C1035568146 rejected (GTIN of another colour) (2026-10-15). | — |
| 6 | Repo moved from `dynamicdolphino/price-radar` to the org repo `Priceradar-SCH/priceradar-sch.github.io`, so the dashboard is served at https://priceradar-sch.github.io/. The Firecrawl secret and the Pages workflow setting moved with it; the old dynamicdolphino.github.io/price-radar address no longer serves the dashboard (2026-10-15). | — |
