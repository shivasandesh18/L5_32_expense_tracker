"""Personal expense tracker used for the static code analysis lab."""

import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD", "")
expenses = []
monthly_budget = 20000
REPORT_DIR = Path(tempfile.gettempdir()) / "expense_reports"


def add_expense(amount, category="Misc", note=""):
    """Record an expense if its amount is positive."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append(
        {
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def total_by_category():
    """Return total spending grouped by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Update the monthly budget."""
    global monthly_budget
    monthly_budget = new_budget


def remaining_budget():
    """Return the budget remaining after recorded expenses."""
    spent = sum(expense["amount"] for expense in expenses)
    return monthly_budget - spent


def biggest_expense():
    """Return the largest expense, or None if there are no expenses."""
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except ValueError:
        return None


def print_ledger():
    """Print each recorded expense."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Compare a supplied password with the configured sync password."""
    return bool(BANK_SYNC_PASSWORD) and password == BANK_SYNC_PASSWORD


def export_report():
    """Create an empty temporary report file and return its path."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        prefix="expense-report-",
        dir=REPORT_DIR,
        delete=False,
        encoding="utf-8",
    ) as report_file:
        return report_file.name


def open_statement(path):
    """Open a statement without invoking a shell."""
    subprocess.run(["xdg-open", os.fspath(path)], check=False)


def main():
    """Run a small demonstration of the expense tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    largest = biggest_expense()
    print("Biggest expense:", largest["note"] if largest else None)
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        monthly_budget,
    )


if __name__ == "__main__":
    main()
