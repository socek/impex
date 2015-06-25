"""create sample data

Revision ID: 351daa7c83b
Revises:
Create Date: 2015-06-25 07:13:31.928021

"""

# revision identifiers, used by Alembic.
revision = '351daa7c83b'
down_revision = None
branch_labels = None
depends_on = None

from sqlalchemy import Column, Integer, String
from alembic import op


def upgrade():
    op.create_table(
        'rooms',
        Column(
            'id',
            Integer,
            primary_key=True),

        Column(
            'name',
            String),
    )


def downgrade():
    op.drop_table('game_borrows')
