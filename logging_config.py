import os
import logging
from config import LOGS_FOLDER

def setup_logger(log_filename="app.log", base_directory=os.getcwd()):
    """

    Logger setup for the app.
    
    Args:
        log_filename (str): Where logs are written
        base_directry: Grab the path we point to for folder to be made in same location as organized files
    
    """
    
    logs_folder = os.path.join(base_directory, LOGS_FOLDER)

    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    
    full_log_path = os.path.join(logs_folder, log_filename)
    
    logging.basicConfig(
        
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=full_log_path,
        # Append so new logs to be added
        filemode="a"
    )
    
    # Create a console handler and set its logging level
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create a formatter and attach it to the console 
    
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    
    # Get the root logger and add the console handler if its not already there
    
    logging.getLogger().addHandler(console_handler)
    
    logging.info(f"Log file will be written to:  {full_log_path}")
    
    