"""Add datetime to audios

Revision ID: b6cae160fc38
Revises: d65450476091
Create Date: 2018-03-17 12:20:30.400668

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b6cae160fc38"
down_revision = "d65450476091"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("audio", sa.Column("audio_dtime", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("audio", "audio_dtime")
    # ### end Alembic commands ###
