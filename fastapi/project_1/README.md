# Project 1 — First API

**Build** An HTTP server with a home route and a health check.

After completing the [track setup](../README.md), start the server from `fastapi`.

```sh
python -m uvicorn main:app --app-dir project_1 --reload
```

In a second terminal, run the client commands.

```sh
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
```

Expect status 200 with `{"message":"Hello, FastAPI!"}` and `{"status":"ok"}`. In your browser, visit `http://127.0.0.1:8000/docs` and try the same requests there.

## Follow a request

1. Uvicorn imports `app` from [main.py](main.py). `--app-dir` tells it where to find the module, and `--reload` restarts the development process after code changes.
2. `@app.get("/health")` registers a function for the GET method and the `/health` path. FastAPI calls that function when a matching request arrives.
3. The function returns a Python dictionary. FastAPI serializes it to JSON and sends it inside an HTTP response with a status code and headers.
4. FastAPI describes the API in OpenAPI. Visit `/openapi.json` and find both paths. The interactive docs use that machine-readable description.

## Your turn

- Add `GET /about` with a name and a version. Check both the JSON output and the operation in `/docs`.
- Request `/missing` and try `curl -i -X POST http://127.0.0.1:8000/health`. Predict which response means an unknown path and which means an unsupported method, then check 404 and 405.

[Next — Price quote API](../project_2/README.md) · [Official FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
