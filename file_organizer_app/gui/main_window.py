import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

from file_organizer_app.gui.organize_tab import OrganizeTab
from file_organizer_app.gui.unused_files_tab import UnusedFilesTab
from file_organizer_app.gui.archive_tab import ArchiveTab

class MainWindow:
    def __init__(self, root):
        """
        Initialize the main application window.

        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("900x600")

       # Notebook Initialization
       # Create a tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

       # Initialize and add tabs to the notebook
       # for organizing, finding unused files, and archiving
        self.organize_tab = OrganizeTab(self.notebook)
        self.unused_files_tab = UnusedFilesTab(self.notebook)
        self.archive_tab = ArchiveTab(self.notebook)

       # Add the initialized tab frames to the notebook widget.
       # Each tab is labeled appropriately based on its functionality.
       # This sets up the tabbed interface for organizing, finding unused files,
       # and archiving or deleting files.
        self.notebook.add(self.organize_tab.frame, text="Organize Files")
        self.notebook.add(self.unused_files_tab.frame, text="Unused Files")
        self.notebook.add(self.archive_tab.frame, text="Archive & Delete")

        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create menu
        self.create_menu()

    def create_menu(self):
        """Create the application menu."""
        menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def show_about(self):
        """Show the about dialog."""
        messagebox.showinfo(
            "About File Organizer",
            "File Organizer v1.0\n\n"
            "A desktop application to organize, manage, and clean up files.\n\n"
            "Features:\n"
            "- Organize files into folders by type\n"
            "- Find unused files\n"
            "- Archive and delete files\n"
        )

    def update_status(self, message):
        """
        Update the status bar message.

        Args:
            message: The message to display
        """
        self.status_var.set(message)
