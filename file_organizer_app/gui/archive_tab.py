import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

from file_organizer_app.utils.file_operations import (
    archive_files, archive_folder, delete_files, delete_folder,
    create_compressed_archive, create_folder_archive
)

class ArchiveTab:
    def __init__(self, parent):
        """
        Initialize the Archive & Delete tab.

        Args:
            parent: The parent notebook widget
        """
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the Archive & Delete tab."""
        # Source directory selection
        source_frame = ttk.LabelFrame(self.frame, text="Source Directory")
        source_frame.pack(fill=tk.X, padx=10, pady=10)

        self.source_var = tk.StringVar()
        source_entry = ttk.Entry(source_frame, textvariable=self.source_var, width=50)
        source_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        source_browse_btn = ttk.Button(source_frame, text="Browse", command=self.browse_source)
        source_browse_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Archive options frame
        options_frame = ttk.LabelFrame(self.frame, text="Archive Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        # Compression options
        ttk.Label(options_frame, text="Compression:").pack(side=tk.LEFT, padx=5, pady=5)

        self.compression_var = tk.StringVar(value="none")
        compression_none = ttk.Radiobutton(options_frame, text="None", variable=self.compression_var, value="none")
        compression_none.pack(side=tk.LEFT, padx=5, pady=5)

        compression_zip = ttk.Radiobutton(options_frame, text="ZIP", variable=self.compression_var, value="zip")
        compression_zip.pack(side=tk.LEFT, padx=5, pady=5)

        compression_targz = ttk.Radiobutton(options_frame, text="TAR.GZ", variable=self.compression_var, value="tar.gz")
        compression_targz.pack(side=tk.LEFT, padx=5, pady=5)

        # Keep structure option
        self.keep_structure_var = tk.BooleanVar(value=True)
        keep_structure_check = ttk.Checkbutton(options_frame, text="Keep folder structure", variable=self.keep_structure_var)
        keep_structure_check.pack(side=tk.LEFT, padx=20, pady=5)

        # File selection
        file_frame = ttk.LabelFrame(self.frame, text="File Selection")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a treeview for file selection
        columns = ("Name", "Path", "Type", "Size")
        self.file_tree = ttk.Treeview(file_frame, columns=columns, show="headings", selectmode="extended")

        # Configure columns
        self.file_tree.heading("Name", text="Name")
        self.file_tree.heading("Path", text="Path")
        self.file_tree.heading("Type", text="Type")
        self.file_tree.heading("Size", text="Size (KB)")

        self.file_tree.column("Name", width=150)
        self.file_tree.column("Path", width=300)
        self.file_tree.column("Type", width=50)
        self.file_tree.column("Size", width=80)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        x_scrollbar = ttk.Scrollbar(file_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.file_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.file_tree.pack(fill=tk.BOTH, expand=True)

        # Buttons frame
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        load_btn = ttk.Button(buttons_frame, text="Load Files", command=self.load_files)
        load_btn.pack(side=tk.LEFT, padx=5, pady=5)

        archive_files_btn = ttk.Button(buttons_frame, text="Archive Selected Files", command=self.archive_selected_files)
        archive_files_btn.pack(side=tk.LEFT, padx=5, pady=5)

        archive_folder_btn = ttk.Button(buttons_frame, text="Archive Entire Folder", command=self.archive_entire_folder)
        archive_folder_btn.pack(side=tk.LEFT, padx=5, pady=5)

        delete_files_btn = ttk.Button(buttons_frame, text="Delete Selected Files", command=self.delete_selected_files)
        delete_files_btn.pack(side=tk.LEFT, padx=5, pady=5)

        delete_folder_btn = ttk.Button(buttons_frame, text="Delete Entire Folder", command=self.delete_entire_folder)
        delete_folder_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def browse_source(self):
        """Open a directory browser dialog for the source directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.source_var.set(directory)

    def load_files(self):
        """Load files from the source directory into the treeview."""
        source_dir = self.source_var.get()
        if not source_dir:
            messagebox.showerror("Error", "Please select a source directory first.")
            return

        if not os.path.exists(source_dir):
            messagebox.showerror("Error", "The selected source directory does not exist.")
            return

        # Clear previous results
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        self.status_var.set("Loading files...")

        # Run the file loading in a separate thread
        def load_thread():
            try:
                files = []
                for root, _, filenames in os.walk(source_dir):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        file_type = os.path.splitext(filename)[1].lower()
                        file_size = os.path.getsize(file_path) / 1024  # Size in KB
                        files.append((filename, file_path, file_type, file_size))

                # Update the UI in the main thread
                self.frame.after(0, lambda: self.update_file_tree(files))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error loading files."))

        threading.Thread(target=load_thread).start()

    def update_file_tree(self, files):
        """
        Update the file treeview.

        Args:
            files: List of tuples containing file information
        """
        for name, path, file_type, size in files:
            self.file_tree.insert("", tk.END, values=(name, path, file_type, round(size, 2)))

        self.status_var.set(f"Loaded {len(files)} files.")

    def archive_selected_files(self):
        """Archive the selected files."""
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "No files selected.")
            return

        # Get the paths of selected files
        file_paths = [self.file_tree.item(item, "values")[1] for item in selected]

        # Get compression type
        compression_type = self.compression_var.get()

        # Determine archive method and message
        if compression_type == "none":
            archive_method = "copy"
            confirm_msg = f"Archive {len(file_paths)} files in their original locations?"
        else:
            archive_method = f"compress ({compression_type})"
            confirm_msg = f"Create {compression_type} archive of {len(file_paths)} files in their original locations?"

        # Confirm the operation
        if not messagebox.askyesno("Confirm", confirm_msg):
            return

        self.status_var.set(f"Archiving files ({archive_method})...")

        # Run the archive operation in a separate thread
        def archive_thread():
            try:
                if compression_type == "none":
                    success_count, errors = archive_files(file_paths)

                    # Update the UI in the main thread
                    self.frame.after(0, lambda: self.archive_complete(success_count, errors))
                else:
                    # Create compressed archive
                    success, error = create_compressed_archive(file_paths, archive_type=compression_type)

                    # Update the UI in the main thread
                    if success:
                        self.frame.after(0, lambda: self.status_var.set(f"Files archived successfully as {compression_type}."))
                        self.frame.after(0, lambda: messagebox.showinfo("Success", f"Files archived successfully as {compression_type}."))
                    else:
                        self.frame.after(0, lambda: self.status_var.set(f"Error: {error}"))
                        self.frame.after(0, lambda: messagebox.showerror("Error", f"Failed to archive files: {error}"))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error archiving files."))

        threading.Thread(target=archive_thread).start()

    def archive_complete(self, success_count, errors):
        """
        Handle completion of archive operation.

        Args:
            success_count: Number of successfully archived files
            errors: List of error messages
        """
        if errors:
            error_msg = "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more errors."
            messagebox.showwarning("Warning", f"Completed with errors:\n{error_msg}")

        self.status_var.set(f"Archived {success_count} files.")

        # Refresh the file list
        self.load_files()

    def archive_entire_folder(self):
        """Archive the entire source folder."""
        source_dir = self.source_var.get()
        if not source_dir:
            messagebox.showerror("Error", "Please select a source directory first.")
            return

        if not os.path.exists(source_dir):
            messagebox.showerror("Error", "The selected source directory does not exist.")
            return

        # Get compression type
        compression_type = self.compression_var.get()

        # Determine archive method and message
        if compression_type == "none":
            archive_method = "copy"
            confirm_msg = f"Archive the entire folder {source_dir} in its parent directory?"
        else:
            archive_method = f"compress ({compression_type})"
            confirm_msg = f"Create {compression_type} archive of folder {source_dir} in its parent directory?"

        # Confirm the operation
        if not messagebox.askyesno("Confirm", confirm_msg):
            return

        self.status_var.set(f"Archiving folder ({archive_method})...")

        # Run the archive operation in a separate thread
        def archive_thread():
            try:
                if compression_type == "none":
                    success, error = archive_folder(source_dir)
                else:
                    # Create compressed archive
                    success, error = create_folder_archive(source_dir, archive_type=compression_type)

                # Update the UI in the main thread
                if success:
                    self.frame.after(0, lambda: self.status_var.set(f"Folder archived successfully{' as ' + compression_type if compression_type != 'none' else ''}."))
                    self.frame.after(0, lambda: messagebox.showinfo("Success", f"Folder archived successfully{' as ' + compression_type if compression_type != 'none' else ''}."))
                else:
                    self.frame.after(0, lambda: self.status_var.set(f"Error: {error}"))
                    self.frame.after(0, lambda: messagebox.showerror("Error", f"Failed to archive folder: {error}"))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error archiving folder."))

        threading.Thread(target=archive_thread).start()

    def delete_selected_files(self):
        """Delete the selected files."""
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "No files selected.")
            return

        # Get the paths of selected files
        file_paths = [self.file_tree.item(item, "values")[1] for item in selected]

        # Confirm the operation
        if not messagebox.askyesno("Confirm", f"Delete {len(file_paths)} files? This cannot be undone!"):
            return

        self.status_var.set("Deleting files...")

        # Run the delete operation in a separate thread
        def delete_thread():
            try:
                success_count, errors = delete_files(file_paths)

                # Update the UI in the main thread
                self.frame.after(0, lambda: self.delete_complete(success_count, errors))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error deleting files."))

        threading.Thread(target=delete_thread).start()

    def delete_complete(self, success_count, errors):
        """
        Handle completion of delete operation.

        Args:
            success_count: Number of successfully deleted files
            errors: List of error messages
        """
        if errors:
            error_msg = "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more errors."
            messagebox.showwarning("Warning", f"Completed with errors:\n{error_msg}")

        self.status_var.set(f"Deleted {success_count} files.")

        # Refresh the file list
        self.load_files()

    def delete_entire_folder(self):
        """Delete the entire source folder."""
        source_dir = self.source_var.get()
        if not source_dir:
            messagebox.showerror("Error", "Please select a source directory first.")
            return

        if not os.path.exists(source_dir):
            messagebox.showerror("Error", "The selected source directory does not exist.")
            return

        # Confirm the operation
        if not messagebox.askyesno("Confirm", f"Delete the entire folder {source_dir}? This cannot be undone!"):
            return

        # Double-check with a more serious warning
        if not messagebox.askyesno("WARNING", "This will permanently delete all files and subfolders. Are you absolutely sure?"):
            return

        self.status_var.set("Deleting folder...")

        # Run the delete operation in a separate thread
        def delete_thread():
            try:
                success, error = delete_folder(source_dir)

                # Update the UI in the main thread
                if success:
                    self.frame.after(0, lambda: self.status_var.set("Folder deleted successfully."))
                    self.frame.after(0, lambda: messagebox.showinfo("Success", "Folder deleted successfully."))
                else:
                    self.frame.after(0, lambda: self.status_var.set(f"Error: {error}"))
                    self.frame.after(0, lambda: messagebox.showerror("Error", f"Failed to delete folder: {error}"))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error deleting folder."))

        threading.Thread(target=delete_thread).start()
