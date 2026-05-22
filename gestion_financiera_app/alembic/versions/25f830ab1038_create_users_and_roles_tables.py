"""create users and roles tables

Revision ID: 25f830ab1038
Revises: b7769d87a3c6
Create Date: 2026-05-21 01:36:29.140796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25f830ab1038'
down_revision: Union[str, Sequence[str], None] = 'b7769d87a3c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
