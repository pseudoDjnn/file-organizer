import tkinter as tk
from tkinter import filedialog

from file_organizer import organize_files

def run_gui():
    # Create the root window
    
    root = tk.Tk()

    # Set the window title
    
    root.title("Simple Tkinter Window")
    
    # Set the window dimensions: width x height
    
    root.geometry("400x300")
    
    # Label to display the selected directory
    
    default_directory = "/mnt/c/Users/lavah/"
    
    selected_directory = None
    
    directory_label = tk.Label(root, text="Please Select a directory", padx=10, pady=10)
    directory_label.pack()
    
    # Function to open a directory chooser dialog
    
    def select_directory():
        nonlocal selected_directory
        # Opens a box to choose a directory
        
        directory = filedialog.askdirectory(
            title="Select Your Directory to Organize",
            # Commented out for the sake of other OS as of right now
            
            # initialdir=default_directory
            )
        if directory:
            selected_directory = directory
            directory_label.config(text=f"Selected: {directory}")
            
    # Button to browse for a directory
    
    browse_button = tk.Button(root, text="Browse Directory", command=select_directory, padx=5, pady=5)
    browse_button.pack()
    
    # Function to run the organizer with the selected directory
    
    def run_organizer_command():
        if selected_directory:
            try:
                organize_files(selected_directory)
                directory_label.config(text=f"Organizer complete for:\n {selected_directory}")
            except Exception as e:
                directory_label.config(text=f"Error:\n {e}")
        else:
            directory_label.config(text=f"Please select a directory first!")

    browse_button = tk.Button(root, text="Run Organizer", command=run_organizer_command, padx=5, pady=5)
    browse_button.pack()
    
    # Start the event loop
    
    root.mainloop()
    
    
if __name__ == '__main__':
    run_gui()