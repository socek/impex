"""add game teams uniqe per event

Revision ID: 20263e0fe25
Revises: 33fb95791ba
Create Date: 2015-12-07 17:13:24.190206

"""

# revision identifiers, used by Alembic.
revision = '20263e0fe25'
down_revision = '33fb95791ba'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.create_unique_constraint(
        "uq_game_teams",
        "games",
        ["event_id", "left_id", "right_id"],
    )


def downgrade():
    pass
