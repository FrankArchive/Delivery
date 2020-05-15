"""empty message

Revision ID: deec9ce7637c
Revises: 8415cda51a97
Create Date: 2020-05-14 09:17:17.080356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deec9ce7637c'
down_revision = '8415cda51a97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courier')
    # ### end Alembic commands ###