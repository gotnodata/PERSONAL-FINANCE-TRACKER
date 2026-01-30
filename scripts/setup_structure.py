#!/usr/bin/env python3
"""
Setup script for creating the organized project structure.
Run this script to create all necessary directories and __init__.py files.
"""

import os
from pathlib import Path


def create_project_structure():
    """Create the complete directory structure for the reorganized project."""
    
    # Define the directory structure
    directories = [
        'config',
        'core', 
        'gui/components',
        'gui/styles',
        'gui/utils',
        'cli',
        'tests/test_core',
        'tests/test_gui', 
        'tests/test_cli',
        'data/backups',
        'logs',
        'docs',
        'scripts'
    ]
    
    # Create directories
    created_dirs = []
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            created_dirs.append(directory)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Failed to create directory {directory}: {e}")
    
    # Create __init__.py files for Python packages
    package_dirs = [
        'config',
        'core',
        'gui',
        'gui/components',
        'gui/styles', 
        'gui/utils',
        'cli',
        'tests',
        'tests/test_core',
        'tests/test_gui',
        'tests/test_cli'
    ]
    
    for package_dir in package_dirs:
        init_file = os.path.join(package_dir, '__init__.py')
        try:
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'"""Package initialization for {package_dir}."""\n')
                print(f"Created __init__.py: {init_file}")
        except Exception as e:
            print(f"Failed to create {init_file}: {e}")
    
    return created_dirs


def create_gitignore():
    """Create a comprehensive .gitignore file."""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Project specific
data/backups/*
!data/backups/.gitkeep
logs/*
!logs/.gitkeep
*.csv.bak
finance_data_*.csv
"""
    
    try:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("Created .gitignore file")
    except Exception as e:
        print(f"Failed to create .gitignore: {e}")


def create_keep_files():
    """Create .gitkeep files for empty directories that should be tracked."""
    keep_dirs = ['data/backups', 'logs']
    
    for directory in keep_dirs:
        keep_file = os.path.join(directory, '.gitkeep')
        try:
            with open(keep_file, 'w') as f:
                f.write("# This file ensures the directory is tracked by git\n")
            print(f"Created .gitkeep: {keep_file}")
        except Exception as e:
            print(f"Failed to create {keep_file}: {e}")


def main():
    """Main setup function."""
    print("Setting up Personal Finance Tracker project structure...\n")
    
    # Create directory structure
    created_dirs = create_project_structure()
    
    print(f"\nCreated {len(created_dirs)} directories")
    
    # Create .gitignore
    create_gitignore()
    
    # Create .gitkeep files
    create_keep_files()
    
    print("\nProject structure setup complete!")
    print("\nNext steps:")
    print("1. Review the created directories")
    print("2. Run the file migration script")
    print("3. Update import statements")
    print("4. Test the reorganized code")


if __name__ == "__main__":
    main()
