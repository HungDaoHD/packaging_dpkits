import pandas as pd


# # IGNORE THIS-----------------------------------------------------------------------------------------------------------
# from fastapi import UploadFile
# import sys
# sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits/src/dpkits')
#
# from ap_data_converter import APDataConverter
# from calculate_lsm import LSMCalculation
# from data_transpose import DataTranspose
# # IGNORE THIS-----------------------------------------------------------------------------------------------------------


from dpkits.ap_data_converter import APDataConverter
from dpkits.calculate_lsm import LSMCalculation
from dpkits.data_transpose import DataTranspose


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

# LSM 6 CALCULATION - Only use for Unilever project which has LSM questions
df_data, df_info = LSMCalculation.cal_lsm_6(df_data, df_info)

df_data = pd.DataFrame(df_data)
df_info = pd.DataFrame(df_info)





# AFTER CONVERTING YOU CAN DO ANYTHING WITH DATAFRAME-------------------------------------------------------------------

# # FOR EXAMPLE:
# # CONVERT DATA FROM STRING TO NUMERIC
# df_data['Q0a_RespondentID'] = df_data['Q0a_RespondentID'].astype(int)
# df_info.loc[df_info['var_name'] == 'Q0a_RespondentID', ['var_type']] = ['NUM']
#
# # UPDATING DATA
# df_data.loc[df_data['Q0a_RespondentID'] == 1001, ['Q0b_Name']] = ['new']


# TRANSPOSE TO STACK
dict_stack_structure = {
    'id_col': 'ResID',
    'sp_col': 'Ma_SP',
    'lst_scr': ['Gender', 'Age', 'City', 'HHI'],
    'dict_sp': {
        1: {
            'Ma_SP1': 'Ma_SP',
            'Q1_SP1': 'Q1',
            'Q2_SP1': 'Q2',
            'Q3_SP1': 'Q3',
        },
        2: {
            'Ma_SP2': 'Ma_SP',
            'Q1_SP2': 'Q1',
            'Q2_SP2': 'Q2',
            'Q3_SP2': 'Q3',
         },
    },
    'lst_fc': ['Awareness1', 'Frequency', 'Awareness2', 'Perception']
}

df_data_stack, df_info_stack = DataTranspose.to_stack(df_data, df_info, dict_stack_structure)


# TRANSPOSE TO UNSTACK
dict_unstack_structure = {
    'id_col': 'ResID',
    'sp_col': 'Ma_SP',
    'lst_col_part_head': ['Gender', 'Age', 'City', 'HHI'],
    'lst_col_part_body': ['Q1', 'Q2', 'Q3'],
    'lst_col_part_tail': ['Awareness1', 'Frequency', 'Awareness2', 'Perception']
}

df_data_unstack, df_info_unstack = DataTranspose.to_unstack(df_data_stack, df_info_stack, dict_unstack_structure)

# ----------------------------------------------------------------------------------------------------------------------




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
    3: {
        'data': df_data_stack,
        'info': df_info_stack,
        'tail_name': 'stack',
        'sheet_name': 'stack',
        'is_recode_to_lbl': False,
    },
    4: {
        'data': df_data_unstack,
        'info': df_info_unstack,
        'tail_name': 'unstack',
        'sheet_name': 'unstack',
        'is_recode_to_lbl': False,
    },
}

converter.generate_multiple_sav_sps(dict_dfs=dict_dfs, is_md=False, is_export_xlsx=True, is_zip=True)
# ----------------------------------------------------------------------------------------------------------------------


print('\n==>TESTING PROCESS DONE')