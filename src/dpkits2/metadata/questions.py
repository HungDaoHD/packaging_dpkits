from pydantic import BaseModel, Field
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
    netted_fields: Optional[List[str]] = None


class _QreBase(BaseModel):
    name: str = Field(min_length=2)
    label: str = Field(min_length=2)
    qtype: str
    data_fields: list[str] = Field(min_length=1)
    index: int
    
    model_config = {
        "extra": "allow"
    }


class QreFreeText(_QreBase):
    qtype: Literal['FT']
    is_other_field: bool = False


class QreNumeric(_QreBase):
    qtype: Literal['NUM']
    pass

    
class QreSingleAnswer(_QreBase):
    qtype: Literal['SA']
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    

class QreMultipleAnswer(_QreBase):
    qtype: Literal['MA']
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None


class QreRanking(_QreBase):
    qtype: Literal['RANKING']
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
    qtype: Literal['MATRIX']
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
