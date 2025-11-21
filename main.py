import logging
from logging_config import setup_logger

from services.file_organizer import FileOrganizer
from ui.project_gui import OrganizerGUI

setup_logger()

# Get our logger form config
logger = logging.getLogger(__name__)


def main():
    """
    Main execution function prompting user for a directory path.
    """

    logging.info("File Organizer started.")
    
    directory_to_organize = input("Enter the directory path to organize: ")
    try:
        organizer = FileOrganizer(directory_to_organize)

        organizer.organize_files()
        logger.info(f"Files organized in directory: {directory_to_organize}")
    except Exception as e:
        logger.error(f"An error occurred during the organization: {e}")
        print(f"An error occured: {e}")
    
if __name__ == "__main__": 
    gui = OrganizerGUI()
    gui.run()