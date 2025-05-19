import pandas as pd
import numpy as np
import time
import datetime
from pathlib import Path


# IGNORE THIS-----------------------------------------------------------------------------------------------------------
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dpkits import (
    APDataConverter,
    DataProcessing,
    DataTranspose,
    DataTableGenerator,
    Tabulation,
    TableFormatter,
    CodeframeReader,
    LSMCalculation,
    DataAnalysis,

    DataTableGeneratorV2,  # not yet done
    TableFormatterV2,  # not yet done
)
# IGNORE THIS-----------------------------------------------------------------------------------------------------------




if __name__ == '__main__':

    # # # --------------------------------------------------------------------------------------------------------------
    # # # Get start time to calculate processing duration---------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------
    st = time.time()

    # # # --------------------------------------------------------------------------------------------------------------
    # # # Define input/output files name--------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------
    str_data_folder_path = 'DataToRun'
    str_file_name = 'VN9999 - Project Name'
    str_tbl_file_name = f'{str_file_name}_Topline.xlsx'

    temp_data_path = Path(f"{str_file_name}_converted.xlsx")  # you could change this file name

    if not temp_data_path.exists():

        # # # ----------------------------------------------------------------------------------------------------------
        # # # Call Class APDataConverter with file_name-----------------------------------------------------------------
        # # # ----------------------------------------------------------------------------------------------------------
        converter = APDataConverter(file_name=f'{str_data_folder_path}/{str_file_name}.xlsx')
        converter.lstDrop.extend(['ResName', 'ResPhone', 'Invite', 'IntName', 'Reward', 'ResEmail'])

        # # # ----------------------------------------------------------------------------------------------------------
        # # # Convert system data to pandas dataframe-------------------------------------------------------------------
        # # # ----------------------------------------------------------------------------------------------------------
        df_data, df_info = converter.convert_df_mc(is_export_xlsx=False)
        df_data, df_info = pd.DataFrame(df_data), pd.DataFrame(df_info)

        # # # ----------------------------------------------------------------------------------------------------------
        # # # Save dataframe for timing saving when converting----------------------------------------------------------
        # # # If saving file to *.csv, notice 'encoding' parameter to ensure string type data saved in right format-----
        # # # ----------------------------------------------------------------------------------------------------------
        with pd.ExcelWriter(temp_data_path) as writer:
            df_data.to_excel(writer, sheet_name='df_data', index=False)
            df_info.to_excel(writer, sheet_name='df_info', index=False)

    else:

        # # # ----------------------------------------------------------------------------------------------------------
        # # # Load the saved dataframe----------------------------------------------------------------------------------
        # # # Be careful with 'val_lbl' when read excel, it will be string type and need to convert to dictionary-------
        # # # ----------------------------------------------------------------------------------------------------------
        df_data = pd.read_excel(temp_data_path, sheet_name='df_data')
        df_info = pd.read_excel(temp_data_path, sheet_name='df_info')






    # # # --------------------------------------------------------------------------------------------------------------
    # # # Pre-processing data (difference for each project)-------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------
    dict_brand_new = {
        '1': 'Sony',
        '2': 'Samsung',
        '3': 'LG',
        '4': 'Panasonic',
        '5': 'Toshiba',
        '6': 'TCL',
        '7': 'Sharp',
        '8': 'Casper',
        '9': 'Hisense',
        '971': 'Others 1',
        '972': 'Others 2',
        '973': 'Others 3',
        '999': 'None of the above',
    }

    str_query = "(var_name.str.contains('^BE2TV_[0-9]{1,2}+$')) | (var_name.str.contains('^BD11TV_[0-9]{2}_[0-9]{1,2}$')) | (var_name.str.contains('^PRE_[0-9]{1,2}+$')) | (var_name == 'PRE_MOST') | (var_name.str.contains('^BD11TV_INT2_[0-9]{2}_[0-9]{1,2}$'))"

    df_info.loc[df_info.eval(str_query), ['val_lbl']] = [dict_brand_new]

    df_info['val_lbl'] = df_info.apply(lambda x: eval(str(x['val_lbl'])), axis=1)

    lst_col_be2tv = df_data.filter(regex='^BE2TV_[0-9]{1,2}$').columns.tolist()
    df_data[lst_col_be2tv] = df_data[lst_col_be2tv].replace({11: 971, 12: 972, 13: 973, 10: 999})

    lst_col_pre = df_data.filter(regex='^PRE_[0-9]{1,2}$').columns.tolist() + ['PRE_MOST']
    df_data[lst_col_pre] = df_data[lst_col_pre].replace({10: 971, 11: 972, 12: 973, 13: 999, 14: 999})

    lst_col_bd11tv = df_data.filter(regex='^BD11TV_[0-9]{2}_[0-9]{1,2}$').columns.tolist()
    df_data[lst_col_bd11tv] = df_data[lst_col_bd11tv].replace({10: 971, 11: 972, 12: 973, 13: 999, 14: 999, 15: 999})

    lst_col_bd11tv_int = df_data.filter(regex='^BD11TV_INT2_[0-9]{2}_[0-9]{1,2}$').columns.tolist()
    df_data[lst_col_bd11tv_int] = df_data[lst_col_bd11tv_int].replace({10: 971, 11: 972, 12: 973, 13: 999, 14: 999, 15: 999})


    # Initialize DataProcessing
    dp = DataProcessing(df_data=df_data, df_info=df_info)

    # Add questions
    dict_add_new_qres = dict()

    for k, v in dict_brand_new.items():

        if int(k) == 999:
            continue

        dict_add_new_qres.update({f'BRAND_{k}': [v, 'SA', dict_brand_new, int(k)]})

    dp.add_qres(dict_add_new_qres)

    # One-hot encoding imagery
    dict_encoding = {
        'id_var': 'ID',
        'regex_imagery_col': r'^BD11TV_(\d+)_\d+$',
        'exclusive_codes': [999],
        'lvl1_name': 'BRAND',
        'lvl2_name': 'IMG',
    }

    dp.imagery_one_hot_encoding(dict_encoding=dict_encoding)

    dict_encoding = {
        'id_var': 'ID',
        'regex_imagery_col': r'^BD11TV_INT2_(\d+)_\d+$',
        'exclusive_codes': [999],
        'lvl1_name': 'BRAND',
        'lvl2_name': 'IMG2',
    }

    dp.imagery_one_hot_encoding(dict_encoding=dict_encoding)



    # One-hot encoding PRE(MA) & PRE_MOST(SA)
    dict_one_hot_regex = {
        'PRE_BIN': '^PRE_[0-9]{1,2}$',
        'PRE_MOST_BIN': '^PRE_MOST$',
        'Q2A_S_BIN': '^Q2A_S_[0-9]{1,2}$',
    }

    dp.one_hot_encoding(dict_one_hot_regex=dict_one_hot_regex)

    # Get processed dataframes
    df_data, df_info = pd.DataFrame(dp.df_data), pd.DataFrame(dp.df_info)


    # Check data (if needed)
    # ...
    # ...
    # ...


    # # # --------------------------------------------------------------------------------------------------------------
    # # # Transpose data to stack---------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    # Define id column name
    id_col = 'ID'

    # Define the column name to break down
    sp_col = 'BRAND'

    # Questions in this list will locate at the beginning of the data file
    lst_scr = ['CITY', 'GEN', 'AGE1', 'AGE2']

    # Questions in this list will locate at the end of the data file
    lst_fc = list()

    # Define breakdown variables
    dict_sp = dict()

    for i, (k, v) in enumerate(dict_brand_new.items()):

        if int(k) > 9:
            continue

        dict_sp.update({
            i + 1: {
                f'BRAND_{k}': 'BRAND',
                f'PRE_BIN_{k}': 'PRE_BIN',
                f'PRE_MOST_BIN_{k}': 'PRE_MOST_BIN',
                f'PUR2TV_{k.zfill(2)}': 'PUR2TV',
                f'CONSTV_{k.zfill(2)}': 'CONSTV',
            } | {
                f'BRAND_{k}_IMG_{i}': f'IMG_{i}' for i in range(1, 20)
            } | {
                f'BRAND_{k}_IMG2_{i}': f'IMG2_{i}' for i in range(1, 17)
            }
        })

    dict_stack_structure = {
        'id_col': id_col,
        'sp_col': sp_col,
        'lst_scr': lst_scr,
        'dict_sp': dict_sp,
        'lst_fc': lst_fc
    }

    df_data_stack, df_info_stack = DataTranspose.to_stack(df_data, df_info, dict_stack_structure)

    # Recode CONSTV
    df_data_stack['CONSTV'] = df_data_stack['CONSTV'].replace({1: 4, 2: 3, 3: 2, 4: 1})
    df_info_stack.loc[df_info_stack['var_name'] == 'CONSTV', ['val_lbl']] = [{'4': 'It would be my first choice', '3': 'I would seriously consider it', '2': 'I might consider it', '1': 'I would not consider it'}]


    with pd.ExcelWriter(f"{str_file_name}_cleaned.xlsx") as writer:
        df_data.to_excel(writer, sheet_name='df_data', index=False)
        df_info.to_excel(writer, sheet_name='df_info', index=False)

        df_data_stack.to_excel(writer, sheet_name='df_data_stack', index=False)
        df_info_stack.to_excel(writer, sheet_name='df_info_stack', index=False)


    # # # # --------------------------------------------------------------------------------------------------------------
    # # # # Transpose data to unstack-------------------------------------------------------------------------------------
    # # # # --------------------------------------------------------------------------------------------------------------
    #
    # dict_unstack_structure = {
    #     'id_col': 'ID',
    #     'sp_col': 'Ma_SP',
    #     'lst_col_part_head': lst_scr,
    #     'lst_col_part_body': ['Ma_SP', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q9', 'Q6', 'Q7', 'Q8', 'Q10', 'F1_YN_New', 'F2_OE_New'],
    #     'lst_col_part_tail': lst_fc
    # }
    #
    # df_data_unstack, df_info_unstack = DataTranspose.to_unstack(df_data_stack, df_info_stack, dict_unstack_structure)


    # # # # --------------------------------------------------------------------------------------------------------------
    # # # # OE data processing (if needed)--------------------------------------------------------------------------------
    # # # # --------------------------------------------------------------------------------------------------------------
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
    # df_data_stack, df_info_stack = dp.add_qres(cfr.dict_add_new_qres_oe, is_add_data_col=False)
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


    # # # # --------------------------------------------------------------------------------------------------------------
    # # # # Export rawdata files (*.sav, *.xlsx)--------------------------------------------------------------------------
    # # # # --------------------------------------------------------------------------------------------------------------
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
    # }
    #
    # converter.generate_multiple_data_files(dict_dfs=dict_dfs, is_export_sav=False, is_zip=False)


    # # # --------------------------------------------------------------------------------------------------------------
    # # # Data tables generation----------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------
    """
    README:
        - Side question properties:
        {
            "qre_name":
                - "$Q15",  # column name, must set '$' if it is MA question
                - "Q16_Merge#combine(Q16a_1, Q16a_2, Q16a_3, Q16a_4, Q16b_1, Q16b_2, Q16b_3)"  # Combine multiple MA questions with same 'cats' define

            "qre_lbl": "{lbl}: new label",  # default df_info label, input {lbl} top keep original label and addin new label

            "qre_filter": "Age.isin([2, 3])",  # use for filter question

            "sort": "des", # sort options: acs / des

            "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}  # calculate mean base on dict: key == code in data, value = weighted values

            "cats": {  # use for define net/combine code with specify format
                'net_code': {
                    '900001|combine|Group 1 + 2': {
                        '1': 'Yellow/dull teeth',
                        '2': 'Sensitive teeth',
                        '3': 'Dental plaque',
                        '4': 'Caries',
                    },
                    '900002|net|Group 1': {
                        '1': 'Yellow/dull teeth',
                        '2': 'Sensitive teeth',
                    },
                    '900003|net|Group 2': {
                        '3': 'Dental plaque',
                        '4': 'Caries',
                    },
                },
                '8': 'Other (specify)',
                '9': 'No problem',
            },

            # use for NUM questions
            "cats": {
                'mean': 'Mean',
                'std': 'Std',
                'min': 'Minimum',
                'max': 'Maximum',
                '25%': 'Quantile 25%',
                '50%': 'Quantile 50%',
                '75%': 'Quantile 75%',
            },

            "calculate": {"lbl": "Sum(T2B, B2B)", "syntax": "[T2B] + [B2B]"},
        },

        - Header question properties:
        {
            "qre_name": "S1",  # define 'S1' if SA, '$S1' if MA, '@S1_xxx' if create header base on specify condition
            "qre_lbl": "City",  # typing every label is fine
            "cats":
                # SA/MA: define category list base on df_info, use 'TOTAL' if need to display total column
                {
                    "TOTAL": "TOTAL",
                    '3': 'Hồ Chí Minh',
                    '4': 'Cần Thơ'

                }
                # @: define header base on specify condition
                {
                    "S3_b.isin([2])": "<=30 (22-30 tuổi)",
                    "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
                }
        },

        - Table properties:
            + key: table key name
            + value: table specify properties

            "Main": {
                "tbl_name": "Main",  # display on excel sheet name
                "tbl_filter": "Ma_SP > 0",  # filter of this table
                "is_count": 0,  # 1 for count, 0 for percentage
                "is_pct_sign": 1,  # 1 for display '%' else 0
                "is_hide_oe_zero_cats": 1,  # 1 for hide answers which percentage = 0% at all header columns
                "is_hide_zero_cols": 1,  # 1 for hide header columns which percentage = 0% at all row
                "sig_test_info":  # define significant test
                {
                    "sig_type": "rel",  # 'rel' for dependent sig test, 'ind' for independent sig test
                    "sig_cols": [],  # define columns to sig, leave it blank if need to sig all columns
                    "lst_sig_lvl": [90, 95]  # sig level: maximum 2 levels
                },
                "lst_side_qres": lst_side_main,  # list of side question
                "lst_header_qres": lst_header,  # list of header defines
                "dict_header_qres": dict_header_main, # dict of header defines to run multiple group header
                "weight_var": [num type], # name of weighting variable in dataframe
            },

    """

    dict_header = {
        # Group header 1st
        'lst_1': [
            # Group header 1st - lvl 1
            [
                {
                    "qre_name": "CITY",
                    "qre_lbl": "City",
                    "cats": {
                        "Total": "Total",
                        '1': 'Ho Chi Minh', '2': 'Hanoi', '3': 'Da Nang'
                    }
                },
            ],
            # Group header 1st - lvl 2
            [
                {
                    "qre_name": "GEN",
                    "qre_lbl": "Gender",
                    "cats": {}
                },

            ],
        ],

        # Group header 2nd
        'lst_2': [
            # Group header 2nd - lvl 1
            [
                {
                    "qre_name": "GEN",
                    "qre_lbl": "Gender",
                    "cats": {}
                },
            ],
            # Group header 2nd - lvl 2
            [
                {
                    "qre_name": "AGE2",
                    "qre_lbl": "Age Group",
                    "cats": {}
                },

            ],
        ],

    }

    lst_side = [
        {"qre_name": "EDU"},
        {"qre_name": "OWNTV"},
        {"qre_name": "$BE2TV"},

        {
            "qre_name": "PUR2TV_01",
            "cats": {
                '1': '0 - I will definitely would not purchase',
                '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7', '9': '8', '10': '9',
                '11': '10 - Definitely would purchase',
                'net_code': {
                    '900001|combine|T2B': {'10': '9', '11': '10'},
                    '900003|combine|B2B': {'1': '0', '2': '1'},
                },
            },
            "mean": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10},

        },

    ]

    lst_func_to_run = [

        {
            'tables_to_run': [
                'Table_Count',
                'Table_Pct',
            ],
            'tables_format': {
                "Table_Count": {
                    "tbl_name": "Table_Count",
                    "tbl_filter": "",
                    "is_count": 1,
                    "is_pct_sign": 0,
                    "is_hide_oe_zero_cats": 0,
                    "is_hide_zero_cols": 0,
                    "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
                    "lst_side_qres": lst_side,
                    "dict_header_qres": dict_header,
                    "weight_var": '',
                },
                "Table_Pct": {
                    "tbl_name": "Table_Pct",
                    "tbl_filter": "",
                    "is_count": 0,
                    "is_pct_sign": 1,
                    "is_hide_oe_zero_cats": 0,
                    "is_hide_zero_cols": 0,
                    "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
                    "lst_side_qres": lst_side,
                    "dict_header_qres": dict_header,
                    "weight_var": '',
                },
            },
        },
    ]


    dtg_1 = DataTableGenerator(df_data=df_data, df_info=df_info, xlsx_name=str_tbl_file_name)
    dtg_1.run_tables_by_js_files(lst_func_to_run)

    dtf = TableFormatter(xlsx_name=str_tbl_file_name)
    dtf.format_workbook()


    # # # # --------------------------------------------------------------------------------------------------------------
    # # # # PENALTY ANALYSIS----------------------------------------------------------------------------------------------
    # # # # --------------------------------------------------------------------------------------------------------------
    #
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


    # # # --------------------------------------------------------------------------------------------------------------
    # # # LINEAR REGRESSION---------------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    da = DataAnalysis(df_data=df_data_stack, df_info=df_info_stack)

    dict_define_linear = {
        'TV_General': {
            'str_query': '',
            'dependent_vars': ['PUR2TV'],
            'explanatory_vars': [f'IMG_{i}' for i in range(1, 20)],
        },
        'Sony': {
            'str_query': '(BRAND == 1)',
            'dependent_vars': ['PUR2TV'],
            'explanatory_vars': [f'IMG_{i}' for i in range(1, 20)],
        },
        'Samsung': {
            'str_query': '(BRAND == 2)',
            'dependent_vars': ['PUR2TV'],
            'explanatory_vars': [f'IMG_{i}' for i in range(1, 20)],
        },

    }

    da.linear_regression(dict_define_linear=dict_define_linear, output_name='VN9999 - Project Name_Linear_Regression')


    # # # --------------------------------------------------------------------------------------------------------------
    # # # Key Driver Analysis (KDA)-------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    da = DataAnalysis(df_data=df_data_stack, df_info=df_info_stack)

    lst_img = [f'IMG_{i}' for i in range(1, 20)]  # + [f'IMG2_{i}' for i in range(1, 17)]

    dict_kda = {
        'KDA_TV_General_1': {
            'str_query': '',
            'axis_x_dependent_vars': None,
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },
        'KDA_Sony_1': {
            'str_query': '(BRAND == 1)',
            'axis_x_dependent_vars': None,
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },
        'KDA_Samsung_1': {
            'str_query': '(BRAND == 2)',
            'axis_x_dependent_vars': None,
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },

        'KDA_LG_1': {
            'str_query': '(BRAND == 3)',
            'axis_x_dependent_vars': None,
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },

        'KDA_TV_General_2': {
            'str_query': '',
            'axis_x_dependent_vars': ['PRE_BIN', 'PRE_MOST_BIN'],
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },
        'KDA_Sony_2': {
            'str_query': '(BRAND == 1)',
            'axis_x_dependent_vars': ['PRE_BIN', 'PRE_MOST_BIN'],
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },
        'KDA_Samsung_2': {
            'str_query': '(BRAND == 2)',
            'axis_x_dependent_vars': ['PRE_BIN', 'PRE_MOST_BIN'],
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },

        'KDA_LG_2': {
            'str_query': '(BRAND == 3)',
            'axis_x_dependent_vars': ['PRE_BIN', 'PRE_MOST_BIN'],
            'axis_y_dependent_vars': ['PUR2TV'],
            'axis_x_explanatory_vars': None,
            'explanatory_vars': lst_img,
        },

    }

    da.key_driver_analysis(dict_kda=dict_kda, output_name='VN9999 - Project Name_KDA')


    # # # --------------------------------------------------------------------------------------------------------------
    # # # Correspondence Analysis (CA)----------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    da = DataAnalysis(df_data=df_data_stack, df_info=df_info_stack)

    lst_img = [f'IMG_{i}' for i in range(1, 20)]  # + [f'IMG2_{i}' for i in range(1, 17)]

    dict_ca = {
        'CA_All_Brand': {
            'str_query': '',
            'id_var': 'ID',
            'brand_var': 'BRAND',
            'imagery_vars': lst_img,
        },
        'CA_Top_4_Brand': {
            'str_query': 'BRAND.isin([1, 2, 3, 6])',
            'id_var': 'ID',
            'brand_var': 'BRAND',
            'imagery_vars': lst_img,
        },
        'CA_Top_3_Brand': {
            'str_query': 'BRAND.isin([1, 2, 3])',
            'id_var': 'ID',
            'brand_var': 'BRAND',
            'imagery_vars': lst_img,
        },
    }

    da.correspondence_analysis(dict_ca=dict_ca, output_name='VN9999 - Project Name_CA')


    # # # --------------------------------------------------------------------------------------------------------------
    # # # Price Sensitive Metric----------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    da = DataAnalysis(df_data=df_data, df_info=df_info)

    dict_psm = {
        'PSM_Total': {
            'str_query': '',
            'qre_psm': {
                'too_expensive': 'QQ1',
                'expensive': 'QQ2',
                'cheap': 'QQ3',
                'too_cheap': 'QQ4',
            },
            'is_remove_outlier': True
        },
        'PSM_HCM': {
            'str_query': '(CITY == 1)',
            'qre_psm': {
                'too_expensive': 'QQ1',
                'expensive': 'QQ2',
                'cheap': 'QQ3',
                'too_cheap': 'QQ4',
            },
            'is_remove_outlier': True
        },
        'PSM_HN': {
            'str_query': '(CITY == 2)',
            'qre_psm': {
                'too_expensive': 'QQ1',
                'expensive': 'QQ2',
                'cheap': 'QQ3',
                'too_cheap': 'QQ4',
            },
            'is_remove_outlier': True
        },
        'PSM_DN': {
            'str_query': '(CITY == 3)',
            'qre_psm': {
                'too_expensive': 'QQ1',
                'expensive': 'QQ2',
                'cheap': 'QQ3',
                'too_cheap': 'QQ4',
            },
            'is_remove_outlier': True
        },
    }

    da.price_sensitive_metric(dict_psm=dict_psm, output_name='VN9999 - Project Name_PSM.xlsx')


    # # # --------------------------------------------------------------------------------------------------------------
    # # # K-mean Segmentation-------------------------------------------------------------------------------------------
    # # # --------------------------------------------------------------------------------------------------------------

    # # ------------------------------------------------------------------
    # # REMEMBER One-hot encoding CATEGORICAL variables before run model
    # # ------------------------------------------------------------------

    dict_one_hot_regex = {
        'GEN_BIN': '^GEN$',
        'AGE2_BIN': '^AGE2$',
        'OWN0_BIN': '^OWN0_[0-9]{1,2}$',
        'BE2TV_BIN': '^BE2TV_[0-9]{1,2}$',
    }

    dp = DataProcessing(df_data=df_data, df_info=df_info)

    dp.one_hot_encoding(dict_one_hot_regex=dict_one_hot_regex)

    # Get processed dataframes
    df_data, df_info = pd.DataFrame(dp.df_data), pd.DataFrame(dp.df_info)


    # # ------------------------------------------
    # # After One-hot encoding then run model
    # # ------------------------------------------

    da = DataAnalysis(df_data=df_data, df_info=df_info)

    lst_qre = [
                'GEN_BIN_1',
                'GEN_BIN_2',
                'AGE2_BIN_1',
                'AGE2_BIN_2',
                'AGE2_BIN_3',
                'AGE2_BIN_4',
                'AGE2_BIN_5',
                'AGE2_BIN_6',
                'AGE2_BIN_7',
                'AGE2_BIN_8',
                'OWN0_BIN_1',
                'OWN0_BIN_2',
                'OWN0_BIN_3',
                'OWN0_BIN_4',
                'OWN0_BIN_5',
                'OWN0_BIN_6',
                'OWN0_BIN_7',
                'OWN0_BIN_8',
                'OWN0_BIN_9',
                'OWN0_BIN_10',
                'OWN0_BIN_11',
                'OWN0_BIN_12',
                'OWN0_BIN_13',
                'OWN0_BIN_14',
                'BE2TV_BIN_1',
                'BE2TV_BIN_2',
                'BE2TV_BIN_3',
                'BE2TV_BIN_4',
                'BE2TV_BIN_5',
                'BE2TV_BIN_6',
                'BE2TV_BIN_7',
                'BE2TV_BIN_8',
                'BE2TV_BIN_9',
                'PUR2TV_01',
                'PUR2TV_02',
                'PUR2TV_03',
                'PUR2TV_04',
                'PUR2TV_05',
                'PUR2TV_06',
                'PUR2TV_07',
                'PUR2TV_08',
                'PUR2TV_09',
            ]

    dict_k_mean = {
        'CLUSTER_1': {
            'str_query': '',
            'lst_qre': lst_qre,
            'n_clusters': 'auto',  # auto = model will find the best fit 'n_clusters', input number if you already know 'n_clusters'
        },
        # 'CLUSTER_2': {
        #     'str_query': '',
        #     'lst_qre': lst_qre,
        #     'n_clusters': 3,
        # },
    }

    df_data, df_info = da.k_mean_segmentation(dict_k_mean=dict_k_mean, output_name='VN9999 - Project Name_k_mean.xlsx')


    print('\nPROCESSING COMPLETED | Duration', datetime.timedelta(seconds=round(time.time() - st, 0)), '\n')



