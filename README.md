# Rheoscale_2.0
### Description
RheoScale 2.0 is a Python-based analysis tool that classifies protein positions based on quantitative variant data. It reads a CSV file containing measured values (e.g., enzyme activity, fluorescence, binding, etc.) for each amino acid substitution and assigns each position to classes such as: Neutral, Rheostat, Toggle, Moderate, Adverse, Enhancing, WT/inactive. The script also generates histograms and a summary output file that can be used for further analysis.

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
data <- the data you had

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



### CLI version
To use the command line interface of rheoscale you can run 
```bash
python -m rheoscale protein_name --input_file (--opitional_inputs)
```
### Excel version

to use the excel version just download the excel sheet from this git hub folder and use as need
to see more information please read the "How to use this calculator" tab found in the excel sheet 

## Documentation

## Examples

## License