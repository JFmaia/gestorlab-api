from typing import Optional, List
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict
from datetime import datetime
from schemas.pending_schema import PendingSchema
from schemas.endereco_schema import EnderecoSchema
from schemas.permissaoLab_schema import PermissaoSchema
class PermissaoLaboratorioResponse(BaseModel):
    id_lab: Optional[UUID4] = None 
    id: Optional[UUID4] = None 
    id_user: Optional[UUID4] = None 
    id_perm: Optional[UUID4] = None 
    permissao: Optional[PermissaoSchema] = None

class PermissaoLaboratorioCreate(BaseModel):
    id_user: UUID4
    id_lab: UUID4
    perm_id: UUID4

class Member(BaseModel):
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
    image: Optional[str] = None

class LaboratorioSchemaCreate(BaseModel):
    nome: str
    descricao: str
    sobre: str
    template: int
    email: EmailStr
    image: Optional[str] = None
    endereco: Optional[EnderecoSchema]=None

class LaboratorioSchemaUp(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    sobre: Optional[str] = None
    template: Optional[int] = None
    email: Optional[EmailStr] = None
    image: Optional[str] = None

class LaboratorioSchemaAddMember(BaseModel):
    idLaboratorio: UUID4
    idUser: UUID4
    perm_id: UUID4

class LaboratorioSchemaAddProjeto(BaseModel):
    id_projeto: str

class PermissaoLaboratorioUp(BaseModel):
    id: UUID4
    id_lab: UUID4
    perm_id: UUID4

class Projeto(BaseModel):
    id: Optional[UUID4] = None 
    titulo: str
    descricao: str
    laboratorio_id: Optional[UUID4] = None 
    image: Optional[str] = None
    autor_id: Optional[UUID4] = None 
    data_inicial: datetime
    data_up: datetime
    membros: Optional[List[Member]] = None

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
    membros: Optional[List[Member]] = None
    permissoes: Optional[List[PermissaoLaboratorioResponse]] = None
    pedidos: Optional[List[PendingSchema]] = None
    endereco_id: Optional[UUID4] = None 
    endereco: Optional[EnderecoSchema]= None
    coordenador: Member
    projetos: Optional[List[Projeto]]= None
    image: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )