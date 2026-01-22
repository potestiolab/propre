import os 
import math 
import argparse

from multiprocessing import cpu_count

from .inp_out import *
from .general import * 


# Function: it checks if empty rows are present in a file in 'Hs-Hk-Nsites.py' program 
def checking_empty_rows_HsHkplot(FileName, File):
    for line in FileName:
        if len(line.strip()) == 0:
            print("\n####################################################################################")
            print("ERROR. In '{}' there is, at least, an empty row. Check it out...\n".format(File))
            print("       Be sure that this file does not contain empty rows and that it is organized in 3 rows: ")
            print("        ○ Resolution (Hs)")
            print("        ○ Relevance (Hk)")
            print("        ○ Nsites (N)")
            print("       Look below for further information")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
    
    FileName.seek(0)
    


# Checking that the number of row is 3. An error is returned if the number of rows is less or larger or smaller of 3. 
def checking_three_rows(FileName, File):
    Nrows = len(FileName.readlines())
    if(Nrows != 3):
        print("\n####################################################################################")
        print("ERROR. The number of lines of '{}' file is {}.".format(File, Nrows))
        print("       Be sure that this file does not contain empty rows and that it is organized in 3 rows: ")
        print("        ○ Resolution (Hs)")
        print("        ○ Relevance (Hk)")
        print("        ○ Nsites (N)")
        print("       Look below for further information.")
        print("####################################################################################\n\n")
        if(sys.argv[1]=="density"):
            print_help_density_HsHkplot()
        if(sys.argv[1]=="bin"):
            print_help_bin_HsHkplot()
        quit()
        
    FileName.seek(0)    
    

# Checking that the 1st row, corresponding at Resolution (Hs), is composed by float(or int) numbers (strings or special characters like comma (,) are not accepted)
def checking_1st_row_int_float(FileName):
    Hs = FileName.readline()
    Hs = Hs.split(" ")
    Hs = [i for i in Hs if(i !="\n" and i !="")]
    for i in Hs:
        i = check_Int_Float_Str(i)
        if(isinstance(i, str)):
            print("\n####################################################################################")
            print("ERROR. The 1st row, corresponding at Resolution (Hs) must contain only integer or float numbers.")
            print("       {} is a string. Check it out and fix the error, please.".format(i))
            print("       Look below for further information.")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
            
    Hs = [float(i) for i in Hs if(i !="\n")] 
       
    return Hs 



# Checking that the 2nd row, corresponding at Relevance (Hk), is composed by float (or int) numbers (strings or special characters like comma (,) are not accepted)
def checking_2nd_row_int_float(FileName):
    Hk = FileName.readline()
    Hk = Hk.split(" ")
    Hk = [i for i in Hk if(i !="\n" and i !="")]   
    for i in Hk:
        i = check_Int_Float_Str(i)
        if(isinstance(i, str)):
            print("\n####################################################################################")
            print("ERROR. The 2nd row, corresponding at Relevance (Hk) must contain only integer or float numbers.")
            print(f"       '{i}' is a string. Check it out and fix the error, please.")
            print("       Look below for further information.")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
            
    Hk = [float(i) for i in Hk if(i !="\n")]
    
    return Hk
    

# Checking that the 3rd row, corresponding at NSites (N), is composed by or integer numbers (strings, float, or special characters like comma (,) are not accepted)
def checking_3rd_row_int(FileName):
    N  = FileName.readline()
    N  = N.split(" ")
    N  = [i for i in N if(i !="\n" and i !="")]
    for i in N: 
        i = check_Int_Float_Str(i)
        if(isinstance(i, str)):
            print("\n####################################################################################")
            print("ERROR. The 3rd row, corresponding at NSites (N) must contain only integer numbers.")
            print(f"       '{i}' is a string. Check it out and fix the error, please.")
            print("       Look below for further information.")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
            
        if(isinstance(i, float)):
            print("\n####################################################################################")
            print("ERROR. The 3rd row, corresponding at Nsites (N) must contain only integer numbers.")
            print(f"       '{i}' is a float number. Check it out and fix the error, please.")
            print("       Look below for further information.")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
    
    N  = [int(i) for i in N if(i !="\n")]
    
    return N 
    

# Checking that the number of points is identical for both resolution, Relevance, and NSites. 
def checking_number_elements(Hs, Hk, N):
    Number_Hs = len(Hs)
    Number_Hk = len(Hk)
    Number_N  = len(N)

    if((Number_Hs != Number_Hk) or (Number_Hk != Number_N) or (Number_Hk != Number_N)):   
        print("\n####################################################################################")
        print("ERROR. Each row must contain the same number of elements:")
        print(f"        ○ The 1st row corresponding at Resolution (Hs) has {Number_Hs} elements.")
        print(f"        ○ The 2nd row corresponding at Relevance (Hk) has {Number_Hk} elements.")
        print(f"        ○ The 3rd row corresponding at Nsites (N) has {Number_N} elements.")
        print("       Please fix the error.")
        print("       Look below for further information.")
        print("####################################################################################\n\n")
        if(sys.argv[1]=="density"):
            print_help_density_HsHkplot()
        if(sys.argv[1]=="bin"):
            print_help_bin_HsHkplot()
        quit()   


# Function: Checking if a mandatory file actually found or not. 
def checking_file_found(FileName):
    if not os.path.isfile(FileName):
        print("\n####################################################################################")
        print("ERROR. Error while opening the file. '{}' does not exist.\n".format(FileName))
        print("####################################################################################\n\n")
        print_usage_ResRel()
        quit()



# Function: Printing help message if 'Hs-Hk-plot.py' does not present valid arguments: 
#           in particular, the first argument must be 'density' or 'bin' according the user choice.
def checking_accepted_tasks_HsHkplot():
    found = False 
    tasks = ['density', 'bin']
    
    for tk in tasks:
        if(sys.argv[1] == tk):
            found = True 
               
    if(found == False): 
        if(sys.argv[1].strip() == "--usage") or (sys.argv[1].strip() == "-u"):
            print_usage_HsHkplot() 
            quit()

        if(sys.argv[1].strip() == "--help" or sys.argv[1].strip() == "-h"):
            print_shorthelp_HsHkplot()  
            quit()
        
        print("\n####################################################################################")    
        print("ERROR. '{}' not in the list of accepted tasks!\n".format(sys.argv[1]))
        print("       Be sure that either 'bin' or 'density' task is the first argument. Other tasks are not allowed.")
        print("       Look below for more information.")
        print("####################################################################################\n\n")
        print_usage_HsHkplot()    
        quit()
        

# Function: Parsing arguments, printing error and help message if 'Hs-Hk-plot.py' presents not allowed arguments, and checking if mandatory files are present 
def checking_valid_arguments_HsHkplot(parser):
    try:
        args  = parser.parse_args()
    except SystemExit:
        print("\n####################################################################################")    
        print("ERROR. Arguments with no flag are not allowed. Check that each flag (e.g. -f) is followed by its specific argument")
        print("       Look below for more information.")
        print("####################################################################################\n\n")
        if(sys.argv[1]=="density"):
            print_help_density_HsHkplot()
        if(sys.argv[1]=="bin"):
            print_help_bin_HsHkplot()
        quit()
        
        
#Function: Parsing arguments, printing error and help message if 'removeH.py' presents not allowed arguments, and checking if mandatory files are present
def checking_valid_arguments_removeH(parser):
    try:
        args  = parser.parse_args()
    except SystemExit:
        print("\n####################################################################################")    
        print("ERROR. Arguments with no flag are not allowed. Check that each flag (e.g. -f) is followed by its specific argument")
        print("       Look below for more information.")
        print("####################################################################################\n\n")
        print_help_removeH()
        quit()
 
#Function: Parsing arguments, printing error and help message if 'ResRel.py' presents not allowed arguments, and checking if mandatory files are present       
def checking_valid_arguments_ResRel(parser):
    try:
        args  = parser.parse_args()
    except SystemExit:
        print("\n####################################################################################")    
        print("ERROR. Arguments with no flag are not allowed. Check that each flag (e.g. -r) is followed by its specific argument")
        print("       Look below for more information.")
        print("####################################################################################\n\n")
        print_help_ResRel()
        quit()

# Function: it checks for not accepted flags for 'remove_H_atoms.py' program
def check_argv_errors_removeH():
    for i in range(1, len(sys.argv)):
        if(i%2 != 0):

            if(sys.argv[i][0] == '-' and len(sys.argv[i]) == 1):
                print("\n####################################################################################")
                print("ERROR. '-' is not accepted as flag. Use, for example, '-r' instead of '-'")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_removeH()
                quit()

            if(sys.argv[i][0] == '-' and sys.argv[i][1] != '-' and  len(sys.argv[i]) > 2):
                print("\n####################################################################################")
                print("ERROR. '{}' not allowed. Each flag must contain '-' plus ONLY ONE letter. Example: -r".format(sys.argv[i]))
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --ref")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_removeH()
                quit()

            if(sys.argv[i][0] == '-' and sys.argv[i][1] == '-' and  len(sys.argv[i]) == 2):
                print("\n####################################################################################")
                print("ERROR. '--' not allowed. Each flag must contain '-' plus ONLY ONE letter. Example: -r.")
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --ref")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_removeH()
                quit()
                

# Function: it checks for not accepted flags for "ResRel-MPI.py" program
def check_argv_errors_ResRel():
    for i in range(1, len(sys.argv)):
        if(i%2 != 0):

            if(sys.argv[i][0] == '-' and len(sys.argv[i]) == 1):
                print("\n####################################################################################")
                print("ERROR. '-' is not accepted as flag. Use, for example, '-r' instead of '-'")
                print("Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()

            if(sys.argv[i][0] == '-' and sys.argv[i][1] != '-' and  len(sys.argv[i]) > 2):
                print("\n####################################################################################")
                print("ERROR. Each flag must contain '-' plus ONLY ONE letter. Example: -r")
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --ref")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()

            if(sys.argv[i][0] == '-' and sys.argv[i][1] == '-' and  len(sys.argv[i]) == 2):
                print("\n####################################################################################")
                print("ERROR. '--' not allowed. Each flag must contain '-' plus ONLY ONE letter. Example: -r")
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --ref")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()


# Function: it checks for not accepted flags for "Hs-Hk-plot.py" program
def check_argv_errors_HsHkplot():
    for i in range(1, len(sys.argv)):
        if(i%2 == 0):   
            
            if(sys.argv[i][0] == '-' and len(sys.argv[i]) == 1):
                print("\n####################################################################################")
                print("ERROR. '-' is not accepted as flag. Use, for example, '-f' instead of '-'")
                print("Look below for further help.")
                print("####################################################################################\n\n")
                if(sys.argv[1]=="density"):
                    print_help_density_HsHkplot()
                if(sys.argv[1]=="bin"):
                    print_help_bin_HsHkplot()    
                quit()

            if(sys.argv[i][0] == '-' and sys.argv[i][1] != '-' and  len(sys.argv[i]) > 2):
                print("\n####################################################################################")
                print("ERROR. '{}' not allowed. Each flag must contain '-' plus ONLY ONE letter. Example: -f".format(sys.argv[i]))
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --file")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                if(sys.argv[1]=="density"):
                    print_help_density_HsHkplot()
                if(sys.argv[1]=="bin"):
                    print_help_bin_HsHkplot()    
                quit()
                
            if(sys.argv[i][0] == '-' and sys.argv[i][1] == '-' and  len(sys.argv[i]) == 2):
                print("\n####################################################################################")
                print("ERROR. '{}' not allowed. Each flag must contain '-' plus ONLY ONE letter. Example: -f".format(sys.argv[i]))
                print("       Otherwise each flag can also contain '--' plus a STRING. Example: --file")
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                if(sys.argv[1]=="density"):
                    print_help_density_HsHkplot()
                if(sys.argv[1]=="bin"):
                    print_help_bin_HsHkplot()    
                quit()     




# Function: it checks if mandatory files in "remove_H_atoms.py" are present 
def mandatory_files_present_removeH(RefFile, TrajFile):
    if (RefFile is None):
        print("\n####################################################################################")
        print("ERROR. The Coordinate file is missing")
        print("       Look below for further help.")
        print("####################################################################################\n\n")
        print_help_removeH()
        quit()

    if (TrajFile is None):
        print("\n####################################################################################")
        print("ERROR. The file containing the Trajectory is missing")
        print("       Look below for further help.")
        print("####################################################################################\n\n")
        print_help_removeH()
        quit()
        


# Function: it checks if mandatory files in "ResRel-MPI.py" are present 
def mandatory_files_present_ResRel(RefFile, TrajFile):
    if (RefFile is None):
        print("\n####################################################################################")
        print("ERROR. The Coordinate file is missing")
        print("       Look below for further help.")
        print("####################################################################################\n\n")
        print_help_ResRel()
        quit()

    if (TrajFile is None):
        print("\n####################################################################################")
        print("ERROR. The file containing the Trajectory is missing")
        print("       Look below for further help.")
        print("####################################################################################\n\n")
        print_help_ResRel()
        quit()       
        
        

# Function: it checks if mandatory files in "Hs-Hk-plot.py" are present
def mandatory_files_present_HsHkplot(DataFile):
    if (DataFile is None):
        print("\n####################################################################################")
        print("ERROR. The file containing the information about Hs, Hk and Nsites (usually named 'Hs-Hk-Nsites.txt') is missing.")
        print("       Look below for further help.")
        print("####################################################################################\n\n")
        
        if(sys.argv[1]=='density'):
            print_help_density_HsHkplot()
        if(sys.argv[1]=='bin'):
            print_help_bin_HsHkplot()
        
        quit()
        





        
        

# Function: Checking if the optional argument "nMapp" is set. An error occurs if a float, string or negative (incl. zero) is inserted. 
#           Only an integer number is accepted. Please, take in account that, after defining arguments, the latter are treated always as STRING, 
#           therefore we have to check if we are deal with INT, FLOAT or STRINGS.       
def checking_errors_nMapp_opt_arg(nMapp):
    if(nMapp is not None):   # If nMapp exists... 
        nMapp = check_Int_Float_Str(nMapp)  # it returns nMapp accordingly with its nature: integer, float, or string
              
        if(not isinstance(nMapp, int)):  # if nMapp is NOT integer (float or string)
            print("\n####################################################################################")
            print("ERROR. '-m/--mapp {}' set, but not recognized. Only an integer number is allowed. 'float', 'strings', or negative numbers are not permitted.".format(nMapp))
            print("       Please, insert an integer number (-m/--mapp <INT>) or ignore this flag leaving the default value of 50 (-m/--mapp 50).")
            print("       Look below for further help.") 
            print("####################################################################################\n\n")
            print_help_ResRel()
            quit()
        else:
            if(nMapp <= 0):
                print("\n####################################################################################")
                print("ERROR. '-m/--mapp {}' set, but not recognized. Only an integer number higher than 0 is allowed".format(nMapp))  
                print("       A negative number or zero are meaningless.")
                print("       Please, insert an integer number (-m/--mapp <INT>) or ignore this flag leaving the default value of 50 (-m/--mapp 50).") 
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit() 
        print("\n● '-m/--mapp {}' set. The number of random mappings for a fixed number of retained sites is {}. NrandomMappings = {}... 20% completed.\n".format(nMapp,nMapp,nMapp))   

    if(nMapp is None):
        nMapp = 50
        print("\n● '-m/--mapp' not set. The number of random mappings for a fixed number of retained sites is 50.")
        print("                       NrandomMappings = 50 (default value)... 20% completed.\n")

    return nMapp



# Function: Checking if the optional argument "nFrames_read" is set. Float, and negative (incl. zero) numbers are not accepted, 
#           and the program returns an error. If the 'all' string is set, then all the trajectory frames are read, 
#           whereas an integer number (less than the total number of frames) is also accepted. Please, take in account that, 
#           after defining arguments, the latter are treated always as STRING, therefore we have to check if we are deal with INT, FLOAT or STRINGS.
def checking_errors_nFramesRead_opt_arg(nFrames_read, TotalFrames):
    if(nFrames_read is not None):   # If nFrames exists... 
        nFrames_read = check_Int_Float_Str(nFrames_read)  # it returns "nFrames_read" accordingly with its nature: integer, float, or string

        if(isinstance(nFrames_read, str)): # If nFrames is a string, only "all" is accepted 
            if(nFrames_read == "all" or nFrames_read == "All" or nFrames_read == "ALL"):
                nFrames_read = TotalFrames 
            
                print("\n● '-f/--frames all' set. All the frames of trajectory will be read. Nframes = {}... 4% completed.\n".format(nFrames_read)) 
            else:
                print("\n####################################################################################")
                print("ERROR. '-f/--frames {}' set. However '{}' string is not recognized.".format(nFrames_read, nFrames_read))
                print("       Only '-f/--frames all' is permitted if you would like to keep all the frames of trajectory.")
                print("       Otherwise, insert an integer number higher than 0 (-f/--frames <INT>) or ignore this flag leaving the default value of 1000 (-f/--frames 1000)")
                print("       Look below for further help.") 
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()
      
        elif(isinstance(nFrames_read, float)): # if nFrames is a float
            print("\n####################################################################################")
            print("ERROR. '-f/--frames {}' set, but not recognized. Only an integer number higher than 0 or the 'all' string is permitted.".format(nFrames_read))
            print("       Please, insert an integer number higher than 0 (-f/--frames <INT>), or the 'all' string (-f/--frames all)")
            print("       or ignore this flag leaving the default value of 1000 (-f/--frames 1000)")
            print("       Look below for further help.") 
            print("####################################################################################\n\n")
            print_help_ResRel()
            quit()
        
        elif(isinstance(nFrames_read, int)):  # if nFrames is an integer 
            if(nFrames_read <= 0 or nFrames_read > TotalFrames):
                print("\n####################################################################################")
                print("ERROR. '-f/--frames {}' set, but not recognized. Only an integer number between 0 (not included) and {} (TotalFrames)".format(nFrames_read, TotalFrames))
                print("       or the 'all' string is permitted. Please, insert an integer number higher than 0 (-f/--frames <INT>),")
                print("       or the 'all' string (-f/--frames all) or ignore this flag leaving the default value of 1000 (-f/--frames 1000)")
                print("       Keeping a negative number of frames of trrajectory is meaningless.")
                print("       Look below for further help.") 
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()
            else:
                print("\n● '-f/--frames {}' set. {} frames of the trajectory with respect the total ({}) will be read. Nframes_read = {}... 25% completed.\n".format(nFrames_read, nFrames_read, TotalFrames, nFrames_read))
            
    if(nFrames_read is None):
        if(TotalFrames >= 1000):
            nFrames_read = 1000
            print("\n● '-f/--frames' not set. 1000 frames (default) of trajectory with respect the total ({}) are read. Nframes_read = {}... 25% completed.\n".format(TotalFrames, nFrames_read))
        else:
            nFrames_read = TotalFrames
            print("\n● '-f/--frames' not set. As the total number of frames is less than 1000 ({}), all frames are read. Nframes_read = {}... 25% completed. \n".format(TotalFrames, nFrames_read))
            
    return nFrames_read
    
    
# Function: Checking if the optional argument "step" is set. The user have two ways of definining this argument: 
#
#      A- This number corresponds at the percentage of the total number of atoms used as step of the number of retained sites in the for-loop employed 
#         in the calculation of Relevance and Resolution. Therefore, integer and float numbers between 0 and 100 (by definition a percentage) 
#         followed by the '%' symbol are accepted are accepted. 
#         In case this percentage returns a step = 0, a Warning is printed on screen and a step = 1 is employed. 
#
#      B- The user has also the possibility of deciding the step without calculating the step as percentage of the total number of atoms.
#         In this latter case, the step must be an INTEGER number between 1 and Natoms-1, otherwise an error is returned. 
#         Please, consider that, after defining arguments, "step" and "step[:-1]" are treated always as STRING, 
#         therefore we have to check if we are deal with INT, FLOAT or STRINGS.

def checking_errors_step_opt_arg(step, Natoms):   
    if(step is not None): # If step exists
        step = check_Int_Float_Str(step)  # it returns "step" accordingly with its nature: integer, float, or string

        # A. First part: "step" treated as percentage of the total number of atoms. 
        if(isinstance(step, str)):
            step_1Part = step[:-1]                      # step[:-1] takes in account the entire string except the last word (it should be a "%")
            step_1Part = check_Int_Float_Str(step_1Part)  
        
        
            if(step[-1]=="%" and (isinstance(step_1Part, int) or isinstance(step_1Part, float))):    # int or float between 0 and 100 are accepted, and last word is "%"
            
                PercentageStep = step 
                ValueStep      = math.floor(step_1Part*Natoms/100)
                                                                                                  
                if(step_1Part<=0 or step_1Part>100):
                    print("\n####################################################################################")
                    print("ERROR. '-s/--step {}' set, but not recognized. If you would like to write the step as percentage of the total number of atoms,".format(PercentageStep))
                    print("       only an integer or float number between 0 (not included) and 100 followed by '%' symbol is permitted.") 
                    print("       Please, insert a percentage, that is an integer or float number higher than 0 and lower than 100 followed by '%' symbol")
                    print("       '(-s/--step <INT>%' or '-s/--step <FLOAT>%' or ignore this flag leaving the default value of 0.5% (-s/--step 0.5).")
                    print("       Otherwise, write direcly the step value inserting an integer number between 1 and {} (Natoms)".format(Natoms))
                    print("       Look below for further help.") 
                    print("####################################################################################\n\n")
                    print_help_ResRel()
                    quit()
                else:
                    if(ValueStep==0):
                        print("\n####################################################################################")
                        print("ERROR. '-s/--step {}' set. {} of {} should be used as step for the number of retained sites.".format(PercentageStep, PercentageStep, Natoms))
                        print("        However, in such case step = {}, that is meaningless. A step, at least equals to 1 should be used.".format(ValueStep))
                        print("        Please insert a new percentage such that the step is not 0,")
                        print("        or ignore this flag leaving the default value of 0.5% (-s/--step 0.5).")
                        print("        Otherwise, write direcly the step value inserting an integer number between 1 and {} (Natoms)".format(Natoms))
                        print("        Look below for further help.")
                        print("####################################################################################\n\n")
                        print_help_ResRel()
                        quit()
                    else:
                        print("\n● '-s/--step {}' set. {} of {} will be used as step for the number of retained sites. step = {}... 30% completed.\n".format(PercentageStep, PercentageStep, Natoms, ValueStep))
                    
                
            else:
                print("\n####################################################################################")
                print("ERROR. '-s/--step {}' set, but not recognized. If you would like to write the step as percentage of the total number of atoms,".format(step))
                print("       only an integer or float number between 0 (not included) and 100 followed by '%' symbol is permitted.")
                print("       Please, insert a percentage that is an integer or float number higher than 0 and lower than 100 followed by '%' symbol")
                print("       (-s/--step <INT>%' or '-s/--step <FLOAT>%' or ignore this flag leaving the default value of 0.5% (-s/--step 0.5).")
                print("       Otherwise, write direcly the step value inserting an integer number between 1 and {} (Natoms)".format(Natoms))
                print("       Look below for further help.")
                print("####################################################################################\n\n") 
                print_help_ResRel()
                quit()
            
            
        # B. Second part. "step" treated as integer, without calculating the step as pecentage of the total number of atoms.
        if(isinstance(step, float)):  
            print("\n####################################################################################") 
            print("ERROR. '-s/--step {}' set, but not recognized. If you would like to write directly the value of step,".format(step))
            print("       only an integer number between 1 and {} (Natoms) is permitted.".format(Natoms)) 
            print("       Please, insert an integer number higher than 1 and lower than {} ('-s/--step <INT>').".format(Natoms))
            print("       Otherwise, if you would like to write the step as percentage of the total number of atoms,") 
            print("       please insert an integer or float number higher than 0 and lower than 100 followed by '%' symbol") 
            print("       ('-s/--step <INT>%' or '-s/--step <FLOAT>%'), or ignore this flag leaving the default value of 0.5% (-s/--step 0.5)")
            print("       Look below for further help.")
            print("####################################################################################\n\n") 
            print_help_ResRel()
            quit()
        
        if(isinstance(step, int)): 
            ValueStep = step 
        
            if(ValueStep<1 or ValueStep>Natoms):
                print("\n####################################################################################")
                print("ERROR. '-s/--step {}' set, but not recognized. If you would like to write directly the value of step,".format(ValueStep))
                print("       only an integer number between 1 and {} (Natoms) is permitted.".format(Natoms)) 
                print("       Please, insert an integer number higher than 1 and lower than {} ('-s/--step <INT>')".format(Natoms))
                print("       Otherwise, if you would like to write the step as percentage of the total number of atoms,") 
                print("       please insert an integer or float number higher than 0 and lower than 100 followed by '%' symbol") 
                print("       ('-s/--step <INT>%' or '-s/--step <FLOAT>%'), or ignore this flag leaving the default value of 0.5% (-s/--step 0.5)")
                print("       Look below for further help.")
                print("####################################################################################\n\n") 
                print_help_ResRel()
                quit()
            else:
                print("\n● '-s/--step {}' set. step = {}... 30% completed.\n".format(ValueStep, ValueStep))    

    if(step is None):
        step = '0.5%'
    
        step_1Part = step[:-1]
        if(isIntFloat(step_1Part)):
            try:
                step_1Part = int(step_1Part)
            except:
                step_1Part = float(step_1Part)
            
    
        PercentageStep = step 
        ValueStep      = math.floor(step_1Part*Natoms/100)
    
        if(ValueStep==0):
            print("\n####################################################################################")
            print("ERROR. '-s/--step' not set. {} (default value) of {} should be used as step for the number of retained sites.".format(PercentageStep, Natoms))
            print("        However, in such case step = {}, that is meaningless. A step, at least equals to 1 should be used.".format(ValueStep))
            print("        Please insert a new percentage such that the step is not 0, or becuase the default one (0.5%) is not good in this specific case.")
            print("        Otherwise, write direcly the step value inserting an integer number between 1 and {} (Natoms)".format(Natoms))
            print("        Look below for further help.")
            print("####################################################################################\n\n")
            print_help_ResRel()
            quit()
        else:        
            print("\n● '-s/--step' not set. 0.5% (default) of {} (Natoms) will be used as step for the number of retained sites. step = {}... 30% completed.\n".format(Natoms, ValueStep))

    return ValueStep
    

    
# Function: Checking if the optional argument "DensityPoints" is set.  
#           As first, this argument can be set ONLY if the 'density' option is set, otherwise an error occurs. 
#           If 'density' option is set, moreover, an error occurs if a float, string or negative (incl. zero) is inserted. Only an integer number is accepted. 
#           Please, take in account that, after defining arguments, the latter are treated always as STRING, therefore we have to check if we are deal with INT, FLOAT or STRINGS.       
def checking_errors_DensityPoints_opt_arg(DensityPoints): 
    if(DensityPoints is not None):   # If DensityPoints exists... 
        if(sys.argv[1]=='density'):      # If 'density' option is set  
            DensityPoints = check_Int_Float_Str(DensityPoints)  # it returns "DensityPoints" accordingly with its nature: integer, float, or string
    
            if(not isinstance(DensityPoints, int)): # if DensityPoints is not integer (i.e. float or string)
                        print("\n####################################################################################")
                        print("ERROR. '-d/--DensityPoints {}' set, but not recognized. Only an integer number higher than 0 is permitted.".format(DensityPoints))
                        print("       Please, insert an integer number higher than 0 (-d/--DensityPoints <INT>)")
                        print("       or ignore this flag leaving the default value of 100 (-d/--DensityPoints 50)")
                        print("       Look below for further help.") 
                        print("####################################################################################\n\n")
                        print_help_density_HsHkplot()
                        quit()
            else:
                if(DensityPoints <= 0):
                    print("\n####################################################################################")
                    print("ERROR. '-d/--DensityPoints {}' set, but not recognized. Only an integer number higher than 0 is allowed.".format(DensityPoints))
                    print("       A negative number or zero are meaningless.") 
                    print("       Please, insert an integer number (-d/--DensityPoints <INT>)")
                    print("       or ignore this flag leaving the default value of 100 (-d/--DensityPoints 100).") 
                    print("       Look below for further help.")
                    print("####################################################################################\n\n")
                    print_help_density_HsHkplot()
                    quit()
            print("\n● '-d/--DensityPoints {}' set. The number of points in each interval for the calculation of average Hs and Hk is {}.".format(DensityPoints,DensityPoints)) 
            print("                                 DensityPoints = {}... 30% completed.\n".format(DensityPoints)) 
    
        if(sys.argv[1]=='bin'):  # If 'bin' option is set
            print("\n####################################################################################")
            print("ERROR. With 'bin' option the optional argument 'DensityPoints' (-d/--DensityPoints <INT>) cannot be set.")
            print("       Please, do not use this flag if 'bin' option is set.")
            print("       Look below for further help.")
            print("####################################################################################\n\n")
            print_help_density_HsHkplot()
            quit()
                    
    if(DensityPoints is None):
        if(sys.argv[1]=='density'):
            DensityPoints = 100
            print("\n● '-d/--DensityPoint' not set. The number of points in each interval for the calculation of average Hs and Hk is 100.")
            print("                               DensityPoints = 100 (default value)... 30% completed.\n")

    return DensityPoints
    
    
    
# Function: Checking if the optional argument "NumberWindows" is set.  
#           As first, this argument can be set ONLY if the 'bin' option is set, otherwise an error occurs. 
#           If 'bin' option is set, moreover, an error occurs if a float, string or negative (incl. zero) is inserted. Only an integer number is accepted. 
#           Please, take in account that, after defining arguments, the latter are treated always as STRING, therefore we have to check if we are deal with INT, FLOAT or STRINGS.       
def checking_errors_NumberWindows_opt_arg(NumberWindows):
    if(NumberWindows is not None):   # If NumberWindows exists... 
        if(sys.argv[1]=='bin'):          # If 'bin' option is set  
            NumberWindows = check_Int_Float_Str(NumberWindows)  # it returns "NumberWindows" accordingly with its nature: integer, float, or string
    
            if(not isinstance(NumberWindows, int)): # if NumberWindows is not integer (i.e. float or string)
                        print("\n####################################################################################")
                        print("ERROR. '-w/--NumberWindows {}' set, but not recognized. Only an integer number higher than 0 is permitted.".format(NumberWindows))
                        print("       Please, insert an integer number higher than 0 (-w/--NumberWindows <INT>)")
                        print("       or ignore this flag leaving the default value of 50 (-w/--NumberWindows 50)")
                        print("       Look below for further help.") 
                        print("####################################################################################\n\n")
                        print_help_bin_HsHkplot()
                        quit()
            else:
                if(NumberWindows <= 0):
                    print("\n####################################################################################")
                    print("ERROR. '-w/--NumberWindows {}' set, but not recognized. Only an integer number higher than 0 is allowed.".format(NumberWindows))
                    print("       A negative number or zero are meaningless.") 
                    print("       Please, insert an integer number (-w/--NumberWindows <INT>),")
                    print("       or ignore this flag leaving the default value of 50 (-w/--NumberWindows 50).") 
                    print("       Look below for further help.")
                    print("####################################################################################\n\n")
                    print_help_density_HsHkplot()
                    quit()           
            print("\n● '-w/--NumberWindows {}' set. The number of windows into which the Resolution range is splitted is {}.".format(NumberWindows,NumberWindows))
            print("                               NumberWindows = {} (default value)... 30% completed.\n".format(NumberWindows))
    
        if(sys.argv[1]=='density'):  # If 'bin' option is set
            print("\n####################################################################################")
            print("ERROR. With 'density' option the optional argument 'NumberWindows' (-w/--NumberWindows <INT>) cannot be set.")
            print("       Please, do not use this flag if 'density' option is set.")
            print("       Look below for further help.")
            print("####################################################################################\n\n")
            print_help_bin_HsHkplot()
            quit()
                    
    if(NumberWindows is None):
        if(sys.argv[1]=='bin'):
            NumberWindows = 50   
            print("\n● '-w/--NumberWindows' not set. The number of windows into which the Resolution range is splitted is 50.")
            print("                                NumberWindows = 50 (default value)... 30% completed.\n")
    
    return NumberWindows
    
    

# Function: Checking if the optional argument "SlopeRange" is set.  
#           This argument can be set in two different ways:
#            1) If a percentage is defined, then the rightmost value of slope in the range (-1 +/- <INT/FLOAT>%) is token. Default = 10%
#               that corresponds at th interval [-1.10; -0.90]
#
#            2) If 'closest' string is set [-s/--SlopeRange closest], then the closest value of slope to -1 is token.
#
#           Please, take in account that, after defining arguments, the latter are treated always as STRING, 
#           therefore we have to check if we are deal with INT, FLOAT or STRINGS. 
def checking_errors_SlopeRange_opt_arg(SlopeRange): 
    if(SlopeRange is not None):   # If SlopeRange exists...
        SlopeRange = check_Int_Float_Str(SlopeRange)    # it returns "SlopeRange" accordingly with its nature: integer, float, or string     
       
        if(not isinstance(SlopeRange, str)):            # If "SlopeRange" is not string (i.e. integer or float)
            print("\n####################################################################################")
            print("ERROR. '-s/--SlopeRange {}' set, but not recognized.".format(SlopeRange))
            print("       'SlopeRange' can be set in two different ways:")
            print("        A) If 'closest' string is set [-s/--SlopeRange closest], then the closest value of slope to -1 is token.")
            print("        B) If a percentage is defined, then the rightmost value of slope in the range (-1 \u00B1 <INT/FLOAT>%) is token")  #\u00B1 == +/- symbol
            print("        Please, insert a percentage or the 'closest' string or ignore this flag leaving the default value of 10%")
            print("        corresponding at the interval [-1.10; -0.90].")
            print("        Look below for further help.")
            print("####################################################################################\n\n")
            if(sys.argv[1]=="density"):
                print_help_density_HsHkplot()
            if(sys.argv[1]=="bin"):
                print_help_bin_HsHkplot()
            quit()
            
        
        # A. First part: "SlopeRange" treated as percentage of the total number of atoms. 
        if(isinstance(SlopeRange, str)):
            SlopeRange_1Part = SlopeRange[:-1]                  # SlopeRange[:-1] takes in account the entire string except the last word (it should be a "%")
            SlopeRange_1Part = check_Int_Float_Str(SlopeRange_1Part)    
            
            if(SlopeRange[-1]=="%" and (isinstance(SlopeRange_1Part, int) or isinstance(SlopeRange_1Part, float))):    # int or float between 0 and 100 
      														       # are accepted, and last word is "%"   
                
                if(SlopeRange_1Part<=0 or SlopeRange_1Part>100):
                    print("\n####################################################################################")
                    print("ERROR. '-s/--SlopeRange {}' set, but not recognized. If you would like to write the SlopeRange as percentage".format(SlopeRange))
                    print("       in order to take the rightmost value of slope in range -1 \u00B1 <INT/FLOAT>%,")
                    print("       then only an integer or float number between 0 (not included) and 100 followed by '%' symbol is permitted.")
                    print("       Please, insert a percentage, that is an integer or float number higher than 0 and lower than 100 followed by '%' symbol")
                    print("       '-s/--SlopeRange <INT>%' or '-s/--SlopeRange <FLOAT>%'")
                    print("       or ignore this flag leaving the default value of 10% (-s/--SlopeRange 10%).")
                    print("       Otherwise, write the string 'closest' [-s/--SlopeRange closest], in order that the closest value of slope to -1 is token.")
                    print("       Look below for further help.") 
                    print("####################################################################################\n\n")
                    if(sys.argv[1]=="density"):
                        print_help_density_HsHkplot()
                    if(sys.argv[1]=="bin"):
                        print_help_bin_HsHkplot()
                    quit()
                    
                ValueSlope  = SlopeRange_1Part/100
                SlopeLeft  = -1 - ValueSlope
                SlopeRight = -1 + ValueSlope
                
                print("\n● '-s/--SlopeRange {}' set. The range is, thus, -1 \u00B1 {}, i.e. [{}, {}]".format(SlopeRange, SlopeRange, SlopeLeft, SlopeRight))
                print("                            The rightmost value of slope in such range is token... 4% completed.\n")
                    
            elif(SlopeRange.strip() != "closest"):
                   print("\n####################################################################################")
                   print("ERROR. '-s/--SlopeRange {}' set, but not recognized. If you would like to write the SlopeRange as percentage".format(SlopeRange))
                   print("       in order to take the rightmost value of slope in range -1 \u00B1 <INT/FLOAT>%,")
                   print("       then only an integer or float number between 0 (not included) and 100 followed by '%' symbol is permitted.")
                   print("       Please, insert a percentage, that is an integer or float number higher than 0 and lower than 100 followed by '%' symbol")
                   print("       '-s/--SlopeRange <INT>%' or '-s/--SlopeRange <FLOAT>%'")
                   print("       or ignore this flag leaving the default value of 10% (-s/--SlopeRange 10%).")
                   print("       Otherwise, write the string 'closest' [-s/--SlopeRange closest], in order that the closest value of slope to -1 is token.")
                   print("       Look below for further help.") 
                   print("####################################################################################\n\n")
                   if(sys.argv[1]=="density"):
                       print_help_density_HsHkplot()
                   if(sys.argv[1]=="bin"):
                       print_help_bin_HsHkplot()
                   quit()
            else:          
                print("\n● '-s/--SlopeRange closest' set. The closest value of slope to -1 is token... 40% completed.\n")
                   
         
    if(SlopeRange is None): 
        SlopeRange = '10%'
    
        print("\n● '-s/--SlopeRange' not set. The default value is 10%. The range is -1 \u00B1 10% i.e. [-1.10, -0.90]")
        print("                             The rightmost value of slope in such range is token... 40% completed.\n")
    
    return SlopeRange


# Function: Checking if the optional argument "ncpu" is set. The program returns an error if the user askes for a number of cores 
#           higher than the maximum allowed. If 'ncpu' is not specified, the maximum number of cores is employed.  
def checking_errors_ncpu_opt_arg(ncpu):
    if(ncpu is not None):
        ncpu = check_Int_Float_Str(ncpu)  # it returns "ncpu" accordingly with its nature: integer, float, or string
        if(not isinstance(ncpu, int)): # if ncpu is not integer (i.e. float or string)
                        print("\n####################################################################################")
                        print("ERROR. '-n/--ncpu {}' set, but not recognized. Only an integer number higher than 0 is permitted.".format(ncpu))
                        print("       Please, insert an integer number higher than 0 (-n/--ncpu <INT>)")
                        print("       or ignore this flag, that means that the maximum number of cores are employed (-n/--ncpu {})".format(cpu_count()))
                        print("       Look below for further help.") 
                        print("####################################################################################\n\n")
                        print_help_ResRel()
                        quit()
        else:
            if(ncpu <= 0):
                print("\n####################################################################################")
                print("ERROR. '-n/--ncpu {}' set, but not recognized. Only an integer number higher than 0 is allowed.".format(ncpu))
                print("       A negative number or zero are meaningless.") 
                print("       Please, insert an integer number (-n/--ncpu <INT>),")
                print("       or ignore this flag leaving that means that the maximum number of cores are employed (-n/--npu {})".format(cpu_count())) 
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()           
       





            if(ncpu > cpu_count()):
                print("\n####################################################################################")
                print("ERROR. '-n/--ncpu {} set, but not recognized. The maximum number of cores available of your cluster/laptop is {}.".format(ncpu, cpu_count()))
                print("       You are asking for {} cores. Please, take care of it and repeat!".format(ncpu)) 
                print("       Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit()

        ncpu_employed = ncpu 
        print("\n● The number of cores employed is {}\n".format(ncpu_employed))
    
    if(ncpu is None):
        ncpu_employed = cpu_count()
        print("\n● The number of cores employed is {}\n".format(ncpu_employed))

    return ncpu_employed 


# Function: Checking if the optional file "RestartFile" is set. The program will raise an error if the user attempts to use a different file 
#           instead of the one generated by the ResRel-MPI.py code specifically named 'Hs-Hk-Nsites-${ProteinName}.txt'.
def checking_error_restart_opt_arg(RestartFile, ValueStep, Natoms):
    if(RestartFile is not None):
        with open(RestartFile, "r") as ResF:
            lines = ResF.readlines() 
            if(len(lines)!=3):
                print("\n####################################################################################")
                print("ERROR. '-c/--checkpoint {} set, but not recognized. The restart file must be the output of this code".format(os.path.basename(RestartFile))) 
                print("        namely 'Hs-Hk-Nsites-${ProteinName}.txt'. The latter file has three rows") 
                print("        that indicate the Resolution (Hs), Relevance (Hk) and the number of retained sites (N) respectively")
                print("        This file contains {} rows".format(len(lines))) 
                print("        If you have your own file, please take care of the the number of rows")
                print("        Look below for further help.")
                print("####################################################################################\n\n")
                print_help_ResRel()
                quit() 

        Nretained_Sites_row     = lines[-1].strip()
        Nretained_Sites_columns = Nretained_Sites_row.split(' ')
        Restart_Value_Nsites    = Nretained_Sites_columns[-1]             # Last value of N_retained_sites. This will be the checkpoint 
          
        Restart_Value_Nsites = check_Int_Float_Str(Restart_Value_Nsites)  # it returns "Restart_Value_Nsites" accordingly with its nature: integer, float, or string
								           # However, it should be an integer as it corresponds at the number of sites reached. 
  
        checkpoint = Restart_Value_Nsites - ValueStep
        print("\n● Relevance and Resolution not completed. Checkpoint found. Calculation will start from {} sites\n".format(checkpoint))
 
    if(RestartFile is None):
        checkpoint = Natoms - 1    

    return checkpoint
 
