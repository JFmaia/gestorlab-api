from typing import Optional, List
from pydantic import BaseModel, UUID4,EmailStr
from datetime import datetime
from .usuario_schema import UsuarioSchemaBase

class ProjetoSchema(BaseModel):
    id: Optional[UUID4] = None 
    titulo: str
    descricao: str
    autor_id: Optional[UUID4] = None 
    data_inicial: datetime
    data_up: datetime
    membros: Optional[List[UsuarioSchemaBase]] = None

    class Config:
        from_attributes = True

class ProjetoSchemaCreate(BaseModel):
    titulo: str
    descricao: str
    labCreator: str

class ProjetoSchemaUp(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None

class ProjetoSchemaAddMember(BaseModel):
    id_projeto: str
    email_user: EmailStr