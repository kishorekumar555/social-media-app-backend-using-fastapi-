"""add content column to the posts table

Revision ID: b0d8d7785757
Revises: 3e2466b7a3fc
Create Date: 2024-02-21 20:19:03.950872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0d8d7785757'
down_revision: Union[str, None] = '3e2466b7a3fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('Posts','content')
    pass
