# # # THIS USE BY ADMIN-------------------------------------------------------------------------------------------------
import sys
sys.path.insert(0, "C:\\Users\\PC\\OneDrive\\DevZone\\PyPackages\\packaging_dpkits\\src")

from dpkits2 import (
    DataConverter,
    InputFile,

)
# # # ------------------------------------------------------------------------------------------------------------------


# # # START HERE
converter = DataConverter(InputFile(folder_name='DataToRun', file_name='VN9999 - Project Name.xlsx'))
converter.convert()










print('>>>>>>>>>>>>>>>>>>> Finish Task')





