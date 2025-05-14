import os
import sys
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_organizer_app.utils.file_organizer import organize_files, find_duplicate_files
from file_organizer_app.utils.file_metadata import find_unused_files
from file_organizer_app.utils.file_operations import archive_files, delete_files

def test_organize_files(test_dir):
    """Test the organize_files function."""
    print(f"\n--- Testing organize_files on {test_dir} ---")

    # Check if the directory exists
    if not os.path.exists(test_dir):
        print(f"Error: Directory {test_dir} does not exist.")
        return

    # Get the list of files before organizing
    files_before = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            files_before.append(os.path.join(root, file))

    print(f"Files before organizing: {len(files_before)}")
    for file in files_before:
        print(f"  {file}")

    # Organize the files
    results = organize_files(test_dir)

    # Print the results
    print("\nOrganize results:")
    for ext, count in results.items():
        if count > 0:
            print(f"  {ext}: {count} files moved")

    # Get the list of files after organizing
    files_after = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            files_after.append(os.path.join(root, file))

    print(f"\nFiles after organizing: {len(files_after)}")
    for file in files_after:
        print(f"  {file}")

    # Check if the number of files is the same
    if len(files_before) != len(files_after):
        print(f"Warning: Number of files changed from {len(files_before)} to {len(files_after)}")

    print("\nTest completed.")

def test_find_duplicates(test_dir):
    """Test the find_duplicate_files function."""
    print(f"\n--- Testing find_duplicate_files on {test_dir} ---")

    # Check if the directory exists
    if not os.path.exists(test_dir):
        print(f"Error: Directory {test_dir} does not exist.")
        return

    # Find duplicate files
    duplicates = find_duplicate_files(test_dir)

    # Print the results
    print(f"\nFound {len(duplicates)} duplicate file pairs:")
    for file1, file2 in duplicates:
        print(f"  {file1} and {file2}")

    print("\nTest completed.")

def test_find_unused_files(test_dir, days=1):
    """Test the find_unused_files function."""
    print(f"\n--- Testing find_unused_files on {test_dir} with {days} days threshold ---")

    # Check if the directory exists
    if not os.path.exists(test_dir):
        print(f"Error: Directory {test_dir} does not exist.")
        return

    # Find unused files
    unused_files = find_unused_files(test_dir, days)

    # Print the results
    print(f"\nFound {len(unused_files)} unused files:")
    for file_info in unused_files:
        print(f"  {file_info['path']} (Last accessed: {file_info['accessed']})")

    print("\nTest completed.")

def test_archive_files(test_dir, archive_dir):
    """Test the archive_files function."""
    print(f"\n--- Testing archive_files from {test_dir} to {archive_dir} ---")

    # Check if the directories exist
    if not os.path.exists(test_dir):
        print(f"Error: Directory {test_dir} does not exist.")
        return

    # Create the archive directory if it doesn't exist
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Get a list of files to archive (first 2 files in the test directory)
    files_to_archive = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            files_to_archive.append(os.path.join(root, file))
            if len(files_to_archive) >= 2:
                break
        if len(files_to_archive) >= 2:
            break

    print(f"\nFiles to archive: {len(files_to_archive)}")
    for file in files_to_archive:
        print(f"  {file}")

    # Archive the files
    success_count, errors = archive_files(files_to_archive, archive_dir)

    # Print the results
    print(f"\nArchived {success_count} files.")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  {error}")

    # List files in the archive directory
    print("\nFiles in archive directory:")
    for root, _, files in os.walk(archive_dir):
        for file in files:
            print(f"  {os.path.join(root, file)}")

    print("\nTest completed.")

def test_delete_files(test_dir):
    """Test the delete_files function."""
    print(f"\n--- Testing delete_files on {test_dir} ---")

    # Check if the directory exists
    if not os.path.exists(test_dir):
        print(f"Error: Directory {test_dir} does not exist.")
        return

    # Get a list of files to delete (first file in the test directory)
    files_to_delete = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            files_to_delete.append(os.path.join(root, file))
            if len(files_to_delete) >= 1:
                break
        if len(files_to_delete) >= 1:
            break

    print(f"\nFiles to delete: {len(files_to_delete)}")
    for file in files_to_delete:
        print(f"  {file}")

    # Delete the files
    success_count, errors = delete_files(files_to_delete)

    # Print the results
    print(f"\nDeleted {success_count} files.")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  {error}")

    print("\nTest completed.")

def main():
    """Main function to run the tests."""
    # Define test directories
    test_dir = "d:/software/test_files"
    archive_dir = "d:/software/test_archive"

    # Run the tests
    test_organize_files(test_dir)
    test_find_duplicates(test_dir)
    test_find_unused_files(test_dir)
    test_archive_files(test_dir, archive_dir)
    test_delete_files(test_dir)

if __name__ == "__main__":
    main()
