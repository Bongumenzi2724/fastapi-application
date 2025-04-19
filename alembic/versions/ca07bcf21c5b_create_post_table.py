"""create post table

Revision ID: ca07bcf21c5b
Revises: 
Create Date: 2025-04-19 10:44:57.697188

"""
from typing import Sequence, Union
from sqlalchemy import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca07bcf21c5b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean,nullable=False),
                    sa.Column('created_at',TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
