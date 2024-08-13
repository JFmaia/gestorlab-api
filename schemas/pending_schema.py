from typing import Optional, List
from pydantic import BaseModel, UUID4

class PendingSchema(BaseModel):
    id: Optional[UUID4] = None
    id_user: Optional[UUID4] = None
    nome_user: Optional[UUID4] = None
    id_lab: Optional[UUID4] = None
    nome_lab: Optional[UUID4] = None
    id_project: Optional[UUID4] = None
    nome_project: Optional[UUID4] = None
    ativo: Optional[bool] = None
    data_create: Optional[str] = None
    data_atualizacao: Optional[str] = None
    matricula_user: Optional[int] = None

    class Config:
        from_attributes = True

class PendingAccepted(BaseModel):
    id: UUID4
    id_user: Optional[UUID4] = None
    id_lab: Optional[UUID4] = None
    id_project: Optional[UUID4] = None
    id_perm: Optional[UUID4] = None
    list_permissoes: Optional[List[UUID4]] = None