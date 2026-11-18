# FastAPI

Start with [Project 1 — First API](project_1/README.md). Use Python 3.11 or later and run the setup from this `fastapi` folder. Keep the environment active for the lessons.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Use two terminals when a lesson shows server and client commands. Keep the server running in the first terminal. Run requests from the second. Stop a server with Ctrl+C before starting the next project on the same port.

| Project | Build | Practice |
| --- | --- | --- |
| [1](project_1/README.md) | First API | Routes, JSON, HTTP and OpenAPI |
| [2](project_2/README.md) | Price quote API | Path and query parameters, Pydantic and validation |
| [3](project_3/README.md) | Notes API | CRUD, resource IDs, status codes and app factories |
| [4](project_4/README.md) | Reading list API | SQLite, dependency injection, transactions and lifecycle |
| [5](project_5/README.md) | Protected metrics API | Bearer authentication, async I/O, timeouts and dependency overrides |
| [6](project_6/README.md) | Study task API | Routers, versioning, pagination, logs, tests and container packaging |

The [official FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) is a reference as you work. For Python functions, type annotations, SQLite, and tests, revisit [Python Fundamentals](../python_fundamentals/README.md).
