"""init

Revision ID: e0ff150fc718
Revises: 
Create Date: 2022-07-31 21:14:01.238175

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e0ff150fc718"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "quote",
        sa.Column("quote_id", sa.Integer, primary_key=True),
        sa.Column("pair", sa.String(length=50)),
        sa.Column("ts", sa.DateTime, default=datetime.now),
        sa.Column("rate", sa.DECIMAL(6, 3)),
    )


def downgrade() -> None:
    op.drop_table("quote")
