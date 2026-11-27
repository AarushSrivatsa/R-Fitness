from datetime import datetime, timedelta, timezone
import secrets

import jwt
from fastapi import APIRouter, HTTPException, status
from pwdlib import PasswordHash

from app.config import settings
from app.schemas import AdminLogin, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
password_hasher = PasswordHash.recommended()
TOKEN_LIFETIME_SECONDS = 8 * 60 * 60


@router.post("/login", response_model=TokenResponse)
def login(payload: AdminLogin) -> TokenResponse:
    configured_email = settings.admin_email.strip().lower()
    encoded_password_hash = settings.admin_password_hash
    if (
        not configured_email
        or not encoded_password_hash
        or not settings.jwt_secret
        or len(settings.jwt_secret) < 32
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin authentication is not configured.",
        )

    try:
        password_matches = password_hasher.verify(payload.password, encoded_password_hash)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin password hash configuration is invalid.",
        ) from exc

    email_matches = secrets.compare_digest(
        payload.email.strip().lower().encode("utf-8"),
        configured_email.encode("utf-8"),
    )
    if not email_matches or not password_matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=TOKEN_LIFETIME_SECONDS)
    token = jwt.encode(
        {
            "sub": configured_email,
            "role": "admin",
            "iat": now,
            "exp": expires_at,
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    return TokenResponse(access_token=token, expires_in=TOKEN_LIFETIME_SECONDS)
