import uuid
from sqlalchemy import Column, ForeignKey
from core.config import settings
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

class PermissaoLab(settings.DBBaseModel):
    __tablename__ = 'permissaoLabs'

    id_lab = Column(UUIDType(binary=False), ForeignKey('laboratorios.id'), nullable=True)
    laboratorio = relationship('Laboratorio', back_populates='permissoes')
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUIDType(binary=False), nullable=False)
    id_perm = Column(UUIDType(binary=False), ForeignKey('permissaoOfLabs.id'), nullable=False)
    permissao = relationship('PermissaoOfLab', back_populates='perm')