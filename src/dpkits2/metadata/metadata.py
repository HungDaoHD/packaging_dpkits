from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator  # , computed_field, EmailStr
from typing import Union, Optional, Literal, Dict, List, Annotated
import pandas as pd
import re



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
    other_fields: Optional[Dict[str, QreFreeText]] = None
    

class QreMultipleAnswer(_QreBase):
    qtype: Literal['MA']
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[Dict[str, QreFreeText]] = None


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



class Metadata(BaseModel):
    qres: Dict[str, Question] = Field(default_factory=dict)
    lst_qre_simple: List[str] = Field(default_factory=list)
    lst_qre_matrix: List[str] = Field(default_factory=list)
    
    model_config = {
        'arbitrary_types_allowed': True
    }
    
    
    def sort_qres_by_index(self):
        sorted_items = sorted(
            self.qres.items(),
            key=lambda item: item[1].index,  # item = (key, Question)
        )
        
        self.qres = dict(sorted_items)
        return self
        
    
    
    def to_json(self, indent: int = 4):
        return self.model_dump_json(indent=indent)
    
    
    def save_json(self, filepath: str, indent: int = 4):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=indent))
    
    
    @classmethod
    def from_json(cls, json_str: str) -> "Metadata":
        """Create a Metadata instance from a JSON string."""
        return cls.model_validate_json(json_str)

    
    @classmethod
    def from_json_file(cls, filepath: str) -> "Metadata":
        """Create a Metadata instance from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            json_str = f.read()
        
        return cls.model_validate_json(json_str)


class MetadataBuilder:
    
    def __init__(
        self, df_data: pd.DataFrame, df_info: pd.DataFrame, 
        col_name: str = 'Name of items', 
        col_qtype: str = 'Question type', 
        col_q_label: str = 'Question(Normal)', 
        col_q_matrix_label: str = 'Question(Matrix)',
        col_q_simple_group: str = 'Qre_Simple_Group',
        col_q_matrix_group: str = 'Qre_Matrix_Group',
    ):
        
        self.df_data = df_data
        self.df_info = df_info
          
        self.col_name = col_name
        self.col_qtype = col_qtype
        self.col_q_label = col_q_label
        self.col_q_matrix_label = col_q_matrix_label
        self.col_q_simple_group = col_q_simple_group
        self.col_q_matrix_group = col_q_matrix_group
        self.prop_cols = [col_name, col_qtype, col_q_label, col_q_matrix_label, col_q_simple_group, col_q_matrix_group]
        self.code_cols = [c for c in df_info.columns if str(c).isdigit()]
        
        
        
    
    # -----------------------------
    # Helpers
    # -----------------------------
    def _safe_label(self, label_raw: str, fallback: str) -> str:
        """
        Make sure label meets min_length requirement of QreSimple.label.
        Adjust / relax this if you change the model constraint.
        """
        min_lenght = 2
        
        label = (label_raw or "").strip()
        if len(label) < min_lenght:
            # simple fallback strategy; feel free to change
            label = fallback if len(fallback) >= min_lenght else (label or fallback).ljust(min_lenght, "_")
        return label
    
    
    
    def _build_codes(self, qre: pd.DataFrame, other_fields: list) -> tuple[Dict[int, GeneralCode], list]:
        
        EXCLKUSIVE = ['NONE', 'REFUSE', 'KHÔNG CÓ', 'KHÔNG BIẾT']
        codes: Dict[int, GeneralCode] = {}
        qtype = qre[self.col_qtype].values[0]
        
        if qtype in ['SA', 'RANKING']:
            sr_codes_only = qre.drop(columns=self.prop_cols + ['prefix', 'code'], errors='ignore').T.squeeze()
            col_prefix = qre[self.col_name].values[0]
            
        else:
            sr_codes_only = (
                qre[['code', 'label']]
                .set_index('code', drop=True)
                .squeeze()
            )
            col_prefix = qre['prefix'].values[0]
            
            
        
        for code, label in sr_codes_only.items():
            
            code_val = int(code)
            code_lbl = str(label).strip()
            
            is_exclusive = True if any(k in code_lbl.upper() for k in EXCLKUSIVE) else False
            is_other = True if other_fields and f"{col_prefix}_o{code_val}" in other_fields else False
            
            
            codes[code_val] = GeneralCode(
                value=code_val,
                label=code_lbl,
                is_exclusive=is_exclusive,
                is_other=is_other
            )

        
        return codes
    
    
    
    def _build_freetext_numeric_question(self, qre: pd.DataFrame) -> QreFreeText | QreNumeric:
        
        sr_qre = qre.squeeze()
        
        name = str(sr_qre[self.col_name]).strip()
        qtype = str(sr_qre[self.col_qtype]).strip()
        label_raw = sr_qre.get(self.col_q_label)
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        index = sr_qre.name
        
        
        if qtype == 'FT':
        
            obj_qre = QreFreeText(
                name=name,
                label=label,
                qtype=qtype,
                index=index,
                data_fields=[name],
                is_other_field=re.fullmatch(r"^.+_o\d+$", name) is not None
            )
            
        else:
          
           obj_qre = QreNumeric(
                name=name,
                label=label,
                qtype=qtype,
                index=index,
                data_fields=[name]
            ) 
        
        return obj_qre
    
    
    
    def _build_single_answer_question(self, qre: pd.DataFrame) -> QreSingleAnswer:
        
        df_qre = qre.loc[qre[self.col_qtype] == 'SA']
        df_other = qre.loc[qre[self.col_qtype] == 'FT']
        
        index = df_qre.index[0]
        
        name = str(df_qre.loc[index, self.col_name]).strip()
        qtype = str(df_qre.loc[index, self.col_qtype]).strip()
        label_raw = df_qre.loc[index, self.col_q_label]
        
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        codes = self._build_codes(df_qre, other_fields=df_other[self.col_name].to_list() if not df_other.empty else [])
        
        obj_others = dict()
        if not df_other.empty:
            for _, qre_other in df_other.iterrows():
                obj_other = self._build_simple_question(qre_other.to_frame(), 'FT')
                obj_others[obj_other.name] = obj_other
        
        
        obj_qre = QreSingleAnswer(
            name=name,
            label=label,
            qtype=qtype,
            codes=codes,
            index=index,
            data_fields=[name],
            other_fields=obj_others if obj_others else None
        )
        
        return obj_qre
    
    
    
    def _build_multiple_answer_question(self, qre: pd.DataFrame) -> QreMultipleAnswer:
        
        index = qre.index[0]
        lst_col_splited = ['prefix', 'code']
        
        df_qre = (
            qre
            .loc[qre[self.col_qtype] == 'MA']
            .rename(columns={1: 'label'})
        )
        df_qre[lst_col_splited] = df_qre[self.col_name].str.rsplit('_', n=1, expand=True)
        
        df_other = qre.loc[qre[self.col_qtype] == 'FT']
        if not df_other.empty:
            df_other.loc[:, lst_col_splited] = df_other[self.col_name].str.rsplit('_', n=1, expand=True)
            
        name = str(df_qre.loc[index, lst_col_splited[0]]).strip()
        qtype = str(df_qre.loc[index, self.col_qtype]).strip()
        label_raw = df_qre.loc[index, self.col_q_label]

        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        codes = self._build_codes(df_qre, other_fields=df_other[self.col_name].to_list() if not df_other.empty else [])
        
        obj_others = dict()
        if not df_other.empty:
            for _, qre_other in df_other.iterrows():
                obj_other = self._build_simple_question(qre_other.to_frame(), 'FT')
                obj_others[obj_other.name] = obj_other
        
        obj_qre = QreMultipleAnswer(
            name=name,
            label=label,
            qtype=qtype,
            codes=codes,
            index=index,
            data_fields=df_qre[self.col_name].values.tolist(),
            other_fields=obj_others if obj_others else None 
        )
        
        return obj_qre

    
    
    def _build_ranking_question(self, qre: pd.DataFrame) -> QreMultipleAnswer:
        
        index = qre.index[0]
        lst_col_splited = ['prefix', 'code']
        df_qre = qre.loc[qre[self.col_qtype] == 'RANKING']
        df_qre[lst_col_splited] = df_qre[self.col_name].str.rsplit('_', n=1, expand=True)
        
        name = str(df_qre.loc[index, lst_col_splited[0]]).strip()
        qtype = str(df_qre.loc[index, self.col_qtype]).strip()
        label_raw = df_qre.loc[index, self.col_q_label]
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        
        codes = self._build_codes(df_qre.loc[index, :].to_frame().T, other_fields=[])
        
        obj_qre = QreRanking(
            name=name,
            label=label,
            qtype=qtype,
            codes=codes,
            index=index,
            data_fields=df_qre[self.col_name].values.tolist(),
            other_fields=None
        )
        
        return obj_qre
    
    
    
    # -----------------------------
    # Simple questions (non-matrix)
    # -----------------------------
    def _build_simple_question(self, df_qre: pd.DataFrame, qtype: str) -> QreFreeText | QreNumeric | QreSingleAnswer | QreMultipleAnswer | QreRanking:
        
        df_qre = df_qre.dropna(how='all', axis=1)
        
        match qtype:
            case 'FT' | 'NUM':
                return self._build_freetext_numeric_question(df_qre)
                
            case 'SA':
                return self._build_single_answer_question(df_qre)
                
            case 'MA':
                return self._build_multiple_answer_question(df_qre)
            
            case 'RANKING':
                return self._build_ranking_question(df_qre)
            
            case _:
                raise ValueError(f"{df_qre[self.col_name]}: Question type {qtype} is undefined!!!")
    
    
    # -----------------------------
    # Matrix questions
    # -----------------------------
    def _build_matrix_question(self, qre_grp: str, df_qre: pd.DataFrame, ) -> QreMatrix:
        
        df_qre = df_qre.dropna(how='all', axis=1)
        index = df_qre.index[0]
        
        obj_sub_qres = {}
        
        for _, df_sub_qre in df_qre.groupby(self.col_q_simple_group, sort=False):
            
            obj_sub_qre = self._build_simple_question(df_sub_qre, df_sub_qre[self.col_qtype].values[0])
            obj_sub_qres[obj_sub_qre.name] = obj_sub_qre
            print(f'Metadata: Matrix sub-question {obj_sub_qre.name} was built.')
        
        
        obj_matrix = QreMatrix(
            name=qre_grp,
            label=df_qre.loc[index, self.col_q_matrix_label],
            qtype='MATRIX',
            index=index,
            data_fields=df_qre[self.col_name].values.tolist(),
            sub_qres=obj_sub_qres
        )
    

        return obj_matrix
    
    
    
    # -----------------------------
    # Public API
    # -----------------------------
    def build(self) -> Metadata:
         
        qres: Dict[str, Union[QreFreeText, QreNumeric, QreSingleAnswer, QreMultipleAnswer, QreRanking, QreMatrix, QreMatrix]] = {}
        
        matrix_mask = self.df_info[self.col_q_matrix_group].notna()
        df_simple = self.df_info[~matrix_mask]
        df_matrix = self.df_info[matrix_mask]
        
        lst_qre_simple = list()
        lst_qre_matrix = list()
        
        
        # Build matrix questions from qme dataframe to pydantic model
        for qre_grp, df_qre in df_matrix.groupby(self.col_q_matrix_group, sort=False):
            
            obj_qre = self._build_matrix_question(qre_grp, df_qre)
            lst_qre_matrix.append(obj_qre.name)
            qres[obj_qre.name] = obj_qre
            print(f'Metadata: Matrix question {qre_grp} was built.')
            
        
        # Build simple questions from qme dataframe to pydantic model
        for qre_grp, df_qre in df_simple.groupby(self.col_q_simple_group, sort=False):
            
            obj_qre = self._build_simple_question(df_qre, df_qre[self.col_qtype].values[0])
            lst_qre_simple.append(obj_qre.name)
            qres[obj_qre.name] = obj_qre
            print(f'Metadata: Simple question {obj_qre.name} was built.')
            
        
        return Metadata(qres=qres, lst_qre_simple=lst_qre_simple, lst_qre_matrix=lst_qre_matrix).sort_qres_by_index()

    





    
    
    
    