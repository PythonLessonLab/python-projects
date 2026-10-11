"""Local HTTP tests: no test contacts a public web site."""

from __future__ import annotations

import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pythonlessonlab_crawler import Crawler, normalize_url  # noqa: E402


class LocalSiteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.routes: dict[str, tuple[int, str, bytes, dict[str, str]]] = {}
        self.hits: list[str] = []
        site = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                site.hits.append(self.path)
                status, content_type, body, headers = site.routes.get(
                    self.path,
                    (404, "text/plain", b"Not found", {}),
                )
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def add(
        self,
        path: str,
        body: str,
        *,
        status: int = 200,
        content_type: str = "text/html; charset=utf-8",
        headers: dict[str, str] | None = None,
    ) -> None:
        self.routes[path] = (status, content_type, body.encode(), headers or {})

    def test_url_normalization_keeps_query_and_drops_fragment(self) -> None:
        self.assertEqual(
            normalize_url("HTTP://Example.COM:80/a/../b?q=1#section"),
            "http://example.com/b?q=1",
        )
        self.assertEqual(
            normalize_url("../next#x", "https://example.com/a/page"),
            "https://example.com/next",
        )
        with self.assertRaises(ValueError):
            normalize_url("http://user:password@example.com/")
        with self.assertRaises(ValueError):
            normalize_url("javascript:alert(1)", "https://example.com/")

    def test_breadth_first_deduplicates_and_obeys_robots_and_origin(self) -> None:
        self.add(
            "/robots.txt",
            "User-agent: PythonLessonLabCrawler\nDisallow: /private/\n",
            content_type="text/plain",
        )
        self.add(
            "/",
            "<title>Start</title>"
            '<a href="/a#one">A</a><a href="/a#two">A again</a>'
            '<a href="/b">B</a><a href="/private/secret">Private</a>'
            '<a href="https://example.org/offsite">Outside</a>'
            '<a href="/ignored" rel="nofollow">No follow</a>',
        )
        self.add("/a", '<title>A</title><a href="/c">C</a>')
        self.add("/b", "<title>B</title>")
        self.add("/c", "<title>C</title>")
        crawler = Crawler(self.base + "/", max_pages=10, max_depth=2, request_interval=0)
        report = crawler.crawl()

        self.assertEqual([p.title for p in report.pages], ["Start", "A", "B", "C"])
        self.assertEqual([p.depth for p in report.pages], [0, 1, 1, 2])
        self.assertEqual(self.hits.count("/a"), 1)
        self.assertNotIn("/private/secret", self.hits)
        self.assertNotIn("/ignored", self.hits)
        self.assertTrue(any(item.reason == "Blocked by robots.txt" for item in report.skipped))
        self.assertEqual(report.requests_made, 5)  # robots + four HTML pages

    def test_missing_robots_allows_a_bounded_local_crawl(self) -> None:
        self.add("/", "<title>Start</title><a href='/next'>Next</a>")
        self.add("/next", "<title>Next</title>")
        report = Crawler(self.base, max_pages=1, request_interval=0).crawl()
        self.assertEqual([p.title for p in report.pages], ["Start"])
        self.assertEqual(report.stop_reason, "Page limit reached")
        self.assertEqual(self.hits, ["/robots.txt", "/"])

    def test_robots_server_error_fails_closed(self) -> None:
        self.add("/robots.txt", "Unavailable", status=503, content_type="text/plain")
        self.add("/", "<title>Should not be read</title>")
        report = Crawler(self.base, request_interval=0).crawl()
        self.assertEqual(report.pages, [])
        self.assertEqual(self.hits, ["/robots.txt"])
        self.assertIn("robots.txt returned HTTP 503", report.stop_reason)

    def test_429_stops_without_retrying_or_visiting_next_url(self) -> None:
        self.add("/robots.txt", "User-agent: *\nDisallow:\n", content_type="text/plain")
        self.add("/", "<title>Start</title><a href='/busy'>Busy</a><a href='/later'>Later</a>")
        self.add("/busy", "Slow down", status=429, headers={"Retry-After": "120"})
        self.add("/later", "<title>Later</title>")
        report = Crawler(self.base, request_interval=0).crawl()
        self.assertEqual([p.title for p in report.pages], ["Start"])
        self.assertIn("HTTP 429; Retry-After: 120", report.stop_reason)
        self.assertNotIn("/later", self.hits)
        self.assertEqual(self.hits.count("/busy"), 1)

    def test_503_page_stops_without_retry(self) -> None:
        self.add("/robots.txt", "User-agent: *\nDisallow:\n", content_type="text/plain")
        self.add("/", "<title>Start</title><a href='/busy'>Busy</a>")
        self.add("/busy", "Temporarily unavailable", status=503)
        report = Crawler(self.base, request_interval=0).crawl()
        self.assertIn("HTTP 503", report.stop_reason)
        self.assertEqual(self.hits.count("/busy"), 1)

    def test_redirect_is_not_followed_even_if_location_is_external(self) -> None:
        self.add("/robots.txt", "User-agent: *\nDisallow:\n", content_type="text/plain")
        self.add("/", "<title>Start</title><a href='/redirect'>Redirect</a>")
        self.add(
            "/redirect",
            "Moved",
            status=302,
            headers={"Location": "https://example.org/should-not-be-requested"},
        )
        report = Crawler(self.base, request_interval=0).crawl()
        self.assertEqual([p.title for p in report.pages], ["Start"])
        self.assertTrue(any("HTTP 302" in item.reason for item in report.skipped))
        self.assertEqual(self.hits, ["/robots.txt", "/", "/redirect"])

    def test_robots_crawl_delay_can_only_increase_request_interval(self) -> None:
        self.add(
            "/robots.txt",
            "User-agent: PythonLessonLabCrawler\nCrawl-delay: 2\nDisallow:\n",
            content_type="text/plain",
        )
        self.add("/", "<title>Start</title>")
        fake_time = [0.0]
        waits: list[float] = []

        def fake_pause(seconds: float) -> None:
            waits.append(seconds)
            fake_time[0] += seconds

        crawler = Crawler(
            self.base,
            request_interval=1,
            clock=lambda: fake_time[0],
            pause=fake_pause,
        )
        report = crawler.crawl()
        self.assertEqual([p.title for p in report.pages], ["Start"])
        self.assertEqual(crawler.interval, 2)
        self.assertEqual(waits, [2])


if __name__ == "__main__":
    unittest.main()
