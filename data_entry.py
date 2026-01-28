"""Input validation utilities for the Personal Finance Tracker CLI."""

from datetime import datetime
from typing import Optional

from constants import DATE_FORMAT, CATEGORY_SHORTCUTS


def get_date(prompt: str, allow_default: bool = False) -> str:
    """Get and validate a date from user input.

    Args:
        prompt: The prompt to display to the user
        allow_default: If True, allow empty input to default to today

    Returns:
        Validated date string in DATE_FORMAT
    """
    date_str = input(prompt)

    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)

    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print(f"Invalid date format. Please enter the date in {DATE_FORMAT} format!")
        return get_date(prompt, allow_default)


def get_amount() -> float:
    """Get and validate an amount from user input.

    Returns:
        Validated positive amount
    """
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a positive, non-zero value!")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category() -> str:
    """Get and validate a category from user input.

    Returns:
        Validated category string
    """
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORY_SHORTCUTS:
        return CATEGORY_SHORTCUTS[category]

    print("Invalid category. Please enter 'I' for Income and 'E' for Expense!")
    return get_category()


def get_description() -> str:
    """Get a description from user input.

    Returns:
        Description string
    """
    return input("Enter the description: ")


def get_transaction_id() -> int:
    """Get and validate a transaction ID from user input.

    Returns:
        Transaction ID
    """
    try:
        transaction_id = int(input("Enter transaction ID: "))
        if transaction_id <= 0:
            raise ValueError("Transaction ID must be positive")
        return transaction_id
    except ValueError as e:
        print(f"Invalid input: {e}")
        return get_transaction_id()
