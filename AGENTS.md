# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Personal Finance Tracker is a dual-interface Python application (CLI and GUI) for tracking income and expenses. Data is stored in CSV format (`finance_data.csv`) with the date format `dd-mm-yyyy` (`%d-%m-%Y`).

## Running the Application

### GUI Version (Primary)
```pwsh
python gui_app.py
```

### CLI Version
```pwsh
python main.py
```

### Installing Dependencies
```pwsh
pip install -r requirements.txt
```

Core dependencies: pandas, matplotlib, tkinter (built-in)

## Development Commands

### Code Formatting
```pwsh
black *.py
```

### Linting
```pwsh
flake8 *.py
```

### Type Checking
```pwsh
mypy *.py
```

### Testing
```pwsh
pytest
```

Note: Test files/framework may not exist yet. Check the repository before assuming pytest is configured.

### Building Standalone Executable
```pwsh
pyinstaller --onefile --windowed --name=PersonalFinanceTracker --add-data=data_entry.py;. --add-data=finance_data.csv;. gui_app.py
```

Executable will be in `dist/PersonalFinanceTracker.exe`

## Architecture

### Core Components

**constants Module** (`constants.py`)
- Centralized configuration for date formats, file paths, currencies
- Category enum for type-safe transaction categories
- All magic strings and configuration values in one place

**DataManager Class** (`data_manager.py`)
- **SHARED** data management layer used by both CLI and GUI
- Handles all file I/O operations with `finance_data.csv`
- Methods: `add_transaction()`, `update_transaction()`, `delete_transaction()`, `get_transactions()`, `get_summary()`, `export_to_json()`, `export_to_excel()`, `backup_data()`
- Includes automatic CSV migration from old format (without IDs) to new format (with IDs)

**Transaction Class** (`data_manager.py`)
- Dataclass representing a financial transaction
- Built-in validation for date format, amount, and category
- Methods: `to_dict()`, `from_dict()`, `validate()`

**FinanceTrackerGUI Class** (`gui_app.py`)
- Tkinter-based GUI with **7 tabs**: Add Transaction, View Transactions, Edit/Delete, Search, Reports, Dashboard, Backup & Export
- Uses DataManager for all data operations (no duplication)
- Enhanced features: transaction editing, advanced search, multiple export formats

**CLI Application** (`main.py`)
- Command-line interface with **8 menu options**
- Uses DataManager for all data operations
- Features: add, view, edit, delete, search, reports, backup/export

**data_entry Module** (`data_entry.py`)
- Input validation utilities used by CLI
- Functions: `get_date()`, `get_amount()`, `get_category()`, `get_description()`, `get_transaction_id()`
- All functions have type hints and docstrings

### Key Design Details

**Data Format**
- CSV file: `id,date,amount,category,description`
- Date format: `dd-mm-yyyy` (stored as string, parsed with `%d-%m-%Y`)
- Category: Must be exactly "Income" or "Expense" (validated by Transaction class)
- Amount: Float, must be positive (validated by Transaction class)
- **Transaction IDs**: Auto-incrementing integer IDs for unique identification

**No Code Duplication**
- Both CLI and GUI use the same DataManager class
- All data logic is centralized in `data_manager.py`
- Changes to data handling only need to be made in one place

**Visualization**
- CLI uses `plt.show()` for interactive matplotlib plots
- GUI embeds matplotlib in tkinter using `FigureCanvasTkAgg`
- Both use constants from `constants.py` for colors (INCOME_COLOR, EXPENSE_COLOR)

**Date Handling**
- All date operations use `DATE_FORMAT` constant from `constants.py`
- Pandas conversion: `pd.to_datetime(df["date"], format=DATE_FORMAT)`
- GUI defaults to today's date on form load

**Type Safety**
- All modules have comprehensive type hints
- Category enum prevents invalid category values
- Transaction class validates all fields on creation

## Working with this Codebase

### When Adding Features
- Add data operations to `DataManager` class in `data_manager.py`
- Update both CLI (`main.py`) and GUI (`gui_app.py`) to use the new operations
- Add tests to `test_finance_tracker.py` for new functionality
- Run `black *.py` to format code

### When Modifying Data Storage
- `finance_data.csv` is created automatically on first run
- Old CSV files (without IDs) are automatically migrated with backup
- Changes to CSV schema should update `CSV_COLUMNS` in `constants.py`
- Update `Transaction` class validation if adding/changing fields

### When Testing
- Run `pytest` to execute all unit tests (32 tests covering all core functionality)
- Tests use temporary files and don't affect production data
- Run `pytest --cov` for coverage report
- All tests must pass before committing changes

### Virtual Environment
Windows users should activate with:
```pwsh
venv\Scripts\activate
```

macOS/Linux users:
```bash
source venv/bin/activate
```
