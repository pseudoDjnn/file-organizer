from pathlib import Path

def get_desktop_defaults():
    
    paths_for_clients = {
        "OneDrive": Path("/mnt/c/Users/lavah/OneDrive/Desktop"),
        "WindowsOS": Path("/mnt/c/Users/lavah/Desktop")
    }
    
    desktop_defaults = {}
    
    for key, path in paths_for_clients.items():
        try:
            if path.exists():
                desktop_defaults[key] = path
        except Exception as e:
            raise Exception(f"Error checking {key} at {path}: {e}")
    
    
    if not desktop_defaults:
        raise FileNotFoundError("Path not found: {key} or {path}")
    return desktop_defaults

def get_active_desktop(desktop_defaults: dict):
    
    if "OneDrive" in desktop_defaults:
        # print("Using OneDrive:", desktop_defaults["OneDriveDesktop"])
        return desktop_defaults["OneDrive"]
    elif "WindowsOS" in desktop_defaults:
        # print("Using Desktop:", desktop_defaults["StandardDesktop"])
        return desktop_defaults["WindowsOS"]
    else:
        raise FileNotFoundError("No valid entry...")
    
def get_system_folder_path(onedrive_directory=True):

    if onedrive_directory:
        directory_to_use = Path("mnt/c/Users/lavah/OneDrive/")
    else:
        directory_to_use = Path("mnt/c/Users/lavah/")
        
        return {
            "Documents": directory_to_use / "Documents",
            "Pictures": directory_to_use / "Pictures",
            "Music": directory_to_use / "Music",
            "Videos": directory_to_use / "Videos",
        }

def main():
    # Get candidate desktop defaults
    desktop_defaults = get_desktop_defaults()
    # print(f"DEBUGGING", desktop_defaults)

    clients_active_desktop = get_active_desktop(desktop_defaults)
    print(f"Now Running on {clients_active_desktop}")    
    

if __name__ == "__main__":
    main()