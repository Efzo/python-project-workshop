# Project 6 — Study task API

**Build** A versioned service with persistent tasks, pagination, authentication, request timing, tests, and a container image recipe.

From the `fastapi` folder, start the API using a disposable training token.

```sh
STUDY_API_TOKEN=local-training-token python -m uvicorn study_api.main:app --app-dir project_6
```

```sh
curl -i http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/v1/tasks -H 'Authorization: Bearer local-training-token' \
  -H 'Content-Type: application/json' -d '{"title":"Read about dependencies"}'
curl -i 'http://127.0.0.1:8000/v1/tasks?limit=5&offset=0' \
  -H 'Authorization: Bearer local-training-token'
curl -i -X PATCH http://127.0.0.1:8000/v1/tasks/1 \
  -H 'Authorization: Bearer local-training-token' \
  -H 'Content-Type: application/json' -d '{"done":true}'
python -m unittest discover -s project_6 -v
```

On a fresh database, the first task has ID 1. Expect 201 on creation, 200 for list and patch, and `"done":true` after the patch. On later runs use the ID returned by POST.

## Follow a task through the service

- [study_api/main.py](study_api/main.py) creates the app, adds a timing middleware, exposes health, and mounts the tasks router under `/v1`. Compare a health response's timing header to the corresponding server log.
- [study_api/tasks.py](study_api/tasks.py) defines the router, shared authorization, schemas and route handlers. The list operation orders rows before applying `LIMIT` and `OFFSET` so you can navigate a stable list.
- [study_api/db.py](study_api/db.py) initializes SQLite at startup and supplies a connection to each request. The completion update uses SQLite's `RETURNING` clause, available in SQLite 3.35 and later.
- [test_api.py](test_api.py) launches two app lifespans over the same temporary database, verifying that data survives a restart. It also verifies authorization, validation and missing IDs.

## Package and run in Docker

Run these from the `fastapi` folder on a machine with Docker. The build context is the track folder. A named volume keeps SQLite data across runs. The host port is bound to localhost for practice.

```sh
docker build -f project_6/Dockerfile -t study-api .
docker volume create study-api-data
export STUDY_API_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker run --rm -p 127.0.0.1:8000:8000 -v study-api-data:/data -e STUDY_API_TOKEN study-api
```

Stop any other server on port 8000 first. In a second terminal, check `/health`. For a protected request, use the generated token from the shell that launched the container or use `docker run -d` to make requests from that shell.

For a deployed version, keep TLS and authentication secrets in your hosting setup, decide who can access each task, and design migrations and backups for the storage you choose. A single shared token gives all authorized callers access to the same tasks in this example.

## Your turn

1. Add a delete route and tests for deleting a task, deleting a missing task, and making the request without a token.
2. Add a `done` filter and verify that it composes with pagination.
3. Rebuild the service for a habit tracker. Write down its routes and request models before coding. Test one full lifecycle, one invalid request and one unauthorized request.

[Back to the FastAPI roadmap](../README.md)
