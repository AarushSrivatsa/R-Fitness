import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AdminCredential

bearer_scheme = HTTPBearer(auto_error=False)


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in required.")

    credential = db.get(AdminCredential, 1)
    if credential is None:
        raise HTTPException(status_code=503, detail="Administrator account has not been initialized.")

    try:
        claims = jwt.decode(
            credentials.credentials,
            credential.jwt_secret,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub"]},
        )
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session.") from exc

    if claims.get("role") != "admin" or claims.get("sub") != credential.admin_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required.")

    return claims
