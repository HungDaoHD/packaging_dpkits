# <center>`dpkits` Document</center>

## Note:
- All Scrip should be in `if __name__ == '__main__':` because of multiple proccessing.
- Only hide future warning of script by `warnings.simplefilter(action='ignore', category=FutureWarning)`
- Do __NOT__ hide script performance

## Class `APDataConverter`:
- Initialize `APDataConverter(file_name, is_qme)`:
  - file_name: `str` or `list[str]` 
  - is_qme: `bool` default `True`
```python
# Input file name
str_file_name = 'VN8413_ProjectName'

# output data table / topline file name
str_tbl_file_name = f'{str_file_name}_Topline.xlsx'

# Initialize Class APDataConverter with file_name
converter = APDataConverter(file_name=f'{str_file_name}.xlsx')

# Add dropping variables ==> these are will be removed while converting
converter.lstDrop.extend(['DV'])
```  
- Method `converter.convert_df_mc()`: _Convert input data file to 2 dataframes_
  - `df_data`:
  
      |  ID  | Q1_1 | Q1_2 | Q1_3 |
      |:----:|:----:|:----:|:----:|
      | 1001 |  1   |  3   |  5   |
      | 1002 |  2   |  5   | nan  |
  
  - `df_info`:
  
     | var_name | var_lbl  | var_type |                     val_lbl                      |
     |:--------:|:--------:|:--------:|:------------------------------------------------:|
     |   Q1_1   | label Q1 |    MA    | {'1': 'A', '2': 'B', '3': 'C', 4: 'D', '5': 'E'} |
     |   Q1_2   | label Q1 |    MA    | {'1': 'A', '2': 'B', '3': 'C', 4: 'D', '5': 'E'} |
     |   Q1_3   | label Q1 |    MA    | {'1': 'A', '2': 'B', '3': 'C', 4: 'D', '5': 'E'} |


- Method `converter.convert_df_md()`: Convert input data file to 2 dataframes_
  - `df_data`:

    |  ID  | Q1_1 | Q1_2 | Q1_3 | Q1_4 | Q1_5 |
    |:----:|:----:|:----:|:----:|:----:|:----:|
    | 1001 |  1   | nan  |  1   | nan  |  1   | 
    | 1002 | nan  |  1   | nan  | nan  |  1   |
  
  - `df_info`:
    
    | var_name |  var_lbl   | var_type |  val_lbl   |
    |:--------:|:----------:|:--------:|:----------:|
    |   Q1_1   | label Q1_A |    MA    | {'1': 'A'} |
    |   Q1_2   | label Q1_B |    MA    | {'1': 'B'} |
    |   Q1_3   | label Q1_C |    MA    | {'1': 'C'} |
    |   Q1_4   | label Q1_D |    MA    | {'1': 'D'} |
    |   Q1_5   | label Q1_E |    MA    | {'1': 'E'} |

- Method `converter.generate_multiple_data_files(dict_dfs, is_export_sav, is_export_xlsx, is_zip)`: _from `df_data` and `df_info` export *.xlsx, *.csv, *.sav_
  - dict_dfs: dict
  - is_export_sav: bool
  - is_export_xlsx: bool
  - is_zip: bool
```python

# dict_dfs: dict, is_export_sav: bool = True, is_export_xlsx: bool = True, is_zip: bool = True

dict_dfs = {
    1: {
        'data': df_data,
        'info': df_info,
        'tail_name': 'ByCode',
        'sheet_name': 'ByCode',
        'is_recode_to_lbl': False,
    },
    2: {
        'data': df_data,
        'info': df_info,
        'tail_name': 'ByText',
        'sheet_name': 'ByText',
        'is_recode_to_lbl': True,
    },
}

converter.generate_multiple_data_files(dict_dfs=dict_dfs, is_export_sav=False)
```

## Class `LSMCalculation`:
- Initialize `LSMCalculation()`: _no argument needed_
- Method `LSMCalculation.cal_lsm_6()`:
  - input: `df_data` and `df_info`
  - output: added variables to `df_data` and `df_info` and return them
    - CC1_Score, CC2_Score, CC3_Score, CC4_Score, CC5_Score, CC6_Score: calculate score from CC1 to CC6
    - LSM_Score sum of CC1_Score,..., CC6_Score
    - LSM: classify by LSM_Score
```python
lsm = LSMCalculation()
df_data, df_info = lsm.cal_lsm_6(df_data, df_info)
```

## Class `DataProcessing`:
## Class `DataTranspose`:
## Class `DataTableGenerator`:
## Class `TableFormatter`:
## Class `CodeframeReader`:

## Class `DataAnalysis`:


## Class `Tabulation`: