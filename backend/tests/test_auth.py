from fastapi.testclient import TestClient
import jwt
from pwdlib import PasswordHash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import AdminCredential

client = TestClient(app)
TEST_EMAIL = "owner@rfitness.example"
TEST_PASSWORD = "correct-horse-battery-staple-2026"
TEST_JWT_SECRET = "test-only-secret-that-is-long-enough-123456"


def install_test_admin_database():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with TestSession() as db:
        db.add(
            AdminCredential(
                id=1,
                admin_email=TEST_EMAIL,
                password_hash=PasswordHash.recommended().hash(TEST_PASSWORD),
                jwt_secret=TEST_JWT_SECRET,
            )
        )
        db.commit()

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return engine


def test_admin_login_returns_signed_token():
    engine = install_test_admin_database()
    try:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["token_type"] == "bearer"
        assert payload["expires_in"] == 8 * 60 * 60
        claims = jwt.decode(payload["access_token"], TEST_JWT_SECRET, algorithms=["HS256"])
        assert claims["sub"] == TEST_EMAIL
        assert claims["role"] == "admin"
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_admin_login_rejects_wrong_password():
    engine = install_test_admin_database()
    try:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": TEST_EMAIL, "password": "incorrect-password-long-enough"},
        )
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_admin_login_rejects_wrong_email():
    engine = install_test_admin_database()
    try:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "other@rfitness.example", "password": TEST_PASSWORD},
        )
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


def test_admin_routes_reject_missing_token():
    engine = install_test_admin_database()
    try:
        response = client.get("/api/v1/admin/overview")
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
