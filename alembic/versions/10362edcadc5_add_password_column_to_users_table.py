"""add password column to users table

Revision ID: 10362edcadc5
Revises: 3c1e36aa712a
Create Date: 2025-04-19 12:58:36.523889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10362edcadc5'
down_revision: Union[str, None] = '3c1e36aa712a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users',sa.Column('password',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users','password')
    pass
