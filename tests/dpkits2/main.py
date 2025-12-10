from dpkits2 import *


# # # ------------------------------------------------------------------------------------------------------------------


# # # START HERE
cvt = DataConverter(InputFile(folder_name='tests\\dpkits2\\DataToRun', file_name='VN9999 - Project Name.xlsx'))
output = cvt.convert()


output.metadata.qres['AGE2'].codes[9002] = NettedCode(
    value=9002,
    label='abc def ghi',
    netted_type='Net',
    netted_fields=['5', '6', '7'] 
)



output.metadata.save_json('tests\\dpkits2\\metadata.json')


# output.metadata = output.metadata.from_json_file('metadata.json')

# aaa = output.metadata.qres

print('>>> Finish Tasks')





