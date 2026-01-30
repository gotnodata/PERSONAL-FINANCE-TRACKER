#!/usr/bin/env python3
"""
GUI App Splitter Script
This script splits the monolithic gui_app.py file into organized components.
"""

import os
import re
from pathlib import Path


def create_dashboard_component():
    """Create the dashboard component file."""
    dashboard_content = '''"""Dashboard component for the Personal Finance Tracker GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config.constants import DATE_FORMAT, CURRENCY_SYMBOL, INCOME_COLOR, EXPENSE_COLOR
from core.data_manager import DataManager
from core.models import Category


class DashboardTab:
    """Dashboard tab component."""
    
    def __init__(self, parent, data_manager: DataManager):
        """Initialize dashboard tab."""
        self.parent = parent
        self.data_manager = data_manager
        self.frame = ttk.Frame(parent, padding="20")
        self.create_dashboard_content()
    
    def create_dashboard_content(self):
        """Create dashboard tab content."""
        title_label = ttk.Label(
            self.frame, text="Financial Dashboard", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        chart_frame = ttk.LabelFrame(
            self.frame, text="Income vs Expense Chart", padding="10"
        )
        chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ttk.Button(
            self.frame, text="Refresh Dashboard", command=self.update_dashboard,
        ).grid(row=2, column=0, pady=10)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.update_dashboard()
    
    def update_dashboard(self):
        """Update the dashboard chart."""
        try:
            df = self.data_manager.get_transactions()
            if df.empty:
                messagebox.showinfo("Info", "No data available for dashboard")
                return

            df_copy = df.copy()
            df_copy.set_index("date", inplace=True)

            income_df = df_copy[df_copy["category"] == Category.INCOME.value].resample("D").sum().reindex(df_copy.index, fill_value=0)
            expense_df = df_copy[df_copy["category"] == Category.EXPENSE.value].resample("D").sum().reindex(df_copy.index, fill_value=0)

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            ax.plot(income_df.index, income_df["amount"], label="Income", color=INCOME_COLOR, linewidth=2)
            ax.plot(expense_df.index, expense_df["amount"], label="Expense", color=EXPENSE_COLOR, linewidth=2)

            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel(f"Amount ({CURRENCY_SYMBOL})", fontsize=12)
            ax.set_title("Income and Expense Over Time", fontsize=14, fontweight="bold")
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error updating dashboard: {e}")
    
    def get_frame(self):
        """Return the dashboard frame."""
        return self.frame
'''
    
    try:
        os.makedirs('gui/components', exist_ok=True)
        with open('gui/components/dashboard.py', 'w') as f:
            f.write(dashboard_content)
        print("Created: gui/components/dashboard.py")
    except Exception as e:
        print(f"Failed to create dashboard component: {e}")


def create_transaction_forms_component():
    """Create the transaction forms component file."""
    forms_content = '''"""Transaction forms component for the Personal Finance Tracker GUI."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from config.constants import DATE_FORMAT, CURRENCY_SYMBOL
from core.data_manager import DataManager
from core.models import Category, Transaction


class AddTransactionForm:
    """Add transaction form component."""
    
    def __init__(self, parent, data_manager: DataManager):
        self.parent = parent
        self.data_manager = data_manager
        self.frame = ttk.Frame(parent, padding="20")
        
        self.date_var = tk.StringVar(value=datetime.now().strftime(DATE_FORMAT))
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()
        
        self.create_form_content()
    
    def create_form_content(self):
        """Create add transaction form content."""
        title_label = ttk.Label(self.frame, text="Add New Transaction", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(self.frame, text=f"Date ({DATE_FORMAT}):", style="Header.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(self.frame, textvariable=self.date_var, width=30)
        self.date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        ttk.Label(self.frame, text="Amount:", style="Header.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(self.frame, textvariable=self.amount_var, width=30)
        self.amount_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        ttk.Label(self.frame, text="Category:", style="Header.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.category_combo = ttk.Combobox(self.frame, textvariable=self.category_var, values=[Category.INCOME.value, Category.EXPENSE.value], width=27, state="readonly")
        self.category_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.category_combo.set(Category.EXPENSE.value)

        ttk.Label(self.frame, text="Description:", style="Header.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_entry = ttk.Entry(self.frame, textvariable=self.description_var, width=30)
        self.description_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)

        self.frame.columnconfigure(1, weight=1)
    
    def add_transaction(self):
        """Add a new transaction."""
        try:
            date_str = self.date_var.get().strip()
            amount_str = self.amount_var.get().strip()
            category = self.category_var.get()
            description = self.description_var.get().strip()

            if not date_str or not amount_str or not description:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError("Amount must be positive")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid amount: {e}")
                return

            transaction = Transaction(
                date=datetime.strptime(date_str, DATE_FORMAT),
                amount=amount,
                category=Category(category),
                description=description
            )

            self.data_manager.add_transaction(transaction)
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add transaction: {e}")
    
    def clear_form(self):
        """Clear all form fields."""
        self.date_var.set(datetime.now().strftime(DATE_FORMAT))
        self.amount_var.set("")
        self.description_var.set("")
        self.category_combo.set(Category.EXPENSE.value)
    
    def get_frame(self):
        """Return the form frame."""
        return self.frame
'''
    
    try:
        os.makedirs('gui/components', exist_ok=True)
        with open('gui/components/transaction_forms.py', 'w') as f:
            f.write(forms_content)
        print("Created: gui/components/transaction_forms.py")
    except Exception as e:
        print(f"Failed to create transaction forms component: {e}")


def main():
    """Main function to create all components."""
    print("Creating GUI components...")
    
    create_dashboard_component()
    create_transaction_forms_component()
    
    print("GUI components created successfully!")
    print("\nNext steps:")
    print("1. Run: python scripts/migrate_files.py")
    print("2. Update import statements")
    print("3. Test the reorganized code")


if __name__ == "__main__":
    main()
