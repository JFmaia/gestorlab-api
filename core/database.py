from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import settings

engine = create_engine(settings.DB_URL)

Session: sessionmaker = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=engine
)