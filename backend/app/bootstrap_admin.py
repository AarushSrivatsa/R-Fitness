"""Create a random administrator login once, storing only its password hash."""
import logging
import secrets

from pwdlib import PasswordHash

from app.config import settings
from app.database import SessionLocal
from app.models import AdminCredential

logger = logging.getLogger("rfitness.bootstrap")


def main() -> None:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is required to initialize administrator credentials.")

    with SessionLocal() as db:
        existing = db.get(AdminCredential, 1)
        if existing is not None:
            logger.info("R Fitness administrator account is already initialized.")
            return

        initial_password = secrets.token_urlsafe(24)
        credential = AdminCredential(
            id=1,
            admin_email=settings.admin_email.strip().lower(),
            password_hash=PasswordHash.recommended().hash(initial_password),
            jwt_secret=secrets.token_urlsafe(48),
        )
        db.add(credential)
        db.commit()

    # This is emitted only on first initialization. The plaintext password is
    # never persisted; the Argon2 hash and JWT key live in Neon.
    logger.warning("INITIAL R FITNESS ADMIN LOGIN — email: %s", settings.admin_email)
    logger.warning("INITIAL R FITNESS ADMIN PASSWORD (copy this now): %s", initial_password)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
