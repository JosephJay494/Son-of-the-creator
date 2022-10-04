"""add foreign-key to books table

Revision ID: ceabb9f476a8
Revises: 70ddf50e5ce0
Create Date: 2022-10-04 02:01:04.334140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceabb9f476a8'
down_revision = '70ddf50e5ce0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('books', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('books_users_fk', source_table='books', referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('books_users_fk', table_name='books')
    op.drop_column('books', 'owner_id')
    pass 
