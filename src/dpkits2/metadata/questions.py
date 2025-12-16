import re
from pydantic import BaseModel, Field, model_validator
from typing import Union, Optional, Literal, Dict, List, Annotated




class GeneralCode(BaseModel):
    value: int
    label: str = Field(min_length=1)
    factor: Optional[Union[int, float]] = None
    is_exclusive: bool = False
    is_other: bool = False
    

class NettedCode(BaseModel):
    value: int
    label: str = Field(min_length=1)
    netted_type: Literal['Net', 'Combine']
    netted_fields: Optional[List[int]] = None


class _QreBase(BaseModel):
    name: str = Field(min_length=2)
    label: str = Field(min_length=2)
    qtype: str
    data_fields: list[str] = Field(min_length=1, default=None)
    index: Optional[int] = None
    
    model_config = {
        "extra": "allow"
    }

    
    # -------------------------
    # MODEL VALIDATION
    # -------------------------
    @model_validator(mode="after")
    def validate_qre_fields(self):
        
        errs = list()
        
        if self.name is None:
            errs.append('name must not None!')
        
        if self.label is None:
            errs.append('label must not None!')
        
        # if self.data_fields is None:
        #     errs.append('data_fields must not None!')
        
        # if self.index is None:
        #     errs.append('index must not None!')
        
        if errs:
            raise ValueError('\n'.join(errs))
        
        return self
    
    

class QreFreeText(_QreBase):
    qtype: Literal['FT'] = Field(default='FT')
    is_other_field: bool = False


class QreNumeric(_QreBase):
    qtype: Literal['NUM'] = Field(default='NUM')


class QreSingleAnswer(_QreBase):
    qtype: Literal['SA'] = Field(default='SA')
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    

    @model_validator(mode="after")
    def validate_fields(self):
        
        other_codes = {code_val for code_val, code in self.codes.items() if isinstance(code, GeneralCode) and code.is_other}
        other_codes = {f'{self.name}_o{int(code)}' for code in other_codes}
        
        if self.other_fields is not None or len(other_codes) > 0:
            
            other_fields_keys = set(self.other_fields.keys())
        
            missing = sorted(set().union(other_codes - other_fields_keys, other_fields_keys - other_codes))
            
            if missing:
                raise ValueError(f'Error: Missing other fields / other codes: {missing}')
        
        
        if self.name != self.data_fields[0] or len(self.data_fields) > 1:
            raise ValueError("Error: name and data_fields aren't match.")
        
        return self
    
    
    

class QreMultipleAnswer(_QreBase):
    qtype: Literal['MA'] = Field(default='MA')
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    
    
    @model_validator(mode="after")
    def validate_fields(self):
        
        other_codes = {code_val for code_val, code in self.codes.items() if isinstance(code, GeneralCode) and code.is_other}
        other_codes = {f'{self.name}_o{int(code)}' for code in other_codes}
        
        if self.other_fields is not None or len(other_codes) > 0:
            
            other_fields_keys = set(self.other_fields.keys())
        
            missing = sorted(set().union(other_codes - other_fields_keys, other_fields_keys - other_codes))
            
            if missing:
                raise ValueError(f'Error: Missing other fields / other codes: {missing}')
        
        
        general_codes = {code_val for code_val, code in self.codes.items() if isinstance(code, GeneralCode)}
        general_codes = {f'{self.name}_{int(code)}' for code in general_codes}
        
        missing = sorted(set().union(general_codes - set(self.data_fields), set(self.data_fields) - general_codes))
        
        if missing:
            raise ValueError(f"Error: name and data_fields aren't match: {missing}")
        
        return self
        
        
    
    
    
    

class QreRanking(_QreBase):
    qtype: Literal['RANKING'] = Field(default='RANKING')
    codes: Dict[int, Union[GeneralCode, NettedCode]]


MatrixSubQuestion = Annotated[
     Union[
        QreFreeText,
        QreNumeric,
        QreSingleAnswer,
        QreMultipleAnswer,
        QreRanking
    ],
    Field(discriminator='qtype'),
]



class QreMatrix(_QreBase):
    qtype: Literal['MATRIX'] = Field(default='MATRIX')
    sub_qres: Dict[str, MatrixSubQuestion] = Field(default_factory=dict)
    
    
    
Question = Annotated[
     Union[
        QreFreeText,
        QreNumeric,
        QreSingleAnswer,
        QreMultipleAnswer,
        QreRanking,
        QreMatrix
    ],
    Field(discriminator='qtype'),
]    
