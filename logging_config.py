import os
import logging

def setup_logger(log_filename="app.log"):
    """

    Logger setup for the app.
    
    Args:
        log_filename (str): Where logs are written
    
    """

    # print("setup_logger() is being called.")
    
    # # Convert the log filename to an absolute path
    # full_log_path = os.path.abspath(log_filename)
    # print("Logging to:", full_log_path)  # Debug print
    
    
    logging.basicConfig(
        
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_filename,
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
    
    logger = logging.getLogger()
    logger.addHandler(console_handler)