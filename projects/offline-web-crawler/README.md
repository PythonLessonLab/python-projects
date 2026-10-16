# Project: Offline Web Crawler

Companion lesson: https://pythonlessonlab.com/lessons/project-offline-web-crawler/

This **offline fixture** maps URL strings to local HTML strings. `crawl_fixture`
extracts anchor links, resolves relative URLs, removes fragments, and visits only
fixture keys in breadth-first order. A seen set prevents cycles, and `max_pages`
bounds visits. It makes **no HTTP requests**.

From this directory:

```powershell
py -3 offline_crawler.py
py -3 -m unittest -v
```

Expected demo order: home, `/a`, `/b`, `/c`, each once. Try a cycle and two
links with different fragments to one page. For a **separate local-network
tutorial**, see [Simple Web Crawler](../simple-web-crawler/), which adds request
handling, a local practice site, robots rules, and rate limits. Do not present
this in-browser fixture as a live crawl of public websites.
