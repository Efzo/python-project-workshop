import argparse
import csv
from datetime import date
from pathlib import Path
import sqlite3

from .storage import add_task, complete_task, list_tasks, open_board


def parse_date(value):
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("use YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("use YYYY-MM-DD")
    return parsed


def make_parser():
    parser = argparse.ArgumentParser(description="Manage tasks in a local database.")
    parser.add_argument("--db", type=Path, default=Path("tasks.db"))
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add")
    add.add_argument("title")
    add.add_argument("--due", type=parse_date)
    listing = commands.add_parser("list")
    listing.add_argument("--all", action="store_true", help="include completed tasks")
    done = commands.add_parser("done")
    done.add_argument("id", type=int)
    export = commands.add_parser("export")
    export.add_argument("file", type=Path)
    return parser


def export_tasks(tasks, path):
    with path.open("x", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["id", "title", "due", "status"])
        for task in tasks:
            writer.writerow(
                [task.id, task.title, task.due, "done" if task.done else "open"]
            )


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        with open_board(args.db) as database:
            if args.command == "add":
                task_id = add_task(database, args.title, args.due)
                message = f"Added task {task_id}."
            elif args.command == "done":
                complete_task(database, args.id)
                message = f"Completed task {args.id}."
            elif args.command == "export":
                tasks = list_tasks(database, include_done=True)
                export_tasks(tasks, args.file)
                message = f"Exported {len(tasks)} task(s)."
            else:
                tasks = list_tasks(database, include_done=args.all)
                lines = []
                for task in tasks:
                    status = "done" if task.done else "open"
                    due = f" (due {task.due})" if task.due else ""
                    lines.append(f"{task.id}. [{status}] {task.title}{due}")
                message = "\n".join(lines) or "No tasks."
    except (OSError, OverflowError, sqlite3.Error, ValueError) as error:
        parser.exit(1, f"Could not use task board: {error}\n")

    print(message)
