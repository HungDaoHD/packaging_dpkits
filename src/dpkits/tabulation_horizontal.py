from .tabulation_vertical import TabulationVertical
import pandas as pd
import numpy as np



class TabulationHorizontal(TabulationVertical):

    def __init__(self):

        super().__init__()

        self.df_data = pd.DataFrame()
        self.df_info = pd.DataFrame()
        self.dict_tbl_info = dict





