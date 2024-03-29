"""Remove relationship user_post_votes from User

Revision ID: eb0af8454c7d
Revises: 77f108118d24
Create Date: 2022-03-06 16:17:40.416042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb0af8454c7d'
down_revision = '77f108118d24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'unit', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit', type_='foreignkey')
    # ### end Alembic commands ###
