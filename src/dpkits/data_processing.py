import pandas as pd
import numpy as np
from colorama import Fore


class DataProcessing:

    def __init__(self, df_data: pd.DataFrame, df_info: pd.DataFrame):

        self.df_data: pd.DataFrame = df_data
        self.df_info: pd.DataFrame = df_info



    def add_qres(self, dict_add_new_qres: dict, is_add_oe_col: bool = False) -> (pd.DataFrame, pd.DataFrame):
        info_col_name = ['var_name', 'var_lbl', 'var_type', 'val_lbl']

        for key, val in dict_add_new_qres.items():

            if val[1] in ['MA']:
                qre_ma_name, max_col = str(key).rsplit('|', 1)

                for i in range(1, int(max_col) + 1):
                    self.df_info = pd.concat([self.df_info, pd.DataFrame(columns=info_col_name, data=[[f'{qre_ma_name}_{i}', val[0], val[1], val[2]]])], axis=0, ignore_index=True)

                    if '_OE' not in key or is_add_oe_col is True:
                        self.df_data = pd.concat([self.df_data, pd.DataFrame(columns=[f'{qre_ma_name}_{i}'], data=[val[-1]] * self.df_data.shape[0])], axis=1)

            else:
                self.df_info = pd.concat([self.df_info, pd.DataFrame(columns=info_col_name, data=[[key, val[0], val[1], val[2]]])], axis=0, ignore_index=True)

                if '_OE' not in key or is_add_oe_col is True:
                    self.df_data = pd.concat([self.df_data, pd.DataFrame(columns=[key], data=[val[-1]] * self.df_data.shape[0])], axis=1)


        self.df_data.reset_index(drop=True, inplace=True)
        self.df_info.reset_index(drop=True, inplace=True)

        return self.df_data, self.df_info



    def align_ma_values_to_left(self, qre_name: str | list, fillna_val: float = None) -> pd.DataFrame:

        lst_qre_name = [qre_name] if isinstance(qre_name, str) else qre_name

        for qre_item in lst_qre_name:

            qre, max_col = qre_item.rsplit('|', 1)

            lst_qre = [f'{qre}_{i}' for i in range(1, int(max_col) + 1)]

            df_fil = self.df_data.loc[:, lst_qre].copy()
            df_fil = df_fil.T
            df_sort = pd.DataFrame(np.sort(df_fil.values, axis=0), index=df_fil.index, columns=df_fil.columns)
            df_sort = df_sort.T
            self.df_data[lst_qre] = df_sort[lst_qre]

            del df_fil, df_sort

            if fillna_val:
                self.df_data.loc[self.df_data.eval(f"{qre}_1.isnull()"), f'{qre}_1'] = fillna_val

        return self.df_data




    def delete_qres(self, lst_col: list) -> (pd.DataFrame, pd.DataFrame):

        self.df_data.drop(columns=lst_col, inplace=True)
        self.df_info = self.df_info.loc[self.df_info.eval(f"~var_name.isin({lst_col})"), :].copy()

        self.df_data.reset_index(drop=True, inplace=True)
        self.df_info.reset_index(drop=True, inplace=True)

        return self.df_data, self.df_info



    def merge_qres(self, *, lst_merge: list, lst_to_merge: list, dk_code: int) -> pd.DataFrame:

        codelist = self.df_info.loc[self.df_info.eval("var_name == @lst_merge[0]"), 'val_lbl'].values.tolist()[0]

        if len(lst_merge) < len(codelist.keys()):
            print(f"{Fore.RED}Merge_qres(error): Length of lst_merge should be greater than or equal length of codelist!!!\n"
                  f"lst_merge = {lst_merge}\ncodelist = {codelist}\nProcessing terminated!!!{Fore.RESET}")
            exit()


        def merge_row(sr_row: pd.Series, lst_col_name: list, dk: int) -> pd.Series:

            lst_output = sr_row.reset_index(drop=True).drop_duplicates(keep='first').dropna().sort_values().values.tolist()
            output_len = len(lst_col_name)

            if len(lst_output) > 1 and dk in lst_output:
                lst_output.remove(dk)

            if len(lst_output) < output_len:
                lst_output.extend([np.nan] * (output_len - len(lst_output)))

            return pd.Series(data=lst_output, index=lst_col_name)

        self.df_data[lst_merge] = self.df_data[lst_to_merge].apply(merge_row, lst_col_name=lst_merge, dk=dk_code, axis=1)

        return self.df_data



    @staticmethod
    def concept_evaluate(cpt_filename: str, ) -> (pd.DataFrame, dict):
        # Here: May 16
        # 1. clean inputted concept
        # 2. create codeframe for each word for concept
        # 3. match verbatim to concept codeframe
        # 4. return dataframe with codes of the words in concept

        return pd.DataFrame(), dict()  # dataframe & codelíst




