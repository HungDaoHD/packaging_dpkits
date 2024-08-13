import os
import pandas as pd
import numpy as np
import time
import json
import sys
import math
import functools
from colorama import Fore
from scipy import stats
from datetime import datetime, timedelta
from .table_formater import TableFormatter


class DataTables(TableFormatter):

    def __init__(self, *, tbl_file_name: str):
        """
        :param tbl_file_name: output xlsx file name
        """

        try:
            check_perm = open(tbl_file_name)
            check_perm.close()
        except PermissionError:
            print(f'{Fore.RED}Permission Error when access file: {tbl_file_name} Processing terminated.{Fore.RESET}')
            exit()
        except FileNotFoundError:
            pass

        self.tbl_file_name = tbl_file_name.rsplit('/', 1)[-1] if '/' in tbl_file_name else tbl_file_name
        super().__init__(self.tbl_file_name)

        self.dict_all_tables = {
            'Content': pd.DataFrame(columns=['#', 'Content'], data=[]),
        }



    @staticmethod
    def preprocess_inputted_dataframes(func):

        @functools.wraps(func)
        def inner_preprocess_inputted_dataframes(*args, **kwargs):

            print(f"{Fore.MAGENTA}Pre-process inputted dataframes:")

            is_md: bool = kwargs['dict_tbl_info']['data_to_run']['is_md']
            df_data: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_data']
            df_info: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_info']

            # ----------------------------------------------------------------------------------------------------------
            if df_info['val_lbl'].dtype in [str, object]:
                print(f" - Convert 'val_lbl' from str to dict")

                def convert_to_dict(row):

                    if row == '{}':
                        return {}
                    elif isinstance(row, dict):
                        return row
                    else:
                        return eval(row)

                df_info['val_lbl'] = df_info['val_lbl'].apply(convert_to_dict)

            # ----------------------------------------------------------------------------------------------------------
            if is_md:

                print(f' - Convert MD to MC')

                def recode_md_to_mc(row: pd.Series):
                    lst_re = [i + 1 for i, v in enumerate(row.values.tolist()) if v == 1]
                    return lst_re + ([np.nan] * (len(row.index) - len(lst_re)))

                def create_info_mc(row: pd.Series):
                    lst_val = row.values.tolist()
                    dict_re = {str(i + 1): v['1'] for i, v in enumerate(lst_val)}
                    return [dict_re] * len(lst_val)

                for idx in df_info.query(
                        "var_type.isin(['MA', 'MA_mtr']) & var_name.str.contains(r'^\\w+\\d*_1$')").index:
                    qre = df_info.at[idx, 'var_name'].rsplit('_', 1)[0]
                    fil_idx = df_info.eval(f"var_name.str.contains('^{qre}_[0-9]+$')")
                    cols = df_info.loc[fil_idx, 'var_name'].values.tolist()

                    df_data[cols] = df_data[cols].apply(recode_md_to_mc, axis=1, result_type='expand')
                    df_info.loc[fil_idx, ['val_lbl']] = df_info.loc[fil_idx, ['val_lbl']].apply(create_info_mc,
                                                                                                result_type='expand')

            # ----------------------------------------------------------------------------------------------------------
            print(f" - Add 'val_lbl_unnetted'")

            df_info['val_lbl_str'] = df_info['val_lbl'].astype(str)
            df_info['val_lbl_unnetted'] = df_info['val_lbl']

            for idx in df_info.query("val_lbl_str.str.contains('net_code')").index:

                dict_netted = df_info.at[idx, 'val_lbl_unnetted']
                dict_unnetted = dict()

                for key, val in dict_netted.items():

                    if 'net_code' in key:
                        val_lbl_lv1 = dict_netted['net_code']

                        for net_key, net_val in val_lbl_lv1.items():

                            if isinstance(net_val, str):
                                dict_unnetted.update({str(net_key): net_val})
                            else:
                                print(f" - Unnetted {net_key}")
                                dict_unnetted.update(net_val)

                    else:
                        dict_unnetted.update({str(key): val})

                df_info.at[idx, 'val_lbl_unnetted'] = dict_unnetted

            df_info.drop(columns='val_lbl_str', inplace=True)
            print(f">>> Completed\n{Fore.RESET}")

            return func(*args, **kwargs)

        return inner_preprocess_inputted_dataframes



    @staticmethod
    def valcheck_outstanding_values(func):

        @functools.wraps(func)
        def inner_valcheck_outstanding_values(*args, **kwargs):

            print(f"{Fore.MAGENTA}Valcheck outstanding values:")

            df_data: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_data'].copy()
            df_info: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_info'].copy()

            df_info = df_info.loc[df_info.eval("~var_type.isin(['FT', 'FT_mtr', 'NUM']) | var_name == 'ID'"), :].drop(
                columns=['var_lbl', 'var_type', 'val_lbl'])
            df_data = df_data[df_info['var_name'].values.tolist()].dropna(axis=1, how='all').dropna(axis=0, how='all')
            df_info = df_info.set_index('var_name').loc[df_data.columns.tolist(), :]

            def convert_val_lbl(row):
                if row[0] != {}:
                    row[0] = {int(k): np.nan for k in row[0].keys()}

                return row

            df_info = df_info.apply(convert_val_lbl, axis=1)
            dict_replace = df_info.to_dict()['val_lbl_unnetted']

            df_data = df_data.replace(dict_replace).dropna(axis=1, how='all')

            cols = df_data.columns.tolist()

            if 'ID' in cols:
                cols.remove('ID')

            df_data = df_data.dropna(subset=cols, how='all', axis=0)

            if not df_data.empty:
                df_data.reset_index(drop=True if 'ID' in df_data.columns else False, inplace=True)
                df_data = pd.melt(df_data, id_vars=df_data.columns[0], value_vars=df_data.columns[1:]).dropna()

                print(f'{Fore.RED}{df_data.to_string()}\n>>> Terminated{Fore.RESET}\n')
                exit()
            else:
                print(f'>>> Completed\n{Fore.RESET}')

            return func(*args, **kwargs)

        return inner_valcheck_outstanding_values



    @staticmethod
    def remove_duplicate_ma_values(func):

        @functools.wraps(func)
        def inner_remove_duplicate_ma_values(*args, **kwargs):
            print(f"{Fore.MAGENTA}Remove duplicated values in MA questions")

            df_data: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_data']
            df_info: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_info']

            str_query = "var_name.str.contains(r'^\\w+_1$') & var_type.str.contains('MA')"
            df_info_ma = df_info.query(str_query)

            def remove_dup(row: pd.Series):
                row_idx = row.index.values.tolist()
                lst_val = row.drop_duplicates(keep='first').values.tolist()
                return lst_val + ([np.nan] * (len(row_idx) - len(lst_val)))

            for qre_ma in df_info_ma['var_name'].values.tolist():
                prefix, suffix = qre_ma.rsplit('_', 1)
                cols = df_info.loc[
                    df_info.eval(f"var_name.str.contains('^{prefix}_[0-9]{{1,2}}$')"), 'var_name'].values.tolist()
                df_data[cols] = df_data[cols].apply(remove_dup, axis=1, result_type='expand')

            print(f'>>> Completed\n{Fore.RESET}')
            return func(*args, **kwargs)

        return inner_remove_duplicate_ma_values



    @preprocess_inputted_dataframes
    @valcheck_outstanding_values
    @remove_duplicate_ma_values
    def generate_data_tables(self, *, dict_tbl_info: dict):
        """
        :param dict_tbl_info: tables information
        :return: none
        """

        lst_tbl_to_run = dict_tbl_info['tables_to_run']

        for tbl in lst_tbl_to_run:
            self.generate_data_table(
                tbl_info=dict_tbl_info['tables_format'][tbl],
                df_data=dict_tbl_info['data_to_run']['df_data'],
                df_info=dict_tbl_info['data_to_run']['df_info'],
            )



    def generate_data_table(self, *, tbl_info: dict, df_data: pd.DataFrame, df_info: pd.DataFrame):
        """
        :param tbl_info:
        :param df_data:
        :param df_info:
        :return:
        """

        # NOTE:
        # should run and add to 'self.dict_all_tables'
        # filter tables need to run

        """
        covert this patten to dataframe and merge with self.dict_all_tables

        'Tbl_count': {
            "tbl_name": "Tbl_count",
            "tbl_filter": "",
            "is_count": 1,
            "is_pct_sign": 0,
            "is_hide_oe_zero_cats": 1,
            "is_hide_zero_cols": 0,
            "sig_test_info": {"sig_type": "", "sig_cols": [], "lst_sig_lvl": []},
            "dict_header_qres": dict_header,
            "lst_side_qres": lst_side,
            "weight_var": '',
        },
        """

        try:

            self.dict_all_tables.update({tbl_info['tbl_name']: pd.DataFrame})

        except Exception:
            pass

    # need to revise 'run_tables_by_item' and 'run_standard_table_sig'

    def run_tables_by_item(self, item: dict):

        if 'json_file' in item.keys():

            with open(item['json_file'], encoding="UTF-8") as json_file:
                dict_tables = json.load(json_file)

        else:

            dict_tables = item['tables_format']

        if item['tables_to_run']:

            dict_tables_selected = dict()

            for tbl in item['tables_to_run']:
                dict_tables_selected[tbl] = dict_tables[tbl]

            dict_tables = dict_tables_selected

        for tbl_key, tbl_val in dict_tables.items():
            if tbl_val.get('weight_var') and tbl_val.get('sig_test_info').get('sig_type'):
                print(
                    f'\x1b[31;20m\nCannot run table "{tbl_key}" with significant test and weighting at the same time. Processing terminated!!!')
                exit()

        for tbl_key, tbl_val in dict_tables.items():
            start_time = time.time()

            print(Fore.GREEN, f"Run table: {tbl_val['tbl_name']}", Fore.RESET)

            df_tbl = getattr(self, item['func_name'])(tbl_val)

            print(Fore.GREEN, f"Create sheet: {tbl_val['tbl_name']}", Fore.RESET)

            with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df_tbl.to_excel(writer, sheet_name=tbl_val['tbl_name'], index=False)  # encoding='utf-8-sig'

            print(Fore.GREEN, f"Create sheet: {tbl_val['tbl_name']} Duration: ",
                  timedelta(seconds=time.time() - start_time), Fore.RESET)



    def run_standard_table_sig(self, tbl: dict) -> pd.DataFrame:

        df_tbl = pd.DataFrame()

        # create df_data with tbl_filter in json file
        df_data = self.df_data.query(tbl['tbl_filter']).copy() if tbl.get('tbl_filter') else self.df_data.copy()

        # create df_info with lst_side_qres in json file
        df_info = pd.DataFrame(columns=['var_name', 'var_lbl', 'var_type', 'val_lbl', 'qre_fil'], data=[])
        for qre in tbl['lst_side_qres']:

            if '$' in qre['qre_name']:

                if '_RANK' in str(qre['qre_name']).upper():
                    lst_qre_col = self.df_info.loc[self.df_info['var_name'].str.contains(
                        f"^{qre['qre_name'][1:]}[0-9]+$"), 'var_name'].values.tolist()
                else:
                    lst_qre_col = self.df_info.loc[self.df_info['var_name'].str.contains(
                        f"^{qre['qre_name'][1:]}_[0-9]+$"), 'var_name'].values.tolist()

                var_name = qre['qre_name'].replace('$', '')

            elif '#combine' in qre['qre_name']:
                var_name, str_comb = qre['qre_name'].split('#combine')
                lst_qre_col = str_comb.replace('(', '').replace(')', '').split(',')
            else:
                lst_qre_col = [qre['qre_name']]
                var_name = qre['qre_name']

            # NEW-------------------------------------------------------------------------------------------------------
            df_qre_info = self.df_info.query(f"var_name.isin({lst_qre_col})").copy()
            df_qre_info.reset_index(drop=True, inplace=True)

            if df_qre_info.empty:
                print(Fore.RED, f"\n\tQuestion(s) is not found: {qre['qre_name']}\n\tProcess terminated.", Fore.RESET)
                exit()

            dict_row = {
                'var_name': var_name,
                'var_lbl': qre['qre_lbl'].replace('{lbl}', df_qre_info.at[0, 'var_lbl']) if qre.get('qre_lbl') else
                df_qre_info.at[0, 'var_lbl'],
                'var_type': 'MA_comb' if '#combine' in qre['qre_name'] else (
                    'MA_Rank' if '$' in qre['qre_name'] and '_RANK' in str(qre['qre_name']).upper() else df_qre_info.at[
                        0, 'var_type']),
                'val_lbl': qre['cats'] if qre.get('cats') else df_qre_info.at[0, 'val_lbl'],
                'qre_fil': qre['qre_filter'] if qre.get('qre_filter') else "",
                'lst_qre_col': lst_qre_col,
                'mean': qre['mean'] if qre.get('mean') else {},
                'sort': qre['sort'] if qre.get('sort') else "",
                'calculate': qre['calculate'] if qre.get('calculate') else {},
                'friedman': qre['friedman'] if qre.get('friedman') else {},
                'weight_var': tbl['weight_var'] if tbl.get('weight_var') else "",
            }

            df_info = pd.concat([df_info, pd.DataFrame(columns=list(dict_row.keys()), data=[list(dict_row.values())])],
                                axis=0, ignore_index=True)

            # ----------------------------------------------------------------------------------------------------------

        if tbl.get('lst_header_qres'):
            # Maximum 5 levels of header
            lst_group_header = self.group_sig_table_header(tbl['lst_header_qres'])
        else:
            # TO DO: Run multiple header with same level
            lst_group_header = list()
            lvl_hd = -1
            for key_hd, val_hd in tbl['dict_header_qres'].items():

                if lvl_hd == -1:
                    lvl_hd = len(val_hd)
                else:
                    if lvl_hd != len(val_hd):
                        print("\x1b[31;20mHeader don't have the same level:", tbl['dict_header_qres'])
                        exit()

                # Maximum 5 levels for each header
                lst_group_header.extend(self.group_sig_table_header(val_hd))

        for grp_hd in lst_group_header:

            print(Fore.LIGHTCYAN_EX, f"Run table: {tbl['tbl_name']} -> group header:", Fore.RESET)

            for i in grp_hd.values():
                print(Fore.LIGHTGREEN_EX, f"\t{i['lbl']}", Fore.RESET)

            tbl_info_sig = {
                'tbl_name': tbl['tbl_name'],
                'is_count': tbl['is_count'],
                'is_pct_sign': tbl['is_pct_sign'],
                'sig_test_info': tbl['sig_test_info'],
                'dict_grp_header': grp_hd,
                'weight_var': tbl.get('weight_var') if tbl.get('weight_var') else ''
            }

            df_temp = self.run_standard_header_sig(df_data, df_info, tbl_info_sig=tbl_info_sig)

            if df_tbl.empty:
                df_tbl = df_temp
            else:
                lst_col_temp_to_add = list(df_temp.columns)[5:]
                df_tbl = pd.concat([df_tbl, df_temp[lst_col_temp_to_add]], axis=1)

        # drop row which have all value is nan
        df_tbl.dropna(how='all', inplace=True)

        # Drop rows in qre oe that have all columns are 0
        if tbl['is_hide_oe_zero_cats']:

            df_sum_oe_val = df_tbl.query("qre_name.str.contains('_OE') & qre_type == 'MA'").copy()

            if not df_sum_oe_val.empty:
                fil_col = list(df_sum_oe_val.columns)
                df_sum_oe_val = df_sum_oe_val.loc[:, fil_col[5:]]
                df_sum_oe_val.replace({'': np.nan, 0: np.nan}, inplace=True)

                # df_sum_oe_val = df_sum_oe_val.astype(float)
                # df_sum_oe_val['sum_val'] = df_sum_oe_val.sum(axis=1, skipna=True, numeric_only=True)

                df_sum_oe_val['sum_val'] = df_sum_oe_val.count(axis=1, numeric_only=True)

                df_sum_oe_val = df_sum_oe_val.query('sum_val == 0')

                df_tbl.drop(df_sum_oe_val.index, inplace=True)

        # Drop columns which all value equal 0
        if tbl['is_hide_zero_cols']:

            start_idx = df_tbl.query(f"cat_val == 'base'").index.tolist()[0]
            lst_val_col = [v for i, v in enumerate(df_tbl.columns.tolist()[5:]) if i % 2 == 0]

            df_fil = df_tbl.query("index >= @start_idx")[lst_val_col].copy()
            df_fil.replace({0: np.nan}, inplace=True)
            df_fil.dropna(axis='columns', how='all', inplace=True)

            lst_keep_col = list()
            for i in df_fil.columns.tolist():
                lst_keep_col.extend([i, i.replace('@val@', '@sig@')])

            df_tbl = df_tbl[df_tbl.columns.tolist()[:5] + lst_keep_col]

            # df_tbl.to_excel('df_tbl_review.xlsx')

        # Reset df table index
        df_tbl.reset_index(drop=True, inplace=True)

        # df_tbl.to_excel('zzz_df_tbl.xlsx', encoding='utf-8-sig')

        return df_tbl



# Note:
#     - fix sig test, do not sig total with other code
#     - fix sort method


# ----------------------------------------------------------------------------------------------------------------------