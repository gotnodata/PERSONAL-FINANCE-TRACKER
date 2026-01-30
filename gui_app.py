"""Graphical user interface for the Personal Finance Tracker."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config.constants import (
    DATE_FORMAT,
    CURRENCY_SYMBOL,
    INCOME_COLOR,
    EXPENSE_COLOR,
    Category,
    GUI_WINDOW_SIZE,
    GUI_BACKGROUND_COLOR,
)
from core.data_manager import DataManager
from core.models import Transaction


class FinanceTrackerGUI:
    """Main GUI application class."""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry(GUI_WINDOW_SIZE)
        self.root.configure(bg=GUI_BACKGROUND_COLOR)

        # Initialize data manager
        self.data_manager = DataManager()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure styles
        self.style.configure(
            "Title.TLabel", font=("Arial", 16, "bold"), background=GUI_BACKGROUND_COLOR
        )
        self.style.configure(
            "Header.TLabel", font=("Arial", 12, "bold"), background=GUI_BACKGROUND_COLOR
        )
        self.style.configure("TFrame", background=GUI_BACKGROUND_COLOR)
        self.style.configure("TButton", font=("Arial", 10), padding=10)
        self.style.map("TButton", background=[("active", "#4CAF50")])

        # Create main container
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        # Create tabs
        self.create_add_transaction_tab()
        self.create_view_transactions_tab()
        self.create_edit_delete_tab()
        self.create_search_tab()
        self.create_reports_tab()
        self.create_dashboard_tab()
        self.create_backup_export_tab()

    def create_add_transaction_tab(self) -> None:
        """Create the Add Transaction tab."""
        self.add_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.add_frame, text="Add Transaction")

        # Title
        title_label = ttk.Label(
            self.add_frame, text="Add New Transaction", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Date field
        ttk.Label(
            self.add_frame, text=f"Date ({DATE_FORMAT}):", style="Header.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime(DATE_FORMAT))
        self.date_entry = ttk.Entry(
            self.add_frame, textvariable=self.date_var, width=30
        )
        self.date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Amount field
        ttk.Label(self.add_frame, text="Amount:", style="Header.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(
            self.add_frame, textvariable=self.amount_var, width=30
        )
        self.amount_entry.grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        # Category field
        ttk.Label(self.add_frame, text="Category:", style="Header.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            self.add_frame,
            textvariable=self.category_var,
            values=[Category.INCOME.value, Category.EXPENSE.value],
            width=27,
            state="readonly",
        )
        self.category_combo.grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        self.category_combo.set(Category.EXPENSE.value)

        # Description field
        ttk.Label(self.add_frame, text="Description:", style="Header.TLabel").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(
            self.add_frame, textvariable=self.description_var, width=30
        )
        self.description_entry.grid(
            row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        # Buttons
        button_frame = ttk.Frame(self.add_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame, text="Add Transaction", command=self.add_transaction
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(
            side=tk.LEFT, padx=5
        )

        # Configure grid weights
        self.add_frame.columnconfigure(1, weight=1)

    def create_view_transactions_tab(self) -> None:
        """Create the View Transactions tab."""
        self.view_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.view_frame, text="View Transactions")

        # Title
        title_label = ttk.Label(
            self.view_frame, text="View Transactions", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Date range frame
        date_frame = ttk.LabelFrame(self.view_frame, text="Date Range", padding="10")
        date_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        # Start date
        ttk.Label(date_frame, text="Start Date:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(
            date_frame, textvariable=self.start_date_var, width=20
        )
        self.start_date_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # End date
        ttk.Label(date_frame, text="End Date:").grid(
            row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0)
        )
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(
            date_frame, textvariable=self.end_date_var, width=20
        )
        self.end_date_entry.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))

        # View button
        ttk.Button(
            date_frame, text="View Transactions", command=self.view_transactions
        ).grid(row=0, column=4, pady=5, padx=(20, 0))

        # Summary frame
        self.summary_frame = ttk.LabelFrame(
            self.view_frame, text="Summary", padding="10"
        )
        self.summary_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        self.summary_text = tk.Text(
            self.summary_frame, height=4, width=80, wrap=tk.WORD
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Transactions text area
        transactions_frame = ttk.LabelFrame(
            self.view_frame, text="Transactions", padding="10"
        )
        transactions_frame.grid(
            row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        # Create scrolled text widget
        self.transactions_text = scrolledtext.ScrolledText(
            transactions_frame, height=15, width=80, wrap=tk.NONE
        )
        self.transactions_text.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.rowconfigure(3, weight=1)

    def create_edit_delete_tab(self) -> None:
        """Create the Edit/Delete Transaction tab."""
        self.edit_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.edit_frame, text="Edit/Delete")

        # Title
        title_label = ttk.Label(
            self.edit_frame, text="Edit or Delete Transaction", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Transaction ID
        ttk.Label(self.edit_frame, text="Transaction ID:", style="Header.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.edit_id_var = tk.StringVar()
        self.edit_id_entry = ttk.Entry(
            self.edit_frame, textvariable=self.edit_id_var, width=30
        )
        self.edit_id_entry.grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Button(
            self.edit_frame,
            text="Load Transaction",
            command=self.load_transaction_for_edit,
        ).grid(row=1, column=2, pady=5, padx=(10, 0))

        # Current transaction frame
        current_frame = ttk.LabelFrame(
            self.edit_frame, text="Current Transaction", padding="10"
        )
        current_frame.grid(
            row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 10)
        )

        self.current_transaction_text = tk.Text(
            current_frame, height=6, width=60, wrap=tk.WORD
        )
        self.current_transaction_text.pack(fill=tk.BOTH, expand=True)

        # Edit fields
        ttk.Label(
            self.edit_frame,
            text="New Date (leave empty to keep current):",
            style="Header.TLabel",
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.edit_date_var = tk.StringVar()
        self.edit_date_entry = ttk.Entry(
            self.edit_frame, textvariable=self.edit_date_var, width=30
        )
        self.edit_date_entry.grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Label(self.edit_frame, text="New Amount:", style="Header.TLabel").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.edit_amount_var = tk.StringVar()
        self.edit_amount_entry = ttk.Entry(
            self.edit_frame, textvariable=self.edit_amount_var, width=30
        )
        self.edit_amount_entry.grid(
            row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Label(self.edit_frame, text="New Category:", style="Header.TLabel").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        self.edit_category_var = tk.StringVar()
        self.edit_category_combo = ttk.Combobox(
            self.edit_frame,
            textvariable=self.edit_category_var,
            values=["", Category.INCOME.value, Category.EXPENSE.value],
            width=27,
            state="readonly",
        )
        self.edit_category_combo.grid(
            row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Label(self.edit_frame, text="New Description:", style="Header.TLabel").grid(
            row=6, column=0, sticky=tk.W, pady=5
        )
        self.edit_description_var = tk.StringVar()
        self.edit_description_entry = ttk.Entry(
            self.edit_frame, textvariable=self.edit_description_var, width=30
        )
        self.edit_description_entry.grid(
            row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        # Buttons
        button_frame = ttk.Frame(self.edit_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)

        ttk.Button(
            button_frame, text="Update Transaction", command=self.update_transaction
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="Delete Transaction", command=self.delete_transaction
        ).pack(side=tk.LEFT, padx=5)

        self.edit_frame.columnconfigure(1, weight=1)

    def create_search_tab(self) -> None:
        """Create the Search tab."""
        self.search_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.search_frame, text="Search")

        # Title
        title_label = ttk.Label(
            self.search_frame, text="Advanced Search", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Search filters
        ttk.Label(
            self.search_frame, text="Description Search:", style="Header.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.search_description_var = tk.StringVar()
        self.search_description_entry = ttk.Entry(
            self.search_frame, textvariable=self.search_description_var, width=30
        )
        self.search_description_entry.grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Label(
            self.search_frame, text="Category Filter:", style="Header.TLabel"
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.search_category_var = tk.StringVar()
        self.search_category_combo = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_category_var,
            values=["All", Category.INCOME.value, Category.EXPENSE.value],
            width=27,
            state="readonly",
        )
        self.search_category_combo.grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )
        self.search_category_combo.set("All")

        ttk.Label(
            self.search_frame, text="Minimum Amount:", style="Header.TLabel"
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.search_min_amount_var = tk.StringVar()
        self.search_min_amount_entry = ttk.Entry(
            self.search_frame, textvariable=self.search_min_amount_var, width=30
        )
        self.search_min_amount_entry.grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        ttk.Label(
            self.search_frame, text="Maximum Amount:", style="Header.TLabel"
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.search_max_amount_var = tk.StringVar()
        self.search_max_amount_entry = ttk.Entry(
            self.search_frame, textvariable=self.search_max_amount_var, width=30
        )
        self.search_max_amount_entry.grid(
            row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0)
        )

        # Search button
        ttk.Button(
            self.search_frame, text="Search", command=self.search_transactions
        ).grid(row=5, column=0, columnspan=2, pady=20)

        # Results text area
        results_frame = ttk.LabelFrame(self.search_frame, text="Results", padding="10")
        results_frame.grid(
            row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        self.search_results_text = scrolledtext.ScrolledText(
            results_frame, height=15, width=80, wrap=tk.NONE
        )
        self.search_results_text.pack(fill=tk.BOTH, expand=True)

        self.search_frame.columnconfigure(1, weight=1)
        self.search_frame.rowconfigure(6, weight=1)

    def create_reports_tab(self) -> None:
        """Create the Reports tab."""
        self.reports_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.reports_frame, text="Reports")

        # Title
        title_label = ttk.Label(
            self.reports_frame, text="Financial Reports", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Report type selector
        report_type_frame = ttk.Frame(self.reports_frame)
        report_type_frame.grid(row=1, column=0, pady=10)

        ttk.Button(
            report_type_frame,
            text="Category Breakdown",
            command=self.show_category_breakdown,
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            report_type_frame, text="Overall Summary", command=self.show_overall_summary
        ).pack(side=tk.LEFT, padx=5)

        # Report display area
        report_display_frame = ttk.LabelFrame(
            self.reports_frame, text="Report", padding="10"
        )
        report_display_frame.grid(
            row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        self.report_text = scrolledtext.ScrolledText(
            report_display_frame, height=20, width=80, wrap=tk.WORD
        )
        self.report_text.pack(fill=tk.BOTH, expand=True)

        self.reports_frame.columnconfigure(0, weight=1)
        self.reports_frame.rowconfigure(2, weight=1)

    def create_dashboard_tab(self) -> None:
        """Create the Dashboard tab."""
        self.dashboard_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.dashboard_frame, text="Dashboard")

        # Title
        title_label = ttk.Label(
            self.dashboard_frame, text="Financial Dashboard", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Chart frame
        chart_frame = ttk.LabelFrame(
            self.dashboard_frame, text="Income vs Expense Chart", padding="10"
        )
        chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Refresh button
        ttk.Button(
            self.dashboard_frame,
            text="Refresh Dashboard",
            command=self.update_dashboard,
        ).grid(row=2, column=0, pady=10)

        # Configure grid weights
        self.dashboard_frame.columnconfigure(0, weight=1)
        self.dashboard_frame.rowconfigure(1, weight=1)

    def create_backup_export_tab(self) -> None:
        """Create the Backup & Export tab."""
        self.backup_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.backup_frame, text="Backup & Export")

        # Title
        title_label = ttk.Label(
            self.backup_frame, text="Backup & Export Data", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Backup section
        backup_section = ttk.LabelFrame(self.backup_frame, text="Backup", padding="10")
        backup_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(backup_section, text="Create a backup of your transaction data").pack(
            pady=5
        )
        ttk.Button(
            backup_section, text="Create Backup", command=self.create_backup
        ).pack(pady=5)

        # Export section
        export_section = ttk.LabelFrame(self.backup_frame, text="Export", padding="10")
        export_section.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(export_section, text="Export transactions to different formats").pack(
            pady=5
        )

        export_buttons = ttk.Frame(export_section)
        export_buttons.pack(pady=5)

        ttk.Button(
            export_buttons, text="Export to JSON", command=self.export_to_json
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            export_buttons, text="Export to Excel", command=self.export_to_excel
        ).pack(side=tk.LEFT, padx=5)

        # Status text
        status_frame = ttk.LabelFrame(self.backup_frame, text="Status", padding="10")
        status_frame.grid(
            row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        self.backup_status_text = scrolledtext.ScrolledText(
            status_frame, height=10, width=60, wrap=tk.WORD
        )
        self.backup_status_text.pack(fill=tk.BOTH, expand=True)

        self.backup_frame.columnconfigure(0, weight=1)
        self.backup_frame.rowconfigure(3, weight=1)

    def add_transaction(self) -> None:
        """Add a new transaction."""
        try:
            date = self.date_var.get().strip()
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get().strip()

            transaction = self.data_manager.add_transaction(
                date, amount, category, description
            )
            messagebox.showinfo(
                "Success", f"Transaction #{transaction.id} added successfully!"
            )
            self.clear_form()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_form(self) -> None:
        """Clear the add transaction form."""
        self.date_var.set(datetime.now().strftime(DATE_FORMAT))
        self.amount_var.set("")
        self.description_var.set("")
        self.category_combo.set(Category.EXPENSE.value)

    def view_transactions(self) -> None:
        """View transactions with filters."""
        try:
            start_date = self.start_date_var.get().strip() or None
            end_date = self.end_date_var.get().strip() or None

            df = self.data_manager.get_transactions(
                start_date=start_date, end_date=end_date
            )

            if df.empty:
                self.transactions_text.delete(1.0, tk.END)
                self.transactions_text.insert(
                    tk.END, "No transactions found in the given date range!"
                )
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, "No data to summarize")
            else:
                # Display transactions
                self.transactions_text.delete(1.0, tk.END)
                display_df = df.copy()
                display_df["date"] = display_df["date"].dt.strftime(DATE_FORMAT)
                self.transactions_text.insert(tk.END, display_df.to_string(index=False))

                # Calculate and display summary
                summary = self.data_manager.get_summary(start_date, end_date)

                self.summary_text.delete(1.0, tk.END)
                summary_str = (
                    f"Total Income:  {CURRENCY_SYMBOL}{summary['total_income']:.2f}\n"
                    f"Total Expense: {CURRENCY_SYMBOL}{summary['total_expense']:.2f}\n"
                    f"Net Savings:   {CURRENCY_SYMBOL}{summary['net_savings']:.2f}\n"
                    f"Transactions:  {summary['transaction_count']}"
                )
                self.summary_text.insert(tk.END, summary_str)

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_transaction_for_edit(self) -> None:
        """Load a transaction for editing."""
        try:
            transaction_id = int(self.edit_id_var.get())
            transaction = self.data_manager.get_transaction_by_id(transaction_id)

            if not transaction:
                messagebox.showerror(
                    "Error", f"Transaction #{transaction_id} not found!"
                )
                return

            # Display current transaction
            self.current_transaction_text.delete(1.0, tk.END)
            current_text = (
                f"ID:          {transaction.id}\n"
                f"Date:        {transaction.date}\n"
                f"Amount:      {CURRENCY_SYMBOL}{transaction.amount:.2f}\n"
                f"Category:    {transaction.category}\n"
                f"Description: {transaction.description}"
            )
            self.current_transaction_text.insert(tk.END, current_text)

            # Clear edit fields
            self.edit_date_var.set("")
            self.edit_amount_var.set("")
            self.edit_category_var.set("")
            self.edit_description_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Invalid transaction ID")

    def update_transaction(self) -> None:
        """Update a transaction."""
        try:
            transaction_id = int(self.edit_id_var.get())

            new_date = self.edit_date_var.get().strip() or None
            new_amount = (
                float(self.edit_amount_var.get())
                if self.edit_amount_var.get().strip()
                else None
            )
            new_category = self.edit_category_var.get().strip() or None
            new_description = self.edit_description_var.get().strip() or None

            if self.data_manager.update_transaction(
                transaction_id, new_date, new_amount, new_category, new_description
            ):
                messagebox.showinfo(
                    "Success", f"Transaction #{transaction_id} updated successfully!"
                )
                self.current_transaction_text.delete(1.0, tk.END)
                self.edit_id_var.set("")
            else:
                messagebox.showerror(
                    "Error", f"Failed to update transaction #{transaction_id}"
                )

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def delete_transaction(self) -> None:
        """Delete a transaction."""
        try:
            transaction_id = int(self.edit_id_var.get())

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete transaction #{transaction_id}?",
            )

            if not confirm:
                return

            if self.data_manager.delete_transaction(transaction_id):
                messagebox.showinfo(
                    "Success", f"Transaction #{transaction_id} deleted successfully!"
                )
                self.current_transaction_text.delete(1.0, tk.END)
                self.edit_id_var.set("")
            else:
                messagebox.showerror(
                    "Error", f"Failed to delete transaction #{transaction_id}"
                )

        except ValueError:
            messagebox.showerror("Error", "Invalid transaction ID")

    def search_transactions(self) -> None:
        """Search transactions with filters."""
        try:
            description_search = self.search_description_var.get().strip() or None
            category = self.search_category_var.get()
            if category == "All":
                category = None

            min_amount = None
            if self.search_min_amount_var.get().strip():
                min_amount = float(self.search_min_amount_var.get())

            max_amount = None
            if self.search_max_amount_var.get().strip():
                max_amount = float(self.search_max_amount_var.get())

            df = self.data_manager.get_transactions(
                category=category,
                description_search=description_search,
                min_amount=min_amount,
                max_amount=max_amount,
            )

            self.search_results_text.delete(1.0, tk.END)

            if df.empty:
                self.search_results_text.insert(
                    tk.END, "No transactions found matching your search!"
                )
            else:
                display_df = df.copy()
                display_df["date"] = display_df["date"].dt.strftime(DATE_FORMAT)
                self.search_results_text.insert(
                    tk.END, f"Found {len(df)} transaction(s):\n\n"
                )
                self.search_results_text.insert(
                    tk.END, display_df.to_string(index=False)
                )

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def show_category_breakdown(self) -> None:
        """Show category breakdown report."""
        breakdown = self.data_manager.get_category_breakdown()

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "=== Category Breakdown ===\n\n")

        if not breakdown:
            self.report_text.insert(tk.END, "No data available")
        else:
            for category, amount in breakdown.items():
                self.report_text.insert(
                    tk.END, f"{category}: {CURRENCY_SYMBOL}{amount:.2f}\n"
                )

    def show_overall_summary(self) -> None:
        """Show overall summary report."""
        summary = self.data_manager.get_summary()

        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "=== Overall Summary ===\n\n")

        summary_str = (
            f"Total Income:  {CURRENCY_SYMBOL}{summary['total_income']:.2f}\n"
            f"Total Expense: {CURRENCY_SYMBOL}{summary['total_expense']:.2f}\n"
            f"Net Savings:   {CURRENCY_SYMBOL}{summary['net_savings']:.2f}\n"
            f"Transactions:  {summary['transaction_count']}"
        )
        self.report_text.insert(tk.END, summary_str)

    def update_dashboard(self) -> None:
        """Update the dashboard chart."""
        try:
            df = self.data_manager.get_transactions()

            if df.empty:
                messagebox.showinfo("Info", "No data available for dashboard")
                return

            df_copy = df.copy()
            df_copy.set_index("date", inplace=True)

            # Resample data by day
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

            # Clear previous plot
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            # Plot data
            ax.plot(
                income_df.index,
                income_df["amount"],
                label="Income",
                color=INCOME_COLOR,
                linewidth=2,
            )
            ax.plot(
                expense_df.index,
                expense_df["amount"],
                label="Expense",
                color=EXPENSE_COLOR,
                linewidth=2,
            )

            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel(f"Amount ({CURRENCY_SYMBOL})", fontsize=12)
            ax.set_title("Income and Expense Over Time", fontsize=14, fontweight="bold")
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Rotate x-axis labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

            self.figure.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error updating dashboard: {e}")

    def create_backup(self) -> None:
        """Create a backup of the data."""
        try:
            backup_path = self.data_manager.backup_data()
            self.backup_status_text.delete(1.0, tk.END)
            self.backup_status_text.insert(
                tk.END, f"✓ Backup created successfully!\n\nLocation: {backup_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")

    def export_to_json(self) -> None:
        """Export data to JSON."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            )

            if file_path:
                self.data_manager.export_to_json(file_path)
                self.backup_status_text.delete(1.0, tk.END)
                self.backup_status_text.insert(
                    tk.END,
                    f"✓ Data exported to JSON successfully!\n\nLocation: {file_path}",
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to JSON: {e}")

    def export_to_excel(self) -> None:
        """Export data to Excel."""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            )

            if file_path:
                self.data_manager.export_to_excel(file_path)
                self.backup_status_text.delete(1.0, tk.END)
                self.backup_status_text.insert(
                    tk.END,
                    f"✓ Data exported to Excel successfully!\n\nLocation: {file_path}",
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to Excel: {e}")


def main() -> None:
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
