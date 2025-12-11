import os
import re
import time
import datetime
import functools
import zipfile
import pandas as pd
import numpy as np

from pydantic import BaseModel, Field, model_validator

from ..metadata.metadata import MetadataBuilder
from ..databox.databox import DataBox



class InputFile(BaseModel):
    folder_name: str = Field(min_length=1, default='DataToRun')
    file_name: str = Field(pattern=r"^.+\.(xlsx|csv|zip)$")
    is_qme_file: bool = Field(default=True)
    is_zip_file: bool = Field(default=False)
    
    
    @model_validator(mode='after')
    def check_file_exists(self):
        path = os.path.join(self.folder_name, self.file_name)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f'Error: File(s) not found: {path}')

        if '.zip' in self.file_name:
            self.is_zip_file = True
        
        return self



class DataConverter:

    def __init__(self, input_file: InputFile | dict):
        
        self.input_file = InputFile(**input_file) if isinstance(input_file, dict) else input_file
        self.data_box = DataBox(file_name=self.input_file.file_name.rsplit('.', 1)[0])
        self.lst_dropped = [
            'Approve',
            'Reject',
            'Re - do request',
            'Re-do request',
            'Reason to reject',
            'Memo',
            'No.',
            'Date',
            'Country',
            'Channel',
            'Chain / Type',
            'Distributor',
            'Method',
            'Panel FB',
            'Panel Email',
            'Panel Phone',
            'Panel Age',
            'Panel Gender',
            'Panel Area',
            'Panel Income',
            'Login ID',
            'User name',
            'Store ID',
            'Store Code',
            'Store name',
            'Store level',
            'District',
            'Ward',
            'Store address',
            'Area group',
            'Store ranking',
            'Region 2',
            'Nhóm cửa hàng',
            'Nhà phân phối',
            'Manager',
            'Telephone number',
            'Contact person',
            'Email',
            'Others 1',
            'Others 2',
            'Others 3',
            'Others 4',
            'Check in',
            'Store Latitude',
            'Store Longitude',
            'User Latitude',
            'User Longitude',
            'Check out',
            'Distance',
            'Task duration',
            'Panel ID',
            'InterviewerID',
            'InterviewerName',
            'RespondentName',
            'Edited',
            'Edited by',
            'Edited ratio',
            'Verify Status',
            'Images',
            'PVV',
            'Name',
            'Phone_number',
            'Q_Name',
            'Q_SDT',
            'Q_GT',
            'Tenpvv',
            'Infor',
            'Infor_1',
            'Infor_2',
            'infor',
            'infor_1',
            'infor_2',
            'InvitorName',
            'Phone',
            'RespondentAddress',
            'Respondent_name',
            'Respondent_info_1',
            'Respondent_info_2',
            'Respondent_NextSurvey',
            'Respondent_Channel',
            'RespondentPhonenumber',
            'ResName',
            'ResPhone',
            'ResAdd',
            'ResAdd_1',
            'ResAdd_2',
            'ResAdd_3',
            'ResDistrictHCM',
            'ResDistrictHN',
            'B2B_reward',
            'Company_Name',
            'Company_tax_number',
            'Company_tax_number_o3',
            'Phone_DV',
            'RespondentPhone',
            'PVV_Name',
            'Invite',
            'Interviewer_Name',
            'Address',
            'IP address (Public user)',
            'Group 3',
            'Personal information agreement',
            'Photo',
            'Reward',
            'IntName',
            'ResEmail',
        ]

    
    # Helpers ------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _time_it(func):

        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            st = time.time()
            run_func = func(*args, **kwargs)
            et = time.time()
            print(f'Run {func.__name__} - {datetime.timedelta(seconds=et - st)}')

            return run_func

        return inner_func

    
    
    @staticmethod
    def _cleanhtml(sr: pd.Series) -> str:
        CLEANR = re.compile('{.*?}|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\n|\xa0')
        sr['Question(Matrix)'] = re.sub(CLEANR, '', sr['Question(Matrix)']) if isinstance(sr['Question(Matrix)'], str) else sr['Question(Matrix)']
        sr['Question(Normal)'] = re.sub(CLEANR, '', sr['Question(Normal)']) if isinstance(sr['Question(Normal)'], str) else sr['Question(Normal)']
        return sr
    
    
    
    @staticmethod
    def _qre_grouping(sr: pd.Series) -> list:
        
        is_simple_qre = pd.isnull(sr['Question(Matrix)'])
        qtype = sr['Question type']
        qname = sr['Name of items']
        
        
        match qtype:
            case 'FT':
                
                if is_simple_qre:
                    if re.match(pattern=r".+_o\d{1,2}$", string=qname):
                        
                        return [qname.rsplit('_', 1)[0], np.nan]
                        
                    else:
                        return [qname, np.nan]

                else: 
                    
                    if re.match(pattern=r".+_o\d{1,2}$", string=qname):
                        return [qname.rsplit('_', 1)[0], qname.rsplit('_', 2)[0]]

                    else:
                        return [qname, qname.rsplit('_', 1)[0]]
            

            case 'NUM' | 'SA':
                
                if is_simple_qre:
                    return [qname, np.nan]
                
                else: 
                    return [qname, qname.rsplit('_', 1)[0]]
            
            
            case 'MA' | 'RANKING':
                
                if is_simple_qre:
                    return [qname.rsplit('_', 1)[0], np.nan]
                
                else:
                    return [qname.rsplit('_', 1)[0], qname.rsplit('_', 2)[0]]
                    
            case _:
                return [np.nan, np.nan]
        
       
            
        
    
    # End of Helpers -----------------------------------------------------------------------------------------------------------------------------------------
        
    

    @_time_it
    def _read_qme_file(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        
        print(f'Read input file {self.input_file.file_name}.')
        
        # Read file and convert to qme dataframe
        if not self.input_file.is_qme_file:
            print(f'Error: {self.input_file.file_name} is not Q&Me data file.')
            return
        
        str_full_path = '/'.join([self.input_file.folder_name, self.input_file.file_name])
        
        if self.input_file.is_zip_file:
            df_info_qme = pd.DataFrame()
            df_data_qme = pd.DataFrame()

            with zipfile.ZipFile(str_full_path) as zf:
                for f in zf.filelist:
                    with zf.open(f.filename) as ff:
                        if 'Questions' in f.filename:
                            df_info_qme = pd.read_csv(ff)
                            
                        else:
                            df_data_qme = pd.read_csv(ff, low_memory=False, header=4)

        else:
            df_info_qme = pd.read_excel(str_full_path, sheet_name='Question')
            df_data_qme = pd.read_excel(str_full_path, sheet_name='Data', header=4)
        
        # Re-format Matrix MA questions in 'df_info_qme'
        mask = (
            df_info_qme['Question(Matrix)'].notna()
            & (df_info_qme['Question type'] == 'MA')
            & df_info_qme[1].isna()
        )
        
        df_info_qme.loc[mask, 1] = df_info_qme.loc[mask, 'Question(Normal)']
        df_info_qme.loc[mask, 'Question(Normal)'] = np.nan
        df_info_qme['Question(Normal)'] = df_info_qme['Question(Normal)'].ffill()
        
        # Remove unuse rows of matrix questions in 'df_info_qme'
        mask = (
            df_info_qme['Question(Matrix)'].notna()
            & (df_info_qme['Question type'] == 'MA')
            & df_info_qme[2].notna()
        )
        lst_dropped_columns = df_info_qme.loc[mask, 'Name of items'].tolist()
        lst_dropped_columns.extend(set(df_info_qme.query("`Question type` == 'RANKING'")['Name of items'].values.tolist()).difference(df_data_qme.columns.to_list()))
        
        # Insert 'ID' row to 'df_info_qme'
        df_info_qme = pd.concat([pd.DataFrame(
            columns=df_info_qme.columns.to_list(),
            data=[['ID', 'FT', np.nan, 'ID'] + [np.nan] * (df_info_qme.shape[1] - 4)]
        ), df_info_qme.query("~(`Name of items`.isin(@lst_dropped_columns))")], ignore_index=True)
        
        df_info_qme = (
            df_info_qme
            .set_index('Name of items')
            .drop(index=self.lst_dropped, errors='ignore')
            .reset_index(drop=False)
        )
        
        # Check duplicated variables 'Name of items' in 'df_info_qme'
        dup_vars = df_info_qme.duplicated(subset=['Name of items'])
        if dup_vars.any():
            print(f"Error: Please check duplicated variables: {', '.join(df_info_qme.loc[dup_vars, 'Name of items'].values.tolist())}")
            return

        # Clean HTML formatting in 'df_info_qme'
        df_info_qme[['Question(Matrix)', 'Question(Normal)']] = df_info_qme[['Question(Matrix)', 'Question(Normal)']].apply(self._cleanhtml, axis=1)
        
        # Add group to all questions
        df_info_qme[['Qre_Simple_Group', 'Qre_Matrix_Group']] = df_info_qme.apply(self._qre_grouping, axis=1, result_type='expand')
        
        df_info_qme.insert(4, 'Qre_Matrix_Group', df_info_qme.pop('Qre_Matrix_Group'))
        df_info_qme.insert(4, 'Qre_Simple_Group', df_info_qme.pop('Qre_Simple_Group'))
        
        
        # drop all nan codes columns
        code_cols = [c for c in df_info_qme.columns if str(c).isdigit()]
        code_cols_dropped = df_info_qme[code_cols].isna().all(axis=0)
        df_info_qme = df_info_qme.drop(columns=code_cols_dropped[code_cols_dropped].index)
        
        
        # Start format df_data_qme
        df_data_qme = df_data_qme.T.reset_index(drop=False)
        mask = df_data_qme[0].notnull()
        
        df_data_qme.loc[mask, 'index'] = (
            df_data_qme
            .loc[mask, 'index']
            .replace(r"^Unnamed: \d+$", np.nan, regex=True)
            .ffill()
        )
        
        df_data_qme.loc[mask, 'index'] = (
            df_data_qme
            .loc[mask, ['index', 0]]
            .apply(lambda x: f'{x['index']}_{x[0].rsplit('_', 1)[-1]}', axis=1)
        )
        
        df_data_qme = (
            df_data_qme
            .set_index(keys='index', drop=True).T
            .loc[2:, df_info_qme['Name of items'].values.tolist()]
            .reset_index(drop=True)
        )
        
        # for idx in df_temp.index:
        #     str_prefix = df_data_header.at[idx, 3]
        #     str_suffix = df_data_header.at[idx, 4]
        #     if 'Reply' in str_suffix:
        #         df_data_header.at[idx, 3] = f"{str_prefix}_{str_suffix.replace(' - ', '_').replace(' ',  '_')}"
        #     else:
        #         df_data_header.at[idx, 3] = f"{str_prefix}_{str_suffix.rsplit('_', 1)[1]}"
        # df_data_header.loc[pd.isnull(df_data_header[3]), 3] = df_data_header.loc[pd.isnull(df_data_header[3]), 5]
        # dict_header = df_data_header[3].to_dict()
        # df_data = df_data.rename(columns=dict_header).drop(list(range(6)))
        
        return df_data_qme, df_info_qme

        

    
    @_time_it
    def convert(self) -> DataBox:    
        
        df_data_qme, df_info_qme = self._read_qme_file()

        # # For test
        # df_data_qme.to_csv(f'tests\\dpkits2\\df_data_qme.csv', encoding='utf-8-sig', index=False)
        # df_info_qme.to_csv(f'tests\\dpkits2\\df_info_qme.csv', encoding='utf-8-sig', index=False)
        # # For test
        
        metadata_builder = MetadataBuilder(df_data=df_data_qme, df_info=df_info_qme)
        
        self.data_box.metadata = metadata_builder.build()
        self.data_box.df_data = df_data_qme
        self.data_box.validate_data_box()
        
        return self.data_box

        

    