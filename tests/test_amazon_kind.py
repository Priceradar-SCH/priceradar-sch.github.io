"""Offline checks for Amazon page classification and the soft-block retry."""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import parse  # noqa: E402
import scrape  # noqa: E402

DUMP_TODAY = Path("/tmp/priceradar-failed-pages")
DUMP_YDAY = Path("/tmp/nov17-failed")


class KindFixtures(unittest.TestCase):
    def test_homepage(self):
        self.assertEqual(
            parse.amazon_page_kind(
                '<link rel="canonical" href="https://www.amazon.de/">',
                {"url": "https://www.amazon.de/"},
                "https://www.amazon.de/dp/B08MV1HD9K",
            ),
            "soft_block",
        )

    def test_locale_homepage(self):
        self.assertEqual(
            parse.amazon_page_kind(
                '<link rel="canonical" href="https://www.amazon.de/-/en/">',
                {"url": "https://www.amazon.de/-/en/"},
                "https://www.amazon.de/dp/B08MV1HD9K",
            ),
            "soft_block",
        )

    def test_product(self):
        html = '<span id="productTitle">X</span><div id="twister-plus-buying-options-price-data">{ }</div>'
        self.assertEqual(
            parse.amazon_page_kind(html, {"url": "https://www.amazon.de/dp/B08MV1HD9K"}, "https://www.amazon.de/dp/B08MV1HD9K"),
            "product",
        )

    def test_no_buybox(self):
        html = '<span id="productTitle">Schiesser 95/5</span>'
        self.assertEqual(
            parse.amazon_page_kind(html, {"url": "https://www.amazon.de/dp/B0G34NXB6F"}, "https://www.amazon.de/dp/B0G34NXB6F"),
            "no_buybox",
        )

    def test_asin_from_url(self):
        self.assertEqual(parse.asin_from_url("https://www.amazon.de/dp/B08MV1HD9K"), "B08MV1HD9K")
        self.assertEqual(parse.asin_from_url("https://www.amazon.de/gp/product/B00HQTQCK0?th=1"), "B00HQTQCK0")
        self.assertIsNone(parse.asin_from_url("https://www.amazon.de/"))


@unittest.skipUnless(DUMP_TODAY.exists(), "today's failed-page dumps not present")
class KindDumpsToday(unittest.TestCase):
    def test_all_today_amazon_dumps_are_soft_blocks_without_price(self):
        files = list(DUMP_TODAY.glob("*amazon*.json"))
        self.assertGreaterEqual(len(files), 8)
        for path in files:
            data = json.loads(path.read_text())
            kind = parse.amazon_page_kind(data.get("html") or "", data.get("metadata") or {}, data.get("url"))
            result = parse.extract(data)
            self.assertEqual(kind, "soft_block", path.name)
            self.assertIsNone(result["price"], path.name)


@unittest.skipUnless((DUMP_YDAY / "183243-908_amazon.json").exists(), "yesterday's dump not present")
class KindDumpYesterday(unittest.TestCase):
    def test_183243_is_product_page_without_buybox(self):
        data = json.loads((DUMP_YDAY / "183243-908_amazon.json").read_text())
        kind = parse.amazon_page_kind(data.get("html") or "", data.get("metadata") or {}, data.get("url"))
        self.assertEqual(kind, "no_buybox")
        self.assertIsNone(parse.extract(data)["price"])


class RetryLogic(unittest.TestCase):
    def test_homepage_then_product_retries_enhanced_nl(self):
        home = {"metadata": {"url": "https://www.amazon.de/", "statusCode": 200}, "html": '<link rel="canonical" href="https://www.amazon.de/">'}
        product = {"metadata": {"url": "https://www.amazon.de/dp/B08MV1HD9K", "statusCode": 200, "proxyUsed": "enhanced"},
                   "html": '<span id="productTitle">X</span><div id="twister-plus-buying-options-price-data">{}</div>'}
        match = {"id": 1, "sku": "173983-000", "marketplace": "amazon", "url": "https://www.amazon.de/dp/B08MV1HD9K"}
        with mock.patch.object(scrape, "firecrawl_fetch", return_value=product) as fetch:
            with mock.patch.object(scrape.time, "sleep"):
                page, fails = scrape.retry_amazon_if_soft_blocked(match, home, "key", 0)
        fetch.assert_called_once()
        kwargs = fetch.call_args
        self.assertEqual(kwargs[0][0], match["url"])
        self.assertEqual(kwargs.kwargs.get("proxy") or (kwargs[1].get("proxy") if kwargs[1] else None), "enhanced")
        # location NL
        loc = kwargs.kwargs.get("location") if kwargs.kwargs else kwargs[1].get("location")
        self.assertEqual(loc["country"], "NL")
        self.assertEqual(fails, 0)
        self.assertEqual(parse.amazon_page_kind(page["html"], page["metadata"], match["url"]), "product")

    def test_two_homepages_count_as_enhanced_failure(self):
        home = {"metadata": {"url": "https://www.amazon.de/", "statusCode": 200}, "html": '<link rel="canonical" href="https://www.amazon.de/">'}
        match = {"id": 1, "sku": "173983-000", "marketplace": "amazon", "url": "https://www.amazon.de/dp/B08MV1HD9K"}
        with mock.patch.object(scrape, "firecrawl_fetch", return_value=home):
            with mock.patch.object(scrape.time, "sleep"):
                page, fails = scrape.retry_amazon_if_soft_blocked(match, home, "key", 0)
        self.assertEqual(fails, 1)
        self.assertEqual(parse.amazon_page_kind(page["html"], page["metadata"], match["url"]), "soft_block")

    def test_circuit_breaker_skips_further_enhanced_calls(self):
        home = {"metadata": {"url": "https://www.amazon.de/", "statusCode": 200}, "html": '<link rel="canonical" href="https://www.amazon.de/">'}
        match = {"id": 1, "sku": "173983-000", "marketplace": "amazon", "url": "https://www.amazon.de/dp/B08MV1HD9K"}
        with mock.patch.object(scrape, "firecrawl_fetch") as fetch:
            page, fails = scrape.retry_amazon_if_soft_blocked(match, home, "key", scrape.ENHANCED_FAIL_LIMIT)
        fetch.assert_not_called()
        self.assertEqual(fails, scrape.ENHANCED_FAIL_LIMIT)

    def test_product_page_is_not_retried(self):
        product = {"metadata": {"url": "https://www.amazon.de/dp/B08MV1HD9K"}, "html": '<span id="productTitle">X</span><div id="twister-plus-buying-options-price-data">{}</div>'}
        match = {"id": 1, "sku": "173983-000", "marketplace": "amazon", "url": "https://www.amazon.de/dp/B08MV1HD9K"}
        with mock.patch.object(scrape, "firecrawl_fetch") as fetch:
            page, fails = scrape.retry_amazon_if_soft_blocked(match, product, "key", 0)
        fetch.assert_not_called()
        self.assertEqual(fails, 0)
        self.assertIs(page, product)


if __name__ == "__main__":
    unittest.main()
