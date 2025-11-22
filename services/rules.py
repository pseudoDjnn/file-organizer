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
    pass