import pandas as pd
import numpy as np
import time
import math
import functools
from scipy import stats
from datetime import datetime, timedelta
from .table_formater import TableFormatter
from .logging import Logging
from .tabulation_horizontal import TabulationHorizontal



class Tabulation(Logging, TabulationHorizontal, TableFormatter):

    def __init__(self, *, tbl_file_name: str, dict_tbl_info: dict[dict]):
        """
        :param tbl_file_name: output xlsx file name
        :param dict_tbl_info: all tables information for processing
        """

        self.tbl_file_name = tbl_file_name.rsplit('/', 1)[-1] if '/' in tbl_file_name else tbl_file_name

        Logging.__init__(self)
        TableFormatter.__init__(self, self.tbl_file_name)
        TabulationHorizontal.__init__(self, dict_tbl_info)



    @staticmethod
    def deco_tbl_file_name_permission(func):

        @functools.wraps(func)
        def inner_func(*args, **kwargs):

            try:
                with open(args[0].tbl_file_name):
                    args[0].print(f'File: "{args[0].tbl_file_name}" is accessed >>> Completed', args[0].clr_magenta)

            except PermissionError:
                args[0].print(f'Permission Error when access file: "{args[0].tbl_file_name}" Processing terminated.', args[0].clr_err)
                exit()

            except FileNotFoundError:
                pass

            return func(*args, **kwargs)

        return inner_func



    @staticmethod
    def deco_preprocess_inputted_dataframes(func):

        @functools.wraps(func)
        def inner_func(*args, **kwargs):

            args[0].print(f"Pre-process inputted dataframes:", args[0].clr_magenta)

            is_md: bool = kwargs['dict_tbl_info']['data_to_run']['is_md']
            df_data: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_data']
            df_info: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_info']

            # ----------------------------------------------------------------------------------------------------------
            if df_info['val_lbl'].dtype in [str, object]:
                args[0].print(f" - Convert 'val_lbl' from str to dict", args[0].clr_magenta, end='')

                def convert_to_dict(row):

                    if row == '{}':
                        return {}
                    elif isinstance(row, dict):
                        return row
                    else:
                        return eval(row)

                df_info['val_lbl'] = df_info['val_lbl'].apply(convert_to_dict)

                args[0].print(f" - Convert 'val_lbl' from str to dict >>> Completed", args[0].clr_magenta, is_remove_prev=True)

            # ----------------------------------------------------------------------------------------------------------
            if is_md:

                args[0].print(f' - Convert MD to MC', args[0].clr_magenta, end='')

                def recode_md_to_mc(row: pd.Series):
                    lst_re = [i + 1 for i, v in enumerate(row.values.tolist()) if v == 1]
                    return lst_re + ([np.nan] * (len(row.index) - len(lst_re)))

                def create_info_mc(row: pd.Series):
                    lst_val = row.values.tolist()
                    dict_re = {str(i + 1): v['1'] for i, v in enumerate(lst_val)}
                    return [dict_re] * len(lst_val)

                for idx in df_info.query("var_type.isin(['MA', 'MA_mtr']) & var_name.str.contains(r'^\\w+\\d*_1$')").index:
                    qre = df_info.at[idx, 'var_name'].rsplit('_', 1)[0]
                    fil_idx = df_info.eval(f"var_name.str.contains('^{qre}_[0-9]+$')")
                    cols = df_info.loc[fil_idx, 'var_name'].values.tolist()

                    df_data[cols] = df_data[cols].apply(recode_md_to_mc, axis=1, result_type='expand')
                    df_info.loc[fil_idx, ['val_lbl']] = df_info.loc[fil_idx, ['val_lbl']].apply(create_info_mc, result_type='expand')

                args[0].print(f' - Convert MD to MC >>> Completed', args[0].clr_magenta, is_remove_prev=True)

            # ----------------------------------------------------------------------------------------------------------
            args[0].print(f" - Add 'val_lbl_unnetted'", args[0].clr_magenta, end='')

            df_info['val_lbl_str'] = df_info['val_lbl'].astype(str)
            df_info['val_lbl_unnetted'] = df_info['val_lbl']

            args[0].print(f" - Add 'val_lbl_unnetted' >>> Completed", args[0].clr_magenta, is_remove_prev=True)

            for idx in df_info.query("val_lbl_str.str.contains('net_code')").index:

                dict_netted = df_info.at[idx, 'val_lbl_unnetted']
                dict_unnetted = dict()

                for key, val in dict_netted.items():

                    if 'net_code' in key:
                        val_lbl_lv1 = dict_netted['net_code']

                        for net_key, net_val in val_lbl_lv1.items():

                            args[0].print(f" - Unnetted {net_key}", args[0].clr_magenta, end='')

                            if isinstance(net_val, str):
                                dict_unnetted.update({str(net_key): net_val})
                            else:
                                args[0].print(f" - Unnetted {net_key} >>> Completed", args[0].clr_magenta, is_remove_prev=True)
                                dict_unnetted.update(net_val)

                    else:
                        dict_unnetted.update({str(key): val})

                df_info.at[idx, 'val_lbl_unnetted'] = dict_unnetted

            df_info.drop(columns='val_lbl_str', inplace=True)

            return func(*args, **kwargs)

        return inner_func



    @staticmethod
    def deco_valcheck_outstanding_values(func):

        @functools.wraps(func)
        def inner_func(*args, **kwargs):

            args[0].print(f"Valcheck outstanding values", args[0].clr_magenta, end='')

            df_data: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_data'].copy()
            df_info: pd.DataFrame = kwargs['dict_tbl_info']['data_to_run']['df_info'].copy()

            df_info = df_info.loc[df_info.eval("~var_type.isin(['FT', 'FT_mtr', 'NUM']) | var_name == 'ID'"), :].drop(columns=['var_lbl', 'var_type', 'val_lbl'])
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

                args[0].print(f'Outstanding values are detected\n{df_data.to_string()}\n>>> Terminated', args[0].clr_err, is_remove_prev=True)
                exit()
            else:
                args[0].print(f'Valcheck outstanding values >>> Completed', args[0].clr_magenta, is_remove_prev=True)

            return func(*args, **kwargs)

        return inner_func



    @staticmethod
    def deco_remove_duplicate_ma_values(func):

        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            args[0].print(f"Remove duplicated values in MA questions", args[0].clr_magenta, end='')

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
                cols = df_info.loc[df_info.eval(f"var_name.str.contains('^{prefix}_[0-9]{{1,2}}$')"), 'var_name'].values.tolist()
                df_data[cols] = df_data[cols].apply(remove_dup, axis=1, result_type='expand')

            args[0].print(f'Remove duplicated values in MA questions >>> Completed', args[0].clr_magenta, is_remove_prev=True)
            return func(*args, **kwargs)

        return inner_func



    @deco_tbl_file_name_permission
    @deco_preprocess_inputted_dataframes
    # @deco_valcheck_outstanding_values
    # @deco_remove_duplicate_ma_values
    def tabulate(self, *, lst_tbl_running: list):


        self.print(f"run: {lst_tbl_running}", self.clr_succ)




        pass


    # Note:
    #     - fix sig test, do not sig total with other code
    #     - fix sort method