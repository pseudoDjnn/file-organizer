import os
import shutil
from pathlib import Path

def get_system_folders():
    # Get the user's home directory
    home = Path.home()

    # Define the Desktop folder path
    desktop = home / "Desktop"
    print("Desktop Path:", desktop)
    return {
        "Downloads": home / "Downloads",
        "Documents": home / "Documents",
        "Pictures": home / "Pictures",
        "Music": home / "Music",
        "Videos": home / "Videos",
    }
    
    
def get_file_mapping(system_folders: dict):
    pass
    
    
def main():
    get_system_folders()

if __name__=="__main__":
    main()