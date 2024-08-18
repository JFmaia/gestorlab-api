import uuid
from sqlalchemy import Column, String
from core.config import settings
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

class Genero(settings.DBBaseModel):
  __tablename__ = 'generos'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  title = Column(String(256), nullable=False)
  usuario = relationship('Usuario', back_populates='genero')