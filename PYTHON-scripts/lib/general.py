import math 
import random 
import os 
import sys 
import numpy as np

from MDAnalysis.analysis.rms import rmsd
from scipy.special import comb


# Function: it checks if the file is empty
def check_empty_file(file):
    if(os.path.getsize(file) == 0):
        print("Error. Your file is empty. Please, fill out {} with significant data or use another file".format(file))
        quit()
        

# Function: it checks if X is Integer or Float (Note that isdigit returns True only if X is Integer) 
def isIntFloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
        

# Function: it checks if an argument of argparse (that will be treated always as string) is integer, float, or string. The function returns "x" 
def check_Int_Float_Str(x):
    if(isIntFloat(x)):
        try:
            x = int(x)
        except:
            x = float(x)
    return x


# Function: RSD map in terms of upper triangular matrix (The symmetric part will be computing later). For each couple of frame, an allignment is done.  RSD = sqrt(Natoms)*RMSD 
def rsd_map_func(positions, Natoms, ts):
    rsd_map = []
    for ts_new in range(ts+1, len(positions)):
        v = rmsd(positions[ts], positions[ts_new], center=True, superposition=True)
        v = v*math.sqrt(Natoms)
        rsd_map.append(v)
    return rsd_map    
        


# Function: Given a list (iterable) of numbers (that in this case corresponds at the at_number of the atoms retained), 
#           the "r" lenght, and the number of random samples "k", it returns "k" random subsets of the main list. 
#           Example: LIST = [1,2,3,4,5]. "r" = 4, k = 2. It returns 2 random lists of 4 elements (of 5 in total), 
#           for instance [1,2,3,5] and [2,3,4,5].
#
#           In general, the total number of combination is given by: 
#           C(Natoms,Natoms_retained) = (Natoms)!/[(Natoms_retained)!*(Natoms-Natoms_retained)!]
#
#           If the total number of combinations [C(5,3) in the previuos example = 5!/(3!*2!)= 10] is less than 
#           "k" (usual 50), then all possible combinations are returned, otherwise  "k" lists are token (usual 50 by default).  
#           This fact is ensured by the last part of code: 
#           "if len(results) >= min(k, comb(len(iterable),r)): break" that takes the minimum value between  Nrandom_mappings (k)
#           and the number of combinations. 
#
#           "results = set()" ensures that the random combination chosen will not be equals ("if new_combo not in results:")
def random_subset(iterable, r, k):
    """Returns at most `n` random samples of
    `r` length (combinations of) subsequences of elements in `iterable`.
    """

    def random_combination(iterable, r):
        "Random selection from itertools.combinations(iterable, r)"
        pool = tuple(iterable)
        n = len(pool)
        indices = sorted(random.sample(range(n), r))
        return tuple(pool[i] for i in indices)

    results = set()
    while True:
        new_combo = random_combination(iterable, r)

        if new_combo not in results:
            results.add(new_combo)

        if len(results) >= min(k, comb(len(iterable),r)): 
            break						   								 
    							 								
    return results	
    
    

# Function: It returns the complete RSD map after computing the symmetric lower matrix.    
def compute_complete_RSD_map(rsd_AT_mat, Nframes_reduced):
    
    y = np.hstack(rsd_AT_mat)    # np.stack has the purpose of having a unique np.array instead of list of lists.
    
    ## a- Computing the symmetric lower triangular matrix "tri".
    idx = np.triu_indices(Nframes_reduced, k=1, m=Nframes_reduced)
    tri = np.zeros((Nframes_reduced, Nframes_reduced))
    tri[idx] = y 
    
    ## b- Completing the matrix, merging the upper and lower symmetric trinagular matrices, making a square symmetric matrix.
    tri = np.tril(tri.T,1) + tri
    rsd_AT_mat = tri 
    
    return rsd_AT_mat
