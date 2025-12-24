from pydantic import BaseModel, Field, model_validator
from typing import Union, Optional, Literal, Dict, List, Annotated
import re as regex
from collections import Counter



# CONST VARIABLES DEFINE
OTHER_PATTERN = regex.compile(r'^.+_o\d+$')




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
    data_fields: Optional[List[str]] = None
    index: Optional[int] = None
    
    model_config = {
        "extra": "allow"
    }

    

    @staticmethod
    def validate_duplicate_codes(codes: dict | list) -> tuple:
        convertesd_codes = codes if isinstance(codes, list) else list(codes.values())
        values = [c.value for c in convertesd_codes]
        dup_values = [v for v, n in Counter(values).items() if n > 1]
        return sorted(dup_values)
    
    
    
    @staticmethod
    def validate_duplicate_other_fields(other_fields: dict | list) -> tuple:
        convertesd_other_fields = other_fields if isinstance(other_fields, list) else list(other_fields.values())
        otf_names = [otf.name for otf in convertesd_other_fields]
        dup_otf_names = [n for n, k in Counter(otf_names).items() if k > 1]
        return dup_otf_names
        
    
    
    @model_validator(mode='before')
    @classmethod
    def valcheck_and_auto_generate_fields(cls, qre_values: dict):
        
        # get qtype from input OR from class default
        qtype = qre_values.get('qtype')
        if qtype is None:
            qre_values['qtype'] = cls.model_fields.get("qtype").default
            
        
        if qre_values.get('qtype') in ['FT', 'NUM']:
            
            # Set 'is_other_field'
            qre_values['is_other_field'] = bool(OTHER_PATTERN.match(qre_values['name']))
            
            if qre_values.get('data_fields') is None:
                qre_values['data_fields'] = [qre_values.get('name')]

        
        if qre_values.get('qtype') in ['SA', 'MA', 'RANKING']:
            
            if qre_values.get('codes') is None:
                raise ValueError(f"Error: {qre_values.get('name')} codes must not None!")
            
            dup_values = cls.validate_duplicate_codes(qre_values.get('codes'))
            if dup_values:
                raise ValueError(f"Error: {qre_values.get('name')} has duplicated code value(s): {sorted(dup_values)}")
            
            # Convert LIST to DICT
            if isinstance(qre_values.get('codes'), list):
                qre_values['codes'] = {int(i.value): i for i in qre_values.get('codes')}
            
            
            # Auto add data_fields when qtype == 'SA'
            if qre_values.get('qtype') in ['SA'] and qre_values.get('data_fields') is None:
                qre_values['data_fields'] = [qre_values.get('name')]
            
            
            # Auto add data_fields when qtype == 'MA' | 'RANKING'
            if qre_values.get('qtype') in ['MA', 'RANKING'] and qre_values.get('data_fields') is None:
                
                lst_data_fields = list()
                
                for v in qre_values['codes'].values():
                    if isinstance(v, GeneralCode):
                        lst_data_fields.append(f'{qre_values.get('name')}_{int(v.value)}')
                
                qre_values['data_fields'] = list(dict.fromkeys(lst_data_fields))
                
            
            if qre_values.get('other_fields'):
                dup_other_fields = cls.validate_duplicate_other_fields(qre_values.get('other_fields'))
                if dup_other_fields:
                    raise ValueError(f"Error: {qre_values.get('name')} has duplicated other field(s): {sorted(dup_other_fields)}")
        
        
            if qre_values.get('other_fields') and isinstance(qre_values.get('other_fields'), list):
                
                dict_other_fields = dict()
                
                for item in qre_values.get('other_fields'):
                    
                    if not bool(OTHER_PATTERN.match(item.name)):
                        raise ValueError(f"Error: Other fields {item.name} must be in other pattern.")
                    
                    item.is_other_field = True
                    dict_other_fields[item.name] = item

                qre_values['other_fields'] = dict_other_fields

        
        return qre_values
    
    
    
    # -------------------------
    # MODEL VALIDATION ALL QUESTION TYPE
    # -------------------------
    @model_validator(mode='after')
    def validate_qre_fields(self):
        
        
        errs = list()
        
        if self.name is None:
            errs.append('name must not None!')
        
        if self.label is None:
            errs.append('label must not None!')
        
        if self.qtype is None:
            errs.append('qtype must not None!')
        
        if self.data_fields is None:
            errs.append('data_fields must not None!')
        
        # if self.index is None:
        #     errs.append('index must not None!')
        
        if errs:
            raise ValueError('\n'.join(errs))
        
        
        if self.qtype in ['FT', 'NUM', 'SA']: 
            
            if len(self.data_fields) != 1:
                raise ValueError(f"Error: type '{self.qtype}' data_fields must have 1 item.")
            
            if self.name != self.data_fields[0]:
                raise ValueError(f"Error: type '{self.qtype}' question name and data fields must be the same.")

        else:
        
            if len(self.data_fields) == 1:
                raise ValueError(f"Error: '{self.qtype}' data_fields must have more than 1 item.")
        
        
        if self.qtype in ['FT', 'NUM']:
            
            is_ot_pattern = bool(OTHER_PATTERN.match(self.name))
            
            if (self.is_other_field and not is_ot_pattern) or (not self.is_other_field and is_ot_pattern):
                raise ValueError(f"Error: question name '{self.name}' is {'not' if not is_ot_pattern else ''} in other fields pattern but 'is_other_field' is {bool(OTHER_PATTERN.match(self.name))}.")
            
        
        
        if self.qtype in ['SA', 'MA']:
        
            other_codes = {code.value for code in self.codes.values() if isinstance(code, GeneralCode) and code.is_other}
            other_fields_name = {f'{self.name}_o{int(code)}' for code in other_codes}
            
            if self.other_fields is not None or len(other_fields_name) > 0:
                
                other_fields_keys = set(self.other_fields.keys())
            
                missing = sorted(set().union(other_fields_name - other_fields_keys, other_fields_keys - other_fields_name))
                
                if missing:
                    raise ValueError(f'Error: Missing other fields / other codes: {missing}')
            
        
        
        if self.qtype in ['MA']:
            
            general_codes = {code_val for code_val, code in self.codes.items() if isinstance(code, GeneralCode)}
            general_code_data_fields = {f'{self.name}_{int(code)}' for code in general_codes}
            
            missing = sorted(set().union(general_code_data_fields - set(self.data_fields), set(self.data_fields) - general_code_data_fields))
            
            if missing:
                raise ValueError(f"Error: name and data_fields aren't match: {missing}")
        
        
        
        
        
        return self
    
    

class QreFreeText(_QreBase):
    qtype: Literal['FT'] = Field(default='FT')
    is_other_field: bool = False



class QreNumeric(_QreBase):
    qtype: Literal['NUM'] = Field(default='NUM')
    is_other_field: bool = False
    
    

class QreSingleAnswer(_QreBase):
    qtype: Literal['SA'] = Field(default='SA')
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    
    

class QreMultipleAnswer(_QreBase):
    qtype: Literal['MA'] = Field(default='MA')
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    


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



class Attribute(BaseModel):
    value: int
    label: str = Field(min_length=1)
    data_fields: Optional[List[str]] = None
    other_fields: Optional[Dict[str, QreFreeText | QreNumeric]] = None
    


class QreMatrix(_QreBase):
    qtype: Literal['MATRIX'] = Field(default='MATRIX')
    attributes: Dict[str, Attribute]
    sub_qres: Dict[str, MatrixSubQuestion] = Field(default_factory=dict)
    
    
    # HERE: Re-define the structure of matrix
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
