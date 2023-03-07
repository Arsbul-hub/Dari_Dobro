"""users table

Revision ID: 7dc6aa88d3f4
Revises: 812c26ee6f2d
Create Date: 2023-02-24 19:08:54.162270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dc6aa88d3f4'
down_revision = '812c26ee6f2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_email')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), nullable=True))
        batch_op.create_index('ix_user_email', ['email'], unique=False)

    # ### end Alembic commands ###
