from core.config import settings
from datetime import datetime
from sqlalchemy import String, Column, Integer
from sqlalchemy_utils import UUIDType
import uuid
class Endereco(settings.DBBaseModel):
  __tablename__ = 'enderecos'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  logradouro = Column(String(256), nullable=False)
  numero= Column(Integer(), nullable=False)
  complemento = Column(String(256), nullable=True)
  bairro = Column(String(256), nullable=True)
  cidade = Column(String(256), nullable=True)
  estado = Column(String(256), nullable=True)
  cep = Column(Integer(), nullable=True)
  pais = Column(String(256), nullable=True)
  data_inicial = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
  data_up = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)



  