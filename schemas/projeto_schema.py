from typing import Optional, List
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict
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

class LaboratorioProjeto(BaseModel):
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

class ProjetoSchemaCreate(BaseModel):
    titulo: str
    image: Optional[str] = None
    descricao: str
    laboratorio_id: UUID4

class ProjetoSchemaUp(BaseModel):
    titulo: Optional[str] = None
    image: Optional[str] = None
    descricao: Optional[str] = None

class ProjetoSchemaAddMember(BaseModel):
    idProjeto: str
    idUsuario: str
class ProjetoSchema(BaseModel):
    id: Optional[UUID4] = None 
    titulo: str
    descricao: str
    laboratorio_id: Optional[UUID4] = None 
    image: Optional[str] = None
    autor_id: Optional[UUID4] = None 
    data_inicial: datetime
    data_up: datetime
    membros: Optional[List[User]] = None
    laboratorio: Optional[LaboratorioProjeto] = None

    model_config = ConfigDict(
        from_attributes=True
    )