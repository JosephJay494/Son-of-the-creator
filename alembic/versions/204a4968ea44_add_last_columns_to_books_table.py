"""add last columns to books table

Revision ID: 204a4968ea44
Revises: ceabb9f476a8
Create Date: 2022-10-04 02:15:02.418439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '204a4968ea44'
down_revision = 'ceabb9f476a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('books', sa.Column(
        'author', sa.String(), nullable = False),)
    op.add_column('books', sa.Column('synopsis', sa.String(), nullable = False),)
    op.add_column('books', sa.Column('published', sa.Boolean(), server_default= 'True', nullable = False),)
    op.add_column('books', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default= sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('books', 'synopsis')
    op.drop_column('books', 'published')
    op.drop_column('books', 'created_at')
    pass
