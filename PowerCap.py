import subprocess
import os
import glob
import time

def execute(SourceLocation, LP, SP, LI, SI):
    lpc, spc, lic, sic = 100, 100, 100, 100
   # Benchmark = ["2mm","seidel-2d","atax"]

    # Run initial command
    output_folder = "Output"
    output_folder_path = os.path.join(".", output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Process LP array
    for i in range(len(LP) - 1):
        subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "0", "-l", LP[i]])
        for j in range(len(SourceLocation) - 1):
            subprocess.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            move_output_files(SourceLocation[j],extract_folder_name(SourceLocation[j])+"Output")
            time.sleep(5)

    subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "0", "-l", lpc])
    # Process SP array
    for i in range(len(SP) - 1):
        subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "1", "-l", SP[i]])
        for j in range(len(SourceLocation) - 1):
            subprocess.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            move_output_files(SourceLocation[j], extract_folder_name(SourceLocation[j])+"Output")
            time.sleep(5)
    
    subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "1", "-l", spc])
    
    # Process LI array
    for i in range(len(LI) - 1):
        subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "0", "-s", LI[i]])
        for j in range(len(SourceLocation) - 1):
            subprocess.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            move_output_files(SourceLocation[j] ,extract_folder_name(SourceLocation[j])+"Output")
            time.sleep(5)     


    subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "0", "-s", lic])    
    # Process SI array
    for i in range(len(SI) - 1):
        subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "1", "-s", SI[i]])
        for j in range(len(SourceLocation) - 1):    
            subprocess.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            move_output_files(SourceLocation[j], extract_folder_name(SourceLocation[j])+"Output")
            time.sleep(5)

def move_output_files(SourceLocation ,output_folder):
    # Create the "ThisOutput" folder if it doesn't exist
    output_folder_path = os.path.join(".", output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Move all files in the source location to the "ThisOutput" folder
    files = glob.glob(os.path.join(SourceLocation, "*.pdf"))
    for file in files:
        if os.path.isfile(file):
            destination_file_path = os.path.join(output_folder_path, os.path.basename(file))
            os.rename(file, destination_file_path)

def extract_folder_name(path):
    folder_name = os.path.basename(os.path.dirname(path))
    return folder_name


def userinputSelection ():

    NumSource = int(input("Enter the number of source: "))
    for i in range(NumSource):
        SourceLocation[i] = input("Enter the source location: ")


    choice = input("Enter your choice, 1 for jumping . 2 for providing values: ")
    if choice == '1':
        NumLP = int(input("Enter the number of LP: "))
        for i in range(NumLP):
            LP.append (int(input("Enter the Long power values: ")))
        
        NumSP = int( input("Enter the number of SP: "))
        for i in range(NumSP):
            SP.append(int(input("Enter the Short power values: ")))

        NumLI = int(input("Enter the number of LI: "))
        for i in range(NumLI):
            LI.append(int( input("Enter the Long interval values: ")))

        NumSI = int(input("Enter the number of SI: "))
        for i in range(NumSI):
            SI.append(int(input("Enter the Short interval values: ")))


    elif choice == '2':
        print("Providing values")
        NumChanges = input("Enter the number of input: ")
        ChangeValue = input("Enter the value to jump: ")
        choice2 = input("Enter your choice, 1 default of system, 2 for providing value: ")
        if choice2 == '1':
            LP.append( 100)
            SP.append( 100)
            LI.append (100)
            SI.append (100)
        else :
            LP.append(int(input("Enter the Long power values: ")))
            SP.append(int(input("Enter the Short power values: ")))
            LI.append(int(input("Enter the Long interval values: ")))
            SI.append(int(input("Enter the Short interval values: ")))
        for i in range(0,NumChanges -2):
            LP[i+1] = LP[i] + ChangeValue
            SP[i+1] = SP[i] + ChangeValue
            LI[i+1] = LI[i] + ChangeValue
            SI[i+1] = SI[i] + ChangeValue

    else:
        print("Invalid input")


# Example usage:
SourceLocation = ["/path/to/source1", "/path/to/source2", "/path/to/source3"]#subprocess.run(["sudo", "rapl-set", "--zone=0", "-c", "1", "-l", "5000000"])
LP = [1, 2, 3, 4]  # Replace with actual LP values
SP = [10, 20, 30]  # Replace with actual SP values
LI = [100, 200, 300, 400]  # Replace with ac tual LI values
SI = [1000, 2000]  # Replace with actual SI values

execute(SourceLocation, LP, SP, LI, SI)
