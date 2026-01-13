# PERSONAL-FINANCE-TRACKER

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#)

One-line summary: A lightweight personal finance tracker written in Python that uses a CSV file as its datastore for transactions, budgets, and simple reports.

Table of contents
- [About](#about)
- [Features](#features)
- [Quick Start](#quick-start)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Running](#running)
- [Data format (CSV)](#data-format-csv)
- [Usage](#usage)
  - [Add / List / Report examples](#add--list--report-examples)
  - [Import & Export](#import--export)
- [Data integrity & concurrency](#data-integrity--concurrency)
- [Configuration](#configuration)
- [Testing](#testing)
- [Development](#development)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Contact](#contact)

About
-----
This repository contains a small Python application to track personal income and expenses. It stores all records in a CSV file (by default `data/finance_data.csv`). The goal is a simple, portable tool that is easy to read and edit manually while providing useful CLI commands for everyday finance tasks.

Features
--------
- Add, edit, delete transactions stored in a CSV file
- Categorize transactions and add optional tags/notes
- Simple monthly/annual text reports (totals by category)
- CSV import from bank exports and CSV export for backups
- Lightweight — no database server required
- Designed for single-user, local use



Quick Start
-----------

Requirements
- Python 3.8 or newer
- pip
- (Optional) git for cloning the repo

Installation
------------
```bash
# clone repo (if not already)
git clone https://github.com/gotnodata/PERSONAL-FINANCE-TRACKER.git
cd PERSONAL-FINANCE-TRACKER

# create virtual environment and activate
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

Running
-------
This project ships as a small CLI.

```bash
# example 1: run as a module (if package exposes a CLI)
python -m pft --help

# example 2: run a script directly
python main.py --help
```

Data format (CSV)
-----------------
By default transactions are stored in a CSV file at `data/finance_data.csv`. The expected columns are:

```csv
date,amount,category,description
12-01-2026,-23.45,Groceries,Supermarket
```

Important: date format is DD-MM-YYYY (day-month-year), for example `12-01-2026`.

Column descriptions:
- date: date in DD-MM-YYYY format (e.g., `12-01-2026`)
- amount: positive for income, negative for expense (decimal)
- category: e.g., Groceries, Rent, Salary
- description: free-form text (optional details like payee or note)

Usage
-----

Add / List / Report examples
```bash
# add a transaction (note the date format DD-MM-YYYY)
python main.py add --date 12-01-2026 --amount -23.45 --category Groceries --description "supermarket"

# list the last 30 transactions
python main.py list --limit 30

# generate a monthly report (summary by category)
# if your CLI accepts month input, use a matching format (e.g., 01-2026 or follow your implementation)
python main.py report --month 01-2026

# delete a transaction by id (if your CLI assigns/uses ids)
python main.py delete --id 42
```

Import & Export
```bash
# import from a bank CSV (you may need to supply a mapping file)
python main.py import --file imports/bank-export.csv --mapping mappings/bank-a.json

# export all transactions to CSV
python main.py export --format csv --output backups/export-2026-01-13.csv
```

Data integrity & concurrency
----------------------------
Using a plain CSV file is simple and portable but has limitations:
- Not transactional: concurrent writes can corrupt the file.
- No automatic schema enforcement beyond your code.

Recommended practices:
- Keep regular backups (export CSV).
- Perform atomic writes: write to a temporary file then rename to the main CSV.
- If multiple processes may access the file, use file locking (e.g., portalocker or flock) or switch to SQLite for concurrent access.
- Validate imported CSVs before merging.

Configuration
-------------
Store configuration in `config.yml` or environment variables. Example `.env` values:
```
TRANSACTIONS_FILE=data/finance_data.csv
BACKUP_DIR=backups
DEFAULT_CURRENCY=USD
DATE_FORMAT=DD-MM-YYYY
```

Testing
-------
Run unit tests with pytest:
```bash
pytest -q
```

Development
-----------
- Lint: `flake8` or `ruff` (if used)
- Format: `black .`
- Run tests after changes before committing

Contributing
------------
Contributions are welcome. Suggested workflow:
1. Fork the repository
2. Create a branch: `git checkout -b feat/my-feature`
3. Run tests and linters
4. Open a pull request with a clear description and small focused changes

Consider adding a `CONTRIBUTING.md` with coding guidelines and commit message format.

Roadmap
-------
Planned improvements:
- Add an optional SQLite backend for safer concurrent access
- Add automatic backups and scheduled export
- Provide a small web UI for visualization
- Improve import mapping UI

License
-------
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Contact
-------
Maintainer: Paul Kahara — [kahara1738@gmail.com](mailto:kahara1738@gmail.com)  
Repository: https://github.com/gotnodata/PERSONAL-FINANCE-TRACKER
