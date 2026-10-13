"""Deterministic flashcard grading with a small interactive example."""

from __future__ import annotations


DEFAULT_CARDS = [
    {"prompt": "Function keyword?", "answer": "def"},
    {"prompt": "Key-value collection?", "answer": "dict"},
    {"prompt": "Exit a loop?", "answer": "break"},
]


def grade_flashcards(cards: list[dict[str, str]], responses: list[str]) -> dict:
    """Return correct and total counts plus missed prompts in deck order."""
    if len(cards) != len(responses):
        raise ValueError("One response is required for each card")
    correct = 0
    missed: list[str] = []
    for card, response in zip(cards, responses):
        if response.strip().casefold() == card["answer"].strip().casefold():
            correct += 1
        else:
            missed.append(card["prompt"])
    return {"correct": correct, "total": len(cards), "missed": missed}


def main() -> None:
    responses = [input(card["prompt"] + " ") for card in DEFAULT_CARDS]
    report = grade_flashcards(DEFAULT_CARDS, responses)
    print(f"Score: {report['correct']}/{report['total']}")
    if report["missed"]:
        print("Review: " + ", ".join(report["missed"]))
    else:
        print("No missed cards")


if __name__ == "__main__":
    main()
