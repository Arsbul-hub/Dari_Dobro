"""empty message

Revision ID: edd5a6116cc7
Revises: b50ec5ce817f
Create Date: 2023-05-20 17:11:16.419073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edd5a6116cc7'
down_revision = 'b50ec5ce817f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('config', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('config', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
