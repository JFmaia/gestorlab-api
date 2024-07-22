from typing import Optional, List
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from .usuario_schema import UsuarioSchemaBase
from .projeto_schema import ProjetoSchema
from .pending_schema import PendingSchema

class PermissaoLaboratorioResponse(BaseModel):
    id: UUID4
    id_user: UUID4
    id_lab: UUID4
    perm_id: UUID4

class PermissaoLaboratorioCreate(BaseModel):
    id_user: UUID4
    id_lab: UUID4
    perm_id: UUID4

class LaboratorioSchema(BaseModel):
    id: Optional[UUID4] = None 
    coordenador_id: Optional[UUID4] = None 
    nome: str
    sobre: str
    template: int
    descricao: str
    image: Optional[str] = None
    email: EmailStr
    data_inicial: Optional[datetime] = None 
    data_up: Optional[datetime] = None
    membros: Optional[List[UsuarioSchemaBase]] = None
    projetos: Optional[List[ProjetoSchema]] = None
    lista_perm: Optional[List[PermissaoLaboratorioResponse]] = None
    lista_acess: Optional[List[PendingSchema]] = None

    class Config:
        from_attributes = True

class LaboratorioSchemaCreate(BaseModel):
    nome: str
    descricao: str
    sobre: str
    template: int
    email: EmailStr
    image: Optional[str] = None

class LaboratorioSchemaUp(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sobre: Optional[str] = None
    template: Optional[int] = None
    email: Optional[EmailStr] = None
    image: Optional[str] = None

class LaboratorioSchemaAddMember(BaseModel):
    idLaboratorio: str
    idUser: str

class LaboratorioSchemaAddProjeto(BaseModel):
    id_projeto: str

class PermissaoLaboratorioUp(BaseModel):
    id: UUID4
    id_lab: UUID4
    perm_id: UUID4