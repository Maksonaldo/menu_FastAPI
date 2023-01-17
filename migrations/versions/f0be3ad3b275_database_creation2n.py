"""Database creation2n

Revision ID: f0be3ad3b275
Revises: da7a5352d1e3
Create Date: 2023-01-18 02:50:14.780312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0be3ad3b275'
down_revision = 'da7a5352d1e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dish', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('dish', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('dish', 'price',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('submenu', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('submenu', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('submenu', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('submenu', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('dish', 'price',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('dish', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('dish', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
