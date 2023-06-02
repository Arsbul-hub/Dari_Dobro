"""empty message

Revision ID: a4924da1fd8f
Revises: 
Create Date: 2023-05-26 18:54:07.276649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4924da1fd8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('animals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('animal_type', sa.String(), nullable=True),
    sa.Column('age_type', sa.String(), nullable=True),
    sa.Column('cover', sa.String(), nullable=True),
    sa.Column('have_house', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('config',
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    op.create_table('documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gallery',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('file', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_materials_timestamp'), ['timestamp'], unique=False)

    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('cover', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_news_timestamp'), ['timestamp'], unique=False)

    op.create_table('pages_data',
    sa.Column('page', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('page')
    )
    op.create_table('partners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('logo', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('smi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('cover', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('smi', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_smi_timestamp'), ['timestamp'], unique=False)

    op.create_table('social_networks',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('qr', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))

    op.drop_table('users')
    op.drop_table('social_networks')
    with op.batch_alter_table('smi', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_smi_timestamp'))

    op.drop_table('smi')
    op.drop_table('partners')
    op.drop_table('pages_data')
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_news_timestamp'))

    op.drop_table('news')
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_materials_timestamp'))

    op.drop_table('materials')
    op.drop_table('gallery')
    op.drop_table('documents')
    op.drop_table('config')
    op.drop_table('animals')
    # ### end Alembic commands ###