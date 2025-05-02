import os
import shutil

UNDO_LOG_FILE = "undo_log.txt"

FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Data": [".csv", ".json", ".xml"],
    "Others": []
}
    
def organize_files(directory):
    """
    Organizes file sin the given dir based on their file type
    """
    if not os.path.isdir(directory):
        raise Exception(f"Error: {directory} is not a valid directory")

    # Craet category directories if they don't exist
    
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)
        
    # Store moved file for undo func
    moved_files = []
        
    # Process files in the directory
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip existing directories
        if os.path.isdir(file_path):
            continue

        file_moved = False
        for category, extentions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extentions):
                destination = os.path.join(directory, category, filename)
                shutil.move(file_path, destination)
                moved_files.append((file_path, destination))
                file_moved = True
                break
            
        if not file_moved:
            destination = os.path.join(directory, "Others", filename)
            shutil.move(file_path, destination)
            moved_files.append((file_path, destination))
            
    # Save the undo log is files were moved
    if moved_files:
        with open(UNDO_LOG_FILE, "w") as undo_file:
            for original, new in moved_files:
                undo_file.write(f"{original}|{new}\n")
                
        print(f"Undo log saved: {UNDO_LOG_FILE}")
            


def main():
    directory_to_organize = input("Enter the directory path to organize: ")
    organize_files(directory_to_organize)

    
if __name__ == "__main__": 
    main()