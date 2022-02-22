"""tags

Revision ID: b1ef2bb7e867
Revises: bdb0160bebce
Create Date: 2022-02-21 19:00:20.058455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1ef2bb7e867'
down_revision = 'bdb0160bebce'
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
