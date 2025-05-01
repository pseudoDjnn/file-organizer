import os
import shutil

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

    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)
        
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isdir(file_path):
            continue

        file_moved = False
        for category, extentions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extentions):
                shutil.move(file_path, os.path.join(directory, category, filename))
                file_moved = True
                break
            
        if not file_moved:
            shutil.move(file_path, os.path.join(directory, "Others", filename))


def main():
    pass
    
if __name__ == "__main__":
    main()