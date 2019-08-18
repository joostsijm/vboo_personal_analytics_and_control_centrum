"""initial_migration

Revision ID: 948ce5107c93
Revises: 
Create Date: 2019-08-18 01:45:56.906214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '948ce5107c93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_request'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('registration_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_table('key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expire_at', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('used_at', sa.DateTime(), nullable=True),
    sa.Column('uses', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_key_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_key'))
    )
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('succes', sa.Boolean(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=True),
    sa.Column('key_id', sa.Integer(), nullable=True),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['key_id'], ['key.id'], name=op.f('fk_log_key_id_key')),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], name=op.f('fk_log_request_id_request')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_log'))
    )


def downgrade():
    op.drop_table('log')
    op.drop_table('key')
    op.drop_table('user')
    op.drop_table('request')
