from contextlib import closing, contextmanager
from dataclasses import dataclass
from datetime import date
import sqlite3


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    due: date | None
    done: bool


@contextmanager
def open_board(path):
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    due TEXT,
                    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
                )
                """
            )
            yield connection


def add_task(database, title, due):
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Enter a task title.")
    row = database.execute(
        "INSERT INTO tasks (title, due) VALUES (?, ?)",
        (clean_title, due.isoformat() if due else None),
    )
    return row.lastrowid


def list_tasks(database, include_done):
    rows = database.execute(
        """
        SELECT id, title, due, done FROM tasks
        WHERE done = 0 OR ? = 1
        ORDER BY due IS NULL, due, id
        """,
        (include_done,),
    )
    return [
        Task(task_id, title, date.fromisoformat(due) if due else None, bool(done))
        for task_id, title, due, done in rows
    ]


def complete_task(database, task_id):
    result = database.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    if result.rowcount == 0:
        raise ValueError(f"No task with ID {task_id}.")
