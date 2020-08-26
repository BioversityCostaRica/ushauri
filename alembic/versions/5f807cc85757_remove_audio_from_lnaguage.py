"""Remove audio from lnaguage

Revision ID: 5f807cc85757
Revises: c7c86f035f4d
Create Date: 2020-08-25 16:52:37.930898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "5f807cc85757"
down_revision = "c7c86f035f4d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_language_audio_id_audio", "language", type_="foreignkey")
    op.drop_index("ix_language_audio_id", table_name="language")
    op.drop_column("language", "audio_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "language", sa.Column("audio_id", mysql.VARCHAR(length=80), nullable=False)
    )
    op.create_foreign_key(
        "fk_language_audio_id_audio", "language", "audio", ["audio_id"], ["audio_id"]
    )
    op.create_index("ix_language_audio_id", "language", ["audio_id"], unique=False)
    # ### end Alembic commands ###
