# Project 3 — Order reporter

**Build** Validate a CSV and produce a machine-readable summary of shipped orders.

```sh
python3 project_3/report.py project_3/orders.csv
```

Expect 3 orders, 2 shipped orders, and 2000 shipped cents in the JSON output.

## How it works

1. [report.py](report.py) opens the CSV with `newline=""` so the CSV library handles line endings. `DictReader` makes each row a dictionary keyed by the header.
2. Validate the header before reading rows. For each row, add the order ID to a set after checking that it is present and unique. The input row number helps you find a bad value.
3. Keep money in integer cents so addition stays exact. Only shipped records increment the shipped count and total.
4. `json.dumps` serializes the final dictionary. Data goes to standard output and error messages go to standard error. This lets another script consume the JSON.

## Your turn

- In a copy of the sample, duplicate order `A10`. Check that the command exits with code 1 and reports the row.
- Include `pending_orders` in the report. The original file should produce 1. Test a header-only file and expect zero counts.
- Redirect the report to a file with `> summary.json` and read it back with `python3 -m json.tool summary.json`.

[Next — Stock feed checker](../project_4/README.md)
