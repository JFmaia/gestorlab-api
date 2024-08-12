import uuid
from sqlalchemy import Column, ForeignKey
from core.config import settings
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

class PermissaoLaboratorio(settings.DBBaseModel):
    __tablename__ = 'permissao_laboratorio'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUIDType(binary=False), nullable=False)
    id_lab = Column(UUIDType(binary=False), nullable=False)
    perm_id = Column(UUIDType(binary=False), nullable=False)