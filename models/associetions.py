from sqlalchemy import Column, ForeignKey, Table
from core.config import settings
from sqlalchemy_utils import UUIDType

# Tabela de associação muitos para muitos entre Usuario e Laboratorio
usuario_laboratorio_association = Table(
    'usuario_laboratorio',
    settings.DBBaseModel.metadata,
    Column('usuario_id', UUIDType(binary=False), ForeignKey('usuario.id')),
    Column('laboratorio_id', UUIDType(binary=False), ForeignKey('laboratorios.id'))
)

# Tabela de associação muitos para muitos entre Usuario e Projeto
usuario_projeto_association = Table(
    'usuario_projeto',
    settings.DBBaseModel.metadata,
    Column('usuario_id', UUIDType(binary=False), ForeignKey('usuario.id')),
    Column('projeto_id', UUIDType(binary=False), ForeignKey('projetos.id'))
)

laboratorio_projeto_association = Table(
    'laboratorio_projeto',
    settings.DBBaseModel.metadata,
    Column('laboratorio_id', UUIDType(binary=False), ForeignKey('laboratorios.id')),
    Column('projeto_id', UUIDType(binary=False), ForeignKey('projetos.id'))
)

usuario_permission_association = Table(
    'usuario_permissao',
    settings.DBBaseModel.metadata,
    Column('usuario_id', UUIDType(binary=False), ForeignKey('usuario.id')),
    Column('permissao_id', UUIDType(binary=False), ForeignKey('permissao.id'))
)

laboratorio_permission_association = Table(
    'laboratorio_permissao',
    settings.DBBaseModel.metadata,
    Column('laboratorio_id', UUIDType(binary=False), ForeignKey('laboratorios.id')),
    Column('permissao_laboratorio_id', UUIDType(binary=False), ForeignKey('permissao_laboratorio.id'))
)

laboratorio_pending_association = Table(
    'laboratorio_pending',
    settings.DBBaseModel.metadata,
    Column('laboratorio_id', UUIDType(binary=False), ForeignKey('laboratorios.id')),
    Column('pending_id', UUIDType(binary=False), ForeignKey('pendings.id'))
)

usuario_pending_association = Table(
    'usuario_pending',
    settings.DBBaseModel.metadata,
    Column('usuario_id', UUIDType(binary=False), ForeignKey('usuario.id')),
    Column('pending_id', UUIDType(binary=False), ForeignKey('pendings.id'))
)