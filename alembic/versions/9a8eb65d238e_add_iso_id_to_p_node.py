"""add iso_id to p_node

Revision ID: 9a8eb65d238e
Revises: f9118269f440
Create Date: 2024-09-29 14:45:15.120309

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9a8eb65d238e"
down_revision: Union[str, None] = "f9118269f440"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("p_nodes", sa.Column("iso_id", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("p_nodes", "iso_id")
    # ### end Alembic commands ###
