import unittest

from flashcard_quiz import grade_flashcards


class FlashcardQuizTests(unittest.TestCase):
    def test_score_and_review_order(self):
        cards = [
            {"prompt": "A?", "answer": "yes"},
            {"prompt": "B?", "answer": "no"},
            {"prompt": "C?", "answer": "yes"},
        ]
        self.assertEqual(
            grade_flashcards(cards, [" wrong ", "NO", "wrong"]),
            {"correct": 1, "total": 3, "missed": ["A?", "C?"]},
        )

    def test_empty_deck(self):
        self.assertEqual(grade_flashcards([], []), {"correct": 0, "total": 0, "missed": []})

    def test_length_mismatch_is_rejected(self):
        cards = [{"prompt": "A?", "answer": "a"}]
        with self.assertRaises(ValueError):
            grade_flashcards(cards, [])
        with self.assertRaises(ValueError):
            grade_flashcards(cards, ["a", "extra"])


if __name__ == "__main__":
    unittest.main()
