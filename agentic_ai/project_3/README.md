# Project 3 — Study planning loop

**Build** Give a study assistant multiple turns so one tool result can inform the next decision.

```sh
python3 project_3/agent.py "Build a plan to learn loops"
python3 project_3/agent.py "Build a plan to learn loops" --max-turns 2
```

The first run prints a `read_topic` observation, an `estimate_minutes` observation and a 24-minute plan. The second exhausts the budget of two model decisions, since a third decision is needed to return the final answer.

## Follow the loop

1. In [agent.py](agent.py), the decision is an `Action` or a `Final`. Both variants have explicit fields so the application has a clear dispatch rule.
2. On the first turn, the fixture requests the loops topic. The application executes the allowed action and keeps its result in `observations`.
3. On the second turn, the fixture reads `pages` from the observation to form the estimate action. On the third turn it uses the estimate to answer.
4. `max_turns` includes every decision. Progress messages make the tool sequence visible. A question outside the fixture's topics can end before any tool call.

## Your turn

- Add a second topic with four pages and verify that its plan uses 12 minutes.
- Write a fixture that keeps asking for `read_topic`. Confirm the turn limit stops it.
- Move the progress callback out of the loop implementation. From a test, record tool names in a list and check their order.

[Next — Local retrieval](../project_4/README.md)
