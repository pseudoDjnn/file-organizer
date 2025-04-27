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
    return {
        ".txt": system_folders["Documents"],
        ".pdf": system_folders["Documents"],
        ".doc": system_folders["Documents"],
        ".docx": system_folders["Documents"],
        
        ".jpg": system_folders["Pictures"],
        ".jpeg": system_folders["Pictures"],
        ".png": system_folders["Pictures"],
        ".gif": system_folders["Pictures"],
        
        ".mp3": system_folders["Music"],
        ".wav": system_folders["Music"],
        ".flac": system_folders["Music"],
        
        ".mp4": system_folders["Videos"],
        ".mov": system_folders["Videos"],
        ".avi": system_folders["Videos"],
    }
    
    
def main():
    get_system_folders()

if __name__=="__main__":
    main()