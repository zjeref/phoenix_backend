"""empty message

Revision ID: 9452402e522b
Revises: c04f5e3c4ea0
Create Date: 2018-04-01 23:54:41.109546

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9452402e522b'
down_revision = 'c04f5e3c4ea0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('branch_id', sa.Integer(), nullable=True))
    op.add_column('student', sa.Column('category_id', sa.Integer(), nullable=True))
    op.drop_column('student', 'category')
    op.drop_column('student', 'branch')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('branch', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('student', sa.Column('category', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('student', 'category_id')
    op.drop_column('student', 'branch_id')
    # ### end Alembic commands ###