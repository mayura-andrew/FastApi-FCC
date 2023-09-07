"""add content column to posts table

Revision ID: d6d18c2531d9
Revises: 96a30e5471c7
Create Date: 2023-09-06 21:43:35.987737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6d18c2531d9'
down_revision: Union[str, None] = '96a30e5471c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
