"""add slider event

Revision ID: 4936b733f921
Revises: dbb20b732671
Create Date: 2016-02-12 19:56:59.346287

"""

# revision identifiers, used by Alembic.
revision = '4936b733f921'
down_revision = 'dbb20b732671'
branch_labels = None
depends_on = None

from alembic import op
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    op.create_table(
        'slider_events',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('value', String),
        Column('when_created', DateTime(), default=datetime.now),
    )


def downgrade():
    op.drop_table('slider_events')
