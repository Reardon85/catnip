"""empty message

Revision ID: 5c6b0ecfe026
Revises: 3524ba839be4
Create Date: 2023-05-29 18:56:35.819808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c6b0ecfe026'
down_revision = '3524ba839be4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('interested_in', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('interested_in')

    # ### end Alembic commands ###
