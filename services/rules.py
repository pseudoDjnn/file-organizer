import os
from services.models import FileItem


def filter_excluded(files, excluded_items, excluded_ext):
    return [
        file for file in files
        if file.name not in excluded_items
        and not file.name.lower().endswith(tuple(excluded_ext))
    ]

def group_by_date(files, depth="month"):
#  Empty dictyionary we append into later in the func
    grouped = {}
#  Move through out files with a loop
    for file in files:
    # This is looking only for the "year"
        if depth == "year":
            key = file.year_created()
    # This is looking for the "year" and "month"
        elif depth == "month":
            key = (file.year_created(), file.month_created())
    # This is looking for the "year" and "month" and "day"
        elif depth == "day":
            key = (file.year_created(), file.month_created(), file.day_created())
    #  Insert the logic into the dictionary insuring there is always a list at the key
        grouped.setdefault(key, []).append(file)    
    return grouped

def build_destination(base_dir, file, depth="month"):
    """

    Build the destination folder path based on owner and date
    
    """
    
#  Start with owner
    base_dir = os.path.join(base_dir, file.owner)
    
#  Always include which year
    year = str(file.year_created())
    
    if depth == "year":
        return os.path.join(base_dir,year)
    
    month = f"{file.month_created():02d}"
    if depth == "month":
        return os.path.join(base_dir, year, month)
    
    day = f"{file.day_created():02d}"
    if depth == "day":
        return os.path.join(base_dir, year, month, day)
    
    raise ValueError(f"Unsupported depth: {depth}")