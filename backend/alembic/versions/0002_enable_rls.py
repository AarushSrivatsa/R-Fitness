"""Enable Row Level Security on all application tables.

No browser-facing policies are created. Browser requests access application
data only through FastAPI, which connects using private server-side PostgreSQL
credentials and performs authorization before admin operations.
"""

from alembic import op

revision = "0002_enable_rls"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

TABLES = (
    "leads",
    "membership_plans",
    "programs",
    "trainers",
    "gallery_items",
    "faqs",
)


def upgrade() -> None:
    for table in TABLES:
        op.execute(f'ALTER TABLE public."{table}" ENABLE ROW LEVEL SECURITY')


def downgrade() -> None:
    for table in reversed(TABLES):
        op.execute(f'ALTER TABLE public."{table}" DISABLE ROW LEVEL SECURITY')
