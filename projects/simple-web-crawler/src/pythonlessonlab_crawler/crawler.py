"""A deliberately small crawler: one origin, bounded work, and robots first."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from time import monotonic, sleep
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser


USER_AGENT = "PythonLessonLabCrawler/1.0 (educational example)"
MAX_HTML_BYTES = 512_000
MAX_ROBOTS_BYTES = 512_000
MAX_LINKS_PER_PAGE = 200
MAX_URL_LENGTH = 2_048


def normalize_url(value: str, base: str | None = None) -> str:
    """Resolve an HTTP(S) URL, remove its fragment, and normalize its origin.

    Queries are kept: ``/search?q=a`` and ``/search?q=b`` can be different pages.
    This is intentionally not a universal URL canonicalizer; servers may assign
    different meanings to case, trailing slashes, or query parameter order.
    """
    absolute = urljoin(base, value) if base else value
    if len(absolute) > MAX_URL_LENGTH:
        raise ValueError("URL is too long")
    parsed = urlsplit(absolute)
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Only absolute HTTP(S) URLs are supported")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs with embedded credentials are not supported")
    try:
        host = parsed.hostname.encode("idna").decode("ascii").lower()
        port = parsed.port
    except (UnicodeError, ValueError) as exc:
        raise ValueError("Invalid URL host or port") from exc
    if port == 0:
        raise ValueError("Port 0 is not valid for crawling")
    if ":" in host:  # IPv6 literals need brackets in URLs.
        host = f"[{host}]"
    netloc = host
    if port is not None and not ((scheme == "http" and port == 80) or (scheme == "https" and port == 443)):
        netloc = f"{host}:{port}"
    # urljoin resolves literal dot segments without decoding %2F or changing
    # query parameters. Start at this origin's root so a path cannot switch it.
    path = urlsplit(urljoin(f"{scheme}://{netloc}/", (parsed.path or "/").lstrip("/"))).path
    return urlunsplit((scheme, netloc, path or "/", parsed.query, ""))


def origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlsplit(url)
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return parsed.scheme, parsed.hostname or "", port


@dataclass(frozen=True)
class Page:
    url: str
    depth: int
    title: str
    links_found: int


@dataclass(frozen=True)
class Skipped:
    url: str
    reason: str


@dataclass
class CrawlReport:
    pages: list[Page] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    requests_made: int = 0
    stop_reason: str = "Queue exhausted"


class _NoRedirects(HTTPRedirectHandler):
    """Never follow a Location header before checking origin and robots."""

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


class _LinksAndTitle(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self.in_title = True
        if tag != "a" or len(self.links) >= MAX_LINKS_PER_PAGE:
            return
        values = dict(attrs)
        if "nofollow" in (values.get("rel") or "").lower().split():
            return
        href = values.get("href")
        if href:
            self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join(" ".join(self.title_parts).split())


class Crawler:
    """Breadth-first crawler. Supply only a site you own or may crawl."""

    def __init__(
        self,
        seed_url: str,
        *,
        max_pages: int = 10,
        max_depth: int = 2,
        request_interval: float = 1.0,
        timeout: float = 10.0,
        clock: Callable[[], float] = monotonic,
        pause: Callable[[float], None] = sleep,
    ) -> None:
        if not 1 <= max_pages <= 100:
            raise ValueError("max_pages must be between 1 and 100")
        if not 0 <= max_depth <= 5:
            raise ValueError("max_depth must be between 0 and 5")
        if request_interval < 0 or timeout <= 0:
            raise ValueError("request_interval must be nonnegative and timeout positive")
        self.seed_url = normalize_url(seed_url)
        self.site_origin = origin(self.seed_url)
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.interval = request_interval
        self.timeout = timeout
        self.clock = clock
        self.pause = pause
        self.next_request_at = 0.0
        self.opener = build_opener(_NoRedirects())
        self.report = CrawlReport()
        # Includes robots.txt and failed HTTP requests, so a site with errors is bounded.
        self.max_requests = 3 * max_pages + 1

    def _open(self, url: str):
        wait = self.next_request_at - self.clock()
        if wait > 0:
            self.pause(wait)
        self.report.requests_made += 1
        try:
            return self.opener.open(Request(url, headers={"User-Agent": USER_AGENT}), timeout=self.timeout)
        finally:
            self.next_request_at = self.clock() + self.interval

    def _load_robots(self) -> RobotFileParser | None:
        # Build from the normalized seed so the non-default port is preserved.
        seed = urlsplit(self.seed_url)
        robots_url = urlunsplit((seed.scheme, seed.netloc, "/robots.txt", "", ""))
        try:
            with self._open(robots_url) as response:
                if response.status != 200:
                    self.report.stop_reason = f"robots.txt returned HTTP {response.status}; stopped"
                    return None
                data = response.read(MAX_ROBOTS_BYTES + 1)
                if len(data) > MAX_ROBOTS_BYTES:
                    self.report.stop_reason = "robots.txt is too large; stopped"
                    return None
        except HTTPError as exc:
            if exc.code == 404:
                # Missing robots.txt means there are no rules at this origin.
                parser = RobotFileParser()
                parser.parse([])
                return parser
            self.report.stop_reason = f"robots.txt returned HTTP {exc.code}; stopped"
            return None
        except (URLError, TimeoutError, OSError) as exc:
            self.report.stop_reason = f"Could not read robots.txt ({type(exc).__name__}); stopped"
            return None

        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.parse(data.decode("utf-8", errors="replace").splitlines())
        # Some sites publish these non-standard directives. Our own interval is
        # always applied as well; these values can only make requests slower.
        delay = parser.crawl_delay(USER_AGENT)
        if delay is not None:
            self.interval = max(self.interval, float(delay))
        rate = parser.request_rate(USER_AGENT)
        if rate and rate.requests > 0:
            self.interval = max(self.interval, rate.seconds / rate.requests)
        # The robots request already set next_request_at using the old interval.
        # Enforce any longer interval before fetching the first page.
        self.next_request_at = max(self.next_request_at, self.clock() + self.interval)
        return parser

    def crawl(self) -> CrawlReport:
        rules = self._load_robots()
        if rules is None:
            return self.report
        queue = deque([(self.seed_url, 0)])
        seen = {self.seed_url}

        while queue and len(self.report.pages) < self.max_pages:
            if self.report.requests_made >= self.max_requests:
                self.report.stop_reason = "Request limit reached"
                break
            url, depth = queue.popleft()
            if not rules.can_fetch(USER_AGENT, url):
                self.report.skipped.append(Skipped(url, "Blocked by robots.txt"))
                continue
            try:
                with self._open(url) as response:
                    content_type = response.headers.get_content_type()
                    if content_type != "text/html":
                        self.report.skipped.append(Skipped(url, f"Not HTML ({content_type})"))
                        continue
                    raw = response.read(MAX_HTML_BYTES + 1)
                    if len(raw) > MAX_HTML_BYTES:
                        self.report.skipped.append(Skipped(url, "HTML exceeds size limit"))
                        continue
                    charset = response.headers.get_content_charset() or "utf-8"
                    try:
                        html = raw.decode(charset, errors="replace")
                    except LookupError:
                        html = raw.decode("utf-8", errors="replace")
            except HTTPError as exc:
                if exc.code in {429, 503}:
                    retry_after = exc.headers.get("Retry-After")
                    suffix = f"; Retry-After: {retry_after}" if retry_after else ""
                    self.report.stop_reason = f"HTTP {exc.code}{suffix}; stopped without retry"
                    self.report.skipped.append(Skipped(url, self.report.stop_reason))
                    break
                # HTTP redirects are deliberately not followed. A future lesson
                # could enqueue same-origin Location URLs after validating them.
                self.report.skipped.append(Skipped(url, f"HTTP {exc.code}; not followed"))
                continue
            except (URLError, TimeoutError, OSError) as exc:
                self.report.skipped.append(Skipped(url, f"Request failed ({type(exc).__name__})"))
                continue

            parser = _LinksAndTitle()
            parser.feed(html)
            self.report.pages.append(Page(url, depth, parser.title, len(parser.links)))
            if depth >= self.max_depth:
                continue
            for href in parser.links:
                try:
                    child = normalize_url(href, url)
                except ValueError:
                    continue
                if origin(child) != self.site_origin or child in seen:
                    continue
                seen.add(child)
                queue.append((child, depth + 1))

        if len(self.report.pages) >= self.max_pages:
            self.report.stop_reason = "Page limit reached"
        return self.report
