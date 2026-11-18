# Project 3 — Notes CLI

**Goal** Save notes between runs and find them through a command-line interface.

From the `python_fundamentals` folder, run the commands below. They use `notes.json` in your current directory.

```sh
python3 project_3/notes.py add "Practice Python every day"
python3 project_3/notes.py add "Buy a notebook"
python3 project_3/notes.py list
python3 project_3/notes.py search python
```

On a fresh file, `list` shows notes 1 and 2. Search prints `1. Practice Python every day`. Run with `--help` for available options. To use a second file, pass `--file practice-notes.json` before the command.

## Follow the data

- In [notes.py](notes.py), `argparse` converts command-line tokens into named values such as `args.query`. Quotes in the shell keep a multiword note together.
- `Path` represents the file location. The `with` block closes the file when its body ends, including when an exception occurs.
- `json.load` decodes stored text into Python data. The loader returns an empty list if the file is missing. A malformed file raises an error so an `add` command preserves the original file.
- `json.dump` writes Python values as JSON. The program writes a temporary file in the same folder before replacing the destination. Use one writer at a time. Concurrent `add` commands can load the same original list and overwrite each other's changes.
- `enumerate(notes, start=1)` pairs each note with a display number before filtering. `.casefold()` enables case-insensitive substring search.

## Your turn

1. Add a `count` command. Check that a missing file gives zero and a file with two notes gives two.
2. Add `delete NUMBER`. Use `type=int` when defining the argument and convert the displayed number to a list index by subtracting one. Test deleting note 2, then test 0 and an out-of-range number.
3. Create a separate file containing only `{` and try to add a note with `--file` pointed at it. Check that the command exits with an error and the file still contains `{`.

Next up is [Project 4 — Lending library](../project_4/README.md).
