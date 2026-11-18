import argparse
import csv
import json
from pathlib import Path


def summarize(path):
    seen = set()
    shipped_orders = 0
    shipped_cents = 0
    with path.open(encoding="utf-8", newline="") as file:
        records = csv.DictReader(file)
        required = {"order_id", "status", "amount_cents"}
        if not required.issubset(records.fieldnames or []):
            raise ValueError("Missing required CSV columns.")
        for record in records:
            order_id = (record["order_id"] or "").strip()
            if not order_id or order_id in seen:
                raise ValueError(f"Line {records.line_num}: blank or duplicate order ID.")
            status = record["status"]
            try:
                cents = int(record["amount_cents"] or "")
            except ValueError as error:
                raise ValueError(f"Line {records.line_num}: invalid cents.") from error
            if status not in {"pending", "shipped"} or cents < 0:
                raise ValueError(f"Line {records.line_num}: invalid status or amount.")
            seen.add(order_id)
            if status == "shipped":
                shipped_orders += 1
                shipped_cents += cents
    return {"orders": len(seen), "shipped_orders": shipped_orders, "shipped_cents": shipped_cents}


def main():
    parser = argparse.ArgumentParser(description="Summarize orders in a CSV file.")
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(summarize(args.csv_file), indent=2))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Could not read orders: {error}\n")


if __name__ == "__main__":
    main()
