import warnings
import pandas as pd
import numpy as np
import time
import datetime


# from dpkits import (
#     APDataConverter,
#     DataProcessing,
#     DataTranspose,
#     DataTableGenerator,
#     Tabulation,
#     TableFormatter,
#     CodeframeReader,
#     LSMCalculation,
# )



# IGNORE THIS-----------------------------------------------------------------------------------------------------------
import sys
sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits')

from src.dpkits import (
    APDataConverter,
    DataProcessing,
    DataTranspose,
    DataTableGenerator,
    TableFormatter,
    CodeframeReader,
    LSMCalculation,
    DataAnalysis,
    Tabulation
)
# IGNORE THIS-----------------------------------------------------------------------------------------------------------


import win32com.client


# Initialize PowerPoint Application
ppt = win32com.client.Dispatch("PowerPoint.Application")
ppt.Visible = True  # Optional: Make PowerPoint visible

# Open the source and target presentations
source_ppt = ppt.Presentations.Open(r"C:\Users\PC\OneDrive\Dev Area\PyPackages\packaging_dpkits\tests\Acecook audit output sample_102224 - Template.pptx")
target_ppt = ppt.Presentations.Open(r"C:\Users\PC\OneDrive\Dev Area\PyPackages\packaging_dpkits\tests\Acecook audit output sample_102224 - Template_Output.pptx")


# Loop through all slides in reverse order and delete each one
for i in range(target_ppt.Slides.Count, 0, -1):
    target_ppt.Slides(i).Delete()

for source_slide in source_ppt.Slides:

    # # Select the slide to copy (e.g., the first slide)
    # source_slide = source_ppt.Slides(1)  # 1-based index for slides in PowerPoint

    # Copy the slide
    source_slide.Copy()

    # Paste the slide into the target presentation at the desired position
    target_ppt.Slides.Paste(len(target_ppt.Slides) + 1)  # Paste as the last slide



# Select the slide that contains the table (e.g., slide 1)

for i, slide in enumerate(target_ppt.Slides):

    print(f"Slide {slide.SlideIndex}:")

    # slide = target_ppt.Slides(1)  # 1-based index

    # Find the table shape (assuming it's the first shape with a table)
    for j, shape in enumerate(slide.Shapes):

        print(f"  Shape Name: {shape.Name}")

        # If the shape has a text frame, print the text
        if shape.HasTextFrame:
            text = shape.TextFrame.TextRange.Text
            if text:
                print(f"    Text: {text}")


        if shape.HasTable:
            table = shape.Table
            for row in range(1, table.Rows.Count + 1):
                for col in range(1, table.Columns.Count + 1):
                    cell_text = table.Cell(row, col).Shape.TextFrame.TextRange.Text
                    print(f"    Table Cell ({row}, {col}): {cell_text}")

            # # Modify the values in the table (row 1, column 1, for example)
            # # PowerPoint tables are 1-based indexing
            # table.Cell(2, 2).Shape.TextFrame.TextRange.Text = "11%"
            # table.Cell(2, 3).Shape.TextFrame.TextRange.Text = "12%"
            # table.Cell(2, 4).Shape.TextFrame.TextRange.Text = "66%"
            # table.Cell(2, 5).Shape.TextFrame.TextRange.Text = "88%"


        if shape.HasChart:

            chart = shape.Chart
            # chart_title = chart.ChartTitle.Text
            # print(f"    Chart Title: {chart_title}")

            # Access the embedded Excel workbook
            workbook = chart.ChartData.Workbook
            worksheet = workbook.Worksheets(1)  # Get the first worksheet

            # Iterate over the used range in the worksheet and print the data
            used_range = worksheet.UsedRange
            for row in range(1, used_range.Rows.Count + 1):
                row_data = []
                for col in range(1, used_range.Columns.Count + 1):
                    cell_value = worksheet.Cells(row, col).Value
                    row_data.append(cell_value)
                print(f"    Row {row}: {row_data}")

            # Close the Excel workbook (optional, if you don't want to edit anything)
            workbook.Close()

            if i == 1 and j == 12:

                chart = shape.Chart

                # Access the Excel workbook linked to the chart
                workbook = chart.ChartData.Workbook
                worksheet = workbook.Worksheets(1)  # Get the first worksheet

                # Update data in the worksheet
                worksheet.Cells(2, 2).Value = .45  # Modify the value at row 2, column 2
                worksheet.Cells(3, 2).Value = .55  # Modify the value at row 3, column 2

                # Activate the chart's data
                chart.ChartData.Activate()

                # Close the workbook after changes
                workbook.Close()

                # Update the chart in PowerPoint (optional, may update automatically)
                chart.Refresh()



    print()



# Save the updated target presentation
target_ppt.Save()

# Optional: Close the presentations
source_ppt.Close()
target_ppt.Close()

# Quit PowerPoint Application
ppt.Quit()

















# if __name__ == '__main__':
#
#     warnings.simplefilter(action='ignore', category=FutureWarning)
#
#     st = time.time()
#
#     # Define input/output files name
#     str_file_name = 'DataToRun/VN8543 - FINHAY'
#     str_tbl_file_name = f'{str_file_name} - Topline.xlsx'
#
#     # Call Class APDataConverter with file_name
#     converter = APDataConverter(file_name=f'{str_file_name}.xlsx')
#
#     # df_data, df_info = converter.convert_df_mc()
#     # df_data, df_info = pd.DataFrame(df_data), pd.DataFrame(df_info)
#
#
#     df_data = pd.read_csv('df_data.csv', index_col=False, low_memory=False)
#     df_info = pd.read_csv('df_info.csv', index_col=False)
#
#
#     lst_linear = [
#         'CS_rec_a_03',
#         'CS_rec_a_04',
#         'CS_rec_a_05',
#         'CS_rec_a_06',
#         # 'CS_rec_a_07',
#         # 'CS_rec_a_08',
#         # 'CS_rec_a_09',
#         # 'CS_rec_a_10',
#         # 'CS_rec_a_11',
#         # 'CS_rec_a_12',
#         # 'CS_rec_a_13',
#         # 'CS_rec_a_14',
#         # 'CS_rec_a_15',
#         # 'CS_rec_a_16',
#         # 'CS_rec_a_17',
#         # 'CS_rec_a_18',
#         # 'CS_rec_a_19',
#         # 'CS_rec_a_20',
#         # 'CS_rec_a_21',
#         # 'CS_rec_b_01',
#         # 'CS_rec_b_02',
#         # 'CS_rec_b_03',
#         # 'CS_rec_b_04',
#         # 'CS_rec_b_05',
#         # 'CS_rec_b_06',
#     ]
#
#     dict_define_linear = {
#         'L1': {
#             'str_query': '',
#             'dependent_vars': lst_linear[:1],
#             'explanatory_vars': lst_linear[1:]},
#         'L2': {
#             'str_query': '',
#             'dependent_vars': lst_linear[:2],
#             'explanatory_vars': lst_linear[2:],
#         },
#     }
#
#     df_data[lst_linear] = df_data[lst_linear].fillna(0)
#
#     alz = DataAnalysis(df_data=df_data, df_info=df_info)
#
#     # alz.linear_regression(dict_define_linear=dict_define_linear, output_name='lnr testing.xlsx')
#
#
#     alz.correlation(dict_define_corr=dict_define_linear, output_name='lnr testing.xlsx')
#
#
#
#     exit()
#
#
#
#
#     # df_data.loc[:, 'S1'] = 999
#     # df_data.loc[[11, 13, 17, 19, 23], 'S2'] = 888
#     # df_info.loc[df_info.eval("var_name == 'S1'"), ['val_lbl']] = [{'net_code': {'9000001|net|AAAA': {'1': 'Male', '2': 'Female'}}}]
#
#     # dp = DataProcessing(df_data=df_data, df_info=df_info)
#     # dp.count_ma_choice(lst_ma_qre=['A1', 'A2', 'A3'], dict_replace={0: np.nan})
#     # df_data, df_info = dp.calculate_ranking_score(lst_ranking_qre=['A8_Important_ranking'])
#
#
#     # # CHECK POPULATE
#     # # SA
#     # df_data.loc[[0, 3, 5, 7], 'S8'] = np.nan
#     # a0 = eval(df_info.loc[df_info.eval("var_name == 'S8'"), 'val_lbl'].values[0])
#     # df_a = pd.DataFrame(columns=['code', 'label'], data=[['-1', 'Base']] + [[k, v] for k, v in a0.items()])
#     #
#     # a1 = df_data['S8'].value_counts()
#     # a1[-1] = df_data['S8'].count()
#     # a1 = a1.sort_index()
#     #
#     # a1 = pd.DataFrame(columns=['count'], data=a1)
#     # a1['code'] = a1.index.astype(int).astype(str)
#     # df_a = df_a.merge(a1, how='left', on='code')
#     # df_a.to_csv('df_a.csv')
#     # # MA
#     # a2 = df_data[[
#     #     'A1_1',
#     #     'A1_2',
#     #     'A1_3',
#     #     'A1_4',
#     #     'A1_5',
#     #     'A1_6',
#     #     'A1_7',
#     #     'A1_8',
#     #     'A1_9',
#     #     'A1_10',
#     #     'A1_11',
#     #     'A1_12',
#     # ]].melt().dropna()
#     #
#     # a2_count = a2['value'].value_counts().sort_index()
#
#
#     # arr = np.array([
#     #     [11, 12, 13, 14, 15],
#     #     [21, 22, 23, 24, 25],
#     #     [31, 32, 33, 34, 35],
#     #     [41, 42, 43, 44, 45],
#     #     [51, 52, 53, 54, 55],
#     #     [61, 62, 63, 64, 65],
#     #     [71, 72, 73, 74, 75],
#     # ])
#     #
#     # arr2 = arr.transpose()
#
#
#
#
#     dict_header = {
#         'lst_0': [
#             [
#                 {
#                     "qre_name": "S2",
#                     "qre_lbl": "City",
#                     "cats": {
#                         "-1": 'Total',
#                         "1": "Hanoi",
#                         "2": "HCMC",
#                     }
#                 },
#                 {
#                     "qre_name": "S1",
#                     "qre_lbl": "Gender",
#                     "cats": {}
#                 },
#                 {
#                     "qre_name": "S4",
#                     "qre_lbl": "Age",
#                     "cats": {
#                         "2": "22 - 29",
#                         "3": "30 - 39",
#                         "4": "40 - 45",
#                     }
#                 },
#                 {
#                     "qre_name": "S8",
#                     "qre_lbl": "MII",
#                     "cats": {}
#                 },
#             ],
#             [
#                 {
#                     "qre_name": "@Resp",
#                     "qre_lbl": "Resp",
#                     "cats": {
#                         "(Resp == 1 | Resp == 2)": "User",
#                         "(Resp == 1)": "Ever used",
#                         "(Resp == 2)": "Using",
#                         "(Resp == 3)": "Intender",
#                     }
#                 },
#
#                 {
#                     "qre_name": "$A3",
#                     "qre_lbl": "What financial product channels are you currently investing in?",
#                     "cats": {
#                         '1': 'Saving',
#                         '2': 'Crypto',
#                         '3': 'Stock',
#                         '4': 'Bonds',
#                         '5': 'Gold',
#                     }
#                 },
#
#             ],
#         ],
#
#         # Group header 1st
#         # 'lst_1': [
#         #     [
#         #         {
#         #             "qre_name": "S2",
#         #             "qre_lbl": "City",
#         #             "cats": {
#         #                 "-1": 'Total',
#         #                 "1": "Hanoi",
#         #                 "2": "HCMC",
#         #             }
#         #         },
#         #         {
#         #             "qre_name": "S1",
#         #             "qre_lbl": "Gender",
#         #             "cats": {}
#         #         },
#         #         {
#         #             "qre_name": "S4",
#         #             "qre_lbl": "Age",
#         #             "cats": {
#         #                 "2": "22 - 29",
#         #                 "3": "30 - 39",
#         #                 "4": "40 - 45",
#         #             }
#         #         },
#         #     ],
#         #     [
#         #         {
#         #             "qre_name": "@Resp",
#         #             "qre_lbl": "Resp",
#         #             "cats": {
#         #                 "(Resp == 1 | Resp == 2)": "User",
#         #                 "(Resp == 1)": "Ever used",
#         #                 "(Resp == 2)": "Using",
#         #                 "(Resp == 3)": "Intender",
#         #             }
#         #         },
#         #         {
#         #             "qre_name": "S8",
#         #             "qre_lbl": "MII",
#         #             "cats": {}
#         #         },
#         #     ],
#         #     [
#         #         {
#         #             "qre_name": "@S8_2",
#         #             "qre_lbl": "MII _ 2",
#         #             "cats": {
#         #                 'S8.isin([1,2,3])': '< 20tr',
#         #                 'S8.isin([4,5])': '20 - 39',
#         #                 'S8.isin([6,7])': '> 40',
#         #             }
#         #         },
#         #         {
#         #             "qre_name": "$A3",
#         #             "qre_lbl": "What financial product channels are you currently investing in?",
#         #             "cats": {
#         #                 '1': 'Saving',
#         #                 '2': 'Crypto',
#         #                 '3': 'Stock',
#         #                 '4': 'Bonds',
#         #                 '5': 'Gold',
#         #                 '6': 'Real estate',
#         #                 '7': 'Mutual funds',
#         #                 '8': 'ETF',
#         #                 '9': 'Foreign exchange (Forex)',
#         #                 '10': 'Derivatives',
#         #                 '11': 'Others, please specify',
#         #                 '12': 'I have not invested in any product before',
#         #                 '13': 'I have not invested in any product in the past 3 years',
#         #                 '14': 'I’m not investing in finance'
#         #             }
#         #         },
#         #     ],
#         # ],
#
#         # # Group header 2nd
#         # 'lst_2': [
#         #     [
#         #         {
#         #             "qre_name": "S2",
#         #             "qre_lbl": "City",
#         #             "cats": {
#         #                 "-1": 'Total',
#         #                 "1": "Hanoi",
#         #                 "2": "HCMC",
#         #             }
#         #         },
#         #
#         #     ],
#         #     [
#         #         {
#         #             "qre_name": "S4",
#         #             "qre_lbl": "Age",
#         #             "cats": {
#         #                 "2": "22 - 29",
#         #                 "3": "30 - 39",
#         #                 "4": "40 - 45",
#         #             }
#         #         },
#         #
#         #
#         #     ],
#         #     [
#         #         {
#         #             "qre_name": "S1",
#         #             "qre_lbl": "Gender",
#         #             "cats": {}
#         #         },
#         #         {
#         #             "qre_name": "@S8_2",
#         #             "qre_lbl": "MII _ 2",
#         #             "cats": {
#         #                 'S8.isin([1,2,3])': '< 20tr',
#         #                 'S8.isin([4,5])': '20 - 39',
#         #                 'S8.isin([6,7])': '> 40',
#         #             }
#         #         },
#         #     ]
#         # ],
#
#
#     }
#
#     lst_side = [
#         {'name': 'S1'},
#         {'name': '$A1', 'label': 'A1 (MA). Label', 'cats': {
#
#             '900001|net|Group1': {
#
#                 '9000011|net|Group1.1': {
#                     '1': 'Saving',
#                     '2': 'Stock',
#
#
#                     '90000111|net|Group1.1.1': {
#                         '3': 'Bonds',
#                         '4': 'Gold',
#                     },
#
#                 },
#
#                 '9000012|net|Group1.2': {
#                     '5': 'Real estate',
#                     '6': 'Mutual funds',
#                 },
#
#                 '7': 'ETF',
#
#             },
#             '900002|combine|Group2': {
#                 '8': 'Foreign exchange (Forex)',
#                 '9': 'Derivatives',
#                 '10': 'Crypto',
#             },
#
#             '11': 'I have not invested in any product before',
#             '12': 'Others, please specify'
#
#         }},
#
#         {
#             'name': 'CS4_a_10',
#             'label': '{lbl} - aaaaa 10000',
#             'cats': {
#                 '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             },
#             'mean_factor': {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
#         },
#
#         {
#             'name': 'CS4_a_20',
#             'label': '{lbl} - aaaaa',
#             'cats': {
#                 '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#
#             },
#             'mean_factor': {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
#         },
#
#         {
#             'name': 'CS_rec_a_02',
#             'cats': {
#                 '1': '0 - Definitely will not recommend', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7',
#                 '9': '8', '10': '9', '11': '10- Definitely will recommend',
#                 '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                 '900002|combine|Passives': {'8': '7', '9': '8'},
#                 '900003|combine|Promoters': {'10': '9', '11': '10'},
#
#             },
#             'mean_factor': {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#             'calculation': {'NPS': 'abs([Promoters] - [Detractors])'},
#         },
#
#
#
#     ]
#
#     grp_tbl_info = {
#         'group_tbl_1': {
#             'data_to_run': {
#                 'is_md': False,
#                 'df_data': df_data,
#                 'df_info': df_info,
#             },
#             'tables_to_run': [
#                 'Table_HN',
#                 'Table_HCM',
#             ],
#             'tables_format': {
#                 'Table_HN': {
#                     'tbl_name': "Table_HN",
#                     'tbl_filter': "S2 == 1",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#                 'Table_HCM': {
#                     'tbl_name': "Table_HCM",
#                     'tbl_filter': "S2 == 2",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#             },
#         },
#
#         'group_tbl_2': {
#             'data_to_run': {
#                 'is_md': False,
#                 'df_data': df_data,
#                 'df_info': df_info,
#             },
#             'tables_to_run': [
#                 # 'Table_HN',
#                 'Table_HCM',
#             ],
#             'tables_format': {
#                 'Table_HN': {
#                     'tbl_name': "Table_HN",
#                     'tbl_filter': "S2 == 1",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#                 'Table_HCM': {
#                     'tbl_name': "Table_HCM",
#                     'tbl_filter': "S2 == 2",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#             },
#         },
#
#
#         'group_tbl_3': {
#             'data_to_run': {
#                 'is_md': False,
#                 'df_data': df_data,
#                 'df_info': df_info,
#             },
#             'tables_to_run': [
#                 'Table_HN',
#                 # 'Table_HCM',
#             ],
#             'tables_format': {
#                 'Table_HN': {
#                     'tbl_name': "Table_HN",
#                     'tbl_filter': "S2 == 1",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#                 'Table_HCM': {
#                     'tbl_name': "Table_HCM",
#                     'tbl_filter': "S2 == 2",
#                     'tbl_cell_content': ['c', 'p', '%'],
#                     'tbl_header': dict_header,
#                     'tbl_side': lst_side,
#                     'sig_test': {'type': 'non', 'lvl': [], 'cols': []},
#                     'is_hide_zero_cats': False,
#                     'is_hide_zero_cols': False,
#                     'weight_var': '',
#                 },
#             },
#         },
#
#
#     }
#
#
#     dtbl = Tabulation(tbl_file_name=str_tbl_file_name, grp_tbl_info=grp_tbl_info)
#     dtbl.tabulate_tables(lst_running_tables_group=['group_tbl_1'])
#
#
#
#
#
#
#
#
#
#     here = 1
#
#
#     exit()
#
#
#
#     # AFTER CONVERTING YOU CAN DO ANYTHING WITH DATAFRAME-------------------------------------------------------------------
#     codelist_cs2_cs3 = {'1': 'Vina Securities Joint Stock Company (VNSC)', '2': 'VNSC by Finhay', '3': 'VPS Securities Company (VPS)', '4': 'VNDIRECT Securities Corporation', '5': 'SSI Securities Corporation (SSI)', '6': 'Hồ Chí Minh Securities Corporation (HSC)', '7': 'BIDV Securities Company (BSC)', '8': 'Vietcap Securities Company (VCSC)', '9': 'Mirae Asset Securities Vietnam', '10': 'Techcom Securities (TCBS)', '11': 'Vietcombank Securities (VCBS)', '12': 'MB Securities (MBS)', '13': 'PINE TREE', '14': 'Đại Nam Securities (DNSE)', '15': 'KB Securities', '16': 'Prudential', '17': 'Manulife', '18': 'Dai-ichi Life', '19': 'Generali', '20': 'Others, please clarify', '21': 'I do not know any securities brand/ company', '22': 'I do not invest in stock market now'}
#
#     st_add_qre = time.time()
#
#     dict_add_new_qres = {
#         'Resp': ['Resp', 'SA', {'1': 'Ever used', '2': 'Using', '3': 'Intender'}, np.nan],
#         'A4': ['What method do you use to invest in stocks?', 'SA', {'1': 'Self-investment', '2': 'Through a stockbroker'}, np.nan],
#
#         'CS1|21': ['The securities brokerage brands/companies that you have used for investment up to now. Multiple answers are possible', 'MA', {'1': 'Vina Securities Joint Stock Company (VNSC)', '2': 'VNSC by Finhay', '3': 'VPS Securities Company (VPS)', '4': 'VNDIRECT Securities Corporation', '5': 'SSI Securities Corporation (SSI)', '6': 'Hồ Chí Minh Securities Corporation (HSC)', '7': 'BIDV Securities Company (BSC)', '8': 'Vietcap Securities Company (VCSC)', '9': 'Mirae Asset Securities Vietnam', '10': 'Techcom Securities (TCBS)', '11': 'Vietcombank Securities (VCBS)', '12': 'MB Securities (MBS)', '13': 'PINE TREE', '14': 'Đại Nam Securities (DNSE)', '15': 'KB Securities', '16': 'Prudential', '17': 'Manulife', '18': 'Dai-ichi Life', '19': 'Generali', '20': 'Others, please clarify', '21': 'I do not know any securities brand/ company'}, np.nan],
#         'CS2|22': ['The financial/investment brands/companies you are currently using. Multiple answers are possible.', 'MA', codelist_cs2_cs3, np.nan],
#
#         'CS3_01|22': ['Which securities brokerage firms are you investing in these products with? Multiple answers are possible_Stock', 'MA', codelist_cs2_cs3, np.nan],
#         'CS3_02|22': ['Which securities brokerage firms are you investing in these products with? Multiple answers are possible_Bonds', 'MA', codelist_cs2_cs3, np.nan],
#         'CS3_03|22': ['Which securities brokerage firms are you investing in these products with? Multiple answers are possible_Mutual funds', 'MA', codelist_cs2_cs3, np.nan],
#         'CS3_04|22': ['Which securities brokerage firms are you investing in these products with? Multiple answers are possible_ETF', 'MA', codelist_cs2_cs3, np.nan],
#         'CS3_05|22': ['Which securities brokerage firms are you investing in these products with? Multiple answers are possible_Derivatives', 'MA', codelist_cs2_cs3, np.nan],
#
#         'CS_motive_01|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Vina Securities Joint Stock Company (VNSC)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_02|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_VNSC by Finhay', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_03|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_VPS Securities Company (VPS)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_04|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_VNDIRECT Securities Corporation', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_05|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_SSI Securities Corporation (SSI)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_06|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Hồ Chí Minh Securities Corporation (HSC)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_07|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_BIDV Securities Company (BSC)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_08|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Vietcap Securities Company (VCSC)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_09|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Mirae Asset Securities Vietnam', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_10|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Techcom Securities (TCBS)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_11|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Vietcombank Securities (VCBS)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_12|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_MB Securities (MBS)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_13|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_PINE TREE', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_14|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Đại Nam Securities (DNSE)', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_15|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_KB Securities', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_16|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Prudential', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_17|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Manulife', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_18|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Dai-ichi Life', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_19|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Generali', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#         'CS_motive_20|24': ['The motivations driving you to use these securities brokerage brands/companies for investment:_Others, please clarify', 'MA', {'1': 'Allows investing with small capital', '2': 'Application with intuitive/clean interface and user-friendly design', '3': 'Easy-to-use application, doesn’t require much time to learn', '4': 'Diverse investment products (stocks, mutual funds, gold, etc.)', '5': 'Saves transaction time', '6': 'Provides timely and continuous market updates', '7': 'Transparent and clear transaction information', '8': 'Managed by reputable organizations in the market', '9': 'Good brand reputation, widely used by many people', '10': 'Ability to place/match orders quickly', '11': 'High stability, smooth experience', '12': 'Low transaction fees', '13': 'Safe and secure personal information', '14': 'Applying many smart features helps make investing convenient', '15': 'Modern technical charts and comprehensive advanced features', '16': 'Provides in-depth analysis to support investment decisions', '17': 'Dedicated customer service staff', '18': 'Regularly improve, update utilities and new features', '19': 'Recommendations from friends and family', '20': 'Simple, fast account opening procedures', '21': 'Many free knowledge training programs', '22': 'Phí giao dịch cao', '23': 'Ứng dụng khó sử dụng', '24': 'Others, please clarify'}, np.nan],
#
#         'CS_abandon_01|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Vina Securities Joint Stock Company (VNSC)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_02|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._VNSC by Finhay', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_03|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._VPS Securities Company (VPS)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_04|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._VNDIRECT Securities Corporation', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_05|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._SSI Securities Corporation (SSI)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_06|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Hồ Chí Minh Securities Corporation (HSC)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_07|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._BIDV Securities Company (BSC)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_08|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Vietcap Securities Company (VCSC)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_09|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Mirae Asset Securities Vietnam', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_10|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Techcom Securities (TCBS)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_11|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Vietcombank Securities (VCBS)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_12|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._MB Securities (MBS)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_13|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._PINE TREE', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_14|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Đại Nam Securities (DNSE)', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_15|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._KB Securities', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_16|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Prudential', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_17|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Manulife', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_18|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Dai-ichi Life', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_19|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Generali', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#         'CS_abandon_20|16': ['Why did you use to invest in the  brand that you no longer use? Multiple answers are possible._Others, please clarify', 'MA', {'1': 'High transaction fees', '2': 'Difficult-to-use interface', '3': 'Limited investment options', '4': 'Lack of trust in security measures', '5': 'Slow and incomplete market information updates', '6': 'Slow transaction process', '7': 'Unclear and non-transparent transaction information', '8': 'Lack of trust in management organizations', '9': 'Low stability', '10': 'Inadequate transaction information from exchanges and investment channels', '11': 'Limited in-depth analysis to support investment', '12': 'Unrealistic profit commitment', '13': 'Inefficient and indifferent issue resolution support', '14': 'Reducing the number of platforms/apps used for easier asset management', '15': 'Few features/utilities for convenient investment', '16': 'Other, please specify'}, np.nan],
#
#         'CS4_01': ['Please rate your satisfaction level with the brands you are currently using._Vina Securities Joint Stock Company (VNSC)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_02': ['Please rate your satisfaction level with the brands you are currently using._VNSC by Finhay', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_03': ['Please rate your satisfaction level with the brands you are currently using._VPS Securities Company (VPS)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_04': ['Please rate your satisfaction level with the brands you are currently using._VNDIRECT Securities Corporation', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_05': ['Please rate your satisfaction level with the brands you are currently using._SSI Securities Corporation (SSI)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_06': ['Please rate your satisfaction level with the brands you are currently using._Hồ Chí Minh Securities Corporation (HSC)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_07': ['Please rate your satisfaction level with the brands you are currently using._BIDV Securities Company (BSC)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_08': ['Please rate your satisfaction level with the brands you are currently using._Vietcap Securities Company (VCSC)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_09': ['Please rate your satisfaction level with the brands you are currently using._Mirae Asset Securities Vietnam', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_10': ['Please rate your satisfaction level with the brands you are currently using._Techcom Securities (TCBS)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_11': ['Please rate your satisfaction level with the brands you are currently using._Vietcombank Securities (VCBS)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_12': ['Please rate your satisfaction level with the brands you are currently using._MB Securities (MBS)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_13': ['Please rate your satisfaction level with the brands you are currently using._PINE TREE', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_14': ['Please rate your satisfaction level with the brands you are currently using._Đại Nam Securities (DNSE)', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_15': ['Please rate your satisfaction level with the brands you are currently using._KB Securities', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_16': ['Please rate your satisfaction level with the brands you are currently using._Prudential', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_17': ['Please rate your satisfaction level with the brands you are currently using._Manulife', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_18': ['Please rate your satisfaction level with the brands you are currently using._Dai-ichi Life', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_19': ['Please rate your satisfaction level with the brands you are currently using._Generali', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#         'CS4_20': ['Please rate your satisfaction level with the brands you are currently using._Others, please clarify', 'SA', {'1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied'}, np.nan],
#
#         'CS_rec_01': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Vina Securities Joint Stock Company (VNSC)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_02': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_VNSC by Finhay', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_03': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_VPS Securities Company (VPS)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_04': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_VNDIRECT Securities Corporation', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_05': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_SSI Securities Corporation (SSI)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_06': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Hồ Chí Minh Securities Corporation (HSC)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_07': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_BIDV Securities Company (BSC)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_08': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Vietcap Securities Company (VCSC)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_09': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Mirae Asset Securities Vietnam', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_10': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Techcom Securities (TCBS)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_11': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Vietcombank Securities (VCBS)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_12': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_MB Securities (MBS)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_13': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_PINE TREE', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_14': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Đại Nam Securities (DNSE)', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_15': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_KB Securities', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_16': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Prudential', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_17': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Manulife', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_18': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Dai-ichi Life', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_19': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Generali', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#         'CS_rec_20': ['Please select the willingness level to recommend this securities brokerage brand/company to friends and family based on the scoring from 0->10, with 0 is definitely will not recommend and 10 is definitely will recommend_Others, please clarify', 'SA', {'1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend'}, np.nan],
#
#         'ADD_ab': ['Which securities brokerage brand/company are you considering/ most desiring to use for stock investment?', 'SA', {'1': 'Vina Securities Joint Stock Company (VNSC)', '2': 'VNSC by Finhay', '3': 'VPS Securities Company (VPS)', '4': 'VNDIRECT Securities Corporation', '5': 'SSI Securities Corporation (SSI)', '6': 'Hồ Chí Minh Securities Corporation (HSC)', '7': 'BIDV Securities Company (BSC)', '8': 'Vietcap Securities Company (VCSC)', '9': 'Mirae Asset Securities Vietnam', '10': 'Techcom Securities (TCBS)', '11': 'Vietcombank Securities (VCBS)', '12': 'MB Securities (MBS)', '13': 'PINE TREE', '14': 'Đại Nam Securities (DNSE)', '15': 'KB Securities', '16': 'Prudential', '17': 'Manulife', '18': 'Dai-ichi Life', '19': 'Generali', '20': 'Others, please clarify', '21': 'I do not know any securities brand/ company', '22': 'I do not have an intention to change'}, np.nan],
#
#         'Weighting': ['Weighting', 'NUM', {}, 2.9],
#     }
#
#
#     dp = DataProcessing(df_data=df_data, df_info=df_info)
#     dp.add_qres(dict_add_new_qres)
#
#     # Weighting
#     dp.df_data.loc[dp.df_data.eval("S1 == 2"), ['Weighting']] = [3.3]
#
#     # Resp
#     dp.df_data.loc[dp.df_data.eval("((A2_1 == 2 | A2_2 == 2) & (A3_1 != 3 & A3_2 != 3 & A3_3 != 3))"), 'Resp'] = 1
#     dp.df_data.loc[dp.df_data.eval("A3_1 == 3 | A3_2 == 3 | A3_3 == 3"), 'Resp'] = 2
#     dp.df_data.loc[dp.df_data.eval("((A3_intend_1 == 2 | A3_intend_2 == 2) & (A7 == 1))"), 'Resp'] = 3
#
#     # A4
#     dp.df_data.loc[dp.df_data.eval("A4_user == 1 | A4_intender == 1"), 'A4'] = 1
#     dp.df_data.loc[dp.df_data.eval("A4_user == 2 | A4_intender == 2"), 'A4'] = 2
#
#     dp.merge_qres(
#         lst_merge=[f'CS1_{i}' for i in range(1, 22)],
#         lst_to_merge=[f'CS1_a_{i}' for i in range(1, 22)] + [f'CS1_b_{i}' for i in range(1, 22)],
#         dk_code=21
#     )
#
#     dp.merge_qres(
#         lst_merge=[f'CS2_{i}' for i in range(1, 23)],
#         lst_to_merge=[f'CS2_a_{i}' for i in range(1, 23)] + [f'CS2_b_{i}' for i in range(1, 23)],
#         dk_code=22
#     )
#
#
#     for att in range(1, 6):
#         dp.merge_qres(
#             lst_merge=[f'CS3_0{att}_{i}' for i in range(1, 23)],
#             lst_to_merge=[f'CS3_a_0{att}_{i}' for i in range(1, 23)] + [f'CS3_b_0{att}_{i}' for i in range(1, 23)],
#             dk_code=22
#         )
#
#
#     for att in range(1, 21):
#         att = f'0{att}' if att < 10 else att
#
#         dp.merge_qres(
#             lst_merge=[f'CS_motive_{att}_{i}' for i in range(1, 25)],
#             lst_to_merge=[f'CS_motive_a_{att}_{i}' for i in range(1, 25)] + [f'CS_motive_b_{att}_{i}' for i in range(1, 25)],
#             dk_code=999
#         )
#
#         dp.merge_qres(
#             lst_merge=[f'CS_abandon_{att}_{i}' for i in range(1, 17)],
#             lst_to_merge=[f'CS_abandon_a_{att}_{i}' for i in range(1, 17)] + [f'CS_abandon_b_{att}_{i}' for i in range(1, 17)],
#             dk_code=999
#         )
#
#         dp.df_data[f'CS4_{att}'] = dp.df_data[[f'CS4_a_{att}', f'CS4_b_{att}']].sum(axis=1, numeric_only=True, min_count=1)
#         dp.df_data[f'CS_rec_{att}'] = dp.df_data[[f'CS_rec_a_{att}', f'CS_rec_b_{att}']].sum(axis=1, numeric_only=True, min_count=1)
#
#
#
#
#     dp.df_data[f'ADD_ab'] = dp.df_data[[f'ADD_a', f'ADD_b']].sum(axis=1, numeric_only=True, min_count=1)
#
#     # str_path = f'{str_file_name.rsplit('/', 1)[-1]}_preview - original.xlsx'
#     # dp.df_data, dp.df_info = pd.read_excel(str_path, sheet_name='df_data', index_col=0), pd.read_excel(str_path, sheet_name='df_info', index_col=0)
#     # for idx in dp.df_info.index:
#     #     dp.df_info.at[idx, 'val_lbl'] = eval(dp.df_info.at[idx, 'val_lbl'])
#
#
#     # query_fil:  điều kiện filter df_data để update
#     # qre_name: câu hỏi cần update, nếu là câu MA thì input 'tên câu hỏi|số column'
#     # lst_val_update: list giá trị cần update.
#     # method: có 3 dạng gồm:
#     #   - o (overlay): update giá trị mới lên toàn bộ giá trị cũ. Độ dài của 'lst_val_update' PHẢI bằng với độ dài của câu cần update.
#     #   - a (append): insert thêm giá trị mới vào câu cần update.
#     #   - r (remove): xóa giá trị trong 'lst_val_update' của câu cần update
#
#     dp.update_qres_data(query_fil="S4 == 2", qre_name='A1|12', lst_val_update=[4, 5] + [np.nan] * 10, method='o')
#     dp.update_qres_data(query_fil="S4 == 3", qre_name='A1|12', lst_val_update=[10, 11], method='a')
#     dp.update_qres_data(query_fil="S4 == 4", qre_name='A1|12', lst_val_update=[2, 3], method='r')
#
#     df_data = pd.DataFrame(dp.df_data)
#     df_info = pd.DataFrame(dp.df_info)
#
#
#
#
#
#     # Just for checking
#     with pd.ExcelWriter(f'{str_file_name.rsplit('/', 1)[-1]}_preview.xlsx', engine="openpyxl") as writer:
#         df_data.to_excel(writer, sheet_name='df_data')
#         df_info.to_excel(writer, sheet_name='df_info')
#
#
#
#     # # ----------------------------------------------------------------------------------------------------------------------
#     # # OE RUNNING------------------------------------------------------------------------------------------------------------
#     # # ----------------------------------------------------------------------------------------------------------------------
#     # # cfr = CodeframeReader(cf_file_name='Coding/VN8534 - MASTERISE HOME - DANPHUONG - CODEFRAME RECEIVED - Mar 26 - v1.xlsm')
#     # #
#     # # # READ '*.xlsm' file -> CREATE 'output.xlsx' file -> RUN OE
#     # # # cfr.to_dataframe_file()
#     # #
#     # # # READ 'output.xlsx' file create before -> RUN OE
#     # # cfr.read_dataframe_output_file()
#     # #
#     # # df_data, df_info = DataProcessing.add_qres(df_data, df_info, cfr.dict_add_new_qres_oe)
#     # # df_data, df_info = pd.DataFrame(df_data), pd.DataFrame(df_info)
#     # #
#     # # df_coding = pd.DataFrame(cfr.df_full_oe_coding)
#     # #
#     # # # # ['ID', 'Ma_SP'] will be defined base on each project
#     # # # df_coding[['ID', 'Ma_SP']] = df_coding['RESPONDENTID'].str.rsplit('_', n=1, expand=True)
#     # # # df_coding.drop(columns=['RESPONDENTID'], inplace=True)
#     # #
#     # # # df_data_stack['Ma_SP'] = df_data_stack['Ma_SP'].astype(int)
#     # # # df_coding['Ma_SP'] = df_coding['Ma_SP'].astype(int)
#     # #
#     # # lst_oe_col = df_coding.columns.tolist()
#     # # # lst_oe_col.remove('ID')
#     # # # lst_oe_col.remove('Ma_SP')
#     # #
#     # # df_data['RESPONDENTID'] = df_data['ID']
#     # #
#     # # df_data = df_data.merge(df_coding, how='left', on=['RESPONDENTID'])
#     # #
#     # # for i in lst_oe_col:
#     # #     df_data[i].replace({99999: np.nan}, inplace=True)
#     # #
#     # # df_data.drop(columns=['RESPONDENTID'], inplace=True)
#     # #
#     # #
#     # # # Just for checking OE
#     # # with pd.ExcelWriter(f'{str_file_name}_checkOE.xlsx', engine="openpyxl") as writer:
#     # #     df_data.to_excel(writer, sheet_name='df_data')
#     # #     df_info.to_excel(writer, sheet_name='df_info')
#     # #
#     # #
#
#     # dict_dfs = {
#     #     1: {
#     #         'data': df_data,
#     #         'info': df_info,
#     #         'tail_name': 'ByCode',
#     #         'sheet_name': 'ByCode',
#     #         'is_recode_to_lbl': False,
#     #     },
#     # }
#     #
#     # converter.generate_multiple_data_files(dict_dfs=dict_dfs)
#
#
#     dict_header = {
#         # Group header 1st
#         'lst_1': [
#             [
#
#                 {
#                     "qre_name": "S2",
#                     "qre_lbl": "City",
#                     "cats": {
#                         "Total": 'Total',
#                         "1": "Hanoi",
#                         "2": "HCMC",
#                     }
#                 },
#                 # {
#                 #     "qre_name": "S1",
#                 #     "qre_lbl": "Gender",
#                 #     "cats": {}
#                 # },
#                 # {
#                 #     "qre_name": "S4",
#                 #     "qre_lbl": "Age",
#                 #     "cats": {
#                 #         "2": "22 - 29",
#                 #         "3": "30 - 39",
#                 #         "4": "40 - 45",
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "@Resp",
#                 #     "qre_lbl": "Resp",
#                 #     "cats": {
#                 #         "(Resp == 1 | Resp == 2)": "User",
#                 #         "(Resp == 1)": "Ever used",
#                 #         "(Resp == 2)": "Using",
#                 #         "(Resp == 3)": "Intender",
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "A4",
#                 #     "qre_lbl": "A4",
#                 #     "cats": {
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "S8",
#                 #     "qre_lbl": "MII",
#                 #     "cats": {
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "@S8_2",
#                 #     "qre_lbl": "MII _ 2 ",
#                 #     "cats": {
#                 #         'S8.isin([1,2,3])': '< 20tr ',
#                 #         'S8.isin([4,5])': '20 - 39 ',
#                 #         'S8.isin([6,7])': ' > 40 ',
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$A3",
#                 #     "qre_lbl": "What financial product channels are you currently investing in?",
#                 #     "cats": {
#                 #         '1': 'Saving',
#                 #         '2': 'Crypto',
#                 #         '3': 'Stock',
#                 #         '4': 'Bonds',
#                 #         '5': 'Gold',
#                 #         '6': 'Real estate',
#                 #         '7': 'Mutual funds',
#                 #         '8': 'ETF',
#                 #         '9': 'Foreign exchange (Forex)',
#                 #         '10': 'Derivatives',
#                 #         '11': 'Others, please specify',
#                 #         '12': 'I have not invested in any product before',
#                 #         '13': 'I have not invested in any product in the past 3 years',
#                 #         '14': 'I’m not investing in finance'
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$A3_intend",
#                 #     "qre_lbl": "What financial product channels do you intend to invest in the next 6 months",
#                 #     "cats": {
#                 #         '1': 'Saving',
#                 #         '2': 'Stock',
#                 #         '3': 'Bonds',
#                 #         '4': 'Gold',
#                 #         '5': 'Real estate',
#                 #         '6': 'Mutual funds',
#                 #         '7': 'ETF',
#                 #         '8': 'Foreign exchange (Forex)',
#                 #         '9': 'Derivatives',
#                 #         '10': 'Crypto',
#                 #         '11': 'I do not intend to invest in finance',
#                 #         '12': 'Khác (ghi rõ)'
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$BA_aided_stock",
#                 #     "qre_lbl": "Among the options below, which are the securities brokerage firms that you are familiar with, have seen, or heard of",
#                 #     "cats": {
#                 #         '1': 'Vina Securities Joint Stock Company (VNSC)',
#                 #         '2': 'VNSC by Finhay',
#                 #         '3': 'VPS Securities Company (VPS)',
#                 #         '4': 'VNDIRECT Securities Corporation',
#                 #         '5': 'SSI Securities Corporation (SSI)',
#                 #         '6': 'Hồ Chí Minh Securities Corporation (HSC)',
#                 #         '7': 'BIDV Securities Company (BSC)',
#                 #         '8': 'Vietcap Securities Company (VCSC)',
#                 #         '9': 'Mirae Asset Securities Vietnam',
#                 #         '10': 'Techcom Securities (TCBS)',
#                 #         '11': 'Vietcombank Securities (VCBS)',
#                 #         '12': 'MB Securities (MBS)',
#                 #         '13': 'PINE TREE',
#                 #         '14': 'Đại Nam Securities (DNSE)',
#                 #         '15': 'KB Securities',
#                 #         '16': 'Prudential',
#                 #         '17': 'Manulife',
#                 #         '18': 'Dai-ichi Life',
#                 #         '19': 'Generali',
#                 #         '20': 'I do not know any securities brand/ company',
#                 #         '21': 'Others, please clarify'
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$BA_aided1_fintech",
#                 #     "qre_lbl": "Among the following financial technology (fintech) applications, which ones have you ever seen, heard of, or come across?",
#                 #     "cats": {
#                 #         '1': 'Momo',
#                 #         '2': 'ViettelPay',
#                 #         '3': 'ZaloPay',
#                 #         '4': 'VNPAY',
#                 #         '5': 'Money Lover',
#                 #         '6': 'Tikop',
#                 #         '7': 'Cake by VP Bank',
#                 #         '8': 'Finhay',
#                 #         '9': 'I have never seen/known the above brands',
#                 #         '10': 'Others, please clarify'
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "@A6_03",
#                 #     "qre_lbl": "How long have you been investing?_Stock",
#                 #     "cats": {
#                 #         "(A6_03.isin([1,2,3]))": "Dưới 1 năm",
#                 #         "(A6_03 == 4)": "Từ 1 - 3 năm",
#                 #         "(A6_03.isin([5,6]))": "Trên 3 năm"
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$CS1",
#                 #     "qre_lbl": "CS1_Combine",
#                 #     "cats": {
#                 #         '1': 'Vina Securities Joint Stock Company (VNSC)',
#                 #         '2': 'VNSC by Finhay',
#                 #         '3': 'VPS Securities Company (VPS)',
#                 #         '4': 'VNDIRECT Securities Corporation',
#                 #         '5': 'SSI Securities Corporation (SSI)',
#                 #         '6': 'Hồ Chí Minh Securities Corporation (HSC)',
#                 #         '7': 'BIDV Securities Company (BSC)',
#                 #         '8': 'Vietcap Securities Company (VCSC)',
#                 #         '9': 'Mirae Asset Securities Vietnam',
#                 #         '10': 'Techcom Securities (TCBS)',
#                 #         '11': 'Vietcombank Securities (VCBS)',
#                 #         '12': 'MB Securities (MBS)',
#                 #         '13': 'PINE TREE',
#                 #         '14': 'Đại Nam Securities (DNSE)',
#                 #         '15': 'KB Securities',
#                 #         '16': 'Prudential',
#                 #         '17': 'Manulife',
#                 #         '18': 'Dai-ichi Life',
#                 #         '19': 'Generali',
#                 #         '20': 'Others, please clarify',
#                 #         '21': 'I do not know any securities brand/ company'
#                 #     }
#                 # },
#                 # {
#                 #     "qre_name": "$CS2",
#                 #     "qre_lbl": "CS2_Combine",
#                 #     "cats": {
#                 #         '1': 'Vina Securities Joint Stock Company (VNSC)',
#                 #         '2': 'VNSC by Finhay',
#                 #         '3': 'VPS Securities Company (VPS)',
#                 #         '4': 'VNDIRECT Securities Corporation',
#                 #         '5': 'SSI Securities Corporation (SSI)',
#                 #         '6': 'Hồ Chí Minh Securities Corporation (HSC)',
#                 #         '7': 'BIDV Securities Company (BSC)',
#                 #         '8': 'Vietcap Securities Company (VCSC)',
#                 #         '9': 'Mirae Asset Securities Vietnam',
#                 #         '10': 'Techcom Securities (TCBS)',
#                 #         '11': 'Vietcombank Securities (VCBS)',
#                 #         '12': 'MB Securities (MBS)',
#                 #         '13': 'PINE TREE',
#                 #         '14': 'Đại Nam Securities (DNSE)',
#                 #         '15': 'KB Securities',
#                 #         '16': 'Prudential',
#                 #         '17': 'Manulife',
#                 #         '18': 'Dai-ichi Life',
#                 #         '19': 'Generali',
#                 #         '20': 'Others, please clarify',
#                 #         '21': 'I do not know any securities brand/ company',
#                 #         '22': 'I do not invest in stock market now'
#                 #     }
#                 # },
#             ],
#         ],
#
#         # # Group header 2nd
#         # 'lst_2': [
#         #     [
#         #
#         #     ],
#         #
#         # ],
#
#     }
#
#     lst_header_qres_extra = [
#         [
#
#             {
#                 "qre_name": "$CS1",
#                 "qre_lbl": "CS1_Combine",
#                 "cats": {
#                     '1': 'Vina Securities Joint Stock Company (VNSC)',
#                     '2': 'VNSC by Finhay',
#                     '3': 'VPS Securities Company (VPS)',
#                     '4': 'VNDIRECT Securities Corporation',
#                     '5': 'SSI Securities Corporation (SSI)',
#                     '6': 'Hồ Chí Minh Securities Corporation (HSC)',
#                     '7': 'BIDV Securities Company (BSC)',
#                     '8': 'Vietcap Securities Company (VCSC)',
#                     '9': 'Mirae Asset Securities Vietnam',
#                     '10': 'Techcom Securities (TCBS)',
#                     '11': 'Vietcombank Securities (VCBS)',
#                     '12': 'MB Securities (MBS)',
#                     '13': 'PINE TREE',
#                     '14': 'Đại Nam Securities (DNSE)',
#                     '15': 'KB Securities',
#                     '16': 'Prudential',
#                     '17': 'Manulife',
#                     '18': 'Dai-ichi Life',
#                     '19': 'Generali',
#                     '20': 'Others, please clarify',
#                     '21': 'I do not know any securities brand/ company'
#                 }
#             },
#
#
#         ]
#
#     ]
#
#     # SIDE AXIS-------------------------------------------------------------------------------------------------------------
#     lst_side_axis = [
#         # {"qre_name": "S1"},
#         # {"qre_name": "S2"},
#         # {"qre_name": "S3"},
#         # {"qre_name": "S4"},
#         # {"qre_name": "S5"},
#         # {"qre_name": "S6"},
#         # {"qre_name": "$S7"},
#         # {"qre_name": "S8"},
#         # {"qre_name": "S9"},
#         # {"qre_name": "S10"},
#         # {"qre_name": "S11"},
#         {"qre_name": "$A1"},
#         {"qre_name": "$A2"},
#         {"qre_name": "$A3"},
#         {"qre_name": "$A3_intend"},
#         # {"qre_name": "A4_user"},
#         # {"qre_name": "A4_intender"},
#         # {"qre_name": "A6_01"},
#         # {"qre_name": "A6_02"},
#         # {"qre_name": "A6_03"},
#         # {"qre_name": "A6_04"},
#         # {"qre_name": "A6_05"},
#         # {"qre_name": "A6_06"},
#         # {"qre_name": "A6_07"},
#         # {"qre_name": "A6_08"},
#         # {"qre_name": "A6_09"},
#         # {"qre_name": "A6_10"},
#         # {"qre_name": "A6_11"},
#         # {"qre_name": "A6_12"},
#         # {"qre_name": "A6_13"},
#         # {"qre_name": "A7"},
#         # {"qre_name": "$BA_aided_stock"},
#         # {"qre_name": "$BA_Channel_01"},
#         # {"qre_name": "$BA_Channel_02"},
#         # {"qre_name": "$BA_Channel_03"},
#         # {"qre_name": "$BA_Channel_04"},
#         # {"qre_name": "$BA_Channel_05"},
#         # {"qre_name": "$BA_Channel_06"},
#         # {"qre_name": "$BA_Channel_07"},
#         # {"qre_name": "$BA_Channel_08"},
#         # {"qre_name": "$BA_Channel_09"},
#         # {"qre_name": "$BA_Channel_10"},
#         # {"qre_name": "$BA_Channel_11"},
#         # {"qre_name": "$BA_Channel_12"},
#         # {"qre_name": "$BA_Channel_13"},
#         # {"qre_name": "$BA_Channel_14"},
#         # {"qre_name": "$BA_Channel_15"},
#         # {"qre_name": "$BA_Channel_16"},
#         # {"qre_name": "$BA_Channel_17"},
#         # {"qre_name": "$BA_Channel_18"},
#         # {"qre_name": "$BA_Channel_19"},
#         # {"qre_name": "$BA_Channel_20"},
#         # {"qre_name": "$BA_Channel_21"},
#         # {"qre_name": "$BP1_01"},
#         # {"qre_name": "$BP1_02"},
#         # {"qre_name": "$BP1_03"},
#         # {"qre_name": "$BP1_04"},
#         # {"qre_name": "$BP1_05"},
#         # {"qre_name": "$BP1_06"},
#         # {"qre_name": "$BP1_07"},
#         # {"qre_name": "$BP1_08"},
#         # {"qre_name": "$BP1_09"},
#         # {"qre_name": "$BP1_10"},
#         # {"qre_name": "$BP1_11"},
#         # {"qre_name": "$BP1_12"},
#         # {"qre_name": "$BP1_13"},
#         # {"qre_name": "$BP1_14"},
#         # {"qre_name": "$BP1_15"},
#         # {"qre_name": "$BP1_16"},
#         # {"qre_name": "$BP1_17"},
#         # {"qre_name": "$BP1_18"},
#         # {"qre_name": "$BP1_19"},
#         # {"qre_name": "$BP1_20"},
#         # {"qre_name": "$BP1_21"},
#         # {"qre_name": "$BP1_22"},
#         # {"qre_name": "$CS1"},
#         # {"qre_name": "$CS2"},
#         # {"qre_name": "$CS3_01"},
#         # {"qre_name": "$CS3_02"},
#         # {"qre_name": "$CS3_03"},
#         # {"qre_name": "$CS3_04"},
#         # {"qre_name": "$CS3_05"},
#         # {"qre_name": "$CS_motive_01"},
#         # {"qre_name": "$CS_motive_02"},
#         # {"qre_name": "$CS_motive_03"},
#         # {"qre_name": "$CS_motive_04"},
#         # {"qre_name": "$CS_motive_05"},
#         # {"qre_name": "$CS_motive_06"},
#         # {"qre_name": "$CS_motive_07"},
#         # {"qre_name": "$CS_motive_08"},
#         # {"qre_name": "$CS_motive_09"},
#         # {"qre_name": "$CS_motive_10"},
#         # {"qre_name": "$CS_motive_11"},
#         # {"qre_name": "$CS_motive_12"},
#         # {"qre_name": "$CS_motive_13"},
#         # {"qre_name": "$CS_motive_14"},
#         # {"qre_name": "$CS_motive_15"},
#         # {"qre_name": "$CS_motive_16"},
#         # {"qre_name": "$CS_motive_17"},
#         # {"qre_name": "$CS_motive_18"},
#         # {"qre_name": "$CS_motive_19"},
#         # {"qre_name": "$CS_motive_20"},
#         # {"qre_name": "$CS_abandon_01"},
#         # {"qre_name": "$CS_abandon_02"},
#         # {"qre_name": "$CS_abandon_03"},
#         # {"qre_name": "$CS_abandon_04"},
#         # {"qre_name": "$CS_abandon_05"},
#         # {"qre_name": "$CS_abandon_06"},
#         # {"qre_name": "$CS_abandon_07"},
#         # {"qre_name": "$CS_abandon_08"},
#         # {"qre_name": "$CS_abandon_09"},
#         # {"qre_name": "$CS_abandon_10"},
#         # {"qre_name": "$CS_abandon_11"},
#         # {"qre_name": "$CS_abandon_12"},
#         # {"qre_name": "$CS_abandon_13"},
#         # {"qre_name": "$CS_abandon_14"},
#         # {"qre_name": "$CS_abandon_15"},
#         # {"qre_name": "$CS_abandon_16"},
#         # {"qre_name": "$CS_abandon_17"},
#         # {"qre_name": "$CS_abandon_18"},
#         # {"qre_name": "$CS_abandon_19"},
#         # {"qre_name": "$CS_abandon_20"},
#         #
#         # {"qre_name": "CS4_01", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_02", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_03", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_04", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_05", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_06", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_07", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_08", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_09", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_10", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_11", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_12", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_13", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_14", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_15", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_16", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_17", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_18", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "CS4_19", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         #
#         # {"qre_name": "CS4_20", "cats": {
#         #     '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         #
#         # {
#         #     "qre_name": "CS_rec_01",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_02",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_03",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_04",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_05",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_06",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_07",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_08",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_09",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_10",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_11",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_12",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_13",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_14",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_15",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_16",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_17",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_18",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_19",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {
#         #     "qre_name": "CS_rec_20",
#         #     "cats": {
#         #         '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
#         #         '9': 8, '10': 9, '11': '10- Definitely will recommend',
#         #         'net_code': {
#         #             '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         #             '900002|combine|Passives': {'8': '7', '9': '8'},
#         #             '900003|combine|Promoters': {'10': '9', '11': '10'},
#         #         }
#         #     }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},
#         #     "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         # },
#         #
#         # {"qre_name": "$CS_rec1_VNSC"},
#         # {"qre_name": "$CS_rec1_Finhay"},
#         # {"qre_name": "$CS_rec1_VPS"},
#         # {"qre_name": "$CS_rec1_VNDIRECT"},
#         # {"qre_name": "$CS_rec1_SSI"},
#         # {"qre_name": "$CS_rec1_HSC"},
#         # {"qre_name": "$CS_rec1_BSC"},
#         # {"qre_name": "$CS_rec1_VCSC"},
#         # {"qre_name": "$CS_rec1_MAS"},
#         # {"qre_name": "$CS_rec1_TCBS"},
#         # {"qre_name": "$CS_rec1_VCBS"},
#         # {"qre_name": "$CS_rec1_MBS"},
#         # {"qre_name": "$CS_rec1_Pinetree"},
#         # {"qre_name": "$CS_rec1_DNSE"},
#         # {"qre_name": "$CS_rec1_KB"},
#         # {"qre_name": "$CS_rec2_VNSC"},
#         # {"qre_name": "$CS_rec2_Finhay"},
#         # {"qre_name": "$CS_rec2_VPS"},
#         # {"qre_name": "$CS_rec2_VNDIRECT"},
#         # {"qre_name": "$CS_rec2_SSI"},
#         # {"qre_name": "$CS_rec2_HSC"},
#         # {"qre_name": "$CS_rec2_BSC"},
#         # {"qre_name": "$CS_rec2_VCSC"},
#         # {"qre_name": "$CS_rec2_MAS"},
#         # {"qre_name": "$CS_rec2_TCBS"},
#         # {"qre_name": "$CS_rec2_VCBS"},
#         # {"qre_name": "$CS_rec2_MBS"},
#         # {"qre_name": "$CS_rec2_Pinetree"},
#         # {"qre_name": "$CS_rec2_DNSE"},
#         # {"qre_name": "$CS_rec2_KB"},
#         # {"qre_name": "$A8_Important"},
#         # {"qre_name": "A8_Important_ranking_Rank1"},
#         # {"qre_name": "A8_Important_ranking_Rank2"},
#         # {"qre_name": "A8_Important_ranking_Rank3"},
#         # {"qre_name": "A8_Important_ranking_Rank4"},
#         # {"qre_name": "A8_Important_ranking_Rank5"},
#         # {"qre_name": "ADD_ab"},
#         # {"qre_name": "$A9_Influence"},
#         # {"qre_name": "A10_Most_influence"},
#         # {"qre_name": "$BA_aided1_fintech"},
#         # {"qre_name": "$BA_aided2_fintech"},
#         # {"qre_name": "$D2a"},
#         #
#         # {"qre_name": "D2", "cats": {
#         #     '1': 'Very positive', '2': 'Positive', '3': 'No change', '4': 'Negative', '5': 'Very negative',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         #
#         # {"qre_name": "$BI_Change"},
#         # {"qre_name": "$BI_Change1"},
#         # {"qre_name": "CS_intention", "cats": {
#         #     '1': 'Will definitely consider using it', '2': 'Might consider using it', '3': 'I’m not sure', '4': 'Probably wouldn’t consider using it', '5': 'Will definitely not consider using it',
#         #     'net_code': {
#         #         '900001|combine|T2B': {'1': '1', '2': '2'},
#         #         '900002|combine|Neutral': {'3': '3'},
#         #         '900003|combine|B2B': {'4': '4', '5': '5'},
#         #     }
#         # }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         # {"qre_name": "$CS_Cons"},
#         # {"qre_name": "$CS_Not_Cons"},
#         #
#         # # {"qre_name": "Q19_01", "cats": {
#         # #     'net_code': {
#         # #         '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#         # #         '900002|combine|Passives': {'8': '7', '9': '8'},
#         # #         '900003|combine|Promoters': {'10': '9', '11': '10'},
#         # #     }
#         # # }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}},
#     ]
#
#
#     lst_side_axis_extra = [
#         {"qre_name": "$CS1"},
#         {"qre_name": "$CS2"},
#         {"qre_name": "$CS3_01"},
#         {"qre_name": "$CS3_02"},
#         {"qre_name": "$CS3_03"},
#         {"qre_name": "$CS3_04"},
#         {"qre_name": "$CS3_05"},
#         {"qre_name": "$CS_motive_01"},
#         {"qre_name": "$CS_motive_02"},
#         {"qre_name": "$CS_motive_03"},
#         {"qre_name": "$CS_motive_04"},
#         {"qre_name": "$CS_motive_05"},
#         {"qre_name": "$CS_motive_06"},
#         {"qre_name": "$CS_motive_07"},
#         {"qre_name": "$CS_motive_08"},
#         {"qre_name": "$CS_motive_09"},
#         {"qre_name": "$CS_motive_10"},
#         {"qre_name": "$CS_motive_11"},
#         {"qre_name": "$CS_motive_12"},
#         {"qre_name": "$CS_motive_13"},
#         {"qre_name": "$CS_motive_14"},
#         {"qre_name": "$CS_motive_15"},
#         {"qre_name": "$CS_motive_16"},
#         {"qre_name": "$CS_motive_17"},
#         {"qre_name": "$CS_motive_18"},
#         {"qre_name": "$CS_motive_19"},
#         {"qre_name": "$CS_motive_20"},
#         {"qre_name": "$CS_abandon_01"},
#         {"qre_name": "$CS_abandon_02"},
#         {"qre_name": "$CS_abandon_03"},
#         {"qre_name": "$CS_abandon_04"},
#         {"qre_name": "$CS_abandon_05"},
#         {"qre_name": "$CS_abandon_06"},
#         {"qre_name": "$CS_abandon_07"},
#         {"qre_name": "$CS_abandon_08"},
#         {"qre_name": "$CS_abandon_09"},
#         {"qre_name": "$CS_abandon_10"},
#         {"qre_name": "$CS_abandon_11"},
#         {"qre_name": "$CS_abandon_12"},
#         {"qre_name": "$CS_abandon_13"},
#         {"qre_name": "$CS_abandon_14"},
#         {"qre_name": "$CS_abandon_15"},
#         {"qre_name": "$CS_abandon_16"},
#         {"qre_name": "$CS_abandon_17"},
#         {"qre_name": "$CS_abandon_18"},
#         {"qre_name": "$CS_abandon_19"},
#         {"qre_name": "$CS_abandon_20"},
#
#         {"qre_name": "CS4_01", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_02", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_03", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_04", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_05", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_06", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_07", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_08", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_09", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_10", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_11", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_12", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_13", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_14", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_15", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_16", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_17", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_18", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_19", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#         {"qre_name": "CS4_20", "cats": {
#             '1': 'Completely satisfied', '2': 'Satisfied', '3': 'Neutral', '4': 'Dissatisfied', '5': 'Completely dissatisfied',
#             'net_code': {
#                 '900001|combine|T2B': {'1': '1', '2': '2'},
#                 '900002|combine|Neutral': {'3': '3'},
#                 '900003|combine|B2B': {'4': '4', '5': '5'},
#             }
#         }, "mean": {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}},
#
#         {
#             "qre_name": "CS_rec_01",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_02",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_03",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_04",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_05",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_06",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_07",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_08",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_09",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_10",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_11",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_12",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_13",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_14",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_15",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_16",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_17",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_18",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_19",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {
#             "qre_name": "CS_rec_20",
#             "cats": {
#                 '1': '0 - Definitely will not recommend', '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, '11': '10- Definitely will recommend',
#                 'net_code': {
#                     '900001|combine|Detractors': {'1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6'},
#                     '900002|combine|Passives': {'8': '7', '9': '8'},
#                     '900003|combine|Promoters': {'10': '9', '11': '10'},
#                 }
#             }, "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10}, "calculate": {"NPS": "abs([Promoters] - [Detractors])"}
#         },
#
#         {"qre_name": "ADD_ab"},
#
#     ]
#
#
#
#     lst_func_to_run = [
#         {
#             'func_name': 'run_standard_table_sig',
#             'tables_to_run': [
#                 'Total_C_W',
#                 'Total_C',
#                 'Total_P_W',
#                 # 'Total_P_sig',
#
#             ],
#             'tables_format': {
#                 "Total_P": {
#                     "tbl_name": "Total_P",
#                     "tbl_filter": "S1 > 0",
#                     "is_count": 0,
#                     "is_pct_sign": 1,
#                     "is_hide_oe_zero_cats": 1,
#                     "is_hide_zero_cols": 1,
#                     "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
#                     "lst_side_qres": lst_side_axis,
#                     "dict_header_qres": dict_header,
#                     "weight_var": '',
#                 },
#                 "Total_C": {
#                     "tbl_name": "Total_C",
#                     "tbl_filter": "S1 > 0",
#                     "is_count": 1,
#                     "is_pct_sign": 0,
#                     "is_hide_oe_zero_cats": 1,
#                     "is_hide_zero_cols": 1,
#                     "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
#                     "lst_side_qres": lst_side_axis,
#                     "dict_header_qres": dict_header,
#                     "weight_var": '',
#                 },
#                 "Total_P_W": {
#                     "tbl_name": "Total_P_W",
#                     "tbl_filter": "S1 > 0",
#                     "is_count": 0,
#                     "is_pct_sign": 1,
#                     "is_hide_oe_zero_cats": 1,
#                     "is_hide_zero_cols": 1,
#                     "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
#                     "lst_side_qres": lst_side_axis,
#                     "dict_header_qres": dict_header,
#                     "weight_var": 'Weighting',
#                 },
#                 "Total_C_W": {
#                     "tbl_name": "Total_C_W",
#                     "tbl_filter": "S1 > 0",
#                     "is_count": 1,
#                     "is_pct_sign": 0,
#                     "is_hide_oe_zero_cats": 1,
#                     "is_hide_zero_cols": 1,
#                     "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
#                     "lst_side_qres": lst_side_axis,
#                     "dict_header_qres": dict_header,
#                     "weight_var": 'Weighting',
#                 },
#
#
#                 "Total_P_sig": {
#                     "tbl_name": "Total_P_sig",
#                     "tbl_filter": "S1 > 0",
#                     "is_count": 0,
#                     "is_pct_sign": 1,
#                     "is_hide_oe_zero_cats": 1,
#                     "is_hide_zero_cols": 1,
#                     "sig_test_info": {"sig_type": "ind", "sig_cols": [], "lst_sig_lvl": [95]},
#                     "lst_side_qres": lst_side_axis,
#                     "dict_header_qres": dict_header,
#                     "weight_var": '',
#                 },
#             },
#         },
#     ]
#
#
#     dtg = DataTableGenerator(df_data=df_data, df_info=df_info, xlsx_name=str_tbl_file_name)
#     dtg.run_tables_by_js_files(lst_func_to_run)
#     dtf = TableFormatter(xlsx_name=str_tbl_file_name)
#     dtf.format_sig_table()
#
#
#
#
#     # FORMAT TABLES---------------------------------------------------------------------------------------------------------
#
#
#
#
#
#
#
#     print('\nPROCESSING COMPLETED | Duration', datetime.timedelta(seconds=time.time() - st))
