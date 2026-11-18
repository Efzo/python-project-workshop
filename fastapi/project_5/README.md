# Project 5 — Protected metrics API

**Build** Authorize access with a bearer token, then fetch two simulated metrics concurrently.

```sh
METRICS_TOKEN=local-training-token python -m uvicorn main:app --app-dir project_5 --reload
```

```sh
curl -i http://127.0.0.1:8000/metrics
curl -i http://127.0.0.1:8000/metrics -H 'Authorization: Bearer local-training-token'
python -m unittest discover -s project_5 -v
```

Expect 401 on the first request, then 200 with `{"queued":3,"ready":7}`. Run the tests from the activated environment. The token above is a disposable local value for the lesson.

## Follow the request

- [main.py](main.py) uses `HTTPBearer` to parse the authorization header. The dependency reads settings from the environment, verifies the supplied token, and ends unauthorized requests with 401.
- `compare_digest` compares token bytes without early exit based on their contents. This example uses one shared token for a local service. User login, roles, and revocation need an identity system.
- The handler uses `asyncio.gather` to overlap two simulated I/O operations. `asyncio.timeout` bounds the wait. Replace the simulated calls only with async I/O or move blocking calls out of the event loop.
- [test_main.py](test_main.py) overrides the settings dependency. Tests control configuration directly and use `TestClient` without opening a server port.

## Your turn

- Add another metric and verify its response field.
- Change one simulated wait to two seconds. Confirm the handler returns 504 around the one-second deadline.
- Add a test for a wrong token, then another for empty settings. Expect 401 and 503 respectively.

[Next — Study task API](../project_6/README.md) · [Official FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
