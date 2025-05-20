import tkinter as tk
from tkinter import filedialog

def run_gui():
    # Create the root window
    
    root = tk.Tk()

    # Set the window title
    
    root.title("Simple Tkinter Window")
    
    # Set the window dimensions: width x height
    
    root.geometry("400x300")
    
    # Label to display the selected directory
    
    default_directory = "/mnt/c/Users/lavah/"
    directory_label = tk.Label(root, text=f"Selected: {default_directory}", padx=10, pady=10)
    directory_label.pack()
    
    # Function to open a directory chooser dialog
    
    def select_directory():
        # Opens a box to choose a directory
        
        directory = filedialog.askdirectory(
            title="Select Your Directory to Organize",
            initialdir=default_directory
            )
        if directory:
            directory_label.config(text="Selected: {directory}")
            
    # Button to browse for a directory
    
    browse_button = tk.Button(root, text="Browse Directory", command=select_directory, padx=5, pady=5)
    browse_button.pack()

    # Start the event loop
    
    root.mainloop()
    
    
if __name__ == '__main__':
    run_gui()