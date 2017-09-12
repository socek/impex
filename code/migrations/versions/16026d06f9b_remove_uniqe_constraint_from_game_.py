"""remove uniqe constraint from game.priorities

Revision ID: 16026d06f9b
Revises: 20263e0fe25
Create Date: 2015-12-07 22:36:29.860394

"""

# revision identifiers, used by Alembic.
revision = '16026d06f9b'
down_revision = '20263e0fe25'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_constraint(
        "uq_game_priority",
        "games",
    )


def downgrade():
    pass
