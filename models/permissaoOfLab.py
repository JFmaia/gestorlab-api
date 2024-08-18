import uuid
from sqlalchemy import Column, String
from core.config import settings
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

class PermissaoOfLab(settings.DBBaseModel):
  __tablename__ = 'permissaoOfLabs'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  title = Column(String(256), nullable=False)
  perm = relationship('PermissaoLab', back_populates='permissao')