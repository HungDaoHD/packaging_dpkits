import pandas as pd
import numpy as np
import time
import datetime


# from dpkits import *

# IGNORE THIS-----------------------------------------------------------------------------------------------------------
import sys
sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits')

from src.dpkits import (
    APDataConverter,
    DataProcessing,
    DataTranspose,
    DataTableGenerator,
    DataTableGeneratorV2,
    Tabulation,
    TableFormatter,
    CodeframeReader,
    LSMCalculation,
    DataAnalysis
)
# IGNORE THIS-----------------------------------------------------------------------------------------------------------





if __name__ == '__main__':

    # Get start time
    st = time.time()

    # Define input/output files name
    str_file_name = 'DataToRun/VN9999 - Project Name'
    str_file_name_no_path = str_file_name.rsplit('/', 1)[-1]
    str_tbl_file_name = f'{str_file_name_no_path}_Topline.xlsx'

    # Call Class APDataConverter with file_name
    converter = APDataConverter(file_name=f'{str_file_name}.xlsx')
    converter.lstDrop.extend(['P0', 'NAME', 'PHONE'])

    df_data, df_info = converter.convert_df_mc()
    df_data, df_info = pd.DataFrame(df_data), pd.DataFrame(df_info)



    # Add new question to df_data & df_info-----------------------------------------------------------------------------
    dict_add_new_qres = {
        'CIO_Usage_Visa': ['CIO Usage - Visa', 'SA', {'1': 'VISA'}, np.nan],
        'CIO_Usage_Mastercard': ['CIO Usage - Mastercard', 'SA', {'1': 'Mastercard'}, np.nan],
        'CIO_Usage_JCB': ['CIO Usage - JCB', 'SA', {'1': 'JCB'}, np.nan],

        'Q54_Merge|6': ['(International travellers) For what purposes have you visited the countries in the last 1 year?_Merge', 'MA', {'1': 'Business', '2': 'Leisure', '3': 'Family visit', '4': 'Education', '5': 'Medical', '6': 'Others'}, np.nan],
        'Q54_2_Merge|4': ['(International travellers) What kind of travel do you often prefer when coming to each country?_Merge', 'MA', {'1': 'Full tour depart from Vietnam', '2': 'Independent/ self-guided travel', '3': 'Purchase tour/ experience via online travel and activities booking platform (e.g. Klook, Viator, Getyourguide)', '4': 'Others'}, np.nan],

        'Q8_1_Sum': ['Q8_1_Sum', 'SA', {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6'}, np.nan],
        'Q53_Sum': ['Q53_Sum', 'SA', {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7'}, np.nan],

        'Q8_1_Net': ['Credit Card Usage', 'SA', {'1': 'Single', '2': 'Multiple'}, 1],

        'L7_Score_1': ['L7. Score_Everyday expenses (e.g., groceries, dining, fuel)', 'NUM', {}, 0],
        'L7_Score_2': ['L7. Score_Large purchases (e.g., electronics, furniture)', 'NUM', {}, 0],
        'L7_Score_3': ['L7. Score_Travel-related expenses (e.g., flights, hotels, transport)', 'NUM', {}, 0],
        'L7_Score_4': ['L7. Score_Online shopping', 'NUM', {}, 0],
        'L7_Score_5': ['L7. Score_Business-related expenses', 'NUM', {}, 0],
        'L7_Score_6': ['L7. Score_Medical or health-related payments', 'NUM', {}, 0],
        'L7_Score_7': ['L7. Score_Subscription services (e.g., streaming, memberships)', 'NUM', {}, 0],
        'L7_Score_8': ['L7. Score_Emergency or unexpected expenses', 'NUM', {}, 0],
        'L7_Score_9': ['L7. Score_Entertainment and relaxation (movie, bar/ club, spa)', 'NUM', {}, 0],
        'L7_Score_10': ['L7. Score_Social events (for kids, parents, networking)', 'NUM', {}, 0],
        'L7_Score_11': ['L7. Score_Other (specify)', 'NUM', {}, 0],

        'L7_Pct_by_Score_1': ['L7. Pct by Score_Everyday expenses (e.g., groceries, dining, fuel)', 'NUM', {}, 0],
        'L7_Pct_by_Score_2': ['L7. Pct by Score_Large purchases (e.g., electronics, furniture)', 'NUM', {}, 0],
        'L7_Pct_by_Score_3': ['L7. Pct by Score_Travel-related expenses (e.g., flights, hotels, transport)', 'NUM', {}, 0],
        'L7_Pct_by_Score_4': ['L7. Pct by Score_Online shopping', 'NUM', {}, 0],
        'L7_Pct_by_Score_5': ['L7. Pct by Score_Business-related expenses', 'NUM', {}, 0],
        'L7_Pct_by_Score_6': ['L7. Pct by Score_Medical or health-related payments', 'NUM', {}, 0],
        'L7_Pct_by_Score_7': ['L7. Pct by Score_Subscription services (e.g., streaming, memberships)', 'NUM', {}, 0],
        'L7_Pct_by_Score_8': ['L7. Pct by Score_Emergency or unexpected expenses', 'NUM', {}, 0],
        'L7_Pct_by_Score_9': ['L7. Pct by Score_Entertainment and relaxation (movie, bar/ club, spa)', 'NUM', {}, 0],
        'L7_Pct_by_Score_10': ['L7. Pct by Score_Social events (for kids, parents, networking)', 'NUM', {}, 0],
        'L7_Pct_by_Score_11': ['L7. Pct by Score_Other (specify)', 'NUM', {}, 0],

        'Logic_Check': ['Logic_Check', 'FT', {}, np.nan],
    }

    dp = DataProcessing(df_data=df_data, df_info=df_info)
    dp.add_qres(dict_add_new_qres)
    dp.convert_percentage(lst_qres=['L8|11', 'Q38|5', 'Q59|5'], fil_nan=None, is_check_sum=True)

    dp.merge_qres(lst_merge=['Q54_Merge_1', 'Q54_Merge_2', 'Q54_Merge_3', 'Q54_Merge_4', 'Q54_Merge_5', 'Q54_Merge_6'], lst_to_merge=['Q54_01_1', 'Q54_01_2', 'Q54_01_3', 'Q54_01_4', 'Q54_01_5', 'Q54_01_6', 'Q54_02_1', 'Q54_02_2', 'Q54_02_3', 'Q54_02_4', 'Q54_02_5', 'Q54_02_6', 'Q54_03_1', 'Q54_03_2', 'Q54_03_3', 'Q54_03_4', 'Q54_03_5', 'Q54_03_6', 'Q54_04_1', 'Q54_04_2', 'Q54_04_3', 'Q54_04_4', 'Q54_04_5', 'Q54_04_6', 'Q54_05_1', 'Q54_05_2', 'Q54_05_3', 'Q54_05_4', 'Q54_05_5', 'Q54_05_6', 'Q54_06_1', 'Q54_06_2', 'Q54_06_3', 'Q54_06_4', 'Q54_06_5', 'Q54_06_6', 'Q54_07_1', 'Q54_07_2', 'Q54_07_3', 'Q54_07_4', 'Q54_07_5', 'Q54_07_6', 'Q54_08_1', 'Q54_08_2', 'Q54_08_3', 'Q54_08_4', 'Q54_08_5', 'Q54_08_6', 'Q54_09_1', 'Q54_09_2', 'Q54_09_3', 'Q54_09_4', 'Q54_09_5', 'Q54_09_6', 'Q54_10_1', 'Q54_10_2', 'Q54_10_3', 'Q54_10_4', 'Q54_10_5', 'Q54_10_6', 'Q54_11_1', 'Q54_11_2', 'Q54_11_3', 'Q54_11_4', 'Q54_11_5', 'Q54_11_6', 'Q54_12_1', 'Q54_12_2', 'Q54_12_3', 'Q54_12_4', 'Q54_12_5', 'Q54_12_6', 'Q54_13_1', 'Q54_13_2', 'Q54_13_3', 'Q54_13_4', 'Q54_13_5', 'Q54_13_6', 'Q54_14_1', 'Q54_14_2', 'Q54_14_3', 'Q54_14_4', 'Q54_14_5', 'Q54_14_6'], dk_code=None)
    dp.merge_qres(lst_merge=['Q54_2_Merge_1', 'Q54_2_Merge_2', 'Q54_2_Merge_3', 'Q54_2_Merge_4'], lst_to_merge=['Q54_2_01_1', 'Q54_2_01_2', 'Q54_2_01_3', 'Q54_2_01_4', 'Q54_2_02_1', 'Q54_2_02_2', 'Q54_2_02_3', 'Q54_2_02_4', 'Q54_2_03_1', 'Q54_2_03_2', 'Q54_2_03_3', 'Q54_2_03_4', 'Q54_2_04_1', 'Q54_2_04_2', 'Q54_2_04_3', 'Q54_2_04_4', 'Q54_2_05_1', 'Q54_2_05_2', 'Q54_2_05_3', 'Q54_2_05_4', 'Q54_2_06_1', 'Q54_2_06_2', 'Q54_2_06_3', 'Q54_2_06_4', 'Q54_2_07_1', 'Q54_2_07_2', 'Q54_2_07_3', 'Q54_2_07_4', 'Q54_2_08_1', 'Q54_2_08_2', 'Q54_2_08_3', 'Q54_2_08_4', 'Q54_2_09_1', 'Q54_2_09_2', 'Q54_2_09_3', 'Q54_2_09_4', 'Q54_2_10_1', 'Q54_2_10_2', 'Q54_2_10_3', 'Q54_2_10_4', 'Q54_2_11_1', 'Q54_2_11_2', 'Q54_2_11_3', 'Q54_2_11_4', 'Q54_2_12_1', 'Q54_2_12_2', 'Q54_2_12_3', 'Q54_2_12_4', 'Q54_2_13_1', 'Q54_2_13_2', 'Q54_2_13_3', 'Q54_2_13_4', 'Q54_2_14_1', 'Q54_2_14_2', 'Q54_2_14_3', 'Q54_2_14_4'], dk_code=None)

    df_data, df_info = pd.DataFrame(dp.df_data), pd.DataFrame(dp.df_info)

    # add value to 'CIO_Usage'
    dict_cio_usage = {
        'Visa': {
            'Q10_1': [1, 5],
            'Q10_2': [1, 2, 3],
            'Q10_3': [1, 3, 4],
            'Q10_4': [1, 2],
            'Q10_5': [1, 2, 3],
            'Q10_6': [1, 4, 5],
            'Q10_7': [4, 5],
            'Q10_8': [1, 3],
            'Q10_9': [2, 3],
            'Q10_10': [1, 3],
            'Q10_12': [2],
            'Q10_14': [1, 2],
            'Q10_16': [2],
            'Q10_17': [2, 3, 4],
            'Q10_18': [3, 4],
            'Q10_19': [2],
        },
        'Mastercard': {
            'Q10_1': [3],
            'Q10_3': [5],
            'Q10_4': [3],
            'Q10_7': [2],
            'Q10_8': [2],
            'Q10_11': [1],
            'Q10_12': [3],
            'Q10_13': [1, 2, 4],
            'Q10_15': [2],
            'Q10_17': [1],
            'Q10_18': [2, 5, 6, 7, 8],
            'Q10_19': [1, 3],
        },
        'JCB': {
            'Q10_1': [4],
            'Q10_3': [2, 6],
            'Q10_7': [1, 3, 7],
            'Q10_8': [4],
            'Q10_9': [1, 4],
            'Q10_10': [2, 4],
            'Q10_11': [2],
            'Q10_12': [4],
            'Q10_13': [3],
            'Q10_15': [1, 3],
            'Q10_16': [1, 3],
        },
    }

    for key, val in dict_cio_usage.items():
        str_query = str()

        for sub_key, sub_val in val.items():
            lst_col = df_info.loc[df_info.eval(f"var_name.str.contains('^{sub_key}_[0-9]+$')"), 'var_name'].values.tolist()
            lst_col = [f"{i}.isin({sub_val})" for i in lst_col]

            if len(str_query) > 0:
                str_query += f" | ({'|'.join(lst_col)})"
            else:
                str_query = f"({'|'.join(lst_col)})"

        df_data.loc[df_data.eval(str_query), f'CIO_Usage_{key}'] = 1

    # Add new question to df_data & df_info-----------------------------------------------------------------------------


    # # Align MA data values to left--------------------------------------------------------------------------------------
    # df_data = dp.align_ma_values_to_left(qre_name='New_MA|6')

    df_data, df_info = pd.DataFrame(df_data), pd.DataFrame(df_info)

    df_data['Q47'] = df_data['Q47'].astype(float)
    df_info.loc[df_info.eval("var_name == 'Q47'"), 'var_type'] = 'NUM'
    df_data[['Q59_3', 'Q59_4', 'Q59_5']] = df_data[['Q59_3', 'Q59_4', 'Q59_5']].fillna(0)

    df_data['Q8_1_Sum'] = df_data[['Q8_1_01', 'Q8_1_02']].replace({6: 0}).sum(axis=1)
    df_data['Q53_Sum'] = df_data[[f'Q53_{str(i).zfill(2)}' for i in range(1, 15)]].replace({2: 1, 3: 4, 4: 7, 5: 10}).sum(axis=1)


    # LOGIC CHECKING----------------------------------------------------------------------------------------------------


    def logic_check(sr: pd.Series) -> str:

        lst_err = list()

        # L6 vs L3------------------------------------------------------------------------------------------------------
        l6_val = sr.filter(regex=r'^L6_[0-9]+$', axis=0).dropna().values.tolist()
        lst_check_l6 = [
            ['L3_01', 'L3_02', 3],
            ['L3_05', 'L3_06', 9],
            ['L3_08', 'L3_10', 10],
        ]

        for item in lst_check_l6:
            if (sr[item[0]] in [1, 2, 3] or sr[item[1]] in [1, 2, 3]) and item[-1] not in l6_val:
                lst_err.extend([f"{item[0]} or {item[1]} chose 1/2/3 and L6 doesn't chose {item[-1]}"])

        # L7 vs L8------------------------------------------------------------------------------------------------------
        for i in range(1, 11):
            l7_rank_curr = sr[f'L7_Rank{i}']
            l7_rank_next = sr[f'L7_Rank{i+1}']

            if not pd.isnull(l7_rank_next):
                l8_pct_curr = sr[f'L8_{int(l7_rank_curr)}']
                l8_pct_next = sr[f'L8_{int(l7_rank_next)}']

                if l8_pct_curr < l8_pct_next:
                    lst_err.extend([f"L7_Rank{i} = {l7_rank_curr} & L7_Rank{i+1} = {l7_rank_next} but L8_{int(l7_rank_curr)} < L8_{int(l7_rank_next)}"])


        # Q8_1_02 vs count of Q9
        q9_val = sr.filter(regex=r'^Q9_[0-9]+$', axis=0).dropna().values.tolist()

        if len(q9_val) > sr['Q8_1_02']:
            lst_err.extend([f"Count of bank in Q9 must less than or equal to Q8_1_02 == {sr['Q8_1_02']}"])

        # Q8_1_02 vs count of sum(Q10_1 to Q10_22)
        lst_q10_col = sr.filter(regex=r'^Q10_[0-9]+_[0-9]+$', axis=0).dropna().values.tolist()

        match sr['Q8_1_02']:
            case 1 | 2 | 3 | 4:
                if len(lst_q10_col) != sr['Q8_1_02']:
                    lst_err.extend([f"Count of card in Q10 must equal to Q8_1_02 == {sr['Q8_1_02']}"])

            case 5:
                if len(lst_q10_col) < sr['Q8_1_02']:
                    lst_err.extend([f"Count of card in Q10 must greater than or equal to Q8_1_02 == {sr['Q8_1_02']}"])

            case _:
                lst_err.extend([f"{sr['Q8_1_02']} = Not owning any types of this card"])


        # Q11_2 vs Q33_1
        q11_2 = sr['Q11_2']
        q33_1_main_card = sr[f'Q33_1_{str(int(q11_2)).zfill(2)}']
        q33_1_min = sr.filter(regex=r'^Q33_1_[0-9]+$', axis=0).dropna().min()

        if q33_1_main_card > q33_1_min:
            lst_err.extend([f"Q11_2 == {q11_2} so Q33_1_{str(int(q11_2)).zfill(2)} must equal {q33_1_min}"])


        # Q11_2 vs Q33_2
        q33_2_main_card = sr[f'Q33_2_{str(int(q11_2)).zfill(2)}']
        q33_2_max = sr.filter(regex=r'^Q33_2_[0-9]+$', axis=0).dropna().max()

        if q33_2_main_card > q33_2_max:
            lst_err.extend([f"Q11_2 == {q11_2} so Q33_2_{str(int(q11_2)).zfill(2)} must equal {q33_2_max}"])


        # Q38 code 3 vs Q8_1
        if sr['Q38_3'] > 0 and sr['Q8_1_01'] == 6 and sr['Q8_1_02'] == 1:
            lst_err.extend([f"Q8_1_01 = 6 & Q8_1_02 = 1 & Q38_3 > 0"])


        # Q59 code 3 vs Q8_1
        if sr['Q59_3'] > 0 and sr['Q8_1_01'] == 6 and sr['Q8_1_02'] == 1:
            lst_err.extend([f"Q8_1_01 = 6 & Q8_1_02 = 1 & Q59_3 > 0"])


        # Q52 vs Q53_01 -> 14
        q52_val = sr.filter(regex=r'^Q52_[0-9]+$', axis=0).dropna().values.tolist()

        for i in q52_val:
            if sr[f'Q53_{str(int(i)).zfill(2)}'] == 1:
                lst_err.extend([f"Q52 = {int(i)} but Q53_{str(int(i)).zfill(2)} = 1"])

        return ' | '.join(lst_err)



    df_data['Logic_Check'] = df_data.apply(logic_check, axis=1)
    # END LOGIC CHECKING------------------------------------------------------------------------------------------------

    # REBASE L8
    lst_l8_col = ['L8_1', 'L8_2', 'L8_3', 'L8_4', 'L8_5', 'L8_6', 'L8_7', 'L8_8', 'L8_9', 'L8_10', 'L8_11']
    df_data[lst_l8_col] = df_data[lst_l8_col].fillna(0)

    df_data.loc[df_data.eval("(~(Q8_1_02 == 1 & Q8_1_01 == 6))"), 'Q8_1_Net'] = 2

    df_data.loc[df_data.eval("Q31 > 0"), [f'Q32_2_{i}' for i in range(1, 9)]] = [np.nan] * 8

    df_info.loc[df_info.eval(f"var_name == 'Q47'"), ['var_type', 'val_lbl']] = ['SA', {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10'}]


    def scoring_l7(sr: pd.Series) -> pd.Series:
        dict_score = {
            1: 11,
            2: 10,
            3: 9,
            4: 8,
            5: 7,
            6: 6,
            7: 5,
            8: 4,
            9: 3,
            10: 2,
            11: 1,
        }

        l7_sum = 0

        for i in range(1, 12):
            val_rank = sr[f'L7_Rank{i}']

            if pd.isnull(val_rank):
                continue

            sr[f'L7_Score_{val_rank}'] = dict_score[i]

            l7_sum += dict_score[i]


        for i in range(1, 12):
            val_rank = sr[f'L7_Rank{i}']

            if pd.isnull(val_rank):
                continue

            sr[f'L7_Pct_by_Score_{val_rank}'] = dict_score[i] / l7_sum

        return sr


    df_data = df_data.apply(scoring_l7, axis=1)











    # Just for checking
    with pd.ExcelWriter(f'{str_file_name_no_path}_preview.xlsx') as writer:
        df_data.to_excel(writer, sheet_name='df_data')
        df_info.to_excel(writer, sheet_name='df_info')



    # # TRANSPOSE TO STACK----------------------------------------------------------------------------------------------------
    # lst_scr = ['S1', 'S2', 'S3_a', 'S3_b', 'S4', 'S5', 'S6_1', 'S6_2', 'S6_3', 'S6_4', 'S6_5', 'S6_6', 'S7', 'S8', 'S10', 'Weight_Var']
    #
    # lst_fc = ['F1_ByProdCode']
    #
    # dict_stack_structure = {
    #     'id_col': 'ID',
    #     'sp_col': 'Ma_SP',
    #     'lst_scr': lst_scr,
    #     'dict_sp': {
    #         1: {
    #             'Ma_SP_1': 'Ma_SP',
    #             'Q1_1': 'Q1',
    #             'Q2_1': 'Q2',
    #             'Q3_1': 'Q3',
    #             'Q4_1': 'Q4',
    #             'Q5_1': 'Q5',
    #             'Q9_1': 'Q9',
    #             'Q6_1': 'Q6',
    #             'Q7_1': 'Q7',
    #             'Q8_1': 'Q8',
    #             'Q10_1': 'Q10',
    #             'F1_YN_1': 'F1_YN_New',
    #             'F2_OE_1': 'F2_OE_New',
    #         },
    #         2: {
    #             'Ma_SP_2': 'Ma_SP',
    #             'Q1_2': 'Q1',
    #             'Q2_2': 'Q2',
    #             'Q3_2': 'Q3',
    #             'Q4_2': 'Q4',
    #             'Q5_2': 'Q5',
    #             'Q9_2': 'Q9',
    #             'Q6_2': 'Q6',
    #             'Q7_2': 'Q7',
    #             'Q8_2': 'Q8',
    #             'Q10_2': 'Q10',
    #             'F1_YN_2': 'F1_YN_New',
    #             'F2_OE_2': 'F2_OE_New',
    #         },
    #         3: {
    #             'Ma_SP_3': 'Ma_SP',
    #             'Q1_3': 'Q1',
    #             'Q2_3': 'Q2',
    #             'Q3_3': 'Q3',
    #             'Q4_3': 'Q4',
    #             'Q5_3': 'Q5',
    #             'Q9_3': 'Q9',
    #             'Q6_3': 'Q6',
    #             'Q7_3': 'Q7',
    #             'Q8_3': 'Q8',
    #             'Q10_3': 'Q10',
    #             'F1_YN_3': 'F1_YN_New',
    #             'F2_OE_3': 'F2_OE_New',
    #         },
    #     },
    #     'lst_fc': lst_fc
    # }
    #
    # df_data_stack, df_info_stack = DataTranspose.to_stack(df_data, df_info, dict_stack_structure)
    #
    #
    #
    # # TRANSPOSE TO UNSTACK--------------------------------------------------------------------------------------------------
    # dict_unstack_structure = {
    #     'id_col': 'ID',
    #     'sp_col': 'Ma_SP',
    #     'lst_col_part_head': lst_scr,
    #     'lst_col_part_body': ['Ma_SP', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q9', 'Q6', 'Q7', 'Q8', 'Q10', 'F1_YN_New', 'F2_OE_New'],
    #     'lst_col_part_tail': lst_fc
    # }
    #
    # df_data_unstack, df_info_unstack = DataTranspose.to_unstack(df_data_stack, df_info_stack, dict_unstack_structure)
    #
    #
    # # ----------------------------------------------------------------------------------------------------------------------
    # # OE RUNNING------------------------------------------------------------------------------------------------------------
    # # ----------------------------------------------------------------------------------------------------------------------
    # cfr = CodeframeReader(cf_file_name='VN8413_Codeframe.xlsm')
    #
    # # READ '*.xlsm' file -> CREATE 'output.xlsx' file -> RUN OE
    # # cfr.to_dataframe_file()
    #
    # # READ 'output.xlsx' file create before -> RUN OE
    # cfr.read_dataframe_output_file()
    #
    # dp = DataProcessing(df_data_stack, df_info_stack)
    #
    # df_data_stack, df_info_stack = dp.add_qres(cfr.dict_add_new_qres_oe)
    # df_data_stack, df_info_stack = pd.DataFrame(df_data_stack), pd.DataFrame(df_info_stack)
    #
    # df_coding = pd.DataFrame(cfr.df_full_oe_coding)
    #
    # # ['ID', 'Ma_SP'] will be defined base on each project
    # df_coding[['ID', 'Ma_SP']] = df_coding['RESPONDENTID'].str.rsplit('_', n=1, expand=True)
    # df_coding.drop(columns=['RESPONDENTID'], inplace=True)
    #
    # df_data_stack['Ma_SP'] = df_data_stack['Ma_SP'].astype(int)
    # df_coding['Ma_SP'] = df_coding['Ma_SP'].astype(int)
    #
    # lst_oe_col = df_coding.columns.tolist()
    # lst_oe_col.remove('ID')
    # lst_oe_col.remove('Ma_SP')
    #
    # df_data_stack = df_data_stack.merge(df_coding, how='left', on=['ID', 'Ma_SP'])
    #
    # for i in lst_oe_col:
    #     # df_data_stack[i].replace({99999: np.nan}, inplace=True)
    #     df_data_stack.replace({i: {99999: np.nan}}, inplace=True)
    #
    # # ----------------------------------------------------------------------------------------------------------------------
    # # EXPORT SAV DATA FILES-------------------------------------------------------------------------------------------------
    # # ----------------------------------------------------------------------------------------------------------------------
    # dict_dfs = {
    #     1: {
    #         'data': df_data,
    #         'info': df_info,
    #         'tail_name': 'ByCode',
    #         'sheet_name': 'ByCode',
    #         'is_recode_to_lbl': False,
    #     },
    #     2: {
    #         'data': df_data_stack,
    #         'info': df_info_stack,
    #         'tail_name': 'Stack',
    #         'sheet_name': 'Stack',
    #         'is_recode_to_lbl': False,
    #     },
    #     # 3: {
    #     #     'data': df_data_unstack,
    #     #     'info': df_info_unstack,
    #     #     'tail_name': 'Unstack',
    #     #     'sheet_name': 'Unstack',
    #     #     'is_recode_to_lbl': False,
    #     # },
    # }
    #
    # converter.generate_multiple_data_files(dict_dfs=dict_dfs, is_export_sav=False)
    #
    #
    #
    #
    # # ----------------------------------------------------------------------------------------------------------------------
    # # EXPORT DATA TABLES----------------------------------------------------------------------------------------------------
    # # ----------------------------------------------------------------------------------------------------------------------
    # """
    # README:
    #     - Side question properties:
    #     {
    #         "qre_name":
    #             - "$Q15",  # column name, must set '$' if it is MA question
    #             - "Q16_Merge#combine(Q16a_1, Q16a_2, Q16a_3, Q16a_4, Q16b_1, Q16b_2, Q16b_3)"  # Combine multiple MA questions with same 'cats' define
    #
    #         "qre_lbl": "{lbl}: new label",  # default df_info label, input {lbl} top keep original label and addin new label
    #
    #         "qre_filter": "Age.isin([2, 3])",  # use for filter question
    #
    #         "sort": "des", # sort options: acs / des
    #
    #         "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}  # calculate mean base on dict: key == code in data, value = weighted values
    #
    #         "cats": {  # use for define net/combine code with specify format
    #             'net_code': {
    #                 '900001|combine|Group 1 + 2': {
    #                     '1': 'Yellow/dull teeth',
    #                     '2': 'Sensitive teeth',
    #                     '3': 'Dental plaque',
    #                     '4': 'Caries',
    #                 },
    #                 '900002|net|Group 1': {
    #                     '1': 'Yellow/dull teeth',
    #                     '2': 'Sensitive teeth',
    #                 },
    #                 '900003|net|Group 2': {
    #                     '3': 'Dental plaque',
    #                     '4': 'Caries',
    #                 },
    #             },
    #             '8': 'Other (specify)',
    #             '9': 'No problem',
    #         },
    #
    #         # use for NUM questions
    #         "cats": {
    #             'mean': 'Mean',
    #             'std': 'Std',
    #             'min': 'Minimum',
    #             'max': 'Maximum',
    #             '25%': 'Quantile 25%',
    #             '50%': 'Quantile 50%',
    #             '75%': 'Quantile 75%',
    #         },
    #
    #         "calculate": {"lbl": "Sum(T2B, B2B)", "syntax": "[T2B] + [B2B]"},
    #     },
    #
    #     - Header question properties:
    #     {
    #         "qre_name": "S1",  # define 'S1' if SA, '$S1' if MA, '@S1_xxx' if create header base on specify condition
    #         "qre_lbl": "City",  # typing every label is fine
    #         "cats":
    #             # SA/MA: define category list base on df_info, use 'TOTAL' if need to display total column
    #             {
    #                 "TOTAL": "TOTAL",
    #                 '3': 'Hồ Chí Minh',
    #                 '4': 'Cần Thơ'
    #
    #             }
    #             # @: define header base on specify condition
    #             {
    #                 "S3_b.isin([2])": "<=30 (22-30 tuổi)",
    #                 "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
    #             }
    #     },
    #
    #     - Table properties:
    #         + key: table key name
    #         + value: table specify properties
    #
    #         "Main": {
    #             "tbl_name": "Main",  # display on excel sheet name
    #             "tbl_filter": "Ma_SP > 0",  # filter of this table
    #             "is_count": 0,  # 1 for count, 0 for percentage
    #             "is_pct_sign": 1,  # 1 for display '%' else 0
    #             "is_hide_oe_zero_cats": 1,  # 1 for hide answers which percentage = 0% at all header columns
    #             "is_hide_zero_cols": 1,  # 1 for hide header columns which percentage = 0% at all row
    #             "sig_test_info":  # define significant test
    #             {
    #                 "sig_type": "rel",  # 'rel' for dependent sig test, 'ind' for independent sig test
    #                 "sig_cols": [],  # define columns to sig, leave it blank if need to sig all columns
    #                 "lst_sig_lvl": [90, 95]  # sig level: maximum 2 levels
    #             },
    #             "lst_side_qres": lst_side_main,  # list of side question
    #             "lst_header_qres": lst_header,  # list of header defines
    #             "dict_header_qres": dict_header_main, # dict of header defines to run multiple group header
    #             "weight_var": [num type], # name of weighting variable in dataframe
    #         },
    #
    # """
    #
    #
    # lst_header = [
    #     # header lvl 1
    #     [
    #         {
    #             "qre_name": "S1",
    #             "qre_lbl": "City",
    #             "cats": {
    #                 # "TOTAL": "TOTAL",
    #                 # '3': 'Hồ Chí Minh',
    #                 # '4': 'Cần Thơ'
    #             }
    #         },
    #     ],
    #     # header lvl 2
    #     [
    #         {
    #             "qre_name": "@S3_b_Group",
    #             "qre_lbl": "Age",
    #             "cats": {
    #                 "S3_b > 0": "TOTAL",
    #                 "S3_b.isin([2])": "<=30 (22-30 tuổi)",
    #                 "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
    #             }
    #         },
    #         {
    #             "qre_name": "@S4_Class",
    #             "qre_lbl": "Class",
    #             "cats": {
    #                 "S4.isin([1, 2])": "A&B (Từ 13,500,000 đến 22,499,000 VND & Trên 22,500,000)",
    #                 "S4.isin([3])": "C (Từ 7,500,000 đến 13,499,000 VND)",
    #             }
    #         },
    #         {
    #             "qre_name": "@S8_BUMO",
    #             "qre_lbl": "BUMO",
    #             "cats": {
    #                 "S8.isin([2])": "Tiger nâu",
    #                 "S8.isin([6, 7, 8])": "Sài Gòn",
    #                 "S8.isin([12, 13, 14])": "Larue",
    #             }
    #         },
    #
    #         {
    #             "qre_name": "$S6",
    #             "qre_lbl": "S6",
    #             "cats": {}
    #         },
    #
    #
    #     ],
    #     # header lvl 3
    #     [
    #         {
    #             "qre_name": "Ma_SP",
    #             "qre_lbl": "Mã Concept",
    #             "cats": {}  # {'1': 'Concept 1', '2': 'Concept 2', '3': 'Concept 3'}
    #         },
    #     ],
    # ]
    #
    #
    #
    # # ----------------------------------------------------------------------------------------------------------------------
    # # Run multiple header with same level
    # # ----------------------------------------------------------------------------------------------------------------------
    # dict_header_scr = {
    #     # Group header 1st
    #     'lst_1': [
    #         # header lvl 1
    #         [
    #             {
    #                 "qre_name": "S1",
    #                 "qre_lbl": "City",
    #                 "cats": {
    #                     "Total": "Total",
    #                     '3': 'Hồ Chí Minh',
    #                     '4': 'Cần Thơ'
    #                 }
    #             },
    #         ],
    #         # header lvl 2
    #         [
    #             {
    #                 "qre_name": "@S3_b_Group",
    #                 "qre_lbl": "Age",
    #                 "cats": {
    #                     "S3_b > 0": "TOTAL",
    #                     "S3_b.isin([2])": "<=30 (22-30 tuổi)",
    #                     "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
    #                 }
    #             },
    #             # {
    #             #     "qre_name": "@S4_Class",
    #             #     "qre_lbl": "Class",
    #             #     "cats": {
    #             #         "S4.isin([1, 2])": "A&B (Từ 13,500,000 đến 22,499,000 VND & Trên 22,500,000)",
    #             #         "S4.isin([3])": "C (Từ 7,500,000 đến 13,499,000 VND)",
    #             #     }
    #             # },
    #             # {
    #             #     "qre_name": "@S8_BUMO",
    #             #     "qre_lbl": "BUMO",
    #             #     "cats": {
    #             #         "S8.isin([2])": "Tiger nâu",
    #             #         "S8.isin([6, 7, 8])": "Sài Gòn",
    #             #         "S8.isin([12, 13, 14])": "Larue",
    #             #     }
    #             # },
    #
    #         ],
    #     ],
    #
    #     # Group header 2nd
    #     'lst_2': [
    #         # header lvl 1
    #         [
    #             {
    #                 "qre_name": "@S4_Class",
    #                 "qre_lbl": "Class",
    #                 "cats": {
    #                     "S4.isin([1, 2])": "A&B (Từ 13,500,000 đến 22,499,000 VND & Trên 22,500,000)",
    #                     "S4.isin([3])": "C (Từ 7,500,000 đến 13,499,000 VND)",
    #                 }
    #             },
    #         ],
    #         # header lvl 2
    #         [
    #             {
    #                 "qre_name": "S1",
    #                 "qre_lbl": "City",
    #                 "cats": {
    #                     "TOTAL": "TOTAL",
    #                     '3': 'Hồ Chí Minh',
    #                     '4': 'Cần Thơ'
    #                 }
    #             },
    #             # {
    #             #     "qre_name": "@S8_BUMO",
    #             #     "qre_lbl": "BUMO",
    #             #     "cats": {
    #             #         "S8.isin([2])": "Tiger nâu",
    #             #         "S8.isin([6, 7, 8])": "Sài Gòn",
    #             #         "S8.isin([12, 13, 14])": "Larue",
    #             #     }
    #             # },
    #             #
    #             # {
    #             #     "qre_name": "$S6",
    #             #     "qre_lbl": "S6. testing",
    #             #     "cats": {}
    #             # },
    #
    #
    #         ],
    #     ],
    #     # Group header 3rd
    #     'lst_3': [
    #         # header lvl 1
    #         [
    #             {
    #                 "qre_name": "@S8_BUMO",
    #                 "qre_lbl": "BUMO",
    #                 "cats": {
    #                     "S8.isin([2])": "Tiger nâu",
    #                     "S8.isin([6, 7, 8])": "Sài Gòn",
    #                     "S8.isin([12, 13, 14])": "Larue",
    #                 }
    #             },
    #         ],
    #         # header lvl 2
    #         [
    #             {
    #                 "qre_name": "@S3_b_Group",
    #                 "qre_lbl": "Age",
    #                 "cats": {
    #                     "S3_b > 0": "TOTAL",
    #                     "S3_b.isin([2])": "<=30 (22-30 tuổi)",
    #                     "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
    #                 }
    #             },
    #             # {
    #             #     "qre_name": "@S4_Class",
    #             #     "qre_lbl": "Class",
    #             #     "cats": {
    #             #         "S4.isin([1, 2])": "A&B (Từ 13,500,000 đến 22,499,000 VND & Trên 22,500,000)",
    #             #         "S4.isin([3])": "C (Từ 7,500,000 đến 13,499,000 VND)",
    #             #     }
    #             # },
    #         ],
    #     ],
    # }
    #
    # dict_header_main = copy.deepcopy(dict_header_scr)
    #
    # dict_header_main['lst_1'] += [[
    #     {
    #         "qre_name": "Ma_SP",
    #         "qre_lbl": "Mã Concept",
    #         "cats": {}
    #     },
    # ]]
    #
    # dict_header_main['lst_2'] += [[
    #     {
    #         "qre_name": "Ma_SP",
    #         "qre_lbl": "Mã Concept",
    #         "cats": {}
    #     },
    # ]]
    #
    # dict_header_main['lst_3'] += [[
    #     {
    #         "qre_name": "Ma_SP",
    #         "qre_lbl": "Mã Concept",
    #         "cats": {}
    #     },
    # ]]
    #
    # # SIDE AXIS-------------------------------------------------------------------------------------------------------------
    # lst_side_scr_tagon = [
    #
    #     {"qre_name": "S1"},
    #     {"qre_name": "S2", "qre_lbl": "{lbl} - HCM", "qre_filter": "S1 == 3"},
    #     {"qre_name": "S3_a"},
    #     {"qre_name": "S3_b"},
    #     {"qre_name": "S4"},
    #     {"qre_name": "S5"},
    #
    #     {"qre_name": "$S6"},
    #     {"qre_name": "$S6_Merge"},
    #
    #
    #     {"qre_name": "$S6", "qre_lbl": "S6. Test derefine without full cats", "cats": {
    #         'net_code': {
    #             '900001|net|Net 0: aaaa': {
    #                 '1': 'Bia lon/chai',
    #             },
    #             '900002|combine|Net 0: code 2 -> 5': {
    #                 '2': 'Cà phê hòa tan/ uống liền',
    #                 '3': 'Nước ngọt có ga',
    #                 '4': 'Nước uống đóng chai',
    #                 '5': 'Nước tăng lực'
    #             },
    #             '900003|combine|Net 1: code 2 - 3': {
    #                 '2': 'Cà phê hòa tan/ uống liền',
    #                 '3': 'Nước ngọt có ga',
    #             },
    #             '900004|net|Net 2: code 2': {
    #                 '2': 'Cà phê hòa tan/ uống liền',
    #             },
    #             '900005|net|Net 2: code 3': {
    #                 '3': 'Nước ngọt có ga',
    #             },
    #             '900006|net|Net 1: 4 - 5': {
    #                 '4': 'Nước uống đóng chai',
    #                 '5': 'Nước tăng lực'
    #             },
    #
    #             '6': 'Tôi không uống loại nào ở trên'
    #         }
    #     }},
    #
    #     {"qre_name": "S7"},
    #     {"qre_name": "S8"},
    #     {"qre_name": "S10"},
    #
    #     {"qre_name": "Dealer_HCM_01_Rank1"},
    #     {"qre_name": "$Dealer_HCM_02_Rank"},
    # ]
    #
    # lst_side_main = [
    #     {"qre_name": "Q1", 'cats': {
    #         '1': '1 - Hoàn toàn không thích', '2': '2 - Không thích', '3': '3 - Không thích cũng không ghét', '4': '4 - Thích', '5': '5 - Rất thích',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         }
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, "friedman": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, "calculate": {
    #         "NPS": "abs([T2B] - [B2B])",
    #         "4 - Thích weight 0.2": "[4 - Thích]*0.2",
    #         "5 - Rất thích weight 0.8": "[5 - Rất thích]*0.8",
    #     }},
    #     {"qre_name": "Q4", 'cats': {
    #         '1': 'Hoàn toàn không phù hợp', '2': 'Không phù hợp', '3': 'Hơi không phù hợp', '4': 'Phù hợp', '5': 'Rất Phù hợp',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         }
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},
    #
    #     {"qre_name": "Q5", 'cats': {
    #         '1': 'Hoàn toàn không mới lạ và khác biệt', '2': 'Không mới lạ và khác biệt', '3': 'Hơi không mới lạ và khác biệt', '4': 'Mới lạ và khác biệt', '5': 'Rất mới lạ và khác biệt',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         }
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},
    #
    #     {"qre_name": "Q9", 'cats': {
    #         '1': 'Hoàn toàn không cao cấp', '2': 'Không cao cấp', '3': 'Hơi không cao cấp', '4': 'Cao cấp', '5': 'Rất cao cấp',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         }
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},
    #
    #     {"qre_name": "Q6", 'cats': {
    #         '1': 'Chắc chắn sẽ không mua', '2': 'Không mua', '3': 'Có thể sẽ mua hoặc không', '4': 'Sẽ mua', '5': 'Chắc chắn sẽ mua',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         }
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},
    #
    #     {"qre_name": "Q10", 'cats': {
    #         '1': 'Chắc chắn sẽ không mua', '2': 'Không mua', '3': 'Có thể sẽ mua hoặc không', '4': 'Sẽ mua', '5': 'Chắc chắn sẽ mua',
    #         'net_code': {
    #             '900001|combine|T2B': {'4': '4', '5': '5'},
    #             '900002|combine|Medium': {'3': '3'},
    #             '900003|combine|B2B': {'1': '1', '2': '2'},
    #         },
    #     }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, "friedman": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},
    #
    #     {"qre_name": "F1_YN_New", "calculate": {
    #         "Yes*0.2": "[Yes]*0.2",
    #         "Yes*0.8": "[Yes]*0.8",
    #     }},
    #
    # ]
    #
    # lst_side_oe = [
    #     {"qre_name": "$Q2_OE"},
    #     {"qre_name": "$Q3_OE"},
    #     {"qre_name": "$Q7_OE"},
    #     {"qre_name": "$Q8_OE"},
    #     {"qre_name": "$F2_OE_OE"},
    # ]
    #
    #
    # lst_func_to_run = [
    #     # SCREENER
    #     {
    #         'func_name': 'run_standard_table_sig',
    #         'tables_to_run': [
    #             'Scr_Tagon_count_Unweight',
    #             # 'Scr_Tagon_count_Weight',
    #             'Scr_Tagon_pct_Unweight',
    #             # 'Scr_Tagon_pct_Weight',
    #         ],
    #         'tables_format': {
    #             "Scr_Tagon_count_Unweight": {
    #                 "tbl_name": "Scr_Tagon_count_Unweight",
    #                 "tbl_filter": "S1 > 0",
    #                 "is_count": 1,
    #                 "is_pct_sign": 0,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_scr_tagon,
    #                 # "lst_header_qres": lst_header[:-1],
    #                 "dict_header_qres": dict_header_scr,
    #                 "weight_var": '',
    #             },
    #             "Scr_Tagon_count_Weight": {
    #                 "tbl_name": "Scr_Tagon_count_Weight",
    #                 "tbl_filter": "S1 > 0",
    #                 "is_count": 1,
    #                 "is_pct_sign": 0,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_scr_tagon,
    #                 # "lst_header_qres": lst_header[:-1],
    #                 "dict_header_qres": dict_header_scr,
    #                 "weight_var": 'Weight_Var',
    #             },
    #             "Scr_Tagon_pct_Unweight": {
    #                 "tbl_name": "Scr_Tagon_pct_Unweight",
    #                 "tbl_filter": "S1 > 0",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_scr_tagon,
    #                 # "lst_header_qres": lst_header[:-1],
    #                 "dict_header_qres": dict_header_scr,
    #                 "weight_var": '',
    #             },
    #             "Scr_Tagon_pct_Weight": {
    #                 "tbl_name": "Scr_Tagon_pct_Weight",
    #                 "tbl_filter": "S1 > 0",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_scr_tagon,
    #                 # "lst_header_qres": lst_header[:-1],
    #                 "dict_header_qres": dict_header_scr,
    #                 "weight_var": 'Weight_Var',
    #             },
    #         },
    #     },
    #
    #     # MAIN
    #     {
    #         'func_name': 'run_standard_table_sig',
    #         'tables_to_run': [
    #             'Main_Unweight',
    #             # 'Main_Weight',
    #             'Main_oe_Unweight',
    #             # 'Main_oe_Weight',
    #         ],
    #         'tables_format': {
    #
    #             "Main_Unweight": {
    #                 "tbl_name": "Main_Unweight",
    #                 "tbl_filter": "",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "rel", "sig_cols": [], "lst_sig_lvl": [90, 95]},
    #                 "lst_side_qres": lst_side_main,
    #                 # "lst_header_qres": lst_header,
    #                 "dict_header_qres": dict_header_main,
    #                 "weight_var": '',
    #             },
    #
    #             "Main_Weight": {
    #                 "tbl_name": "Main_Weight",
    #                 "tbl_filter": "",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_main,
    #                 # "lst_header_qres": lst_header,
    #                 "dict_header_qres": dict_header_main,
    #                 "weight_var": 'Weight_Var',
    #             },
    #
    #             "Main_oe_Unweight": {
    #                 "tbl_name": "Main_oe_Unweight",
    #                 "tbl_filter": "Ma_SP > 0",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_oe,
    #                 # "lst_header_qres": lst_header,
    #                 "dict_header_qres": dict_header_main,
    #                 "weight_var": '',
    #             },
    #
    #             "Main_oe_Weight": {
    #                 "tbl_name": "Main_oe_Weight",
    #                 "tbl_filter": "Ma_SP > 0",
    #                 "is_count": 0,
    #                 "is_pct_sign": 1,
    #                 "is_hide_oe_zero_cats": 1,
    #                 "is_hide_zero_cols": 1,
    #                 "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
    #                 "lst_side_qres": lst_side_oe,
    #                 # "lst_header_qres": lst_header,
    #                 "dict_header_qres": dict_header_main,
    #                 "weight_var": 'Weight_Var',
    #             },
    #         },
    #
    #     },
    # ]
    #
    #
    # # RUN TABLE FOR SCREENER
    # dtg_1 = DataTableGenerator(df_data=df_data, df_info=df_info, xlsx_name=str_tbl_file_name)
    # dtg_1.run_tables_by_js_files(lst_func_to_run[:1])
    #
    #
    # # RUN TABLE FOR MAIN
    # dtg_2 = DataTableGenerator(df_data=df_data_stack, df_info=df_info_stack, xlsx_name=str_tbl_file_name)
    # dtg_2.run_tables_by_js_files(lst_func_to_run[1:], is_append=True)
    #
    #
    # # FORMAT TABLES---------------------------------------------------------------------------------------------------------
    # dtf = TableFormatter(xlsx_name=str_tbl_file_name)
    # dtf.format_sig_table()  # OLD
    # dtf.format_workbook()  # NEW
    #
    #
    # # PENALTY ANALYSIS------------------------------------------------------------------------------------------------------
    # da = DataAnalysis(df_data=df_data_stack, df_info=df_info_stack)
    #
    # dict_jar_qres = {
    #     'Q4': {
    #         'label': 'Q4. AAA',
    #         'b2b': {'label': 'Weak', 'code': [1, 2]},
    #         'jar': {'label': 'Just about right', 'code': [3]},
    #         't2b': {'label': 'Strong', 'code': [4, 5]},
    #     },
    #     'Q5': {
    #         'label': 'Q5. BBB',
    #         'b2b': {'label': 'Weak', 'code': [1, 2]},
    #         'jar': {'label': 'Just about right', 'code': [3]},
    #         't2b': {'label': 'Strong', 'code': [4, 5]},
    #     },
    #     'Q9': {
    #         'label': 'Q9. CCC',
    #         'b2b': {'label': 'Weak', 'code': [1, 2]},
    #         'jar': {'label': 'Just about right', 'code': [3]},
    #         't2b': {'label': 'Strong', 'code': [4, 5]},
    #     },
    #     'Q6': {
    #         'label': 'Q6. DDD',
    #         'b2b': {'label': 'Weak', 'code': [1, 2]},
    #         'jar': {'label': 'Just about right', 'code': [3]},
    #         't2b': {'label': 'Strong', 'code': [4, 5]},
    #     },
    #     'Q10': {
    #         'label': 'Q10. EEE',
    #         'b2b': {'label': 'Weak', 'code': [1, 2]},
    #         'jar': {'label': 'Just about right', 'code': [3]},
    #         't2b': {'label': 'Strong', 'code': [4, 5]},
    #     },
    # }
    #
    # dict_define_pen = {
    #     'Total': {
    #         'query': '',
    #         'prod_pre': 'Ma_SP',
    #         'ol_qre': 'Q1',
    #         'jar_qres': dict_jar_qres
    #     },
    #     'Male': {
    #         'query': 'S2 == 2',
    #         'prod_pre': 'Ma_SP',
    #         'ol_qre': 'Q1',
    #         'jar_qres': dict_jar_qres
    #     },
    #     'HCM': {
    #         'query': 'S1 == 3',
    #         'prod_pre': 'Ma_SP',
    #         'ol_qre': 'Q1',
    #         'jar_qres': dict_jar_qres
    #     },
    #     'CanTho': {
    #         'query': 'S1 == 4',
    #         'prod_pre': 'Ma_SP',
    #         'ol_qre': 'Q1',
    #         'jar_qres': dict_jar_qres
    #     },
    # }
    #
    # da.penalty_analysis(dict_define_pen=dict_define_pen, output_name='VN8413_Penalty_Analysis')
    #
    #
    # # LINEAR REGRESSION-----------------------------------------------------------------------------------------------------
    # dict_define_linear = {
    #     'lnr1': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q4', 'Q5', 'Q9', 'Q6', 'Q10'],
    #     },
    #     'lnr2': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q4', 'Q5', 'Q9', 'Q10'],
    #     },
    #     'lnr3': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q4', 'Q5'],
    #     },
    #     'lnr4': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q9', 'Q10'],
    #     },
    #     'lnr5': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q4'],
    #     },
    #     'lnr6': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q5'],
    #     },
    #     'lnr7': {
    #         'str_query': '',
    #         'dependent_vars': ['Q1'],
    #         'explanatory_vars': ['Q10'],
    #     },
    # }
    #
    # da.linear_regression(dict_define_linear=dict_define_linear, output_name='VN8413_Linear_Regression')



    print('\nPROCESSING COMPLETED | Duration', datetime.timedelta(seconds=round(time.time() - st, 0)), '\n')



