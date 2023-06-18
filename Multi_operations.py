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

def perform_operation(operation):
    if operation == 'compile':
        # Example compile operation
        folder_name = 'codes'
        output_folder_name = 'output'

        # Search for the 'codes' folder in the current working directory and get its path
        folder_path = os.path.join(os.getcwd(), folder_name)

        # Create the output folder path relative to the current working directory
        output_folder_path = os.path.join(os.getcwd(), output_folder_name)

        # Prompt the user to enter the compiler command
        compile_command = input("Enter the compiler command: ")

        compile_files(folder_path, output_folder_path, compile_command)
        print("Compilation complete.")

    elif operation == 'other_operation':
        # Example of another operation
        print("Performing another operation...")
        # Add the code for the desired operation here

    else:
        print("Invalid operation selected.")

# Available operations
operations = {
    '1': 'Compile',
    '2': 'Other Operation',
}

# Display the available operations to the user
print("Available operations:")
for key in operations:
    print(f"{key}: {operations[key]}")

# Prompt the user to select an operation
selected_option = input("Enter the desired operation number: ")

# Get the selected operation based on the user's choice
selected_operation = operations.get(selected_option)

if selected_operation:
    perform_operation(selected_operation.lower())
else:
    print("Invalid operation number selected.")
