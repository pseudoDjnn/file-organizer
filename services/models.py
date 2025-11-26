import os
import datetime
import getpass

class FileItem:
    def __init__(self, path, owner=None):
        """
        Represents a single file in the system with our metadata.
        
        Parameters:
            path (str): Full file path (e.g. "/home/user/photos/photo.jpeg")
            owner (str, optional): Logical owner of the file (team, project, user) 
                                                    Defaults to current system user.
        """
        
    #  Full path to file

        self.path = path
        
    #  Extract just the filename (e.g. photo.jpg)
    
        self.name = os.path.basename(path)
        
    #  FIle extension (e.g. "jpeg"), normalized to lowercase for consistency

        self.extension = os.path.splitext(self.name)[1].lower()
        
    #  Get files bytes (e.g. "skip tiny files" or "group by size")
    
        self.size = os.path.getsize(path)
        
    #  Create timestamp (datetime object) - help with chronology
    
        self.created = datetime.datetime.fromtimestamp(os.path.getctime(path))
        
    #  Last modification timestamp (datetime object) - useful for "recently updated" rules
    
        self.modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        
    # Logical owner (defaults to current system user if not provided)
    
    # This allows business-like ownership (teams, projects, individuals)
    
        self.owner = owner if owner else getpass.getuser()
        
    def year_created(self):
        """Return the year the file was created (int)"""
        return self.created.year
    
    def month_created(self):
        """Return the month the file was created (int, 1-12)"""
        return self.created.month
    
    def day_created(self):
        """Return the day of the month the file was created (int, 1-31)"""
        return self.created.day
    
    def __repr__(self):
        """
        Dev friendly (str) representation of the FileItem.
        Shows key metadata for quick debugging.
        """
        return (f"<FileItem name={self.name}, ext={self.extension}, >"
                f"size={self.size}, bytes, owner={self.owner}")