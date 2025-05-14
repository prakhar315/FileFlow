import tkinter as tk
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import from the package
from file_organizer_app.gui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    # Create the main window
    root = tk.Tk()
    app = MainWindow(root)

    # Set window icon and title
    root.title("File Organizer Pro")

    # Center the window on screen
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
