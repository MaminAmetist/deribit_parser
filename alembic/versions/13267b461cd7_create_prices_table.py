"""create prices table

Revision ID: 13267b461cd7
Revises: 54593c130cfd
Create Date: 2026-01-16 21:27:41.948874

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '13267b461cd7'
down_revision: Union[str, Sequence[str], None] = '54593c130cfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ticker", sa.String(length=10), nullable=False, index=True),
        sa.Column("price", sa.Numeric(20, 8), nullable=False),
        sa.Column("timestamp", sa.BigInteger, nullable=False, index=True),
        schema="public",
    )


def downgrade() -> None:
    op.drop_table("prices", schema="public")
