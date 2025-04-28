"""Change duration column type from str to int

Revision ID: d7e5394e430a
Revises: 6069c5dd3ea9
Create Date: 2025-04-28 17:57:55.449538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e5394e430a'
down_revision: Union[str, None] = '6069c5dd3ea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        ALTER TABLE eventmodel
        ALTER COLUMN duration TYPE INTEGER
        USING duration::integer
    """)

def downgrade():
    op.execute("""
        ALTER TABLE eventmodel
        ALTER COLUMN duration TYPE VARCHAR
    """)
