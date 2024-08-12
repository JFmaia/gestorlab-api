from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models.genero import Genero
from models.usuario import Usuario
from models.laboratorio import Laboratorio
from models.projeto import Projeto
from core.config import settings
from main import app
import pytest
from core.deps import get_session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use o prefixo 'sqlite+aiosqlite://' para indicar o uso do aiosqlite

# Crie um AsyncEngine usando o aiosqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Crie uma função de fábrica de sessão assíncrona
TestingSessionLocal: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine
)
settings.DBBaseModel.metadata.drop_all(bind=engine)
settings.DBBaseModel.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def db():
    db = TestingSessionLocal()

    genero = Genero(
        title="Coodernador"
    )

    db.add(genero)
    db.commit()
    genero_id = genero.id

    # Cria um usuário
    user = Usuario(
        primeiro_nome="User",
        segundo_nome="Admin",
        data_nascimento="08/08/2000",
        senha="1234",
        genero= genero_id,
        email="admin@gmail.com",
        matricula=123131311224,
        tel=84999215902,
        primeiro_acesso=True
    )

    db.add(user)
    db.commit()
    user_id = user.id

    # Cria um laboratório
    lab = Laboratorio(
        nome="Labens3",
        descricao="Muito bom",
        image= None,
        sobre="gosto daqui",
        template=1,
        email="labens4@gmail.com",
        coordenador_id=user_id,
        membros=[]
    )
    db.add(lab)
    db.commit()
    lab_id = lab.id

    # Cria um projeto associado ao usuário e ao laboratório
    project = Projeto(
        autor_id=user_id,
        image= None,
        lab_creator= lab_id,
        titulo='My Projeto',
        descricao='Tudo bom'
    )
    db.add(project)
    db.commit()
    project_id = project.id

    yield db, user_id, lab_id, project_id

    db.close()