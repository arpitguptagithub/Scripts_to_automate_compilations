import os

def search_files(folder_path, file_extension):
    found_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                found_files.append(file_path)

    return found_files

# Example usage
folder_name = 'my_folder'
file_extension = '.txt'

# Search for the 'my_folder' folder in the current working directory and get its path
folder_path = os.path.join(os.getcwd(), folder_name)

# Prompt the user to enter the file extension to search for
file_extension = input("Enter the file extension to search for: ")

# Perform the file search
results = search_files(folder_path, file_extension)

# Display the results
if results:
    print(f"Found {len(results)} files with the extension '{file_extension}':")
    for file_path in results:
        print(file_path)
else:
    print(f"No files found with the extension '{file_extension}' in the folder '{folder_path}'.")
