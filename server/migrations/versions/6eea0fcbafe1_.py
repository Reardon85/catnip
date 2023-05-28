"""empty message

Revision ID: 6eea0fcbafe1
Revises: b0bf44a2b3cf
Create Date: 2023-05-22 18:27:39.615125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eea0fcbafe1'
down_revision = 'b0bf44a2b3cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_one_id', sa.Integer(), nullable=True),
    sa.Column('user_two_id', sa.Integer(), nullable=True),
    sa.Column('user_one_seen', sa.Boolean(), nullable=True),
    sa.Column('user_two_seen', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_one_id'], ['users.id'], name=op.f('fk_conversations_user_one_id_users')),
    sa.ForeignKeyConstraint(['user_two_id'], ['users.id'], name=op.f('fk_conversations_user_two_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('favorited_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorited_id'], ['users.id'], name=op.f('fk_favorites_favorited_id_users')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_favorites_user_id_users'))
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_one_id', sa.Integer(), nullable=True),
    sa.Column('user_two_id', sa.Integer(), nullable=True),
    sa.Column('user_one_liked', sa.Boolean(), nullable=True),
    sa.Column('user_two_liked', sa.Boolean(), nullable=True),
    sa.Column('matched', sa.Boolean(), nullable=True),
    sa.Column('user_one_seen', sa.Boolean(), nullable=True),
    sa.Column('user_two_seen', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_one_id'], ['users.id'], name=op.f('fk_matches_user_one_id_users')),
    sa.ForeignKeyConstraint(['user_two_id'], ['users.id'], name=op.f('fk_matches_user_two_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_messages_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('animal', sa.String(), nullable=True),
    sa.Column('breed', sa.String(), nullable=True),
    sa.Column('temperment', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_pets_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_photos_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visitors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('visitor_id', sa.Integer(), nullable=False),
    sa.Column('seen', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_visitors_user_id_users')),
    sa.ForeignKeyConstraint(['visitor_id'], ['users.id'], name=op.f('fk_visitors_visitor_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'visitor_id', name='unique_user_visitor')
    )
    op.create_table('petphotos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('pet_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], name=op.f('fk_petphotos_pet_id_pets')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('petphotos')
    op.drop_table('visitors')
    op.drop_table('photos')
    op.drop_table('pets')
    op.drop_table('messages')
    op.drop_table('matches')
    op.drop_table('favorites')
    op.drop_table('conversations')
    # ### end Alembic commands ###