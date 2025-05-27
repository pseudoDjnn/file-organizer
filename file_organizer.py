import os
import shutil
import datetime
import logging

from config import FILE_CATEGORIES, LOGS_FOLDER, EXCLUDED_ITEMS, EXCLUDED_EXT, YEAR_RANGE
from rules_engine import RulesEngine, ExtensionRule, FallbackRule
from report_generator import generate_CSV_report

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
        
    def _collect_files(self):

        """
        Organizes files in the given dir based on their file type and subfolders based on date.
        Raises an error if the path provided is invalid or inaccessible.
        
        """
        
        # Proactive call 
        # self.create_main_category_folders(directory)
            
        # Process files in the directory
        
        files = []
        
        for filename in os.listdir(self.directory):
            
            # Skip our audit report so it isn't processed by Rules
            
            if filename.lower() == "report.csv":
                logger.info(f"Skipping audit file:  {filename}")
                continue

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
                files.append({'name': filename, 'path': file_path})
                
        return files
    
    def _setup_rules(self, engine):
        """
        
        Configures rules engine by setting up extension rules for 
        each file category and fallback for unrecognized files.
        
        """
        
        # Loop configured categories (not 'Others' since that is fallback)
        
        for category, extensions in self.file_categories.items():
            if category == "Others":
                continue
            
            # Determine the destination folder for the category
            
            destination_folder = os.path.join(self.directory, category)
            
            # if not os.path.exists(destination_folder):
            #     os.makedirs(destination_folder)
            #     logger.info(f"Created folder: {destination_folder}")
            
            # Create an Extension that accepts a list of extension for this category
            
            extension_rule = ExtensionRule(
                name=f"{category} Rule",
                description=f"Moves files matching the {category} category",
                target_extensions=extensions,
                destination_folder=destination_folder,
                enabled=True
            )
            engine.add_rule(extension_rule)
        
        # Add the fallback rule for any file not handled by the above rules
        
        fallback_rule = FallbackRule(
            name="Fallback Rule",
            description="Handles unrecognized files by moving them to the 'Other' folder",
            base_destination=self.directory,
            enabled=True
        )
        engine.add_rule(fallback_rule)
        
        
    def organize_files(self):
        """
        
        Organizes files by moving them based on their on their type into category folders.
        Also generate an audit report that goes into the 'log' folder
        
        """
        logger.info(f"Starting file organizer in: {self.directory}")
        
        # Collect  files from the selected directory
        
        file_list = self._collect_files()

        logger.info(f"Collected {len(file_list)} files for processing.")
        
        # Init the rules engine
        
        engine = RulesEngine()
        self._setup_rules(engine)
        
        # Process the files using our 'Rules' and collect the reports
        
        report_data = []

        engine.process_files(file_list, report_data)
        
        # Generate the .CSV and ensure the 'logs' folder is in the directory
        
        logs_folder_path = os.path.join(self.directory, LOGS_FOLDER)
        
        if not os.path.exists(logs_folder_path):
            os.makedirs(logs_folder_path)
            logger.info(f"Created logs folder:  {logs_folder_path}")
            
        # Define the CSV report filepath inside of our 'logs' folder
        
        csv_filepath = os.path.join(logs_folder_path, "report.csv")
        
        logger.info(f"CSV report will be generated at:  {csv_filepath}")
        
        # Generate the report
        
        generate_CSV_report(report_data, csv_filename=csv_filepath)