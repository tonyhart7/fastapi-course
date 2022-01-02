"""create posts table

Revision ID: 35270ac773d8
Revises: 
Create Date: 2021-12-30 16:01:55.876545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35270ac773d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False), sa.Column('title', sa.String(length=255), nullable=False), sa.Column('body', sa.Text(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('title'))
    pass


def downgrade():
    op.drop_table('posts')
    pass
