"""Application settings and configuration management."""

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
