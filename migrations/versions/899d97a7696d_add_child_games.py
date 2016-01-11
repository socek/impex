"""Add child games

Revision ID: 899d97a7696d
Revises: 4ca11fb82c9
Create Date: 2016-01-06 22:12:20.956942

"""

# revision identifiers, used by Alembic.
revision = '899d97a7696d'
down_revision = '4ca11fb82c9'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


def upgrade():
    op.add_column(
        'games',
        Column('child_id', Integer, ForeignKey('games.id'))
    )


def downgrade():
    op.drop_column('games', 'child_id')
