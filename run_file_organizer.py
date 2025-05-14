#!/usr/bin/env python
"""
Launcher script for the File Organizer application.
"""
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Run the application
from file_organizer_app.main import main

if __name__ == "__main__":
    main()
