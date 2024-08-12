import uuid
from datetime import datetime
from sqlalchemy import String, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from core.config import settings
from sqlalchemy_utils import UUIDType
from models.associetions import usuario_laboratorio_association, laboratorio_projeto_association, laboratorio_permission_association, laboratorio_pending_association

class Laboratorio(settings.DBBaseModel):
    __tablename__ = 'laboratorios'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    coordenador_id = Column(UUIDType(binary=False), ForeignKey("usuario.id"), nullable=False)
    nome = Column(String(256), nullable=False)
    sobre = Column(String(10000), nullable=False)
    image =  Column(Text, nullable=True)
    descricao = Column(String(5000), nullable=True)
    email = Column(String(256), unique=True, nullable=True)
    data_inicial = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    data_up = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    coordenador = relationship("Usuario", back_populates='laboratorios', lazy='joined')
    membros = relationship(
        "Usuario",
        secondary=usuario_laboratorio_association,
        back_populates="laboratorios",
        lazy="joined"
    )
    projetos = relationship(
        "Projeto",
        secondary=laboratorio_projeto_association,
        back_populates="laboratorios",
        lazy="joined"
    )
    lista_perm = relationship(
        "PermissaoLaboratorio",
        secondary=laboratorio_permission_association,
        lazy="joined"
    )
    lista_acess = relationship(
        "Pending",
        secondary=laboratorio_pending_association,
        lazy="joined"
    )
    template = Column(Integer, nullable=False)
    endereco_id = Column(UUIDType(binary=False), ForeignKey("enderecos.id"), nullable=True) 
    endereco = relationship("Endereco", lazy='joined')
