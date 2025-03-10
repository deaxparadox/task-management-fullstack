"""otp counter table

Revision ID: 9498ba23054c
Revises: 63eca535177c
Create Date: 2025-02-13 15:48:34.156861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9498ba23054c'
down_revision: Union[str, None] = '63eca535177c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otp',
    sa.Column('counter', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('counter')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('otp')
    # ### end Alembic commands ###
