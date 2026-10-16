import hashlib
import io
import unittest
import warnings
import zipfile

from archive_manifest import verify_archive


def make_zip(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in members:
            archive.writestr(name, data)
    return buffer.getvalue()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ArchiveManifestTests(unittest.TestCase):
    def test_reports_all_three_categories(self):
        archive = make_zip([("a.txt", b"alpha"), ("b.txt", b"bad"), ("c.txt", b"extra")])
        manifest = {"a.txt": digest(b"alpha"), "b.txt": digest(b"good"), "old.txt": digest(b"old")}
        self.assertEqual(
            verify_archive(archive, manifest),
            {"missing": ["old.txt"], "extra": ["c.txt"], "changed": ["b.txt"]},
        )

    def test_sorted_empty_and_directory_behavior(self):
        archive = make_zip([("dir/", b""), ("dir/x.txt", b"ok")])
        self.assertEqual(
            verify_archive(archive, {"dir/x.txt": digest(b"ok")}),
            {"missing": [], "extra": [], "changed": []},
        )
        empty = make_zip([])
        self.assertEqual(
            verify_archive(empty, {"z.txt": digest(b"z"), "a.txt": digest(b"a")}),
            {"missing": ["a.txt", "z.txt"], "extra": [], "changed": []},
        )

    def test_duplicate_member_name_is_ambiguous(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            archive = make_zip([("same.txt", b"a"), ("same.txt", b"b")])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_archive(archive, {})


if __name__ == "__main__":
    unittest.main()
