"""Add_new_columns

Revision ID: a94dd874ec87
Revises: 92e43ebf37f7
Create Date: 2024-02-21 21:41:08.867185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a94dd874ec87'
down_revision: Union[str, None] = '92e43ebf37f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column('Posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('Posts','published')
    op.drop_column('Posts','created_at')
    pass
