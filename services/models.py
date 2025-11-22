import os
import datetime

class FileItem:
    def __init__(self, path):
    #  Stores the full file path as string (eg. "/home/user/photos/photo.jpg")
        self.path = path
    #  Extract just the filename (eg. photo.jpg)
        self.name = os.path.basename(path)
    #  Splits our filename to the root and then makes it lowercase for ease of use
        self.extension = os.path.splitext(self.name)[1].lower()
    #  Get files bytes (Useful for rules)
        self.size = os.path.getsize(path)
    #  Get the files creation time (helps use configurations easier later on)
        self.created = datetime.datetime.fromtimestamp(os.path.getctime(path))
    #  Get the date last modified (Useful for rules)
        self.modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        
    def year_created(self):
        pass
    
    def __repr__(self):
        pass