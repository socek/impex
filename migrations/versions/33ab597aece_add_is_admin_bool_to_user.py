"""Add is_admin bool to user.

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


def upgrade():
    op.add_column(
        'users',
        Column('is_admin', Boolean(), default=False)
    )


def downgrade():
    op.drop_column('users', 'is_admin')
