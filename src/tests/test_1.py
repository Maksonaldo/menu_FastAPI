import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.models.database import get_session
from src.main import app
# from .main import app
# @pytest.fixture(scope='session')
# def test_a():
#     assert 1 == 1
app = FastAPI()


@app.get("/")
def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_a():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
