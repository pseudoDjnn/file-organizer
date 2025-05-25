import os
import shutil
import datetime
import logging

from config import FILE_CATEGORIES, EXCLUDED_ITEMS, EXCLUDED_EXT, YEAR_RANGE
from rules_engine import RulesEngine, ExtensionRule, FallbackRule

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
        
    def organize_files(self):

        """
        Organizes files in the given dir based on their file type and subfolders based on date.
        Raises an error if the path provided is invalid or inaccessible.
        
        """
        
        # Proactive call 
        # self.create_main_category_folders(directory)
            
        # Process files in the directory
        
        file_list = []
        
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
            
            # Optionally avoid processing and handling of directories

            if os.path.isfile(file_path):
                file_list.append({'name': filename, 'path': file_path})
                
        # Init our Rule class
                
        engine = RulesEngine()
        
        # Loop configured categories (not 'Others' since that is fallback)
        
        for category, extensions in self.file_categories.items():
            if category == "Others":
                continue
            
            # Determine the destination folder for the category
            
            destination_folder = os.path.join(self.directory, category)
            
            # Create an Extension that accepts a list of extension for this category
            
            rule = ExtensionRule(
                name=f"{category} Rule",
                description=f"Moves files matching the {category} category",
                target_extensions=extensions,
                destination_folder=destination_folder,
                enabled=True
            )
            engine.add_rule(rule)
        
        # Add the fallback rule for any file not handled by the above rules
        
        fallback_rule = FallbackRule(
            name="Fallback Rule",
            description="Handles unrecognized files by moving them to the 'Other' folder",
            base_destination=self.directory,
            enabled=True
        )
        engine.add_rule(fallback_rule)
        
        # Process all the file form the file_list using the rules engine.
        
        engine.process_files(file_list)