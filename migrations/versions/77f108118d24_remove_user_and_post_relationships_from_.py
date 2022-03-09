"""remove user and post relationships from postvote class and changed user and post backrefs to 'voter' and 'post' respectively

Revision ID: 77f108118d24
Revises: 1e5b79d18a51
Create Date: 2022-03-06 16:15:39.007482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f108118d24'
down_revision = '1e5b79d18a51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('upvote', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_vote_timestamp'), 'post_vote', ['timestamp'], unique=False)
    op.create_foreign_key(None, 'unit', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'unit', type_='foreignkey')
    op.drop_index(op.f('ix_post_vote_timestamp'), table_name='post_vote')
    op.drop_table('post_vote')
    # ### end Alembic commands ###
