"""Command-line entry point for the tutorial crawler."""

from __future__ import annotations

import argparse
import ipaddress
import socket
from urllib.parse import urlsplit

from .crawler import Crawler, normalize_url


def _public_target_is_global(host: str) -> bool:
    """Reject obvious private targets before the optional public-site demo."""
    try:
        addresses = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False
    return bool(addresses) and all(
        ipaddress.ip_address(item[4][0]).is_global for item in addresses
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Crawl a small number of pages on one site, respecting robots.txt."
    )
    parser.add_argument("url", help="A local fixture URL, or a permitted public site")
    parser.add_argument("--max-pages", type=int, default=10, help="1-100 HTML pages (default: 10)")
    parser.add_argument("--max-depth", type=int, default=2, help="0-5 link hops (default: 2)")
    parser.add_argument("--interval", type=float, default=1.0, help="Minimum seconds between requests (default: 1)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout per request in seconds (default: 10)")
    parser.add_argument(
        "--allow-public",
        action="store_true",
        help="Required for a public site you own or have permission to crawl",
    )
    args = parser.parse_args(argv)

    try:
        seed = normalize_url(args.url)
    except ValueError as exc:
        parser.error(str(exc))
    host = urlsplit(seed).hostname or ""
    is_local = host in {"localhost", "127.0.0.1", "::1"}
    if not is_local and not args.allow_public:
        parser.error("Public URLs require --allow-public and permission from the site owner")
    if not is_local and not _public_target_is_global(host):
        parser.error("The target must resolve only to public IP addresses")
    if not is_local and args.interval < 1.0:
        parser.error("Public sites require --interval of at least 1 second")
    try:
        crawler = Crawler(
            seed,
            max_pages=args.max_pages,
            max_depth=args.max_depth,
            request_interval=args.interval,
            timeout=args.timeout,
        )
    except ValueError as exc:
        parser.error(str(exc))

    report = crawler.crawl()
    for page in report.pages:
        print(f"depth={page.depth}  {page.url}")
        print(f"  title: {page.title or '(none)'}; links found: {page.links_found}")
    for item in report.skipped:
        print(f"skipped: {item.url} - {item.reason}")
    print(f"\nPages: {len(report.pages)} | HTTP requests: {report.requests_made}")
    print(f"Stopped: {report.stop_reason}")
    return 0 if report.pages else 1
