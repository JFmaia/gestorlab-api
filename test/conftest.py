from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
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