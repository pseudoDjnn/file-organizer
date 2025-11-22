import os
import datetime
import getpass

class FileItem:
    def __init__(self, path, owner=None):
    #  Stores the full file path as string (e.g. "/home/user/photos/photo.jpg")
        self.path = path
    #  Extract just the filename (e.g. photo.jpg)
        self.name = os.path.basename(path)
    #  Splits our filename to the root and then makes it lowercase for ease of use
        self.extension = os.path.splitext(self.name)[1].lower()
    #  Get files bytes (Useful for rules)
        self.size = os.path.getsize(path)
    #  Get the files creation time (helps use configurations easier later on)
        self.created = datetime.datetime.fromtimestamp(os.path.getctime(path))
    #  Get the date last modified (Useful for rules)
        self.modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        
    # Grants business like ownership (e.g. teams, projects, individuals, etc...)
        self.owner = owner if owner else getpass.getuser()
        
    def year_created(self):
        """
        
        Grab the year the file was created and return it
        
        """
        return self.created.year
    
    def month_created(self):
        """

        Grab the month the file was created and return it
        
        """
        return self.created.month
    
    def day_created(self):
        """

        Grab the day the file was created and return it
        
        """
        return self.created.day
    
    def __repr__(self):
        pass