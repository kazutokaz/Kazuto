from fastapi.testclient import TestClient


def test_register_login_me(tmp_path, monkeypatch):
    # DBをテスト用に差し替え（import前に環境変数セットするのがポイント）
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_PATH", str(db_path))
    monkeypatch.setenv("JWT_SECRET", "test-secret")

    from app.main import app  # noqa: E402

    client = TestClient(app)

    r = client.post("/register", json={"email": "a@example.com", "password": "pass1234"})
    assert r.status_code == 200
    assert r.json()["email"] == "a@example.com"
    user_id = r.json()["id"]
    assert isinstance(user_id, int)

    r = client.post("/login", json={"email": "a@example.com", "password": "pass1234"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "a@example.com"
