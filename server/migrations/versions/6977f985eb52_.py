"""empty message

Revision ID: 6977f985eb52
Revises: 6eea0fcbafe1
Create Date: 2023-05-23 11:04:04.653412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6977f985eb52'
down_revision = '6eea0fcbafe1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_url', sa.String(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_url', sa.String(), nullable=True))
        batch_op.drop_column('profile_pic_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic_url', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('avatar_url')

    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.drop_column('avatar_url')

    # ### end Alembic commands ###
