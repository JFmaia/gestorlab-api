from typing import Optional
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

class Endereco(BaseModel):
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
    coordenador:  Optional[User]= None
    endereco: Optional[Endereco]= None
    image: Optional[str] = None

class PendingSchema(BaseModel):
    id: Optional[UUID4] = None
    id_user: Optional[UUID4] = None
    usuario: Optional[User] = None
    id_lab: Optional[UUID4] = None
    laboratorio: Optional[Laboratorio] = None
    ativo: Optional[bool] = None
    data_create: Optional[str] = None
    data_atualizacao: Optional[str] = None
    matricula_user: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )

class PendingAccepted(BaseModel):
    id: UUID4
    id_user: Optional[UUID4] = None
    id_lab: Optional[UUID4] = None
    id_perm: UUID4