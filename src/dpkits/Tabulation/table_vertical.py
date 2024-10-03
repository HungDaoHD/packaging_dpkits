import pandas as pd
import numpy as np
from .logging import Logging
from .tabulation_model import TableFormat, SideQre, SideQres






class TabulationVertical(Logging):



    def generate_df_vertical(self, tbl_format: TableFormat, df_info: pd.DataFrame) -> pd.DataFrame:

        side_qres = SideQres(qres=tbl_format.tbl_side, df_info=df_info)

        for qre in side_qres.qres:
            print(qre.name)

        return pd.DataFrame()





    # dataframe of side qres
    # Here













