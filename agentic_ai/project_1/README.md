# Project 1 — Structured request classifier

**Build** Turn a natural-language request into a Python object with a category and reason.

```sh
python3 project_1/classify.py "Help me study loops"
python3 project_1/classify.py "Plan my week"
```

Expect `study` and `planning` at the start of the respective lines.

## Follow one response

1. [classify.py](classify.py) passes instructions and user text as separate arguments. Instructions define the task and output shape. The request is the input being classified.
2. `FixtureModel.complete()` uses simple word rules and returns JSON text. This simulates a provider response and makes experiments repeatable.
3. `json.loads()` parses the response. The program then checks that the object has exactly two keys, that the category is supported, and that the reason contains text.
4. `Classification` stores the validated result. Other code can read `result.category` without parsing a text message again.

## Your turn

- Run `"schedule time to study"` and explain which category wins based on the order of the rules.
- Add a `debugging` category for `fix`, then test `"Please fix this"` and one unrelated request.
- Write a fake provider that returns plain text or an unsupported category. Call `classify` with your provider and check that both results raise a validation error.

[Next — Tool dispatcher](../project_2/README.md)
