"""add Base and Users DB models

Revision ID: 3b853ad76675
Revises: 
Create Date: 2023-12-17 02:28:34.245404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b853ad76675'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('last_seen', sa.Integer(), nullable=False),
    sa.Column('secret_word_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_vk_id'), 'users', ['vk_id'], unique=True)
    op.drop_index('ix_user_vk_id', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('vk_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
    sa.Column('last_seen', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('secret_word_hash', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pk_user')
    )
    op.create_index('ix_user_vk_id', 'user', ['vk_id'], unique=False)
    op.drop_index(op.f('ix_users_vk_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###