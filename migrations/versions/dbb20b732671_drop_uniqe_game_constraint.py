"""drop uniqe game constraint

Revision ID: dbb20b732671
Revises: efa0f32b2e4d
Create Date: 2016-02-05 22:39:34.497774

"""

# revision identifiers, used by Alembic.
revision = 'dbb20b732671'
down_revision = 'efa0f32b2e4d'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.drop_constraint(
        "uq_game_teams",
        "games",
    )


def downgrade():
    pass
