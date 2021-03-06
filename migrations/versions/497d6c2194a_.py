"""empty message

Revision ID: 497d6c2194a
Revises: 445a81c3851
Create Date: 2015-10-10 18:01:12.594587

"""

# revision identifiers, used by Alembic.
revision = '497d6c2194a'
down_revision = '445a81c3851'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription')
    ### end Alembic commands ###
