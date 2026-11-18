# Agentic AI with Python

Start with [Project 1 — Structured request classifier](project_1/README.md). Run commands from this `agentic_ai` folder unless the lesson says to change directories. Use Python 3.11 or later. The core projects use local fixtures so you can make repeatable runs. Project 6 adds an optional hosted model.

| Project | Build | Practice |
| --- | --- | --- |
| [1](project_1/README.md) | Request classifier | Prompts, structured output, parsing and validation |
| [2](project_2/README.md) | Tool dispatcher | Tool names, arguments, allowlists and error handling |
| [3](project_3/README.md) | Study planning loop | Decisions, tool results, progress and termination |
| [4](project_4/README.md) | Local retrieval | Search, ranking, source IDs and missing evidence |
| [5](project_5/README.md) | Approved exercise writer | Human review, file effects and deterministic evals |
| [6](project_6/README.md) | Study coach | Adaptive tool calling, a provider adapter, traces, persisted history and export |

A workflow follows application-defined steps. In an agent loop, a model can choose the next tool based on the request and prior tool results. Projects 1–5 isolate the components using ordinary Python. Project 6 shows a simple offline workflow and a hosted model choosing tools at runtime.

[Back to the workspace roadmap](../README.md)
