"""Breadth-first traversal over an in-memory HTML fixture graph only."""

from __future__ import annotations

from collections import deque
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.extend(value for key, value in attrs if key == "href" and value)


def crawl_fixture(pages, start, max_pages=10):
    """Visit fixture URLs once in BFS order, stopping after max_pages.

    No HTTP request is made. Only keys already present in pages may be queued.
    """
    if start not in pages or type(max_pages) is not int or max_pages <= 0:
        raise ValueError("invalid start or page limit")
    queue = deque([start])
    queued = {start}
    visited = []
    while queue and len(visited) < max_pages:
        url = queue.popleft()
        visited.append(url)
        parser = LinkParser()
        parser.feed(pages[url])
        for href in parser.links:
            target = urldefrag(urljoin(url, href)).url
            if target in pages and target not in queued:
                queued.add(target)
                queue.append(target)
    return visited


if __name__ == "__main__":
    root = "https://example.test/"
    pages = {
        root: '<a href="/a">A</a><a href="/b">B</a>',
        root + "a": '<a href="/">Home</a><a href="/c#part">C</a>',
        root + "b": '<a href="/c">C</a>',
        root + "c": '<a href="/a">A</a>',
    }
    print(crawl_fixture(pages, root, 4))
