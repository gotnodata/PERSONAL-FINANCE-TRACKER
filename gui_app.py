import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import csv
from data_entry import get_date, get_amount, get_category, get_description

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=10)
        self.style.map('TButton', background=[('active', '#4CAF50')])
        
        # Initialize CSV
        self.CSV_FILE = "finance_data.csv"
        self.COLUMNS = ["date", "amount", "category", "description"]
        self.FORMAT = "%d-%m-%Y"
        self.initialize_csv()
        
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
        self.notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create tabs
        self.create_add_transaction_tab()
        self.create_view_transactions_tab()
        self.create_dashboard_tab()
        
    def initialize_csv(self):
        try:
            pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.CSV_FILE, index=False)
    
    def create_add_transaction_tab(self):
        # Add Transaction Tab
        self.add_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.add_frame, text="Add Transaction")
        
        # Title
        title_label = ttk.Label(self.add_frame, text="Add New Transaction", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Date field
        ttk.Label(self.add_frame, text="Date (dd-mm-yyyy):", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime(self.FORMAT))
        self.date_entry = ttk.Entry(self.add_frame, textvariable=self.date_var, width=30)
        self.date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Amount field
        ttk.Label(self.add_frame, text="Amount:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self.add_frame, textvariable=self.amount_var, width=30)
        self.amount_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Category field
        ttk.Label(self.add_frame, text="Category:", style='Header.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.add_frame, textvariable=self.category_var, 
                                         values=["Income", "Expense"], width=27, state="readonly")
        self.category_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.category_combo.set("Expense")
        
        # Description field
        ttk.Label(self.add_frame, text="Description:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_var = tk.StringVar()
        self.description_entry = ttk.Entry(self.add_frame, textvariable=self.description_var, width=30)
        self.description_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(self.add_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.add_frame.columnconfigure(1, weight=1)
    
    def create_view_transactions_tab(self):
        # View Transactions Tab
        self.view_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.view_frame, text="View Transactions")
        
        # Title
        title_label = ttk.Label(self.view_frame, text="View Transactions", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Date range frame
        date_frame = ttk.LabelFrame(self.view_frame, text="Date Range", padding="10")
        date_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start date
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(date_frame, textvariable=self.start_date_var, width=20)
        self.start_date_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # End date
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(date_frame, textvariable=self.end_date_var, width=20)
        self.end_date_entry.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        
        # View button
        ttk.Button(date_frame, text="View Transactions", command=self.view_transactions).grid(row=0, column=4, pady=5, padx=(20, 0))
        
        # Summary frame
        self.summary_frame = ttk.LabelFrame(self.view_frame, text="Summary", padding="10")
        self.summary_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.summary_text = tk.Text(self.summary_frame, height=4, width=80, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # Transactions text area
        transactions_frame = ttk.LabelFrame(self.view_frame, text="Transactions", padding="10")
        transactions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create scrolled text widget
        self.transactions_text = scrolledtext.ScrolledText(transactions_frame, height=15, width=80, wrap=tk.NONE)
        self.transactions_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.rowconfigure(3, weight=1)
    
    def create_dashboard_tab(self):
        # Dashboard Tab
        self.dashboard_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        
        # Title
        title_label = ttk.Label(self.dashboard_frame, text="Financial Dashboard", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Chart frame
        chart_frame = ttk.LabelFrame(self.dashboard_frame, text="Income vs Expense Chart", padding="10")
        chart_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Refresh button
        ttk.Button(self.dashboard_frame, text="Refresh Dashboard", command=self.update_dashboard).grid(row=2, column=0, pady=10)
        
        # Configure grid weights
        self.dashboard_frame.columnconfigure(0, weight=1)
        self.dashboard_frame.rowconfigure(1, weight=1)
    
    def add_transaction(self):
        try:
            date = self.date_var.get().strip()
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            description = self.description_var.get().strip()
            
            # Validate date
            datetime.strptime(date, self.FORMAT)
            
            # Validate amount
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            # Add to CSV
            new_entry = {
                "date": date,
                "amount": amount,
                "category": category,
                "description": description
            }
            
            with open(self.CSV_FILE, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
                writer.writerow(new_entry)
            
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.clear_form()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def clear_form(self):
        self.date_var.set(datetime.now().strftime(self.FORMAT))
        self.amount_var.set("")
        self.description_var.set("")
        self.category_combo.set("Expense")
    
    def view_transactions(self):
        try:
            start_date = self.start_date_var.get().strip()
            end_date = self.end_date_var.get().strip()
            
            if not start_date or not end_date:
                messagebox.showerror("Error", "Please enter both start and end dates")
                return
            
            # Validate dates
            datetime.strptime(start_date, self.FORMAT)
            datetime.strptime(end_date, self.FORMAT)
            
            # Get transactions
            df = pd.read_csv(self.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=self.FORMAT)
            start_date_dt = datetime.strptime(start_date, self.FORMAT)
            end_date_dt = datetime.strptime(end_date, self.FORMAT)
            
            mask = (df["date"] >= start_date_dt) & (df["date"] <= end_date_dt)
            filtered_df = df.loc[mask]
            
            if filtered_df.empty:
                self.transactions_text.delete(1.0, tk.END)
                self.transactions_text.insert(tk.END, "No transactions found in the given date range!")
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, "No data to summarize")
            else:
                # Display transactions
                self.transactions_text.delete(1.0, tk.END)
                display_df = filtered_df.copy()
                display_df["date"] = display_df["date"].dt.strftime(self.FORMAT)
                self.transactions_text.insert(tk.END, display_df.to_string(index=False))
                
                # Calculate summary
                total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
                total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
                net_savings = total_income - total_expense
                
                # Display summary
                self.summary_text.delete(1.0, tk.END)
                summary = f"Total Income: ${total_income:.2f}\n"
                summary += f"Total Expense: ${total_expense:.2f}\n"
                summary += f"Net Savings: ${net_savings:.2f}"
                self.summary_text.insert(tk.END, summary)
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def update_dashboard(self):
        try:
            df = pd.read_csv(self.CSV_FILE)
            if df.empty:
                messagebox.showinfo("Info", "No data available for dashboard")
                return
            
            df["date"] = pd.to_datetime(df["date"], format=self.FORMAT)
            df.set_index("date", inplace=True)
            
            # Resample data by day
            income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
            expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
            
            # Clear previous plot
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Plot data
            ax.plot(income_df.index, income_df["amount"], label="Income", color="green", linewidth=2)
            ax.plot(expense_df.index, expense_df["amount"], label="Expense", color="red", linewidth=2)
            
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Amount", fontsize=12)
            ax.set_title("Income and Expense Over Time", fontsize=14, fontweight="bold")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating dashboard: {e}")

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
