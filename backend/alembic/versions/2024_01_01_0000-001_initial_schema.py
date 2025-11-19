"""initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create country table
    op.create_table('country',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('region_group', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_country_code'), 'country', ['code'], unique=True)
    op.create_index(op.f('ix_country_id'), 'country', ['id'], unique=False)

    # Create factor_definition table
    op.create_table('factor_definition',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('group', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_factor_definition_code'), 'factor_definition', ['code'], unique=True)
    op.create_index(op.f('ix_factor_definition_group'), 'factor_definition', ['group'], unique=False)
    op.create_index(op.f('ix_factor_definition_id'), 'factor_definition', ['id'], unique=False)

    # Create factor_series table
    op.create_table('factor_series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.Column('factor_definition_id', sa.Integer(), nullable=False),
        sa.Column('source_name', sa.String(length=100), nullable=False),
        sa.Column('frequency', sa.String(length=20), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
        sa.ForeignKeyConstraint(['factor_definition_id'], ['factor_definition.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('country_id', 'factor_definition_id', 'frequency', 'source_name',
                          name='uq_country_factor_freq_source')
    )
    op.create_index('ix_factor_series_country_factor', 'factor_series',
                   ['country_id', 'factor_definition_id'], unique=False)
    op.create_index(op.f('ix_factor_series_country_id'), 'factor_series', ['country_id'], unique=False)
    op.create_index(op.f('ix_factor_series_factor_definition_id'), 'factor_series',
                   ['factor_definition_id'], unique=False)
    op.create_index(op.f('ix_factor_series_id'), 'factor_series', ['id'], unique=False)

    # Create factor_return table
    op.create_table('factor_return',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('factor_series_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('return_value', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['factor_series_id'], ['factor_series.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('factor_series_id', 'date', name='uq_factor_series_date')
    )
    op.create_index('ix_factor_return_series_date', 'factor_return',
                   ['factor_series_id', 'date'], unique=False)
    op.create_index(op.f('ix_factor_return_date'), 'factor_return', ['date'], unique=False)
    op.create_index(op.f('ix_factor_return_factor_series_id'), 'factor_return',
                   ['factor_series_id'], unique=False)
    op.create_index(op.f('ix_factor_return_id'), 'factor_return', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('factor_return')
    op.drop_table('factor_series')
    op.drop_table('factor_definition')
    op.drop_table('country')
