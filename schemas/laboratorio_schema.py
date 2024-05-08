from typing import Optional, List
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from .usuario_schema import UsuarioSchemaBase

class LaboratorioSchema(BaseModel):
    id: Optional[UUID4] = None 
    coordenador_id: Optional[UUID4] = None 
    nome: str
    sobre: str
    template: int
    descricao: str
    email: EmailStr
    data_inicial: Optional[datetime] = None 
    data_up: Optional[datetime] = None
    membros: Optional[List[UsuarioSchemaBase]] = None

    class Config:
        from_attributes = True

class LaboratorioSchemaCreate(BaseModel):
    nome: str
    descricao: str
    sobre: str
    template: int
    email: EmailStr

class LaboratorioSchemaUp(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sobre: Optional[str] = None
    template: Optional[int] = None
    email: Optional[EmailStr] = None

class LaboratorioSchemaAddMember(BaseModel):
    id_laboratorio: str
    email_user: EmailStr