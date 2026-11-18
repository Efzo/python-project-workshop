import argparse
from contextlib import closing
import csv
from datetime import date
import json
import logging
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory


def read_sales(source):
    with source.open(encoding="utf-8", newline="") as input_file:
        reader = csv.DictReader(input_file)
        if not {"sale_id", "amount_cents"}.issubset(reader.fieldnames or []):
            raise ValueError("Expected sale_id and amount_cents columns.")
        sales = {}
        for row in reader:
            sale_id = (row["sale_id"] or "").strip()
            amount = int(row["amount_cents"] or "")
            if not sale_id or sale_id in sales or not 0 <= amount <= 1_000_000_000:
                raise ValueError(f"Invalid or duplicate sale on line {reader.line_num}.")
            sales[sale_id] = amount
    return sales


def record_report(database, day, sales):
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS daily_report (day TEXT PRIMARY KEY, count INTEGER, cents INTEGER)"
        )
        connection.execute(
            """
            INSERT INTO daily_report VALUES (?, ?, ?)
            ON CONFLICT(day) DO UPDATE SET count=excluded.count, cents=excluded.cents
            """,
            (day.isoformat(), len(sales), sum(sales.values())),
        )


def write_report(output_dir, day, sales):
    report = {"date": day.isoformat(), "sales": len(sales), "total_cents": sum(sales.values())}
    destination = output_dir / f"{day}.json"
    with TemporaryDirectory(dir=output_dir) as staging:
        temporary = Path(staging) / "report.json"
        temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        temporary.replace(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description="Publish a daily sales report.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--day", type=date.fromisoformat, default=date.today())
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        sales = read_sales(args.source)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        record_report(args.output_dir / "runs.db", args.day, sales)
        destination = write_report(args.output_dir, args.day, sales)
    except (OSError, ValueError, OverflowError, csv.Error, sqlite3.Error) as error:
        parser.exit(1, f"Report failed: {error}\n")
    logging.info("Wrote %s from %s sale(s)", destination, len(sales))


if __name__ == "__main__":
    main()
