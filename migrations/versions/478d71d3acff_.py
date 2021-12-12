"""empty message

Revision ID: 478d71d3acff
Revises: 
Create Date: 2021-12-07 17:56:47.066708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '478d71d3acff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_club_name'), 'club', ['name'], unique=True)
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('major', sa.String(length=64), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('dateTime', sa.String(length=64), nullable=True),
    sa.Column('address', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('clubID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clubID'], ['club.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_address'), 'event', ['address'], unique=False)
    op.create_index(op.f('ix_event_dateTime'), 'event', ['dateTime'], unique=False)
    op.create_index(op.f('ix_event_name'), 'event', ['name'], unique=False)
    op.create_table('member_to_club',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('memberID', sa.Integer(), nullable=True),
    sa.Column('clubID', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['clubID'], ['club.id'], ),
    sa.ForeignKeyConstraint(['memberID'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('member_to_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('memberID', sa.Integer(), nullable=True),
    sa.Column('eventID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['eventID'], ['event.id'], ),
    sa.ForeignKeyConstraint(['memberID'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_to_event')
    op.drop_table('member_to_club')
    op.drop_index(op.f('ix_event_name'), table_name='event')
    op.drop_index(op.f('ix_event_dateTime'), table_name='event')
    op.drop_index(op.f('ix_event_address'), table_name='event')
    op.drop_table('event')
    op.drop_table('member')
    op.drop_index(op.f('ix_club_name'), table_name='club')
    op.drop_table('club')
    # ### end Alembic commands ###
