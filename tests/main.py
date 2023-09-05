# from fastapi import UploadFile
# import sys
# sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits/src/dpkits')
# from AP_DataConverter import APDataConverter


from dpkits.AP_DataConverter import APDataConverter



# with open('apdatatest.xlsx', 'rb') as data_file:
#     file = UploadFile(file=data_file, filename='apdatatest.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     converter = APDataConverter(files=[file])
#     df_data, df_info = converter.convert_df_mc()


converter = APDataConverter(file_name='apdatatest.xlsx')
df_data, df_info = converter.convert_df_mc()

# df_data.to_excel('df_data.xlsx')
# df_info.to_excel('df_info.xlsx')

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

converter.generate_multiple_sav_sps(dict_dfs=dict_dfs, is_md=False, is_export_xlsx=True)


print('TESTING DONE')