"""Add place to a game

Revision ID: efa0f32b2e4d
Revises: f4b90973823f
Create Date: 2016-01-31 23:19:17.763701

"""

# revision identifiers, used by Alembic.
revision = 'efa0f32b2e4d'
down_revision = 'f4b90973823f'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer


def upgrade():
    op.add_column(
        'games',
        Column('place_id', Integer, ForeignKey('places.id'))
    )


def downgrade():
    op.drop_column('games', 'place_id')
