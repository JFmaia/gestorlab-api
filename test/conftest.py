import pytest
from fastapi.testclient import TestClient
from core.config_test import settingsTest
from core.database import enginetest
from main import app
import os

@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown():
    # Setup: set TESTING environment variable to True
    os.environ["TESTING"] = "True"
    
    # Create tables for the test database
    async with enginetest.begin() as conn:
        await conn.run_sync(settingsTest.DBBaseModel.metadata.create_all)
    
    # Run the tests
    yield
    
    # Teardown: set TESTING environment variable to False
    os.environ["TESTING"] = "False"
    
    # Drop all tables after the tests are done
    async with enginetest.begin() as conn:
        await conn.run_sync(settingsTest.DBBaseModel.metadata.drop_all)
        

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

