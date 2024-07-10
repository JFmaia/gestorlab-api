import os
from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
class Settings(BaseSettings): 
    API_V1_STR: str = os.getenv('API_V1_STR')
    DATABASE_PORT: int = os.getenv('DATABASE_PORT')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    
    @property
    def DB_URL(self) -> str:
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@dbpostgrestest:{self.DATABASE_PORT}/{self.POSTGRES_DB}'
    
    DBBaseModel: ClassVar = declarative_base()

    #DIca de como gerar token no pront do python: token: str = secrets.token_urlsafe(32)
    JWT_SECRET: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

settings: Settings = Settings()
