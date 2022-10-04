"""create books table

Revision ID: f0f22c3604a1
Revises: 
Create Date: 2022-10-04 00:12:18.379970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0f22c3604a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('books', sa.Column('id', sa.Integer(), nullable = False,
     primary_key = True), sa.Column('title', sa.String(), nullable =False))


def downgrade():
    op.drop_table('books')
    pass
