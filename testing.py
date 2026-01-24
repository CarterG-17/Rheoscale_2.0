from rheoscale.config import RheoscaleConfig
from rheoscale.rheoscale_runner import RheoscaleRunner
import pandas as pd, numpy as np
from dataclasses import replace
column_mapping = {
    'Position': 'position',
    '# of variants': 'num_of_variants',
    'Enhancing': 'enhancing_score',
    'Neutral': 'neutral_score',
    'Unweighted rheostat': 'rheostat_score',
    'Weighted rheostat': 'weighted_rheostat_score',
    'Toggle': 'toggle_score',
    'Binary': 'binary',
    'Average': 'average',
    'Standard Deviation': 'st_dev',
    'Assignment': 'assignment'
}
type_mapping = {
    '# of variants': int,
    'Enhancing': float,
    'Neutral': float,
    'Unweighted rheostat': float,
    'Weighted rheostat': float,
    'Toggle': float,
    
    'Standard Deviation': float,
    
}
def compare_dataframes(df1, df2):
    
    df1 = df1.set_index('position')
    df2 = df2.set_index('position')

    common_positions = df1.index.intersection(df2.index)

    df1 = df1.loc[common_positions]
    df2 = df2.loc[common_positions]
    
    comparison = (
    df1[['assignment']]
    .rename(columns={'assignment': 'assignment_df1'})
    .join(
        df2[['assignment']]
        .rename(columns={'assignment': 'assignment_df2'})
            )
    )

    comparison['match'] = (
        comparison['assignment_df1'].str.lower()
            == comparison['assignment_df2'].str.lower()
    )

    if not comparison['match'].all():
        print("There is at least one False")
        raise
    else:
        print('YAYAYAYAYAYA')
        return True

   
def compare_rheoscale(df_python: pd.DataFrame, path_to_RESULTS, name: str,sep='\t'):




    df_excel = pd.read_csv(path_to_RESULTS, sep=sep, on_bad_lines='skip')
    
    # Then convert columns, handling spaces/errors
    for col, dtype in type_mapping.items():
        if col in df_excel.columns:
            df_excel[col] = pd.to_numeric(df_excel[col], errors='coerce')

    # Drop rows where conversions failed (resulted in NaN)
    df_excel = df_excel.dropna(subset=list(type_mapping.keys()))

    df_excel = df_excel.dropna(how='any')
    df_python = df_python.dropna(how='any')
    
    
    df_excel = df_excel.rename(columns=column_mapping)    
    df_python = df_python.drop('histogram', axis=1)
    df_python = df_python.set_index('position', drop=False)
    df_excel = df_excel.set_index('position', drop=False)


    if compare_dataframes(df_python, df_excel):
        print(f'!!!!!  {name} IS A MATCH')




    pass

def make_config_from_excel(name, path_to_config, log_scale, columns:dict = None, sep='\t')-> RheoscaleConfig:


    df = pd.read_csv(path_to_config, sep=sep)
    if columns is None:
       my_config= RheoscaleConfig(name, output_histogram_plots=True)
    else:
        my_config= RheoscaleConfig(name, columns=columns, output_histogram_plots=True)
    my_dict = df.set_index(df.columns[0])[df.columns[1]].to_dict()

    if log_scale:
        my_config=replace(my_config,log_scale = True)

    if not pd.isna(my_dict['Minimum']):
        my_config=replace(my_config,min_val =float(my_dict['Minimum']))

    if not pd.isna(my_dict['Maximum']):
        my_config=replace(my_config,max_val = float(my_dict['Maximum']))

    if my_dict['Nonfunctional protein value ("Dead")'] != 'minimum':
        my_config=replace(my_config,dead_extremum = 'Max')
    
    if not pd.isna(my_dict['Error override']):
        my_config=replace(my_config,error_val = float(my_dict['Error override']))

    if not pd.isna(my_dict['Number of bins override']):
        my_config=replace(my_config,number_of_bins = int(my_dict['Number of bins override']))

    if not pd.isna(my_dict['Neutral Bin size override']):
        my_config=replace(my_config,neutral_binsize = float(my_dict['Neutral Bin size override']))

    if not pd.isna(my_dict['Enhancing Score assignment']):
        my_config=replace(my_config,enhancing_threshold = float(my_dict['Enhancing Score assignment']))

    if not pd.isna(my_dict['Neutral Score Assignment']):
        my_config=replace(my_config,enhancing_threshold = float(my_dict['Neutral Score assignment']))

    if not pd.isna(my_dict['Rheostat Score assignment']):
        my_config=replace(my_config,enhancing_threshold = float(my_dict['Rheostat Score assignment']))
    
    if not pd.isna(my_dict['Toggle Score assignment']):
        my_config= replace(my_config,enhancing_threshold = float(my_dict['Toggle Score assignment']))



    return my_config



def run_checker(path_to_data, path_to_config, path_to_results,columns,  name,sep='\t'):
    #for Mpro DATA
    mpro_df = pd.read_csv(path_to_data, sep=sep)
    mpro_data_columns = columns
    mpro_config = make_config_from_excel(name, path_to_config, False, columns, sep=sep)
    #mpro_config = RheoscaleConfig(min_val=0.07, columns=columns, output_histogram_plots=False, output_folder_name_prefix='Mpro_2022_run_2')
    #mpro_config = RheoscaleConfig.from_json(r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\New_implemetation\Rheoscale_analysis\_Rheoscale\running_config.json")
    mpro_rheoscale = RheoscaleRunner(mpro_config, mpro_df)
    python_output =mpro_rheoscale.run()
    
    path_to_exceloutput = path_to_results
    
    compare_rheoscale(python_output, path_to_exceloutput, name)



def main():
    
    #for mpro data
    mpro_path_to_data = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\Carter_Mpro_2024\DATA.tsv"
    mpro_path_to_results = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\Carter_Mpro_2024\RESULTS.tsv"
    mpro_path_to_config = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\Carter_Mpro_2024\CONFIG.tsv"
    name = 'Mpro_2024_carter_style'
    mpro_columns = {"position": "Position",
            "substitution": 'Mutation',
            "value": 'Functional Value',
            "error": 'Error'}
    run = run_checker(mpro_path_to_data,mpro_path_to_config, mpro_path_to_results, mpro_columns, name)
    #position_info = run.position_data
    
    
    
    pass
    #for Lener lab 
    len_path_to_data = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_lener\L_DATA.tsv"
    
    len_path_to_results = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_lener\L_RESULTS.tsv"
    len_path_to_config = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_lener\L_CONFIG.tsv"
    name = 'Lener'
    mpro_columns = {"position": "Position",
            "substitution": 'Mutation',
            "value": 'Functional Value',
            "error": 'Error'}
    run = run_checker(len_path_to_data,len_path_to_config, len_path_to_results, mpro_columns, name)
    #for rocklin lab
    rock_path_to_data = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_rocklin\R_DATA.tsv"
    
    rock_path_to_config = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_rocklin\R_CONFIG.tsv"
    rock_path_to_results = r"C:\Lab_code\Rheoscale 2.0\RheoScale2.0-Dec25\Carters_runs\Check_rheoscale\hannah_rocklin\R_RESULTS.tsv"
    name = 'rock'
    mpro_columns = {"position": "Position",
            "substitution": 'Mutation',
            "value": 'Functional Value',
            "error": 'Error'}
    run = run_checker(rock_path_to_data,rock_path_to_config, rock_path_to_results, mpro_columns, name)
    
    
    pass


main()