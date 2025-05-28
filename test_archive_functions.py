import os
import sys
import shutil
from pathlib import Path

# Add the parent directory to the path to allow importing from the main package
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

# Import the archive functions from the main application package
from file_organizer_app.utils.file_operations import (
    archive_files, archive_folder, 
    create_compressed_archive, create_folder_archive
)

def setup_test_environment():
    """
    Create a test directory with sample files for testing archive functions.
    
    This function:
    1. Creates a clean test directory structure
    2. Creates sample text files in the main directory and subfolder
    
    Returns:
        Path: Path object pointing to the created test directory
    """
    # Create test directory structure (remove if it already exists)
    test_dir = Path("test_archive_dir")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    # Create fresh main directory and subfolder
    test_dir.mkdir()
    (test_dir / "subfolder").mkdir()
    
    # Create sample test files with content
    (test_dir / "file1.txt").write_text("Test file 1")
    (test_dir / "file2.txt").write_text("Test file 2")
    (test_dir / "subfolder" / "file3.txt").write_text("Test file 3")
    
    return test_dir

def test_archive_files():
    """
    Test the archive_files function which creates timestamped copies of files.
    
    This test:
    1. Gets paths to test files
    2. Calls archive_files to create timestamped copies in the same location
    3. Prints results and lists files in the directory after archiving
    """
    print("\n=== Testing archive_files ===")
    
    # Get paths to the test files we want to archive
    test_dir = Path("test_archive_dir")
    file_paths = [
        str(test_dir / "file1.txt"),
        str(test_dir / "file2.txt")
    ]
    
    # Call the archive_files function (creates timestamped copies in the same location)
    print(f"Archiving files: {file_paths}")
    success_count, errors = archive_files(file_paths)
    
    # Print the results of the archive operation
    print(f"Successfully archived {success_count} files")
    if errors:
        print(f"Errors: {errors}")
    
    # List all files in the directory after archiving to verify results
    print("\nFiles in directory after archiving:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_archive_folder():
    """
    Test the archive_folder function which creates a timestamped copy of a folder.
    
    This test:
    1. Gets path to the subfolder
    2. Calls archive_folder to create a timestamped copy in the parent directory
    3. Prints results and lists files/folders in the directory after archiving
    """
    print("\n=== Testing archive_folder ===")
    
    # Get path to the subfolder we want to archive
    test_dir = Path("test_archive_dir")
    subfolder_path = str(test_dir / "subfolder")
    
    # Call the archive_folder function (creates timestamped copy in parent directory)
    print(f"Archiving folder: {subfolder_path}")
    success, error = archive_folder(subfolder_path)
    
    # Print the results of the archive operation
    if success:
        print("Successfully archived folder")
    else:
        print(f"Error: {error}")
    
    # List all files and folders in the directory after archiving to verify results
    print("\nFiles in directory after archiving:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_compressed_archive_files():
    """
    Test the create_compressed_archive function which creates a ZIP archive of files.
    
    This test:
    1. Gets paths to test files
    2. Calls create_compressed_archive to create a ZIP file containing the files
    3. Prints results and lists files in the directory after creating the archive
    """
    print("\n=== Testing create_compressed_archive ===")
    
    # Get paths to the test files we want to include in the archive
    test_dir = Path("test_archive_dir")
    file_paths = [
        str(test_dir / "file1.txt"),
        str(test_dir / "file2.txt")
    ]
    
    # Create a ZIP archive containing the specified files
    print(f"Creating ZIP archive of files: {file_paths}")
    success, error = create_compressed_archive(file_paths, archive_type="zip")
    
    # Print the results of the archive operation
    if success:
        print("Successfully created ZIP archive")
    else:
        print(f"Error: {error}")
    
    # List all files in the directory after creating the archive to verify results
    print("\nFiles in directory after creating archive:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_compressed_archive_folder():
    """
    Test the create_folder_archive function which creates a TAR.GZ archive of a folder.
    
    This test:
    1. Gets path to the subfolder
    2. Calls create_folder_archive to create a TAR.GZ archive of the folder
    3. Prints results and lists files in the directory after creating the archive
    """
    print("\n=== Testing create_folder_archive ===")
    
    # Get path to the subfolder we want to archive
    test_dir = Path("test_archive_dir")
    subfolder_path = str(test_dir / "subfolder")
    
    # Create a TAR.GZ archive of the specified folder
    print(f"Creating TAR.GZ archive of folder: {subfolder_path}")
    success, error = create_folder_archive(subfolder_path, archive_type="tar.gz")
    
    # Print the results of the archive operation
    if success:
        print("Successfully created TAR.GZ archive")
    else:
        print(f"Error: {error}")
    
    # List all files in the directory after creating the archive to verify results
    print("\nFiles in directory after creating archive:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def main():
    """
    Main function that runs all the archive function tests in sequence.
    
    This function:
    1. Sets up the test environment with sample files
    2. Runs each test function in sequence
    3. Prints a completion message when all tests are done
    """
    # Setup test environment with sample files and directories
    test_dir = setup_test_environment()
    print(f"Created test directory: {test_dir}")
    
    # Run each test function in sequence
    test_archive_files()
    test_archive_folder()
    test_compressed_archive_files()
    test_compressed_archive_folder()
    
    # Print completion message
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
