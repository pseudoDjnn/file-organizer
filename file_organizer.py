import os
import shutil
import datetime
import logging

from config import FILE_CATEGORIES, EXCLUDED_ITEMS, EXCLUDED_EXT, YEAR_RANGE

# Get a module-specific logger
logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self,
        directory,
        file_categories=FILE_CATEGORIES,
        excluded_items=EXCLUDED_ITEMS,
        excluded_ext=EXCLUDED_EXT,
        year_range=YEAR_RANGE):
        
        if not os.path.isdir(directory):
            logger.error("Invalid directory: %s", directory)
            raise Exception(f"Error: {directory} is not a valid directory")
        
        self.directory = directory
        self.file_categories = file_categories
        self.excluded_items = excluded_items
        self.excluded_ext = excluded_ext
        self.year_range = year_range
        
    def get_year_month_subfolder(self, file_path):
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
            if (current_year - modified_date.year) <= self.year_range:
                # Convert month number to name
                month_name = modified_date.strftime("%B")
                
                return f"{modified_date.year}-{month_name}"
            else:
                # Log unexpected dates instead of silently ignoring them
                logger.info(f"Unexpected date: {modified_date.year}-{modified_date.strftime('%m')} for {file_path}")
                # Ignore unexpected dates
                return "Unknown"
            
        except Exception as e:
            logger.error(f"Error extracting year for {file_path}: {e}")
            return "Unknown"
        
    def create_main_category_folders(self):
        # Create category directories if they don't exist before organizing
        
        for category in self.file_categories:
            folder_path = os.path.join(self.directory, category)
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Ensure category folder exists: {folder_path}")
        
    def organize_files(self):

        """
        Organizes files in the given dir based on their file type and subfolders based on date.
        Raises an error if the path provided is invalid or inaccessible.
        
        """
        
        # Proactive call 
        # self.create_main_category_folders(directory)
            
        # Process files in the directory
        
        for filename in os.listdir(self.directory):
            # Skip sys default items if needed
            if filename in self.excluded_items:
                logger.info(f"Skipping excluded item: {filename}")
                continue
            
            # Skip excluded file extentions
            if any(filename.lower().endswith(ext) for ext in self.excluded_ext):
                logger.info(f"Skipping file with excluded extension: {filename}")
                continue
            file_path = os.path.join(self.directory, filename)
            
            # Skip existing directories that are not in FILE_CATEGORIES (prevents re-moving)
            if os.path.isdir(file_path) and filename not in self.file_categories:
                # Skips unrelated folders
                continue

            # Track whether a file has been moved
            file_moved = False
            
            # Iterate through FILE_CATEGORIES to match file extensions
            for category, extensions in self.file_categories.items():
                if any(filename.lower().endswith(ext) for ext in extensions):
                    # print(f"Matched '{filename}' as '{category}'")
                    # Determine the file's year for correct placement
                    year_subfolder = self.get_year_month_subfolder(file_path)
                    # Define the subfolder path within the correct category
                    destination_folder = os.path.join(self.directory, category, year_subfolder)
                    # Ensure category and year subfolder exist
                    os.makedirs(destination_folder, exist_ok=True)
                    logger.info(f"Created/Verified Folder: {destination_folder}")
                    
                    # Move file into its category/year folder
                    destination = os.path.join(destination_folder, filename)
                    try:
                        shutil.move(file_path, destination)
                        logger.info(f"Moved {filename} to {destination}")
                        print(f"Task Completed: '{filename}' has been moved to '{destination}'")
                    except Exception as e:
                        logger.error(f"Failed to move {file_path} to {destination}: {e}")
                    # Mark as moved
                    file_moved = True
                    # Stop searching once a match is found
                    break
                
            # Place unrecognized files inside of "Others/YYYY"
            if not file_moved:
                self.handle_unrecognized_files(file_path)
        

    def handle_unrecognized_files(self, file_path):
        """
        
        Moves files we might not normally encounter into the "Others/YYYY-Month" folder.

        """

        if os.path.isdir(file_path):
            logger.info(f"Skipping move for existing directory: {file_path}")
            return
        
        year_month_subfolder = self.get_year_month_subfolder(file_path)
        
        if year_month_subfolder == "Unknown":
            logger.info(f"Skipping unrecognized file with invalid date: {file_path}")
            return
        
        destination_folder = os.path.join(self.directory, "Others", year_month_subfolder)
        os.makedirs(destination_folder, exist_ok=True)

        destination = os.path.join(destination_folder, os.path.basename(file_path))
        
        try:
            shutil.move(file_path, destination)
            logger.info(f"Moved '{file_path}' to '{destination}'")
        except Exception as e:
            logger.error(f"Failed to move {file_path} to {destination}: {e}")