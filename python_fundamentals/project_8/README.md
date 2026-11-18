# Project 8 — Concurrent order prep

**Goal** Simulate preparing orders with a limited number of stations and observe how waiting can overlap.

From the `python_fundamentals` folder, run the following.

```sh
python3 project_8/order_prep.py --stations 1
python3 project_8/order_prep.py --stations 2
python3 project_8/order_prep.py --stations 3
```

Expect roughly 0.90, 0.50, and 0.40 seconds respectively. Timings vary by machine. With two stations, B normally finishes first, freeing a station for C.

## Follow an order

- In [order_prep.py](order_prep.py), calling an `async def` function creates a coroutine. `asyncio.run()` starts the event loop and drives the top-level coroutine to completion.
- `TaskGroup.create_task()` schedules work. Exiting the task group waits for its tasks. If one task fails with an ordinary exception, the group cancels the remaining tasks and reports the failure.
- `async with stations` borrows a semaphore permit and returns it at the end of the block. With two permits, at most two orders can be preparing at once.
- `await asyncio.sleep(...)` lets the event loop run other coroutines while this order waits. This example models waiting for resources. CPU-intensive work inside a coroutine can block the event loop.
- `task.result()` is called after the group finishes. The summary preserves submission order, while the progress messages report completion order. If a coroutine catches `CancelledError` for cleanup, it re-raises it afterward.

## Your turn

1. Add order D with a duration of 0.1 seconds. Predict the total for one and four stations, then measure it.
2. Temporarily raise a `RuntimeError` for order B immediately after its sleep. Run with three stations and watch what happens to A and C.
3. Add `--deadline SECONDS` and wrap the task group in `asyncio.timeout()`. Catch `TimeoutError` at the CLI so a deadline produces a clear message. Try 0.25 seconds with three stations and check that B finishes before the deadline and the remaining work is cancelled.

Next up is [Project 9 — Task board](../project_9/README.md).
