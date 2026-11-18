from collections.abc import Iterator
from contextlib import asynccontextmanager, closing
import sqlite3

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(app.state.db_path)) as db, db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
            )
            """
        )
    yield


def get_db(request: Request) -> Iterator[sqlite3.Connection]:
    with closing(sqlite3.connect(request.app.state.db_path, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db
