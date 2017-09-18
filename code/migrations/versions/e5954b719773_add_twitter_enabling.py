"""add twitter enabling

Revision ID: e5954b719773
Revises: 9185bf2d51b1
Create Date: 2016-02-28 11:36:36.827448

"""

# revision identifiers, used by Alembic.
revision = 'e5954b719773'
down_revision = '9185bf2d51b1'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import Boolean


def upgrade():
    op.add_column(
        'events',
        Column('enable_twtitter', Boolean(), default=False, server_default='false')
    )


def downgrade():
    op.drop_column('events', 'enable_twtitter')
