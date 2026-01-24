# io.py
import pandas as pd, os
from types import MappingProxyType
from typing import Optional
from .config import RheoscaleConfig
from .plotting_histograms import plot_all_positions

def load_data(config: RheoscaleConfig) -> pd.DataFrame:

    # Otherwise load from file
    if config.input_file_name is not None:
        DMS_data = pd.read_csv(config.input_file_name)
        
        return DMS_data
    else:
        raise ValueError('Either a input file must be entered within the configeration XOR a df must be added during this call')
    
    
def validate_columns(df: pd.DataFrame, config: RheoscaleConfig):
    missing = set(config.columns.values()) - set(df.columns)

    if not missing:
        print("Column names in config match the CSV or DataFrame")
    else:
        raise ValueError(
            f"Missing columns in DataFrame: {missing}"
        )
    
def write_outputs(running_config: RheoscaleConfig, position_df: pd.DataFrame):
    out_dir = running_config.output_dir
    json_path = rf'{out_dir}\running_config.json'
    #make_config_output 
    print('hello')
    running_config.to_json(json_path)

    #make data sheet output 
    data_path = rf'{out_dir}\raw_data.csv'
    position_df.to_csv(data_path)

    #just classifcations
    just_pos_and_assign = position_df[['position', 'assignment']]
    class_path = rf'{out_dir}\classifications.csv'
    position_df.to_csv(class_path)

    if running_config.output_histogram_plots:
        is_hist_plots = True
    else:
        is_hist_plots= False
    if running_config.dead_extremum == "Min":
        dead_value = running_config.min_val
    else:
        dead_value = running_config.max_val

    position_list = position_df['position'].to_list()
    hist_list = position_df['histogram'].to_list()
    plot_output = rf'{out_dir}\{running_config.protein_name}_plots'
    os.makedirs(plot_output, exist_ok=True)
    plot_all_positions(position_list, hist_list, running_config.dead_extremum, running_config.WT_val,dead_value ,plot_output, running_config.neutral_binsize,running_config.protein_name, is_hist_plots, is_even_bins=running_config.even_bins)




