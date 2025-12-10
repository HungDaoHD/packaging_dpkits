from dpkits2.converter.data_converter import *


# # # ------------------------------------------------------------------------------------------------------------------


# # # START HERE
converter = DataConverter(InputFile(folder_name='DataToRun', file_name='VN9999 - Project Name.xlsx'))
output = converter.convert()





output.metadata.qres['AGE2'].codes[9002] = NettedCode(
    value=9002,
    label='abc def ghi',
    netted_type='Net',
    netted_fields=['5', '6', '7'] 
)



output.metadata.save_json('metadata.json')


# output.metadata = output.metadata.from_json_file('metadata.json')

# aaa = output.metadata.qres

print('>>> Finish Task')





