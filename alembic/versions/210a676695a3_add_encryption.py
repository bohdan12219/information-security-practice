"""Add field-level encryption for User email and phone

Revision ID: 210a676695a3
Revises: 3a341bf3694b
Create Date: 2026-10-12 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '210a676695a3'
down_revision = '3a341bf3694b'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('encrypted_email', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('email_index', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('encrypted_phone', sa.String(length=500), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_email_index'), ['email_index'], unique=True)
        batch_op.drop_index('ix_users_email')
        batch_op.drop_column('email')

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=100), nullable=True))
        batch_op.create_index('ix_users_email', ['email'], unique=False)
        batch_op.drop_index(batch_op.f('ix_users_email_index'))
        batch_op.drop_column('encrypted_phone')
        batch_op.drop_column('email_index')
        batch_op.drop_column('encrypted_email')


        