"""Data models for the Personal Finance Tracker."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class Category(Enum):
    """Transaction category enumeration."""
    INCOME = "Income"
    EXPENSE = "Expense"


@dataclass
class Transaction:
    """Transaction data model."""
    date: datetime
    amount: float
    category: Category
    description: str
    
    def __post_init__(self):
        """Validate transaction data after initialization."""
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        if not self.description.strip():
            raise ValueError("Description cannot be empty")
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            "date": self.date.strftime("%d-%m-%Y"),
            "amount": self.amount,
            "category": self.category.value,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create transaction from dictionary."""
        return cls(
            date=datetime.strptime(data["date"], "%d-%m-%Y"),
            amount=float(data["amount"]),
            category=Category(data["category"]),
            description=data["description"]
        )
    
    def __str__(self) -> str:
        """String representation of transaction."""
        return f"{self.date.strftime('%d-%m-%Y')} | {self.category.value:8} | ${self.amount:8.2f} | {self.description}"


@dataclass
class FinancialSummary:
    """Financial summary data model."""
    total_income: float
    total_expense: float
    net_savings: float
    transaction_count: int
    
    @property
    def savings_rate(self) -> float:
        """Calculate savings rate as percentage."""
        if self.total_income == 0:
            return 0.0
        return (self.net_savings / self.total_income) * 100
    
    def to_dict(self) -> dict:
        """Convert summary to dictionary."""
        return {
            "total_income": self.total_income,
            "total_expense": self.total_expense,
            "net_savings": self.net_savings,
            "transaction_count": self.transaction_count,
            "savings_rate": self.savings_rate
        }
