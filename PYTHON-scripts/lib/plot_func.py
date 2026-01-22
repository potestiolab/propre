import matplotlib.pyplot as plt
import numpy as np 

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from .general import * 

# FUNCTION: Scatter Plot, Average Hs-Hk curve, Zoom of the region of interest (where the slope is -1) 
def Hs_Hk_scatter_plot(ax, Hs, Hk, N, Hs_avg, Hk_avg, Hs_area_best_slope, Hk_area_best_slope):
    
    ## 1) Computing maximum and minimum value for Hs and Hk in the region where the slope is close to -1
    Max_Hk_area_best_slope = max(Hk_area_best_slope) 
    Min_Hk_area_best_slope = min(Hk_area_best_slope)
    
    Max_Hs_area_best_slope = max(Hs_area_best_slope) 
    Min_Hs_area_best_slope = min(Hs_area_best_slope)
     
        
    ## 2) Plotting Scatter Plot
    points = ax.scatter(Hs, Hk, edgecolors='none', s=10, c=N, cmap="viridis_r")  #, norm=matplotlib.colors.PowerNorm(gamma=0.5))
    cb = plt.colorbar(points)
    plt.ylim(0, max(Hk)+0.05)
    plt.yticks(np.arange(0, max(Hk)+0.05, 0.1))
    plt.xlim(0,1)      
    
    ## 3) Writing title for plot, axis and color-bar
    plt.title("H[s]-H[k]")
    
    plt.ylabel('Relevance H[k]', horizontalalignment='center')
    plt.xlabel('Resolution H[s]', horizontalalignment='center')    
    
    cb.set_label('Number retained sites (N)')                                       
    
    
    ## 4) Average Hs-Hk (".-k" means points + lines + black_color)
    plt.plot(Hs_avg, Hk_avg, ".-k", lw=1)     


    ## 5) Zoom in the resolution area where the slope is closest to -1 (set zoom = 5)
    axins = zoomed_inset_axes(ax, 5, loc="center", bbox_to_anchor=(0.55,0.35), bbox_transform=ax.transAxes)   
    
    #### 5.a) Creating a window with linewidth=1 and color "grey"
    for axis in ['top','bottom','left','right']:   
        axins.spines[axis].set_linewidth(1)       
        axins.spines[axis].set_color('grey')
    
    #### 5.b) Defining "Min_Hs_u < x1 < Max_Hs_u" and "Min_Hk_u < y  < Max_Hk_u"
    x1 = np.array([Min_Hs_area_best_slope, Max_Hs_area_best_slope])             
    y1 = np.array([Min_Hk_area_best_slope, Min_Hk_area_best_slope])                   
    y2 = np.array([Max_Hk_area_best_slope, Max_Hk_area_best_slope])
    
    #### 5.c) Filling zoom-window with a purple trasparent color
    axins.fill_between(x1, y1,y2, color='purple', alpha=.3, edgecolor="none")   
    
    #### 5.d) Plotting Scatter Plot in the zoom-window
    axins.plot(Hs_avg, Hk_avg, marker ="o", markerfacecolor='black', markeredgecolor='black', linestyle='solid', color='black', lw=2)    
    axins.scatter(Hs, Hk, c=N, s=5, cmap="viridis_r")#, norm=matplotlib.colors.PowerNorm(gamma=1. / 2.))
    axins.set_xlim(Min_Hs_area_best_slope-0.02, Max_Hs_area_best_slope+0.02)
    axins.set_ylim(Min_Hk_area_best_slope-0.005, Max_Hk_area_best_slope+0.005)
    plt.xticks([])
    plt.yticks([])
    mark_inset(ax, axins, loc1=2, loc2=4, edgecolor="0.5", facecolor="none")
    
     
     
    


# FUNCTION: Zoom of Resolution and Relevance curve (Hk-Hs) in the windows of Res where the slope is -1 
def Hs_Hk_scatter_plot_zoom(Hs_avg, Hk_avg, Hs_area_best_slope, Hk_area_best_slope, N_area_best_slope): 
    
    ## 1) Computing maximum and minimum value for Hs and Hk in the region where the slope is close to -1
    Max_Hk_area_best_slope = max(Hk_area_best_slope) 
    Min_Hk_area_best_slope = min(Hk_area_best_slope)
    
    Max_Hs_area_best_slope = max(Hs_area_best_slope) 
    Min_Hs_area_best_slope = min(Hs_area_best_slope)
    
    
    ## 2) Plotting Scatter Plot in the area where the slope is closest to -1. 
    
    points = plt.scatter(Hs_area_best_slope, Hk_area_best_slope, c=N_area_best_slope, s=15, cmap="viridis_r")  
    cb = plt.colorbar(points)   
    plt.plot(Hs_avg, Hk_avg, "-k", lw=2)
    plt.plot(Hs_avg, Hk_avg, "ok") 
    plt.ylim(Min_Hk_area_best_slope-0.01, Max_Hk_area_best_slope+0.01)    
    plt.xlim(Min_Hs_area_best_slope-0.01, Max_Hs_area_best_slope+0.01)
    
    
    ## 3) Writing title for plot, axis and color-bar
    
    plt.title("H[s]-H[k] in the region of interest")
    plt.ylabel('Relevance H[k]', horizontalalignment='center')
    plt.xlabel('Resolution H[s]', horizontalalignment='center')
    cb.set_label('Number retained sites (N)')
    
    


# FUNCTION: Slope versus Windows plot for 'density' option.     
def slope_plot_density_opt(slope, SlopeRange):
    
    ## 1) Computing the lenght of 'slope' list and tracing right line corresponding at y = -1. The slope will have such lenght minus 1 (slope_len - 1). 
    slope_len = len(slope)
    
    x = np.linspace(0,slope_len-1,20)    
    y = np.array(0*x-1)
    plt.plot(x, y, "-r", lw=1)   


    ## 2) Plotting 'slope' list with black lines and black points 
    plt.plot(slope, ".-k")
    
    
    ## 3) Plotting green points for underliying that they are close to -1 value of slope
    
    
    #### 3a) In case of  SlopeRange interval (-s/--SlopeRange <INT/FLOAT>%; default: 10%), green points will be plotted in such range (-1 +/- range)
    if(SlopeRange != "closest"): 
        
        SlopeRange_1Part = SlopeRange[:-1]
        SlopeRange_1Part = check_Int_Float_Str(SlopeRange_1Part)
        
        ValueSlope       = SlopeRange_1Part/100
        
        SlopeLeft        = -1 - ValueSlope
        SlopeRight       = -1 + ValueSlope 
        
        for i in slope:
            if(SlopeLeft < i < SlopeRight):
                plt.plot(slope.index(i), i, "og")
                
    
    #### 3b) If SlopeRange == "closest", then the closest point to -1 slope value is chosen; therefore only one green point will be plotted
    if(SlopeRange == "closest"): 
        
        u = -1 
        for i in slope: 
            closest_u     = [abs(x-u) for x in slope]
            
            index_closest = closest_u.index(min(closest_u))    
            closest_deriv = slope[index_closest]
        
        plt.plot(slope.index(closest_deriv), closest_deriv, "og")
        
        
    ## 4 Plotting the SlopeRange interval only if a SlopeRange interval has been set. The color of this rectangular range-windows is a purple trasparent color     
    if(SlopeRange != "closest"): 
        x1 = np.array([0, slope_len-1])            
        y1 = np.array([SlopeLeft, SlopeLeft])        
        y2 = np.array([SlopeRight, SlopeRight])
    
        plt.fill_between(x1, y1, y2, color='purple', alpha=.2, edgecolor="none")  
        
    
    ## 5) Writing title for plot and axis
    
    plt.title("Slope")
    plt.ylabel('Slope', horizontalalignment='center')
    plt.xlabel('index', horizontalalignment='center')
    
    
# FUNCTION: Plotting HISTOGRAM OF FREQUENCIES: Number of sites with more occourrences
def histo_Nsites_plot(ax, N_area_best_slope):
    
    ## 1) Creating a set of 'N_area_best_slope' and sorting it, in order to have only once the indices for the Number of Sites 
    ##    in the area where the slope is closest to -1
    set_N_area_best_slope = list(set(N_area_best_slope))    
    set_N_area_best_slope.sort()
    
    ## 2) Defining a step for plotting the bars of frequencies. This method allows to have a plot as clean as possible. 
    stepList = [set_N_area_best_slope[i+1] - set_N_area_best_slope[i] for i in range(len(set_N_area_best_slope)-1)]
    step     = min(stepList)
    
    ## 3) Transforming the 'N_area_best_slope' list corresponding at the Number of Sites where the slope is closest to -1, in an np.array   
    N_area_best_slope = np.array(N_area_best_slope)
    
    ## 4) Defining 'LABEL', i.e. the number of sites in the area where the slope is close to -1, 
    ##    and 'COUNTS' i.e. how many times the label is count (frequencies)
    labels, counts    = np.unique(N_area_best_slope, return_counts=True)  
    labels            = list(labels)
    labels            = [str(x) for x in labels]
    counts            = list(counts)
    
    ## 5) Creating histogram of frequencies
    bar_container = ax.bar(labels, counts, color="green", edgecolor="black", align='center')  
    
    ax.set(ylim=(0, max(counts)+2))
    ax.tick_params(axis='x', labelsize=6, rotation=70)
    
    ## 6) Writing title for plot and axis
    plt.title("Histogram")
    plt.ylabel('# occourrences ', horizontalalignment='center')
    plt.xlabel('Label', horizontalalignment='center')
    
