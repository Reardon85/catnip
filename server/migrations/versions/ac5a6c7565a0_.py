"""empty message

Revision ID: ac5a6c7565a0
Revises: 90423db9944e
Create Date: 2023-05-26 16:25:40.223670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac5a6c7565a0'
down_revision = '90423db9944e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('zipcode', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('latitude', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('longitude', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('orientation', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('ethnicity', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('height', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('diet', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('religion', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('religion')
        batch_op.drop_column('diet')
        batch_op.drop_column('height')
        batch_op.drop_column('status')
        batch_op.drop_column('ethnicity')
        batch_op.drop_column('orientation')
        batch_op.drop_column('longitude')
        batch_op.drop_column('latitude')
        batch_op.drop_column('zipcode')

    # ### end Alembic commands ###
