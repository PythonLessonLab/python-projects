# Project: Analyze Application Logs

Companion lesson: https://pythonlessonlab.com/lessons/project-log-analyzer/

Parse lines formatted as `timestamp | level | message`, count each level, keep ERROR messages in order, and report malformed nonblank rows. The first two pipe characters delimit fields; later pipes stay inside the message. The parser checks the field shape but does not validate timestamp syntax or handle multiline stack traces.

Run a UTF-8 sample log:

```powershell
py -3 log_analyzer.py sample.log
```

Run the tests from this directory:

```powershell
py -3 -m unittest -v
```

The website version uses a log string in memory so it also runs in the browser console. This local extension accepts a file path; it does not upload the file.
