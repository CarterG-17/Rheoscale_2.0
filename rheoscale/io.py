# io.py
import pandas as pd, os
from types import MappingProxyType
from typing import Optional
from .config import RheoscaleConfig

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
    
def write_outputs(running_config, position_df):
    
    
    pass


