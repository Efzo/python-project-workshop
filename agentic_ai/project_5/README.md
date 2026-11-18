# Project 5 — Approved exercise writer

**Build** Preview an exercise, require a separate approval to write it, and evaluate the behavior.

```sh
python3 project_5/draft.py loops --output-dir output/drafts
python3 project_5/draft.py loops --output-dir output/drafts --approve
python3 -m unittest discover -s project_5 -v
```

The first command shows a preview. On a fresh path the second writes `output/drafts/exercise.txt`. Run it again and it refuses to replace that file.

## Follow the approval

1. [draft.py](draft.py) proposes content before the write decision. The user's CLI flag controls approval, so proposed content has no authority to save itself.
2. Preview exits before any directory or file is created. An approved run opens the file with mode `"x"`, which reserves a new filename and protects any existing draft.
3. [test_draft.py](test_draft.py) evaluates several outcomes with isolated temporary folders. The preview test checks content relevance and the filesystem. The approval test checks creation and overwrite behavior. A single output check would miss unwanted writes.
4. These checks are deterministic. For a real model, evaluate multiple representative prompts and decide which qualities need human review, such as whether a proposed exercise is clear and appropriate.

## Your turn

- Add a second known exercise. Extend the tests to check that each preview includes relevant content.
- Add `--name` with a restricted filename format. Confirm that an invalid filename leaves the output untouched.
- Sketch an approval screen that shows the final text and destination. Decide how to keep the exact approved content tied to the action if the model can change its draft.

[Next — Study coach capstone](../project_6/README.md)
