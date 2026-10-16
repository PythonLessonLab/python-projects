# Project: Archive Manifest Verifier

Companion lesson: https://pythonlessonlab.com/lessons/project-archive-manifest-verifier/

Compare a small ZIP fixture with a manifest mapping member names to expected
SHA-256 digests. The result has sorted `missing`, `extra`, and `changed` lists.
Members are read from an in-memory buffer; the code never extracts them.

From this directory:

```powershell
py -3 archive_manifest.py
py -3 -m unittest -v
```

Expected demo: `old.txt` is missing, `c.txt` is extra, and `b.txt` changed.
The manifest must come from a trusted source if you need publisher authenticity:
an attacker who replaces both archive and manifest can create matching hashes.
This fixture project does not impose resource limits needed for arbitrary
untrusted archives.
