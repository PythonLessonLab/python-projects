import unittest

from log_analyzer import format_report, summarize_log


class LogAnalyzerTests(unittest.TestCase):
    def test_counts_errors_and_skipped_rows(self):
        sample = "t | INFO | Started\nt | error | Retry | attempt 2\nwrong\nt | ERROR | Failed"
        self.assertEqual(
            summarize_log(sample),
            ({"INFO": 1, "ERROR": 2}, ["Retry | attempt 2", "Failed"], 1),
        )

    def test_blank_lines_do_not_count_as_malformed(self):
        self.assertEqual(summarize_log("\n \n"), ({}, [], 0))
        self.assertEqual(summarize_log("t | INFO | \n"), ({}, [], 1))

    def test_report_sorts_levels(self):
        self.assertEqual(
            format_report(({"INFO": 1, "ERROR": 2}, ["Failed"], 0)),
            "ERROR: 2\nINFO: 1\nSkipped: 0\nErrors: Failed",
        )


if __name__ == "__main__":
    unittest.main()
