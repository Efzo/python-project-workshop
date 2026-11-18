# Project 6 — Daily sales pipeline

**Build** Take a daily CSV from input validation to a logged, repeatable report.

```sh
python3 project_6/daily_sales.py project_6/sales.csv --day 2026-11-17 --output-dir output/reports
cat output/reports/2026-11-17.json
```

The report contains the date, 2 sales, and 2000 total cents. Rerun the command. The contents should be identical, and the database should still hold one row for that day.

## How it works

- [daily_sales.py](daily_sales.py) separates validation, recording and publishing. All input rows pass validation before the job opens the database.
- The report date is a primary key. SQLite's `ON CONFLICT(day) DO UPDATE` updates that day's totals on rerun. The transaction commits before publishing the JSON file.
- The report is written to a temporary file and replaced in one filesystem operation. If publishing fails after the database commits, rerun with the same input and day to regenerate the report. Schedule one instance at a time for each output directory.
- The log records the destination and row count. An invalid input exits with code 1, which a scheduler can surface.

## Schedule it yourself

First run the command manually with your own absolute paths. For a POSIX machine using cron, the example entry runs at 7:00 a.m. in the scheduler's timezone. Replace the executable and all paths. Create the log directory before registering the job. Omitting `--day` uses the Python process's current local date.

```cron
0 7 * * * /path/to/python3 /path/to/python_automation/project_6/daily_sales.py /path/to/current-sales.csv --output-dir /path/to/reports >> /path/to/logs/daily-sales.log 2>&1
```

Use `crontab -e` to add or remove the entry and `crontab -l` to check it. Check the log after the scheduled time and compare it with the report for that day.

## Your turn

1. Add a `--dry-run` that validates and prints a preview without creating the output directory. Verify both the filesystem and exit code.
2. Create a second day's file and compare the two database rows using a short script with `sqlite3`.
3. Change a row in a copy of the first day's input and rerun for the first day. Verify that the database and JSON agree and the second day is unchanged.
4. Rebuild the pipeline for another recurring task, such as attendance reporting. Test the first run, a correction, a malformed input, and a retry.

[Back to the automation roadmap](../README.md)
