# File Organizer Desktop Application

A Python desktop application for organizing, managing, and cleaning up files.

## Features

1. **Organize Files**: Automatically organize files into folders based on their file types (only creates folders for file types that are actually present).
2. **Find Unused Files**: Identify files that haven't been accessed for a specified period with fast client-side filtering.
3. **Archive Files**: Copy files to an archive location for safekeeping with automatic timestamp-based naming.
4. **Delete Files**: Safely delete files and folders with confirmation dialogs.

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

## Installation

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

## Usage

### Organize Files Tab

- Select a directory using the "Browse" button.
- Click "Organize Files" to sort files into folders by type.
- Click "Find Duplicates" to identify duplicate files in the directory.

### Unused Files Tab

- Select a directory using the "Browse" button.
- Set the number of days to consider a file "unused".
- Optionally filter by file type.
- Click "Find Unused Files" to display files that haven't been accessed.
- Right-click on files for additional options.

### Archive & Delete Tab

- Select a source directory containing files to manage.
- Select an archive directory where files will be moved.
- Click "Load Files" to display files in the source directory.
- Select files and use the buttons to archive or delete them.
- Use the "Archive Entire Folder" or "Delete Entire Folder" buttons to process the whole directory.

## Project Structure

- `run_file_organizer.py`: Launcher script for the application
- `run_file_organizer.bat`: Batch file for easy launching on Windows
- `file_organizer_app/`: Main package
  - `main.py`: Entry point for the application
  - `utils/`: Utility functions for file operations
    - `file_organizer.py`: Functions for organizing files and finding duplicates
    - `file_metadata.py`: Functions for retrieving and analyzing file metadata
    - `file_operations.py`: Functions for archiving and deleting files
  - `gui/`: GUI components
    - `main_window.py`: Main application window
    - `organize_tab.py`: File organization tab
    - `unused_files_tab.py`: Unused files tab
    - `archive_tab.py`: Archive and delete tab

## License

This project is open source and available under the MIT License.
