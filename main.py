import os
import shutil
from pathlib import Path

def get_desktop_directory():
    # Get the user's home directory
    one_drive_desktop = Path("/mnt/c/Users/lavah/OneDrive/Desktop")
    standard_windows_desktop = Path("/mnt/c/Users/lavah/Desktop")
    
    if one_drive_desktop.exists():
        print("Using Windows Desktop Path:", one_drive_desktop)
        return one_drive_desktop
    else:
        print("Warning: Windows OneDrive not found.")
        
    if standard_windows_desktop.exists():
        print("Using Windows Desktop Path:", standard_windows_desktop)
        return standard_windows_desktop
    else:
        print("Warning: Windows Desktop path not found.")
    
    
def main():
    get_desktop_directory()
    
if __name__=="__main__":
    main()