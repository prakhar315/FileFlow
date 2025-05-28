# File Organizer Pro

A powerful Python desktop application for organizing, managing, and analyzing your files with advanced features.

## Features

### Core Features
1. **Organize Files**: Automatically organize files into folders based on their file types (only creates folders for file types that are actually present).
2. **Find Unused Files**: Identify files that haven't been accessed for a specified period with fast client-side filtering.
3. **Archive Files**: Archive files in their original locations with automatic timestamp-based naming and compression options (ZIP, TAR.GZ).
4. **Delete Files**: Safely delete files and folders with confirmation dialogs.
5. **Find Duplicates**: Identify and manage duplicate files to free up disk space.

### Advanced Features (Coming Soon)
- **File Tagging System**: Tag files with custom categories for better organization
- **File Versioning**: Track changes to files and restore previous versions
- **Smart Organization**: Machine learning-based file categorization that learns from user behavior
- **Full-Text Search**: Search within file contents across multiple file formats
- **Advanced Filters**: Complex search queries with multiple criteria
- **File Analytics Dashboard**: Visualize storage usage by file type, age, and size

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

## Installation

### Standard Installation
1. Clone or download this repository.
2. Navigate to the project directory.
3. Run the application using one of the following methods:

```bash
# Using the launcher script
python run_file_organizer.py

# Or using the batch file (Windows)
run_file_organizer.bat

# Or directly from the package
python -m file_organizer_app.main
```

### Development Setup
For developers who want to contribute to the project:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/file-organizer-pro.git
cd file-organizer-pro
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Run tests:
```bash
python -m unittest discover tests
```

## Usage

### Organize Files Tab

- **Select Directory**: Use the "Browse" button to choose a directory containing files to organize.
- **Organize Files**: Click "Organize Files" to sort files into folders by type.
- **Find Duplicates**: Click "Find Duplicates" to identify duplicate files in the directory.
- **View Results**: Results are displayed in a tabbed interface showing:
  - File types and counts of organized files
  - Pairs of duplicate files found

### Unused Files Tab

- **Select Directory**: Use the "Browse" button to choose a directory to scan.
- **Set Threshold**: Set the number of days to consider a file "unused".
- **Filter by Type**: Optionally filter by file type for more targeted results.
- **Find Unused Files**: Click "Find Unused Files" to display files that haven't been accessed.
- **File Actions**: Right-click on files for additional options:
  - Open file
  - Open containing folder
  - Select all
  - Deselect all

### Archive & Delete Tab

- **Select Source**: Choose a source directory containing files to manage.
- **Select Archive Location**: Choose an archive directory where files will be moved.
- **Load Files**: Click "Load Files" to display files in the source directory.
- **File Operations**: Select files and use the buttons to:
  - Archive selected files
  - Delete selected files
  - Archive entire folder
  - Delete entire folder

## Project Structure

```
file-organizer-pro/
├── run_file_organizer.py     # Launcher script
├── run_file_organizer.bat    # Windows batch launcher
├── file_organizer_app/       # Main package
│   ├── __init__.py
│   ├── main.py               # Application entry point
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── file_organizer.py # File organization functions
│   │   ├── file_metadata.py  # File metadata functions
│   │   ├── file_operations.py# Archive and delete functions
│   │   ├── database.py       # Database operations
│   │   └── tagging.py        # File tagging system
│   └── gui/                  # GUI components
│       ├── __init__.py
│       ├── main_window.py    # Main application window
│       ├── organize_tab.py   # File organization tab
│       ├── unused_files_tab.py # Unused files tab
│       └── archive_tab.py    # Archive and delete tab
└── tests/                    # Test files
    ├── test_archive_functions.py
    ├── test_tagging.py
    └── test_files/           # Test data directory
```

## Development Roadmap

### Phase 1: Core Functionality (Current)
- Improved file organization
- Unused file detection
- Enhanced archive functionality
- Duplicate file detection

### Phase 2: Advanced Features (Q3 2023)
- File tagging system
- File versioning
- Analytics dashboard
- Advanced search capabilities

### Phase 3: Integration and Extensions (Q4 2023)
- Cloud storage integration
- Plugin system
- Mobile companion app
- Scheduled operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Write docstrings for all functions, classes, and methods
- Add unit tests for new functionality

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Ensure Python 3.6+ is installed and in your PATH
   - Check if Tkinter is installed with your Python distribution

2. **File operations are slow**
   - Large directories may take time to process
   - Consider using more specific directories rather than scanning entire drives

3. **Permission errors**
   - Ensure you have appropriate permissions for the directories you're working with
   - Run the application as administrator if necessary (Windows)

## License

This project is open source and available under the MIT License.

## Acknowledgements

- Thanks to all contributors who have helped improve this project
- Special thanks to the Python and Tkinter communities for their excellent documentation
