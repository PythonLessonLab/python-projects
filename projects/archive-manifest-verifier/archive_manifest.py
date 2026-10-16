"""Compare small ZIP fixture members with a trusted SHA-256 manifest."""

from __future__ import annotations

import hashlib
import io
import zipfile


def verify_archive(zip_bytes, manifest):
    """Return sorted missing, extra, changed member names without extraction.

    This educational function reads members in memory. It is not a general
    untrusted-archive processor or a publisher-authentication mechanism.
    """
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        names = [info.filename for info in archive.infolist() if not info.is_dir()]
        if len(names) != len(set(names)):
            raise ValueError("duplicate ZIP member")
        actual = set(names)
        expected = set(manifest)
        changed = sorted(
            name
            for name in expected & actual
            if hashlib.sha256(archive.read(name)).hexdigest() != manifest[name]
        )
        return {
            "missing": sorted(expected - actual),
            "extra": sorted(actual - expected),
            "changed": changed,
        }


if __name__ == "__main__":
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("a.txt", b"alpha")
        archive.writestr("b.txt", b"bad")
        archive.writestr("c.txt", b"extra")
    manifest = {
        name: hashlib.sha256(data).hexdigest()
        for name, data in (("a.txt", b"alpha"), ("b.txt", b"good"), ("old.txt", b"old"))
    }
    print(verify_archive(buffer.getvalue(), manifest))
