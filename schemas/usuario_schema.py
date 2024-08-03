
from typing import Optional, List 
from pydantic import BaseModel, EmailStr, UUID4
from schemas.permissao_schema import PermissaoSchema
from .pending_schema import PendingSchema

class UsuarioSchemaBase(BaseModel):
    id: Optional[UUID4] = None 
    data_inicial: Optional[str] = None
    data_atualizacao: Optional[str] = None
    primeiro_acesso: Optional[bool] = None
    ativo: Optional[bool] = None
    primeiro_nome: str
    image: Optional[str] = None
    segundo_nome: str
    data_nascimento: str
    genero: UUID4
    email: EmailStr
    matricula: int
    tel: int
    permissoes: Optional[List[PermissaoSchema]] = None
    lista_pending: Optional[List[PendingSchema]] = None

class Config:
    from_attributes = True

from schemas.laboratorio_schema import LaboratorioSchema
from schemas.projeto_schema import ProjetoSchema

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

class UsuarioSchemaAddLaboratorio(UsuarioSchemaBase):
    list_laboratorios: List[UUID4]
class UsuarioSchemaAddProjeto(UsuarioSchemaBase):
    list_Projetos: List[UUID4]
class UsuarioSchemaLaboratoriosAndProjetos(UsuarioSchemaBase):
    laboratorios: Optional[List[LaboratorioSchema]]
    projetos: Optional[List[ProjetoSchema]]

class UsuarioSchemaUp(UsuarioSchemaBase):
    primeiro_nome: Optional[str]
    segundo_nome: Optional[str] 
    senha: Optional[str]
    email: Optional[EmailStr]
    matricula: Optional[int]
    genero: Optional[UUID4]
    tel: Optional[int]
    list_permissoes: Optional[List[UUID4]] = None
    image: Optional[str] = None

class SendEmail(BaseModel):
    email: str

class RecoveryPassword(BaseModel):
    id_user: UUID4
    senha: str