# Project 1 — Folder inventory

**Build** A terminal command that counts files by extension.

```sh
python3 project_1/inventory.py project_1/sample
```

Expect `.csv: 1`, `.txt: 1`, and `Total: 2`. Run the same command with a missing folder and observe the error.

## How it works

1. In [inventory.py](inventory.py), `argparse` accepts a folder and converts it to a `Path`. After parsing, `args.folder` is a Python object you can inspect with filesystem methods.
2. `iterdir()` gives you the immediate children of the folder. `is_file()` filters out folders. The symlink check keeps the count focused on regular files in the sample folder.
3. `path.suffix` gives you the final extension. `.casefold()` puts `.TXT` and `.txt` in the same group. A `Counter` starts each new key at zero.
4. `sorted(counts.items())` gives predictable output. `parser.exit(1, ...)` communicates a failure to a shell or scheduler. Try `echo $?` immediately after a successful or failed command.

## Your turn

- Add a file named `LICENSE` to your copy of the sample. Check that it appears as `(no extension): 1`.
- Add `--recursive` so a nested CSV counts only when the flag is present. Look up `Path.rglob` in Python's built-in help with `python3 -m pydoc pathlib.Path.rglob`.

[Next — File organizer](../project_2/README.md)
