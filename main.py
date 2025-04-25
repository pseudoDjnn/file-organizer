import os
import shutil
from pathlib import Path

def main():
    # Get the user's home directory
    home = Path.home()

    # Define the Desktop folder path
    desktop = home / "Desktop"
    print("Desktop Path:", desktop)
    folder = {
        "Downloads": home / "Downloads",
        "Documents": home / "Documents",
        "Pictures": home / "Pictures",
        "Music": home / "Music",
        "Downloads": home / "Downloads",
    }
    
if __name__=="__main__":
    main()