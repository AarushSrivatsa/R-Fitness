from fastapi.testclient import TestClient
import jwt
from pwdlib import PasswordHash

from app.config import settings
from app.main import app

client = TestClient(app)
TEST_PASSWORD = "correct-horse-battery-staple-2026"


def configure_admin(monkeypatch):
    monkeypatch.setattr(settings, "admin_email", "owner@rfitness.example")
    monkeypatch.setattr(
        settings,
        "admin_password_hash",
        PasswordHash.recommended().hash(TEST_PASSWORD),
    )
    monkeypatch.setattr(settings, "jwt_secret", "test-only-secret-that-is-long-enough-123456")


def test_admin_login_returns_signed_token(monkeypatch):
    configure_admin(monkeypatch)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "owner@rfitness.example", "password": TEST_PASSWORD},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["expires_in"] == 8 * 60 * 60
    claims = jwt.decode(
        payload["access_token"],
        settings.jwt_secret,
        algorithms=["HS256"],
    )
    assert claims["sub"] == "owner@rfitness.example"
    assert claims["role"] == "admin"


def test_admin_login_rejects_wrong_password(monkeypatch):
    configure_admin(monkeypatch)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "owner@rfitness.example", "password": "incorrect-password-long-enough"},
    )

    assert response.status_code == 401


def test_admin_login_rejects_wrong_email(monkeypatch):
    configure_admin(monkeypatch)

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "other@rfitness.example", "password": TEST_PASSWORD},
    )

    assert response.status_code == 401


def test_admin_routes_reject_missing_token():
    response = client.get("/api/v1/admin/overview")
    assert response.status_code == 401
