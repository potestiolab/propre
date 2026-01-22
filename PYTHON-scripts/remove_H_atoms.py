"""
This code has the preliminary scope of removing all the hydrogen atoms (H, H1, H2, HW, etc...) from both the reference file 
(usually 'gro' or 'pdf', 'psf', etc...) and the trajectory one ('xtc', 'trr', 'dcd', 'gro', etc...). 
The reason lies in the fact that, in the calculation of RMSD (or RSD) map and, afterwards, in the calculation of Resolution
and Relevance after keeping a group of atoms, we do not want to consider the hydrogens, as they are not heavy-atoms. 

This code, therefore, will return in output the new reference file and the new trajectory one, without H atoms. The latter 
will be read by 'ResRel.py' or its parallelized version, that is 'ResRel-MPI.py'. 
"""

                   ##############################################################################
#####################  1. Import libraries, parse arguments, and check if errors are present   ####################################
                   ##############################################################################

# 1.1 Importing main libraries 
import MDAnalysis as mda
import os 
import sys
import argparse

# 1.2 Importing user-libraries 
from lib.inp_out import *
from lib.check_errors import * 

# 1.3 Input Arguments -------------------------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False) 

group_in=parser.add_argument_group("Required Arguments") 
					                                             
group_in.add_argument('-r', '--ref',  dest='RefFile',  action='store', metavar = 'FILE', help = argparse.SUPPRESS)        # Mandatory
group_in.add_argument('-t', '--traj', dest='TrajFile', action='store', metavar = 'FILE', help = argparse.SUPPRESS)        # Mandatory 

group_in.add_argument('-h', '--help', action='help', help = argparse.SUPPRESS)                                            # Optional
# --------------------------------------------------------------------------------------------------------------------------------------


    
# 1.4 Printing on terminal that this code is running 
print("\n####################################################\n")
print("'{}' running...".format(os.path.basename(sys.argv[0]))) 
print("---------------------------------\n")



# 1.5 Printing help message if the script does not have any arguments  
if len(sys.argv)==1:
    print_usage_removeH()
    quit()
    
if(sys.argv[1].strip() == "--usage") or (sys.argv[1].strip() == "-u"):
    print_usage_removeH()
    quit()

if(sys.argv[1].strip() == "--help" or sys.argv[1].strip() == "-h"):
    print_help_removeH()
    quit()
    
    
    
# 1.6 Printing help message if the script does not present valid arguments
check_argv_errors_removeH()

 
# 1.7 Printing error and help message if code presents not allowed arguments
checking_valid_arguments_removeH(parser)


# 1.8 Parsing arguments
args           = parser.parse_args()

RefFile        = args.RefFile           # Mandatory 
TrajFile       = args.TrajFile          # Mandatory  


# 1.9 Checking if mandatory files are present 
mandatory_files_present_removeH(RefFile, TrajFile)


# 1.10 Checking if RefFile is actually found and that it is not empty 
checking_file_found(RefFile)     
check_empty_file(RefFile)

print("\n● '-r/--ref {}' set. Coordinate file correctly read...20% completed.\n".format(os.path.basename(RefFile)))  # Print ONLY Filename


# 1.11 Checking if TrajFile is actually found and that it is not empty 
checking_file_found(TrajFile)     
check_empty_file(TrajFile)

print("\n● '-t/--traj {}' set. Trajectory file correctly read... 40% completed.\n".format(os.path.basename(TrajFile)))



                   ########################################################################
##################### 2. Creating Coordinate File and Trajectory File without hydrogens  ###############################
                   ########################################################################

# 2.1 Creating the Universe of trajectory
u = mda.Universe(RefFile,TrajFile)


# 2.2 Selecting all the atoms except the hydrogens (H)         
Ref_noH  = u.select_atoms("all and not type H")


# 2.3 Writing the Reference File (.gro) without Hydrogen atoms (noH)   
Ref_noH.write("Reference_noH.gro")
print("\n● Coordinate file without hydrogens 'Reference_noH.gro' correctly written... 60% completed\n")


# 2.4 Writing the Trajectory File(.xtc) without Hydrogen atoms (noH) 
with mda.Writer("Trajectory_noH.xtc", Ref_noH.n_atoms) as W:
    for ts in u.trajectory:
        W.write(Ref_noH)


print("\n● Trajectory file without hydrogens 'Trajectory_noH.xtc' correctly written... 80% completed\n")
print("\n● No errors... 100% completed\n")
