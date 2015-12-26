"""Create Group model.

Revision ID: 4ca11fb82c9
Revises: 16026d06f9b
Create Date: 2015-12-26 14:01:43.418603

"""

# revision identifiers, used by Alembic.
revision = '4ca11fb82c9'
down_revision = '16026d06f9b'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import table


def upgrade():
    groups = op.create_table(
        'groups',
        Column(
            'id',
            Integer,
            primary_key=True
        ),

        Column(
            'name',
            String,
            nullable=False,
        ),
    )

    op.bulk_insert(
        groups,
        [
            {
                'id': 1,
                'name': 'Grupa A',
            },
            {
                'id': 2,
                'name': 'Grupa B',
            },
            {
                'id': 3,
                'name': 'Finały',
            },
        ]
    )

    op.add_column(
        'games',
        Column('group_id', Integer, ForeignKey('groups.id')),
    )
    games = table(
        'games',
        Column(
            'group_id', Integer, ForeignKey('groups.id')
        )
    )
    op.execute(
        games
        .update()
        .values({'group_id': 1})
    )
    op.alter_column("games", "group_id", nullable=True)


def downgrade():
    op.drop_column('games', 'group_id')
    op.drop_table('groups')
