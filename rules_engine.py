

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
            return: True is theis rule applies and False is not
        
        """
    
    def apply(self, file_path):
        """
        
        Carry out the action of the rule method above on the file.
        
        Parameter:
            file_path:  dict with file metadata.
        
        """