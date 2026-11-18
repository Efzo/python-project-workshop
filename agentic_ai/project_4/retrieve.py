import argparse
import json
from pathlib import Path
import re


STOP_WORDS = {"a", "an", "the", "is", "how", "what", "i", "to", "for", "when", "about"}


def terms(text):
    return set(re.findall(r"[a-z]+", text.casefold())) - STOP_WORDS


def retrieve(question, notes, limit=2):
    query_words = terms(question)
    scored = []
    for note in notes:
        score = len(query_words & terms(note["id"] + " " + note["text"]))
        if score:
            scored.append((score, note))
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [note for _, note in scored[:limit]]


def main():
    parser = argparse.ArgumentParser(description="Answer questions with cited local notes.")
    parser.add_argument("question")
    args = parser.parse_args()
    notes_path = Path(__file__).with_name("notes.json")
    notes = json.loads(notes_path.read_text(encoding="utf-8"))
    evidence = retrieve(args.question, notes)
    if not evidence:
        print("No supporting notes found.")
        return
    for note in evidence:
        print(f"[{note['id']}] {note['text']}")


if __name__ == "__main__":
    main()
