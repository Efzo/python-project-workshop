# Project 3 — Notes API

**Build** Create, read, replace, and delete notes by ID.

```sh
python -m uvicorn main:app --app-dir project_3 --reload
```

```sh
curl -i http://127.0.0.1:8000/notes -H 'Content-Type: application/json' \
  -d '{"title":"Study","body":"Read about HTTP."}'
curl -i http://127.0.0.1:8000/notes/1
curl -i -X PUT http://127.0.0.1:8000/notes/1 -H 'Content-Type: application/json' \
  -d '{"title":"Study more","body":"Practice PUT."}'
curl -i -X DELETE http://127.0.0.1:8000/notes/1
curl -i http://127.0.0.1:8000/notes/1
```

On a fresh server, expect 201, 200, 200, 204 with an empty body, and 404.

## Follow the resource

- In [main.py](main.py), `NoteInput` is user-provided data. `Note` adds the ID the server assigns.
- `create_app()` makes a new dictionary and ID counter for each instance. A lock serializes changes to this process's dictionary. Restarting the server resets its contents, and separate workers each have their own state.
- The GET methods read resources. POST creates a server-assigned resource. PUT replaces the note at a known ID in this API, and DELETE removes it.
- `HTTPException` stops the operation and becomes an HTTP error response. A 204 response has no content.

## Your turn

- Add a `contains` query parameter to the collection route and filter by title. Create two notes and check that the query returns only the matching one.
- Write a small test using `TestClient(create_app())`. Create and delete a note, then check the subsequent GET returns 404.
- Design a PATCH route that changes the title while preserving the body. Compare that behavior with your full PUT replacement.

[Next — Reading list API](../project_4/README.md)
