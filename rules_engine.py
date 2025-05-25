import os
import shutil
import datetime

class Rule:
    def __init__(self, name, description, enabled=True):
        """
        
        Init a rule with a name, description, and whether it's enabled
        
        """
        
        self.name = name
        self.description = description
        self.enabled = enabled
        
    def applies_to(self, file_info):
        """
        
        Make a determination whether the reule applies to the given file.
        Return 'True' if the rule should act on the file.
        
        Parameter:
            file_info:  dict with the file metadata (e.g., 'name', 'path')

        Return:
            'True' if the rule applies and False is not
        
        """
        
        raise NotImplementedError("This method must be overridden by subclasses.")
    
    def apply(self, file_info):
        """
        
        Carry out the action of the rule method above on the file.
        
        Parameter:
            file_path: Dictionary containing file metadata ('name', 'path').
        
        """
        
        raise NotImplementedError("This method must be overridden by subclasses.")
    
    
class ExtensionRule(Rule):
    def __init__(self, name, description, target_extensions, destination_folder, enabled=True):
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
        
        
    def applies_to(self, file_info):
        """
        
        Identify name of the file using a dict.
        Make sure we lower the name of the file and it ends with our target_extension (that is also lowered up above)
        
        Parameters:
            file_info: dict that will allow out file name, if any, to match our extension
        Return: 
            'True' if file_name ends with our target_extension
        
        """

        file_name = file_info.get('name', '').lower()
        
        return any(file_name.endswith(ext) for ext in self.target_extensions)
    
    def apply(self, file_info):
        """
        
        Move the file to the designated folder.
        
        Parameters:
            file_info: Out dict with the metadata
        
        """
        
        # Fetch the abs path of the file
        
        file_path = file_info.get('path')
        if not file_path:
            return
        
        # Ensure our folder exists and create one if it doesn't; True so we don't raise an exception
        
        os.makedirs(self.destination_folder, exist_ok=True)
        
        # Create full destination by joining destination_folder and file_path
        
        destination = os.path.join(self.destination_folder, os.path.basename(file_path))
        
        #  Attempt to move using shutil.move
        
        try:
            shutil.move(file_path, destination)
            print(f"Rule '{self.name}' move '{file_info.get('name')}' to {destination}")
        except Exception as e:
            print(f"Rule '{self.name}' failed to move '{file_info.get('name')}', Error: {e}")
            
        
        
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
    
    def process_files(self, file_list):
        """
        
        Process each file in file_list.
        Check each file; check each rule.
        If a rule's condition (applies_to) returns True, then the rule's action (apply) is executed.

        Parameters:
            file_list:  A list of dicts, each contain the metadata.
                        Example: [{'name'}: 'photo.jpg', 'path': '/images/photo.jpg']
        
        """
        # Iterate over each file_list
        
        for file_info in file_list:
            
            # Iterate over each rule of the file
            
            for rule in self.rules:
                
                # Only when rules are active
                
                if not rule.enabled:
                    print(f"[SKIPPED] Rule '{rule.name}' is disabled")
                    continue
                    
                    # Check if rule applies to the file and then call our method when we have a match
                    
                if rule.applies_to(file_info):
                        
                    # Execute the action on the file when all criteria has been met
                        
                    rule.apply(file_info)
                        
                        
class FallbackRule(Rule):
    def __init__(self, name, description, base_destination, enabled=True):
        """
        
        Init fallback for files we do not look for (Others folder).
        
        Parameters:
            base_destination: Base folder for our fallback destination
        
        """
        super().__init__(name, description, enabled)
        self.base_destination = base_destination
        
    def applies_to(self, file_info):
        """
        
        Determine if a fallback should happen to a give file.
        
        Parameters:
            file_info: dict with our metadata
            
        Returns:
            True is we have a file that matches, False otherwise
        
        """
        
        file_path = file_info.get('path')
        return file_path is not None and os.path.exists(file_path)
    
    def apply(self, file_info):
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
        
        file_path = file_info.get('path')
        if not file_path or not os.path.exists(file_path):
            return
        
        # Compute the year-month from the file's last modification time
        
        try:
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            month_and_year = modified_time.strftime("%Y-%B")
        except Exception as e:
            print(f"[ERROR] FallbackRule: Unable to retrieve modification time for '{file_info.get('name')}'. Error: {e}")
            return
        
        # Specify destination
        
        destination_folder = os.path.join(self.base_destination, "Others", month_and_year)
        os.makedirs(destination_folder, exist_ok=True)
        
        # Full destination path with our folder name
        
        destination = os.path.join(destination_folder, os.path.basename(file_path))

        # try/except to move the file
        
        try:
            shutil.move(file_path, destination)
            print(f"Fallback to Others folder '{file_info.get('name')}' to '{destination}'")
        except Exception as e:
            print(f"Fallback failed to move '{file_info.get('name')}'. Error: {e}")