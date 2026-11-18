# Project 4 — Lending library

**Goal** Model books and loans as objects, then verify their behavior with automated tests.

From the `python_fundamentals` folder, run the demo and tests.

```sh
python3 project_4/library.py
python3 -m unittest discover -s project_4 -v
```

The demo shows only `Pride and Prejudice` while `The Hobbit` is checked out. After the return, it shows both books.

## Follow a loan

- [library.py](library.py) defines a `Book` dataclass. The decorator generates an initializer and equality behavior from the fields. `frozen=True` prevents assigning a different code or title after creation.
- `Library` holds `Book` instances. This is composition. `self` refers to the library instance on which the method is called, so two libraries keep independent state.
- The dictionary looks up books by code. The set tracks unique checked-out codes and supports membership tests with `in`.
- `check_out` enforces the library's rules before it changes anything. The `-> None` annotation documents that callers use the method for its effect on state. Python does not enforce these annotations at runtime.
- In [test_library.py](test_library.py), `setUp` creates fresh state before each test. `assertEqual` checks output, and `assertRaisesRegex` checks an error type and its message.

## Your turn

1. Write a test for checking out an unknown code. It should expect a `ValueError` and leave all registered books available.
2. Add `remove_book(code)` with tests for removing an available book and rejecting one on loan.
3. Add an `author` field to `Book` and a `by_author(name)` method on `Library`. Verify that two books by the same author are returned and an unknown author yields an empty list.

Next up is [Project 5 — Reading log](../project_5/README.md).
