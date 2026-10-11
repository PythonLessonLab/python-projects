# Simple Web Crawler — a PythonLessonLab project

Build a small breadth-first crawler and learn how HTTP requests, HTML links,
queues, URL normalization, and `robots.txt` fit together. The project uses only
Python's standard library and starts on a **local practice site**.

## Run the local example

Use Python 3.10 or newer. On Windows, use `py -3.10` for the commands below
if `python` selects an older version. In one terminal, from this directory:

```bash
python -m http.server 8000 --directory fixtures/site
```

In another terminal, install this local project and run the crawler:

```bash
python -m pip install -e .
python -m pythonlessonlab_crawler http://127.0.0.1:8000/index.html
```

The installation also provides the `pythonlessonlab-crawl` command.

The expected page titles are **Crawler practice site**, **Guide**, and
**Notes**. The crawler skips `/private/secret.html` because the fixture's
`robots.txt` disallows it. It also ignores the external link and visits
`guide.html` only once even though the index links to two fragments of it.

Run the tests without installing anything:

```bash
python -m unittest discover -s tests -v
```

## How it works

1. **Fetch `robots.txt` first.** The crawler asks whether its user agent may
   fetch each URL. It stops if the rules cannot be read safely. A missing
   `robots.txt` (HTTP 404) means no rules were published for that origin.
2. **Keep a FIFO queue.** Each entry stores a URL and its link depth. Removing
   from the front explores pages breadth first.
3. **Normalize and deduplicate.** Relative links become absolute links;
   fragments are removed and default ports normalized. A `seen` set prevents
   duplicate requests. Query strings remain because they may select different
   content.
4. **Stay on one origin.** A different scheme, host, or port is not queued.
   HTTP redirects are not followed, since their destination may leave the
   origin or bypass the robots check.
5. **Bound the work.** Page, depth, total request, response size, link count,
   and timeout limits keep this an educational sample rather than an open-ended
   site crawl. It waits at least one second between requests by default and
   honors a longer `Crawl-delay` or `Request-rate` when present.
6. **Stop on overload.** A page returning HTTP 429 or 503 ends the run. The
   response's `Retry-After` value is reported; the crawler does not retry
   automatically.

Open [`src/pythonlessonlab_crawler/crawler.py`](src/pythonlessonlab_crawler/crawler.py)
and follow `Crawler.crawl()` from the queue initialization to the page parser.
The local HTTP tests in [`tests/test_crawler.py`](tests/test_crawler.py) cover
deduplication, depth, `robots.txt`, rate limits, redirects, and HTTP 429.

## Try a site you may crawl

The command refuses a public URL unless you add `--allow-public`:

```bash
python -m pythonlessonlab_crawler https://YOUR-OWN-DOMAIN.example/ \
  --allow-public --max-pages 5 --max-depth 1 --interval 2
```

Use a domain you own or have permission to crawl. `robots.txt` expresses crawl
preferences; it is not a grant of permission. Public targets must resolve to
public IP addresses and use an interval of at least one second. Keep your first
run small and check the output before increasing any limit. This program is a
tutorial, not a security boundary or a production crawler.

## Small exercises

- Print the number of links found per page as a table.
- Save page URLs and titles to a CSV file.
- Add same-origin redirect handling **after** checking the destination against
  the origin and `robots.txt` rules.
- Test a `503` response and explain why stopping is safer than immediate retry.

For the broader Python learning path, visit [PythonLessonLab](https://pythonlessonlab.com/).

## Notes on `robots.txt`

The example uses Python's
[`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html).
The core robots rules are defined in [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html).
`Crawl-delay` and `Request-rate` are optional extensions understood by Python's
parser; the crawler always applies its own fixed minimum interval as well.

## License

MIT. See the repository [LICENSE](../../LICENSE).
