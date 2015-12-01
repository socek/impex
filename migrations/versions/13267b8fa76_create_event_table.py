"""Create Event table.

Revision ID: 13267b8fa76
Revises: 33ab597aece
Create Date: 2015-12-01 15:07:50.701588

"""

# revision identifiers, used by Alembic.
revision = '13267b8fa76'
down_revision = '33ab597aece'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    op.create_table(
        'events',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('start_date', Date),
        Column('end_date', Date),
        Column('is_visible', Boolean(), default=False),
    )


def downgrade():
    op.drop_table('events')
