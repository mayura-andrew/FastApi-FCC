"""auto-vote

Revision ID: b1543dba33dc
Revises: 66cdc98bc836
Create Date: 2023-09-07 00:51:42.401532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1543dba33dc'
down_revision: Union[str, None] = '66cdc98bc836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'username')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    # ### end Alembic commands ###