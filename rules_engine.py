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
    
    def apply(self):
        pass