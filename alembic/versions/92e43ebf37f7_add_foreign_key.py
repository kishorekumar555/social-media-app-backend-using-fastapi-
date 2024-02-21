"""Add foreign key

Revision ID: 92e43ebf37f7
Revises: 78be2e16a098
Create Date: 2024-02-21 20:48:05.006681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92e43ebf37f7'
down_revision: Union[str, None] = '78be2e16a098'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('Posts_Users_fk',source_table="Posts",referent_table="Users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('Posts_Users_fk',table_name="Posts")
    op.drop_column('Posts','owner_id')
    pass
