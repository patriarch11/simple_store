"""product_reserved_count

Revision ID: 0005
Revises: 0004
Create Date: 2024-09-14 14:15:24.263908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0005'
down_revision: Union[str, None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('reserved_count', sa.Integer(), nullable=False))
    op.drop_column('products', 'free_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('free_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('products', 'reserved_count')
    # ### end Alembic commands ###
