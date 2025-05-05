import os
import shutil
import datetime


FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Data": [".csv", ".json", ".xml"],
    "Others": []
}

def get_year_subfolder(file_path):
    modified_timestamp = os.path.getmtime(file_path)
    modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
    print(f"File: {file_path} - Modified Year: {modified_date.year}")
    return str(modified_date.year)
    
def organize_files(directory):
    """
    Organizes files in the given dir based on their file type
    """
    if not os.path.isdir(directory):
        raise Exception(f"Error: {directory} is not a valid directory")

    # Create category directories if they don't exist
    
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)
        
        
    # Process files in the directory
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # print(f"Processing: {file_path}")
        
        # Skip existing directories
        if os.path.isdir(file_path) and filename not in FILE_CATEGORIES.keys():
            # print(f"Skipping unrelated directory: {file_path}")
            continue

        file_moved = False
        for category, extentions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extentions):
                print(f"Matched '{filename}' as '{category}'")
                year_subfolder = get_year_subfolder(file_path)
                destination_folder = os.path.join(directory, category, year_subfolder)

                # Ensure category and year subfolder exist
                os.makedirs(destination_folder, exist_ok=True)
                print(f"Created/Verified Folder: {destination_folder}")
                
                destination = os.path.join(destination_folder, filename)
                shutil.move(file_path, destination)
                file_moved = True
                break
            
        if not file_moved:
            # Default placement for unrecognized files in "Others/YYYY"
            year_subfolder = get_year_subfolder(file_path)
            destination_folder = os.path.join(directory, "Others", year_subfolder)
            
            os.makedirs(destination_folder, exist_ok=True)
            
            destination = os.path.join(destination_folder, filename)
            
            # Only move files, skip directories
            if not os.path.isdir(file_path):
                shutil.move(file_path, destination)
                print(f"Moved '{filename}' to '{destination}'")
            else:
                print(f"Skipping move for existing directory: {file_path}")


def main():
    directory_to_organize = input("Enter the directory path to organize: ")
    organize_files(directory_to_organize)

    
if __name__ == "__main__": 
    main()