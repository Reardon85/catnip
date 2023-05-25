"""empty message

Revision ID: 90423db9944e
Revises: ceeaaa4be482
Create Date: 2023-05-25 12:43:15.866029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90423db9944e'
down_revision = 'ceeaaa4be482'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('text')

    # ### end Alembic commands ###
