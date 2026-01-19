"""create prices table

Revision ID: 54593c130cfd
Revises: 
Create Date: 2026-01-16 21:15:07.527538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54593c130cfd'
down_revision: Union[str, Sequence[str], None] = None
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