import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .data_stuctures import HistogramData

def plot_all_positions(positions: list, hist_list: list, dead_extremum, WT_value,save_path, prefix=''):
    for i in range(len(positions)):
        name = prefix+'_pos_'+str(positions[i])
        make_tuning_plot_one_pos(hist_list[i], dead_extremum, WT_value, save_path, tle=name)

    
def make_tuning_plot_one_pos(hist_data: HistogramData , dead_extremum, WT_value,path,     
    tle: str = "Histogram",
    xlabel: str = "Value",
    ylabel: str = "Count",
    log_y: bool = True,
    label_precision: int = 2):
        
        counts = hist_data.counts
        bin_edges = hist_data.bin_edges

        # ---- sanity check ----
        if len(bin_edges) != len(counts) + 1:
            raise ValueError("bin_edges must be one element longer than counts")

        
        bin_widths = np.diff(bin_edges)
        bin_centers = bin_edges[:-1] + bin_widths / 2


        
        fmt = f"{{:.{label_precision}f}}"
        bin_labels = [
            f"{fmt.format(left)}–{fmt.format(right)}"
            for left, right in zip(bin_edges[:-1], bin_edges[1:])
        ]

        # ---- create figure & axes ----
        fig, ax = plt.subplots()

        # ---- plot ----
        ax.bar(
            bin_centers,
            counts,
            width=bin_widths*0.66,
            align="center",
            color='black'
        )
        
        

        WT_index =  np.digitize(WT_value, bin_edges) - 1
        WT_bin_center = bin_centers[WT_index]

        if dead_extremum == 'Min':
            regular_bin_size = bin_widths[-1]/2
            ax.axvspan(bin_edges[0], bin_edges[1], alpha=0.3, color='red')
        else: 
             ax.axvspan(bin_edges[-1], bin_edges[-2], alpha=0.3, color='red')
             regular_bin_size = bin_widths[0]/2

        ax.axvspan(WT_bin_center-regular_bin_size, WT_bin_center+regular_bin_size, alpha=0.3, color='green')

        # ---- axes formatting ----
        ax.set_ylim(0.001, 21)
        ax.set_yticks([i for i in range(5,21, 5)])
        ax.set_xticks(bin_centers)
        ax.set_xticklabels(bin_labels, rotation=45, ha="right")

        ax.set_xlabel(xlabel)
        ax.set_title(tle)

        if log_y:
            pass
            #ax.set_yscale("log")

        fig.tight_layout()
        plt.savefig(rf'{path}\{tle}.png')
        plt.close()

        





'''

    ax1.set_ylim(0, 20.5)
    ax1.set_yticks([i for i in range(0,21, 5)])
    ax1.bar(bin_counts.index.astype(str), bin_counts.values, width=.5,
            label='All subs', color='black', zorder=1)
    
    #Make WT frame
    WT_bin_index = np.digitize(wt_value, bins) - 1

    # safety check
    if 0 <= WT_bin_index < len(bins) - 1:
        #will make a WT indication on the bin at
        ax1.axvspan(bins[WT_bin_index], bins[WT_bin_index + 1], color='green', alpha=0.3, label='Wild-type')
    
    #Make dead frame
    dead_bin_index = np.digitize(dead_value, bins) - 1

    # safety check
    if 0 <= dead_bin_index < len(bins) - 1:
        ax1.axvspan(bins[dead_bin_index], bins[dead_bin_index + 1], color='red', alpha=0.3, label='Dead')
    
    
    ax1.tick_params(axis='x', rotation=45)
    plt.setp(ax1.get_xticklabels(), ha='right')
    ax1.set_xlabel("Log10(Value)" if is_log_scale else "Value", fontsize=14, fontfamily='Arial')
    ax1.set_ylabel("Number of Variants", fontsize=14, fontfamily='Arial')
    
    ax1.legend()
     
    ax1.set_title(f'Position {position_number}')
    
    plt.tight_layout()
    plt.savefig(output_name, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    '''
