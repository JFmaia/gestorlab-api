from typing import Optional, List 
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict
from schemas.permissao_schema import PermissaoSchema
from schemas.genero_schema import GeneroSchema
from schemas.pending_schema import PendingSchema
from datetime import datetime
class User(BaseModel):
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
class LaboratorioEndereco(BaseModel):
    id: Optional[UUID4] = None
    logradouro: str
    numero:int
    complemento:str
    bairro:str
    cidade:str
    estado:str
    cep:int
    pais:str
    data_inicial:Optional[datetime] = None
    data_up:Optional[datetime] = None

class Projeto(BaseModel):
    id: Optional[UUID4] = None 
    titulo: str
    descricao: str
    laboratorio_id: Optional[UUID4] = None 
    image: Optional[str] = None
    autor_id: Optional[UUID4] = None 
    data_inicial: datetime
    data_up: datetime
    membros: Optional[List[User]] = None
class Laboratorio(BaseModel):
    id: Optional[UUID4] = None 
    coordenador_id: Optional[UUID4] = None 
    nome: str
    sobre: str
    template: int
    descricao: str
    email: EmailStr
    data_inicial: Optional[datetime] = None 
    data_up: Optional[datetime] = None
    endereco_id: Optional[UUID4] = None
    coordenador: User
    endereco: Optional[LaboratorioEndereco]= None
    image: Optional[str] = None
    projetos: Optional[List[Projeto]] = None

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
    laboratorios: Optional[List[Laboratorio]] = None
    projetos: Optional[List[Projeto]] = None
    image: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True
    )

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