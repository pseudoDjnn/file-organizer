import logging

def logger(log_filename="app.log"):
    """

    Logger setup for the app.
    
    Args:
        log_filename (str): Where logs are written
    
    """
    logging.basicConfig(
        filename=log_filename,
        
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        # Append so new logs to be added
        filemode="a"
    )