# Entry 3 — New Firecrawl key, Amazon buy-box parser (2026-10-15)

## Trigger

After the card redesign (entry 2) every marketplace fetch failed with Firecrawl
HTTP 402. The team account had 0 of 1000 credits left; most of October's usage came
from the `Default` key (research in other projects), not from `price-radar`.

## What changed

- The user set `FIRECRAWL_API_KEY` to a key from a second, free Firecrawl account that
  is used only by this repo. A manual run then priced Otto (2) and Galeria (1).
- Amazon pages have no price meta tags and no JSON-LD. `parse.from_amazon` reads the
  hidden `twister-plus-buying-options-price-data` JSON (buy-box price of the variant
  the page shows) and `#availability`. Pages with only a size/colour price range stay
  unpriced instead of picking one end of the range.
- `183216-931`: B0DPRB9FST returned 404, replaced by B0D79WQC9C.
  `205159-100`: B01ATOOYEE was a 4-pack (own article is a 2-pack), replaced by
  B0C61N6L3Z, which returned 404 in the verification run (B-10).
- Verification run: 7 of 8 matches priced (Amazon 4 of 5).
- Local `main` had unpushed September UX-pass edits that the redesign superseded. They
  are kept on the local branch `archive/sep-ux-pass-unpushed`, not pushed.

## Cost

Two manual runs, about 16 Firecrawl credits on the new account. A daily run needs
about 8 credits (one per active match), roughly 240 per month.
