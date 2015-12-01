"""Create users table.

Revision ID: 33ab597aece
Revises: 2c5ee5723dd
Create Date: 2015-11-30 15:14:06.217865

"""

# revision identifiers, used by Alembic.
revision = '33ab597aece'
down_revision = '2c5ee5723dd'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


def upgrade():
    table = op.create_table(
        'users',
        Column(
            'id',
            Integer,
            primary_key=True
        ),

        Column(
            'name',
            String,
        ),
        Column(
            'email',
            String,
            unique=True,
        ),
        Column(
            'password',
            String(128),
        ),
        Column(
            'is_admin',
            Boolean(),
            default=False,
        )
    )

    op.bulk_insert(
        table,
        [
            {
                'id': 1,
                'name': 'admin',
                'email': 'admin@admin.com',
                'password': 'e8dce00e7eb216e09d6ca309f862650495d7282092a1d2d41659d7f54a183780d69d8be907d5793c',
                'is_admin': True,

            },
        ]
    )


def downgrade():
    op.drop_table(
        'users',
    )
