import os
import shutil
import datetime

# Dictionary defining file categories and their associated extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Data": [".csv", ".json", ".xml"],

    # Unrecognized files will go here
    "Others": []
}

# Made to not tamper with a Windows Desktop
EXCLUDED_ITEMS = {

    # Common Windows system file
    "deskstop.ini",
    
    # Virtual folder (if it appears)
    "This PC",
    "Recycle Bin",
    "Network",
    
    # Default OneDrive shortcut
    "OneDrive",
    
    # Legacy config
    "Control Panel"
}

# File extensions we are not wanting to include
EXCLUDED_EXT = {
    ".exe"
}

# Defines how many years of files should be organized (past 5 years)
YEAR_RANGE = 5

# Define log filename for review
LOG_FILE = "unexpected_dates.log"

def get_year_month_subfolder(file_path):
    """
    Determines the last modified year of the file.
    Ensures the year falls within a valid range before categorization.
    """
    try:
        # Get modification time
        modified_timestamp = os.path.getmtime(file_path)

        # Convert to date
        modified_date = datetime.datetime.fromtimestamp(modified_timestamp)
        current_year = datetime.datetime.now().year
        
        # Ensure the file year falls within the valid YEAR_RANGE
        if (current_year - modified_date.year) <= YEAR_RANGE:
            # Convert month number to name
            month_name = modified_date.strftime("%B")
            
            return f"{modified_date.year}-{month_name}"
        else:
            # Log unexpected dates instead of silently ignoring them
            with open(LOG_FILE, "a") as log:
                log.write(f"{modified_date.year}-{modified_date.strftime('%m')}: {file_path}\n")
            # Ignore unexpected dates
            return "Unknown"
        
    except Exception as e:
        print(f"Error extracting year for {file_path}: {e}")
        return "Unknown"
    
def create_main_category_folders(directory):
    # Create category directories if they don't exist before organizing
    
    for category in FILE_CATEGORIES:
        folder_path = os.path.join(directory, category)
        os.makedirs(folder_path, exist_ok=True)
    
def organize_files(directory):
    """
    Organizes files in the given dir based on their file type and subfolders based on date.
    Raises an error if the path provided is invalid or inaccessible.
    """
    if not os.path.isdir(directory):
        raise Exception(f"Error: {directory} is not a valid directory")

    # create_main_category_folders(directory)
        
    # Process files in the directory
    
    for filename in os.listdir(directory):
        # Skip sys default items if needed
        if filename in EXCLUDED_ITEMS:
            print(f"Skipping excluded item: {filename}")
            continue
        
        # Skip excluded file extentions
        if any(filename.lower().endswith(ext) for ext in EXCLUDED_EXT):
            print(f"Skipping file with excluded extension: {filename}")
        file_path = os.path.join(directory, filename)
        
        # Skip existing directories that are not in FILE_CATEGORIES (prevents re-moving)
        if os.path.isdir(file_path) and filename not in FILE_CATEGORIES.keys():
            # Skips unrelated folders
            continue

        # Track whether a file has been moved
        file_moved = False
        
        # Iterate through FILE_CATEGORIES to match file extensions
        for category, extensions in FILE_CATEGORIES.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                # print(f"Matched '{filename}' as '{category}'")
                # Determine the file's year for correct placement
                year_subfolder = get_year_month_subfolder(file_path)
                # Define the subfolder path within the correct category
                destination_folder = os.path.join(directory, category, year_subfolder)
                # Ensure category and year subfolder exist
                os.makedirs(destination_folder, exist_ok=True)
                print(f"Created/Verified Folder: {destination_folder}")
                
                # Move file into its category/year folder
                destination = os.path.join(destination_folder, filename)
                shutil.move(file_path, destination)
                # Mark as moved
                file_moved = True
                # Stop searching once a match is found
                break
            
        # Place unrecognized files inside of "Others/YYYY"
        if not file_moved:
            handle_unrecognized_files(file_path, directory)
    

def handle_unrecognized_files(file_path, directory):
    """
    Moves files we might not normally encounter into the "Others/YYYY-Month" folder.
    """
    if os.path.isdir(file_path):
        print(f"Skipping move for existing directory: {file_path}")
        return
    
    year_month_subfolder = get_year_month_subfolder(file_path)
    
    if year_month_subfolder == "Unknown":
        print(f"Skipping unrecognized file with invalid date: {file_path}")
        return
    
    destination_folder = os.path.join(directory, "Others", year_month_subfolder)
    os.makedirs(destination_folder, exist_ok=True)

    destination = os.path.join(destination_folder, os.path.basename(file_path))
    
    shutil.move(file_path, destination)
    print(f"Moved '{file_path}' to '{destination}'")

def main():
    """
    Main execution function prompting user for a directory path.
    """
    directory_to_organize = input("Enter the directory path to organize: ")
    organize_files(directory_to_organize)

    
if __name__ == "__main__": 
    main()