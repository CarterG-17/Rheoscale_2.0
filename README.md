# Rheoscale_2.0
### Description
RheoScale 2.0 (called rheoscale) is a Python-based analysis tool that classifies protein positions based on quantitative variant data. It reads a CSV file OR takes in a data containing measured values (e.g., enzyme activity, fluorescence, binding, etc.) for each amino acid substitution and assigns each position to classes such as: Neutral, Rheostat, Toggle, Moderate, Adverse, Enhancing, WT/inactive. The script also generates histograms and a summary output file that can be used for further analysis.

## Installation Instructions

to install python version run
```bash
python pip install rheoscale
```




## Usage/Quick Start


this will install rheoscale able to be used on any python scripts by importing rheoscale

### using as a python package

```python 

from rheoscale.rheoscale_config import RheoscaleConfig
from rheoscale.rheoscale_runner import RheoscaleRunner
import pandas as pd
```


if you already have your data loaded as a pandas DataFrame
```python
data #<- the data you had

#create config 
config = RheoscaleConfig('Protein name')


#run script
runner = RheoscaleRunner(config, data)
position_df =runner.run() #returns a Dataframe with positions calucations and numbers

```
if you need Rheoscale to load the data from a csv
```python


#create config 
config = RheoscaleConfig('Protein name', input_file_name=data_path)


#run script
runner = RheoscaleRunner(config)
position_df =runner.run() #returns a Dataframe with positions calucations and numbers

```
Simply put there are 2 steps to running the python rheoscale

#1. Creating a Configuration (RheoscaleConfig) object that sets all the parameters for analysis

#2. Creating a Runner (RheoscaleRunner) object that ensures that all set parameters of the config make sense and then a .run() command can be run


### CLI version
To use the command line interface of rheoscale you can run 
```bash
python -m rheoscale protein_name --input_file (--opitional_inputs)
```
### Excel version

to use the excel version just download the excel sheet from this git hub folder and use as need
to see more information please read the "How to use this calculator" tab found in the excel sheet 

## Documentation

Mainly the setting up the configuration object can be the most difficult task for running rheoscale
 

**Comming Soon: Jupyter UI with widgets... watch out**

**RheoscaleConfig (protein_name,** ***input_file_name***=*None*, ***number_of_positions***=*None*, ***log_scale***=*False*, ***WT_val***=*None*, ***WT_error***=*None*, ***WT_name***=*None*, ***min_val***=*None*, ***max_val***=*None*, ***error_val***=*None*, ***number_of_bins***=*None*, ***dead_extremum***=*'Min'*, ***neutral_binsize***=*None*, ***output_dir***=*None*, ***output_histogram_plots***=*False*, ***even_bins***=*True*, ***columns***=*mappingproxy({'position': 'Position', 'substitution': 'Substitution', 'value': 'Value', 'error': 'Error'}))*

### **Parameters:**

**input_file_name : str (path to CSV file)** <br>
If passing in a mutational data from a CSV file provide the path to the file here
this file must contain 4 columns:  Position, Substitution, Value, Error (these do not have to be the names of the columns see **columns** parameter)

**number_of_positions : int (Defalt= None)**<br>
To this is used as a check that Rheoscale sees the same amount of positions as you expect

**log_scale : bool (Defalt= False)**<br>
Any data set that spans more than three orders of magnitude should be converted to a log scale. Data sets that contain negative or zero values will result in errors if converted to a log scale; substitute with a value 10x smaller than the smallest value.

**WT_val: float (Default=None)** 
If WT values are not found in the DataFrame or CSV file giving to Rheoscale you can add them here. 

**WT_error : float (Default=None)** 
If WT values are given though the config you should also add the error here.

**WT_name : str (Default=None)**
if WT value are in DataFrame or CSV but do not have the label of "WT" in the position column the alternate name can be given here (*e.g.,* if the values are named "wild-type")

**min_val : float (Default=None)**
A data set may not contain the absolute minimum or maximum value associated with the functional data for this protein. The researcher may enter a min OR max value in the boxes below to override the min or max value found in the data set

**max_val : float (Default=None)**
A data set may not contain the absolute minimum or maximum value associated with the functional data for this protein. The researcher may enter a min OR max value in the boxes below to override the min or max value found in the data set

**error_val : float (Default=None)**
If data set does not have errors associated with each data point or if the overall data set is better represented by a predetermined error value, that value can be entered into this override box.

**number_of_bins : int (Default=None)**
If the recommended bin number is too small or large to provide meaningful data, a different bin number may be entered as an override. We recommend bin numbers between 7-13 with 10 being a good starting point. Further insight is provided in the manuscript (**citation**).

**dead_extremum : Literal["Min", "Max"] (Default='Min')**
Determine if the nonfunctional (dead) value associated with this protein and assay is a minimum or a maximum extremum. 

**neutral_binsize : float (Default=None)**
Override the Rheoscale calculated neutral binsize value 

**output_dir : str (Default='Rheoscale_analysis')**
name of the dirertory created by rheoscale

**output_histogram_plots : bool (Default=False)**
If False (default) will only output the "all" histogram for the full dataset. If True will output the position histogram of every position. 

**even_bins : bool (Default=True)**
If True (default), will make historgrams that place all values beyone "dead" and group them with other deads in histogram making all even bins. If False, will make "dead bin" larger to reflect the size of that bin based on the data

**columns : bool (Default=dict({'position': 'Position', 'substitution': 'Substitution', 'value': 'Value', 'error': 'Error'}))**
If your colums names do not match out names. Then creating a dict that maps the that names of the positions to each title. keys of this dict must always be: position, substitution, value, and error
*e.g.,*:
{"position": "Position",
 "substitution": 'Mutation',
 "value": 'Functional Value',
 "error": 'Error'}

## Examples

## License