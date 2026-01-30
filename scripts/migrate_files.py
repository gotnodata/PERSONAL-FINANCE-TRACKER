#!/usr/bin/env python3
"""
File migration script for reorganizing the Personal Finance Tracker project.
This script moves files to their new locations and creates backups.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


def create_backup():
    """Create a backup of the current project state."""
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Files to backup
        files_to_backup = [
            'constants.py',
            'data_entry.py', 
            'data_manager.py',
            'gui_app.py',
            'main.py',
            'requirements.txt',
            'README.md',
            'test_finance_tracker.py',
            'finance_data.csv'
        ]
        
        for file_name in files_to_backup:
            if os.path.exists(file_name):
                shutil.copy2(file_name, os.path.join(backup_dir, file_name))
                print(f"Backed up: {file_name}")
        
        print(f"\nBackup created in: {backup_dir}/")
        return backup_dir
        
    except Exception as e:
        print(f"Backup failed: {e}")
        return None


def migrate_files():
    """Migrate files to their new locations in the organized structure."""
    
    # File mapping: current -> new location
    file_mappings = {
        'constants.py': 'config/constants.py',
        'data_entry.py': 'core/data_entry.py', 
        'data_manager.py': 'core/data_manager.py',
        # gui_app.py will be split, so we'll handle it separately
        'main.py': 'main.py',  # Keep at root for now
        'test_finance_tracker.py': 'tests/test_finance_tracker.py',  # Will be split later
        'finance_data.csv': 'data/finance_data.csv'
    }
    
    migrated_files = []
    
    for src, dst in file_mappings.items():
        if os.path.exists(src):
            try:
                # Ensure destination directory exists
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                
                # Copy file to new location
                shutil.copy2(src, dst)
                migrated_files.append((src, dst))
                print(f"Migrated: {src} to {dst}")
                
            except Exception as e:
                print(f"Failed to migrate {src}: {e}")
        else:
            print(f"Source file not found: {src}")
    
    return migrated_files


def create_config_settings():
    """Create the new settings.py file in config/."""
    settings_content = '''"""Application settings and configuration management."""

import os
from pathlib import Path
from typing import Dict, Any


class Settings:
    """Application settings class."""
    
    def __init__(self):
        """Initialize settings with default values."""
        self.project_root = Path(__file__).parent.parent
        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        self.backups_dir = self.data_dir / "backups"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.backups_dir.mkdir(exist_ok=True)
    
    @property
    def csv_file(self) -> Path:
        """Path to the main CSV data file."""
        return self.data_dir / "finance_data.csv"
    
    @property
    def log_file(self) -> Path:
        """Path to the application log file."""
        return self.logs_dir / "app.log"
    
    def get_database_url(self) -> str:
        """Get database connection string."""
        return f"sqlite:///{self.csv_file}"
    
    def get_backup_dir(self) -> Path:
        """Get backup directory path."""
        return self.backups_dir
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "project_root": str(self.project_root),
            "data_dir": str(self.data_dir),
            "logs_dir": str(self.logs_dir),
            "backups_dir": str(self.backups_dir),
            "csv_file": str(self.csv_file),
            "log_file": str(self.log_file)
        }


# Global settings instance
settings = Settings()
'''
    
    try:
        os.makedirs('config', exist_ok=True)
        with open('config/settings.py', 'w') as f:
            f.write(settings_content)
        print("Created: config/settings.py")
    except Exception as e:
        print(f"Failed to create config/settings.py: {e}")


def create_core_models():
    """Create the new models.py file in core/."""
    models_content = '''"""Data models for the Personal Finance Tracker."""

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
'''
    
    try:
        os.makedirs('core', exist_ok=True)
        with open('core/models.py', 'w') as f:
            f.write(models_content)
        print("Created: core/models.py")
    except Exception as e:
        print(f"Failed to create core/models.py: {e}")


def update_imports():
    """Create a guide for updating import statements."""
    import_guide = '''# Import Update Guide

## Old Imports → New Imports

### Constants
```python
# OLD
from constants import DATE_FORMAT, CURRENCY_SYMBOL, Category

# NEW  
from config.constants import DATE_FORMAT, CURRENCY_SYMBOL, Category
from core.models import Transaction, Category, FinancialSummary
```

### Data Manager
```python
# OLD
from data_manager import DataManager, Transaction

# NEW
from core.data_manager import DataManager
from core.models import Transaction
```

### Settings
```python
# NEW
from config.settings import settings
```

## Files to Update

1. main.py
2. gui_app.py (will be split)
3. test_finance_tracker.py (will be split)
4. Any other files that import from moved modules

## Testing

After updating imports, run:
```bash
python -m pytest tests/
python main.py
python gui_app.py
```
'''
    
    try:
        with open('IMPORT_UPDATE_GUIDE.md', 'w') as f:
            f.write(import_guide)
        print("Created: IMPORT_UPDATE_GUIDE.md")
    except Exception as e:
        print(f"Failed to create import guide: {e}")


def main():
    """Main migration function."""
    print("Starting file migration...\n")
    
    # Create backup first
    print("1. Creating backup...")
    backup_dir = create_backup()
    if not backup_dir:
        print("Backup failed. Aborting migration.")
        return
    
    # Migrate files
    print("\n2. Migrating files...")
    migrated_files = migrate_files()
    
    # Create new files
    print("\n3. Creating new configuration files...")
    create_config_settings()
    create_core_models()
    update_imports()
    
    # Summary
    print(f"\nMigration completed!")
    print(f"Backup location: {backup_dir}")
    print(f"Files migrated: {len(migrated_files)}")
    
    print("\nNext steps:")
    print("1. Review IMPORT_UPDATE_GUIDE.md")
    print("2. Update import statements in your files")
    print("3. Test the migrated code")
    print("4. Run: python scripts/split_gui_app.py to split the GUI file")
    
    print("\nImportant:")
    print("- Original files are still in place")
    print("- Test thoroughly before removing original files")
    print("- Keep the backup until you're sure everything works")


if __name__ == "__main__":
    main()
