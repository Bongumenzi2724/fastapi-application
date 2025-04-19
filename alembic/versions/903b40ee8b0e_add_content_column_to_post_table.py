"""add content column to post table

Revision ID: 903b40ee8b0e
Revises: ca07bcf21c5b
Create Date: 2025-04-19 12:27:16.190956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '903b40ee8b0e'
down_revision: Union[str, None] = 'ca07bcf21c5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass

#drop the content column
def downgrade() -> None:
    op.drop_column('posts','content')
    pass
