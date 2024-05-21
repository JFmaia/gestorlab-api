import uuid
from datetime import datetime
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from core.config import settings
from sqlalchemy_utils import UUIDType
from models.associetions import usuario_projeto_association, laboratorio_projeto_association
class Projeto(settings.DBBaseModel):
    __tablename__ = 'projetos'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(256), unique=True, nullable=False)
    descricao = Column(String(5000), nullable=True)
    lab_creator= Column(UUIDType(binary=False), ForeignKey("laboratorios.id"), nullable=False)
    autor_id = Column(UUIDType(binary=False), ForeignKey("usuario.id"), nullable=False)
    data_inicial = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    data_up = Column(String(256), default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), nullable=False)
    autor = relationship("Usuario", back_populates='projetos', lazy='joined')
    membros = relationship(
        "Usuario",
        secondary=usuario_projeto_association,
        back_populates="projetos",
        lazy="joined"
    )
    laboratorios = relationship(
        "Laboratorio",
        secondary=laboratorio_projeto_association,
        back_populates="projetos",
        lazy="joined"
    )