"""Deterministic price extraction from scraped pages. No LLM involved.

Extraction order per page:
  1. Firecrawl metadata (og/twitter/product meta tags) — covers Zalando
  2. JSON-LD <script type="application/ld+json"> Product/Offer blocks
  3. Amazon buy-box JSON (Amazon has neither price meta tags nor JSON-LD)
"""
import html as htmllib
import json
import re

META_PRICE_KEYS = (
    "product:price:amount",
    "og:price:amount",
    "twitter:data1",
)


def parse_price_str(s):
    """'95,95 €' / '€ 1.234,56' / '95.95' -> float, else None."""
    if not s:
        return None
    m = re.search(r"(\d{1,3}(?:[.\s]\d{3})*,\d{1,2}|\d+(?:\.\d{1,2})?)", str(s))
    if not m:
        return None
    num = m.group(1)
    if "," in num:
        num = num.replace(".", "").replace(" ", "").replace(",", ".")
    try:
        return float(num)
    except ValueError:
        return None


def from_metadata(meta):
    for key in META_PRICE_KEYS:
        if key == "twitter:data1" and meta.get("twitter:label1") not in ("Preis", "Price"):
            continue
        price = parse_price_str(meta.get(key))
        if price is not None:
            return price
    return None


def _iter_jsonld(html):
    pattern = r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>"
    for m in re.finditer(pattern, html, re.S | re.I):
        raw = m.group(1).strip()
        # Try the block verbatim first: Otto embeds entity-escaped quotes
        # (&#34;) inside JSON strings, and unescaping them first breaks the JSON.
        for candidate in (raw, htmllib.unescape(raw)):
            try:
                yield json.loads(candidate)
                break
            except json.JSONDecodeError:
                continue


def _walk(node):
    """Yield every dict inside arbitrarily nested JSON-LD."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def from_jsonld(html):
    """-> (price, currency, available) or (None, None, None)."""
    for doc in _iter_jsonld(html):
        for node in _walk(doc):
            if str(node.get("@type", "")).lower() not in ("product", "productgroup"):
                continue
            for offer in _walk(node.get("offers", {})):
                price = parse_price_str(offer.get("price") or offer.get("lowPrice"))
                if price is None:
                    continue
                currency = offer.get("priceCurrency") or "EUR"
                availability = str(offer.get("availability", ""))
                available = None
                if availability:
                    available = "instock" in availability.lower().replace(" ", "")
                return price, currency, available
    return None, None, None


def from_amazon(html):
    """-> (price, available) or (None, None).

    Amazon keeps the buy-box price of the variant the page shows in a hidden
    JSON div. Pages that only show a size/colour price range have no buy box,
    and they stay without a price rather than picking one end of the range.
    """
    m = re.search(r"twister-plus-buying-options-price-data\"[^>]*>\s*(\{.*?\})\s*</div>",
                  html, re.S)
    if not m:
        return None, None
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None, None
    for offer in data.get("desktop_buybox_group_1") or []:
        price = parse_price_str(offer.get("priceAmount"))
        if price is None:
            continue
        status = re.search(r"id=\"availability\" class=\"a-section[^>]*>(.*?)</div>", html, re.S)
        available = None
        if status:
            available = "nicht verfügbar" not in re.sub(r"<[^>]+>", " ", status.group(1))
        return price, available
    return None, None


def _meta_map(html):
    meta = {}
    for tag in re.findall(r"<meta\b[^>]*>", html or "", re.I):
        key = re.search(r"(?:property|name|itemprop)\s*=\s*[\"']([^\"']+)[\"']", tag, re.I)
        val = re.search(r"content\s*=\s*[\"']([^\"']*)[\"']", tag, re.I)
        if key and val:
            meta[key.group(1)] = htmllib.unescape(val.group(1))
    return meta


def page_from_html(html):
    """Build the {metadata, html} dict extract() expects, from a raw page."""
    return {"metadata": _meta_map(html), "html": html or ""}


def image_url(page):
    """og:image (then twitter:image) from a fetched page, absolute https URL."""
    meta = page.get("metadata") or {}
    html = page.get("html") or ""
    img = meta.get("og:image") or meta.get("twitter:image")
    if not img:
        img = _meta_map(html).get("og:image")
    if not img:
        return None
    img = img.strip()
    if img.startswith("//"):
        img = "https:" + img
    elif img.startswith("http://"):
        img = "https://" + img[len("http://"):]
    return img or None


AMAZON_HOST_RE = re.compile(r"(?:^|\.)amazon\.[a-z.]+$", re.I)
AMAZON_ASIN_RE = re.compile(r"/(?:dp|gp/product|gp/aw/d)/([A-Z0-9]{10})", re.I)


def asin_from_url(url):
    """ASIN from an amazon.de /dp/ or /gp/product/ URL, else None."""
    if not url:
        return None
    m = AMAZON_ASIN_RE.search(url)
    return m.group(1).upper() if m else None


def _amazon_is_homepage(url):
    if not url:
        return False
    m = re.match(r"https?://([^/]+)(/[^?]*)?", url, re.I)
    if not m:
        return False
    host, path = m.group(1).split(":")[0], (m.group(2) or "/")
    if not AMAZON_HOST_RE.search(host):
        return False
    if AMAZON_ASIN_RE.search(path):
        return False
    # "/" or locale roots like "/-/en/" or "/-/de/"
    return bool(re.match(r"^/(?:-/?\w{2,3}/?)?$", path))


def amazon_page_kind(html, meta=None, requested_url=None):
    """Classify a fetched Amazon page: 'product', 'no_buybox', or 'soft_block'.

    Amazon sometimes answers HTTP 200 with the homepage instead of the product
    (a soft block). Those pages must not be parsed for a price, because they
    only carry carousel offers.
    """
    meta = meta or {}
    html = html or ""
    low = html.lower()
    if "validatecaptcha" in low or "opfcaptcha" in low or "enter the characters you see" in low:
        return "soft_block"
    canonical = ""
    cm = re.search(r'rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, re.I)
    if not cm:
        cm = re.search(r'href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']', html, re.I)
    if cm:
        canonical = cm.group(1)
    final = meta.get("url") or ""
    if _amazon_is_homepage(final) or _amazon_is_homepage(canonical):
        return "soft_block"
    has_title = bool(re.search(r'id=["\']productTitle["\']', html))
    has_buybox = "twister-plus-buying-options-price-data" in html
    if not has_title and not has_buybox:
        return "soft_block"
    if has_title and not has_buybox:
        return "no_buybox"
    return "product"


def extract(page):
    """page: {"metadata": {...}, "html": "..."} (either part may be missing).
    -> {"price", "currency", "available", "source"}
    """
    meta = page.get("metadata") or {}
    html = page.get("html") or page.get("rawHtml") or ""

    jl_price, jl_currency, jl_available = from_jsonld(html)
    meta_price = from_metadata(meta)

    # Meta tags carry the price actually displayed (incl. sale discounts) on
    # Zalando, while its JSON-LD holds the list price — so meta wins on conflict.
    if meta_price is not None:
        currency = (jl_currency or meta.get("og:price:currency")
                    or meta.get("product:price:currency") or "EUR")
        source = "meta" if jl_price in (None, meta_price) else "meta>jsonld"
        return {"price": meta_price, "currency": currency,
                "available": jl_available, "source": source}
    if jl_price is not None:
        return {"price": jl_price, "currency": jl_currency,
                "available": jl_available, "source": "jsonld"}
    amz_price, amz_available = from_amazon(html)
    if amz_price is not None:
        return {"price": amz_price, "currency": "EUR",
                "available": amz_available, "source": "amazon"}
    return {"price": None, "currency": None, "available": None, "source": "none"}
