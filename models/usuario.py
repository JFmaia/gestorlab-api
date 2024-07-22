import uuid
from datetime import datetime
from sqlalchemy import BigInteger, String, Column, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.config import settings
from sqlalchemy_utils import UUIDType
from models.associetions import usuario_laboratorio_association, usuario_projeto_association, usuario_permission_association, usuario_pending_association
class Usuario(settings.DBBaseModel):
    __tablename__ = 'usuario'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    primeiro_nome = Column(String(256), nullable=False)
    image =  Column(Text, nullable=True)
    segundo_nome = Column(String(256), nullable=False)
    primeiro_acesso = Column(Boolean(), nullable=False)
    ativo = Column(Boolean(True), nullable=False, default=False)
    matricula = Column(BigInteger, nullable=False, unique=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    tel = Column(BigInteger, nullable=True)
    senha = Column(String(256), nullable=False)
    laboratorios = relationship(
        "Laboratorio",
        secondary=usuario_laboratorio_association,
        back_populates="membros",
        lazy="joined"
    )
    projetos = relationship(
        "Projeto",
        secondary=usuario_projeto_association,
        back_populates="membros",
        lazy="joined"
    )
    permissoes = relationship(
        "Permissao",
        secondary=usuario_permission_association,
        lazy="joined"
    )
    lista_pending = relationship(
        "Pending",
        secondary= usuario_pending_association,
        lazy="joined"
    )
    genero = Column(UUIDType(binary=False), ForeignKey("generos.id"), nullable=False)
    data_inicial = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    data_nascimento = Column(String(256), nullable=False)
    data_atualizacao = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)