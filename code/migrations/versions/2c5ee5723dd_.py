"""Create teams table

Revision ID: 2c5ee5723dd
Revises:
Create Date: 2015-11-27 15:27:35.981503

"""

# revision identifiers, used by Alembic.
revision = '2c5ee5723dd'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    op.create_table(
        'teams',
        Column(
            'id',
            Integer,
            primary_key=True),

        Column(
            'name',
            String,
            nullable=False),

        Column(
            'hometown',
            String),
    )


def downgrade():
    op.drop_table('teams')
