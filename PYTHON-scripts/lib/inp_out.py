import sys 
import os

from .general import * 


    
# Function: it prints the main usage of "remove_H_atoms.py" program
def print_usage_removeH():
    print("Usage: python3 {} -r <Coordinate FILE> -t <Trajectory FILE> ".format(sys.argv[0]))
    print("   or: python3 {} --ref <Coordinate FILE> --traj <Trajectory FILE> ".format(sys.argv[0]))

    print("\nTry python3 {} -h or {} --help for more information.\n".format(sys.argv[0], sys.argv[0]))

    

# Function: it prints the main help of remove_H_atoms.py program 
def print_help_removeH():  
    print("Usage: python3 {} -r <Coordinate FILE> -t <Trajectory FILE> ".format(sys.argv[0]))
    print("   or: python3 {} --ref <Coordinate FILE> --traj <Trajectory FILE> ".format(sys.argv[0]))
    
    print("\n-----------------------------------------------------------------------------------------------------")

    print("*{}* requires the following inputs:\n".format(sys.argv[0]));
    print("   Coordinate FILE                MANDATORY          File of atom Coordinates")
    print("                                                     (xyz, gro, pdb, psf, ..., formats are accepted)\n")
    print("   Trajectory FILE                MANDATORY          File containing the Trajectory of the biomolecule")
    print("                                                     (xtc, trr, dcd, gro, ..., formats are accepted).\n")

    print("-----------------------------------------------------------------------------------------------------");
    print("Hereafter the list of flags:\n");

    print("   -r   --ref                     FILE               Coordinate FILE (no hydrogens) (gro, pdb, psf, ..., format)")
    print("   -t   --traj                    FILE               Trajectory FILE (no hydrogens) (xtc, trr, dcd, gro, ..., format)")

    print("  [-h] [--help]                                      Give this help list\n")

    print("Report bugs to <raffaello.potestio@unitn.it>\n")
    

        
# Function: it prints the main usage of "ResRel-MPI.py" program
def print_usage_ResRel():
    print("Usage: python3 {} -r <Coordinate FILE> -t <Trajectory FILE> [-m <NMappings>] [-f <Nframes>] [-s <Nsteps>] [-n <nCPU>] [-c <RestartFILE>] ".format(sys.argv[0]))
    print("   or: python3 {} --ref <Coordinate FILE> --traj <Trajectory FILE> [--mapp NMappings>] [--frames <Nframes>] [--step <Nsteps>] [--ncpu <nCPU>] [--checkpoint <RestartFILE>] ".format(sys.argv[0]))

    print("\nTry python3 {} -h or {} --help for more information.\n".format(sys.argv[0], sys.argv[0]))


# Function: it prints the main help of "ResRel-MPI.py" program 
def print_help_ResRel():  
    print("Usage: python3 {} -r <Coordinate FILE> -t <Trajectory FILE> [-m <NMappings>] [-f <Nframes>] [-s <Nsteps>] [-n <nCPU>] [-c <RestartFILE>] ".format(sys.argv[0]))
    print("   or: python3 {} --ref <Coordinate FILE> --traj <Trajectory FILE> [--mapp NMappings>] [--frames <Nframes>] [--step <Nsteps>] [--ncpu <nCPU>] --checkpoint <RestartFILE>] ".format(sys.argv[0]))
    
    print("\n-----------------------------------------------------------------------------------------------------")

    print("*{}* requires the following inputs:\n".format(sys.argv[0]))
    print("   Coordinate FILE                MANDATORY          File of atom Coordinates (without hydrogens)")
    print("                                                     (xyz, gro, pdb, psf, ..., formats are accepted)\n")
    print("   Trajectory FILE                MANDATORY          File containing the Trajectory of the biomolecule (without hydrogens)")
    print("                                                     (xtc, trr, dcd, gro, ..., formats are accepted).\n")
    print("  [Nmappings]                     OPTIONAL           Number of random mappings at fixed number of sites retained.")
    print("                                                     Any integer number higher than 0 is accepted.")
    print("                                                     The default value is 50. For a fixed number of sites")
    print("                                                     the code choses randomly 50 combinations with respect the total number of atoms.")
    print("                                                     Changing such value, more or less combinations are chosen.\n")
    print("  [Nframes]                       OPTIONAL           Number of frames read in our trajectory. In order to guarantee") 
    print("                                                     this precise number of frames and the spanning of entire trajectory,")
    print("                                                     an initial number of frames will be discarded and the trajectory every nSteps is read.")
    print("                                                     The default value is 1000. Any integer number (less than the original number of frames)")
    print("                                                     is accepted. If the string 'all' is set, then every frame of trajectory is read")
    print("                                                     A trajectory, in general, could contain more than 1000 frames. However, since the calculation")
    print("                                                     of the RSD map goes as Nframes squared (N^2), increasing the number of frames")
    print("                                                     would require much more time. Higher the number of cores containing your cluster") 
    print("                                                     in a single node, more frames can be token in account.")
    print("                                                     Be careful choosing such value or selecting all frames\n")
    print("  [Nstep]                         OPTIONAL           Number that describes the variation of the number of retained sites") 
    print("                                                     in the calculation of 'Nmappings' Resolution and Relevance points.") 
    print("                                                     It means that, starting from the total number of atoms minus 1 (Natoms-1)")
    print("                                                     'Nmappings' Resolution and Relevance points are computed for each  mapping.") 
    print("                                                     Then, according with 'Nstep' value, the number of retained sites decreases of 'Nstep'") 
    print("                                                     (Natoms-1-Nstep) and other 'Nmappings' Resolution and Relevance points are computed") 
    print("                                                     for each mapping, and so on... until 3 retained sites are reached.")    
    print("                                                     The user have two ways of defining this argument:")
    print("                                                     ● As percentage of the total number of atoms: the number of retained sites")
    print("                                                       in the for-loop employed in the calculation of Relevance and Resolution.")
    print("                                                       will decrease of such percentage. The default value is 0.5%.")
    print("                                                       Therefore, it means that if the total number of atoms (Natoms) is 10'000, then")
    print("                                                       the 0.5% of such number is 50. In each for-loop the number of retained sites")
    print("                                                       starts from 10'000, and decreases by 50, until 1 is reached")
    print("                                                       (Natoms, Natoms-50, Natoms-100, ..., 1).")
    print("                                                       According with percentage definition, Nstep is an integer and float numbers")
    print("                                                       between 0 and 100 followed by the '%' symbol i.e. <INT/FLOAT>% (no spaces between)")
    print("                                                       In case this percentage returns a step = 0, an error is printed on screen")
    print("                                                       Default value = 0.5%")
    print("                                                     ● It is also possible to write directly the step without calculating it as percentage") 
    print("                                                       of the total number of atoms. In such case, the step must be an INTEGER number")
    print("                                                       between 1 and Natoms-1, otherwise an error is returned.")
    print("                                                       For example if Natoms=10000 and Nstep=100, then starting from Natoms,")
    print("                                                       in each for-loop the number of retained sites wll decrease by 100, until 1 is reached")
    print("                                                       (Natoms, Natoms-100, Natoms-200, ..., 1).\n")
    print("  [NumberCpu]                     OPTIONAL           Integer number corresponding at the number of cpus that you would like to employ")
    print("                                                     for calculating the RSD map.")
    print("                                                     If '-n/--ncpu <nCPU>' is set, the code will be parallelized by employing nCPU cores")
    print("                                                     If '-n/--npu <nCPU>' is not set, the code will be parallelized by employing")
    print("                                                     the maximum number of allowed cores in your laptop/cluster\n")
    print("  [RestartFILE]                   OPTIONAL           Due to the walltime limit on the node of your cluster or other potential factors,")
    print("                                                     the calculation of Relevance and Resolution points may be interrupted at any time.")
    print("                                                     However, to ensure continuity, you can utilize the same output file as a restart point,")
    print("                                                     identified as 'Hs-Hk-Nsites-${ProteinName}.txt'.")
    print("                                                     This allows the calculation to resume seamlessly from where it was last interrupted.\n")

    print("-----------------------------------------------------------------------------------------------------");
    print("Hereafter the list of flags:\n");

    print("   -r   --ref                     FILE               Coordinate FILE (no hydrogens) (gro, pdb, psf, ..., format)")
    print("   -t   --traj                    FILE               Trajectory FILE (no hydrogens) (xtc, trr, dcd, gro, ..., format)")
    print("  [-m] [--mapp]                   INT                Number of random mappings at fixed Number of retained sites (default = 50)")
    print("  [-f] [--frames]                 STR/INT            Number frames for the trajectory (default = 1000)")
    print("  [-s] [--step]                   INT/FLOAT + %      1) Percentage of Natoms used as step for the number of retained sites (default = 0.5%)")
    print("  [-s] [--step]                   INT                2) Number corresponding directly to the step for the number of retained sites.") 
    print("  [-n] [--ncpu]                   INT                Integer number corresponding at the number of cores employed for parallelizing the code")
    print("  [-c] [--checkpoint]             FILE               Restart FILE (Hs-Hk-Nsites-${ProteinName}.txt) from which the calculation of Hs-Hk-N resumes.") 
    print("  [-h] [--help]                                      Give this help list\n")
   
    print("Report bugs to <raffaello.potestio@unitn.it>\n")
    

# Function: it prints the main usage of "Hs-Hk-plot.py" program
def print_usage_HsHkplot():  
    tasks = ["density", "bin"]
   
    for tk in tasks: 
        print("Usage: python3 {} {} [OPTIONS]".format(sys.argv[0], tk))

    print("\nTry python3 {} -h or {} --help for more information.\n".format(sys.argv[0], sys.argv[0]))


# Function: it prints the short help of block.py program
def print_shorthelp_HsHkplot(): 
    tasks = ["density", "bin"]

    for tk in tasks:
        print("Usage: python3 {} {} [OPTIONS]".format(sys.argv[0], tk))
    
    print("\n-----------------------------------------------------------------------------------------------------")
    print("Please, choose one of the following tasks:\n")
    print("   *density*                            If using this option (recommended) the calculation of the average values")
    print("                                        for Resolution (Hs) and Relevance (Hk) is based on the same density of points.")
    print("                                        Indeed, every N points (the default value is 100) the average calculation")
    print("                                        for Hs and Hk is performed. In this way, the computation of average values is more fair")
    print("                                        since the lenght of interval is not fixed, but it is chosen in order that")
    print("                                        the number of points (Hs-Hk) is always the same.")
    print("                                        The default value for N is 100 points; however, such value con be changed using the flag [-d].\n")
    print("   *bin*                                If using this option the calculation of the average values")
    print("                                        for Resolution (Hs) and Relevance (Hk) is based on the same bin lenght.")
    print("                                        Indeed, the Resolution (that goes from 0 to 1) is divided in X windows (the default value is 50)")
    print("                                        and the 'bin' is thus defined as 1/X.")
    print("                                        This option could be not ideal beacuse the density of points along the curve is different:")
    print("                                        there will be windows very dense of points, and other ones with few points. ")
    print("                                        In this way, the computation of average values could be not fair and not precise")
    print("                                        Use this option with caution. The default value for X is 50 windows;")
    print("                                        however, such value can be changed using the flag [-w]\n")
    print("----------------------------------------------------------------------------------------------------")
    print("Hereafter the list of OPTIONS:\n");

    print("  -f   --file             FILE          Data FILE containing Hs, Hk, and Nsites organized in three different rows")
    print(" [-t] [--TargetSlope]     FLOAT         Target slope for optimal interval selection (defaults to -1 if not set)")
    print(" [-d] [--DensityPoints]   INT           Constant number of points for the calculation of average Hs and Hk [ONLY FOR *density* OPTION]")
    print(" [-s] [--SlopeRange]      STR           Range (percentage) of slope close to the target slope (default is 10% (for a target slope equal to -1 it is from -1.10 to -0.90) ")
    print(" [-w] [--NumberWindows]   INT           Number of windows (default = 50) into which the Resolution range is splitted [ONLY FOR *bin* OPTION]")
    print(" [-h] [--help]                          Give this help list\n")

    print("Try: python3 {} <TASK> for more information about the mandatory options of a specific task\n".format(sys.argv[0]))

    print("Report bugs to <raffaello.potestio@unitn.it>\n")
     


# Function: it prints the help of block.py program for DENSITY option
def print_help_density_HsHkplot():
    print("Usage: python3 {} density -f <Hs-Hk-N FILE> [-t <slopeTarget>] [-d <density>] [-s <slope(%)>] ".format(sys.argv[0]))
    print("   or: python3 {} density --file <Hs-Hk-N FILE> [--TargetSlope <slopeTarget>] [--DensityPoints <density>] [--SlopeRange <slope(%)>] ".format(sys.argv[0]))
    
    print("\n--------------------------------------------------------------------------------------------------------------------")     

    print("{} *{}* requires the following inputs:\n".format(sys.argv[0], sys.argv[1]))
    print("   Hs-Hk-NSites FILE       FILE               MANDATORY      File containing the Resolution (Hs), Relevance (Hk)")
    print("                                                             and the number of sites (N) in the 1st, 2nd and 3rd row, respectively.")
    print("                                                             This is the ouptut of 'Res-Rel.py' program. However, in case you have ")
    print("                                                             your own file be sure that it is organized in 3 rows. Each one contains")
    print("                                                             the value od Hs, Hk, and Nsites separated by one space.")
    print("                                                                ----------------------------------------------------")
    print("                                                                | Hs-1       Hs-2       Hs-3       .....  Hs-N     |")  
    print("                                                                | Hk-1       Hk-2       Hk-3       .....  Hk-N     |")
    print("                                                                | Nsites-1   Nsites-2   Nsites-3   .....  Nsites-N |")
    print("                                                                ----------------------------------------------------- \n")
    print("  [TargetSlope]          FLOAT                OPTIONAL       Target slope for selecting the optimal interval.")
    print("                                                             This value specifies the desired slope (e.g. -1.00) used")
    print("                                                             to determine the best interval on the average Hs-Hk curve.")
    print("                                                             If not provided, it defaults to -1.\n")
    print("  [DensityPoints]          INT                OPTIONAL       Every N points (the default value is 100) the average calculation")
    print("                                                             for Hs and Hk is performed. In this way the computation of average values is more fair")
    print("                                                             since the number of points (Hs-Hk) is always the same in each interval.")
    print("                                                             Such value (Integer number) con be changed using this flag.\n")
    print("  [SlopeRange]             STR                OPTIONAL       After computing the average values for Resolution and Relevance,")
    print("                                                             it is necessary to identify the best interval where the slope of this new curve")
    print("                                                             is close to the target slope (as specified by --TargetSlope).")
    print("                                                             Two ways to define this argument are possible:")
    print("                                                             ● Define a percentage range around the target slope (default is 10%;")
    print("                                                               e.g., if the target slope is -1, the interval is from -1.10 to -0.90),")
    print("                                                               and select the rightmost value (i.e., with higher Resolution) within this range.")
    print("                                                             ● Alternatively, use the string 'closest' to choose the slope value")
    print("                                                               that is closest to the target slope (i.e., [-s/--SlopeRange closest]).\n")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Hereafter the list of flags:\n")

    print("  -f   --file              FILE                              Data FILE containing Hs, Hk, and Nsites organized in three different rows")
    print(" [-t] [--TargetSlope]      FLOAT                             Target slope for optimal interval selection (defaults to -1 if not set)")
    print(" [-d] [--DensityPoints]    INT                               Constant number of points for the calculation of average Hs and Hk")
    print(" [-s] [--SlopeRange]       INT/FLOAT + %                     1) Define a percentage range around the target slope (<INT/FLOAT>%).")
    print("                                                             Default is 10% (e.g., for a target slope of -1, the interval is from -1.10 to -0.90).")
    print(" [-s] [--SlopeRange]       STR                               2) Use 'closest' to select the slope value closest to the target slope.")
    print(" [-h] [--help]                                               Give this help list\n")
    
    print("Report bugs to <raffaello.potestio@unitn.it>\n")
    
 
    

# Function: it prints the help of block.py program for BIN option
def print_help_bin_HsHkplot():
    print("Usage: python3 {} bin -f <Hs-Hk-N FILE> [-t <slopeTarget>] [-w <nWindows>] [-s <slope(%)>] ".format(sys.argv[0]))
    print("   or: python3 {} bin --file <Hs-Hk-N FILE> [--TargetSlope <slopeTarget>] [--NumberWindows <nWindows>] [--SlopeRange <slope(%)>] ".format(sys.argv[0]))
    
    print("\n--------------------------------------------------------------------------------------------------------------------")     

    print("{} *{}* requires the following inputs:\n".format(sys.argv[0], sys.argv[1]))
    print("   Hs-Hk-NSites FILE       FILE               MANDATORY      File containing the Resolution (Hs), Relevance (Hk)")
    print("                                                             and the number of sites (N) in the 1st, 2nd and 3rd row, respectively.")
    print("                                                             This is the ouptut of 'Res-Rel.py' program. However, in case you have ")
    print("                                                             your own file be sure that it is organized in 3 rows. Each one contains")
    print("                                                             the value od Hs, Hk, and Nsites separated by one space.")
    print("                                                                ----------------------------------------------------")
    print("                                                                | Hs-1       Hs-2       Hs-3       .....  Hs-N     |")  
    print("                                                                | Hk-1       Hk-2       Hk-3       .....  Hk-N     |")
    print("                                                                | Nsites-1   Nsites-2   Nsites-3   .....  Nsites-N |")
    print("                                                                ----------------------------------------------------- \n")
    print("  [TargetSlope]          FLOAT                OPTIONAL       Target slope for selecting the optimal interval.")
    print("                                                             This value specifies the desired slope (e.g. -1.00) used")
    print("                                                             to determine the best interval on the average Hs-Hk curve.")
    print("                                                             If not provided, it defaults to -1.\n")
    print("  [NumberWindows]          INT                OPTIONAL       The Resolution range(that goes from 0 to 1) is divided in X windows")
    print("                                                             and a 'bin' is thus defined as 1/X (the default value is X = 50 windows,")
    print("                                                             and bin = 1/50 = 0.02.) In each windows, the average calculation")
    print("                                                             of Hs and Hk is performed, whatever the number of points is involved.")
    print("                                                             In this way, the computation of average values could be not fair and not precise")
    print("                                                             Use this option with caution. The default value for X is 50 windows;")
    print("                                                             Such value (Integer number) con be changed using this flag.\n")
    print("  [SlopeRange]             STR                OPTIONAL       After computing the average values for Resolution and Relevance,")
    print("                                                             it is necessary to identify the best interval where the slope of this new curve")
    print("                                                             is close to the target slope (as specified by --TargetSlope).")
    print("                                                             Two ways to define this argument are possible:")
    print("                                                             ● Define a percentage range around the target slope (default is 10%;")
    print("                                                               e.g., if the target slope is -1, the interval is from -1.10 to -0.90),")
    print("                                                               and select the rightmost value (i.e., with higher Resolution) within this range.")
    print("                                                             ● Alternatively, use the string 'closest' to choose the slope value")
    print("                                                               that is closest to the target slope (i.e., [-s/--SlopeRange closest]).\n")
    print("----------------------------------------------------------------------------------------------------------------------");
    print("Hereafter the list of flags:\n");
    
    print("  -f   --file              FILE                               Data FILE containing Hs, Hk, and Nsites organized in three different rows")
    print(" [-t] [--TargetSlope]     FLOAT                              Target slope for optimal interval selection (defaults to -1 if not set)")
    print(" [-w] [--NumberWindows]    INT                                Number of windows (default = 50) into which the Resolution range is splitted")
    print(" [-s] [--SlopeRange]       INT/FLOAT + %                     1) Define a percentage range around the target slope (<INT/FLOAT>%).")
    print("                                                             Default is 10% (e.g., for a target slope of -1, the interval is from -1.10 to -0.90).")
    print(" [-s] [--SlopeRange]       STR                               2) Use 'closest' to select the slope value closest to the target slope.")
    print(" [-h] [--help]                                                Give this help list\n")
    
    print("Report bugs to <raffaello.potestio@unitn.it>\n")
    
       
    
    
               
                
# Function: It computes the total number of points and it prints a summary of the arguments that will be employed in the calculation of Relevance & Resolution. 
def print_summary(Natoms, ValueStep, nMapp, TotalFrames, nFrames_read, checkpoint):
    print("\n\n\n○ The number of retained sites will range between 1 and {} (Natoms-1) with a step = {}\n".format(Natoms-1, ValueStep))

    print("\n○ The number of random mapping for each number of retained sites is NrandomMappings = {}\n".format(nMapp))

    Step_List = [x for x in range(Natoms-checkpoint, Natoms-2, ValueStep)]
    tot_points = len(Step_List) * nMapp

    print("\n○ Thus, the total number of Relevance & Resolution points is tot_points = {}".format(tot_points))

    print("\n\n-----------------------------------------------------------")
    print("                           SUMMARY               ")
    print("-----------------------------------------------------------\n")

    print(f"frames_traj      = {TotalFrames}")
    print(f"Nframes_read     = {nFrames_read}")
    print(f"Natoms           = {Natoms}")
    print(f"step             = {ValueStep}")
    print(f"NrandomMappings  = {nMapp}")
    print(f"tot_points       = {tot_points}")
    print("\n-----------------------------------------------------------\n")
    
    return tot_points
    


# Function: It prints a summary of the arguments that will be employed in the calculation of Hs-Hk-plot. 
def print_summary_HsHk_plot(DataFile, DensityPoints, NumberWindows, SlopeRange, TargetSlope):
    
    print("\n\n-----------------------------------------------------------")
    print("                           SUMMARY               ")
    print("-----------------------------------------------------------\n")

    print("File Name         = {}".format(os.path.basename(DataFile)))
    print(f"Option            = {sys.argv[1]}")
    print(f"Target Slope      = {TargetSlope}")
    if(sys.argv[1].strip()=="density"):
        print(f"DensityPoints     = {DensityPoints}")
    elif(sys.argv[1].strip()=="bin"):
        print(f"NumberWindows     = {NumberWindows}")
        
    if(SlopeRange == "closest"):
        print(f"SlopeRange        = {SlopeRange}")
    else:
        SlopeRange_1Part = SlopeRange[:-1]
        SlopeRange_1Part = check_Int_Float_Str(SlopeRange_1Part)
        ValueSlope  = SlopeRange_1Part/100
        SlopeLeft  = TargetSlope - ValueSlope
        SlopeRight = TargetSlope + ValueSlope
            
        print("SlopeRange        = [{}, {}]".format(SlopeLeft, SlopeRight))
    print("\n-----------------------------------------------------------\n")

    
    
    
# Function: It prints of a file the summary of the arguments that will be employed in the calculation of Hs-Hk-plot. 
def write_file_summary_HsHk_plot(g, DataFile, DensityPoints, NumberWindows, SlopeRange, TargetSlope):
    
    g.write("\n\n-----------------------------------------------------------\n")
    g.write("                           SUMMARY               \n")
    g.write("-----------------------------------------------------------\n\n")

    g.write("File Name         = {}\n".format(os.path.basename(DataFile)))
    g.write(f"Option            = {sys.argv[1]}\n")
    if(sys.argv[1].strip()=="density"):
        g.write(f"DensityPoints     = {DensityPoints}\n")
    elif(sys.argv[1].strip()=="bin"):
        g.write(f"NumberWindows     = {NumberWindows}\n")
        
    if(SlopeRange == "closest"):
        g.write(f"SlopeRange        = {SlopeRange}\n")
    else:
        SlopeRange_1Part = SlopeRange[:-1]
        SlopeRange_1Part = check_Int_Float_Str(SlopeRange_1Part)
        ValueSlope  = SlopeRange_1Part/100
        SlopeLeft  = TargetSlope - ValueSlope
        SlopeRight = TargetSlope + ValueSlope
            
        g.write("SlopeRange        = [{}, {}]\n".format(SlopeLeft, SlopeRight))
    g.write("\n\n-----------------------------------------------------------\n\n") 
