from typing import Optional, List
from pydantic import BaseModel, UUID4

class PendingSchema(BaseModel):
    id: Optional[UUID4] = None
    id_user: Optional[UUID4] = None
    ativo: Optional[bool] = None
    data_create: Optional[str] = None
    data_atualizacao: Optional[str] = None
    matricula_user: int

    class Config:
        from_attributes = True

class PendingAccepted(BaseModel):
    id: UUID4
    id_user: UUID4
    list_permissoes: List[UUID4]