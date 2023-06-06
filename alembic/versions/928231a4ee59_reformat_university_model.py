"""reformat university model

Revision ID: 928231a4ee59
Revises: 83a3f2c97e94
Create Date: 2023-06-06 02:28:51.076150

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '928231a4ee59'
down_revision = '83a3f2c97e94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('university', 'short_name')
    op.drop_column('university', 'image')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('university', sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=False))
    op.add_column('university', sa.Column('short_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###