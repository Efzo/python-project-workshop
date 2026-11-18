# Project 2 — Price quote API

**Build** Accept validated input from query strings, paths, and JSON request bodies.

```sh
python -m uvicorn main:app --app-dir project_2 --reload
```

```sh
curl 'http://127.0.0.1:8000/products?max_cents=200'
curl http://127.0.0.1:8000/shipping/3
curl -i http://127.0.0.1:8000/quotes -H 'Content-Type: application/json' \
  -d '{"unit_cents":450,"quantity":3,"label":"Notebook"}'
```

Expect only the pen on the first call, shipping of 400 cents on the second, and a quote total of 1350 cents on the third. Change the quantity to 0 and expect status 422.

## Follow the input

- In [main.py](main.py), `max_cents` comes from the query string. `quantity` on the shipping route comes from the path placeholder. These parts of a URL arrive as text, and FastAPI parses them into integers.
- `QuoteRequest` is a Pydantic model, so it describes the JSON body. Its integer fields use strict validation. JSON `"3"` fails for that body field, while JSON `3` passes.
- `Field` describes bounds. `StringConstraints` handles whitespace and length. The API rejects extra body fields because the input model says `extra="forbid"`.
- `response_model` describes the output contract. Compare the request and response schemas in `/docs`.

## Your turn

- Add `tax_percent` defaulting to zero and limited to 0–25. Define how to round fractions of a cent. At 10% on a 1350-cent quote, expect 1485 cents.
- Add `GET /products/{name}`. Return 404 for an unknown product and verify that the existing query route remains usable.
- Try a blank label, an unexpected field, and a malformed JSON body. Find where the error response identifies the problem.

[Next — Notes API](../project_3/README.md)
