"""minor tweaks

Revision ID: 684e7462e977
Revises: 9a8eb65d238e
Create Date: 2024-09-29 17:46:36.587027

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "684e7462e977"
down_revision: Union[str, None] = "9a8eb65d238e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "hourly_forecasts",
        "forecast_created_s",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_constraint(
        "forecast_uq_channel_start_created", "hourly_forecasts", type_="unique"
    )
    op.create_unique_constraint(
        "forecast_uq_gn_channel_start_created",
        "hourly_forecasts",
        ["from_g_node_alias", "channel_name", "start_unix_s", "forecast_created_s"],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "forecast_uq_gn_channel_start_created", "hourly_forecasts", type_="unique"
    )
    op.create_unique_constraint(
        "forecast_uq_channel_start_created",
        "hourly_forecasts",
        ["channel_name", "start_unix_s", "forecast_created_s"],
    )
    op.alter_column(
        "hourly_forecasts",
        "forecast_created_s",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    # ### end Alembic commands ###
