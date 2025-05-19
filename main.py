import logging
from file_organizer import organize_files


def main():
    """
    Main execution function prompting user for a directory path.
    """

    logging.info("File Organizer started.")
    
    directory_to_organize = input("Enter the directory path to organize: ")
    try:
        organize_files(directory_to_organize)
        logging.info(f"Files organized in directory: {directory_to_organize}")
    except Exception as e:
        logging.error(f"An error occurred during the organization: {e}")
        print(f"An error occured: {e}")
    
if __name__ == "__main__": 
    main()