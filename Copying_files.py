import os
import shutil

def copy_files(source_folder_path, destination_folder_path):
    os.makedirs(destination_folder_path, exist_ok=True)

    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder_path, file)
            shutil.copy(file_path, destination_path)

    print("Files copied successfully.")

# Example usage
source_folder_name = 'source'
destination_folder_name = 'destination'

# Search for the 'source' folder in the current working directory and get its path
source_folder_path = os.path.join(os.getcwd(), source_folder_name)

# Create the destination folder path relative to the current working directory
destination_folder_path = os.path.join(os.getcwd(), destination_folder_name)

# Prompt the user to enter the source and destination folder paths
source_folder_path = input("Enter the path of the source folder: ")
destination_folder_path = input("Enter the path of the destination folder: ")

copy_files(source_folder_path, destination_folder_path)
