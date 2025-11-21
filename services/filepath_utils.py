class FilePathUtils:
    def __init__(self, max_length=50):
        """
        
        Init for the class.
        
        Parameters:
            max_length (int): Max length of the string before we shorten
        
        """
        
        self.max_length = max_length
        
        
    def shortener(self, path):
        """
        
        Just shortens the file path name if it reaches the set max_length.
        
        Parameters:
            path (str): Our full file path
            
        Return:
            A string that is a shortened version of the file path itself
        
        """
        
        if len(path) <= self.max_length:
            return path
        
        # Reserve 3 characters for the ellipsis '...'
        
        part_len = (self.max_length - 3) // 2
        return path[:part_len] + "..." + path[-part_len:]