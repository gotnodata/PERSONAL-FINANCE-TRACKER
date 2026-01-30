"""Transaction forms component for the Personal Finance Tracker GUI."""

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
