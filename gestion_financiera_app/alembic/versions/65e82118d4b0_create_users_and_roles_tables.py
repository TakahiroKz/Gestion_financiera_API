"""create users and roles tables

Revision ID: 65e82118d4b0
Revises: 25f830ab1038
Create Date: 2026-05-21 01:38:15.733089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65e82118d4b0'
down_revision: Union[str, Sequence[str], None] = '25f830ab1038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
