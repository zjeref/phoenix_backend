"""empty message

Revision ID: 866f24677210
Revises: b99ff7b0224b
Create Date: 2018-02-27 11:15:30.353032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '866f24677210'
down_revision = 'b99ff7b0224b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('faculty', sa.Column('gender', sa.Enum('male', 'female', 'others', name='gender'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('faculty', 'gender')
    # ### end Alembic commands ###
