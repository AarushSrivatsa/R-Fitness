"""Add the database-backed administrator credential record."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0003_admin_credentials"
down_revision = "0002_enable_rls"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    # The initial migration creates current metadata on an empty database, so
    # guard this migration for fresh installs as well as existing deployments.
    if not inspect(bind).has_table("app_admin_credentials"):
        op.create_table(
            "app_admin_credentials",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("admin_email", sa.String(length=254), nullable=False, unique=True),
            sa.Column("password_hash", sa.Text(), nullable=False),
            sa.Column("jwt_secret", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        )

    op.execute('ALTER TABLE public."app_admin_credentials" ENABLE ROW LEVEL SECURITY')


def downgrade() -> None:
    op.drop_table("app_admin_credentials")
