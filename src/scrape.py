"""Daily scrape run: fetch every active match via the Firecrawl API, extract the
price deterministically, append one snapshot per match. Stdlib only, no LLM.

Usage:
  python3 src/scrape.py                  # live run (needs FIRECRAWL_API_KEY in .env)
  python3 src/scrape.py --ingest FILE    # offline: FILE is a JSON list of
                                         # {"url":..., "metadata":..., "html":...}
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db
import parse

FIRECRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/scrape"
MAX_PAGES_PER_RUN = int(os.environ.get("MAX_PAGES_PER_RUN", "200"))
REQUEST_PAUSE_S = 2
# Marketplaces whose product pages answer a plain fetch with a JSON-LD price.
# They are read directly first and only fall back to Firecrawl on failure.
DIRECT_MARKETPLACES = {"galeria"}


def load_env():
    env_file = db.ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def firecrawl_fetch(url, api_key):
    payload = json.dumps({
        "url": url,
        "formats": ["rawHtml"],
        "onlyMainContent": False,
        "maxAge": 0,
        "location": {"country": "DE", "languages": ["de-DE"]},
    }).encode()
    req = urllib.request.Request(
        FIRECRAWL_ENDPOINT,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.load(resp)
    data = body.get("data") or {}
    return {"metadata": data.get("metadata") or {}, "html": data.get("rawHtml") or ""}


def dump_failure(match, page):
    """If DEBUG_DUMP_DIR is set, keep the fetched page of a failed extraction so
    the marketplace's markup can be inspected offline (CI uploads it as an artifact)."""
    dump_dir = os.environ.get("DEBUG_DUMP_DIR")
    if not dump_dir:
        return
    Path(dump_dir).mkdir(parents=True, exist_ok=True)
    out = Path(dump_dir) / f"{match['sku']}_{match['marketplace']}.json"
    out.write_text(json.dumps({"url": match["url"], "metadata": page.get("metadata"),
                               "html": page.get("html")}, ensure_ascii=False))


def fetch_html(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/122.0.0.0 Safari/537.36"),
            "Accept-Language": "de-DE,de;q=0.9",
            "Accept": "text/html",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def refresh_shops(conn):
    """Read each active product's own shop page and store price + og:image.

    The shop (Shopify) answers a normal fetch and carries og:price:amount and
    og:image, so this does not spend a Firecrawl credit. A failed fetch leaves
    the CSV price and image in place.
    """
    rows = conn.execute(
        "SELECT sku, shop_url FROM products WHERE active=1 AND shop_url IS NOT NULL"
    ).fetchall()
    ok = 0
    for row in rows:
        label = f"{row['sku']} @ shop"
        try:
            html = fetch_html(row["shop_url"])
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  FAIL  {label}: {exc}")
            continue
        page = parse.page_from_html(html)
        result = parse.extract(page)
        image = parse.image_url(page)
        if result["price"] is None:
            print(f"  FAIL  {label}: no price on shop page")
            if image:
                conn.execute("UPDATE products SET image_url=? WHERE sku=?", (image, row["sku"]))
                conn.commit()
            continue
        db.record_shop_price(conn, row["sku"], result["price"], image)
        ok += 1
        print(f"  OK    {label}: {result['price']} EUR" + (f"  image={image}" if image else ""))
    print(f"shops: {ok}/{len(rows)} own prices recorded")


def record(conn, match, page):
    result = parse.extract(page)
    status = page.get("metadata", {}).get("statusCode")
    error = None
    if result["price"] is None:
        error = f"no price found (http {status}, source={result['source']})"
        dump_failure(match, page)
    db.add_snapshot(conn, match["id"], result["price"], result["currency"],
                    result["available"], result["source"], error)
    label = f"{match['sku']} @ {match['marketplace']}"
    if error:
        print(f"  FAIL  {label}: {error}")
        return False
    print(f"  OK    {label}: {result['price']} {result['currency']}")
    return True


def direct_fetch(match):
    """Page dict from a plain fetch, or None when the marketplace needs Firecrawl
    or the plain fetch did not yield a price."""
    if match["marketplace"] not in DIRECT_MARKETPLACES:
        return None
    try:
        page = parse.page_from_html(fetch_html(match["url"]))
    except (urllib.error.URLError, TimeoutError):
        return None
    return page if parse.extract(page)["price"] is not None else None


def run_live(conn):
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        sys.exit("FIRECRAWL_API_KEY missing — put it in .env (see .env.example)")
    matches = db.active_matches(conn)
    if len(matches) > MAX_PAGES_PER_RUN:
        sys.exit(f"budget guard: {len(matches)} matches > MAX_PAGES_PER_RUN={MAX_PAGES_PER_RUN}")
    ok = 0
    for match in matches:
        try:
            page = direct_fetch(match) or firecrawl_fetch(match["url"], api_key)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            db.add_snapshot(conn, match["id"], None, None, None, "none", f"fetch error: {exc}")
            print(f"  FAIL  {match['sku']} @ {match['marketplace']}: {exc}")
            continue
        ok += record(conn, match, page)
        time.sleep(REQUEST_PAUSE_S)
    print(f"done: {ok}/{len(matches)} prices recorded")


def run_ingest(conn, path):
    pages = json.loads(Path(path).read_text())
    by_url = {}
    for p in pages:
        by_url[p["url"]] = p
        for alias in p.get("aliases", []):
            by_url[alias] = p
    ok = total = 0
    for match in db.active_matches(conn):
        page = by_url.get(match["url"])
        if not page:
            continue
        total += 1
        ok += record(conn, match, page)
    print(f"done (ingest): {ok}/{total} prices recorded")


def main():
    load_env()
    conn = db.connect()
    db.sync_from_csv(conn)
    refresh_shops(conn)
    if len(sys.argv) >= 3 and sys.argv[1] == "--ingest":
        run_ingest(conn, sys.argv[2])
    else:
        run_live(conn)


if __name__ == "__main__":
    main()
