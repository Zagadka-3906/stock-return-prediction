"""Check lookup continuity when later cleanups remove older retained copies."""
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from tools.find_archive_record import find_record, resolve_record


class ArchiveLookupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def catalog(self, name, rows):
        path = self.root / name
        with gzip.open(path, "wt", encoding="utf-8") as stream:
            for row in rows:
                stream.write(json.dumps(row) + "\n")
        return path

    def test_old_lookup_follows_new_copy_without_mutating_record(self):
        old = {"removed_path": "old/a.py", "retained_path": "analysis/a.py", "git_blob_oid": "same"}
        new = {"removed_path": "analysis/a.py", "retained_path": "frozen/a.py", "git_blob_oid": "same"}
        catalogs = [self.catalog("new.gz", [new]), self.catalog("old.gz", [old])]
        found = find_record("old/a.py", catalogs)
        result = resolve_record(found, catalogs)
        self.assertEqual(result["retained_path"], "frozen/a.py")
        self.assertEqual(result["retained_path_chain"], ["old/a.py", "analysis/a.py", "frozen/a.py"])
        self.assertEqual(found, old)

    def test_newest_catalog_takes_precedence(self):
        old = {"removed_path": "a.py", "retained_path": "old.py"}
        new = {"removed_path": "a.py", "retained_path": "new.py"}
        catalogs = [self.catalog("new.gz", [new]), self.catalog("old.gz", [old])]
        self.assertEqual(find_record("a.py", catalogs), new)
        self.assertIsNone(find_record("missing.py", catalogs))

    def test_explicit_single_catalog_remains_supported(self):
        row = {"removed_path": "a.py", "retained_path": "b.py"}
        catalogs = [self.catalog("one.gz", [row])]
        self.assertEqual(resolve_record(find_record("a.py", catalogs), catalogs), row)

    def test_mapping_cycle_is_rejected(self):
        rows = [{"removed_path": "a.py", "retained_path": "b.py"},
                {"removed_path": "b.py", "retained_path": "a.py"}]
        catalogs = [self.catalog("cycle.gz", rows)]
        with self.assertRaisesRegex(ValueError, "cycle"):
            resolve_record(rows[0], catalogs)

    def test_mapping_cannot_change_content_identity(self):
        rows = [{"removed_path": "a.py", "retained_path": "b.py", "git_blob_oid": "first"},
                {"removed_path": "b.py", "retained_path": "c.py", "git_blob_oid": "different"}]
        catalogs = [self.catalog("mismatch.gz", rows)]
        with self.assertRaisesRegex(ValueError, "identity"):
            resolve_record(rows[0], catalogs)

    def test_removed_last_copy_preserves_historical_fallback(self):
        rows = [{"removed_path": "a.py", "retained_path": "b.py"},
                {"removed_path": "b.py", "historical_url": "https://example.com/b.py"}]
        catalogs = [self.catalog("historical.gz", rows)]
        result = resolve_record(rows[0], catalogs)
        self.assertIsNone(result["retained_path"])
        self.assertEqual(result["resolved_historical_url"], "https://example.com/b.py")


if __name__ == "__main__":
    unittest.main()
