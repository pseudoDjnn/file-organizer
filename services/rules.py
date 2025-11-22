import os

def filter_excluded(files, excluded_items, excluded_ext):
    return [
        file for file in files
        if file.name not in excluded_items
        and not file.name.lower().endswith(tuple(excluded_ext))
    ]

def group_by_date(files, depth="month"):
    pass

def build_destination(base_dir, file, depth="month"):
    pass