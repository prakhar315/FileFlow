import os
import datetime
import hashlib
import shutil
from typing import List, Tuple, Dict, Optional

# Function to organize a single file
def organize_file(file_path: str, dir_path: str) -> Tuple[bool, Optional[str]]:
    """
    Organizes a single file by moving it to the appropriate folder based on its extension.

    Args:
        file_path: Path to the file to organize
        dir_path: Base directory for organizing

    Returns:
        Tuple containing success status and file extension if successful
    """
    # Define common file extensions and their corresponding folders
    extensions = {
        '.pdf': 'pdf_only',
        '.jpg': 'jpg_only',
        '.png': 'png_only',
        '.jpeg': 'jpeg_only',
        '.docx': 'docx_only',
        '.pptx': 'pptx_only',
        '.doc': 'doc_only',
        '.txt': 'txt_only',
        '.xlsx': 'xlsx_only',
        '.zip': 'zip_only',
        '.mp3': 'mp3_only',
        '.mp4': 'mp4_only',
        '.exe': 'exe_only',
        '.dll': 'dll_only',
        '.html': 'html_only',
        '.css': 'css_only',
        '.js': 'js_only',
        '.py': 'py_only',
        '.java': 'java_only',
        '.c': 'c_only',
        '.cpp': 'cpp_only',
        '.h': 'h_only',
        '.json': 'json_only',
        '.xml': 'xml_only',
        '.csv': 'csv_only'
    }

    try:
        # Get file extension
        file_ext = os.path.splitext(file_path)[-1].lower()

        # Check if we handle this extension
        if file_ext not in extensions:
            return False, None

        # Create destination folder if it doesn't exist
        folder = extensions[file_ext]
        destination_folder_path = os.path.join(dir_path, folder)
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

        # Get filename
        filename = os.path.basename(file_path)
        dest_path = os.path.join(destination_folder_path, filename)

        # Check if destination file already exists
        if os.path.exists(dest_path):
            # Add a timestamp to make the filename unique
            name, ext = os.path.splitext(filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_filename = f"{name}_{timestamp}{ext}"
            dest_path = os.path.join(destination_folder_path, new_filename)

        # Move the file
        os.rename(file_path, dest_path)
        return True, file_ext
    except Exception as e:
        print(f"Error organizing {file_path}: {e}")
        return False, None

# Function to organize the files into folders
def organize_files(dir_path: str) -> Dict[str, int]:
    """
    Organizes files in the given directory into folders based on file extension.
    Only creates folders for file types that are present in the directory.

    Args:
        dir_path: Path to the directory containing files to organize

    Returns:
        Dictionary with file types as keys and count of files moved as values
    """
    # Define common file extensions and their corresponding folders
    extensions = {
        '.pdf': 'pdf_only',
        '.jpg': 'jpg_only',
        '.png': 'png_only',
        '.jpeg': 'jpeg_only',
        '.docx': 'docx_only',
        '.pptx': 'pptx_only',
        '.doc': 'doc_only',
        '.txt': 'txt_only',
        '.xlsx': 'xlsx_only',
        '.zip': 'zip_only',
        '.mp3': 'mp3_only',
        '.mp4': 'mp4_only',
        '.exe': 'exe_only',
        '.dll': 'dll_only',
        '.html': 'html_only',
        '.css': 'css_only',
        '.js': 'js_only',
        '.py': 'py_only',
        '.java': 'java_only',
        '.c': 'c_only',
        '.cpp': 'cpp_only',
        '.h': 'h_only',
        '.json': 'json_only',
        '.xml': 'xml_only',
        '.csv': 'csv_only'
    }

    # First scan to find which file types are actually present
    present_extensions = set()
    for root, _, file_names in os.walk(dir_path):
        # Skip folders that might already be organized
        if any(folder in root for folder in extensions.values()):
            continue

        for file in file_names:
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext in extensions:
                present_extensions.add(file_ext)

    # Create folders only for file types that are present
    for ext in present_extensions:
        folder = extensions[ext]
        destination_folder_path = os.path.join(dir_path, folder)
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

    # Dictionary to track number of files moved by type
    files_moved = {ext: 0 for ext in extensions.keys()}

    # Walk through directory and organize files
    for root, _, file_names in os.walk(dir_path):
        # Skip the destination folders to avoid moving already organized files
        if any(folder in root for folder in extensions.values()):
            continue

        for file in file_names:
            file_ext = os.path.splitext(file)[-1].lower()
            if file_ext in extensions:
                source_path = os.path.join(root, file)
                dest_folder = os.path.join(dir_path, extensions[file_ext])
                dest_path = os.path.join(dest_folder, file)

                # Check if destination file already exists
                if os.path.exists(dest_path):
                    # Add a timestamp to make the filename unique
                    filename, ext = os.path.splitext(file)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    new_filename = f"{filename}_{timestamp}{ext}"
                    dest_path = os.path.join(dest_folder, new_filename)

                try:
                    os.rename(source_path, dest_path)
                    files_moved[file_ext] += 1
                except Exception as e:
                    print(f"Error moving {file}: {e}")

    return files_moved

# Function to get file hash
def get_file_hash(filepath: str) -> str:
    """
    Calculates MD5 hash of a file.

    Args:
        filepath: Path to the file

    Returns:
        MD5 hash of the file as a hexadecimal string
    """
    hasher = hashlib.md5()

    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to find duplicate files
def find_duplicate_files(path: str) -> List[Tuple[str, str]]:
    """
    Finds duplicate files in the given directory.

    Args:
        path: Path to the directory to search for duplicates

    Returns:
        List of tuples containing paths of duplicate files
    """
    seen_hash = {}
    duplicates = []

    for root, _, files in os.walk(path):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                file_hash = get_file_hash(filepath)

                if file_hash in seen_hash:
                    duplicates.append((filepath, seen_hash[file_hash]))
                else:
                    seen_hash[file_hash] = filepath
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    return duplicates
