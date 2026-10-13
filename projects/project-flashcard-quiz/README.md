# Project: Flashcard Quiz

Companion lesson: https://pythonlessonlab.com/lessons/project-flashcard-quiz/

Grade one response per card, accept surrounding whitespace and case differences, and return a list of prompts to review. The grader rejects missing or extra responses instead of silently dropping a card. The website lesson uses fixed responses so its browser console run is repeatable; this local extension reads responses interactively.

Run the quiz:

```powershell
py -3 flashcard_quiz.py
```

Run the tests from this directory:

```powershell
py -3 -m unittest -v
```

To extend it, load cards from a trusted local JSON file, show correct answers after grading, or save progress between sessions.
