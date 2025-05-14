# File Organizer Pro

A powerful Python desktop application for organizing, managing, and analyzing your files with advanced features.

## Current Features

1. **Organize Files**: Automatically organize files into folders based on their file types (only creates folders for file types that are actually present).
2. **Find Unused Files**: Identify files that haven't been accessed for a specified period with fast client-side filtering.
3. **Archive Files**: Archive files and folders in their original locations with automatic timestamp-based naming and compression options (ZIP, TAR.GZ).
4. **Delete Files**: Safely delete files and folders with confirmation dialogs.

## Upcoming Features

The application is being enhanced with the following advanced features:

### Advanced File Management
- **File Tagging System**: Tag files with custom categories for better organization
- **File Versioning**: Track changes to files and restore previous versions
- **Smart Organization**: Machine learning-based file categorization that learns from user behavior

### Enhanced Search and Discovery
- **Full-Text Search**: Search within file contents across multiple file formats
- **Advanced Filters**: Complex search queries with multiple criteria
- **File Analytics Dashboard**: Visualize storage usage by file type, age, and size

### Automation and Scheduling
- **Scheduled Tasks**: Set up recurring file organization tasks
- **File Organization Rules**: Create custom rules for automatic file handling
- **Batch Processing**: Process multiple files with custom operations

### Integration and Connectivity
- **Cloud Storage Integration**: Connect to popular cloud services
- **External Device Management**: Detect and manage external drives
- **API and Plugin System**: Extend functionality with plugins

### Security and Privacy
- **File Encryption**: Encrypt sensitive files and folders
- **Privacy Scanner**: Identify files with sensitive information
- **Secure Deletion**: Military-grade file shredding

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

- `main.py`: Entry point for the application
- `utils/`: Utility functions for file operations
  - `file_operations.py`: Functions for archiving and deleting files
  - `file_metadata.py`: Functions for retrieving and analyzing file metadata
- `gui/`: GUI components
  - `main_window.py`: Main application window
  - `organize_tab.py`: File organization tab
  - `unused_files_tab.py`: Unused files tab
  - `archive_tab.py`: Archive and delete tab

## Development Roadmap

### Phase 1: Core Functionality (Current)
- Improved file organization
- Unused file detection
- Enhanced archive functionality

### Phase 2: Advanced Features
- File tagging system
- File versioning
- Analytics dashboard

### Phase 3: Integration and Extensions
- Cloud storage integration
- Plugin system
- Mobile companion app

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
