"""create posts table

Revision ID: 96a30e5471c7
Revises: 05078dee79b0
Create Date: 2023-09-06 21:37:13.241479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96a30e5471c7'
down_revision: Union[str, None] = '05078dee79b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
