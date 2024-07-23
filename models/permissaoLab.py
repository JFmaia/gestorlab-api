import uuid
from sqlalchemy import Column, String
from core.config import settings
from sqlalchemy_utils import UUIDType

class PermissaoOfLab(settings.DBBaseModel):
  __tablename__ = 'permissaooflab'

  id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
  title = Column(String(256), nullable=False)