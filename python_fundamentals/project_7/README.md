# Project 7 — Sales report

**Goal** Read a CSV one row at a time, then rank categories by total sales.

From the `python_fundamentals` folder, run the following.

```sh
python3 project_7/sales_report.py project_7/sales.csv
```

The final three lines show Books at $25.00, Music at $12.00, and Supplies at $5.00 in that order.

## Follow a sale

- In [sales_report.py](sales_report.py), calling `read_sales(path)` returns a generator. The file opens when iteration begins. Each `yield` hands one sale to the caller and pauses the generator until another value is requested.
- `csv.DictReader` treats the first row as column names. The CSV parser handles quoted fields that include commas. `newline=""` lets the CSV library handle line endings.
- `summarize` consumes the generator and stores one total per category. It can process a file without keeping all the input rows in memory.
- `@timed` replaces `summarize` with a wrapper that times its call and returns its result. `*args` and `**kwargs` forward the caller's arguments. `wraps` preserves metadata such as the original function name.
- The `lambda` returns a tuple sort key. Negative totals give descending order, and category names break ties in ascending order.

## Your turn

1. Add a `--top N` option. On the sample file, `--top 2` should print only Books and Music after the timing line.
2. Add a line `"Office, Paper",10.00` to a copy of the CSV. Check that the category appears as `Office, Paper`. Try an invalid amount and check that the error names the line.
3. In a small script, create one generator with `read_sales` and pass it to `summarize` twice. Predict why the first call produces totals and the second returns an empty dictionary.

Next up is [Project 8 — Concurrent order prep](../project_8/README.md).
