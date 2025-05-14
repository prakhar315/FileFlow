import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from datetime import datetime

from file_organizer_app.utils.file_metadata import find_unused_files

class UnusedFilesTab:
    def __init__(self, parent):
        """
        Initialize the Unused Files tab.

        Args:
            parent: The parent notebook widget
        """
        self.frame = ttk.Frame(parent)
        # Store all unused files for client-side filtering
        self.all_unused_files = []
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the Unused Files tab."""
        # Directory selection
        dir_frame = ttk.LabelFrame(self.frame, text="Directory Selection")
        dir_frame.pack(fill=tk.X, padx=10, pady=10)

        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        browse_btn = ttk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Filter options
        filter_frame = ttk.LabelFrame(self.frame, text="Filter Options")
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(filter_frame, text="Days since last access:").pack(side=tk.LEFT, padx=5, pady=5)

        self.days_var = tk.IntVar(value=90)
        days_spinbox = ttk.Spinbox(filter_frame, from_=1, to=1000, textvariable=self.days_var, width=5)
        days_spinbox.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Label(filter_frame, text="File type:").pack(side=tk.LEFT, padx=5, pady=5)

        self.file_type_var = tk.StringVar(value="All")
        self.file_type_combo = ttk.Combobox(filter_frame, textvariable=self.file_type_var, width=10)
        self.file_type_combo['values'] = ('All', '.pdf', '.jpg', '.png', '.docx', '.txt', '.xlsx',
                                         '.mp3', '.mp4', '.exe', '.zip', '.py', '.html', '.css', '.js')
        self.file_type_combo.pack(side=tk.LEFT, padx=5, pady=5)
        # Bind the combobox to filter results when changed
        self.file_type_combo.bind("<<ComboboxSelected>>", self.filter_results)

        find_btn = ttk.Button(filter_frame, text="Find Unused Files", command=self.find_unused_files)
        find_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Results frame
        results_frame = ttk.LabelFrame(self.frame, text="Unused Files")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a treeview for results
        columns = ("Name", "Path", "Size", "Last Accessed", "Last Modified", "Type")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")

        # Configure columns
        self.results_tree.heading("Name", text="Name")
        self.results_tree.heading("Path", text="Path")
        self.results_tree.heading("Size", text="Size (KB)")
        self.results_tree.heading("Last Accessed", text="Last Accessed")
        self.results_tree.heading("Last Modified", text="Last Modified")
        self.results_tree.heading("Type", text="Type")

        self.results_tree.column("Name", width=150)
        self.results_tree.column("Path", width=250)
        self.results_tree.column("Size", width=80)
        self.results_tree.column("Last Accessed", width=150)
        self.results_tree.column("Last Modified", width=150)
        self.results_tree.column("Type", width=50)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        x_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.results_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        self.results_tree.pack(fill=tk.BOTH, expand=True)

        # Add right-click menu
        self.context_menu = tk.Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Open File", command=self.open_file)
        self.context_menu.add_command(label="Open Containing Folder", command=self.open_folder)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all)
        self.context_menu.add_command(label="Deselect All", command=self.deselect_all)

        self.results_tree.bind("<Button-3>", self.show_context_menu)

        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(self.frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def browse_directory(self):
        """Open a directory browser dialog."""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)

    def find_unused_files(self):
        """Find unused files in the selected directory."""
        directory = self.dir_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        if not os.path.exists(directory):
            messagebox.showerror("Error", "The selected directory does not exist.")
            return

        days = self.days_var.get()
        file_type = self.file_type_var.get()

        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self.status_var.set("Finding unused files... This may take a while for large directories.")

        # Store all unused files for client-side filtering
        self.all_unused_files = []

        # Run the search in a separate thread
        def search_thread():
            try:
                # Get all unused files regardless of type
                unused_files = find_unused_files(directory, days)

                # Store all results for client-side filtering
                self.all_unused_files = unused_files

                # Apply filter if needed
                filtered_files = unused_files
                if file_type != "All":
                    filtered_files = [f for f in unused_files if f["extension"] == file_type]

                # Update the UI in the main thread
                self.frame.after(0, lambda: self.update_results(filtered_files))
            except Exception as e:
                self.frame.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
                self.frame.after(0, lambda: self.status_var.set("Error finding unused files."))

        threading.Thread(target=search_thread).start()

    def update_results(self, unused_files):
        """
        Update the results treeview.

        Args:
            unused_files: List of dictionaries containing metadata of unused files
        """
        for file_info in unused_files:
            # Format the size in KB
            size_kb = round(file_info["size"] / 1024, 2)

            # Format the dates
            accessed = file_info["accessed"].strftime("%Y-%m-%d %H:%M")
            modified = file_info["modified"].strftime("%Y-%m-%d %H:%M")

            self.results_tree.insert("", tk.END, values=(
                file_info["name"],
                file_info["path"],
                size_kb,
                accessed,
                modified,
                file_info["extension"]
            ))

        self.status_var.set(f"Found {len(unused_files)} unused files.")

    def show_context_menu(self, event):
        """Show the context menu on right-click."""
        # Select the item under the cursor
        item = self.results_tree.identify_row(event.y)
        if item:
            self.results_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def open_file(self):
        """Open the selected file."""
        selected = self.results_tree.selection()
        if selected:
            item = selected[0]
            file_path = self.results_tree.item(item, "values")[1]
            try:
                os.startfile(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def open_folder(self):
        """Open the folder containing the selected file."""
        selected = self.results_tree.selection()
        if selected:
            item = selected[0]
            file_path = self.results_tree.item(item, "values")[1]
            folder_path = os.path.dirname(file_path)
            try:
                os.startfile(folder_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {str(e)}")

    def select_all(self):
        """Select all items in the treeview."""
        for item in self.results_tree.get_children():
            self.results_tree.selection_add(item)

    def deselect_all(self):
        """Deselect all items in the treeview."""
        for item in self.results_tree.get_children():
            self.results_tree.selection_remove(item)

    def filter_results(self, event=None):
        """
        Filter the results based on the selected file type without re-searching.
        This is a client-side filter that works on already loaded data.
        """
        # If we don't have any results yet, do nothing
        if not self.all_unused_files:
            return

        file_type = self.file_type_var.get()

        # Clear current display
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Apply filter
        if file_type == "All":
            filtered_files = self.all_unused_files
        else:
            filtered_files = [f for f in self.all_unused_files if f["extension"] == file_type]

        # Update display with filtered results
        self.update_results(filtered_files)

        # Update status
        self.status_var.set(f"Showing {len(filtered_files)} unused files with type {file_type}")
