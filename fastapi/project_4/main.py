from collections.abc import Iterator
from contextlib import asynccontextmanager, closing
from pathlib import Path
import sqlite3
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, StringConstraints


class BookInput(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class Book(BookInput):
    id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(app.state.db_path)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT UNIQUE NOT NULL)")
    yield


def get_db(request: Request) -> Iterator[sqlite3.Connection]:
    # A request owns this connection. FastAPI can dispatch sync work on different threads.
    with closing(sqlite3.connect(request.app.state.db_path, check_same_thread=False)) as db:
        yield db


Database = Annotated[sqlite3.Connection, Depends(get_db)]


def create_app(db_path: Path):
    app = FastAPI(title="Reading List API", lifespan=lifespan)
    app.state.db_path = db_path

    @app.post("/books", response_model=Book, status_code=201)
    def add_book(book: BookInput, db: Database):
        try:
            with db:
                row = db.execute("INSERT INTO books (title) VALUES (?)", (book.title,))
            return Book(id=row.lastrowid, title=book.title)
        except sqlite3.IntegrityError as error:
            raise HTTPException(status_code=409, detail="Title already exists") from error

    @app.get("/books", response_model=list[Book])
    def list_books(db: Database):
        return [Book(id=book_id, title=title) for book_id, title in db.execute(
            "SELECT id, title FROM books ORDER BY id"
        )]

    return app


app = create_app(Path(__file__).parent / "data" / "books.db")
