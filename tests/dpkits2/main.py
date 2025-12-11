from dpkits2.manager import Manager
from dpkits2.metadata.questions import *


mgr = Manager(folder_name='tests\\dpkits2\\DataToRun', file_name='VN9999 - Project Name.xlsx')
mgr.run()
mgr.metadata_to_json('tests\\dpkits2\\metadata.json')



# add / update / remove qres in data & metadata

# validate metadata vs df_data

# transform to stack data & metadata

# visual data to data table

# run advance models


print('FINISH TASKS')





