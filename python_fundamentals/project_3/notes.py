import argparse
import json
from pathlib import Path


def load_notes(path):
    try:
        with path.open(encoding="utf-8") as notes_file:
            notes = json.load(notes_file)
    except FileNotFoundError:
        return []
    if not isinstance(notes, list) or not all(isinstance(note, str) for note in notes):
        raise ValueError("The notes file must contain a list of strings.")
    return notes


def save_notes(path, notes):
    temporary_path = path.with_name(path.name + ".tmp")
    with temporary_path.open("w", encoding="utf-8") as notes_file:
        json.dump(notes, notes_file, indent=2, ensure_ascii=False)
        notes_file.write("\n")
    temporary_path.replace(path)


def main():
    parser = argparse.ArgumentParser(description="Save and search short notes.")
    parser.add_argument("--file", type=Path, default=Path("notes.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    add = commands.add_parser("add")
    add.add_argument("text")
    search = commands.add_parser("search")
    search.add_argument("query")
    args = parser.parse_args()

    try:
        notes = load_notes(args.file)
        if args.command == "add":
            note = args.text.strip()
            if not note:
                raise ValueError("Enter a nonempty note.")
            notes.append(note)
            save_notes(args.file, notes)
            print(f"Saved note {len(notes)}.")
        else:
            query = args.query.casefold() if args.command == "search" else ""
            for number, note in enumerate(notes, start=1):
                if query in note.casefold():
                    print(f"{number}. {note}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
