"""Command-line interface for the Personal Finance Tracker."""


from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from config.constants import (
    DATE_FORMAT,
    CURRENCY_SYMBOL,
    INCOME_COLOR,
    EXPENSE_COLOR,
    Category,
)
from core.data_manager import DataManager
from core.models import Transaction
from core.data_entry import (
    get_amount,
    get_category,
    get_description,
    get_transaction_id,
    get_date,
)


def add_transaction(data_manager: DataManager) -> None:
    """Add a new transaction interactively."""
    print("\n=== Add New Transaction ===")
    date = get_date(
        f"Enter the date of the transaction ({DATE_FORMAT}) or press Enter for today: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    try:
        transaction = data_manager.add_transaction(date, amount, category, description)
        print(f"\n✓ Transaction #{transaction.id} added successfully!")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def view_transactions(data_manager: DataManager) -> None:
    """View transactions with optional filters."""
    print("\n=== View Transactions ===")
    print("Leave fields blank to skip filtering")

    start_date_input = input(
        f"\nEnter start date ({DATE_FORMAT}) or press Enter to skip: "
    ).strip()
    start_date = start_date_input if start_date_input else None

    end_date_input = input(
        f"Enter end date ({DATE_FORMAT}) or press Enter to skip: "
    ).strip()
    end_date = end_date_input if end_date_input else None

    # Optional filters
    print("\nOptional filters:")
    category_filter = (
        input("Filter by category (Income/Expense) or press Enter to skip: ")
        .strip()
        .title()
    )
    if category_filter not in [Category.INCOME.value, Category.EXPENSE.value]:
        category_filter = None

    description_search = input("Search description or press Enter to skip: ").strip()
    if not description_search:
        description_search = None

    # Get filtered transactions
    df = data_manager.get_transactions(
        start_date=start_date,
        end_date=end_date,
        category=category_filter,
        description_search=description_search,
    )

    if df.empty:
        print("\nNo transactions found matching your filters!")
        return

    # Display transactions
    print(f"\n{'=' * 80}")
    print(
        df.to_string(
            index=False, formatters={"date": lambda x: x.strftime(DATE_FORMAT)}
        )
    )
    print(f"{'=' * 80}")

    # Display summary
    summary = data_manager.get_summary(start_date, end_date)
    print(f"\n📊 Summary:")
    print(f"   Total Income:  {CURRENCY_SYMBOL}{summary['total_income']:.2f}")
    print(f"   Total Expense: {CURRENCY_SYMBOL}{summary['total_expense']:.2f}")
    print(f"   Net Savings:   {CURRENCY_SYMBOL}{summary['net_savings']:.2f}")
    print(f"   Transactions:  {summary['transaction_count']}")

    # Offer to plot
    if input("\nDo you want to plot these transactions? (y/n): ").lower() == "y":
        plot_transactions(df)


def edit_transaction(data_manager: DataManager) -> None:
    """Edit an existing transaction."""
    print("\n=== Edit Transaction ===")
    transaction_id = get_transaction_id()

    # Get current transaction
    transaction = data_manager.get_transaction_by_id(transaction_id)
    if not transaction:
        print(f"\n✗ Transaction #{transaction_id} not found!")
        return

    print(f"\nCurrent transaction:")
    print(f"  ID:          {transaction.id}")
    print(f"  Date:        {transaction.date}")
    print(f"  Amount:      {CURRENCY_SYMBOL}{transaction.amount:.2f}")
    print(f"  Category:    {transaction.category}")
    print(f"  Description: {transaction.description}")

    print("\nEnter new values (press Enter to keep current value):")

    # Get new values
    new_date = input(f"Date [{transaction.date}]: ").strip()
    if not new_date:
        new_date = None

    new_amount_str = input(f"Amount [{transaction.amount}]: ").strip()
    new_amount = None
    if new_amount_str:
        try:
            new_amount = float(new_amount_str)
        except ValueError:
            print("Invalid amount, keeping current value")

    new_category = input(f"Category [{transaction.category}]: ").strip().title()
    if new_category not in [Category.INCOME.value, Category.EXPENSE.value]:
        new_category = None

    new_description = input(f"Description [{transaction.description}]: ").strip()
    if not new_description:
        new_description = None

    # Update transaction
    if data_manager.update_transaction(
        transaction_id, new_date, new_amount, new_category, new_description
    ):
        print(f"\n✓ Transaction #{transaction_id} updated successfully!")
    else:
        print(f"\n✗ Failed to update transaction #{transaction_id}")


def delete_transaction(data_manager: DataManager) -> None:
    """Delete a transaction."""
    print("\n=== Delete Transaction ===")
    transaction_id = get_transaction_id()

    # Get transaction to confirm
    transaction = data_manager.get_transaction_by_id(transaction_id)
    if not transaction:
        print(f"\n✗ Transaction #{transaction_id} not found!")
        return

    print(f"\nTransaction to delete:")
    print(f"  ID:          {transaction.id}")
    print(f"  Date:        {transaction.date}")
    print(f"  Amount:      {CURRENCY_SYMBOL}{transaction.amount:.2f}")
    print(f"  Category:    {transaction.category}")
    print(f"  Description: {transaction.description}")

    confirm = input("\nAre you sure you want to delete this transaction? (yes/no): ")
    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    if data_manager.delete_transaction(transaction_id):
        print(f"\n✓ Transaction #{transaction_id} deleted successfully!")
    else:
        print(f"\n✗ Failed to delete transaction #{transaction_id}")


def search_transactions(data_manager: DataManager) -> None:
    """Search transactions with advanced filters."""
    print("\n=== Advanced Search ===")

    # Get filter criteria
    description_search = input("Search in description: ").strip()
    if not description_search:
        description_search = None

    category_filter = (
        input("Filter by category (Income/Expense) or press Enter to skip: ")
        .strip()
        .title()
    )
    if category_filter not in [Category.INCOME.value, Category.EXPENSE.value]:
        category_filter = None

    min_amount_str = input("Minimum amount or press Enter to skip: ").strip()
    min_amount = None
    if min_amount_str:
        try:
            min_amount = float(min_amount_str)
        except ValueError:
            print("Invalid amount, skipping filter")

    max_amount_str = input("Maximum amount or press Enter to skip: ").strip()
    max_amount = None
    if max_amount_str:
        try:
            max_amount = float(max_amount_str)
        except ValueError:
            print("Invalid amount, skipping filter")

    # Search
    df = data_manager.get_transactions(
        category=category_filter,
        description_search=description_search,
        min_amount=min_amount,
        max_amount=max_amount,
    )

    if df.empty:
        print("\nNo transactions found matching your search!")
        return

    print(f"\nFound {len(df)} transaction(s):")
    print(f"\n{'=' * 80}")
    print(
        df.to_string(
            index=False, formatters={"date": lambda x: x.strftime(DATE_FORMAT)}
        )
    )
    print(f"{'=' * 80}")


def show_reports(data_manager: DataManager) -> None:
    """Show financial reports and analysis."""
    print("\n=== Financial Reports ===")
    print("1. Category Breakdown")
    print("2. Monthly Summary")
    print("3. Overall Summary")
    choice = input("\nSelect report type (1-3): ").strip()

    if choice == "1":
        breakdown = data_manager.get_category_breakdown()
        print("\n📊 Category Breakdown:")
        for category, amount in breakdown.items():
            print(f"   {category}: {CURRENCY_SYMBOL}{amount:.2f}")

    elif choice == "2":
        # Get date range for monthly summary
        start_date = get_date(f"Enter start date ({DATE_FORMAT}): ")
        end_date = get_date(f"Enter end date ({DATE_FORMAT}): ")
        summary = data_manager.get_summary(start_date, end_date)

        print(f"\n📊 Summary from {start_date} to {end_date}:")
        print(f"   Total Income:  {CURRENCY_SYMBOL}{summary['total_income']:.2f}")
        print(f"   Total Expense: {CURRENCY_SYMBOL}{summary['total_expense']:.2f}")
        print(f"   Net Savings:   {CURRENCY_SYMBOL}{summary['net_savings']:.2f}")
        print(f"   Transactions:  {summary['transaction_count']}")

    elif choice == "3":
        summary = data_manager.get_summary()
        print(f"\n📊 Overall Summary:")
        print(f"   Total Income:  {CURRENCY_SYMBOL}{summary['total_income']:.2f}")
        print(f"   Total Expense: {CURRENCY_SYMBOL}{summary['total_expense']:.2f}")
        print(f"   Net Savings:   {CURRENCY_SYMBOL}{summary['net_savings']:.2f}")
        print(f"   Transactions:  {summary['transaction_count']}")


def backup_and_export(data_manager: DataManager) -> None:
    """Backup and export data."""
    print("\n=== Backup & Export ===")
    print("1. Create backup")
    print("2. Export to JSON")
    print("3. Export to Excel")
    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        backup_path = data_manager.backup_data()
        print(f"\n✓ Backup created: {backup_path}")

    elif choice == "2":
        output_path = (
            input("Enter output filename (default: transactions.json): ").strip()
            or "transactions.json"
        )
        data_manager.export_to_json(output_path)
        print(f"\n✓ Data exported to {output_path}")

    elif choice == "3":
        output_path = (
            input("Enter output filename (default: transactions.xlsx): ").strip()
            or "transactions.xlsx"
        )
        data_manager.export_to_excel(output_path)
        print(f"\n✓ Data exported to {output_path}")


def plot_transactions(df: pd.DataFrame) -> None:
    """Plot income and expenses over time."""
    if df.empty:
        print("No data to plot!")
        return

    df_copy = df.copy()
    df_copy.set_index("date", inplace=True)

    income_df = (
        df_copy[df_copy["category"] == Category.INCOME.value]
        .resample("D")
        .sum()
        .reindex(df_copy.index, fill_value=0)
    )
    expense_df = (
        df_copy[df_copy["category"] == Category.EXPENSE.value]
        .resample("D")
        .sum()
        .reindex(df_copy.index, fill_value=0)
    )

    plt.figure(figsize=(12, 6))
    plt.plot(
        income_df.index,
        income_df["amount"],
        label="Income",
        color=INCOME_COLOR,
        linewidth=2,
    )
    plt.plot(
        expense_df.index,
        expense_df["amount"],
        label="Expense",
        color=EXPENSE_COLOR,
        linewidth=2,
    )
    plt.xlabel("Date")
    plt.ylabel(f"Amount ({CURRENCY_SYMBOL})")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main() -> None:
    """Main CLI application loop."""
    data_manager = DataManager()

    print("=" * 50)
    print("   Personal Finance Tracker - CLI")
    print("=" * 50)

    while True:
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. Add a new transaction")
        print("2. View transactions")
        print("3. Edit a transaction")
        print("4. Delete a transaction")
        print("5. Search transactions")
        print("6. Financial reports")
        print("7. Backup & Export")
        print("8. Exit")
        print("=" * 50)

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            add_transaction(data_manager)
        elif choice == "2":
            view_transactions(data_manager)
        elif choice == "3":
            edit_transaction(data_manager)
        elif choice == "4":
            delete_transaction(data_manager)
        elif choice == "5":
            search_transactions(data_manager)
        elif choice == "6":
            show_reports(data_manager)
        elif choice == "7":
            backup_and_export(data_manager)
        elif choice == "8":
            print("\n👋 Thank you for using Personal Finance Tracker. Goodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
