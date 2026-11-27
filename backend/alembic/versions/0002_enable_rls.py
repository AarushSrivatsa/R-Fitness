"""Enable Row Level Security on all application tables.

No anon/authenticated policies are created: browser clients use Supabase Auth,
while all application data flows through the FastAPI API with server-side
authorization. The API's private PostgreSQL connection uses the table owner.
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
