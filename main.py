from pathlib import Path

def get_desktop_defaults():
    
    one_drive_desktop = Path("/mnt/c/Users/lavah/OneDrive/Desktop")
    standard_desktop = Path("/mnt/c/Users/lavah/Desktop")
    
    desktop_defaults = {}
    
    if one_drive_desktop.exists():
        desktop_defaults["OneDriveDesktop"] = one_drive_desktop
    else:
        print(f"OneDrive not found at {one_drive_desktop}")
    
    if standard_desktop.exists():
        desktop_defaults["StandardDesktop"] = standard_desktop
    else:
        print(f"Desktop not found at {standard_desktop}")
    
    return desktop_defaults

def get_active_desktop(desktop_defaults: dict):
    
    if "OneDriveDesktop" in desktop_defaults:
        print("Using OneDrive:", desktop_defaults["OneDriveDesktop"])
        return desktop_defaults["OneDriveDesktop"]
    elif "StandardDesktop" in desktop_defaults:
        print("Using Desktop:", desktop_defaults["StandardDesktop"])
        return desktop_defaults["StandardDesktop"]
    else:
        print("No Desktop found...")
        return None

def main():
    # Get candidate desktop defaults
    desktop_defaults = get_desktop_defaults()
    # print(f"DEBUGGING", desktop_defaults)
    
    # Print the defaults
    if desktop_defaults:
        print("Your Desktop has been found:")
        for key, path in desktop_defaults.items():
            print(f"  {key}: {path}")
    else:
        print("No candidate Desktop directories were found.")
    
    # # Choose and print the active desktop directory.
    active_desktop = get_active_desktop(desktop_defaults)
    if active_desktop:
        print("Active Desktop directory is:", active_desktop)
    else:
        print("Aborting: No active Desktop directory found.")

if __name__ == "__main__":
    main()