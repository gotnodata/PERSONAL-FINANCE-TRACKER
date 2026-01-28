"""Comprehensive unit tests for the Personal Finance Tracker."""

import os
import tempfile
from datetime import datetime

import pytest
import pandas as pd

from constants import DATE_FORMAT, Category
from data_manager import DataManager, Transaction
from data_entry import get_date, get_amount, get_category, get_description


class TestTransaction:
    """Tests for the Transaction class."""

    def test_valid_transaction(self):
        """Test creating a valid transaction."""
        t = Transaction(
            id=1,
            date="28-01-2026",
            amount=100.0,
            category=Category.INCOME.value,
            description="Test transaction",
        )
        assert t.id == 1
        assert t.amount == 100.0

    def test_invalid_date_format(self):
        """Test transaction with invalid date format."""
        with pytest.raises(ValueError, match="Invalid date format"):
            Transaction(
                id=1,
                date="2026-01-28",
                amount=100.0,
                category=Category.INCOME.value,
                description="Test",
            )

    def test_negative_amount(self):
        """Test transaction with negative amount."""
        with pytest.raises(ValueError, match="Amount must be positive"):
            Transaction(
                id=1,
                date="28-01-2026",
                amount=-100.0,
                category=Category.INCOME.value,
                description="Test",
            )

    def test_invalid_category(self):
        """Test transaction with invalid category."""
        with pytest.raises(ValueError, match="Invalid category"):
            Transaction(
                id=1,
                date="28-01-2026",
                amount=100.0,
                category="Invalid",
                description="Test",
            )

    def test_to_dict(self):
        """Test converting transaction to dictionary."""
        t = Transaction(
            id=1,
            date="28-01-2026",
            amount=100.0,
            category=Category.INCOME.value,
            description="Test",
        )
        d = t.to_dict()
        assert d["id"] == 1
        assert d["amount"] == 100.0
        assert d["category"] == Category.INCOME.value

    def test_from_dict(self):
        """Test creating transaction from dictionary."""
        data = {
            "id": 1,
            "date": "28-01-2026",
            "amount": 100.0,
            "category": Category.INCOME.value,
            "description": "Test",
        }
        t = Transaction.from_dict(data)
        assert t.id == 1
        assert t.amount == 100.0


class TestDataManager:
    """Tests for the DataManager class."""

    @pytest.fixture
    def temp_csv(self):
        """Create a temporary CSV file for testing."""
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.unlink(path)

    @pytest.fixture
    def data_manager(self, temp_csv):
        """Create a DataManager instance with temp file."""
        return DataManager(temp_csv)

    def test_initialize_csv(self, data_manager):
        """Test CSV initialization."""
        assert os.path.exists(data_manager.csv_file)
        df = pd.read_csv(data_manager.csv_file)
        assert list(df.columns) == ["id", "date", "amount", "category", "description"]

    def test_add_transaction(self, data_manager):
        """Test adding a transaction."""
        t = data_manager.add_transaction(
            date="28-01-2026",
            amount=100.0,
            category=Category.INCOME.value,
            description="Salary",
        )
        assert t.id == 1
        assert t.amount == 100.0

        # Verify it was written to CSV
        df = pd.read_csv(data_manager.csv_file)
        assert len(df) == 1
        assert df.iloc[0]["amount"] == 100.0

    def test_get_transaction_by_id(self, data_manager):
        """Test retrieving a transaction by ID."""
        t1 = data_manager.add_transaction(
            "28-01-2026", 100.0, Category.INCOME.value, "Test"
        )

        t = data_manager.get_transaction_by_id(t1.id)
        assert t is not None
        assert t.id == t1.id
        assert t.amount == 100.0

    def test_get_nonexistent_transaction(self, data_manager):
        """Test retrieving a non-existent transaction."""
        t = data_manager.get_transaction_by_id(999)
        assert t is None

    def test_get_all_transactions(self, data_manager):
        """Test retrieving all transactions."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "T1")
        data_manager.add_transaction("29-01-2026", 50.0, Category.EXPENSE.value, "T2")

        transactions = data_manager.get_all_transactions()
        assert len(transactions) == 2

    def test_get_transactions_with_date_filter(self, data_manager):
        """Test filtering transactions by date range."""
        data_manager.add_transaction("01-01-2026", 100.0, Category.INCOME.value, "T1")
        data_manager.add_transaction("15-01-2026", 50.0, Category.EXPENSE.value, "T2")
        data_manager.add_transaction("31-01-2026", 75.0, Category.INCOME.value, "T3")

        df = data_manager.get_transactions(
            start_date="10-01-2026", end_date="20-01-2026"
        )
        assert len(df) == 1

    def test_get_transactions_with_category_filter(self, data_manager):
        """Test filtering transactions by category."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "T1")
        data_manager.add_transaction("28-01-2026", 50.0, Category.EXPENSE.value, "T2")

        df = data_manager.get_transactions(category=Category.INCOME.value)
        assert len(df) == 1
        assert df.iloc[0]["category"] == Category.INCOME.value

    def test_get_transactions_with_description_search(self, data_manager):
        """Test searching transactions by description."""
        data_manager.add_transaction(
            "28-01-2026", 100.0, Category.INCOME.value, "Salary"
        )
        data_manager.add_transaction(
            "28-01-2026", 50.0, Category.EXPENSE.value, "Groceries"
        )

        df = data_manager.get_transactions(description_search="salary")
        assert len(df) == 1
        assert "Salary" in df.iloc[0]["description"]

    def test_get_transactions_with_amount_range(self, data_manager):
        """Test filtering transactions by amount range."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "T1")
        data_manager.add_transaction("28-01-2026", 50.0, Category.EXPENSE.value, "T2")
        data_manager.add_transaction("28-01-2026", 150.0, Category.INCOME.value, "T3")

        df = data_manager.get_transactions(min_amount=60.0, max_amount=120.0)
        assert len(df) == 1
        assert df.iloc[0]["amount"] == 100.0

    def test_update_transaction(self, data_manager):
        """Test updating a transaction."""
        t = data_manager.add_transaction(
            "28-01-2026", 100.0, Category.INCOME.value, "Original"
        )

        result = data_manager.update_transaction(
            t.id, amount=200.0, description="Updated"
        )
        assert result is True

        updated = data_manager.get_transaction_by_id(t.id)
        assert updated.amount == 200.0
        assert updated.description == "Updated"

    def test_update_nonexistent_transaction(self, data_manager):
        """Test updating a non-existent transaction."""
        result = data_manager.update_transaction(999, amount=200.0)
        assert result is False

    def test_delete_transaction(self, data_manager):
        """Test deleting a transaction."""
        t = data_manager.add_transaction(
            "28-01-2026", 100.0, Category.INCOME.value, "Test"
        )

        result = data_manager.delete_transaction(t.id)
        assert result is True

        deleted = data_manager.get_transaction_by_id(t.id)
        assert deleted is None

    def test_delete_nonexistent_transaction(self, data_manager):
        """Test deleting a non-existent transaction."""
        result = data_manager.delete_transaction(999)
        assert result is False

    def test_get_summary(self, data_manager):
        """Test getting financial summary."""
        data_manager.add_transaction(
            "28-01-2026", 1000.0, Category.INCOME.value, "Salary"
        )
        data_manager.add_transaction(
            "28-01-2026", 200.0, Category.EXPENSE.value, "Rent"
        )
        data_manager.add_transaction("28-01-2026", 50.0, Category.EXPENSE.value, "Food")

        summary = data_manager.get_summary()
        assert summary["total_income"] == 1000.0
        assert summary["total_expense"] == 250.0
        assert summary["net_savings"] == 750.0
        assert summary["transaction_count"] == 3

    def test_get_summary_empty(self, data_manager):
        """Test getting summary with no transactions."""
        summary = data_manager.get_summary()
        assert summary["total_income"] == 0.0
        assert summary["total_expense"] == 0.0
        assert summary["net_savings"] == 0.0
        assert summary["transaction_count"] == 0

    def test_get_category_breakdown(self, data_manager):
        """Test getting category breakdown."""
        data_manager.add_transaction(
            "28-01-2026", 1000.0, Category.INCOME.value, "Salary"
        )
        data_manager.add_transaction(
            "28-01-2026", 200.0, Category.EXPENSE.value, "Rent"
        )

        breakdown = data_manager.get_category_breakdown()
        assert Category.INCOME.value in breakdown
        assert Category.EXPENSE.value in breakdown
        assert breakdown[Category.INCOME.value] == 1000.0
        assert breakdown[Category.EXPENSE.value] == 200.0

    def test_backup_data(self, data_manager, tmp_path):
        """Test creating a backup."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "Test")

        backup_path = str(tmp_path / "backup.csv")
        result = data_manager.backup_data(backup_path)
        assert result == backup_path
        assert os.path.exists(backup_path)

    def test_export_to_json(self, data_manager, tmp_path):
        """Test exporting to JSON."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "Test")

        json_path = str(tmp_path / "export.json")
        data_manager.export_to_json(json_path)
        assert os.path.exists(json_path)

        import json

        with open(json_path, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["amount"] == 100.0

    def test_export_to_excel(self, data_manager, tmp_path):
        """Test exporting to Excel."""
        data_manager.add_transaction("28-01-2026", 100.0, Category.INCOME.value, "Test")

        excel_path = str(tmp_path / "export.xlsx")
        data_manager.export_to_excel(excel_path)
        assert os.path.exists(excel_path)

        df = pd.read_excel(excel_path)
        assert len(df) == 1
        assert df.iloc[0]["amount"] == 100.0

    def test_import_from_json(self, data_manager, tmp_path):
        """Test importing from JSON."""
        # Create JSON file
        json_path = str(tmp_path / "import.json")
        import json

        data = [
            {
                "id": 1,
                "date": "28-01-2026",
                "amount": 100.0,
                "category": Category.INCOME.value,
                "description": "Test",
            }
        ]
        with open(json_path, "w") as f:
            json.dump(data, f)

        count = data_manager.import_from_json(json_path)
        assert count == 1

        transactions = data_manager.get_all_transactions()
        assert len(transactions) == 1


class TestDataEntryHelpers:
    """Tests for data entry helper functions."""

    def test_get_date_with_valid_input(self, monkeypatch):
        """Test get_date with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "28-01-2026")
        result = get_date("Enter date: ")
        assert result == "28-01-2026"

    def test_get_date_with_default(self, monkeypatch):
        """Test get_date with default value."""
        monkeypatch.setattr("builtins.input", lambda _: "")
        result = get_date("Enter date: ", allow_default=True)
        assert result == datetime.today().strftime(DATE_FORMAT)

    def test_get_amount_valid(self, monkeypatch):
        """Test get_amount with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "100.50")
        result = get_amount()
        assert result == 100.50

    def test_get_category_income(self, monkeypatch):
        """Test get_category with Income."""
        monkeypatch.setattr("builtins.input", lambda _: "I")
        result = get_category()
        assert result == Category.INCOME.value

    def test_get_category_expense(self, monkeypatch):
        """Test get_category with Expense."""
        monkeypatch.setattr("builtins.input", lambda _: "E")
        result = get_category()
        assert result == Category.EXPENSE.value

    def test_get_description(self, monkeypatch):
        """Test get_description."""
        monkeypatch.setattr("builtins.input", lambda _: "Test description")
        result = get_description()
        assert result == "Test description"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
