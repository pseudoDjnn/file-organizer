import tkinter as tk
from tkinter import filedialog

from file_organizer import organize_files

def run_gui():
    # Create the root window
    
    root = tk.Tk()

    # Set the window title
    
    root.title("File Organizer")
    
    # Set the window dimensions: Center
    
    window_width = 500
    window_height = 150
    
    # Get Screen dimensions
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    
    # Calc to find center position
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 4
    
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a main frame for better structure
    
    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(fill='both', expand=True)
    
    # Create a frame for file selection
    
    file_frame = tk.Frame(main_frame)
    file_frame.grid(row=0, column=0, sticky="w")
    file_frame.columnconfigure(0, weight=1)
    
    # Label to display the selected directory
    # default_directory = "/mnt/c/Users/lavah/"
    
    selected_directory = None
    
    directory_label = tk.Label(file_frame, text="Please Select a directory", anchor="w")
    directory_label.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")
    
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
    
    browse_button = tk.Button(file_frame, text="Browse Directory", command=select_directory)
    browse_button.grid(row=1, column=0, padx=5, pady=5)
    
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

    browse_button = tk.Button(file_frame, text="Run Organizer", command=run_organizer_command, padx=5, pady=5)
    browse_button.grid(row=1, column=3, padx=5,pady=5)
    
    # Start the event loop
    
    root.mainloop()
    
    
if __name__ == '__main__':
    run_gui()