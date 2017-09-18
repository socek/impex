"""add constraint to games

Revision ID: 33fb95791ba
Revises: 19854096cf
Create Date: 2015-12-06 21:29:19.319780

"""

# revision identifiers, used by Alembic.
revision = '33fb95791ba'
down_revision = '19854096cf'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.create_unique_constraint(
        "uq_game_priority",
        "games",
        ["event_id", "priority"],
    )


def downgrade():
    pass
