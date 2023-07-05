#base) dvfstest2@ullman:~$ cat power_cap_frequency_plot2.py
#Before running the script apply the power cap 
#Script will ask for execution  command 
#make sure the script has taskset -c 0 i.e run the binary on the isolcpus=0 
#script will sample all core frquency for about 10 samples per second 
#script wil finally provide a frequency plot vs exec time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Process,cpu_count,Value,Queue
import sys
import glob
import time
import shutil
import os
import subprocess as sp
import time
from pathlib import Path
import csv
#import pp
from datetime import datetime
#import psutil
import os

#freq_res=[]
#stop_freq_sample_thread=False
print("cpu count is :",cpu_count())
home=Path.home()
sync_file=str(home)+"/sync_file.txt"


SourceLocation = []
LP = []  # Replace with actual LP values
SP = []  # Replace with actual SP values
LI = []  # Replace with ac tual LI values
SI = []  # Replace with actual SI values





def enter_exec_command(exec_command,stop,exec_time):
    #check wether command has 'sudo taskset -c 0' in it 
    #global stop_freq_sample_thread
    pid=os.getpid()
    sp.check_call(["sudo","taskset","-p","-c","0",str(pid)])
    #sub_commnd="sudo taskset -c"
    #if sub_commnd not in exec_command:
    #    print("pin the binary on cpu 0 using taskset" )
    #    sys.e{'Zone 0': {'name': ' uncore', 'enabled': ' 0', 'long_power': 0.0, 'long_interval': 976.0, 'short_power': 250000000.0, 'short_interval': 7808.0}, 'Subzone 0': {'name': ' uncore', 'enabled': ' 0', 'long_power': 0.0, 'long_interval': 976.0, 'short_power': 250000000.0, 'short_interval': 7808.0}, 'Subzone 1': {'name': ' uncore', 'enabled': ' 0', 'long_power': 0.0, 'long_interval': 976.0, 'short_power': 250000000.0, 'short_interval': 7808.0}}
    #xit("TERMINATING..")    
    comm=exec_command.split()
    comm=["sudo"]+comm
    print(comm)
    e_time=sp.run(comm,check=True,stdout=sp.PIPE)
    stop.value=1
    exec_time.put(e_time.stdout)

    print("okokokokok")
    

def sample_core_frequency(home,stop,Qu):
    #global stop_freq_sample_thread
    #global freq_res
    #global sync_file
    pid=os.getpid()
    sp.check_call(["sudo","taskset","-p","-c","1",str(pid)])
    #freq_res=[]
    #freq_res.clear()
    command1 = "cat /proc/cpuinfo"
    command2 = "grep -E 'processor|MHz'"
    command3 = "head -n 2"
    command4 = "tail -n 1"
    #print("%%%%%%%%%%%%",stop_freq_sample_thread,datetime.now())
    while(stop.value == 0):
         print("^^^^^^^")
         #p1=sp.Popen(["cat","/proc/cpuinfo"],stdout=sp.PIPE,stderr=sp.PIPE)         
         #print(p1.stdout)
         #p2=sp.Popen(["grep" ,"-E","'processor|MHz'"],stdout=sp.PIPE,stdin=p1.stdout,stderr=sp.PIPE)
         #print(p2.stdout)
         #p3=sp.Popen(["head","-n","2"],stdout=sp.PIPE,stdin=p2.stdout,stderr=sp.PIPE)
         #print(p3.stdout)
         #p4=sp.Popen(["tail","-n","1"],stdout=sp.PIPE,stdin=p3.stdout,stderr=sp.PIPE)
         #print(p4.stdout)
         #res=p4.communicate()[0].decode()
         
         #command1 = "cat /proc/cpuinfo"
         #command2 = "grep -E 'processor|MHz'"
         #command3 = "head -n 2"
         #command4 = "tail -n 1"

         # Run command1
         p1 = sp.Popen(command1, stdout=sp.PIPE, shell=True)
         #print(p1.stdout)
         # Run command2 with the output of command1 as int(input
         p2 = sp.Popen(command2, stdin=p1.stdout, stdout=sp.PIPE, shell=True)
         #p2 = sp.Popen(command2, stdin=p1.stdout, stdout=sp.PIPE, shell=True)
         #print(p2.stdout)
         # Run command3 with the output of command2 as int(input
         p3 = sp.Popen(command3, stdin=p2.stdout, stdout=sp.PIPE, shell=True)
         #print(p3.stdout)
         # Run command4 with the output of command3 as int(input
         p4 = sp.Popen(command4, stdin=p3.stdout, stdout=sp.PIPE, shell=True)
         #print(p4.stdout)
         # Get the final output
         res = p4.communicate()[0]
         #res=sp.run(["cat","/proc/cpuinfo"],capture_output=True)
         print(res,"\n")
         #print("*******",stop_freq_sample_thread)
         #p1.wait()
         #p2.wait()
         #p3.wait()
         print("!!!",res)
         #res=sp.run(["cat","/proc/cpuinfo","|", "grep" ,"-E","'processor|MHz'","|","head","-n","2","|","tail","-n","1"],stdout=sp.PIPE)
         #freq_res.append(res)
         Qu.put(res)
         #with open(sync_file,'r') as f:
         #    if f.readlines()==["over"]:
         #        break
         time.sleep(0.01) # one reading after 10 ms
    #return freq_res
    with open(str(home)+"/freq_data.txt","wb") as dump:
        while(Qu.empty() is False):
            dump.write(Qu.get())
            #dump.write(b"\n")




def move_output_files(SourceLocation ,subfolder_name, subfolder_name2, output_folder):
    # Create the "ThisOutput" folder if it doesn't exist

    df= pd.read_csv("power_data.csv")

    output_folder_path = os.path.join(".", output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)


    subfolder_path = os.path.join(output_folder_path, subfolder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    
    subfolder_path2 = os.path.join(subfolder_path, subfolder_name2)
    if not os.path.exists(subfolder_path2):
        os.makedirs(subfolder_path2)


#     updated_df = df.append(new_data, ignore_index=True)

# # Change the file location of just the last row

# last_row_index = updated_df.index[-1]  # Get the index of the last row
# updated_df.at[last_row_index, 'file_location'] = 'new_file_location'

# # Write the updated DataFrame to a CSV file
# updated_df.to_csv('updated_data.csv', index=False)


    #update the location in last row


    # Move all files in the source location to the "ThisOutput" folder
    files = glob.glob(os.path.join(SourceLocation, "*.pdf"),recursive = True)
    for file in files:
        if os.path.isfile(file):
            destination_file_path = os.path.join(subfolder_path2, os.path.basename(file))
            print("destination of the file")
            print (destination_file_path)
            shutil.move(file, destination_file_path)
            lr= df.index[-1]
            df.at[lr,'file_location'] = destination_file_path
     
            # os.rename(file, destination_file_path)
    df.to_csv("power_data.csv",index=False)
    

def extract_folder_name(path):
    folder_name = os.path.basename(os.path.dirname(path))
    return folder_name


def userinputSelection ():

    NumSource = int(int(input("Enter the number of source: ")))
    for i in range(0,NumSource):
        SourceLocation.append( input("Enter the source location: "))


    choice = int(input("Enter your choice, 2 for jumping . 1 for providing values: "))
    if choice == 1:
        NumLP = int(input("Enter the number of LP: "))
        for i in range(0,NumLP):
            LP.append( int(input("Enter the Long power values: ")))
        
        NumSP = int(input("Enter the number of SP: "))
        for i in range(0,NumSP):
            SP.append( int(input("Enter the Short power values: ")))

        NumLI = int(input("Enter the number of LI: "))
        for i in range(0,NumLI):
            LI.append(int(input("Enter the Long interval values: ")))

        NumSI = int(input("Enter the number of SI: "))
        for i in range(0,NumSI):
            SI.append(int(input("Enter the Short interval values: ")))    


    elif choice == 2:
        print("Providing values")
        NumChanges = int(input("Enter the number of int(input: "))
        ChangeValue = int(input("Enter the value to jump: "))
        choice2 = int(input("Enter your choice, 1 default of system, 2 for providing value: "))
        if choice2 == 1:
            LP.append (100)
            SP.append (100)
            LI.append (100)
            SI.append (100)
        else :
            LP.append (int(input("Enter the Long power values: ")))
            SP.append(int(input("Enter the Short power values: ")))
            LI.append (int(input("Enter the Long interval values: ")))
            SI.append(int(input("Enter the Short interval values: ")))
        for i in range(1, NumChanges -2):
            LP[i+1] = LP[i] + ChangeValue
            SP[i+1] = SP[i] + ChangeValue
            LI[i+1] = LI[i] + ChangeValue
            SI[i+1] = SI[i] + ChangeValue

    else:
        print("Invalid int(input")




def execute(SourceLocation, LP, SP, LI, SI):
    lpc, spc, lic, sic = 1000000, 10000000, 10000000, 10000000
   # Benchmark = ["2mm","seidel-2d","atax"]
    fields = ["binary_name","watts_long","sec_long","watts_short","sec_short","file_location"]
    rows = ["" ," " , " ", " "]
    filename = "power_data.csv"
    with open(filename, 'w') as csvfile:
         csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
         csvwriter.writerow(fields) 
        
    # writing the data rows 
         csvwriter.writerows(rows)


    # Run initial command
    output_folder = "Output"
    # output_folder_path = os.path.join(".", output_folder)
    # if not os.path.exists(output_folder_path):
    #     os.makedirs(output_folder_path)
     

    CmdBaseC = "sudo rapl-set  --zone=0 -c "
    Cmdlp= CmdBaseC + "0 "+ "-l "
    Cmdsp= CmdBaseC + "1 "+ "-l "
    Cmdli= CmdBaseC + "0 "+ "-s "
    Cmdsi= CmdBaseC + "1 "+ "-s "

    Cmdlpr= CmdBaseC + "0 "+ "-l " + str(lpc)
    Cmdspr= CmdBaseC + "1 "+ "-s " +str(spc)
    Cmdlir= CmdBaseC + "0 "+ "-l " +str(lic)
    print (Cmdlir)
    #c1 , c2 ,c3, c4 
    # Process LP array
    for i in range(len(LP) ):
        print (Cmdlp+str(LP[i]))
        sp.run( (Cmdlp+str(LP[i]) ) ,shell = True)
        for j in range(len(SourceLocation) ):
             #sp.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            main(SourceLocation[j])
            subfolder_name = extract_folder_name(SourceLocation[j]) 
            subfolder_name2= "LP"
            move_output_files("/home/dvfstest2/", subfolder_name, subfolder_name2 ,output_folder)
            time.sleep(5)
        
    sp.run(Cmdlpr ,shell = True)
    # Process SP array
    for i in range(len(SP) ):
        sp.run((Cmdsp+ str(SP[i])), shell = True)
        for j in range(len(SourceLocation) ):
             #sp.run(["python3", "power_cap_frequency_plot2.py", SourceLocation[j]])
            main(SourceLocation[j])
            subfolder_name = extract_folder_name(SourceLocation[j]) 
            subfolder_name2= "SP"
            move_output_files("/home/dvfstest2/", subfolder_name,subfolder_name2, output_folder)
            time.sleep(5)
            

    sp.run(Cmdspr, shell =True)
    
    # Process LI array
    for i in range(len(LI) ):
        sp.run((Cmdli+str(LI[i])), shell =True)
        for j in range(len(SourceLocation) ):
            subfolder_name = extract_folder_name(SourceLocation[j]) 
            subfolder_name2= "LI"
            main(SourceLocation[j])
            move_output_files("/home/dvfstest2/", subfolder_name, subfolder_name2 ,output_folder)
            time.sleep(5)

    sp.run(Cmdlir ,shell =True)    
    # Process SI array
    for i in range(len(SI) ):
        sp.run((Cmdsi + str(SI[i])), shell = True)
        for j in range(len(SourceLocation)):    
            subfolder_name = extract_folder_name(SourceLocation[j]) 
            subfolder_name2= "SI"
            main(SourceLocation[j])
            move_output_files("/home/dvfstest2/", subfolder_name,subfolder_name2, output_folder)
            time.sleep(5)

# Example usage:


def main(SourceLocation):
    #print("%%%%%%%%%%%%",stop_freq_sample_thread,datetime.now())
    global home
    # rows=[]
    #global sync_file
    #job_server=pp.Server()


   #arpiT 
    #exec_comm=int(input("Input the Binary Exec Command!\n")
    
    
    
    exec_comm=SourceLocation
    #home=Path.home()
    #sync_file=str(home)+"/sync_file.txt"
    stop=Value('d',0)
    #exec_time=Value('char* ',"")
    Qu=Queue()
    Qu1=Queue()
    #exec_comm="/home/dvfstest2/PolyBenchC-4.2.1/linear-algebra/kernels/3mm/3mm.out"
    #exec_comm="bash /home/dvfstest2/PolyBenchC-4.2.1/linear-algebra/kernels/3mm/run.sh"
    binary_name=(((((exec_comm.split())[-1]).split("/"))[-1]).split("."))[0]
    #home=Path.home()
    #sync_file=str(home)+"/sync_file.txt"
    #sp.run(["touch",sync_file])
    #enter_exec_command(exec_comm)
    #T1=threading.Thread(target=enter_exec_command,args=(exec_comm,))
    #T2=threading.Thread(target=sample_core_frequency)
    P1=Process(target=enter_exec_command, args=(exec_comm,stop,Qu1))
    P2=Process(target=sample_core_frequency,args=(home,stop,Qu))
    #P1.cpu_affinity([0])
    #P2.cpu_affinity([1])
    #P1=Process(target=enter_exec_command, args=(exec_comm,))
    #P2=Process(target=sample_core_frequency)
    P1.start()
    P2.start()
    #f1=job_server.submit(enter_exec_command,(exec_comm,))
    #f2=job_server.submit(sample_core_frequency)
    #f1()
    #f2()
    print("****************** subprocess execution began ***********************")
    #enter_exec_command(exec_comm)
    #try:
    #    sp.check_call(exec_comm.split(),universal_newlines=True)
    #except sp.CalledProcessError as e:
    #    print(e)
    P1.join()
    #print("@@@@@@@@@@@",stop_freq_sample_thread)
    #i=int(input()
    P2.join()
    
    exec_time=(str(Qu1.get()).split(":")[-1].split("\n"))[0]
    print("list has\n",exec_time.split(":"))
    #print(Qu)

    print("\n\n !!!!!!!!!!!! EXECTION TIME IS : ",exec_time,"!!!!!!!!!!!!!!!!!!!!","\n\n")
    # **** THIS WILL EASE OUT MEMORY NEED ****
    home=Path.home()
    temp_freq=str(home)+"/temp_freq.txt"
    with open(str(home)+"/freq_data.txt","rb") as f1:
        l=f1.readlines()
        l1=[]
        for x in l:
            l1.append(float(((str(x).split(":")[-1]).strip()).split("\\n'")[0]))
        #print(l1)
        #print("\n\n\n")
        #print(len(l1))

    #chunk l1 in 8 parts and get average frequency for these 8 parts
    chunks=8
    chunked_l1=[]
    chunked_freq=[]
    x=0
    t=len(l1)//chunks
    y=t
    for a in range(chunks):
        #print("!!!!",x ,y)        
        avg=0.0
        for f in range(x,y):
            avg+=l1[f]
        avg=avg/(y-x+1)
        for _ in range(x,y):
            chunked_l1.append(avg)    

        chunked_freq.append(avg)
        x=y+1
        y+=t




            
    power_cap=sp.run(["sudo","rapl-info"],capture_output=True)
    #print(power_cap.stdout)
    power_c=(str(power_cap.stdout).split("\\n"))
    #print(power_c)
    zone_dict={}
    key=""
    for x in power_c:
        x1=((x.strip()).split("b'"))[-1]
        if "Zone" in x1 or "zone" in x1:                
            zone_dict[x1]=[]
            key=x1
        else:
            zone_dict[key].append(x1)
    #print(zone_dict)     
    #print("\n\n\n")

    df= pd.read_csv("power_data.csv")
    watts_long=0
    sec_long=0
    watts_short=0
    sec_short=0
    

    zone_const={}
    temp_dict={"name":"","enabled":"","long_power":"","long_interval":"","short_power":"","short_interval":""}
    to_display=""
    f=0
    for key in zone_dict.keys():
        zone_const[key]={"name":"","enabled":"","long_power":"","long_interval":"","short_power":"","short_interval":""}
        f=0
        for x in range(len(zone_dict[key])):
            z1=zone_dict[key][x]
            if "name" in z1 and f==0:
                z=z1.split(":")[-1].strip()
                zone_const[key]["name"]=z
                f=1
                #print(z)
            if "enabled" in z1:
                z=z1.split(":")[-1].strip()
                zone_const[key]["enabled"]=z
                #print(z)
                if z=="0":
                    break
            if "long_term" in z1:
                if "power_limit_uw" in  zone_dict[key][x+1]:
                    zone_const[key]["long_power"]=float(((zone_dict[key][x+1].split(":"))[-1]).strip())/1000000
                    watts_long= zone_const[key]["long_power"]
                    #print(zone_const[key]["long_power"])
                if "time_window_us" in zone_dict[key][x+2]:
                    zone_const[key]["long_interval"]=float(((zone_dict[key][x+2].split(":"))[-1]).strip())/1000000
                    #print(zone_const[key]["long_interval"])
                    sec_long= zone_const[key]["long_interval"]
                    
            if "short_term" in z1:
                if "power_limit_uw" in  zone_dict[key][x+1]:
                    zone_const[key]["short_power"]=float(((zone_dict[key][x+1].split(":"))[-1]).strip())/1000000
                    #print(zone_const[key]["short_power"])                    
                    watts_short= zone_const[key]["short_power"]

                if "time_window_us" in zone_dict[key][x+2]:    
                    zone_const[key]["short_interval"]=float(((zone_dict[key][x+2].split(":"))[-1]).strip())/1000000
                    #print(zone_const[key]["short_interval"])
                    sec_short= zone_const[key]["short_interval"]
                    
    #print(zone_const)
    for key in zone_const.keys():
        temp=""
        for x in zone_const[key].keys():
            if x =="enabled" and zone_const[key][x]=="0":
                temp=""
                break
            else:
                if isinstance(zone_const[key][x],float):
                    temp+=x+":"+str(round(zone_const[key][x],2))+" "
                else:
                    temp+=x+":"+str(zone_const[key][x])+" "

        to_display+=temp
    print(to_display)            


    new_data = pd.DataFrame({'binary_name': binary_name, 'watts_long' : watts_long ,'sec_long': sec_long ,'watts_short': watts_short,'sec_short':sec_short , 'file_location' : ["empty"]})

# Append the new DataFrame to the existing DataFrame
    df = df.append(new_data, ignore_index=True)
    df.to_csv("power_data.csv",index=False)

    # rows = [[binary_name,watts_long,sec_long,watts_short,sec_short,"empty"]]
    
    # rows.append([ binary_name, watts_long ,sec_long, watts_short ,sec_short  ,"empty"])

    # filename = "power_data.csv"
    # with open(filename, 'w') as csvfile:
    #      csvwriter = csv.writer(csvfile) 
        
    # # writing the fields 
    #      csvwriter.writerow(fields) 
        
    # # writing the data rows 
    #      csvwriter.writerows(rows)


    #print(binary_name+" {Isolcpus=0} at \n",to_display)
    #plt.axis([1200,4000,0,len(l1)+10])
    #plt.plot(l1,linestyle="dashed")
    plt.figure(figsize=(30,20))
    plt.title(binary_name+" {Isolcpus=0} at "+to_display,loc='center',fontsize="xx-large",fontweight='bold')
    plt.axis([0,len(l1)+10,50,6000])
    plt.plot(l1,linestyle="dashed")
    actual_x=list(range(len(l1)))
    axis=plt.gca()
    xticks=axis.get_xticks()
    yticks=axis.get_yticks()
    #print(actual_x)
    #print(xticks)
    #print("\n\n")
    #print(yticks)
    vline_x_coord=[]
    vline_y_coord=[]
    for a in range(chunks-1):
        vline_x_coord.append(actual_x[(a+1)*t])
        vline_y_coord.append(l1[(a+1)*t])

    plt.plot(chunked_l1,linestyle="dotted",color='red')
    for x in range(len(vline_x_coord)):
        #print(str(round(float(chunked_freq[x]),2)))
        plt.vlines(vline_x_coord[x],0,vline_y_coord[x]-5.0,linestyles='solid',label="region "+str(x+1)+":  "+str(round(float(chunked_freq[x]),2))+"MHz",color='green')
    
    plt.xlabel("Ticks{0 -> Execution time}",fontsize="x-large",fontweight='bold')
    plt.ylabel("CPU-0 Freq(MHz)",fontsize="x-large",fontweight='bold')
    plt.xticks(fontsize='large')
    plt.yticks(fontsize=20)
    plt.legend(title="Per-Region(left to right) Average Freq")
    #plt.figure(figsize=(30,20))
    #plt.plot(l1,linestyle="dashed")
    #plt.show()
    d=str(datetime.now())
    plt.savefig(str(home)+"/"+binary_name+"_"+d+".pdf",dpi=300)
    #for x in range(len(freq_res)):
        #f1.write(freq_res[x].split(":").strip())
#freq_res.clear()

#with open(temp_freq,"r") as f1:
#    lines=f1.

#if __name__ == "__main__" :
 #   main()

#if __name__ == "__userinputSelection__" :

userinputSelection()  
execute(SourceLocation, LP, SP, LI, SI)
