import os
import shutil
import datetime

# Dictionary defining file categories and thier associated extensions

FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Data": [".csv", ".json", ".xml"],
    # Unreognized files will go here
    "Others": []
}

# Defines how may years of files should be organized (past 5 years)
YEAR_RANGE = 5

def get_year_subfolder(file_path):
    """
    Determines the last modified year of the file.
    Ensures the year falls within a valid range before categorization.
    """
    try:
        # Get modification time
        modified_timestamp = os.path.getmtime(file_path)

        # Conver to date
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        current_year = datetime.datetime.now().year
        
        # Ensure the file year falls within the valid YEAR_RANGE
        if modified_date.year >= (current_year - YEAR_RANGE) and modified_date.year <= current_year:
            return str(modified_date.year)
        else:
            # Ignore unexpected dates
            return "Unknown"
        
    except Exception as e:
        print(f"Error extracting year for {file_path}: {e}")
        return "Unknown"
    
def organize_files(directory):
    """
    Organizes files in the given dir based on their file type and subfolders based on date.
    Raises and error if the path provided is invalid or inaccessible.
    """
    if not os.path.isdir(directory):
        raise Exception(f"Error: {directory} is not a valid directory")

    # Create category directories if they don't exist before organizing
    
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)
        
    # Process files in the directory
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Skip existing directories that are not in FILE_CATEGORIES (prevents re-moving)
        if os.path.isdir(file_path) and filename not in FILE_CATEGORIES.keys():
            # Skips unrealted folders
            continue

        # Track whether a file has been moved
        file_moved = False
        
        # Iterate through FILE_CATEGORIES to mach file extensions
        for category, extentions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extentions):
                # print(f"Matched '{filename}' as '{category}'")
                # Determine the file's year for correct placement
                year_subfolder = get_year_subfolder(file_path)
                # Define the subfolder path within the correct category
                destination_folder = os.path.join(directory, category, year_subfolder)
                # Ensure category and year subfolder exist
                os.makedirs(destination_folder, exist_ok=True)
                print(f"Created/Verified Folder: {destination_folder}")
                
                # Move file into its category/year folder
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