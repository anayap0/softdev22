"""merging Anaya and Bhavik's changes

Revision ID: 2b86ab356816
Revises: 718903c7b257, b1ef2bb7e867
Create Date: 2022-02-23 09:37:17.121261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b86ab356816'
down_revision = ('718903c7b257', 'b1ef2bb7e867')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
