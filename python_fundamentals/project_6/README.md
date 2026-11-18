# Project 6 — Weather client

**Goal** Fetch and validate JSON over HTTP. The example serves a static weather fixture on your computer.

Open two terminals in the `python_fundamentals` folder. In the first, start Python's static file server.

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory project_6/fixtures
```

In the second, run the client.

```sh
python3 project_6/weather.py
python3 project_6/weather.py http://127.0.0.1:8000/missing.json
```

Expect `Austin: 24 °C, Partly cloudy` for the first command and an HTTP 404 error for the second. If port 8000 is busy, change it in the server command and pass the matching URL to the client. Stop the server with Ctrl+C when finished.

## Follow the request

1. [weather.py](weather.py) creates a request with an `Accept` header describing the format the client wants. With no request body or explicit method, it sends a GET request.
2. `urlopen` opens the response with a timeout for blocking operations. The `with` block closes it when decoding finishes.
3. `json.load` turns the response into Python objects. A response can be valid JSON and still have the wrong shape. The checks require a dictionary, text fields, and a plausible Celsius value.
4. The CLI handles transport, timeout and decoding or validation errors and exits with status 1. An HTTP 404 becomes an `HTTPError`, which is a subclass of `URLError`.

## Your turn

- Display degrees Fahrenheit alongside Celsius. A value of 24 °C should display as 75.2 °F.
- Run the client against a copy of the fixture with `"temperature_c": "24"`. A numeric string should fail validation. Restore a numeric value and check that it works again.
- Add a `--timeout` option and reject values less than or equal to zero. Stop the server and verify that the client gives an error if the service is unavailable.

Next up is [Project 7 — Sales report](../project_7/README.md).
