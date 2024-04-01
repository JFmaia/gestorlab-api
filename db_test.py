from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from core.config import SettingsTest


def initialize_test_database(settings: SettingsTest):
    import models.__all_models
    db_url = settings.DB_URL_TEST  # Adapte isso conforme necessário
    engine = create_engine(db_url)

    if not database_exists(db_url):
        create_database(db_url)

    settings.DBBaseModel.metadata.create_all(bind=engine)

    yield

    settings.DBBaseModel.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    settings = SettingsTest()

    for _ in initialize_test_database(settings):
        print("Test database initialized.")