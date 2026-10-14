# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Existing codebase: Python stdlib, SQLite, a self-contained `dashboard.html` (inline CSS and vanilla JS), Firecrawl for marketplace fetches, GitHub Actions publishing GitHub Pages. No interview tool was available in this session; the stack is taken from the repository and the request, and is marked inferred.

## Users

Inferred from the request and README: the shop owner (Schiesser, shop.schiesser.com) checking, in one sitting, where German marketplaces undercut the own shop so they can adjust prices.

## Product Purpose

Price Radar compares marketplace prices with the owner's own shop price and keeps a daily history, so undercutting is visible without reading a chart per product. Success is a scan of 10–20 products that shows who is cheaper, by how much, and for how long.

## Positioning

The reference is always the own shop price, not the cheapest listing. A marketplace price only matters as a gap against that shop.

## Operating Context

Inferred: a daily GitHub Action scrapes stored URLs, appends SQLite snapshots, regenerates one HTML file, and publishes it. The owner opens the dashboard, filters, opens a product, and exports the current view.

## Capabilities and Constraints

- Catalog source of truth: `products.csv` and `matches.csv`. Snapshots are append-only. Existing history must stay.
- German UI, German dates and numbers. Light theme only.
- One self-contained HTML file. No dark mode, no heat strip, no snapshot table.
- Own shop price and product image come from the shop product page when the page can be read (`og:price:amount`, `og:image`).
- Marketplace pages are fetched by the existing Firecrawl pipeline. Direct fetches of Amazon, Otto, Zalando, and idealo are often blocked; a blocked page is an error snapshot, not a guessed price.
- Export of the current view: semicolon CSV with German decimals, an Excel HTML file, and a print view. The daily history files stay.

## Brand Commitments

The name is Price Radar. The approved mockup (light cards, violet accent, Mein Shop as the reference block, red when a marketplace is cheaper) is the visual contract for this dashboard.

## Evidence on Hand

- `pricing.db`: snapshots since 2026-09-01 for the previous adidas demo rows and one Schiesser article. Those rows stay in the database.
- `uploads/price-radar-produkte.csv`: ten Schiesser articles with shop URL, image URL, and idealo offer pages.
- Approved mockup HTML and the two light-theme screenshots.

## Product Principles

- The own shop is the reference every number is measured against.
- A missing or blocked price is shown as missing, never filled in.
- History is appended. Replacing the catalog does not delete past snapshots.
- The daily Action keeps the same entry points: scrape, dashboard, export.

## Accessibility & Inclusion

Inferred: the dashboard is a working tool, so text contrast, keyboard use of filters and the detail panel, and a print view are required. No separate accessibility standard was stated.
