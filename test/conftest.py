from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.config import settings
from typing import AsyncGenerator
from main import app
import pytest
from core.deps import get_session

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Use o prefixo 'sqlite+aiosqlite://' para indicar o uso do aiosqlite

# Crie um AsyncEngine usando o aiosqlite
engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Crie uma função de fábrica de sessão assíncrona
TestingSessionLocal: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)


async def override_get_db() -> AsyncGenerator:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


# Crie todas as tabelas manualmente usando 'async with engine.begin()'
@pytest.fixture(autouse=True)
async def create_test_tables():
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)


# Remova todas as tabelas após os testes
@pytest.fixture(autouse=True)
async def drop_test_tables():
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)