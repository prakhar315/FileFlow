import os
import shutil
import datetime
import zipfile
import tarfile
from typing import List, Tuple, Optional

def archive_files(file_paths: List[str], archive_dir: str = None) -> Tuple[int, List[str]]:
    """
    Archives files by moving them to an archive directory.

    Args:
        file_paths: List of file paths to archive
        archive_dir: Directory to move files to (if None, uses the source file's directory)

    Returns:
        Tuple containing count of successfully archived files and list of errors
    """
    success_count = 0
    errors = []

    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                # Get the filename and directory
                filename = os.path.basename(file_path)
                source_dir = os.path.dirname(file_path)

                # Use source directory if archive_dir is None
                dest_dir = archive_dir if archive_dir else source_dir

                # Create the destination directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                # Create a timestamp to avoid conflicts
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                name, ext = os.path.splitext(filename)
                unique_filename = f"{name}_{timestamp}{ext}"

                # Create the destination path
                dest_path = os.path.join(dest_dir, unique_filename)

                # Copy the file to the archive (instead of moving to avoid errors)
                shutil.copy2(file_path, dest_path)
                success_count += 1
            else:
                errors.append(f"File not found: {file_path}")
        except Exception as e:
            errors.append(f"Error archiving {file_path}: {str(e)}")

    return success_count, errors

def archive_folder(folder_path: str, archive_dir: str = None) -> Tuple[bool, Optional[str]]:
    """
    Archives an entire folder by copying it to an archive directory.

    Args:
        folder_path: Path to the folder to archive
        archive_dir: Directory to copy the folder to (if None, uses the parent directory of the folder)

    Returns:
        Tuple containing success status and error message if any
    """
    try:
        if os.path.exists(folder_path):
            # Get the folder name and parent directory
            folder_name = os.path.basename(folder_path)
            parent_dir = os.path.dirname(folder_path)

            # Use parent directory if archive_dir is None
            dest_dir = archive_dir if archive_dir else parent_dir

            # Create the destination directory if it doesn't exist
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            # Create a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            # Create the destination path with timestamp to avoid conflicts
            dest_path = os.path.join(dest_dir, f"{folder_name}_{timestamp}")

            # Copy the folder to the archive (instead of moving to avoid errors)
            shutil.copytree(folder_path, dest_path)
            return True, None
        else:
            return False, f"Folder not found: {folder_path}"
    except Exception as e:
        return False, f"Error archiving folder {folder_path}: {str(e)}"

def delete_files(file_paths: List[str]) -> Tuple[int, List[str]]:
    """
    Deletes files.

    Args:
        file_paths: List of file paths to delete

    Returns:
        Tuple containing count of successfully deleted files and list of errors
    """
    success_count = 0
    errors = []

    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                success_count += 1
            else:
                errors.append(f"File not found: {file_path}")
        except Exception as e:
            errors.append(f"Error deleting {file_path}: {str(e)}")

    return success_count, errors

def delete_folder(folder_path: str) -> Tuple[bool, Optional[str]]:
    """
    Deletes a folder and all its contents.

    Args:
        folder_path: Path to the folder to delete

    Returns:
        Tuple containing success status and error message if any
    """
    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            return True, None
        else:
            return False, f"Folder not found: {folder_path}"
    except Exception as e:
        return False, f"Error deleting folder {folder_path}: {str(e)}"

def create_compressed_archive(file_paths: List[str], archive_path: str = None, archive_type: str = 'zip') -> Tuple[bool, Optional[str]]:
    """
    Creates a compressed archive of the specified files.

    Args:
        file_paths: List of file paths to include in the archive
        archive_path: Path where the archive will be created (if None, uses the directory of the first file)
        archive_type: Type of archive ('zip' or 'tar.gz')

    Returns:
        Tuple containing success status and error message if any
    """
    try:
        if not file_paths:
            return False, "No files provided for archiving"

        # If archive_path is None, create one based on the first file's location
        if archive_path is None:
            first_file = file_paths[0]
            first_file_dir = os.path.dirname(first_file)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            if archive_type == 'zip':
                archive_path = os.path.join(first_file_dir, f"archive_{timestamp}.zip")
            elif archive_type == 'tar.gz':
                archive_path = os.path.join(first_file_dir, f"archive_{timestamp}.tar.gz")
            else:
                return False, f"Unsupported archive type: {archive_type}"

        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)

        if archive_type == 'zip':
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        # Add file to zip with relative path
                        arcname = os.path.basename(file_path)
                        zipf.write(file_path, arcname)
            return True, None

        elif archive_type == 'tar.gz':
            with tarfile.open(archive_path, 'w:gz') as tarf:
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        # Add file to tar with relative path
                        arcname = os.path.basename(file_path)
                        tarf.add(file_path, arcname=arcname)
            return True, None

        else:
            return False, f"Unsupported archive type: {archive_type}"

    except Exception as e:
        return False, f"Error creating archive: {str(e)}"

def create_folder_archive(folder_path: str, archive_path: str = None, archive_type: str = 'zip') -> Tuple[bool, Optional[str]]:
    """
    Creates a compressed archive of an entire folder.

    Args:
        folder_path: Path to the folder to archive
        archive_path: Path where the archive will be created (if None, uses the parent directory of the folder)
        archive_type: Type of archive ('zip' or 'tar.gz')

    Returns:
        Tuple containing success status and error message if any
    """
    try:
        if not os.path.exists(folder_path):
            return False, f"Folder not found: {folder_path}"

        folder_name = os.path.basename(folder_path)

        # If archive_path is None, create one based on the folder's parent directory
        if archive_path is None:
            parent_dir = os.path.dirname(folder_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            if archive_type == 'zip':
                archive_path = os.path.join(parent_dir, f"{folder_name}_{timestamp}.zip")
            elif archive_type == 'tar.gz':
                archive_path = os.path.join(parent_dir, f"{folder_name}_{timestamp}.tar.gz")
            else:
                return False, f"Unsupported archive type: {archive_type}"

        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)

        if archive_type == 'zip':
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate path inside the zip file
                        rel_path = os.path.relpath(file_path, os.path.dirname(folder_path))
                        zipf.write(file_path, rel_path)
            return True, None

        elif archive_type == 'tar.gz':
            with tarfile.open(archive_path, 'w:gz') as tarf:
                # Add the folder to the archive with its base name
                tarf.add(folder_path, arcname=folder_name)
            return True, None

        else:
            return False, f"Unsupported archive type: {archive_type}"

    except Exception as e:
        return False, f"Error creating folder archive: {str(e)}"
