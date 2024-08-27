from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from models.genero import Genero
from models.permissao import Permissao
from models.usuario import Usuario
from models.laboratorio import Laboratorio
from models.endereco import Endereco
from models.pending import Pending
from models.permissaoOfLab import PermissaoOfLab
from models.projeto import Projeto
from core.config import settings
from main import app
import pytest
from core.deps import get_session
from core.security import gerar_hash_senha

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Crie um AsyncEngine usando o aiosqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Crie uma função de fábrica de sessão assíncrona
TestingSessionLocal: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine
)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def token(client):
    login_data = {
        "username": "admin@gmail.com",
        "password": "1234"
    }
    response = client.post('/gestorlab/usuarios/login', data=login_data)
    assert response.status_code == 200
    data = response.json()
    token = data.get("access_token")
    assert token is not None
    return token


@pytest.fixture(scope="function")
def db():
    settings.DBBaseModel.metadata.drop_all(bind=engine) 
    settings.DBBaseModel.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Aqui, adicione um teste ou log para verificar se a tabela foi criada
    inspector = inspect(db.bind)
    assert 'laboratorios' in inspector.get_table_names(), "Tabela 'laboratorios' não foi criada"


    # Criação de Gênero
    genero = Genero(title="Masculino")
    db.add(genero)
    db.commit()
    genero_id = genero.id

    # Criação de Permissão Geral
    permissao = Permissao(title="Coordenador")
    db.add(permissao)
    db.commit()
    perm_id = permissao.id

    # Criação de Endereço
    endereco = Endereco(
        logradouro='Rua João Velho de Assis',
        numero=123,
        complemento='Rua da farmácia velha',
        bairro='Monique',
        cidade='São Paulo',
        estado='SP',
        cep=59300000,
        pais='Brasil'
    )
    db.add(endereco)
    db.commit()
    endereco_id = endereco.id

    # Criação de Usuário
    user = Usuario(
        primeiro_nome="User",
        segundo_nome="Admin",
        data_nascimento="08/08/2000",
        ativo=True,
        senha=gerar_hash_senha('1234'),
        id_genero=genero_id,
        id_perm=perm_id,
        email="admin@gmail.com",
        matricula=123131311224,
        tel=84999215902,
        primeiro_acesso=True
    )
    db.add(user)
    db.commit()
    user_id = user.id

    user2 = Usuario(
        primeiro_nome="José",
        segundo_nome="Maia",
        data_nascimento="08/08/2000",
        ativo=True,
        senha=gerar_hash_senha('12345'),
        id_genero=genero_id,
        id_perm=perm_id,
        email="jfmaia@gmail.com",
        matricula=123131311226,
        tel=84999215902,
        primeiro_acesso=True
    )
    db.add(user2)
    db.commit()
    user_id2 = user2.id

    # Criação de Laboratório
    lab = Laboratorio(
        nome="Labens",
        descricao="Muito bom",
        image=None,
        sobre="Laboratório focado em desenvolvimento e estudo de banco de dados!",
        template=1,
        email="labens@gmail.com",
        coordenador_id=user_id,
        endereco_id=endereco_id
    )
    db.add(lab)
    db.commit()
    lab_id = lab.id
    

    # Criação de Permissão Específica de Laboratório
    permissaoOfLab = PermissaoOfLab(title="Coordenador")
    db.add(permissaoOfLab)
    db.commit()
    permLab = permissaoOfLab.id

    project: Projeto = Projeto(
        titulo = "CEXT",
        image = None,
        descricao = "uM BOM PROJETO",
        laboratorio_id= lab_id,
        autor_id = user_id
    )
    db.add(project)
    db.commit()
    project_id = project.id

    pending:Pending = Pending(
        id_user = user_id2,
        id_lab = lab_id,
        matricula_user = user2.matricula
    )

    db.add(pending)
    db.commit()
    pedido_id = pending.id

    yield db, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, user.matricula, user_id2

    db.close()