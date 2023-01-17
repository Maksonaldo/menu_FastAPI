"""Database creation2n

Revision ID: 42449af57aa5
Revises: c53502cc417f
Create Date: 2023-01-18 01:19:53.301588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42449af57aa5'
down_revision = 'c53502cc417f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submenu', 'menu_id',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submenu', 'menu_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###