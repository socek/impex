"""Create Place

Revision ID: f4b90973823f
Revises: 631d58827236
Create Date: 2016-01-31 22:49:14.188516

"""

# revision identifiers, used by Alembic.
revision = 'f4b90973823f'
down_revision = '631d58827236'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    places = op.create_table(
        'places',
        Column('id', Integer, primary_key=True),
        Column('name', String, nullable=False)
    )

    op.bulk_insert(
        places,
        [
            {
                'id': 1,
                'name': 'L.O. Staszic - Tarnowskie Góry',
            },
            {
                'id': 2,
                'name': 'MOSIR - Radzionków',
            },
            {
                'id': 3,
                'name': 'Hala Sportowa Tarnowskie Góry',
            },
        ]
    )


def downgrade():
    op.drop_table('places')
