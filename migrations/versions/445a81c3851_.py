"""empty message

Revision ID: 445a81c3851
Revises: 46e2e82b373
Create Date: 2015-10-10 17:09:35.932159

"""

# revision identifiers, used by Alembic.
revision = '445a81c3851'
down_revision = '46e2e82b373'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('gcm', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'gcm')
    ### end Alembic commands ###
