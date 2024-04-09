import os
from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class SettingsTest(BaseSettings):
    DATABASE_PORT_TEST: int = os.getenv('DATABASE_PORT_TEST')
    POSTGRES_PASSWORD_TEST: str = os.getenv('POSTGRES_PASSWORD_TEST')
    POSTGRES_USER_TEST: str = os.getenv('POSTGRES_USER_TEST')
    POSTGRES_DB_TEST: str = os.getenv('POSTGRES_DB_TEST')

    @property
    def DB_URL_TEST(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER_TEST}:{self.POSTGRES_PASSWORD_TEST}@localhost:{self.DATABASE_PORT_TEST}/{self.POSTGRES_DB_TEST}'
   
    DBBaseModel: ClassVar = declarative_base()

settingsTest: SettingsTest = SettingsTest()