from decimal import Decimal, InvalidOperation


def add_expense(expenses, category, entered_amount):
    try:
        amount = Decimal(entered_amount)
    except InvalidOperation as error:
        raise ValueError("Enter a number such as 12.50.") from error

    if not amount.is_finite() or amount <= 0:
        raise ValueError("Enter a positive, finite amount.")
    if amount > 1_000_000:
        raise ValueError("Enter an amount of 1000000 or less.")
    if amount.as_tuple().exponent < -2:
        raise ValueError("Use no more than two decimal places.")

    expenses.append((category, amount))


def totals_by_category(expenses):
    totals = {}
    for category, amount in expenses:
        totals[category] = totals.get(category, Decimal("0")) + amount
    return totals


def show_summary(expenses):
    totals = totals_by_category(expenses)
    if not totals:
        print("No expenses yet.")
        return

    for category, total in sorted(totals.items()):
        print(f"{category}: ${total:.2f}")
    grand_total = sum(totals.values())
    print(f"Total: ${grand_total:.2f}")


def main():
    expenses = []
    while True:
        action = input("[a]dd, [s]ummary, [q]uit: ").strip().lower()
        if action == "a":
            category = input("Category: ").strip().lower()
            if not category:
                print("Enter a category.")
                continue

            amount = input("Amount: ").strip()
            try:
                add_expense(expenses, category, amount)
            except ValueError as error:
                print(error)
        elif action == "s":
            show_summary(expenses)
        elif action == "q":
            return
        else:
            print("Choose a, s, or q.")


if __name__ == "__main__":
    main()
