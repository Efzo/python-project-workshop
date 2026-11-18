# Project 2 — Expense tracker

**Goal** Record expenses during a terminal session and show how much you spent in each category.

From the `python_fundamentals` folder, run [expense_tracker.py](expense_tracker.py).

```sh
python3 project_2/expense_tracker.py
```

Choose `a` and enter `Food` and `12.50`. Add `food` with `2.25`, then choose `s`. Expect `food: $14.75` and `Total: $14.75`. Choose `q` to exit.

## Follow the data

1. `main()` owns the list and passes it to the functions. A function receives arguments through its parameters. `add_expense` uses `.append()` to mutate the same list that `main` holds.
2. Each entry is a tuple `(category, amount)`. The list can grow, while the tuple keeps each pair together. `Decimal("12.50")` represents a base-10 amount directly.
3. `totals_by_category` starts with an empty dictionary. For each entry, `.get(category, Decimal("0"))` retrieves the previous total or gives the first entry a starting balance of zero. This function returns a new dictionary and leaves the expense list alone.
4. `show_summary` formats the dictionary for the user. The `if __name__ == "__main__"` guard starts the menu when you run the script. You can import the functions into another script without starting the menu.
5. Try entering `abc` for the amount. `try` runs the conversion. On failure, `except` catches the conversion error and the menu displays a helpful message.

## Your turn

- Add a count of recorded expenses. Two entries in the same category should report two expenses and one category.
- Add a `u` command that removes the most recent expense using `list.pop()`. Check two expenses, one undo, and an undo when the list is empty.
- Write a script that imports and calls `totals_by_category` with a small list you create. Use `assert` to check that two `Decimal("0.10")` amounts sum to `Decimal("0.20")`.

Next up is [Project 3 — Notes CLI](../project_3/README.md).
