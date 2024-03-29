"""Remove menuwelcome table

Revision ID: ca183d2d94d3
Revises: c7c86f035f4d
Create Date: 2020-12-09 13:37:51.733230

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "ca183d2d94d3"
down_revision = "c7c86f035f4d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("menuwelcome")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "menuwelcome",
        sa.Column("menu_id", mysql.VARCHAR(length=12), nullable=False),
        sa.Column("language_code", mysql.VARCHAR(length=4), nullable=False),
        sa.Column("audio_id", mysql.VARCHAR(length=80), nullable=False),
        sa.ForeignKeyConstraint(
            ["audio_id"], ["audio.audio_id"], name="fk_menuwelcome_audio_id_audio"
        ),
        sa.ForeignKeyConstraint(
            ["language_code"],
            ["language.language_code"],
            name="fk_menuwelcome_language_code_language",
        ),
        sa.ForeignKeyConstraint(
            ["menu_id"],
            ["ivrmenu.menu_id"],
            name="fk_menuwelcome_menu_id_ivrmenu",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("menu_id", "language_code"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("ix_menuwelcome_menu_id", "menuwelcome", ["menu_id"], unique=False)
    op.create_index(
        "ix_menuwelcome_language_code", "menuwelcome", ["language_code"], unique=False
    )
    op.create_index(
        "ix_menuwelcome_audio_id", "menuwelcome", ["audio_id"], unique=False
    )
    # ### end Alembic commands ###
