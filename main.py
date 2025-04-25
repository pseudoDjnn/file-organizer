import os
import shutil
from pathlib import Path

def main():
    home = Path.home()

    desktop = home / "Desktop"
    print("Desktop Path:", desktop)
    
if __name__=="__main__":
    main()