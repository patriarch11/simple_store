"""init

Revision ID: 0001
Revises: 
Create Date: 2024-09-16 17:17:46.958534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('categories_pkey')),
    sa.UniqueConstraint('name', name=op.f('categories_name_key'))
    )
    op.create_table('subcategories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('subcategories_category_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('subcategories_pkey')),
    sa.UniqueConstraint('name', name=op.f('subcategories_name_key'))
    )
    op.create_index(op.f('subcategories_category_id_idx'), 'subcategories', ['category_id'], unique=False)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('subcategory_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('discount_pct', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('total_count', sa.Integer(), nullable=False),
    sa.Column('reserved_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('products_category_id_fkey')),
    sa.ForeignKeyConstraint(['subcategory_id'], ['subcategories.id'], name=op.f('products_subcategory_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('products_pkey'))
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_price', sa.Float(), nullable=False),
    sa.Column('product_discount_pct', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('status', sa.Enum('RESERVED', 'COMPLETED', 'CANCELLED', name='orderstatus'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], name=op.f('orders_product_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('orders_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_index(op.f('subcategories_category_id_idx'), table_name='subcategories')
    op.drop_table('subcategories')
    op.drop_table('categories')
    # ### end Alembic commands ###
