"""Create game

Revision ID: 19854096cf
Revises: 13267b8fa76
Create Date: 2015-12-03 21:11:15.764756

"""

# revision identifiers, used by Alembic.
revision = '19854096cf'
down_revision = '13267b8fa76'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSON


def upgrade():
    op.create_table(
        'games',
        Column('id', Integer, primary_key=True),
        Column('plaing_at', DateTime),
        Column('priority', Integer, nullable=False),
        Column('status', Integer, nullable=False, default=0),
        Column('event_id', Integer, ForeignKey('events.id'), nullable=False),
        Column('left_id', Integer, ForeignKey('teams.id')),
        Column('right_id', Integer, ForeignKey('teams.id')),
        Column('scores', JSON),
    )


def downgrade():
    op.drop_table('games')
