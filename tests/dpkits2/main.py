from dpkits2.manager import Manager
from dpkits2.metadata.questions import *


mgr = Manager(folder_name='tests\\dpkits2\\DataToRun', file_name='VN9999 - Project Name.xlsx')
mgr.run()


# add / update / remove qres in data & metadata
lst_new_qres = [
    QreFreeText(name='New_FT', label='Add new FT testing'),
    QreNumeric(name='New_NUM', label='Add New NUM testing'),
    'ádsadasdsa',
    123123123123
    
    # QreSingleAnswer(
    #     name='New_SA_Scale', label='New_SA_Scale. Testing', index=999999,
    #     data_fields=['New_SA_Scale'],
    #     codes={
    #         1: GeneralCode(value=1, label='5pt', factor=5),
    #         2: GeneralCode(value=2, label='4pt', factor=4),
    #         3: GeneralCode(value=3, label='3pt', factor=3),
    #         4: GeneralCode(value=4, label='2pt', factor=2),
    #         5: GeneralCode(value=5, label='1pt', factor=1),
    #     }
    # ),
    # QreSingleAnswer(
    #     name='New_SA_Others_Exclusive', label='New_SA_Others_Exclusive. Testing', index=999999,
    #     data_fields=['New_SA_Others_Exclusive'],
    #     other_fields={
    #         'New_SA_Others_Exclusive_o7': QreFreeText(name='New_SA_Others_Exclusive_o7', label='New_SA_Others_Exclusive_o7. Testing', data_fields=['New_SA_Others_Exclusive_o7'], index=999999),
    #         'New_SA_Others_Exclusive_o8': QreFreeText(name='New_SA_Others_Exclusive_o8', label='New_SA_Others_Exclusive_o8. Testing', data_fields=['New_SA_Others_Exclusive_o8'], index=999999),
    #     },
    #     codes={
            
    #         9001: NettedCode(value=9001, label='Grp A', netted_type='Net', netted_fields=[1, 2, 3]),
    #         1: GeneralCode(value=1, label='1. AAA'),
    #         2: GeneralCode(value=2, label='2. BBB'),
    #         3: GeneralCode(value=3, label='3. CCC'),
            
    #         9002: NettedCode(value=9002, label='Grp B', netted_type='Combine', netted_fields=[4, 5, 6]),
    #         4: GeneralCode(value=4, label='4. DDD'),
    #         5: GeneralCode(value=5, label='5. EEE'),
    #         6: GeneralCode(value=6, label='6. FFF'),
            
    #         9003: NettedCode(value=9003, label='Grp Others', netted_type='Combine', netted_fields=[7, 8]),
    #         7: GeneralCode(value=7, label='7. Other', is_other=True),
    #         8: GeneralCode(value=8, label='8. Other', is_other=True),
            
    #         9: GeneralCode(value=9, label='9. DK', is_exclusive=True),
            
    #     }
    # ),
    # QreMultipleAnswer(
    #     name='New_MA', label='New_MA. Testing - has other & excl', 
    #     data_fields=['New_MA_1', 'New_MA_2', 'New_MA_3', 'New_MA_4', 'New_MA_5', 'New_MA_6', 'New_MA_7', 'New_MA_8', 'New_MA_9', 'New_MA_10'], index=999999,
    #     other_fields={
    #         'New_MA_o7': QreFreeText(name='New_MA_o7', label='New_MA_o7. Testing', data_fields=['New_MA_o7'], index=999999),
    #         'New_MA_o8': QreFreeText(name='New_MA_o8', label='New_MA_o8. Testing', data_fields=['New_MA_o8'], index=999999),
    #         'New_MA_o10': QreFreeText(name='New_MA_o10', label='New_MA_o10. Testing', data_fields=['New_MA_o10'], index=999999),
    #     },
    #     codes={
            
    #         9001: NettedCode(value=9001, label='Grp A', netted_type='Net', netted_fields=[1, 2, 3]),
    #         1: GeneralCode(value=1, label='1. AAA'),
    #         2: GeneralCode(value=2, label='2. BBB'),
    #         3: GeneralCode(value=3, label='3. CCC'),
            
    #         9002: NettedCode(value=9002, label='Grp B', netted_type='Combine', netted_fields=[4, 5, 6]),
    #         4: GeneralCode(value=4, label='4. DDD'),
    #         5: GeneralCode(value=5, label='5. EEE'),
    #         6: GeneralCode(value=6, label='6. FFF'),
            
    #         9003: NettedCode(value=9003, label='Grp Others', netted_type='Combine', netted_fields=[7, 8]),
    #         7: GeneralCode(value=7, label='7. Other', is_other=True),
    #         8: GeneralCode(value=8, label='8. Other', is_other=True),
    #         10: GeneralCode(value=10, label='10. Other', is_other=True),
            
    #         9: GeneralCode(value=9, label='9. DK', is_exclusive=True),
            
    #     }
    # ),
    
]


# HERE
mgr.add_qres(qres=lst_new_qres)




mgr.metadata_to_json('tests\\dpkits2\\metadata.json')
# mgr.data_box.metadata = mgr.data_box.metadata.from_json_file(filepath='tests\\dpkits2\\metadata.json')








# validate metadata vs df_data

# transform to stack data & metadata

# visual data to data table

# run advance models


print('COMPLETED')





