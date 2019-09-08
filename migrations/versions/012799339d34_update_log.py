"""update_log

Revision ID: 012799339d34
Revises: 948ce5107c93
Create Date: 2019-09-08 14:21:58.698377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012799339d34'
down_revision = '948ce5107c93'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('log', sa.Column('request_type', sa.String(), nullable=True))
    op.add_column('log', sa.Column('request_url', sa.String(), nullable=True))
    op.drop_constraint('fk_log_request_id_request', 'log', type_='foreignkey')
    op.drop_column('log', 'request_id')
    op.drop_table('request')


def downgrade():
    op.drop_column('log', 'request_url')
    op.drop_column('log', 'request_type')
    op.create_table('request',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_request')
    )
    op.add_column('log', sa.Column('request_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_log_request_id_request', 'log', 'request', ['request_id'], ['id'])
