# Project 2 — File organizer

**Build** A command that previews and copies files into folders based on their extensions.

```sh
python3 project_2/organize.py project_2/sample output/organized
python3 project_2/organize.py project_2/sample output/organized --apply
python3 project_2/organize.py project_2/sample output/organized --apply
```

On a fresh destination, expect two `would copy` lines, then two `copied` lines. The last run should show `skip existing`. Compare the source and output files.

## How it works

- [organize.py](organize.py) turns each file's extension into a category and builds a destination using `Path / name`.
- `store_true` gives a Boolean flag. Without `--apply`, the code prints the plan and moves to the next file before calling any write methods.
- The write stages a complete copy in the output folder's filesystem, then creates the final filename with a hard link. If the filename already exists, the existing contents are preserved. The temporary directory cleans up after the attempt. This example needs a filesystem with hard-link support.
- Rerunning the same command finds the same destination paths. That makes retries predictable after a partially completed batch.

## Your turn

- Put a different `notes.txt` in the output category and rerun. Verify that the existing output still contains your version.
- Add an option to include only one extension. With `--only json`, the preview should contain the settings file alone.
- Add a summary count for planned, copied, and skipped files. Check the first run and the rerun.

[Next — Order reporter](../project_3/README.md)
