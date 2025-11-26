import os
import shutil
import datetime
import logging

from config import FILE_CATEGORIES, EXCLUDED_ITEMS, EXCLUDED_EXT, YEAR_RANGE
from services.models import FileItem
from services.rules import build_destination

logger = logging.getLogger(__name__)


class Rule:
    def __init__(self, name, description, enabled=True):
        """
        
        Init a rule with a name, description, and whether it's enabled
        
        """
        
        self.name = name
        self.description = description
        self.enabled = enabled
        
    def applies_to(self):
        """
        
        Make a determination whether the reule applies to the given file.
        Return 'True' if the rule should act on the file.
        
        Parameter:
            file_info:  dict with the file metadata (e.g., 'name', 'path')

        Return:
            'True' if the rule applies and False is not
        
        """
        
        raise NotImplementedError("This method must be overridden by subclasses.")
    
    def apply(self):
        """
        
        Carry out the action of the rule method above on the file.
        
        Parameter:
            file_path: Dictionary containing file metadata ('name', 'path').
        
        """
        
        raise NotImplementedError("This method must be overridden by subclasses.")
    
    
class ExtensionRule(Rule):
    def __init__(self, name, description, target_extensions, destination_folder, enabled=True, depth="month"):
        """
        
        Init an extension-based rule.
        
        Parameter:
            target_extension: e.g., '.jpeg'
        Parameter:
            destination_folder: path where matching files should move
        
        """
        super().__init__(name, description, enabled)
        
        # Ensure target_extensions is a list.  If a string is passed, convert it
        
        if isinstance(target_extensions, str):
            target_extensions = [target_extensions]

        # Call new parms

        self.target_extensions = [ext.lower() for ext in target_extensions]
        self.destination_folder = destination_folder
        # year/month/day
        self.depth = depth
        
        
    def applies_to(self, file: FileItem):
        """
        
        Identify name of the file using a dict.
        Make sure we lower the name of the file and it ends with our target_extension (that is also lowered up above)
        
        Parameters:
            file_info: dict that will allow out file name, if any, to match our extension
        Return: 
            'True' if file_name ends with our target_extension
        
        """

        # file_name = file_info.get('name', '').lower()
        
        # return any(file_name.endswith(ext) for ext in self.target_extensions)
        return file.extension in self.target_extensions
    
    def apply(self, file: FileItem):
        """
        
        Move the file to the designated folder.
        
        Parameters:
            file_info: Out dict with the metadata
        
        """
                    
        try:
            
            #   Build the destination folder using rules.py
            
            destination_folder = build_destination(self.destination_folder, file, depth="month")
            os.makedirs(destination_folder, exist_ok=True)
            
            #  Final location for our path
            
            destination = os.path.join(destination_folder, file.name)
            
            #  Move our file
            
            shutil.move(file.path, destination)
            
            logger.info(f"ExtensionRule '{self.name}' moved '{file.name}' to {destination}")
            return True, destination
        
        except Exception as e:
            logger.info(f"ExtensionRule '{self.name}' failed to move '{file.name}'. Error: {e} ")
            return False, None
        
        
class RulesEngine:
    def __init__(self):
        """
        
        Init the RulesEngine with an empty list
        
        """
        
        self.rules = []
        
    def add_rule(self, rule):
        """
        
        Add a rule to the engines list of rules.
        
        Parameter:
            rule: Init a class derived from Rule
        
        """
        
        self.rules.append(rule)
    
    def process_files(self, file_list, report_data=None):
        """
        
        Process each file in file_list.
        Check each file; check each rule.
        If a rule's condition (applies_to) returns True, then the rule's action (apply) is executed.

        Parameters:
            file_list:  A list of dicts, each contain the metadata.
                        Example: [{'name'}: 'photo.jpg', 'path': '/images/photo.jpg']
            report_data:  A list to report records that get appended
        
        """
        # Iterate over each file_list
        
        for file in file_list:
            
            # Grab the original path for creating a report
            
            original_path = file.path
            
            # Iterate over each rule of the file
            
            for rule in self.rules:
                
                # Only when rules are active
                
                if not rule.enabled:
                    logger.info(f"[SKIPPED] Rule '{rule.name}' is disabled")
                    continue
                    
                    # Check if rule applies to the file and then call our method when we have a match
                    
                if rule.applies_to(file):
                        
                    # Return a tuple: (success, destination)
                    
                    success, dest = rule.apply(file)
                    if success:
                        if report_data is not None:
                            record = {
                                "file_name": file.name,
                                "original_path": original_path,
                                "destination": dest,
                                "rule_applied": rule.name,
                                "processed_at": datetime.datetime.now().isoformat()
                                
                            }
                            report_data.append(record)
                            logger.info(F"[RECORD ADDED] Report entry added for '{file.name}'")
                        
                        # Move if a rule has been applied
                        
                        break
                        
                        
class FallbackRule(Rule):
    def __init__(self, name, description, base_destination, enabled=True, depth="month"):
        """
        
        Init fallback for files we do not look for (Others folder).
        
        Parameters:
            base_destination: Base folder for our fallback destination
        
        """
        super().__init__(name, description, enabled)
        self.base_destination = base_destination
        self.depth = depth
        
    def applies_to(self, file: FileItem):
        """
        
        Determine if a fallback should happen to a give file.
        
        Parameters:
            file_info: dict with our metadata
            
        Returns:
            True if we have a file that matches, False otherwise
        
        """
        
        # file_path = file_info.get('path')
        # return file_path is not None and os.path.exists(file_path)
        
        return os.path.exists(file.path)
    
    def apply(self, file: FileItem):
        """
        
        Move the file to the fallback folder (Others folder)
         
        Steps:
           1. Retrieve the file's modification time
           2. Build a destination (Others) folder using datetime
           3. Ensure our destination folder exists and mkae one if it doesn't
           4. Move our files to the 'Others' destination folder using shutil
            
        Parameters:
            file_info: dict using metadata
        
        """
                
        try:
            #   Build destination path using rules.py logic
            
            base_dir = os.path.join(self.base_destination, "Others")
            destination_folder = build_destination(base_dir, file, depth=self.depth)
            os.makedirs(destination_folder, exist_ok=True)
            
            destination = os.path.join(destination_folder, file.name)
            shutil.move(file.path, destination)
            
            logger.info(f"FallbackRule moved '{file.name}' to '{destination}'")
            return True, destination
        except Exception as e:
            logger.info(f"FallbackRule failed to move '{file.name}'.  Error: {e}")
            return False, None