#!/usr/bin/env python3
"""
This program computes the optimal number of sites for a biomolecule from an atomistic trajectory.
It processes the data in two modes:
  - 'density': groups points by fixed count (DensityPoints) after sorting by resolution.
  - 'bin': groups points in equal-length bins over the [0,1] resolution interval.
For both modes, it computes the average resolution and relevance, calculates the derivative,
selects the interval where the slope is closest to TargetSlope (or within a user-defined percentage range),
and finally estimates the optimal number of sites.
"""

import matplotlib
matplotlib.use('Agg')
import math
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import Counter
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset, inset_axes
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from lib.inp_out import *
from lib.general import *
from lib.check_errors import *

def nan_helper(y):
    """
    Helper function to handle NaN values.
    Returns a boolean array that is True where NaNs are, and a function to get indices of non-NaN elements.
    """
    nans = np.isnan(y)
    return nans, lambda z: z.nonzero()[0]


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    group_in = parser.add_argument_group("Required Arguments")
    group_in.add_argument('option', help=argparse.SUPPRESS)  # Should be 'density' or 'bin'
    group_in.add_argument('-f', '--file', dest='DataFile', metavar='FILE', help=argparse.SUPPRESS)
    group_in.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
    group_in.add_argument('-d', '--DensityPoints', dest='DensityPoints', metavar='INT', help=argparse.SUPPRESS)
    group_in.add_argument('-s', '--SlopeRange', dest='SlopeRange', metavar='STR', help=argparse.SUPPRESS)
    group_in.add_argument('-w', '--NumberWindows', dest='NumberWindows', metavar='INT', help=argparse.SUPPRESS)
    group_in.add_argument('-t', '--TargetSlope', dest='TargetSlope', metavar='FLOAT', type=float, default=-1.0, help=argparse.SUPPRESS)
    return parser.parse_args()





def read_data_file(DataFile):
    """
    Read the data file and return Hs, Hk, and N as lists after performing basic error checks.
    The file is expected to have three rows: Resolution (Hs), Relevance (Hk), and number of sites (N).
    """
    with open(DataFile, 'r') as f:
        lines = f.readlines()

    if not lines:
        print(f"ERROR: The file {DataFile} is empty.")
        sys.exit(1)
    if len(lines) != 3:
        print(f"ERROR: The file {DataFile} must contain exactly 3 rows.")
        sys.exit(1)

    try:
        Hs = [float(x) for x in lines[0].split()]
        Hk = [float(x) for x in lines[1].split()]
        N  = [int(x) for x in lines[2].split()]
    except ValueError:
        print("ERROR: Data file rows do not contain the expected numerical types.")
        sys.exit(1)

    if not (len(Hs) == len(Hk) == len(N)):
        print("ERROR: The rows in the data file must have the same number of elements.")
        sys.exit(1)

    return Hs, Hk, N


def process_density(Hs, Hk, N, DensityPoints):
    """
    Process data using the 'density' option:
      - Sorts data by resolution.
      - Groups points in intervals containing a fixed number of points (DensityPoints).
      - Computes average values for resolution and relevance in each interval.
    Returns Hs_avg, Hk_avg, the sorted Hs_Hk_N list, and the number of intervals.
    """
    tot_points = len(Hs)
    Hs_Hk_N = np.array([[Hs[i], Hk[i], N[i]] for i in range(tot_points)])
    Hs_Hk_N = Hs_Hk_N[Hs_Hk_N[:, 0].argsort()]  # sort by resolution

    DensityPoints = int(DensityPoints)
    N_intervals = tot_points // DensityPoints

    # Only use complete intervals for vectorized averaging:
    reshaped = Hs_Hk_N[:N_intervals * DensityPoints].reshape(N_intervals, DensityPoints, 3)
    Hs_avg = np.mean(reshaped[:, :, 0], axis=1)
    Hk_avg = np.mean(reshaped[:, :, 1], axis=1)

    # Insert a 0 at the beginning as done originally
    Hs_avg = np.insert(Hs_avg, 0, 0)
    Hk_avg = np.insert(Hk_avg, 0, 0)
    
    

    return Hs_avg.tolist(), Hk_avg.tolist(), Hs_Hk_N.tolist(), N_intervals,


def process_bin(Hs, Hk, N, NumberWindows):
    """
    Process data using the 'bin' option:
      - Divides the [0,1] resolution range into equal-length bins.
      - Computes the central resolution of each bin and the average relevance in that bin.
      - If a bin has no points, relevance is set to NaN and later interpolated.
    Returns Hs_avg, Hk_avg, the sorted Hs_Hk_N list, and the bin width.
    """
    tot_points = len(Hs)
    Hs_Hk_N = np.array([[Hs[i], Hk[i], N[i]] for i in range(tot_points)])
    Hs_Hk_N = Hs_Hk_N[Hs_Hk_N[:, 0].argsort()]

    NumberWindows = int(NumberWindows)
    bin_width = 1 / NumberWindows

    Hs_avg = []
    Hk_avg = []
    for i in range(NumberWindows):
        Hs_avg.append(bin_width * (i + 0.5))  # central value of the bin
        mask = (Hs_Hk_N[:, 0] >= i * bin_width) & (Hs_Hk_N[:, 0] < (i + 1) * bin_width)
        values = Hs_Hk_N[mask, 1]
        if values.size > 0:
            Hk_avg.append(np.mean(values))
        else:
            Hk_avg.append(np.nan)

    # Interpolate over any NaN values in Hk_avg
    Hk_avg = np.array(Hk_avg)
    nans, x = nan_helper(Hk_avg)
    if np.any(~nans):
        Hk_avg[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), Hk_avg[~nans])

    return Hs_avg, Hk_avg.tolist(), Hs_Hk_N.tolist(), bin_width


def compute_slopes(Hs_avg, Hk_avg):
    """
    Compute slopes between consecutive average points using vectorized operations.
    Interpolates over NaN values (or zeros due to duplicate points) for a smooth derivative.
    """
    Hs_avg = np.array(Hs_avg)
    Hk_avg = np.array(Hk_avg)
    delta_Hs = np.diff(Hs_avg)
    delta_Hk = np.diff(Hk_avg)
    with np.errstate(divide='ignore', invalid='ignore'):
        slopes = np.where(delta_Hs == 0, np.nan, delta_Hk / delta_Hs)

    # Replace zero slopes (due to duplicate relevance values) with NaN
    slopes[slopes == 0] = np.nan
    nans, x = nan_helper(slopes)
    if np.any(~nans):
        slopes[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), slopes[~nans])
    
    # Filter out noisy slopes (e.g., those lower than -4.0)
    valid = slopes > -4.0
    return slopes[valid].tolist()



def find_best_interval(slopes, SlopeRange, TargetSlope):
    """
    Determine the index (or indices) of the best interval where the slope is close to -1.
    Two methods:
      - 'closest': choose the point with the slope closest to -1.
      - Percentage-based: choose the rightmost point in the range [-1-tol, -1+tol].
    Returns a list of selected index/indices.
    """
    if SlopeRange.strip() == "closest":
        slopes_array = np.array(slopes)
        idx = np.abs(slopes_array - TargetSlope).argmin()
        return [idx]
    else:
        try:
            percent_value = float(SlopeRange.strip()[:-1])
        except ValueError:
            print("ERROR: Invalid SlopeRange value.")
            sys.exit(1)
        tolerance = percent_value / 100.0
        left_bound = TargetSlope - tolerance
        right_bound = TargetSlope + tolerance
        indices = [i for i, s in enumerate(slopes) if left_bound < s < right_bound]
        if not indices:
            print(f"\nERROR. SlopeRange {SlopeRange} set yields interval [{left_bound}, {right_bound}] with no matching slopes.")
            sys.exit(1)
        return indices


def get_area_best_slope_indices(option, index_closest, DensityPoints=None, bin_width=None, Hs_Hk_N=None):
    """
    Extract the indices from the full data (Hs_Hk_N) corresponding to the best slope interval.
    For 'density', each interval is a block of DensityPoints.
    For 'bin', indices are those where the resolution falls within the selected bin.
    """
    if option == "density":
        indices = []
        for idx in index_closest:
            start = max((idx - 1) * int(DensityPoints), 0)
            end = idx * int(DensityPoints)
            indices.extend(range(start, end))
        return indices
    elif option == "bin":
        indices = []
        for idx in index_closest:
            lower = bin_width * idx
            upper = bin_width * (idx + 1)
            for i, entry in enumerate(Hs_Hk_N):
                if lower <= entry[0] < upper:
                    indices.append(i)
        return indices
    else:
        return []


def main():
    print("\n####################################################\n")
    print(f"'{os.path.basename(sys.argv[0])}' running...")
    print("---------------------------------\n")
    
    if len(sys.argv) == 1:
        print_usage_HsHkplot()  
        sys.exit(0)
    
    checking_accepted_tasks_HsHkplot()  
    check_argv_errors_HsHkplot()
    
    args = parse_arguments()
    option = args.option.strip().lower()  # 'density' or 'bin'
    DataFile = args.DataFile
    DensityPoints = args.DensityPoints
    SlopeRange = args.SlopeRange
    NumberWindows = args.NumberWindows
    TargetSlope = args.TargetSlope

    mandatory_files_present_HsHkplot(DataFile)

    print(f"\n● '{option}' option set. 5% completed.\n")
    

    
    # Read data file with error checks.
    Hs, Hk, N = read_data_file(DataFile)
    print(f"\n● '-f/--file {os.path.basename(DataFile)}' set. File containing Hs, Hk, and Nsites correctly read... 10% completed.\n")
    
    print("\n● '-t/--TargetSlope {:.2f}' set. The target slope for the best interval determination is {:.2f}.".format(TargetSlope, TargetSlope))
    print("                               TargetSlope = {:.2f}... 20% completed.\n".format(TargetSlope))



    # Process data based on the selected option.
    if option == "density":
        # DensityPoints: positive integer, used only in 'density' mode.
        DensityPoints = checking_errors_DensityPoints_opt_arg(DensityPoints)

        Hs_avg, Hk_avg, Hs_Hk_N, _ = process_density(Hs, Hk, N, DensityPoints)
    elif option == "bin":
        # NumberWindows: positive integer, used only in 'bin' mode.
        NumberWindows = checking_errors_NumberWindows_opt_arg(NumberWindows)

        Hs_avg, Hk_avg, Hs_Hk_N, bin_width = process_bin(Hs, Hk, N, NumberWindows)
    else:
        print("ERROR: Option must be 'density' or 'bin'.")
        sys.exit(1)

    # SlopeRange: either 'closest' or a percentage, applicable to both modes.
    SlopeRange = checking_errors_SlopeRange_opt_arg(SlopeRange)

    # Print summary of input arguments (custom function).
    print_summary_HsHk_plot(DataFile, DensityPoints, NumberWindows, SlopeRange, TargetSlope)
    
    # Compute slopes using vectorized operations.
    slopes = compute_slopes(Hs_avg, Hk_avg)
    print("\n● The calculation of the derivative of Resolution & Relevance correctly done... 50% completed")
    
    # Find the best interval where the slope is near -1.
    index_closest = find_best_interval(slopes, SlopeRange, TargetSlope)
    print(f"\n● The determination of the best interval (slope near {TargetSlope:.2f}) correctly done... 60% completed")
    
    # Extract the indices corresponding to the best slope area.
    if option == "density":
        area_indices = get_area_best_slope_indices("density", index_closest, DensityPoints=DensityPoints)
    else:
        area_indices = get_area_best_slope_indices("bin", index_closest, bin_width=bin_width, Hs_Hk_N=Hs_Hk_N)
    
    Hs_area_best_slope = [Hs_Hk_N[i][0] for i in area_indices]
    Hk_area_best_slope = [Hs_Hk_N[i][1] for i in area_indices]
    N_area_best_slope = [Hs_Hk_N[i][2] for i in area_indices]
    
    print("\n● The extraction of Resolution, Relevance, and number of sites in the best slope interval correctly done... 70% completed")
    
    # Compute the optimal number of sites as the mean and standard deviation of the sites in the best intervals.
    optimal_number_of_sites = np.mean(N_area_best_slope)
    std_number_of_sites = np.std(N_area_best_slope, ddof=1) 
    print(f"\n● Optimal number of sites: {optimal_number_of_sites:.2f} ± {std_number_of_sites:.2f} ... 80% completed.\n")
    
    # Write summary to file and save data.

    # Build output filenames using the input file name and target slope
    file_prefix = os.path.splitext(os.path.basename(DataFile))[0]
    custom_part = file_prefix.split('-')[-1] if '-' in file_prefix else ""
    target_slope_str = f"{TargetSlope:.2f}"
    summary_filename = f"Opt-number-of-sites_{custom_part}_TargetSlope-{target_slope_str}.txt"
    data_filename    = f"data_{custom_part}_TargetSlope-{target_slope_str}.npz"

    with open(summary_filename, "w") as g:
        write_file_summary_HsHk_plot(g, DataFile, DensityPoints, NumberWindows, SlopeRange, TargetSlope)
        g.write(f"The optimal number of sites is {optimal_number_of_sites:.2f} ± {std_number_of_sites:2f} ")
    
    # Save processed data in compressed NPZ format.
    np.savez_compressed(data_filename,
                        Hs=Hs,
                        Hk=Hk,
                        N=N,
                        Hs_avg=Hs_avg,
                        Hk_avg=Hk_avg,
                        Hs_area_best_slope=Hs_area_best_slope,
                        Hk_area_best_slope=Hk_area_best_slope,
                        slope=slopes,
                        SlopeRange=SlopeRange,
                        N_area_best_slope=N_area_best_slope,
                        index_closest=index_closest,
                        N_opt=optimal_number_of_sites,
                        std_N_opt=std_number_of_sites)
    
    print("\n● Saving data in NPZ format... 95% completed.")
    print("\n● No Errors! 100% completed.")
    print("\n####################################################\n")


if __name__ == '__main__':
    main()
