# Project 5 — Reading log

**Goal** Store reading sessions in SQLite and group the sessions by book.

From the `python_fundamentals` folder, run these commands. They create or update `reading.db`. Use a fresh database for the sample results, or pass `--db practice.db` before each command.

```sh
python3 project_5/reading_log.py add "The Hobbit" 20
python3 project_5/reading_log.py add "The Hobbit" 15
python3 project_5/reading_log.py add "Dune" 25
python3 project_5/reading_log.py report
```

Expect `The Hobbit: 35 pages across 2 session(s)` first and `Dune: 25 pages across 1 session(s)` second.

## Follow a row

1. [reading_log.py](reading_log.py) creates a table with a unique integer ID per reading session. `NOT NULL` and `CHECK (pages > 0)` store rules at the database level.
2. `INSERT` uses `?` placeholders for values. SQLite binds the title and page count from a tuple. Try a title containing an apostrophe.
3. The connection context commits an open transaction on success and rolls it back on an exception. `closing(...)` closes the connection afterward.
4. `GROUP BY book` creates one group per stored title. `COUNT(*)` counts sessions and `SUM(pages)` totals pages. The `for` loop unpacks each returned row.
5. `ORDER BY` sorts by pages descending and uses the book title to break ties.

## Your turn

- Add a `history` command that lists individual sessions ordered by ID. Check that two sessions for one book appear on separate lines.
- Add a `--min-pages` option to `report` and use `HAVING SUM(pages) >= ?` to filter the groups. With a minimum of 30, the example should only show `The Hobbit`.
- Add a `book` command that accepts an exact title and uses `WHERE book = ?` to show only sessions for that title.

Next up is [Project 6 — Weather client](../project_6/README.md).
