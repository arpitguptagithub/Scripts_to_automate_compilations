import os
import subprocess
import shutil

def compile_files(folder_path, output_folder_path, compile_command):
    os.makedirs(output_folder_path, exist_ok=True)
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.c'):
                file_path = os.path.join(root, file)
                output_file = file.replace('.c', '.out')
                output_subfolder = os.path.relpath(root, folder_path)
                output_path = os.path.join(output_folder_path, output_subfolder, output_file)
                
                if not os.path.exists(output_path) or os.path.getmtime(file_path) > os.path.getmtime(output_path):
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    subprocess.call([compile_command, file_path, '-o', output_path])

# Example usage
folder_name = 'codes'
output_folder_name = 'output'

# Search for the 'codes' folder in the current working directory and get its path
folder_path = os.path.join(os.getcwd(), folder_name)

# Create the output folder path relative to the current working directory
output_folder_path = os.path.join(os.getcwd(), output_folder_name)

# Available compiler command options
compiler_options = {
    'gcc': 'gcc',
    'clang': 'clang',
    'msvc': 'cl'
}

# Display the available options to the user
print("Available compiler options:")
for key in compiler_options:
    print(f"{key}: {compiler_options[key]}")

# Prompt the user to select a compiler command
selected_option = input("Enter the desired compiler option: ")

# Get the selected compiler command based on the user's choice
compile_command = compiler_options.get(selected_option.lower())

if compile_command:
    compile_files(folder_path, output_folder_path, compile_command)
else:
    print("Invalid compiler option selected.")
