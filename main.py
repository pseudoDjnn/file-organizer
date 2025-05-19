from file_organizer import organize_files

def main():
    """
    Main execution function prompting user for a directory path.
    """
    directory_to_organize = input("Enter the directory path to organize: ")
    organize_files(directory_to_organize)

    
if __name__ == "__main__": 
    main()