"""add tab data

Revision ID: fd474139b8a7
Revises: 4936b733f921
Create Date: 2016-02-27 17:20:47.750482

"""

# revision identifiers, used by Alembic.
revision = 'fd474139b8a7'
down_revision = '4936b733f921'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    places = op.create_table(
        'tab_data',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False),
        Column('is_visible', Boolean, default=True),
    )

    op.bulk_insert(
        places,
        [
            {
                'id': 1,
                'name': 'loga',
                'is_visible': True,
            },
            {
                'id': 2,
                'name': 'scores',
                'is_visible': True,
            },
            {
                'id': 3,
                'name': 'group_a',
                'is_visible': True,
            },
            {
                'id': 4,
                'name': 'group_b',
                'is_visible': True,
            },
            {
                'id': 5,
                'name': 'finals',
                'is_visible': True,
            },
        ]
    )


def downgrade():
    op.drop_table('tab_data')
