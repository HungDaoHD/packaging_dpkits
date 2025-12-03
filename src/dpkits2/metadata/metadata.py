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
    data_fields: list[str] = Field(min_length=1)


class QreFreeText(_QreBase):
    qtype: str = 'FT'
    is_other_field: bool = False


class QreNumeric(_QreBase):
    qtype: str = 'NUM'

    
class QreSingleAnswer(_QreBase):
    qtype: str = 'SA'
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[List[str]] = None
    

class QreMultipleAnswer(_QreBase):
    qtype: str = 'MA'
    codes: Dict[int, Union[GeneralCode, NettedCode]]
    other_fields: Optional[List[str]] = None


class QreRanking(_QreBase):
    qtype: str = 'RANKING'
    codes: Dict[int, Union[GeneralCode, NettedCode]]



class QreMatrix(_QreBase):
    qre: Union[QreFreeText, QreNumeric, QreSingleAnswer, QreMultipleAnswer, QreRanking]
    
    

class Metadata(BaseModel):
    qres: Dict[str, Union[QreFreeText, QreNumeric, QreSingleAnswer, QreMultipleAnswer, QreRanking, QreMatrix]] = {}
    lst_qre_simple: List[str] = []
    lst_qre_maxtrix: List[str] = []
    
    


class MetadataBuilder:
    
    def __init__(
        self, df_data: pd.DataFrame, df_info: pd.DataFrame, 
        col_name: str = "Name of items", 
        col_qtype: str = "Question type", 
        col_q_label: str = "Question(Normal)", 
        col_q_matrix: str = "Question(Matrix)"
    ):
        
        self.df_data = df_data
        self.df_info = df_info
        self.col_name = col_name
        self.col_qtype = col_qtype
        self.col_q_label = col_q_label
        self.col_q_matrix = col_q_matrix
        self.code_cols = [c for c in df_info.columns if str(c).isdigit()]

    

    # # -----------------------------
    # # Matrix questions
    # # -----------------------------
    # def _derive_matrix_name(self, first_name: str) -> str:
    #     """
    #     Turn e.g. 'CONSTV_01_1' -> 'CONSTV_01'.
    #     Adjust according to your naming convention.
    #     """
    #     first_name = first_name.strip()
    #     if "_" in first_name:
    #         return first_name.rsplit("_", 1)[0]
    #     return first_name

    
    
    # def _build_matrix_question(self, matrix_text: str, group: pd.DataFrame) -> QreMatrix:
    #     first = group.iloc[0]

    #     first_name = str(first[self.col_name]).strip()
    #     mat_name = self._derive_matrix_name(first_name)

    #     label = self._safe_label(matrix_text, fallback=mat_name)
    #     qtype = str(first[self.col_qtype]).strip()

    #     # Codes often duplicated on every row; first row is enough
    #     codes = self._build_codes_from_row(first)

    #     data_fields = [str(v).strip() for v in group[self.col_name].tolist()]

    #     inner_qre = QreSimple(
    #         name=mat_name,
    #         label=label,
    #         qtype=qtype,
    #         codes=codes,
    #         data_fields=data_fields,
    #     )

    #     return QreMatrix(
    #         name=mat_name,
    #         label=label,
    #         qre=inner_qre,
    #     )

    
    
    # -----------------------------
    # Helpers
    # -----------------------------
    def _safe_label(self, label_raw: str, fallback: str) -> str:
        """
        Make sure label meets min_length requirement of QreSimple.label.
        Adjust / relax this if you change the model constraint.
        """
        label = (label_raw or "").strip()
        if len(label) < 5:
            # simple fallback strategy; feel free to change
            label = fallback if len(fallback) >= 5 else (label or fallback).ljust(5, "_")
        return label
    
    
    
    def _build_codes(self, sr_qre: pd.Series | pd.DataFrame) -> tuple[Dict[int, GeneralCode], list]:
        """
        Read code columns ('1','2',...) from one row and convert them to GeneralCode.
        """
        codes: Dict[int, GeneralCode] = {}
        EXCLKUSIVE = ['NONE', 'REFUSE', 'KHÔNG CÓ', 'KHÔNG BIẾT'] 
        
        other_fields = list()
        
        for col in self.code_cols:
            val = sr_qre.get(col)
            
            # treat NaN / empty as no code
            if isinstance(val, float) and pd.isnull(val):
                continue
            
            if val is None:
                continue
            
            if isinstance(val, str) and not val.strip():
                continue

            code_val = int(col)
            code_lbl = str(val).strip() 
            is_exclusive = True if any(k in code_lbl.upper() for k in EXCLKUSIVE) else False
            
            
            is_other = self.df_info[self.col_name].str.contains(rf"^{sr_qre[self.col_name]}_o{code_val}$", regex=True, case=False, na=False).any()
            
            if is_other:
                other_fields.append(f"{sr_qre[self.col_name]}_o{code_val}")
        
            codes[code_val] = GeneralCode(
                value=code_val,
                label=code_lbl,
                is_exclusive=is_exclusive,
                is_other=is_other
            )
            
            
        
        return codes, other_fields
    
    
    
    def _build_freetext_numeric_question(self, sr_qre: pd.Series) -> QreFreeText | QreNumeric:
        
        name = str(sr_qre[self.col_name]).strip()
        qtype = str(sr_qre[self.col_qtype]).strip()
        label_raw = sr_qre.get(self.col_q_label)
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        
        if qtype == 'FT':
        
            obj_qre = QreFreeText(
                name=name,
                label=label,
                qtype=qtype,
                data_fields=[name],
                is_other_field=re.fullmatch(r"^.+_o\d+$", name) is not None
            )
            
        else:
          
           obj_qre = QreNumeric(
                name=name,
                label=label,
                qtype=qtype,
                data_fields=[name],
            ) 
        
        return obj_qre
    
    
    
    def _build_single_answer_question(self, sr_qre: pd.Series) -> QreSingleAnswer:
        
        name = str(sr_qre[self.col_name]).strip()
        qtype = str(sr_qre[self.col_qtype]).strip()
        label_raw = sr_qre.get(self.col_q_label)
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        codes, other_fields = self._build_codes(sr_qre)

        obj_qre = QreSingleAnswer(
            name=name,
            label=label,
            qtype=qtype,
            codes=codes,
            data_fields=[name],
            other_fields=other_fields if other_fields else None
        )
        
        return obj_qre
    
    
    
    def _build_multiple_answer_question(self, df_qre: pd.Series) -> QreMultipleAnswer:
        
        df_qre = (
            df_qre
            .reset_index(drop=True)
            .dropna(how='all', axis=1)
        )
        
        df_qre[['Name', 'code']] = df_qre[self.col_name].str.rsplit('_', n=1, expand=True)
        
        
        
        name = str(df_qre.loc[0, 'Name']).strip()
        qtype = str(df_qre.loc[0, self.col_qtype]).strip()
        
        
        label_raw = df_qre.loc[0, self.col_q_label]
        label = self._safe_label(label_raw if not pd.isna(label_raw) else "", fallback=name)
        # codes, other_fields = self._build_codes(df_qre)

        obj_qre = QreMultipleAnswer(
            name=name,
            label=label,
            qtype=qtype,
            # codes=codes,
            data_fields=df_qre[self.col_name].values.tolist(),
            # other_fields=other_fields if other_fields else None
        )
                
        # class QreMultipleAnswer(_QreBase):
        # qtype: str = 'MA'
        # codes: Dict[int, Union[GeneralCode, NettedCode]]
        # other_fields: Optional[List[str]] = None

        
        
        return obj_qre

    
    
    # -----------------------------
    # Simple questions (non-matrix)
    # -----------------------------
    def _build_simple_question(self, qre: pd.Series | pd.DataFrame, qtype: str) -> QreFreeText | QreNumeric | QreSingleAnswer | QreMultipleAnswer | QreRanking | QreMatrix:
        
        match qtype:
            case 'FT' | 'NUM':
                return self._build_freetext_numeric_question(qre)
                
            case 'SA':
                return self._build_single_answer_question(qre)
                
            case 'MA':
                return self._build_multiple_answer_question(qre)
            
            case 'RANKING':
                # Tạm
                return self._build_single_answer_question(qre)
                
                
            case _:
                raise ValueError(f"{qre[self.col_name]}: Question type {qtype} is undefined!!!")
    
    
    
    
    
    
    # -----------------------------
    # Public API
    # -----------------------------
    def build(self) -> Metadata:
        
        qres: Dict[str, Union[QreFreeText, QreNumeric, QreSingleAnswer, QreMultipleAnswer, QreRanking, QreMatrix, QreMatrix]] = {}
        matrix_mask = self.df_info[self.col_q_matrix].notna()
        df_simple = self.df_info[~matrix_mask]
        lst_qre_simple = list()
        lst_qre_built = list()
        
        
        for _, sr_qre in df_simple.iterrows():
            
            if sr_qre.get(self.col_name) in lst_qre_built:
                continue
            
            if sr_qre.get(self.col_qtype) == 'MA':                
                ma_mask = df_simple[self.col_name].str.contains(rf"^{sr_qre.get(self.col_name).rsplit('_', 1)[0]}_\d{{1,2}}$", regex=True, case=False, na=False)
                obj_qre = self._build_simple_question(df_simple[ma_mask], sr_qre.get(self.col_qtype))
    
            else:
                obj_qre = self._build_simple_question(sr_qre, sr_qre.get(self.col_qtype))
            
            lst_qre_simple.append(obj_qre.name)
            lst_qre_built.append(sr_qre.get(self.col_name))
            qres[obj_qre.name] = obj_qre
                    
        
        
        # # 1) Build all matrices
        # matrix_df = self.df[matrix_mask]
        # for matrix_text, group in matrix_df.groupby(self.col_q_matrix, sort=False):
        #     q_matrix = self._build_matrix_question(matrix_text, group)
        #     qres[q_matrix.name] = q_matrix

        

        return Metadata(qres=qres, lst_qre_simple=lst_qre_simple)

    
    




    
    
    
    