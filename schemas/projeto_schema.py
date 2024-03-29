from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime

class ProjetoSchema(BaseModel):
    id: Optional[UUID4] = None 
    titulo: str
    descricao: str
    autor_id: Optional[UUID4] = None 
    data_inicial: datetime
    data_up: datetime
    mebros: Optional[List[str]] = None

    class Config:
        from_attributes = True

class ProjetoSchemaCreate(BaseModel):
    titulo: str
    descricao: str
    membros: Optional[List[UUID4]] = None

class ProjetoSchemaUp(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    membros: Optional[List[UUID4]] = None