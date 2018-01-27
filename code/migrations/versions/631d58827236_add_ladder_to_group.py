"""Add ladder to Group

Revision ID: 631d58827236
Revises: 899d97a7696d
Create Date: 2016-01-25 20:55:19.163426

"""

# revision identifiers, used by Alembic.
revision = '631d58827236'
down_revision = '899d97a7696d'
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy import Boolean
from sqlalchemy import Column


def upgrade():
    op.add_column(
        'groups',
        Column('ladder', Boolean, nullable=False, default=False, server_default='false')
    )


def downgrade():
    op.drop_column('groups', 'ladder')
