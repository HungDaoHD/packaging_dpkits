# IGNORE THIS-----------------------------------------------------------------------------------------------------------
from fastapi import UploadFile
import sys
sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits/src/dpkits')
from AP_DataConverter import APDataConverter
from calculate_lsm import LSMCalculation
# IGNORE THIS-----------------------------------------------------------------------------------------------------------


# from dpkits.AP_DataConverter import APDataConverter
# from dpkits.calculate_lsm import LSMCalculation


# Call Class APDataConverter with file_name
converter = APDataConverter(file_name='APDataTest.xlsx')

# convert input file to dataframe
# df_data: contains data as pandas dataframe
# df_info: contains data info as pandas dataframe (ex: var_name, var_lbl, var_type, val_lbl)
# var_name = data column name (variable)
# var_lbl = variable label
# var_type = variable type
# val_lbl = value label

df_data, df_info = converter.convert_df_mc()  # Use 'converter.convert_df_md()' if you need md data

df_data, df_info = LSMCalculation.cal_lsm_6(df_data, df_info)

# # AFTER CONVERTING YOU CAN DO ANYTHING WITH DATAFRAME-------------------------------------------------------------------
#
# # FOR EXAMPLE:
# # CONVERT DATA FROM STRING TO NUMERIC
# df_data['Q0a_RespondentID'] = df_data['Q0a_RespondentID'].astype(int)
# df_info.loc[df_info['var_name'] == 'Q0a_RespondentID', ['var_type']] = ['NUM']
#
# # UPDATING DATA
# df_data.loc[df_data['Q0a_RespondentID'] == 1001, ['Q0b_Name']] = ['new']
#
# # ----------------------------------------------------------------------------------------------------------------------


# EXPORTING TO SAV DATA FILES-------------------------------------------------------------------------------------------
dict_dfs = {
    1: {
        'data': df_data,
        'info': df_info,
        'tail_name': 'byCode',
        'sheet_name': 'byCode',
        'is_recode_to_lbl': False,
    },
    2: {
        'data': df_data,
        'info': df_info,
        'tail_name': 'byLabel',
        'sheet_name': 'byLabel',
        'is_recode_to_lbl': True,
    },
}


converter.generate_multiple_sav_sps(dict_dfs=dict_dfs, is_md=False, is_export_xlsx=True, is_zip=True)
# ----------------------------------------------------------------------------------------------------------------------


print('\n==>TESTING PROCESS DONE')