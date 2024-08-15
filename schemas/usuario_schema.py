from typing import Optional, List 
from pydantic import BaseModel, EmailStr, UUID4
from schemas.permissao_schema import PermissaoSchema
from schemas.genero_schema import GeneroSchema
from schemas.pending_schema import PendingSchema
class UsuarioSchemaBase(BaseModel):
    id: Optional[UUID4] = None 
    data_inicial: Optional[str] = None
    data_atualizacao: Optional[str] = None
    primeiro_acesso: Optional[bool] = None
    ativo: Optional[bool] = None
    primeiro_nome: str
    segundo_nome: str
    data_nascimento: str
    email: EmailStr
    matricula: int
    tel: int
    id_genero: Optional[UUID4] = None 
    genero: Optional[GeneroSchema] = None
    id_perm: Optional[UUID4] = None 
    permissao: Optional[PermissaoSchema] = None
    pedidos: Optional[List[PendingSchema]] = None
    image: Optional[str] = None
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
    primeiro_nome: Optional[str] = None
    segundo_nome: Optional[str] = None
    senha: Optional[str] = None
    email: Optional[EmailStr] = None
    matricula: Optional[int] = None
    id_genero: Optional[UUID4] = None
    tel: Optional[int] = None
    id_perm: Optional[UUID4] = None
    image: Optional[str] = None

class SendEmail(BaseModel):
    email: str

class RecoveryPassword(BaseModel):
    id_user: UUID4
    senha: str