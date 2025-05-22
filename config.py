# Dictionary defining file categories and their associated extensions
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Data": [".csv", ".json", ".xml"],

    # Unrecognized files will go here
    "Others": []
}

# Made to not tamper with a Windows Desktop
EXCLUDED_ITEMS = {

    # Common Windows system file
    "desktop.ini",
    
    # Virtual folder (if it appears)
    "This PC",
    "Recycle Bin",
    "Network",
    
    # Default OneDrive shortcut
    "OneDrive",
    
    # Legacy config
    "Control Panel"
}

# File extensions we are not wanting to include
EXCLUDED_EXT = {
    ".exe"
}

# Defines how many years of files should be organized (past 5 years)
YEAR_RANGE = 5

# Define log filename for review
# LOG_FILE = "unexpected_dates.log"