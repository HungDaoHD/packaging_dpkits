from fastapi import UploadFile

# import sys
# sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits/src/dpkits')
# from AP_DataConverter import APDataConverter


from dpkits.AP_DataConverter import APDataConverter



with open('apdatatest.xlsx', 'rb') as data_file:
    file = UploadFile(file=data_file, filename='apdatatest.xlsx', content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    converter = APDataConverter(files=[file])
    df_data, df_info = converter.convert_df_mc()

df_data.to_excel('df_data.xlsx')
df_info.to_excel('df_info.xlsx')