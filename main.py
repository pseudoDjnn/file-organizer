import os
import shutil
from pathlib import Path

def get_desktop_directory():
    # Get the user's home directory
    windows_desktop = Path("/mnt/c/Users/lavah/OneDrive/Desktop")
    if windows_desktop.exists():
        print("Using Windows Desktop Path:", windows_desktop)
        return windows_desktop
    else:
        print("Warning: Windows Desktop path not found.")
    
    
def main():
    get_desktop_directory()
    
if __name__=="__main__":
    main()