# Project 2 — Tool dispatcher

**Build** Translate a structured tool request into a specific Python function call.

```sh
python3 project_2/tools.py lookup_topic '{"name":"loops"}'
python3 project_2/tools.py estimate_time '{"pages":4}'
python3 project_2/tools.py estimate_time '{"pages":true}'
```

The first result contains `for` and `while`. The second gives 12 minutes. The third exits with an input error.

## Follow a tool call

- [tools.py](tools.py) defines the available functions and a dictionary that maps public names to their implementation.
- A tool request contains a tool name and JSON arguments. The terminal commands play the role that a model will play later.
- `dispatch` checks the name and decodes an argument object. Each function then checks its own fields and bounds. Python treats `bool` as a subclass of `int`, so the page check uses `type(value) is int`.
- A result is an ordinary dictionary. In a live loop the application can attach that result to the tool call so the model can use it.

## Your turn

- Add a `quiz_question` function that takes a known topic and returns one question. Check an allowed topic, a missing argument and an unknown topic.
- Try a missing tool name, malformed JSON and an extra field. Confirm each is rejected.
- Write a short tool description and argument schema for `estimate_time`. Include the accepted type, range and one valid example.

[Next — Study planning loop](../project_3/README.md)
