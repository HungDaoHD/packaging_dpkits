import pandas as pd
import numpy as np
import pingouin as pg
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression





class DataAnalysis:

    def __init__(self, *, df_data: pd.DataFrame, df_info: pd.DataFrame):
        self.df_data = df_data
        self.df_info = df_info



    def penalty_analysis(self, *, dict_define_pen: dict, output_name: str):

        df_pen = pd.DataFrame(
            columns=['Section', 'Qre', 'Label', 'Ma_SP_Lbl', 'GroupCode', 'GroupCode_Pct', 'GroupCode_x_OL_Mean', 'JAR_x_OL_Mean', 'Penalty_Score', 'Pull_Down_Index'],
            data=[]
        )

        df_info = self.df_info.copy()

        for k_sec, v_sec in dict_define_pen.items():
            print(f'Processing penalty analysis - {k_sec}')

            df_data = self.df_data.query(v_sec.get('query')).copy() if v_sec.get('query') else self.df_data.copy()

            for k_sp, v_sp in df_info.loc[df_info.eval(f"var_name == '{v_sec['prod_pre']}'"), 'val_lbl'].values[0].items():

                df_fil = df_data.query(f"{v_sec['prod_pre']}.isin([{k_sp}])")

                for k_jar, v_jar in v_sec['jar_qres'].items():

                    jar_ol_mean = df_fil.loc[df_fil.eval(f"{k_jar}.isin({v_jar['jar']['code']})"), v_sec['ol_qre']].mean()

                    for grp in ['b2b', 't2b']:
                        grp_count = df_fil.loc[df_fil.eval(f"{k_jar}.isin({v_jar[grp]['code']})"), k_jar].count()
                        grp_base = df_fil.loc[df_fil.eval(f"{k_jar}.notnull()"), k_jar].count()

                        if not grp_base:
                            continue


                        grp_pct = grp_count / grp_base
                        grp_ol_mean = df_fil.loc[df_fil.eval(f"{k_jar}.isin({v_jar[grp]['code']})"), v_sec['ol_qre']].mean()
                        pen_score = jar_ol_mean - grp_ol_mean

                        dict_pen_data_row = {
                            'Section': k_sec,
                            'Qre': k_jar,
                            'Label': v_jar['label'],
                            'Ma_SP_Lbl': v_sp,
                            'GroupCode': v_jar[grp]['label'],
                            'GroupCode_Pct': grp_pct,
                            'GroupCode_x_OL_Mean': grp_ol_mean,
                            'JAR_x_OL_Mean': jar_ol_mean,
                            'Penalty_Score': pen_score,
                            'Pull_Down_Index': grp_pct * pen_score,
                        }

                        if df_pen.empty:
                            df_pen = pd.DataFrame(columns=list(dict_pen_data_row.keys()), data=[dict_pen_data_row.values()])
                        else:
                            df_pen = pd.concat([df_pen, pd.DataFrame(columns=list(dict_pen_data_row.keys()), data=[dict_pen_data_row.values()])], axis=0, ignore_index=True)

        with pd.ExcelWriter(f'{output_name}.xlsx', engine='openpyxl') as writer:
            df_pen.to_excel(writer, sheet_name=f'Penalty_Analysis')





    def linear_regression(self, *, dict_define_linear: dict, output_name: str | None, coef_only: bool = False) -> dict:
        """
        :param dict_define_linear: dict like
        {
            'lnr1': {
                'str_query': '',
                'dependent_vars': ['Q1'],
                'explanatory_vars': ['Q4', 'Q5', 'Q9', 'Q6', 'Q10'],
            },
            ...
        }
        :param output_name: *.xlsx | None
        :param coef_only: bool
        :return: dict[dataframe]
        """

        # Single: y = b + a*x
        # Multiple: y = b + a1*x1 + a2*x2 + ... + an*xn

        df_lbl: pd.DataFrame = self.df_info[['var_name', 'var_lbl']].copy()
        df_lbl = df_lbl.set_index(keys='var_name', drop=True)

        for k_lnr, v_lnr in dict_define_linear.items():
            print(f'Processing linear regression - {k_lnr}')

            df_data: pd.DataFrame = self.df_data.query(v_lnr['str_query']).copy() if v_lnr['str_query'] else self.df_data.copy()

            # If data have many dependent_vars, have to calculate mean of its
            df_data['dep_var'] = df_data[v_lnr['dependent_vars']].mean(axis=1)
            df_data = df_data.dropna(subset=['dep_var'], how='any')


            # Standardize predictors
            scaler_X = StandardScaler()
            X_std = scaler_X.fit_transform(df_data[v_lnr['explanatory_vars']])
            X_std = pd.DataFrame(X_std)
            X_std.columns = v_lnr['explanatory_vars']

            scaler_y = StandardScaler()
            y_std = scaler_y.fit_transform(df_data['dep_var'].to_numpy().reshape(-1, 1)).ravel()

            df_linear = pg.linear_regression(y=y_std, X=X_std)

            if coef_only:
                df_linear = df_linear[['names', 'coef']]

            dict_lbl = df_lbl.loc[v_lnr['explanatory_vars'], 'var_lbl'].to_dict()

            df_linear.insert(loc=1, column='label', value=df_linear['names'].replace(dict_lbl))

            v_lnr.update({'df_linear': df_linear})


        if output_name:
            with pd.ExcelWriter(f'{output_name}.xlsx') as writer:
                for k_lnr, v_lnr in dict_define_linear.items():

                    ws_name = f'Lnr Reg-{k_lnr}'
                    v_lnr['df_linear'].to_excel(writer, sheet_name=ws_name, startrow=3)

                    # format excel file

                    wb = writer.book
                    ws = writer.sheets[ws_name]

                    bold = wb.add_format({'bold': True})

                    ws.write('B1', 'Filter', bold)
                    ws.write('B2', 'Dependent Variables', bold)

                    ws.write('C1', v_lnr['str_query'] if v_lnr['str_query'] else 'No filter')
                    ws.write('C2', ', '.join(v_lnr['dependent_vars']))


        return dict_define_linear



    def correlation(self, *, dict_define_corr: dict, output_name: str):
        """
        :param dict_define_corr:
        :param output_name:
        :return: NONE
        """

        with pd.ExcelWriter(f'{output_name}', engine='openpyxl') as writer:
            for key, var in dict_define_corr.items():
                print(f'Processing correlation - {key}')

                df_data = self.df_data.query(var['str_query']).copy() if var['str_query'] else self.df_data.copy()

                # if have many dependent_vars, have to calculate mean of its
                df_data.loc[:, 'dep_var'] = df_data.loc[:, var['dependent_vars']].mean(axis=1)

                x = df_data['dep_var']
                df_corr = pd.DataFrame()


                for i, v in enumerate(var['explanatory_vars']):

                    corr = pg.corr(x, df_data[v])

                    corr['method'] = corr.index
                    corr['x'] = '|'.join(var['dependent_vars'])
                    corr['y'] = v
                    corr.index = [f'correlation {i + 1}']
                    corr = corr[['x', 'y'] + list(corr.columns)[:-2]]

                    df_corr = pd.concat([df_corr, corr])

                df_corr.to_excel(writer, sheet_name=key)



    def key_driver_analysis(self, *, dict_kda: dict, output_name: str | None) -> dict:


        for k_kda, v_kda in dict_kda.items():
            print(f'Processing KDA - {k_kda}')

            df_data: pd.DataFrame = self.df_data.query(v_kda['str_query']) if v_kda['str_query'] else self.df_data.copy()

            df_kda: pd.DataFrame = self.df_info.copy().set_index(keys='var_name', drop=False).loc[v_kda['explanatory_vars'], ['var_name', 'var_lbl']]


            if v_kda['axis_x_dependent_vars']:
                lst_col = v_kda['axis_x_dependent_vars'] + v_kda['axis_y_dependent_vars'] + v_kda['explanatory_vars']

            else:
                lst_col = v_kda['axis_y_dependent_vars'] + v_kda['explanatory_vars']


            df_data = df_data.dropna(subset=lst_col, how='any')

            X = df_data[v_kda['explanatory_vars']]
            scaler_X = StandardScaler()
            X_std = scaler_X.fit_transform(X)

            if v_kda['axis_x_dependent_vars']:

                y1 = df_data[v_kda['axis_x_dependent_vars']].mean(axis=1)
                y2 = df_data[v_kda['axis_y_dependent_vars']].mean(axis=1)

                all_y_std = np.concatenate([y1, y2]).reshape(-1, 1)
                scaler_y = StandardScaler().fit(all_y_std)

                y1_std = scaler_y.transform(y1.to_numpy().reshape(-1, 1)).ravel()
                y2_std = scaler_y.transform(y2.to_numpy().reshape(-1, 1)).ravel()

                model1 = LinearRegression(n_jobs=-1).fit(X_std, y1_std)
                model2 = LinearRegression(n_jobs=-1).fit(X_std, y2_std)

                df_kda['coef_axis_x'] = pd.Series(data=model1.coef_, index=v_kda['explanatory_vars'])
                df_kda['coef_axis_y'] = pd.Series(data=model2.coef_, index=v_kda['explanatory_vars'])

                all_coefs = np.concatenate([df_kda['coef_axis_x'], df_kda['coef_axis_y']]).reshape(-1, 1)

                scaler_coefs = StandardScaler().fit(all_coefs)

                df_kda['coef_axis_x_std'] = pd.Series(data=scaler_coefs.transform(df_kda['coef_axis_x'].to_numpy().reshape(-1, 1)).ravel(), index=v_kda['explanatory_vars'])
                df_kda['coef_axis_y_std'] = pd.Series(data=scaler_coefs.transform(df_kda['coef_axis_y'].to_numpy().reshape(-1, 1)).ravel(), index=v_kda['explanatory_vars'])


            else:

                y2 = df_data[v_kda['axis_y_dependent_vars']].mean(axis=1)
                y2_std = StandardScaler().fit_transform(y2.to_numpy().reshape(-1, 1)).ravel()
                model2 = LinearRegression(n_jobs=-1).fit(X_std, y2_std)

                df_kda['coef_axis_x'] = df_data[v_kda['explanatory_vars']].mean(axis=0)
                df_kda['coef_axis_y'] = pd.Series(data=model2.coef_, index=v_kda['explanatory_vars'])

                df_kda['coef_axis_x_std'] = pd.Series(data=StandardScaler().fit_transform(df_kda['coef_axis_x'].to_numpy().reshape(-1, 1)).ravel(), index=v_kda['explanatory_vars'])
                df_kda['coef_axis_y_std'] = pd.Series(data=StandardScaler().fit_transform(df_kda['coef_axis_y'].to_numpy().reshape(-1, 1)).ravel(), index=v_kda['explanatory_vars'])


            v_kda.update({'df_kda': df_kda})



        if output_name:
            with pd.ExcelWriter(f'{output_name}.xlsx') as writer:
                for k_kda, v_kda in dict_kda.items():
                    ws_name = k_kda
                    v_kda['df_kda'].to_excel(writer, sheet_name=ws_name, startrow=5)

                    # format excel file
                    wb = writer.book
                    ws = writer.sheets[ws_name]

                    bold = wb.add_format({'bold': True})

                    ws.write('B1', 'Filter', bold)
                    ws.write('B2', 'Axis-x dependent variables', bold)
                    ws.write('B3', 'Axis-y dependent variables', bold)

                    ws.write('C1', v_kda['str_query'] if v_kda['str_query'] else 'No filter')
                    ws.write('C2', ', '.join(v_kda['axis_x_dependent_vars']) if v_kda['axis_x_dependent_vars'] else 'Mean of Imagery Factors')
                    ws.write('C3', ', '.join(v_kda['axis_y_dependent_vars']))




        return dict_kda



    # MORE ANALYSIS HERE







