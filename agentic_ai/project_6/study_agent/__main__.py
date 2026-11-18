import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

from .providers import offline_answer, openai_answer


def save_run(db, question, provider, result):
    with db:
        row = db.execute(
            "INSERT INTO runs (question, provider, answer, sources) VALUES (?, ?, ?, ?)",
            (question, provider, result.text, json.dumps(result.sources)),
        )
    return row.lastrowid


def main():
    parser = argparse.ArgumentParser(description="Ask a study agent about the sample notes.")
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    ask = commands.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--provider", choices=("offline", "openai"), default="offline")
    commands.add_parser("history")
    export = commands.add_parser("export")
    export.add_argument("id", type=int)
    export.add_argument("output", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "ask":
            question = args.question.strip()
            if not 1 <= len(question) <= 500:
                raise ValueError("Enter a question between 1 and 500 characters.")
            provider = offline_answer if args.provider == "offline" else openai_answer
            result = provider(question, lambda message: print(message, file=sys.stderr))

        args.db.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(args.db)) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY, question TEXT NOT NULL, provider TEXT NOT NULL,
                    answer TEXT NOT NULL, sources TEXT NOT NULL
                )
                """
            )
            if args.command == "ask":
                run_id = save_run(db, question, args.provider, result)
                print(f"Run {run_id}\n{result.text}\nNotes read: {', '.join(result.sources) or 'none'}")
            elif args.command == "history":
                for run_id, question, provider_name in db.execute(
                    "SELECT id, question, provider FROM runs ORDER BY id"
                ):
                    print(f"{run_id}. [{provider_name}] {question}")
            else:
                run = db.execute("SELECT answer, sources FROM runs WHERE id = ?", (args.id,)).fetchone()
                if run is None:
                    raise ValueError("Run not found.")
                answer, sources = run
                with args.output.open("x", encoding="utf-8") as output:
                    output.write(f"{answer}\n\nNotes read: {', '.join(json.loads(sources)) or 'none'}\n")
                print(f"Exported run {args.id} to {args.output}")
    except KeyboardInterrupt:
        parser.exit(130, "Study session stopped.\n")
    except (ValueError, OSError, OverflowError, sqlite3.Error, RuntimeError) as error:
        parser.exit(1, f"Could not complete command: {error}\n")


if __name__ == "__main__":
    main()
