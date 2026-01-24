# Personal Finance Tracker 🏦

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive personal finance management application with both command-line and graphical user interfaces. Track income, expenses, and visualize your financial data with interactive charts.

## ✨ Features

### 🖥️ Dual Interface Options
- **GUI Application**: Modern, interactive tkinter-based interface with tabbed navigation
- **Command-Line Interface**: Traditional terminal-based operation for power users

### 📊 Core Functionality
- **Transaction Management**: Add, view, and categorize financial transactions
- **Data Visualization**: Interactive matplotlib charts showing income vs expense trends
- **Date Range Filtering**: View transactions within specific time periods
- **Real-time Statistics**: Automatic calculation of total income, expenses, and savings
- **Data Persistence**: CSV-based storage for maximum compatibility and portability

### 🎨 GUI Features
- **Modern Design**: Clean, professional interface with ttk styling
- **Tabbed Navigation**: Organized access to all features
- **Interactive Charts**: Real-time financial dashboard with matplotlib integration
- **Form Validation**: Input validation with user-friendly error messages
- **Responsive Layout**: Scalable interface that adapts to window resizing

### 💾 Data Management
- **CSV Storage**: Human-readable data format compatible with spreadsheet applications
- **Automatic Initialization**: Creates data file on first run
- **Data Integrity**: Built-in validation for dates, amounts, and categories
- **Export Ready**: Easy data export for analysis or backup

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-finance-tracker.git
   cd personal-finance-tracker
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### GUI Version (Recommended)
```bash
python gui_app.py
```

#### Command-Line Version
```bash
python main.py
```

## 📖 Usage Guide

### GUI Application

#### Adding Transactions
1. Navigate to the **"Add Transaction"** tab
2. Fill in the transaction details:
   - **Date**: Transaction date (dd-mm-yyyy format, defaults to today)
   - **Amount**: Positive numerical value
   - **Category**: Select "Income" or "Expense" from dropdown
   - **Description**: Brief description of the transaction
3. Click **"Add Transaction"** to save

#### Viewing Transactions
1. Navigate to the **"View Transactions"** tab
2. Enter start and end dates for filtering
3. Click **"View Transactions"** to see:
   - Detailed transaction list
   - Summary statistics (total income, expenses, net savings)

#### Financial Dashboard
1. Navigate to the **"Dashboard"** tab
2. View interactive charts showing:
   - Income trends over time
   - Expense patterns
   - Net savings visualization
3. Click **"Refresh Dashboard"** to update with latest data

### Command-Line Interface

#### Menu Options
```
1. Add a new transaction
2. View transactions and summary within a date range
3. Exit
```

#### Adding Transactions
- Follow the prompts to enter date, amount, category, and description
- Use 'I' for Income or 'E' for Expense
- Press Enter to use today's date

#### Viewing Transactions
- Enter start and end dates (dd-mm-yyyy format)
- View summarized financial data
- Option to generate visual charts

## 🏗️ Project Architecture

### File Structure
```
personal-finance-tracker/
├── main.py                 # Command-line interface
├── gui_app.py             # Graphical user interface
├── data_entry.py          # Input validation and utilities
├── finance_data.csv       # Transaction database (auto-created)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

### Core Components

#### CSV Class (`main.py`)
- **Purpose**: Data management and persistence
- **Methods**:
  - `initialize_csv()`: Creates data file if missing
  - `add_entry()`: Adds new transactions
  - `get_transactions()`: Retrieves filtered transactions

#### FinanceTrackerGUI Class (`gui_app.py`)
- **Purpose**: Graphical user interface implementation
- **Features**:
  - Tabbed interface with three main sections
  - Real-time data visualization
  - Form validation and error handling
  - Responsive design with modern styling

#### Data Entry Module (`data_entry.py`)
- **Purpose**: Input validation and user interaction utilities
- **Functions**:
  - `get_date()`: Date parsing and validation
  - `get_amount()`: Amount validation
  - `get_category()`: Category selection
  - `get_description()`: Description input

### Data Schema

#### Transaction Record Structure
```csv
date,amount,category,description
21-01-2026,200.0,Income,Salary
```

**Field Definitions:**
- **date**: Transaction date in dd-mm-yyyy format
- **amount**: Positive numerical value (float)
- **category**: Either "Income" or "Expense"
- **description**: Free-text description of the transaction

## 🛠️ Development

### Setting Up Development Environment

1. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

2. **Code formatting**
   ```bash
   black *.py
   ```

3. **Linting**
   ```bash
   flake8 *.py
   ```

4. **Type checking**
   ```bash
   mypy *.py
   ```

### Running Tests
```bash
pytest
```

### Building Standalone Executable (Optional)

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build executable**
   ```bash
   pyinstaller --onefile --windowed --name=PersonalFinanceTracker --add-data=data_entry.py;. --add-data=finance_data.csv;. gui_app.py
   ```

3. **Find executable** in `dist/PersonalFinanceTracker.exe`

## 📊 Data Visualization

### Chart Types
- **Line Charts**: Income and expense trends over time
- **Summary Statistics**: Real-time calculation of financial metrics
- **Date Range Analysis**: Filtered data visualization

### Chart Features
- **Interactive**: Zoom and pan capabilities
- **Color-coded**: Green for income, red for expenses
- **Responsive**: Adapts to window resizing
- **Export Ready**: Charts can be saved as images

## 🔧 Configuration

### Customization Options

#### Date Format
- Default: `dd-mm-yyyy`
- Configurable in `CSV.FORMAT` constant

#### Window Size
- GUI default: `1200x800`
- Adjustable in `gui_app.py`

#### Chart Styling
- Colors, fonts, and sizes configurable in matplotlib sections

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### Date Format Issues
- **Problem**: Invalid date format
- **Solution**: Use dd-mm-yyyy format (e.g., 21-01-2026)

#### GUI Not Loading
- **Problem**: tkinter not installed
- **Solution**: 
  - Windows: tkinter comes with Python
  - Linux: `sudo apt-get install python3-tk`
  - macOS: tkinter comes with Python

#### File Permissions
- **Problem**: Cannot write to finance_data.csv
- **Solution**: Ensure write permissions in project directory

### Debug Mode
Add debug prints by modifying the logging level in the main functions.

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Contribution Workflow

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Code Standards
- Follow PEP 8 style guidelines
- Use black for code formatting
- Add docstrings to new functions
- Include type hints where appropriate
- Write tests for new features

### Feature Ideas
- [ ] Budget tracking and alerts
- [ ] Recurring transaction support
- [ ] Data export to multiple formats
- [ ] Advanced chart types (pie charts, bar charts)
- [ ] Transaction categories and tags
- [ ] Search and filter functionality
- [ ] Data backup and restore
- [ ] Multi-currency support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **pandas** - For powerful data manipulation
- **matplotlib** - For beautiful data visualization
- **tkinter** - For the GUI framework
- **Python** - For making this project possible

## 📞 Support

### Getting Help
- **Documentation**: Check this README file
- **Issues**: Report bugs via GitHub Issues
- **Features**: Request features via GitHub Discussions

### FAQ

**Q: Can I use this on macOS/Linux?**
A: Yes! The application is cross-platform compatible.

**Q: How do I backup my data?**
A: Simply copy the `finance_data.csv` file to a safe location.

**Q: Can I import data from other finance apps?**
A: Yes, if you can export to CSV format with the correct column structure.

**Q: Is my financial data secure?**
A: Data is stored locally in CSV format. No internet connection required.

---

## 📈 Project Statistics

- **Lines of Code**: ~500+ lines
- **Languages**: Python
- **Dependencies**: 3 main packages
- **Last Updated**: 2024
- **Version**: 1.0.0

---

**Made with ❤️ for personal finance management**
