import pandas as pd
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
from ..metadata.metadata import Metadata, Question, List



class DataBox(BaseModel):
    file_name: str = Field(min_length=2)
    df_data: pd.DataFrame = Field(default=None)
    metadata: Optional[Metadata] = None
    
    # allow pandas types
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    
    # -------------------------
    # MODEL VALIDATION
    # -------------------------
    @model_validator(mode="after")
    def validate_data_box(self):
        if self.metadata is None or self.df_data is None:
            return self
        
        expected_cols = set(self.metadata.get_data_fields())
        df_cols = set(self.df_data.columns)

        missing = sorted(set().union(expected_cols - df_cols, df_cols - expected_cols))
        
        if missing:
            raise ValueError(f"Validate_data_box: df_data is missing columns required by metadata: {missing}")
        
        print(f"Validate_data_box: 'df_data' and 'metadata' are match.")
        
        return self
    
    
    def add_qres(self, qres: List[Question]) -> DataBox:
        
        # 1. add new to metadata
        # 2. add new cols to df_data
        
        self.metadata.add_qres(qres=qres)
        
        return self
    