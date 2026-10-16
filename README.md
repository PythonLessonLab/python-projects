# PythonLessonLab projects

Runnable companion code for [PythonLessonLab](https://pythonlessonlab.com/). Each project has a lesson with a Python console, checked exercise, quiz, and video walkthrough. All nine projects below use only the Python standard library.

| Project | Learn and watch | Code |
| --- | --- | --- |
| CSV Expense Tracker | [Lesson](https://pythonlessonlab.com/lessons/project-csv-expense-tracker/) | [Open folder](projects/csv-expense-tracker/) |
| Contact Book | [Lesson](https://pythonlessonlab.com/lessons/project-contact-book/) | [Open folder](projects/contact-book/) |
| Log Analyzer | [Lesson](https://pythonlessonlab.com/lessons/project-log-analyzer/) | [Open folder](projects/project-log-analyzer/) |
| Flashcard Quiz | [Lesson](https://pythonlessonlab.com/lessons/project-flashcard-quiz/) | [Open folder](projects/project-flashcard-quiz/) |
| Inventory Reorder Planner | [Lesson](https://pythonlessonlab.com/lessons/project-inventory-reorder-planner/) | [Open folder](projects/inventory-reorder-planner/) |
| Booking Conflict Detector | [Lesson](https://pythonlessonlab.com/lessons/project-booking-conflict-detector/) | [Open folder](projects/booking-conflict-detector/) |
| CSV Import Validator | [Lesson](https://pythonlessonlab.com/lessons/project-csv-import-validator/) | [Open folder](projects/csv-import-validator/) |
| Archive Manifest Verifier | [Lesson](https://pythonlessonlab.com/lessons/project-archive-manifest-verifier/) | [Open folder](projects/archive-manifest-verifier/) |
| Offline Web Crawler | [Lesson](https://pythonlessonlab.com/lessons/project-offline-web-crawler/) | [Open folder](projects/offline-web-crawler/) |

## Advanced project: Simple Web Crawler

The [Simple Web Crawler tutorial and code](projects/simple-web-crawler/) use a local practice site to teach HTTP requests, HTML parsing, queues, URL normalization, and robots.txt. The crawler stays on one origin and limits requests. Its separate companion lesson and video are planned.

## Quick start

Install Python 3.10 or newer. On Windows, use py -3 in place of python if necessary. From the repository root:

    python projects/csv-expense-tracker/expense_tracker.py
    python projects/contact-book/contact_book.py
    python projects/project-flashcard-quiz/flashcard_quiz.py
    python -m unittest discover -s projects/inventory-reorder-planner -p "test_*.py"
    python -m unittest discover -s projects/booking-conflict-detector -p "test_*.py"
    python -m unittest discover -s projects/csv-import-validator -p "test_*.py"
    python -m unittest discover -s projects/archive-manifest-verifier -p "test_*.py"
    python -m unittest discover -s projects/offline-web-crawler -p "test_*.py"

Read each project folder's README for its expected output and experiments. The separate live crawler has its own [local practice instructions](projects/simple-web-crawler/README.md). Example names, addresses, and amounts are fictional. The offline crawler makes no HTTP requests. Avoid committing your own private data, credentials, or generated files.

## License

The code and documentation are available under the [MIT License](LICENSE).
