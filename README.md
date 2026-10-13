# PythonLessonLab projects

Runnable companion code for [PythonLessonLab](https://pythonlessonlab.com/). Each project has a short explanation, a working program, small sample data where needed, and tests you can run locally. The website has the full lesson, an in-browser Python console, a checked exercise, a quiz, and a video walkthrough.

| Project | Learn | Watch | Code |
| --- | --- | --- | --- |
| CSV Expense Tracker | [Project lesson](https://pythonlessonlab.com/lessons/project-csv-expense-tracker/) | [Video](https://youtu.be/A5l-ok68lrI) | [Open folder](projects/csv-expense-tracker/) |
| Contact Book | [Project lesson](https://pythonlessonlab.com/lessons/project-contact-book/) | [Video](https://youtu.be/bBvf1IgZLY8) | [Open folder](projects/contact-book/) |
| Log Analyzer | [Project lesson](https://pythonlessonlab.com/lessons/project-log-analyzer/) | [Video in lesson](https://pythonlessonlab.com/lessons/project-log-analyzer/) | [Open folder](projects/project-log-analyzer/) |
| Flashcard Quiz | [Project lesson](https://pythonlessonlab.com/lessons/project-flashcard-quiz/) | [Video in lesson](https://pythonlessonlab.com/lessons/project-flashcard-quiz/) | [Open folder](projects/project-flashcard-quiz/) |

## Advanced project: Simple Web Crawler

The [Simple Web Crawler tutorial and code](projects/simple-web-crawler/) use a local practice site to teach HTTP requests, HTML parsing, queues, URL normalization, and `robots.txt`. The crawler stays on one origin and limits its requests. Its companion website lesson and video are planned; the repository tutorial is ready to use now.

## Quick start

Install Python 3.10 or newer. The four projects in the table use only the Python standard library; no package installation, API keys, accounts, or network access are required. The commands below assume `python` starts Python 3. On Windows, use `py -3` in place of `python` if `python` points to an older version.

From the repository root:

```sh
python projects/csv-expense-tracker/expense_tracker.py
python projects/contact-book/contact_book.py
python projects/project-flashcard-quiz/flashcard_quiz.py
python -m unittest discover -s projects/csv-expense-tracker -p "test_*.py"
python -m unittest discover -s projects/contact-book -p "test_*.py"
python -m unittest discover -s projects/project-log-analyzer -p "test_*.py"
python -m unittest discover -s projects/project-flashcard-quiz -p "test_*.py"
```

Read each project folder's README for the expected output and suggested changes to try.

The crawler has its own [setup and local practice instructions](projects/simple-web-crawler/README.md). Run its tests from that folder with `python -m unittest discover -s tests -v`.

All names, email addresses, and expense amounts in the first two projects are fictional. Their programs run locally and do not send data anywhere. The crawler starts with a local fixture; its public-site option requires explicit opt-in. Avoid committing your own contact list, financial exports, credentials, or generated files.

## License

The code and documentation in this repository are available under the [MIT License](LICENSE).
