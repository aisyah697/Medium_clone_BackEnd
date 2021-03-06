"""empty message

Revision ID: be5196a02848
Revises: dd672e540bb3
Create Date: 2020-05-26 13:50:32.793068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be5196a02848'
down_revision = 'dd672e540bb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('image_caption', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'image_caption')
    # ### end Alembic commands ###
