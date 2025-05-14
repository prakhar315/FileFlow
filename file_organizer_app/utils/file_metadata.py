import os
import datetime
from typing import Dict, List, Tuple, Optional

def get_file_metadata(file_path: str) -> Dict[str, any]:
    """
    Gets metadata for a file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary containing file metadata
    """
    try:
        stats = os.stat(file_path)

        created_datetime = datetime.datetime.fromtimestamp(stats.st_ctime)
        modified_datetime = datetime.datetime.fromtimestamp(stats.st_mtime)
        accessed_datetime = datetime.datetime.fromtimestamp(stats.st_atime)

        return {
            "path": file_path,
            "name": os.path.basename(file_path),
            "size": stats.st_size,
            "created": created_datetime,
            "modified": modified_datetime,
            "accessed": accessed_datetime,
            "extension": os.path.splitext(file_path)[1].lower()
        }
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return {}

def find_unused_files(dir_path: str, days: int = 90) -> List[Dict[str, any]]:
    """
    Finds files that haven't been accessed in the specified number of days.
    Optimized for faster performance.

    Args:
        dir_path: Path to the directory to search
        days: Number of days to consider a file unused

    Returns:
        List of dictionaries containing metadata of unused files
    """
    unused_files = []
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)

    # Use a more efficient approach by processing files in batches
    batch_size = 100
    all_files = []

    # First, collect all file paths (faster than processing one by one)
    for root, _, files in os.walk(dir_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    # Process files in batches
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i+batch_size]
        for file_path in batch:
            try:
                stats = os.stat(file_path)
                accessed_datetime = datetime.datetime.fromtimestamp(stats.st_atime)

                # Quick check if the file is unused before getting full metadata
                if accessed_datetime < cutoff_date:
                    metadata = get_file_metadata(file_path)
                    if metadata:
                        unused_files.append(metadata)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return unused_files

def print_metadata(dir_path: str) -> None:
    """
    Prints metadata for all files in the directory.

    Args:
        dir_path: Path to the directory
    """
    for root, _, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = get_file_metadata(file_path)

            if metadata:
                print(f"\nFile: {metadata['path']}")
                print(f"Size: {metadata['size']} bytes")
                print(f"Created: {metadata['created']}")
                print(f"Modified: {metadata['modified']}")
                print(f"Accessed: {metadata['accessed']}")
