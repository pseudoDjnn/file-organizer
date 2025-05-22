import tkinter as tk
from tkinter import filedialog

from file_organizer import FileOrganizer
from filepath_utils import FilePathUtils

class OrganizerGUI:
    def __init__(self):
    # Create the root window
    
        self.root = tk.Tk()    
        self.root.title("File Organizer")
    
    # Create a look
    
        self.retro_bg = "#c0c0c0"
        self.root.configure(bg=self.retro_bg)
        
        self.retro_font = ("Ms Sans Serif", 10)

    # Set the window dimensions: Center
    
        self.window_width = 500
        self.window_height = 150
    
    # Get Screen dimensions
    
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
    # Calc to find center position
    
        x_position = (screen_width - self.window_width) // 2
        y_position = (screen_height - self.window_height) // 4
    
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_position}+{y_position}")

    # Label to display the selected directory
    # default_directory = "/mnt/c/Users/lavah/"
    
        self.selected_directory = None
        
    # Init for shortener
    
        self.path_utils = FilePathUtils(max_length=34)
        
    # Build the GUI
    
        self.create_app()
        
    def create_app(self):

    # Create a main frame for better structure
    
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill='both', expand=True)
    
    # Create a frame for file selection
    
        self.file_frame = tk.Frame(self.main_frame)
        self.file_frame.grid(row=0, column=0, sticky="w")
    # file_frame.columnconfigure(0, weight=1)
    
    
        self.directory_label = tk.Label(
            self.file_frame, 
            text="Please Select a directory", 
            anchor="w",
            bg=self.retro_bg,
            fg="black",
            font=self.retro_font
            )
        self.directory_label.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="w")
    
        self.browse_button = tk.Button(
            self.file_frame,
            text="Browse",
            command=self.select_directory,
            bg=self.button_bg,
            relief=tk.RAISED,
            bd=self.button_bd,
            font=self.retro_font
            )
        self.browse_button.grid(row=1, column=0, padx=5, pady=5)

        self.run_button = tk.Button(
            self.file_frame,
            text="Sort Files",
            command=self.run_organizer_command,
            bg=self.button_bg,
            relief=tk.RAISED,
            bd=self.button_bd,
            font=self.retro_font
            )
        self.run_button.grid(row=1, column=3, padx=5,pady=5)

    # Function to open a directory chooser dialog
    
    def select_directory(self):
        # nonlocal selected_directory
        # Opens a box to choose a directory
        
        directory = filedialog.askdirectory(
            title="Select Your Directory to Organize",
            # Commented out for the sake of other OS as of right now
            # initialdir=default_directory
            )
        if directory:
            self.selected_directory = directory
            
            # Adding the shortener
            
            shortener = self.path_utils.shortener(directory)
            self.directory_label.config(text="Selected: " + shortener)
            
    # Button to browse for a directory
    
    button_bg = "#e0e0e0"
    button_relief = tk.RAISED
    button_bd = 2
    
    
    # Function to run the organizer with the selected directory
    
    def run_organizer_command(self):
        if self.selected_directory:
            try:
                organizer = FileOrganizer(self.selected_directory)
                organizer.organize_files()
                self.directory_label.config(text=f"Organizer complete for:\n {self.selected_directory}")
            except Exception as e:
                self.directory_label.config(text=f"Error:\n {e}")
        else:
            self.directory_label.config(text=f"Please select a directory first!")

    
    # Start the event loop
    def run(self):
        self.root.mainloop()
    
    
if __name__ == '__main__':
    gui = OrganizerGUI()
    gui.run()