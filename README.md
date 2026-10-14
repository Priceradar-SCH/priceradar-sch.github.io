# Pricing Tool

Tracks the prices of shop.schiesser.com products across marketplaces, stores a
daily price history in SQLite, and renders a self-contained HTML dashboard.
Pure Python stdlib + the Firecrawl scrape API. No AI/LLM anywhere in the running
pipeline — price extraction is deterministic (JSON-LD / meta tags).

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the full roadmap.

## How it works

```
products.csv + matches.csv          (catalog: what to track, where)
        │  src/scrape.py            (own shop HTML, then Firecrawl -> src/parse.py)
        ▼
pricing.db                          (SQLite: products, shop_prices, matches, snapshots)
        │  src/dashboard.py
        ▼
dashboard.html                      (self-contained card grid + history chart)
```

- `products.csv` — one row per own product: `sku, ean, name, own_price_eur, shop_url, image_url`.
  `own_price_eur` and `image_url` are the fallback until the shop page is read.
- `matches.csv` — one row per (product × marketplace): `sku, marketplace, url`.
  One URL per marketplace. The daily run only scrapes stored URLs.
- Rows that leave the CSVs stay in the database with `active=0`. Their snapshots
  are kept; the daily scrape stops requesting them.
- Each run reads the own shop page first (no Firecrawl credit) and stores
  `og:price:amount` and `og:image` in `products` and one `shop_prices` row per
  calendar day. A failed shop fetch leaves the CSV price and image in place.
- Extraction order per page: og/twitter price meta tags → JSON-LD product offers
  (meta wins on conflict because it carries the displayed sale price).

### Marketplaces (re-checked 2026-10-14)

Direct fetches from this environment. "Parser works" means `src/parse.py` extracted
a price from obtainable HTML. A blocked page was not given a guessed price.

| Source | Parser | In this catalog |
|---|---|---|
| shop.schiesser.com | Works on a normal fetch. `og:price:amount` and `og:image`. All 11 shop pages returned the CSV price on 2026-10-14. | Every active product. |
| `otto` | Historical Firecrawl runs extract JSON-LD. A direct product fetch is blocked (HTTP 400). The parser was not re-run on the new Otto URL. | `SCH-173983-803` keeps its existing URL (priced through 2026-10-08; the 2026-10-14 run failed with Firecrawl HTTP 402). `205221-000` adds `C1035381198`, matched by the Otto search title to the idealo offer title. |
| `galeria` | JSON-LD works when the HTML is obtainable (historical extraction 37.95 on the tracked URL). Catalog search returns 403. | `SCH-173983-803` keeps its existing URL. No new Galeria URL for the other articles. |
| `amazon` | Direct `/dp/` fetch returns 503. A reader proxy returns a block page. Parser not verified. | Five `/dp/` URLs whose slugs contain the article number: `205144-100` B012CR2JQ6, `205159-100` B01ATOOYEE, `205172-100` B00HQTQCK0, `183216-931` B0DPRB9FST (slug has 183216, not the colour `-931`), `183243-908` B0G34NXB6F (slug has 183243; pack size not confirmed on the page). |
| `zalando` | Parser works (`twitter:data1` when the label is Preis/Price) when HTML is obtainable. Direct fetch is 403. Searches for the ten article numbers did not return those articles. | No new rows. The adidas demo matches are inactive. |
| idealo | Direct fetch is 403. When HTML is available, JSON-LD is one aggregate price, not one price per shop. | Not stored as match URLs. The upload file's marketplace links are idealo pages. |
| Kaufland, eBay, About You | No usable product HTML (verification wall, 403, or no article hit). | Not added. |

Otto candidates that were **not** added, because the manufacturer number was not on the page: C1375573893 and C2009241194 (possible `183243-908`), C1899923585 and C1899923512 (Original Classics, not confirmed as `205144-100` / `205172-100`), C1899925848 (title says 2er, slug says 4er), S005P0GN (possible `205145-100`), C1950221931 (href says 5er, title says 10er). No confirmed Otto or Amazon URL for `205222-803`, `205145-100`, `183989-214`, `183994-860`.

### Catalog notes

Eleven active products. Ten come from the 2026-10-14 Schiesser list. The eleventh
is the article that was already being scraped.

- `SCH-173983-803` stays, with its Otto and Galeria matches and every snapshot.
  It is a different article from `183243-908`: both are "Enge Boxershorts 3er-Pack
  Dunkelblau - 95/5" at 39.95 EUR, but the shop barcodes differ
  (`4007065791955` is size 5 of 173983-803; `183243-908` starts at `4007067085311`).
  The shop URL is `https://shop.schiesser.com/products/enge-boxershorts-3er-pack-dunkelblau-95-5-173983-803`.
  The Otto slug still says "6er-pack"; the stored URL is unchanged because its
  JSON-LD `gtin13` 4007065792037 is size 7 of this article.
- `183243-908` is the new-list article and is not merged into `SCH-173983-803`.
- The adidas Stan Smith rows (`DEMO-001`, `DEMO-002`, `DEMO-003`) are `active=0`.
  Their Zalando snapshots stay in `pricing.db` and in the history export. They
  are not on the dashboard and the daily run does not fetch them.

## Setup

1. `cp .env.example .env` and add your Firecrawl API key.
2. Edit `products.csv` and `matches.csv`.
3. Manual run:

```bash
python3 src/scrape.py && python3 src/dashboard.py
```

4. Open `dashboard.html`.

## Dashboard & export

Live dashboard (GitHub Pages, republished by every daily run):
**https://dynamicdolphino.github.io/price-radar/**

`src/dashboard.py` writes a single self-contained `dashboard.html` (inline CSS +
vanilla JS, no external assets, light theme only):

- **KPI row** — how many products a marketplace undercuts, the average gap of the
  cheapest marketplace, the largest undercut, and products undercut on more than
  seven consecutive observed days.
- **Card grid** — shop photo, Mein Shop as the reference price, one row per
  marketplace with the percent gap. Red means the marketplace is cheaper. A note
  names the undercut. A price older than today shows its date.
- **Toolbar** — marketplace and status chips, sort, time range, grid or list.
  There is no search field.
- **Detail panel** — price history of Mein Shop against the marketplaces (hover
  and arrow keys), plus the last captured comparison.
- **Export of the current view** — semicolon CSV with German decimals, an Excel
  HTML file, and a print view ("Als PDF speichern").
- German formats throughout (`dd.mm.yyyy`, `1.234,56 €`). UI language is German
  because that is the audience; code and docs stay English.

Local preview: `python3 src/dashboard.py && python3 -m http.server 8765` and open
`http://localhost:8765/dashboard.html`.

Price history export (linked from the dashboard header):
- `history.csv` — standard CSV (comma separator, dot decimals, ISO dates)
- `history_excel.csv` — opens cleanly in German Excel (semicolon separator,
  comma decimals, `dd.mm.yyyy` dates, UTF-8 BOM)

Regenerate locally with `python3 src/export.py`.

Note: Pages sites are always public, so the repo is public and the dashboard
shows only publicly available marketplace prices (owner's decision, 2026-09-01).

## Daily automation (GitHub Actions — primary)

The workflow in `.github/workflows/daily.yml` runs every day at 06:30 UTC on
GitHub's runners — fully independent of any local machine, no server, no LLM.
It scrapes, rebuilds the dashboard, and commits `pricing.db` + `dashboard.html`
back into the repo (the repo is the persistent store; every day is one commit,
so the full history is also in git).

One-time setup after pushing the repo:

```bash
gh secret set FIRECRAWL_API_KEY
```

(paste your key when prompted). Trigger a run manually any time:

```bash
gh workflow run daily-price-scrape
```

Free tier: private repos get 2,000 Actions minutes/month; this run takes ~2-4
minutes/day at MVP scale.

### Alternative: local launchd (optional, not needed with Actions)

`com.pricingtool.daily.plist` runs the same pipeline locally at 08:30 —
`cp` it to `~/Library/LaunchAgents/` and `launchctl load` it. Only useful if the
Actions route is ever unwanted.

## Cost model

1 Firecrawl credit per scraped page. `products × marketplaces × 1 run/day`:
20 products × 5 marketplaces = 100 credits/day ≈ 3,000/month (Firecrawl hobby
plan ~16 USD/month covers exactly that). `MAX_PAGES_PER_RUN` in `.env` is a hard
abort guard against runaway runs.

## Debugging a failed extraction

Every match whose price could not be extracted is written to `debug/` (env
`DEBUG_DUMP_DIR`) as `{sku}_{marketplace}.json` with the fetched metadata and
HTML; the workflow uploads that folder as the `failed-pages` artifact. Download
it with `gh run download <run-id> -n failed-pages` and feed it to the parser
locally instead of spending credits on repeated live fetches.

## Offline ingest (testing)

`python3 src/scrape.py --ingest pages.json` feeds pre-fetched pages
(`[{"url":..., "metadata":..., "html":...}]`) through the same parse/store path
without spending credits.

## Status & open items

Open topics with priorities: [`BACKLOG.md`](BACKLOG.md). Chronological decision log
(the *why*): [`docs/00-development-log.md`](docs/00-development-log.md).

*Working language: chat and UI are German, everything in the repository is English.*
