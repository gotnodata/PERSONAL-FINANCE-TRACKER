"""Dashboard component for the Personal Finance Tracker GUI."""

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
