import uuid
from sqlalchemy import Column, Boolean, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.config import settings
from sqlalchemy_utils import UUIDType
from datetime import datetime

class Pending(settings.DBBaseModel):
  __tablename__ = 'pedidos'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  id_user = Column(UUIDType(binary=False), ForeignKey('usuario.id'), nullable=True)
  usuario = relationship('Usuario', back_populates='pedidos')
  id_lab = Column(UUIDType(binary=False), ForeignKey('laboratorios.id'), nullable=True)
  laboratorio = relationship('Laboratorio', back_populates='pedidos')
  ativo = Column(Boolean(True),nullable=False, default=True)
  data_create = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
  data_atualizacao = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
  matricula_user = Column(BigInteger, nullable=True, unique=True)