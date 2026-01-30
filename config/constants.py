"""Constants and configuration values for the Personal Finance Tracker."""

import os
from enum import Enum

# File paths
DEFAULT_CSV_FILE = "finance_data.csv"
CSV_FILE = os.environ.get("FINANCE_DATA_FILE", DEFAULT_CSV_FILE)

# Date format
DATE_FORMAT = "%d-%m-%Y"

# CSV columns
CSV_COLUMNS = ["id", "date", "amount", "category", "description"]

# Currency
CURRENCY_SYMBOL = os.environ.get("CURRENCY_SYMBOL", "$")


class Category(Enum):
    """Transaction categories."""

    INCOME = "Income"
    EXPENSE = "Expense"


# Category shortcuts for CLI
CATEGORY_SHORTCUTS = {"I": Category.INCOME.value, "E": Category.EXPENSE.value}

# Chart colors
INCOME_COLOR = "green"
EXPENSE_COLOR = "red"

# GUI settings
GUI_WINDOW_SIZE = "1200x800"
GUI_BACKGROUND_COLOR = "#f0f0f0"
