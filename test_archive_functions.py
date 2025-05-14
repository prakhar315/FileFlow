import os
import sys
import shutil
from pathlib import Path

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

# Import the archive functions
from file_organizer_app.utils.file_operations import (
    archive_files, archive_folder, 
    create_compressed_archive, create_folder_archive
)

def setup_test_environment():
    """Create a test directory with some files."""
    # Create test directory structure
    test_dir = Path("test_archive_dir")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    (test_dir / "subfolder").mkdir()
    
    # Create test files
    (test_dir / "file1.txt").write_text("Test file 1")
    (test_dir / "file2.txt").write_text("Test file 2")
    (test_dir / "subfolder" / "file3.txt").write_text("Test file 3")
    
    return test_dir

def test_archive_files():
    """Test archiving files in their original location."""
    print("\n=== Testing archive_files ===")
    
    # Get file paths
    test_dir = Path("test_archive_dir")
    file_paths = [
        str(test_dir / "file1.txt"),
        str(test_dir / "file2.txt")
    ]
    
    # Archive files
    print(f"Archiving files: {file_paths}")
    success_count, errors = archive_files(file_paths)
    
    # Print results
    print(f"Successfully archived {success_count} files")
    if errors:
        print(f"Errors: {errors}")
    
    # List files in directory
    print("\nFiles in directory after archiving:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_archive_folder():
    """Test archiving a folder in its parent directory."""
    print("\n=== Testing archive_folder ===")
    
    # Get folder path
    test_dir = Path("test_archive_dir")
    subfolder_path = str(test_dir / "subfolder")
    
    # Archive folder
    print(f"Archiving folder: {subfolder_path}")
    success, error = archive_folder(subfolder_path)
    
    # Print results
    if success:
        print("Successfully archived folder")
    else:
        print(f"Error: {error}")
    
    # List files in directory
    print("\nFiles in directory after archiving:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_compressed_archive_files():
    """Test creating a compressed archive of files."""
    print("\n=== Testing create_compressed_archive ===")
    
    # Get file paths
    test_dir = Path("test_archive_dir")
    file_paths = [
        str(test_dir / "file1.txt"),
        str(test_dir / "file2.txt")
    ]
    
    # Create compressed archive
    print(f"Creating ZIP archive of files: {file_paths}")
    success, error = create_compressed_archive(file_paths, archive_type="zip")
    
    # Print results
    if success:
        print("Successfully created ZIP archive")
    else:
        print(f"Error: {error}")
    
    # List files in directory
    print("\nFiles in directory after creating archive:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def test_compressed_archive_folder():
    """Test creating a compressed archive of a folder."""
    print("\n=== Testing create_folder_archive ===")
    
    # Get folder path
    test_dir = Path("test_archive_dir")
    subfolder_path = str(test_dir / "subfolder")
    
    # Create compressed archive
    print(f"Creating TAR.GZ archive of folder: {subfolder_path}")
    success, error = create_folder_archive(subfolder_path, archive_type="tar.gz")
    
    # Print results
    if success:
        print("Successfully created TAR.GZ archive")
    else:
        print(f"Error: {error}")
    
    # List files in directory
    print("\nFiles in directory after creating archive:")
    for file in test_dir.glob("*"):
        print(f"  {file.name}")

def main():
    """Run all tests."""
    # Setup test environment
    test_dir = setup_test_environment()
    print(f"Created test directory: {test_dir}")
    
    # Run tests
    test_archive_files()
    test_archive_folder()
    test_compressed_archive_files()
    test_compressed_archive_folder()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
