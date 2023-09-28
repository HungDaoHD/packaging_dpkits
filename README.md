# Data processing Package

- Requirements
    - pandas
    - pyreadstat
    - numpy
    - zipfile
    - fastapi[UploadFile]

- Step 1: import classes
```
# Convert data to pandas dataframe
from dpkits.ap_data_converter import APDataConverter

# Calculate LSM score
from dpkits.calculate_lsm import LSMCalculation

# Transpose data to stack and untack
from dpkits.data_transpose import DataTranspose

# Create the tables from converted dataframe 
from dpkits.table_generator import DataTableGenerator

# Format data tables 
from dpkits.table_formater import TableFormatter
```

- Step 2: Convert data files to dataframe




- __init__(files, file_name, is_qme):
```
files: list[UploadFile] default = None
file_name: str default = ''
is_qme: bool default = True
```




This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.