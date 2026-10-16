import unittest

from offline_crawler import crawl_fixture


ROOT = "https://example.test/"


class OfflineCrawlerTests(unittest.TestCase):
    def setUp(self):
        self.pages = {
            ROOT: '<a href="/a">A</a><a href="/b">B</a>',
            ROOT + "a": '<a href="/">Home</a><a href="/c#part">C</a>',
            ROOT + "b": '<a href="/c">C</a>',
            ROOT + "c": '<a href="/a">A</a>',
        }

    def test_breadth_first_order_without_cycle_or_duplicate(self):
        self.assertEqual(
            crawl_fixture(self.pages, ROOT, 10),
            [ROOT, ROOT + "a", ROOT + "b", ROOT + "c"],
        )

    def test_page_limit_is_respected(self):
        self.assertEqual(crawl_fixture(self.pages, ROOT, 2), [ROOT, ROOT + "a"])

    def test_fragment_duplicates_and_unknown_links_are_skipped(self):
        pages = {
            ROOT: '<a href="/a#one">A</a><a href="/a#two">A2</a><a href="https://other.test/">X</a>',
            ROOT + "a": "",
        }
        self.assertEqual(crawl_fixture(pages, ROOT), [ROOT, ROOT + "a"])

    def test_invalid_start_and_limit(self):
        for start, limit in ((ROOT, 0), (ROOT, True), ("https://missing.test/", 2)):
            with self.subTest(start=start, limit=limit), self.assertRaises(ValueError):
                crawl_fixture(self.pages, start, limit)


if __name__ == "__main__":
    unittest.main()
