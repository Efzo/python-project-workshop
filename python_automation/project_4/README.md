# Project 4 — Stock feed checker

**Build** Fetch a stock feed, retry a temporary failure and identify sold-out products.

Run the test server in one terminal and the client in another. Start both from `python_automation`.

```sh
python3 project_4/fixture_server.py
```

```sh
python3 project_4/check_stock.py
python3 project_4/check_stock.py http://127.0.0.1:8000/missing.json
```

The first request to the stock feed returns a deliberate 503, then the retry succeeds. Expect a retry message followed by `Out of stock: B20`. The second command should report a 404 without retrying. Stop the fixture server with Ctrl+C.

## How it works

- [fixture_server.py](fixture_server.py) keeps a flag for whether it has simulated the first failure. Restart it to reset the scenario.
- [check_stock.py](check_stock.py) requests JSON with a timeout. Temporary HTTP responses and selected transport failures can be retried. A bad path or invalid data needs a different fix.
- `2 ** attempt` introduces exponential backoff. Each retry waits longer, and the finite attempt count bounds the job.
- `out_of_stock` checks the JSON shape before returning IDs. A valid response body can still break the API contract.

## Your turn

- Change the fixture to fail twice before sending stock. Expect waits of one and two seconds.
- Change a fixture stock count to `"0"`. Check that validation fails. Restore the integer and rerun.
- Inject a function in place of `pause` to record retry delays without sleeping. For a fixture that fails twice, expect `[1, 2]`.

[Next — ZIP backup](../project_5/README.md)
