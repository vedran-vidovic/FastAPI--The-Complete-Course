"""Create phone number for user column

Revision ID: 711f00acdf30
Revises: 
Create Date: 2023-11-18 20:06:18.232939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '711f00acdf30'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
