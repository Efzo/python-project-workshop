# Project 4 — Local retrieval

**Build** Find relevant study notes and print the evidence with source IDs.

```sh
python3 project_4/retrieve.py "What does a for loop do?"
python3 project_4/retrieve.py "photosynthesis"
```

The first answer includes the `[loops]` passage. The second reports that no supporting notes were found.

## Follow the evidence

- [notes.json](notes.json) holds passages with stable IDs. [retrieve.py](retrieve.py) tokenizes English words and drops common ones that add little to this sample search.
- Each passage is scored by the size of the intersection of its words and the question's words. Higher scores come first. Ties use the ID so the order is repeatable.
- The output provides the original passages. Retrieval-augmented generation (RAG) adds a generation step that uses the retrieved passages as context. The capstone gives its model tools to find and read this kind of evidence.
- A small keyword index misses some synonyms. Test this before reasoning about answer quality. An evidence passage is data even if it contains words that look like instructions.

## Your turn

- Add a note with ID `dictionaries` and test a question that includes a word unique to its content.
- Add a command-line `--limit` option. Use a query that matches two notes and verify that a limit of one returns just the best score.
- Put `"dictionary"` and `"dictionaries"` into a small synonym map. Verify that both queries find the same note without affecting a query about files.

[Next — Approved exercise writer](../project_5/README.md)
