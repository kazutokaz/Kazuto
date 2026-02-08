from fastapi.testclient import TestClient

from app.main import app


def t():
    assert TestClient(app).get("/health").json()["ok"]
