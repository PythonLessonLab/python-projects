"""Behavior checks for the in-memory Contact Book."""

import unittest

from contact_book import add_contact, find_contact


class ContactBookTests(unittest.TestCase):
    def test_find_ignores_case_and_edge_spaces(self):
        book = {}
        add_contact(book, "Ada Lovelace", "ada@example.com")
        self.assertEqual(find_contact(book, "  ADA LOVELACE  ")["email"], "ada@example.com")

    def test_adding_same_name_updates_record(self):
        book = {}
        add_contact(book, "Ada Lovelace", "ada@example.com")
        add_contact(book, " ada LOVELACE ", " ada.new@example.com ")
        self.assertEqual(len(book), 1)
        self.assertEqual(find_contact(book, "ADA LOVELACE")["email"], "ada.new@example.com")

    def test_absent_name_returns_none(self):
        self.assertIsNone(find_contact({}, "Unknown Person"))

    def test_blank_name_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "name cannot be blank"):
            add_contact({}, "  ", "person@example.com")

    def test_blank_email_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "email cannot be blank"):
            add_contact({}, "Ada Lovelace", "  ")


if __name__ == "__main__":
    unittest.main()
