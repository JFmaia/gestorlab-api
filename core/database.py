from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from core.config import settings
import os

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_= AsyncSession,
    bind=engine
)