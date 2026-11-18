# Learn Python by building nine projects

Start with [Project 1 — Quiz game](project_1/README.md). The projects build on one another and use only Python's standard library. Use Python 3.11 or later. From the workspace root, check your setup and run your first program.

```sh
cd python_fundamentals
python3 --version
python3 project_1/01_first_program.py
```

| Project | What you build | What you practice |
| --- | --- | --- |
| [1. Quiz game](project_1/README.md) | A quiz that scores answers and lets you replay | Variables, input, strings, numbers, conditions, lists and loops |
| [2. Expense tracker](project_2/README.md) | A terminal app that groups expenses by category | Functions, dictionaries, tuples, mutability and decimal arithmetic |
| [3. Notes CLI](project_3/README.md) | A program that saves and searches notes between runs | Imports, CLI arguments, paths, JSON, exceptions and resource handling |
| [4. Lending library](project_4/README.md) | A library that tracks books and loans | Classes, dataclasses, type hints, sets, composition and unit tests |
| [5. Reading log](project_5/README.md) | A persistent log with a summary by book | SQL, SQLite, constraints, transactions and aggregation |
| [6. Weather client](project_6/README.md) | A client that reads JSON from a local HTTP server | HTTP, JSON validation, timeouts and local integration checks |
| [7. Sales report](project_7/README.md) | A CSV pipeline that produces a category report | Iterators, generators, comprehensions, decorators and sorting |
| [8. Concurrent order prep](project_8/README.md) | A simulation that prepares orders concurrently | Coroutines, task groups, semaphores, cancellation and timing |
| [9. Task board](project_9/README.md) | A packaged CLI with persistence, due dates and CSV export | Packaging, virtual environments, datetimes, application boundaries and end-to-end tests |

## How to study

1. Run the program with the lesson's sample input and compare your result with the expected output.
2. Read the explanation with the source open. Predict what a line will do before running it.
3. Solve the exercises in your own copy. Use the acceptance checks to decide when each change works.
4. Rebuild the main feature from a blank file. Use the working example when you get stuck.
5. Move on when you can explain why the program behaves as it does and add a feature independently.

You can inspect a variable with `print(repr(value))` or pause execution by adding `breakpoint()`. At the debugger prompt, try `p value`, `n` for the next line and `c` to continue. When you get an error, start with the last line of the traceback, then look for the last frame pointing at your own file.
