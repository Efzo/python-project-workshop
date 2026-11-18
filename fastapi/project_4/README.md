# Project 4 — Reading list API

**Build** Persist a reading list across server restarts and reject duplicate titles.

```sh
python -m uvicorn main:app --app-dir project_4 --reload
```

```sh
curl -i http://127.0.0.1:8000/books -H 'Content-Type: application/json' -d '{"title":"Dune"}'
curl -i http://127.0.0.1:8000/books -H 'Content-Type: application/json' -d '{"title":"Dune"}'
curl -i http://127.0.0.1:8000/books
```

On a fresh database, expect 201, then 409, then a list of one book. Restart the server and repeat the GET. The book remains in `project_4/data/books.db`.

## Follow the database

1. [main.py](main.py) uses an async lifespan context manager. The code before `yield` runs at startup and creates the table.
2. `Depends(get_db)` tells FastAPI to resolve the connection for each request that needs it. The dependency yields the connection, then closes it when the request dependency is cleaned up.
3. SQLite work happens in regular `def` routes. Each request has its own connection, and `check_same_thread=False` lets FastAPI's synchronous dependency and handler use it across their worker threads.
4. The write is inside a database transaction. SQLite enforces the unique-title constraint. An integrity error becomes a 409 response for a resource conflict.

## Your turn

- Add `GET /books/{book_id}` using a bound parameter. Verify both a known ID and a missing ID.
- Add a list filter and check that a search containing an apostrophe is passed as a value.
- Build a test with a fresh temporary path and `with TestClient(create_app(path)) as client`. Run the same test twice and confirm the real database does not gain rows.

[Next — Protected metrics API](../project_5/README.md) · [Official lifespan guide](https://fastapi.tiangolo.com/advanced/events/)
