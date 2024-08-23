from .tabulation_vertical import TabulationVertical
import pandas as pd
import numpy as np



class TabulationHorizontal(TabulationVertical):

    def __init__(self, dict_tbl_info: dict):

        super().__init__()

        self.dict_tbl_info = dict_tbl_info
        self.dict_all_tables = {'Content': pd.DataFrame(columns=['#', 'Content'], data=[])}



    def tabulate(self):

        pass


