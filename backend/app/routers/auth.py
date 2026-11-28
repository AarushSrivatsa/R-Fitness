from datetime import datetime, timedelta, timezone
import secrets

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AdminCredential
from app.schemas import AdminLogin, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
password_hasher = PasswordHash.recommended()
TOKEN_LIFETIME_SECONDS = 8 * 60 * 60


@router.post("/login", response_model=TokenResponse)
def login(payload: AdminLogin, db: Session = Depends(get_db)) -> TokenResponse:
    credential = db.get(AdminCredential, 1)
    if credential is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Administrator account has not been initialized.",
        )

    email_matches = secrets.compare_digest(
        payload.email.strip().lower().encode("utf-8"),
        credential.admin_email.encode("utf-8"),
    )
    try:
        password_matches = password_hasher.verify(payload.password, credential.password_hash)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Administrator credentials are unavailable.",
        ) from exc

    if not email_matches or not password_matches:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=TOKEN_LIFETIME_SECONDS)
    token = jwt.encode(
        {
            "sub": credential.admin_email,
            "role": "admin",
            "iat": now,
            "exp": expires_at,
        },
        credential.jwt_secret,
        algorithm="HS256",
    )
    return TokenResponse(access_token=token, expires_in=TOKEN_LIFETIME_SECONDS)
