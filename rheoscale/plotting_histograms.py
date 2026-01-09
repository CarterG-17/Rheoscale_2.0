import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def plot_all_positions(DMS_df):

    for position in DMS_df['Position'].unique():
        position_df = DMS_df[DMS_df['Position'] == position]
        make_tuning_plot_one_pos(position_df)

    
def make_tuning_plot_one_pos(df_with_data, bins, output_name, position_number, is_log_scale, wt_value=1, dead_value=0, is_without_stop_codon=True):
    if is_without_stop_codon:
        df_with_data = df_with_data[df_with_data['Substitution'] != '*']
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    
        # Prepare data
    df = pd.DataFrame({'values': list(df_with_data['Value'])})
        
    # Define bins  
    
    df['binned'] = pd.cut(df['values'], bins=bins, include_lowest=True)
    
    bin_counts = df['binned'].value_counts().sort_index()
    
    # Plot bars 

    ax1.set_xticks(range(len(bins)))

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
