"""Add labels to tab.

Revision ID: 9185bf2d51b1
Revises: fd474139b8a7
Create Date: 2016-02-27 22:14:24.310988

"""

# revision identifiers, used by Alembic.
revision = '9185bf2d51b1'
down_revision = 'fd474139b8a7'
branch_labels = None
depends_on = None

from alembic.op import add_column
from alembic.op import execute
from alembic.op import inline_literal
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.sql import table


def upgrade():
    add_column(
        'tab_data',
        Column('label', String),
    )
    tab = table(
        'tab_data',
        Column('name', String),
        Column('label', String),
    )

    data = [
        ('loga', 'Loga'),
        ('scores', 'Wszystkie Mecze'),
        ('group_a', 'Grupa A'),
        ('group_b', 'Grupa B'),
        ('finals', 'Finały'),
    ]

    for name, label in data:
        execute(
            tab.update()
            .where(tab.c.name == inline_literal(name))
            .values({'label': inline_literal(label)})
        )


def downgrade():
    op.drop_column('tab_data', 'label')
