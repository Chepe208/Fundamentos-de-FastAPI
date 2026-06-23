"""add authentication fields to users

Revision ID: c6cbc851f040
Revises: a05b831928f7
Create Date: 2026-06-23 15:45:32.157541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'c6cbc851f040'
down_revision: Union[str, Sequence[str], None] = 'a05b831928f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute("""
        INSERT INTO users_new (id, name, email, role, is_active, created_at, hashed_password)
        SELECT id, name, email, role, is_active, created_at, 'temporal_hash'
        FROM users
    """)

    op.drop_table('users')

    op.rename_table('users_new', 'users')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'users_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.execute("""
        INSERT INTO users_old (id, name, email, role, is_active, created_at)
        SELECT id, name, email, role, is_active, created_at
        FROM users
    """)

    op.drop_table('users')

    op.rename_table('users_old', 'users')