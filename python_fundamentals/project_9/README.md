# Project 9 — Task board capstone

**Goal** Build a Python package with a command-line interface, persistent tasks, due dates, CSV export, and end-to-end tests.

From the `python_fundamentals` folder, run the following. Use a fresh database and export path for the sample output.

```sh
cd project_9
python3 -m taskboard --db tasks.db add "Finish the Python capstone" --due 2026-12-15
python3 -m taskboard --db tasks.db list
python3 -m taskboard --db tasks.db done 1
python3 -m taskboard --db tasks.db list --all
python3 -m taskboard --db tasks.db export tasks.csv
python3 -m unittest discover -v
```

On a fresh database, the first list shows `1. [open] Finish the Python capstone (due 2026-12-15)`. After completion, `list --all` shows the same task with `[done]`. The export includes a header and one task row.

## Follow a command through the package

1. [taskboard/__main__.py](taskboard/__main__.py) runs when you use `python3 -m taskboard`. It calls the CLI function through a relative import.
2. [taskboard/cli.py](taskboard/cli.py) parses arguments, validates dates and formats output. `date.fromisoformat` rejects impossible dates such as February 30. Comparing the ISO output to the input enforces the written form `YYYY-MM-DD`.
3. [taskboard/storage.py](taskboard/storage.py) owns SQL and converts rows to `Task` objects. It stores due dates as ISO text so they sort by date. Tasks without a due date appear last.
4. `@contextmanager` turns a generator with one `yield` into a context manager. The CLI borrows the database connection inside a `with` block, and the surrounding storage contexts handle the transaction and close the connection.
5. CSV export uses mode `"x"`, which creates a new file and refuses to overwrite an existing one. The CSV writer quotes fields containing commas.
6. [test_taskboard.py](test_taskboard.py) uses temporary files and launches the real CLI in a subprocess. Each command starts a fresh Python process, so the lifecycle test verifies that state survives across runs.

## Install it into a virtual environment

From `project_9`, create the environment and install your package. The build may download packaging tools if they are unavailable locally.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
taskboard --help
deactivate
```

[pyproject.toml](pyproject.toml) declares the build backend and maps the `taskboard` shell command to `taskboard.cli:main`. The editable install lets you change the source and rerun the command in the environment.

## Your turn

1. Add `reopen ID`. Verify that a completed task reappears in the default list and an unknown ID exits with an error.
2. Add `list --overdue`. Compare due dates with `date.today()`. Decide how to test with a fixed date so the test passes consistently. Include a task due today and a task with no due date in your checks.
3. Add a test for two tasks with deadlines and one with no deadline. Confirm they are listed in chronological order, with the undated task last.
4. Rebuild the project in a new folder using a different domain, such as a job application tracker. Write down your commands first, decide what each table stores and cover one complete workflow with a subprocess test.
