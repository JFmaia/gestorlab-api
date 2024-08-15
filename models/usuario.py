import uuid
from datetime import datetime
from sqlalchemy import BigInteger, String, Column, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.config import settings
from sqlalchemy_utils import UUIDType
from models.associetions import usuario_laboratorio_association, usuario_projeto_association
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
    )
    projetos = relationship(
        "Projeto",
        secondary=usuario_projeto_association,
        back_populates="membros",
    )
    id_perm = Column(UUIDType(binary=False), ForeignKey('permissao.id'), nullable=True)
    permissao = relationship('Permissao', back_populates='usuario')
    pedidos =relationship('Pending', back_populates='usuario')
    id_genero = Column(UUIDType(binary=False), ForeignKey("generos.id"), nullable=False)
    genero= relationship('Genero', back_populates='usuario')
    data_inicial = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    data_nascimento = Column(String(256), nullable=False)
    data_atualizacao = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)