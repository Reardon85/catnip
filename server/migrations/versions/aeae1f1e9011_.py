"""empty message

Revision ID: aeae1f1e9011
Revises: 5c6b0ecfe026
Create Date: 2023-05-29 19:31:35.556610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeae1f1e9011'
down_revision = '5c6b0ecfe026'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hobbies', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('hobbies')

    # ### end Alembic commands ###
