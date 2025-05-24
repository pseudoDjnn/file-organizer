import os
import shutil

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
    
    def apply(self, file_path):
        """
        
        Carry out the action of the rule method above on the file.
        
        Parameter:
            file_path:  dict with file metadata.
        
        """
        
        raise NotImplementedError("This method must be overridden bu subclasses.")
    
    
class ExtensionRule(Rule):
    def __init__(self, name, description, target_extension, destination_folder, enabled=True):
        """
        
        Init an extension-based rule.
        
        Parameter:
            target_extension: e.g., '.jpeg'
        Parameter:
            destination_folder: path where matching files should move
        
        """
        super().__init__(self, description, enabled)
        # Call new parms
        self.target_extension = target_extension.lower()
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
        
        return file_name.endswith(self.target_extension)
    
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
                
                if rule.enabled:
                    
                    # Check if rule applies to the file and then call our method when we have a match
                    
                    if rule.applies_to(file_info):
                        
                        # Execute the action on the file when all criteria has been met
                        
                        rule.apply(file_info)
                        
                        
class FallBack(Rule):
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
        pass