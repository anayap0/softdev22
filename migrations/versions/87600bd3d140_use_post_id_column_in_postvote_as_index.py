"""Use post_id column in PostVote as index

Revision ID: 87600bd3d140
Revises: eb0af8454c7d
Create Date: 2022-03-12 16:13:47.517133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87600bd3d140'
down_revision = 'eb0af8454c7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_post_vote_timestamp', table_name='post_vote')
    op.create_index(op.f('ix_post_vote_post_id'), 'post_vote', ['post_id'], unique=False)
    op.drop_column('post_vote', 'timestamp')
    op.create_foreign_key(None, 'unit', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit', type_='foreignkey')
    op.add_column('post_vote', sa.Column('timestamp', sa.DATETIME(), nullable=True))
    op.drop_index(op.f('ix_post_vote_post_id'), table_name='post_vote')
    op.create_index('ix_post_vote_timestamp', 'post_vote', ['timestamp'], unique=False)
    # ### end Alembic commands ###
