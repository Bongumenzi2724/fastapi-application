"""add users table

Revision ID: 3c1e36aa712a
Revises: 903b40ee8b0e
Create Date: 2025-04-19 12:49:16.202951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c1e36aa712a'
down_revision: Union[str, None] = '903b40ee8b0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('username',sa.String(),nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
