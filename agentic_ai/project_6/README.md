# Project 6 — Study coach capstone

**Build** Combine retrieval, tool progress, generated answers, local run history, explicit export and evaluations.

From `agentic_ai`, change into the lesson folder. The following sequence runs offline.

```sh
cd project_6
python3 -m study_agent --db ../output/runs.db ask "Help me study loops and functions"
python3 -m study_agent --db ../output/runs.db history
python3 -m study_agent --db ../output/runs.db export 1 ../output/answer.txt
python3 -m unittest discover -v
```

Expect tool progress for `search_notes` and two `read_note` calls. The answer lists the two passages, and the history records the run. Use the ID displayed by `ask` when exporting. Choose a fresh destination for each export.

## Trace one run

1. [study_agent/knowledge.py](study_agent/knowledge.py) declares the small built-in knowledge base and validates read-only tool arguments.
2. [study_agent/providers.py](study_agent/providers.py) defines both the offline workflow and the hosted adapter. The offline workflow runs a fixed search-and-read sequence. The hosted model uses structured function calls to decide which notes to inspect.
3. The application validates each call and attaches its result to the same `call_id`. The next request includes the transcript. The adapter has a bounded turn count, a request timeout, and an output-token limit. Tool progress is printed to standard error. Press Ctrl+C to stop the CLI.
4. [study_agent/__main__.py](study_agent/__main__.py) saves completed questions and answers to the local database. `history` is an archive of independent runs. Each `ask` starts a new model transcript. `export` writes the stored result to a new file only when invoked explicitly.
5. [test_agent.py](test_agent.py) checks evidence and the no-evidence result, supplies fixture responses for the hosted tool protocol, and verifies that history and export work across Python processes. The list of notes read records actual tool use. Review generated claims against those notes when evaluating grounding.

## Try the live provider

From `project_6`, create a virtual environment in the track folder and install the optional client. Consult the official model list and choose a model available to your API project that supports function calling. No hosted default is chosen because cost, latency, and available models vary by account and task. [Official OpenAI model catalog](https://developers.openai.com/api/docs/models)

```sh
python3 -m venv ../.venv
source ../.venv/bin/activate
python -m pip install -r ../requirements-live.txt
export OPENAI_MODEL='replace-with-your-model-id'
printf 'OpenAI API key: '
read -rs OPENAI_API_KEY
printf '\n'
export OPENAI_API_KEY
python -m study_agent --db ../output/runs.db ask "Give me one practice task for SQLite" --provider openai
unset OPENAI_API_KEY
```

The live call sends your question and any retrieved note text to OpenAI and can incur charges. Use the lesson's sample questions for these runs. Compare one model's tool trace, answer quality and response time on the same prompts. [Official OpenAI function-calling guide](https://developers.openai.com/api/docs/guides/function-calling)

## Your turn

1. Add another topic and a matching unit test. Ask a question with no matching topic and check the missing-evidence behavior in both modes.
2. Expand the fixture evals to cover an unknown tool, malformed arguments and a response that keeps calling tools past the turn limit.
3. Add a `show ID` command and verify that it reads a stored run without invoking a provider.
4. Design a longer-running version with a run ID, progress events and a stop control. Use the FastAPI track's app factory to test routes in isolation. Keep tool permissions and output writes explicit in the server.

[Back to the Agentic AI roadmap](../README.md)
