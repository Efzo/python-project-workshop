import argparse
import csv
from decimal import Decimal, InvalidOperation
from functools import wraps
from pathlib import Path
from time import perf_counter


def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = function(*args, **kwargs)
        print(f"{function.__name__} took {perf_counter() - start:.4f} s")
        return result

    return wrapper


def read_sales(path):
    with path.open(encoding="utf-8", newline="") as sales_file:
        reader = csv.DictReader(sales_file)
        if not {"category", "amount"}.issubset(reader.fieldnames or []):
            raise ValueError("Expected category and amount columns.")
        for row in reader:
            category = (row["category"] or "").strip()
            try:
                amount = Decimal(row["amount"] or "")
            except InvalidOperation as error:
                raise ValueError(f"Line {reader.line_num}: invalid amount.") from error
            if not category or not amount.is_finite() or amount < 0:
                raise ValueError(f"Line {reader.line_num}: invalid category or amount.")
            if amount > 1_000_000 or amount.as_tuple().exponent < -2:
                raise ValueError(f"Line {reader.line_num}: use cents and at most 1000000.")
            yield category, amount


@timed
def summarize(sales):
    totals = {}
    for category, amount in sales:
        totals[category] = totals.get(category, Decimal("0")) + amount
    return totals


def main():
    parser = argparse.ArgumentParser(description="Group CSV sales by category.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        totals = summarize(read_sales(args.file))
        ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
        print("\n".join(f"{category}: ${total:.2f}" for category, total in ranked))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Could not report sales: {error}\n")


if __name__ == "__main__":
    main()
