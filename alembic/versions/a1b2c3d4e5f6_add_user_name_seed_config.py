"""add user name and seed app_config

Revision ID: a1b2c3d4e5f6
Revises: 49b210472100
Create Date: 2026-07-14 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "49b210472100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=120), nullable=True))
    op.execute("UPDATE users SET name = 'Member' WHERE name IS NULL")
    op.alter_column("users", "name", nullable=False)

    op.execute(
        """
        INSERT INTO app_config (id, registration_count, login_enabled, launch_message)
        SELECT 1, 0, false, 'Launching soon'
        WHERE NOT EXISTS (SELECT 1 FROM app_config WHERE id = 1)
        """
    )


def downgrade() -> None:
    op.drop_column("users", "name")
