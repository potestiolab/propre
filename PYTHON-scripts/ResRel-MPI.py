"""
The program has the scope of calculating the Relevance-Resolution (changing the number of sites) plot after calculating the RSD map among each frame and the other ones 
(an allignment between a couple of frames is required every time). Basically, it writes a file splitted in 3 rows:
 - 1st row: values of Resolution (Hs)
 - 2nd row: values of Relevance (Hk)
 - 3rd row: number of retained sites for that specific Hs and Hk  

After computing the fully-atomistic RSD map, we choose a cutoff such that has to be chosen all the atomistic conformations can be distinguish. 
Therefore, after finding such value, we take and Epsilon less than it, i.e. Cutoff_chosen = Cutoff - Espilon (or Cutoff*0.999). 

Then, we use always the same cutoff when computing the dendogram after decimating atoms. 

Based on this criterion, we propose Nrandom_mappings (50) at fixed N_retained_sites and we compute the unique value for Relevance and Resolution
for each mapping. Then, varying the number of retained sites (N_retained_site) it is possible to compute Hs and Hk for other 50 random mappings, and so on...
The number of retained sites (N_retained_sites) goes from 1 to N-1 atoms, with a step equals to 1/200 of Natoms.

Example: Natoms = 12390. Step = math.floor(12390/200) = 61. N_retained_atoms = (1, 12389, 61) = 1, 62, 123, ..., 12323, 12384

Then we have 50 (RandomMapping) times 200 (fixed_N_retained), that is 10'000 points of Relevance and Resolution. 

The final scope will be plotting the result in terms of slope of first derivative and finding the optimal number of sites 
corresponding to slope u = -1. This part will we done with a third code (not this one)
"""


                   #####################################################################################
#####################  1. Importing libraries, parsing arguments, and checking if errors are present  ####################################
                   #####################################################################################


# 1.1 Importing main libraries 
import matplotlib
import math
import random 
import os
import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as mda


from MDAnalysis.analysis.rms import rmsd
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from functools import partial
from multiprocessing import Process, Pool, cpu_count
from datetime import datetime
from scipy.special import comb  
from collections import Counter

import logging
logging.captureWarnings(True)


start_code = datetime.now()

# 1.2 Importing user-libraries 
from lib.inp_out import * 
from lib.general import *
from lib.check_errors import * 

# 1.3 Input Arguments -------------------------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False) 

group_in=parser.add_argument_group("Required Arguments") 
					                                             
group_in.add_argument('-r', '--ref',     dest='RefFile',     action='store', metavar = 'FILE', help = argparse.SUPPRESS)        # Mandatory
group_in.add_argument('-t', '--traj',    dest='TrajFile',    action='store', metavar = 'FILE', help = argparse.SUPPRESS)        # Mandatory 
group_in.add_argument('-h', '--help',    action='help',      help = argparse.SUPPRESS)                                          # Optional
group_in.add_argument('-m', '--mapp',    dest='nMapp',       metavar = 'INT',     help = argparse.SUPPRESS)                     # Optional 
group_in.add_argument('-f', '--frames',  dest='nFrames',     metavar = 'STR/INT', help = argparse.SUPPRESS)                     # Optional
group_in.add_argument('-s', '--step',    dest='step',        metavar = 'FLOAT',   help = argparse.SUPPRESS)                     # Optional
group_in.add_argument('-c', '--checkpoint', dest='RestartFile', action ='store',      metavar = 'FILE', help = argparse.SUPPRESS)  # Optional 
group_in.add_argument('-n', '--ncpu',    dest='NumberCpu',   metavar = 'INT',     help = argparse.SUPPRESS)                     # Optional
# --------------------------------------------------------------------------------------------------------------------------------------
 


if __name__ == '__main__':
    
    
    # 1.5 Printing on terminal that this code is running 
    print("\n####################################################\n")
    print("'{}' running...".format(os.path.basename(sys.argv[0]))) 
    print("---------------------------------\n")
    
    
    # 1.6 Printing help message if the script does not have any arguments  
    if len(sys.argv)==1:
        print_usage_ResRel()
        quit()
    
    if(sys.argv[1].strip() == "--usage") or (sys.argv[1].strip() == "-u"):
        print_usage_ResRel()
        quit()

    if(sys.argv[1].strip() == "--help" or sys.argv[1].strip() == "-h"):
        print_help_ResRel()
        quit()
    
    
    # 1.7 Printing help message if the script does not present valid arguments
    check_argv_errors_ResRel()

 
    # 1.8 Printing error and help message if code presents not allowed arguments
    checking_valid_arguments_ResRel(parser) 


    # 1.9 Parsing arguments
    args           = parser.parse_args()
    
    RefFile        = args.RefFile           # Mandatory 
    TrajFile       = args.TrajFile          # Mandatory 
    nMapp          = args.nMapp             # Optional
    nFrames_read   = args.nFrames           # Optional
    step           = args.step              # Optional 
    RestartFile    = args.RestartFile       # Optional
    ncpu           = args.NumberCpu         # Optional
 
    # 1.10 Checking if mandatory files are present
    mandatory_files_present_ResRel(RefFile, TrajFile)
    
    
    # 1.11 Checking if RefFile is actually found and that it is not empty 
    checking_file_found(RefFile)     
    check_empty_file(RefFile)

    print("\n● '-r/--ref {}' set. Coordinate file correctly read... 5% completed.\n".format(os.path.basename(RefFile)))  # Print ONLY Filename
    
    
    # 1.12 Checking if TrajFile is actually found and that it is not empty 
    checking_file_found(TrajFile)     
    check_empty_file(TrajFile)

    print("\n● '-t/--traj {}' set. Trajectory file correctly read... 10% completed.\n".format(os.path.basename(TrajFile)))
    
    
    # 1.13 Creating the Universe of trajectory 
    u = mda.Universe(RefFile,TrajFile)
    
    print("\n● Universe made up of Trajectory and Coordinate file correctly created... 15% completed.\n")
    


    # 1.14 Computing the total number of frames of trajectory (TotalFrames) and the number of the atoms (Natoms)
    TotalFrames = u.trajectory.n_frames
    Natoms      = u.trajectory.n_atoms
    
    
    
    # 1.15 Checking if the optional argument "nMapp" is set. An error occurs if a float, string or negative (incl. zero) is inserted. Only an integer is accepted. 
    nMapp = checking_errors_nMapp_opt_arg(nMapp)

    
    
    # 1.16 Checking if the optional argument "nFrames_read" is set. An error occurs if float or negative number (incl. zero) is inserted. 
    #      If the 'all' string is set, then all the trajectory frames are read. Also, an integer number (less than the total number of frames) is accepted. 
    nFrames_read = checking_errors_nFramesRead_opt_arg(nFrames_read, TotalFrames)
    
    
    
    # 1.17 Checking if the optional argument "step" is set. Two ways of defining this argument are feasible:
    #      A) As percentage of the total number of atoms (Natoms): it will be converted in terms of step value. 
    #      B) As integer number indicating directly the value of the step. 
    ValueStep = checking_errors_step_opt_arg(step, Natoms)
    
    
    # 1.18 Checking if the optional argument 'ncpu' is set. The program returns an error if the user askes for a number of cores 
    #      higher than the maximum allowed. If 'ncpu' is not specified, the maximum number of cores is employed. 
    ncpu_employed = checking_errors_ncpu_opt_arg(ncpu) 


    # 1.19 Checking if the optional argument file 'RestartFile' is set. The programs returns an error if this file is not found, or it is empty. 
    #      Moreover, this file specifies only the number of retained sites reached so far. This is an integer number. Float or string are not allowed.
    checkpoint = checking_error_restart_opt_arg(RestartFile, ValueStep, Natoms) 


    # 1.20 Printing Summary and returns the total number of points of Resolution and Relevance 
    tot_points = print_summary(Natoms, ValueStep, nMapp, TotalFrames, nFrames_read, checkpoint)
    




                   #####################################################################################
    #################  2. Defining a STEP for reading Trajectory and Remove some initial frames       #################################
                   #####################################################################################   
   
    """                    
    If '-s/--step <Nframes_read> is set (1000 by default), it means that we want a number of frames equals to "Nframes_read" at most 
    (otherwise the calculation of RSD map grow more and more since it goes as [Nframes]^2). Therefore: 
    
    a) we calculate a step_traj for reading the trajectory with a step equals to "step_traj"      
    b) we remove some initial frames in order to guarantee that the number of frames read is actually "Nframes_read". 

    Example: Let suppose that we want that the number of frames read is 1000 (Nframes_read=1000), 
             while the tot number of traj-frames is 12503 (TotalFrames=12503)
    
    'step_traj'                     = math.floor(12503/1000) = 12 
    'init_frames_to_remove_traj'    = 12503 - 1000*12        = 503 
    
    Indeed, 12503 - 503 = 12000 remaining frames. By using a step of 12, the Trajectory contains now 12000/12 frames, namely 1000. 
    """
                   
    step_traj                  = math.floor(TotalFrames/nFrames_read)
    init_frames_to_remove_traj = TotalFrames - nFrames_read*step_traj




    
                                 ######################################################
    ###############################  3. Storing all the position of protein' atoms   #################################
                                 ######################################################

    """
    Storing all the position of protein in an np.array called "positions" for only "Nframes_read" frames (1000 as default) as above mentioned. 
    In order to do it, we use the command "u.select_atoms('protein').positions". The result is a 3D-array: indeed, 
    the size will be (NewFrames, Natoms, 3) where:
    "Nframes_read" is 1000 (default) [or another value defined by user with -f/--frames <INT>], 
    whereas 3 is due to the fact that the poistion of each atom is in 3 coordinates (x,y,z).
    """
                   
    positions = np.array([u.select_atoms('protein').positions for ts in u.trajectory[init_frames_to_remove_traj::step_traj]])
    
    
    
    
                                 ####################################################
    ###############################  4. Computing RSD map for all-atom trajectory  #################################
                                 ####################################################
                                 
    """ 
    Computing the RSD map (using parallelization if possible: more cores, more faster) for all-atom trajectory.
    As first, the upper symmetric triangular matrix is calculated using the parallelized function "rsd_map_func". 
    Then, knowing that the matrix is symmetric with respect the diagonal (made up of zeroes), the complete squared RSD map is calculated. 
    The latter will be a 2D np.array and it will have (Nframes_read, Nframes_read) size. 
    If "Nframes_read" is left equals to 1000 by default, then the size will be 1000 x 1000.                                         
    """                                                         

    # 4.1 Computing the upper symmetric part of the triagular matrix "RSD-map" for the all-atom trajectory (ListRangeFrames goes from '0' to 'Nframes_read-1')                             
    ListRangeFrames = [x for x in range(len(positions))] 

    if(ncpu_employed is not None):
        pool = Pool(ncpu_employed)
    else:
        pool = Pool()

    temp = partial(rsd_map_func, positions, Natoms)

    rsd_AT_mat = pool.map(temp, iterable=ListRangeFrames)

    pool.close()
    pool.join()
    
    # 4.2 Completing the fullyAT RSD matrix merging the upper and lower symmetric triangular matrices, making a square symmetric matrix (the diagonal is made up of zeros)  
    #rsd_AT_mat = compute_complete_RSD_map(rsd_AT_mat, nFrames_read)  

    rsd_AT_mat = np.hstack(rsd_AT_mat)
    
    print(rsd_AT_mat) 
    print(rsd_AT_mat.shape)
    
    print("\n● Atomistic RSD map correctly created... 35% completed.\n")
    
    
    
                                 ####################################################
    ###############################  5. Creating dendogram & Computing the CUTOFF  #################################
                                 ####################################################
                                 
    """
    Creating the dendogram using the average linkage UPGMA algorithm, that could also visualize making use of "dendogram(Z) function.  
    (Z is the result if average linkage algorithm).  
                                 
    Then, the RSD value has to be computed, such that all the atomistic conformations can be distinguished.
    In order to do it, a Epsilon lower than the cutoff is chosen.  
                                 
    Consider that the latter value will be also used when the RSD map is computed for a subset of atoms.  
    'Z' is an array of arrays, organized in terms of increasing RSD values:
    
    Z = [[frame_index1, frame_index2, RSD, num_of_grouped_clusters], [.., .., .., ..] ]
                                 
    The lowest RSD corresponds to the 1st internal array, third column, i.e. Z[0][2].  
    The cutoff will be an espilon less such value, therefore can be calculated as 0.999*Z[0][2]                                                
    """

    # 5.1 Creating the dendogram using the average linkage UPGMA algorithm 
    Z = linkage(rsd_AT_mat, 'average')   

    # 5.2 Finding the cutoff, such that all the atomistic conformations can be distinguished   
    cutoff_rsd_at = 0.999 * Z[0][2] 
    print(f"\n● The cutoff chosen in RSD map such that all the atomistic conformations can be distinguished is {cutoff_rsd_at}... 40% completed.\n")
    
    
    
                       ####################################################################################################
    #####################  6. Computing Relevance & Resolution varying the number retained sites for different mappings  ###########################
                       ####################################################################################################
    
    """
    Changing the number of sites between 1 and Natoms-2 with a step given by ValueStep (default = 1/200 of the total number of atoms),
    it is possible to compute a single point of Resolution & Relevance (since the cutoff has been enstablished) for each random mapping. 
    It is preferable that the number of atoms retained (Natoms_retained) is not lower than 3 otherwise some artifacts could occur, 
    for instance the 'ZeroDivisionError' in the calculation of rmsd (MDanalysis package) when the number of atoms is 2.          
               
    in other words, at the beginning the number of atoms retained (Natoms_retained) is fixed at 'Natoms-1'. Then,the script choses randomly 
    'Nrandom_mappings' configurations among the 'Natoms-1' retained atoms (50 is the default value) and computes for each different mapping 
    the value of Resolution & Relevance single point (since the cutoff has been enstablished). 
                       
    Then, by using a step equals to 'ValueStep' (1/200 of total atoms as default), the number of retained atoms will decrease of such value
    and the script choses again randomly Nrandom_mappings' configurations among the 'Natoms-1-ValueStep' retained sites and computes the value
    of Resolution & Relevance single point for each different mapping (example: ValueStep=6, Natoms_retained=Natoms-1; Natoms-7; Natoms-13,...) 
    This process is iterated until the number of retained sites is, at most, equals to 3.   
                       
    The calculation of different 'Nrandom_mapping' combinations of 'Natoms_retained' is performed by using the user-function 'random_subset'.               
    """
                       
    # 6.1 For-loop changing the number of retained sites between 1 to Natoms-2 with a step equals to ValueStep 
    #     (to 1/200 of the total number of atoms is the default value). For each value of the atoms that will be decimated (N_removed), 
    #     the number of atoms retained is computed (Natoms_retained) and stored in a list (Natoms_retained_list).
    #     If RestartFile not present, then checkpoint = Natoms-1; therefore Natoms-checkpoint = 1. And the for-loop starts from 1 
    #     If RestartFile is present, then checkpoint = last_value_of_retained_sites_found - ValueStep. Therefore, 
    #     the for loop will start from Natoms-checkpoint, namely from the last number of retained sites, without starting from the beginning. 
    #     In this case the file created i.e. Hs-Hk-Nsites-${ProteinName}.txt will be appended with the new values of Hs, Hk, and Nsites.              

    Hs_Hk_Nsites_File = "Hs-Hk-Nsites-" + os.path.basename(RefFile)[:-4] + ".txt" 

    Hs = []  # Resolution 
    Hk = []  # Relevance

    Natoms_retained_list = [] 
 
    tot_count = 1 
    for N_removed in range(Natoms-checkpoint, Natoms-2, ValueStep):                    # FOR LOOP ON NUMBER OF SITES 

        Natoms_retained        = Natoms - N_removed                    # Number retained atoms                                         
        Nrandom_mappings       = nMapp                                 # Number of random mapping (default=50) chosen among those of a combination Comb(Natoms,Natoms_retained)
        
        #Natoms_retained_list.append(Natoms_retained)       
    
        A =[i for i in range(Natoms)]                                  # A = iterable = List of Natoms, starting from 0  
    

        # 6.2 'Nrandom_mapping' combinations of 'Natoms_retained' are calculated by using the user-function 'random_subset'.
        #     For a fixed "Natoms_retained", "samples" is a list of "Natoms_retained" among the total number of atoms (Natoms).
        #     The result consists of  Nrandom_mappings (50 as default) samples (np.array)
        samples = random_subset(A, Natoms_retained, Nrandom_mappings)            
        samples = np.array(list(samples)) 
         
        
        
        # 6.3 For each of Nrandom_mappings number (50 as default) (or the maximum number of combination if less than "Nrandom_mappings" value)
        #     for a fixed number of atoms retained (Natoms_retained), the RSD map is computed and then the value of Resolution (Hs)
        #     and Relevance (Hk) for the cutoff chosen before. 
         
        for t in range(Nrandom_mappings):                              # FOR LOOP ON MAPPINGS AT FIXED NUMBER OF SITES 

            Natoms_retained_list.append(Natoms_retained)      
 
            mapp_start = datetime.now()
            S = samples[t]  



            # 6.4 Computing the position coordinates for only the atoms selected randomly by S=samples[t]. The number of frames has been enstablished by 'nFrames_read'
            #     (1000 is the default value). 'positions[S]' takes ONLY the positions of the selected atoms, without creating new SubTtrajectory and relative universe, 
            #     that is time consuming. The number of atoms selected (Natoms_Sub) is the lenght of "S" list.
            
            positions_Sub = np.array([u.select_atoms('protein').positions[S] for ts in u.trajectory[init_frames_to_remove_traj::step_traj]])
            Natoms_Sub    = len(S) 
                                 


            # 6.5 Computing the upper symmetric part of the triagular matrix "RSD-map" for the only selected-atoms of trajectory (subset of Natoms).    
             
            ListRangeFrames_Sub = [x for x in range(len(positions_Sub))]
 
            if(ncpu_employed is not None):
                pool = Pool(ncpu_employed)
            else:
                pool = Pool()

            temp = partial(rsd_map_func, positions_Sub, Natoms_Sub)

            rsd_AT_mat_Sub = pool.map(temp, iterable=ListRangeFrames_Sub)

            pool.close()
            pool.join()



            # 6.6 Completing the RSD matrix of selected sites merging the upper and lower symmetric triangular matrices, making a square symmetric matrix 
            #     (the diagonal is made up of zeros) 

            Nframes_reduced_Sub = len(positions_Sub)  
            #rsd_AT_mat_Sub      = compute_complete_RSD_map(rsd_AT_mat_Sub, Nframes_reduced_Sub)

            rsd_AT_mat_Sub = np.hstack(rsd_AT_mat_Sub)
    
    
            # 6.7 Creating the dendogram relative to the RSD map of decimated trajectory using the average linkage UPGMA algorithm 
            #     (ZSub is the result if average linkage algorithm). 
            
            ZSub = linkage(rsd_AT_mat_Sub, 'average')
    
    
 
            # 6.8 Cutting the dendogram at atomistic cutoff chosen before (cutoff_rsd_at). Based of the distance criterion, 'fcluster' function 
            #     gives us the frame indeces below such cutoff (A) and, consequently, the number of clusters at such cutoff is calculated (Nclusters_Sub)
            #     In particular, the max value of "A" np.array corresponds at the number of clusters found below the atomistic reference cutoff. 
            #     Any detail can be found on:  https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html 
            
            A=fcluster(ZSub, t=cutoff_rsd_at, criterion='distance')
            Nclusters_Sub = max(A)   
            
            
            
            # 6.9 Calculating the Resolution "Hs" and the relevance "Hk" point for a specific number of assigned sites, for a specific mapping.
            #     The number of clusters is not varied because, for each specific SubTrajectory, the number of clusters (Nclusters_Sub)
            #     has been already calculated. After computing Hs-Hk points varying the mapping at fixed number of sites, the latter will be changed 
            #     and other mappings will be proposed (and a number "Nmappings" Hs-Hk points will be computed)


            ### 6.9.1  Computing "cl_labels", namely a label for each configuration ("cl_labels" is a list, e.g. [ 3 3 3 3 2 2 2 1 1 3 3 3...])   
            
            cl_labels = fcluster(ZSub, t=Nclusters_Sub, criterion='maxclust')   
            
            
            
            ### 6.9.2  Computing "count", namely a dictionary {K_i : N_elements}, that counts the number of frames for each cluster. 
            ###        Example: {1: 2, 2: 83, 3: 26, 4: 15, 5: 30, 6: 15, 7: 33} 
            ###                o cluster 1 --> 2 frames 
            ###                o cluster 2 --> 83 frames
            ###                o cluster 3 --> 26 frames 
            ###                o cluster 4 --> 15 frames
            ###                o cluster 5 --> 30 frames 
            ###                o cluster 6 --> 15 frames
            ###                o cluster 7 --> 33 frames 
            
            counts = Counter(cl_labels)                       


           
            ### 6.9.3 Sorting "counts" with respect the key.
            
            counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[0])}  

             
                                                          
            ### 6.9.4 Creating a list "values_list" and the array "value_array" containing only the values of the previous dictionary. 
            ###       Example: values_list = [2, 83, 26, 15, 30, 15, 33])                          
            
            values_list = list(counts.values()) 
            value_array = np.array(values_list)     
	
    

            ### 6.9.5 Counting how many times an element of list before is repeated (i.e. computing the molteplicity), i.e. mk_dict = {k: mk}  
            ###        Example: k=1 --> m1 = 0 (because the element "1" is not present)
            ###                 k=2 --> m2 = 1 (the element "2" is present only once)
            ###                 ...
            ###                 k=15 -->m15 = 2 (the element 15 is present twice)
            ###
            ###        In other words, this dictionary tell us: "How many clusters have k elements?"
            
            mk_dict     = Counter(values_list)    



            ### 6.9.6 Computing all the elements of the Resolution "Hs". The base of logarithm is M (i.e. the number of frames "Nframes"), therefore 
            ###       the logarithm rule is applied: log_M{a} = ln(a)/ln(M)
            
            Hs_array  = -(value_array/Nframes_reduced_Sub)*np.log(value_array/Nframes_reduced_Sub)/np.log(Nframes_reduced_Sub)  
            
                                                                                                                                

            ### 6.9.7 Computing the sum of the "Hs_array", corresponding to the value of Resolution "Hs" 
           
            somma       = np.sum(Hs_array)         
            Hs.append(somma)   
            
            
            
            ### 6.9.8 Computing all the elements of the Relevance "Hk" (the key of "mk_dict" is the number of clusters having molteplicity equals to "value") 
            ##        The base of logarithm is M (i.e. the number of frames "Nframes"), therefore the logarithm rule is applied: log_M{a} = ln(a)/ln(M)                
            
            somma_Hk = sum(-(k*v/Nframes_reduced_Sub)*math.log(k*v/Nframes_reduced_Sub, Nframes_reduced_Sub) for k,v in mk_dict.items())  



            ### 6.9.9 Computing the value of Relevance "Hk"
            
            Hk.append(somma_Hk)     
            values_list = []
         
         
         
            ### 6.9.10 Printing time for calculating each Hs-Hk point for a specific number of retained sites and random mapping. 
            
            mapp_end = datetime.now()
            mapp_time = (mapp_end - mapp_start).total_seconds()
            
            time_left = mapp_time * (tot_points - tot_count)
            
            print("NatomsRetained = {}   ||  NMapping = {}/{}  ||  time = {:3.4f} sec  |||  {}/{}  ||| time left = {:3.4f} sec.".format(Natoms_retained, t+1, Nrandom_mappings, mapp_time, tot_count,tot_points, time_left))
            

            ### 6.9.11 Writing 'Hs_Hk_Nsites_File' that is the file containing Hs, Hk, and the number of retained sites. denoted as 'Hs-Hk-Nsites-${ProteinName}.txt'
            ###        This file will be written when the Relevance and Resolution points are computed for each M random mapping (default M = 50)
            ###        for a fixed number of retained sites. In other words, when the number of retained sites change, then the file will be written 
            ###        with the M values of Hs,Hk and NSites.
            ###        If 'Hs_Hk_Nsites_File' does not exist, then it will be created, otherwise will be appended with the new values.   

            if os.path.isfile(Hs_Hk_Nsites_File):           
                if(t+1 == Nrandom_mappings):
                    with open(Hs_Hk_Nsites_File, 'r') as h:
                        lines = h.readlines()
                    
                    lines[0] = lines[0].strip() + ' ' + ' '.join(map(str, Hs)) + '\n'
                    lines[1] = lines[1].strip() + ' ' + ' '.join(map(str, Hk)) + '\n' 
                    lines[2] = lines[2].strip() + ' ' + ' '.join(map(str, Natoms_retained_list)) + '\n'

                    with open(Hs_Hk_Nsites_File, 'w') as h:
                        h.writelines(lines)

                    Hs = []
                    Hk = []
                    Natoms_retained_list = [] 
          
            else: # if not exists:
                if(t+1 == Nrandom_mappings):
                    with open(Hs_Hk_Nsites_File, 'w') as h: 
                        for line in Hs:
                            h.write(f"{line} ")
                        h.write("\n")

                        for line in Hk:
                            h.write(f"{line} ")
                        h.write("\n")

                        for line in Natoms_retained_list:
                            h.write(f"{line} ")
                        h.write("\n")
                    
                    Hs = []
                    Hk = [] 
                    Natoms_retained_list = []  
                     
                               ##############################
            #####################  7. Writing trace File   ##########################
                               ##############################
                               
            """
            Hs-Hk-Nsites-${ProteinName}.txt has been written and updated when the number of retained sites changes. Moreover a second file is written in this section: 
            
            "trace_${proteinName}.txt" gives a trace of how many Resolution & Relevance points has already been calculated and the time required for calculating a single point 
            at fixed number of retained sites (lower the retained sites, lower the time for calculating RSD-map and consequently for computing Hs-Hk point); 
                               
            """

            # 7.1 First file: Writing a file whose scope is to know the time required for calculating the value of Hs and Hk given the number of atoms retained
            FileName = "trace_" + os.path.basename(RefFile)[:-4] + ".txt"
            if(tot_count == 1):  # remove file only it is found only the first time. 
                if os.path.exists(FileName):
                    os.remove(FileName)
           
       
            with open(FileName, "a") as g:
                g.write("NatomsRetained = {}   ||  NMapping = {}/{}  ||  time = {:3.4f} sec |||  {}/{}\n".format(Natoms_retained,t+1,Nrandom_mappings,mapp_time,tot_count,tot_points))
            
            tot_count = tot_count + 1
            
            ###### END FIRST FOR-LOOP (about Nsites)
            
    
    end_code = datetime.now()
    
    print("\n● No errors... 100% completed") 
    print("\n● The time for executing the entire core is: ", (end_code - start_code).total_seconds())


