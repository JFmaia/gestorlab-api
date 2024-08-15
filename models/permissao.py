import uuid
from sqlalchemy import Column, String
from core.config import settings
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

class Permissao(settings.DBBaseModel):
  __tablename__ = 'permissao'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  title = Column(String(256), nullable=False)
  usuario = relationship('Usuario', back_populates='permissao')