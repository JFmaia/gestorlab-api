from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from core.config import settings
from core.config_test import settingsTest

engine: AsyncEngine = create_async_engine(settings.DB_URL)
enginetest: AsyncEngine = create_async_engine(settingsTest.DB_URL_TEST)

Session: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_= AsyncSession,
    bind=engine
)

SessionTest: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_= AsyncSession,
    bind=enginetest
)