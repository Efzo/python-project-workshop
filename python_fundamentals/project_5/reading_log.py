import argparse
from contextlib import closing
import sqlite3


CREATE_SESSIONS = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY,
    book TEXT NOT NULL,
    pages INTEGER NOT NULL CHECK (pages > 0)
)
"""


def parse_positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("enter a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(description="Track pages read in each session.")
    parser.add_argument("--db", default="reading.db")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("book")
    add.add_argument("pages", type=parse_positive_int)
    commands.add_parser("report")
    args = parser.parse_args()
    if args.command == "add" and not args.book.strip():
        parser.error("enter a book title")

    try:
        with closing(sqlite3.connect(args.db)) as database:
            with database:
                database.execute(CREATE_SESSIONS)
                if args.command == "add":
                    database.execute(
                        "INSERT INTO sessions (book, pages) VALUES (?, ?)",
                        (args.book.strip(), args.pages),
                    )
                else:
                    rows = database.execute(
                        """
                        SELECT book, COUNT(*), SUM(pages)
                        FROM sessions
                        GROUP BY book
                        ORDER BY SUM(pages) DESC, book ASC
                        """
                    )
                    for book, sessions, pages in rows:
                        print(f"{book}: {pages} pages across {sessions} session(s)")
        if args.command == "add":
            print("Saved reading session.")
    except (sqlite3.Error, OverflowError) as error:
        parser.exit(1, f"Could not use the reading log: {error}\n")


if __name__ == "__main__":
    main()
