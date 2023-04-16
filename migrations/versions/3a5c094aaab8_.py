"""empty message

Revision ID: 3a5c094aaab8
Revises: ce36321b9793
Create Date: 2023-04-12 16:19:28.545463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a5c094aaab8'
down_revision = 'ce36321b9793'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('smi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('smi', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###
