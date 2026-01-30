"""Data management module for the Personal Finance Tracker."""

import csv
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd

from config.constants import (
    CSV_FILE,
    CSV_COLUMNS,
    DATE_FORMAT,
    Category,
    CURRENCY_SYMBOL,
)


@dataclass
class Transaction:
    """Represents a financial transaction."""

    id: int
    date: str
    amount: float
    category: str
    description: str

    def __post_init__(self) -> None:
        """Validate transaction data after initialization."""
        self.validate()

    def validate(self) -> None:
        """Validate transaction data."""
        # Validate date format
        try:
            datetime.strptime(self.date, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"Invalid date format. Expected {DATE_FORMAT}")

        # Validate amount
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number")
        if self.amount <= 0:
            raise ValueError("Amount must be positive")

        # Validate category
        valid_categories = [c.value for c in Category]
        if self.category not in valid_categories:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        """Create transaction from dictionary."""
        return cls(
            id=int(data["id"]),
            date=data["date"],
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
        )


class DataManager:
    """Manages financial data operations."""

    def __init__(self, csv_file: str = CSV_FILE):
        """Initialize data manager with CSV file path."""
        self.csv_file = csv_file
        self.initialize_csv()

    def initialize_csv(self) -> None:
        """Initialize CSV file if it doesn't exist."""
        try:
            df = pd.read_csv(self.csv_file)
            # Check if CSV has correct columns
            if list(df.columns) != CSV_COLUMNS:
                # Migrate old format to new format
                if "id" not in df.columns:
                    self._migrate_csv()
        except FileNotFoundError:
            # Create new CSV file
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(self.csv_file, index=False)
        except pd.errors.EmptyDataError:
            # Handle empty CSV
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(self.csv_file, index=False)

    def _migrate_csv(self) -> None:
        """Migrate old CSV format to new format with IDs."""
        try:
            df = pd.read_csv(self.csv_file)
            # Add ID column
            df.insert(0, "id", range(1, len(df) + 1))
            # Backup old file
            backup_path = f"{self.csv_file}.backup"
            shutil.copy(self.csv_file, backup_path)
            # Save migrated data
            df.to_csv(self.csv_file, index=False)
            print(f"CSV migrated to new format. Backup saved to {backup_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to migrate CSV: {e}")

    def _get_next_id(self) -> int:
        """Get the next available transaction ID."""
        try:
            df = pd.read_csv(self.csv_file)
            if df.empty:
                return 1
            return int(df["id"].max()) + 1
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return 1

    def add_transaction(
        self, date: str, amount: float, category: str, description: str
    ) -> Transaction:
        """Add a new transaction."""
        transaction_id = self._get_next_id()
        transaction = Transaction(transaction_id, date, amount, category, description)

        with open(self.csv_file, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_COLUMNS)
            writer.writerow(transaction.to_dict())

        return transaction

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get a transaction by ID."""
        try:
            df = pd.read_csv(self.csv_file)
            row = df[df["id"] == transaction_id]
            if row.empty:
                return None
            return Transaction.from_dict(row.iloc[0].to_dict())
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return None

    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions."""
        try:
            df = pd.read_csv(self.csv_file)
            if df.empty:
                return []
            return [Transaction.from_dict(row.to_dict()) for _, row in df.iterrows()]
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return []

    def get_transactions(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None,
        description_search: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
    ) -> pd.DataFrame:
        """Get transactions with optional filters."""
        try:
            df = pd.read_csv(self.csv_file)
            if df.empty:
                return df

            # Convert date column to datetime
            df["date"] = pd.to_datetime(df["date"], format=DATE_FORMAT)

            # Apply date range filter
            if start_date:
                start_dt = datetime.strptime(start_date, DATE_FORMAT)
                df = df[df["date"] >= start_dt]

            if end_date:
                end_dt = datetime.strptime(end_date, DATE_FORMAT)
                df = df[df["date"] <= end_dt]

            # Apply category filter
            if category:
                df = df[df["category"] == category]

            # Apply description search
            if description_search:
                df = df[
                    df["description"].str.contains(
                        description_search, case=False, na=False
                    )
                ]

            # Apply amount range filters
            if min_amount is not None:
                df = df[df["amount"] >= min_amount]

            if max_amount is not None:
                df = df[df["amount"] <= max_amount]

            return df

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=CSV_COLUMNS)

    def update_transaction(
        self,
        transaction_id: int,
        date: Optional[str] = None,
        amount: Optional[float] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
    ) -> bool:
        """Update an existing transaction."""
        try:
            df = pd.read_csv(self.csv_file)
            idx = df[df["id"] == transaction_id].index

            if len(idx) == 0:
                return False

            # Update fields if provided
            if date is not None:
                df.loc[idx, "date"] = date
            if amount is not None:
                df.loc[idx, "amount"] = amount
            if category is not None:
                df.loc[idx, "category"] = category
            if description is not None:
                df.loc[idx, "description"] = description

            # Validate updated transaction
            updated_row = df.loc[idx].iloc[0]
            Transaction.from_dict(updated_row.to_dict())

            # Save changes
            df.to_csv(self.csv_file, index=False)
            return True

        except (FileNotFoundError, pd.errors.EmptyDataError, ValueError):
            return False

    def delete_transaction(self, transaction_id: int) -> bool:
        """Delete a transaction by ID."""
        try:
            df = pd.read_csv(self.csv_file)
            initial_len = len(df)
            df = df[df["id"] != transaction_id]

            if len(df) == initial_len:
                return False

            df.to_csv(self.csv_file, index=False)
            return True

        except (FileNotFoundError, pd.errors.EmptyDataError):
            return False

    def get_summary(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, float]:
        """Get financial summary for a date range."""
        df = self.get_transactions(start_date, end_date)

        if df.empty:
            return {
                "total_income": 0.0,
                "total_expense": 0.0,
                "net_savings": 0.0,
                "transaction_count": 0,
            }

        income_df = df[df["category"] == Category.INCOME.value]
        expense_df = df[df["category"] == Category.EXPENSE.value]

        total_income = income_df["amount"].sum() if not income_df.empty else 0.0
        total_expense = expense_df["amount"].sum() if not expense_df.empty else 0.0

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_savings": float(total_income - total_expense),
            "transaction_count": len(df),
        }

    def get_category_breakdown(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, float]:
        """Get breakdown of expenses by category."""
        df = self.get_transactions(start_date, end_date)

        if df.empty:
            return {}

        # Group by category and sum amounts
        breakdown = df.groupby("category")["amount"].sum().to_dict()
        return {k: float(v) for k, v in breakdown.items()}

    def backup_data(self, backup_path: Optional[str] = None) -> str:
        """Create a backup of the CSV file."""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.csv_file}.backup_{timestamp}"

        shutil.copy(self.csv_file, backup_path)
        return backup_path

    def export_to_json(self, output_path: str) -> None:
        """Export transactions to JSON format."""
        transactions = self.get_all_transactions()
        data = [t.to_dict() for t in transactions]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_to_excel(self, output_path: str) -> None:
        """Export transactions to Excel format."""
        df = pd.read_csv(self.csv_file)

        if not df.empty:
            # Convert date to datetime for better Excel formatting
            df["date"] = pd.to_datetime(df["date"], format=DATE_FORMAT)

        df.to_excel(output_path, index=False, sheet_name="Transactions")

    def import_from_json(self, input_path: str) -> int:
        """Import transactions from JSON format. Returns number of imported transactions."""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for item in data:
            try:
                # Skip ID, let system assign new ones
                self.add_transaction(
                    date=item["date"],
                    amount=item["amount"],
                    category=item["category"],
                    description=item["description"],
                )
                count += 1
            except (ValueError, KeyError):
                continue

        return count
