import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import hashlib

# Import the `organize_file` function from the `file_organizer` module.  
# This function is responsible for organizing files based on their types  
# or extensions to maintain a clean and structured directory layout.
from file_organizer_app.utils.file_organizer import organize_file

class OrganizeTab:
    def __init__(self, parent):
        """
        Initialize the Organize Files tab.

        Args:
            parent: The parent notebook widget
        """
        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the Organize Files tab."""
        # Directory selection
        dir_frame = ttk.LabelFrame(self.frame, text="Directory Selection")
        dir_frame.pack(fill=tk.X, padx=10, pady=10)

        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Actions frame
        actions_frame = ttk.LabelFrame(self.frame, text="Actions")
        actions_frame.pack(fill=tk.X, padx=10, pady=10)

        organize_btn = ttk.Button(actions_frame, text="Organize Files", command=self.organize_files)
        organize_btn.pack(side=tk.LEFT, padx=5, pady=5)

        find_duplicates_btn = ttk.Button(actions_frame, text="Find Duplicates", command=self.find_duplicates)
        find_duplicates_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Results frame
        results_frame = ttk.LabelFrame(self.frame, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a notebook for results
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Organize results tab
        self.organize_results_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.organize_results_frame, text="Organize Results")

        # Create a treeview for organize results
        self.organize_tree = ttk.Treeview(self.organize_results_frame, columns=("Type", "Count"), show="headings")
        self.organize_tree.heading("Type", text="File Type")
        self.organize_tree.heading("Count", text="Files Moved")
        self.organize_tree.column("Type", width=150)
        self.organize_tree.column("Count", width=100)
        self.organize_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add scrollbar to organize tree
        organize_scrollbar = ttk.Scrollbar(self.organize_results_frame, orient=tk.VERTICAL, command=self.organize_tree.yview)
        organize_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.organize_tree.configure(yscrollcommand=organize_scrollbar.set)

        # Duplicates results tab
        self.duplicates_frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(self.duplicates_frame, text="Duplicate Files")

       # Define the width of the first column to 350 pixels  
       # for consistent layout and better readability.
        self.duplicates_tree = ttk.Treeview(self.duplicates_frame, columns=("File1", "File2"), show="headings")

        # Set the heading text for the first column to "File 1"  
        # to indicate the path or name of the first duplicate file.
        self.duplicates_tree.heading("File1", text="File 1")
       
        # Set the heading text for the second column to "File 2"  
        # to represent the second duplicate file in each pair. 
        self.duplicates_tree.heading("File2", text="File 2")
        
        # Define the width of the first column to 350 pixels  
        # for consistent layout and better readability.
        self.duplicates_tree.column("File1", width=350)
        
        
       # Define the width of the second column to 350 pixels  
       # to match the first column and maintain symmetry. self.duplicates_tree.column("File2", width=350)
        self.duplicates_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add scrollbar to duplicates tree
        duplicates_scrollbar = ttk.Scrollbar(self.duplicates_frame, orient=tk.VERTICAL, command=self.duplicates_tree.yview)
        duplicates_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.duplicates_tree.configure(yscrollcommand=duplicates_scrollbar.set)

       # Create a new frame to contain the progress bar widget  
       # This frame is placed inside the main frame of the application  
       # and helps organize the layout by grouping related widgets together.
        progress_frame = ttk.Frame(self.frame)
       
       # Pack the progress frame at the bottom of the main frame  
       # Make it stretch horizontally to fill the entire width of the window  
       # Add padding on the x and y axes for spacing around the frame.
       progress_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

       # Create a DoubleVar to track the progress value dynamically  
       # This variable will store a floating-point number between 0 and 100  
       # which will control the progress bar's fill level as a percentage.        
       self.progress_var = tk.DoubleVar()
        
       # Create a progress bar widget inside the progress frame  
       # Link it to the progress_var so the progress bar updates automatically  
       # Set the maximum value to 100 to represent 100% progress.
       self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        
       # Pack the progress bar at the top of the progress frame  
       # Make it expand horizontally to fill the entire width available  
       # Add padding to separate it from other widgets and the frame borders.
       self.progress_bar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        # Create a Tkinter StringVar to hold the status message text  
        # This variable will be dynamically updated to reflect the current status  
        # and allows the label text to change automatically when the variable updates.
        self.status_var = tk.StringVar()
       
       # Initialize the status variable with the default text "Ready"  
       # indicating that the application is idle and ready for user interaction  
       # before any processing or tasks have started.
        self.status_var.set("Ready")
       
       # Create a Label widget inside the progress frame to display status messages  
       # Bind the label's text to the StringVar so it updates automatically  
       # Use a sunken relief and left-align the text for a classic status bar appearance.
        status_label = ttk.Label(progress_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
       
       # Pack the status label widget at the bottom of the frame  
       # Allow it to stretch horizontally to fill the entire width  
       # so the status message is clearly visible and aligned at the bottom.        
       status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_directory(self):
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)

    def organize_files(self):
        """Organize files in the selected directory."""
        directory = self.dir_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        if not os.path.exists(directory):
            messagebox.showerror("Error", "The selected directory does not exist.")
            return

        # Clear previous results
        for item in self.organize_tree.get_children():
            self.organize_tree.delete(item)

        # Reset progress bar
        self.progress_var.set(0)
        self.status_var.set("Scanning directory...")

        # Run the organize operation in a separate thread
        def organize_thread():
            try:
                # First, count total files to organize for progress tracking
                total_files = 0
                file_list = []

                # Update status
                self.frame.after(0, lambda: self.status_var.set("Counting files..."))

                for root, _, files in os.walk(directory):
                    # Skip folders that might already be organized
                    if any(folder in root for folder in ["_only"]):
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_ext = os.path.splitext(file)[-1].lower()
                        file_list.append((file_path, file_ext))
                        total_files += 1

                if total_files == 0:
                    self.frame.after(0, lambda: self.status_var.set("No files to organize."))
                    self.frame.after(0, lambda: self.progress_var.set(100))
                    return

                # Update status
                self.frame.after(0, lambda: self.status_var.set(f"Organizing {total_files} files..."))

                # Organize files with progress updates
                results = {}
                processed = 0

                for file_path, file_ext in file_list:
                    # Call organize_file function (we'll need to modify file_organizer.py)
                    success, ext = organize_file(file_path, directory)

                    # Update results
                    if success and ext:
                        if ext not in results:
                            results[ext] = 0
                        results[ext] += 1

                    # Update progress
                    processed += 1
                    progress = (processed / total_files) * 100
                    self.frame.after(0, lambda p=progress: self.progress_var.set(p))

                    # Update status periodically
                    if processed % 10 == 0 or processed == total_files:
                        self.frame.after(0, lambda p=processed, t=total_files:
                                        self.status_var.set(f"Organized {p}/{t} files..."))

                # Update the UI in the main thread
                self.frame.after(0, lambda: self.update_organize_results(results))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error organizing files."))
                self.frame.after(0, lambda: self.progress_var.set(0))

        threading.Thread(target=organize_thread).start()

    def update_organize_results(self, results):
        """
        Update the organize results treeview.

        Args:
            results: Dictionary with file types as keys and count of files moved as values
        """
        for file_type, count in results.items():
            if count > 0:
                self.organize_tree.insert("", tk.END, values=(file_type, count))

        total_files = sum(results.values())

        # Ensure progress bar is at 100%
        self.progress_var.set(100)

        # Update status
        if total_files > 0:
            self.status_var.set(f"Successfully organized {total_files} files.")
        else:
            self.status_var.set("No files were organized.")

        # Switch to the organize results tab
        self.results_notebook.select(0)

    def find_duplicates(self):
        """Find duplicate files in the selected directory."""
        directory = self.dir_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        if not os.path.exists(directory):
            messagebox.showerror("Error", "The selected directory does not exist.")
            return

        # Clear previous results
        for item in self.duplicates_tree.get_children():
            self.duplicates_tree.delete(item)

        # Reset progress bar
        self.progress_var.set(0)
        self.status_var.set("Scanning for duplicate files...")

        # Run the duplicate finding operation in a separate thread
        def duplicates_thread():
            try:
                # First, count total files for progress tracking
                total_files = 0
                file_list = []

                # Update status
                self.frame.after(0, lambda: self.status_var.set("Counting files..."))

                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_list.append(file_path)
                        total_files += 1

                if total_files == 0:
                    self.frame.after(0, lambda: self.status_var.set("No files found to check for duplicates."))
                    self.frame.after(0, lambda: self.progress_var.set(100))
                    return

                # Update status
                self.frame.after(0, lambda: self.status_var.set(f"Checking {total_files} files for duplicates..."))

                # Calculate hashes with progress updates
                seen_hash = {}
                duplicates = []
                processed = 0

                for file_path in file_list:
                    try:
                        # Calculate file hash
                        file_hash = self.calculate_file_hash(file_path)

                        # Check for duplicates
                        if file_hash in seen_hash:
                            duplicates.append((file_path, seen_hash[file_hash]))
                        else:
                            seen_hash[file_hash] = file_path
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

                    # Update progress
                    processed += 1
                    progress = (processed / total_files) * 100
                    self.frame.after(0, lambda p=progress: self.progress_var.set(p))

                    # Update status periodically
                    if processed % 10 == 0 or processed == total_files:
                        self.frame.after(0, lambda p=processed, t=total_files:
                                        self.status_var.set(f"Processed {p}/{t} files..."))

                # Update the UI in the main thread
                self.frame.after(0, lambda: self.update_duplicates_results(duplicates))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error finding duplicates."))
                self.frame.after(0, lambda: self.progress_var.set(0))

        threading.Thread(target=duplicates_thread).start()

    def calculate_file_hash(self, filepath: str) -> str:
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

    def update_duplicates_results(self, duplicates):
        """
        Update the duplicates results treeview.

        Args:
            duplicates: List of tuples containing paths of duplicate files
        """
        for file1, file2 in duplicates:
            self.duplicates_tree.insert("", tk.END, values=(file1, file2))

        # Ensure progress bar is at 100%
        self.progress_var.set(100)

        # Update status
        if len(duplicates) > 0:
            self.status_var.set(f"Found {len(duplicates)} duplicate file pairs.")
        else:
            self.status_var.set("No duplicate files found.")

        # Switch to the duplicates tab
        self.results_notebook.select(1)
