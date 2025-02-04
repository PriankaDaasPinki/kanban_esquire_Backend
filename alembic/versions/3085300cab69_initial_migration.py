"""Initial migration

Revision ID: 3085300cab69
Revises: 
Create Date: 2025-01-08 19:14:17.718197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3085300cab69'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    op.add_column('project_modules', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_project_modules_created_by'), 'project_modules', ['created_by'], unique=False)
    op.create_foreign_key(None, 'project_modules', 'users', ['created_by'], ['user_id'])
    op.alter_column('projects', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_index(op.f('ix_projects_created_at'), 'projects', ['created_at'], unique=False)
    op.create_index(op.f('ix_projects_description'), 'projects', ['description'], unique=False)
    op.create_index(op.f('ix_projects_owner_id'), 'projects', ['owner_id'], unique=False)
    op.create_index(op.f('ix_projects_project_id'), 'projects', ['project_id'], unique=False)
    op.create_index(op.f('ix_projects_project_name'), 'projects', ['project_name'], unique=False)
    op.drop_constraint('projects_owner_id_fkey', 'projects', type_='foreignkey')
    op.create_foreign_key(None, 'projects', 'users', ['owner_id'], ['user_id'])
    op.add_column('users', sa.Column('first_name', sa.String(length=50), server_default='', nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=50), server_default='', nullable=False))
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=15),
               nullable=False)
    op.alter_column('users', 'password_hash',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('users', 'designation',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.TIMESTAMP(timezone=True),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_designation'), 'users', ['designation'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_last_name'), 'users', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_index(op.f('ix_users_user_image'), 'users', ['user_image'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_user_image'), table_name='users')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_index(op.f('ix_users_last_name'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_designation'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.alter_column('users', 'created_at',
               existing_type=sa.TIMESTAMP(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'designation',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('users', 'password_hash',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
    op.alter_column('users', 'phone',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=25),
               nullable=True)
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_constraint(None, 'projects', type_='foreignkey')
    op.create_foreign_key('projects_owner_id_fkey', 'projects', 'users', ['owner_id'], ['user_id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_projects_project_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_project_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_owner_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_description'), table_name='projects')
    op.drop_index(op.f('ix_projects_created_at'), table_name='projects')
    op.alter_column('projects', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'project_modules', type_='foreignkey')
    op.drop_index(op.f('ix_project_modules_created_by'), table_name='project_modules')
    op.drop_column('project_modules', 'created_by')
    op.create_table('sessions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('session_token', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='sessions_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sessions_pkey'),
    sa.UniqueConstraint('session_token', name='sessions_session_token_key')
    )
    # ### end Alembic commands ###
