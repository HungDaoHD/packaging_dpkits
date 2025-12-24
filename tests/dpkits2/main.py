from dpkits2.manager import Manager
from dpkits2.metadata.questions import *


mgr = Manager(folder_name='tests\\dpkits2\\DataToRun', file_name='VN9999 - Project Name.xlsx')
mgr.run()


# add / update / remove qres in data & metadata
lst_new_qres = [
    
    QreFreeText(name='New_FT', label='Add new FT testing'),
    QreNumeric(name='New_NUM', label='Add New NUM testing'),
    
    QreSingleAnswer(
        name='New_SA_Scale', label='New_SA_Scale. Testing',
        codes=[
            GeneralCode(value=1, label='5pt', factor=5),
            GeneralCode(value=2, label='4pt', factor=4),
            GeneralCode(value=3, label='3pt', factor=3),
            GeneralCode(value=4, label='2pt', factor=2),
            GeneralCode(value=5, label='1pt', factor=1),
        ]
    ),
    
    QreSingleAnswer(
        name='New_SA_Others_Exclusive', label='New_SA_Others_Exclusive. Testing',
        codes=[
            NettedCode(value=9001, label='Grp A', netted_type='Net', netted_fields=[1, 2, 3]),
            GeneralCode(value=1, label='1. AAA'),
            GeneralCode(value=2, label='2. BBB'),
            GeneralCode(value=3, label='3. CCC'),
            NettedCode(value=9002, label='Grp B', netted_type='Combine', netted_fields=[4, 5, 6]),
            GeneralCode(value=4, label='4. DDD'),
            GeneralCode(value=5, label='5. EEE'),
            GeneralCode(value=6, label='6. FFF'),
            NettedCode(value=9003, label='Grp Others', netted_type='Combine', netted_fields=[7, 8]),
            GeneralCode(value=7, label='7. Other', is_other=True),
            GeneralCode(value=8, label='8. Other', is_other=True),
            GeneralCode(value=9, label='9. DK', is_exclusive=True),
        ],
        other_fields=[
            QreFreeText(name='New_SA_Others_Exclusive_o7', label='New_SA_Others_Exclusive_o7. Testing'),
            QreFreeText(name='New_SA_Others_Exclusive_o8', label='New_SA_Others_Exclusive_o8. Testing'),
        ]  
    ),
    
    QreMultipleAnswer(
        name='New_MA', label='New_MA. Testing - has other & excl',
        codes=[
            NettedCode(value=9001, label='Grp A', netted_type='Net', netted_fields=[1, 2, 3]),
            GeneralCode(value=1, label='1. AAA'),
            GeneralCode(value=2, label='2. BBB'),
            GeneralCode(value=3, label='3. CCC'),
            NettedCode(value=9002, label='Grp B', netted_type='Combine', netted_fields=[4, 5, 6]),
            GeneralCode(value=4, label='4. DDD'),
            GeneralCode(value=5, label='5. EEE'),
            GeneralCode(value=6, label='6. FFF'),
            NettedCode(value=9003, label='Grp Others', netted_type='Combine', netted_fields=[7, 8]),
            GeneralCode(value=7, label='7. Other', is_other=True),
            GeneralCode(value=8, label='8. Other', is_other=True),
            GeneralCode(value=10, label='10. Other', is_other=True),
            GeneralCode(value=9, label='9. DK', is_exclusive=True),
        ],
        other_fields=[
            QreFreeText(name='New_MA_o7', label='New_MA_o7. Testing'),
            QreFreeText(name='New_MA_o8', label='New_MA_o8. Testing'),
            QreFreeText(name='New_MA_o10', label='New_MA_o10. Testing'),
        ],
    ),
    
    # QreMatrix(
    #     name='New_Matrix', label='New_Matrix.Testing',
            
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





