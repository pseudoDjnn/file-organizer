import tkinter as tk

def run_gui():
    # Create the root window
    
    root = tk.Tk()

    # Set the window title
    
    root.title("Simple Tkinter Window")
    
    # Set the window dimensions: width x height
    
    root.geometry("400x300")

    # Start the event loop
    
    root.mainloop()